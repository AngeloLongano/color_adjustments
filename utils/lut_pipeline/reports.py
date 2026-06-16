import argparse
from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

from utils.common.image_io import load_rgb
from utils.lut_pipeline.lut import make_lut_summary_image


def write_lut_rankings(summary_path: Path, output_dir: Path) -> None:
    summary = pd.read_csv(summary_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    cols = [
        "image_id",
        "prompt_id",
        "lut_size",
        "rgb_psnr",
        "luma_ssim",
        "delta_e_mean",
        "delta_e_p95",
        "occupied_ratio",
        "summary_path",
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
    by_lut_size = (
        summary.groupby("lut_size")[
            ["rgb_psnr", "luma_ssim", "delta_e_mean", "delta_e_p95", "occupied_ratio"]
        ]
        .mean()
        .reset_index()
    )

    best_delta_e.to_csv(output_dir / "best_by_delta_e.csv", index=False)
    best_psnr.to_csv(output_dir / "best_by_psnr.csv", index=False)
    by_lut_size.to_csv(output_dir / "metrics_by_lut_size.csv", index=False)


def generate_contact_sheets(
    summary_path: Path,
    output_dir: Path,
    lut_sizes: tuple[int, ...] = (17, 33, 65),
    thumb_size: tuple[int, int] = (240, 160),
) -> None:
    summary = pd.read_csv(summary_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()
    thumb_w, thumb_h = thumb_size
    label_h = 24
    pad = 8
    heatmap_lut = lut_sizes[-1]
    cols = ["original", "flux_target", *[f"lut_{size}" for size in lut_sizes], f"error_{heatmap_lut}"]

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
            by_size = {int(item["lut_size"]): item for _, item in row.iterrows()}
            first = row.iloc[0]
            heatmap_row = by_size[heatmap_lut]
            base_dir = Path(first["reconstruction_path"]).parent
            paths = {
                "original": _first_existing_path(
                    first, "original_copy_path", base_dir / "original_input.png", base_dir / "original.png"
                ),
                "flux_target": _first_existing_path(
                    first, "flux_target_copy_path", base_dir / "flux_target.png", base_dir / "target.png"
                ),
                f"error_{heatmap_lut}": Path(heatmap_row["heatmap_path"]),
            }
            for size in lut_sizes:
                paths[f"lut_{size}"] = Path(by_size[size]["reconstruction_path"])

            y = pad + label_h + ri * (thumb_h + label_h + pad)
            draw.text((pad, y), prompt_id, fill=(0, 0, 0), font=font)

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
    summary = pd.read_csv(summary_path)
    for (image_id, prompt_id), group in summary.groupby(["image_id", "prompt_id"]):
        group = group.sort_values("lut_size")
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
                    "reconstruction": load_rgb(Path(row["reconstruction_path"])),
                    "heatmap": load_rgb(Path(row["heatmap_path"])),
                    "metrics": metrics,
                }
            )

        make_lut_summary_image(
            original=load_rgb(original_path),
            target=load_rgb(target_path),
            results=results,
            output_path=summary_output,
            title=f"LUT vs FLUX - {image_id} / {prompt_id}",
            subtitle="Confronto tra target diffusion e ricostruzioni ottenute con LUT globali.",
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
