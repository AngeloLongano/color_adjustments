from __future__ import annotations

import argparse
from pathlib import Path

from utils.data.download import download_images
from utils.flux.generate_targets import (
    DEFAULT_IMAGES_CONFIG,
    DEFAULT_PROMPTS_CONFIG,
    build_run_config,
    run_generation,
)
from utils.flux.flux_grid import build_flux_grid
from utils.lut_pipeline.lut_batch import iter_targets, write_summary
from utils.lut_pipeline.lut_batch import find_original as find_lut_original
from utils.lut_pipeline.lut_batch import prompt_id_for
from utils.lut_pipeline.lut import run_experiment
from utils.data.prepare_images import (
    DEFAULT_TARGET_SIZE,
    prepare_image,
    read_classification_levels,
    read_config_selection,
    selected_image_paths,
    validate_unique_outputs,
    write_manifest,
)
from utils.data.quality import (
    analyze_folder,
    apply_rename_map,
    print_terminal_report,
    rename_images_by_level,
)
from utils.lut_pipeline.reports import (
    generate_case_summaries,
    generate_contact_sheets,
    write_lut_rankings,
)
from utils.flux.target_eval import (
    evaluate_directory,
    print_summary,
    write_csv,
    write_quality_grid,
)
from utils.common.image_io import read_json


CONFIG_PATH = Path("configs/images.yaml")
PROMPTS_PATH = Path("configs/prompts.yaml")
DOWNLOADS_DIR = Path("downloads")
IMAGES_DIR = Path("images")
IMAGES_FLUX_DIR = Path("images_flux")
IMAGES_FLUX_PREVIEW_DIR = IMAGES_FLUX_DIR / "preview"
IMAGES_FLUX_TARGET_DIR = IMAGES_FLUX_DIR / "target"
IMAGES_LUT_DIR = Path("images_lut")


def download_step(overwrite: bool = False) -> list[Path]:
    paths = download_images(
        config_path=CONFIG_PATH,
        output_dir=DOWNLOADS_DIR,
        selection="all",
        overwrite=overwrite,
    )
    print(f"Images ready: {len(paths)}")
    return paths


def classify_step(rename: bool = False) -> None:
    target_resolution = DEFAULT_TARGET_SIZE
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    output_csv = IMAGES_DIR / "classification.csv"
    output_sorted_csv = IMAGES_DIR / "classification_sorted.csv"

    df = analyze_folder(DOWNLOADS_DIR, target_resolution=target_resolution)
    renames = rename_images_by_level(df, DOWNLOADS_DIR) if rename else []
    df = apply_rename_map(df, renames)
    df.to_csv(output_csv, index=False)

    if df.empty:
        df_sorted = df
    else:
        df_sorted = df.sort_values(
            by=["complexity_index", "crop_loss_3_2_%"],
            ascending=[True, True],
        )
    df_sorted.to_csv(output_sorted_csv, index=False)

    print_terminal_report(
        df=df,
        df_sorted=df_sorted,
        output_csv=output_csv,
        output_sorted_csv=output_sorted_csv,
        target_resolution=target_resolution,
        renames=renames,
    )


def prepare_step() -> None:
    image_keys = read_config_selection(CONFIG_PATH, "selected_images")
    levels = read_classification_levels(IMAGES_DIR / "classification.csv")
    selected = selected_image_paths(DOWNLOADS_DIR, image_keys, levels)
    if not selected:
        print(f"No supported images found in {DOWNLOADS_DIR}.")
        return

    validate_unique_outputs(selected, IMAGES_DIR, "png")
    rows = [
        prepare_image(
            image_key=image_key,
            level=level,
            source_path=path,
            output_dir=IMAGES_DIR,
            target_size=DEFAULT_TARGET_SIZE,
            output_format="png",
            jpeg_quality=95,
            dry_run=False,
        )
        for image_key, level, path in selected
    ]
    manifest_path = IMAGES_DIR / "manifest.csv"
    write_manifest(manifest_path, rows)

    print("PREPARAZIONE IMMAGINI")
    print("=" * 80)
    print(f"Input        : {DOWNLOADS_DIR}")
    print(f"Output       : {IMAGES_DIR}")
    print("Formato      : png")
    print(f"Target size  : {DEFAULT_TARGET_SIZE[0]}x{DEFAULT_TARGET_SIZE[1]}")
    print(f"Selection    : selected_images ({CONFIG_PATH})")
    print(f"Classif. CSV : {IMAGES_DIR / 'classification.csv'}")
    print(f"Immagini     : {len(rows)}")
    print(f"Manifest     : {manifest_path}")
    print()

    for row in rows:
        print(
            f"- {row.source_file} -> {row.output_file} "
            f"({row.source_width}x{row.source_height} -> "
            f"crop {row.crop_width}x{row.crop_height} -> "
            f"{row.target_width}x{row.target_height})"
        )


def flux_step(run_type: str | None = None) -> None:
    args = argparse.Namespace(
        run_type=run_type,
        models=None,
        prompts=None,
        images=None,
        images_config=CONFIG_PATH,
        prompts_config=PROMPTS_PATH,
        image_selection="selected_images",
    )
    run_config, prompt_dict = build_run_config(args)
    run_generation(run_config, prompt_dict)


def evaluate_step(
    experiments_dir: Path,
    output: Path,
    quality_grid_output: Path | None = None,
) -> None:
    rows = evaluate_directory(experiments_dir, IMAGES_DIR)
    write_csv(rows, output)
    if quality_grid_output is not None:
        write_quality_grid(
            rows,
            quality_grid_output,
            images_config=CONFIG_PATH,
            originals_dir=IMAGES_DIR,
        )
    print_summary(rows)
    print(f"\nCSV written to: {output}")
    if quality_grid_output is not None:
        print(f"Quality grid written to: {quality_grid_output}")


def flux_grid_step(
    flux_dir: Path = IMAGES_FLUX_PREVIEW_DIR,
    output_path: Path | None = None,
) -> None:
    if output_path is None:
        output_path = flux_dir.parent / f"{flux_dir.name}_grid.jpg"
    missing = build_flux_grid(
        images_config=CONFIG_PATH,
        input_dir=IMAGES_DIR,
        flux_dir=flux_dir,
        output_path=output_path,
    )
    print(f"Flux grid written to: {output_path}")
    if missing:
        print(f"Missing files/placeholders: {len(missing)}")
        for path in missing:
            print(f"- {path}")


def lut_step() -> None:
    all_rows = []
    targets = list(iter_targets(IMAGES_FLUX_TARGET_DIR))

    for index, target_path in enumerate(targets, start=1):
        metadata = read_json(target_path.with_suffix(".json"))
        image_id = target_path.parent.name
        prompt_id = prompt_id_for(target_path, metadata)
        original_path = find_lut_original(target_path, metadata, IMAGES_DIR)
        output_dir = IMAGES_LUT_DIR / image_id / prompt_id

        print(f"[{index}/{len(targets)}] {image_id}/{prompt_id}")
        rows = run_experiment(
            original_path=original_path,
            target_path=target_path,
            output_dir=output_dir,
            lut_sizes=[17, 33, 65],
            sample_count=200000,
            seed=0,
            save_arrays=False,
        )

        for row in rows:
            all_rows.append(
                {
                    "image_id": image_id,
                    "prompt_id": prompt_id,
                    "target_path": str(target_path),
                    **row,
                }
            )

    summary = IMAGES_LUT_DIR / "summary_all.csv"
    write_summary(summary, all_rows)
    print(f"Summary written to: {summary}")


def report_step() -> None:
    summary = IMAGES_LUT_DIR / "summary_all.csv"
    contact_sheet_dir = IMAGES_LUT_DIR / "contact_sheets"
    write_lut_rankings(summary, IMAGES_LUT_DIR)
    generate_case_summaries(summary)
    generate_contact_sheets(summary, contact_sheet_dir)
    print(f"Reports written to: {IMAGES_LUT_DIR}")
    print(f"Contact sheets written to: {contact_sheet_dir}")


def pipeline(include_flux: bool = False) -> None:
    download_step()
    classify_step()
    prepare_step()
    if include_flux:
        flux_step(run_type="targets")
        evaluate_step(IMAGES_FLUX_TARGET_DIR, IMAGES_FLUX_DIR / "i2i_quality_targets.csv")
        lut_step()
        report_step()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Color adjustments experiment pipeline.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("download")
    classify_parser = subparsers.add_parser("classify")
    classify_parser.add_argument("--rename", action="store_true")
    subparsers.add_parser("prepare")
    subparsers.add_parser("generate-previews")
    subparsers.add_parser("generate-targets")
    subparsers.add_parser("evaluate-preview")
    subparsers.add_parser("evaluate-targets")
    flux_grid_parser = subparsers.add_parser("flux-grid")
    flux_grid_parser.add_argument("--flux-dir", type=Path, default=IMAGES_FLUX_PREVIEW_DIR)
    flux_grid_parser.add_argument("--output", type=Path)
    subparsers.add_parser("lut")
    subparsers.add_parser("report")
    pipeline_parser = subparsers.add_parser("pipeline")
    pipeline_parser.add_argument("--include-flux", action="store_true")

    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command == "download":
        download_step()
    elif args.command == "classify":
        classify_step(rename=args.rename)
    elif args.command == "prepare":
        prepare_step()
    elif args.command == "generate-previews":
        flux_step(run_type="preview")
    elif args.command == "generate-targets":
        flux_step(run_type="targets")
    elif args.command == "evaluate-preview":
        evaluate_step(
            IMAGES_FLUX_PREVIEW_DIR,
            IMAGES_FLUX_DIR / "i2i_quality_preview.csv",
        )
    elif args.command == "evaluate-targets":
        evaluate_step(
            IMAGES_FLUX_TARGET_DIR,
            IMAGES_FLUX_DIR / "i2i_quality_targets.csv",
            IMAGES_FLUX_DIR / "i2i_quality_targets_grid.jpg",
        )
    elif args.command == "flux-grid":
        flux_grid_step(flux_dir=args.flux_dir, output_path=args.output)
    elif args.command == "lut":
        lut_step()
    elif args.command == "report":
        report_step()
    elif args.command == "pipeline":
        pipeline(include_flux=args.include_flux)


if __name__ == "__main__":
    main()
