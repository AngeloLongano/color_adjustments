import argparse
from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

from utils.common.image_io import load_rgb
from utils.lut_pipeline.lut import make_best_lut_summary_image, make_lut17_method_grid


def _read_summary(path: Path) -> pd.DataFrame:
    summary = pd.read_csv(path)
    if "fit_method" not in summary.columns:
        summary["fit_method"] = "mean"
    if "apply_method" not in summary.columns:
        summary["apply_method"] = "trilinear"
    if "variant" not in summary.columns:
        summary["variant"] = summary.apply(
            lambda row: (
                f"lut_{int(row['lut_size'])}_"
                f"{row['fit_method']}_{row['apply_method']}"
            ),
            axis=1,
        )
    if "best_summary_path" not in summary.columns:
        summary["best_summary_path"] = summary["summary_path"].apply(
            lambda path: str(Path(path).with_name("best_summary.png"))
        )
    return summary


def write_lut_rankings(summary_path: Path, output_dir: Path) -> None:
    summary = _read_summary(summary_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    cols = [
        "image_id",
        "prompt_id",
        "variant",
        "fit_method",
        "apply_method",
        "lut_size",
        "rgb_psnr",
        "luma_ssim",
        "delta_e_mean",
        "delta_e_p95",
        "occupied_ratio",
        "summary_path",
        "best_summary_path",
        "reconstruction_path",
        "heatmap_path",
    ]
    best_delta_e = (
        summary.sort_values(["image_id", "prompt_id", "delta_e_mean"])
        .groupby(["image_id", "prompt_id"])
        .head(1)[cols]
    )
    best_psnr = (
        summary.sort_values(
            ["image_id", "prompt_id", "rgb_psnr"],
            ascending=[True, True, False],
        )
        .groupby(["image_id", "prompt_id"])
        .head(1)[cols]
    )
    by_variant = (
        summary.groupby(["lut_size", "fit_method", "apply_method"])[
            ["rgb_psnr", "luma_ssim", "delta_e_mean", "delta_e_p95", "occupied_ratio"]
        ]
        .mean()
        .reset_index()
    )
    by_lut_size = (
        summary.groupby("lut_size")[
            ["rgb_psnr", "luma_ssim", "delta_e_mean", "delta_e_p95", "occupied_ratio"]
        ]
        .mean()
        .reset_index()
    )

    best_delta_e.to_csv(output_dir / "best_by_delta_e.csv", index=False)
    best_psnr.to_csv(output_dir / "best_by_psnr.csv", index=False)
    by_variant.to_csv(output_dir / "metrics_by_variant.csv", index=False)
    by_lut_size.to_csv(output_dir / "metrics_by_lut_size.csv", index=False)


def generate_contact_sheets(
    summary_path: Path,
    output_dir: Path,
    thumb_size: tuple[int, int] = (240, 160),
) -> None:
    summary = _read_summary(summary_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()
    thumb_w, thumb_h = thumb_size
    label_h = 42
    pad = 8
    cols = ["original", "flux_target", "best_lut", "best_error"]

    for image_id, group in summary.groupby("image_id"):
        prompts = sorted(group["prompt_id"].unique())
        sheet_w = len(cols) * thumb_w + (len(cols) + 1) * pad
        sheet_h = len(prompts) * (thumb_h + label_h + pad) + label_h + pad * 2
        sheet = Image.new("RGB", (sheet_w, sheet_h), "white")
        draw = ImageDraw.Draw(sheet)

        for ci, col in enumerate(cols):
            x = pad + ci * (thumb_w + pad)
            draw.text((x, pad), col, fill=(0, 0, 0), font=font)

        for ri, prompt_id in enumerate(prompts):
            row = group[group["prompt_id"] == prompt_id]
            best = row.sort_values("delta_e_mean").iloc[0]
            first = row.iloc[0]
            base_dir = Path(first["reconstruction_path"]).parent
            paths = {
                "original": _first_existing_path(
                    first, "original_copy_path", base_dir / "original_input.png", base_dir / "original.png"
                ),
                "flux_target": _first_existing_path(
                    first, "flux_target_copy_path", base_dir / "flux_target.png", base_dir / "target.png"
                ),
                "best_lut": Path(best["reconstruction_path"]),
                "best_error": Path(best["heatmap_path"]),
            }

            y = pad + label_h + ri * (thumb_h + label_h + pad)
            best_label = (
                f"{prompt_id} | best dE {best['delta_e_mean']} | "
                f"{best['variant']}"
            )
            draw.text((pad, y), best_label, fill=(0, 0, 0), font=font)

            for ci, col in enumerate(cols):
                x = pad + ci * (thumb_w + pad)
                img = Image.open(paths[col]).convert("RGB")
                img.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                canvas = Image.new("RGB", (thumb_w, thumb_h), (245, 245, 245))
                ox = (thumb_w - img.width) // 2
                oy = (thumb_h - img.height) // 2
                canvas.paste(img, (ox, oy))
                sheet.paste(canvas, (x, y + label_h))

        sheet.save(output_dir / f"{image_id}_lut_contact_sheet.jpg", quality=92)


def _is_missing_value(value: object) -> bool:
    if value is None:
        return True
    try:
        return bool(pd.isna(value))
    except TypeError:
        return False


def _first_existing_path(row: pd.Series, column: str, *fallbacks: Path) -> Path:
    value = row.get(column)
    if not _is_missing_value(value):
        path = Path(str(value))
        if path.exists():
            return path
    for fallback in fallbacks:
        if fallback.exists():
            return fallback
    if fallbacks:
        return fallbacks[0]
    raise FileNotFoundError(f"No usable path for column {column}")


def generate_case_summaries(summary_path: Path) -> None:
    summary = _read_summary(summary_path)
    for (image_id, prompt_id), group in summary.groupby(["image_id", "prompt_id"]):
        group = group.sort_values(["lut_size", "fit_method", "apply_method"])
        first = group.iloc[0]
        base_dir = Path(first["reconstruction_path"]).parent

        original_path = _first_existing_path(
            first, "original_copy_path", base_dir / "original_input.png", base_dir / "original.png"
        )
        target_path = _first_existing_path(
            first, "flux_target_copy_path", base_dir / "flux_target.png", base_dir / "target.png"
        )
        summary_output = _first_existing_path(
            first, "summary_path", base_dir / "summary.png"
        )
        best_summary_output = Path(
            first.get("best_summary_path", base_dir / "best_summary.png")
        )

        results = []
        for _, row in group.iterrows():
            metrics = {
                "rgb_mae": row["rgb_mae"],
                "rgb_psnr": row["rgb_psnr"],
                "luma_ssim": row["luma_ssim"],
                "delta_e_mean": row["delta_e_mean"],
                "delta_e_p95": row["delta_e_p95"],
                "occupied_ratio": row["occupied_ratio"],
            }
            results.append(
                {
                    "lut_size": int(row["lut_size"]),
                    "fit_method": row["fit_method"],
                    "apply_method": row["apply_method"],
                    "variant": row["variant"],
                    "reconstruction": load_rgb(Path(row["reconstruction_path"])),
                    "heatmap": load_rgb(Path(row["heatmap_path"])),
                    "metrics": metrics,
                }
            )

        make_lut17_method_grid(
            original=load_rgb(original_path),
            target=load_rgb(target_path),
            results=results,
            output_path=summary_output,
            title=f"LUT vs FLUX - {image_id} / {prompt_id}",
            subtitle="LUT 17: confronto tra metodi di fitting e applicazione.",
        )
        best_result = min(results, key=lambda result: result["metrics"]["delta_e_mean"])
        make_best_lut_summary_image(
            original=load_rgb(original_path),
            target=load_rgb(target_path),
            result=best_result,
            output_path=best_summary_output,
            title=f"Best LUT - {image_id} / {prompt_id}",
            subtitle="Migliore variante selezionata per Delta E medio.",
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate aggregate CSVs and contact sheets from LUT metrics."
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("images_lut/summary_all.csv"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("images_lut"),
    )
    parser.add_argument(
        "--contact-sheet-dir",
        type=Path,
        default=Path("images_lut/contact_sheets"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    write_lut_rankings(args.summary, args.output_dir)
    generate_case_summaries(args.summary)
    generate_contact_sheets(args.summary, args.contact_sheet_dir)
    print(f"Reports written to: {args.output_dir}")
    print(f"Contact sheets written to: {args.contact_sheet_dir}")


if __name__ == "__main__":
    main()
