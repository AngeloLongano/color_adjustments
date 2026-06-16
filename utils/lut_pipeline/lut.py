import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.common.image_io import load_rgb, save_rgb, resize_to, write_json
from utils.common.metrics import delta_e_76, psnr, rgb_to_luma, simple_ssim


def identity_lut(size: int) -> np.ndarray:
    axis = np.linspace(0.0, 1.0, size, dtype=np.float32)
    r, g, b = np.meshgrid(axis, axis, axis, indexing="ij")
    return np.stack([r, g, b], axis=-1)


def fit_lut_mean(
    original: np.ndarray,
    target: np.ndarray,
    size: int,
    sample_count: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    pixels_in = original.reshape(-1, 3)
    pixels_out = target.reshape(-1, 3)
    total_pixels = pixels_in.shape[0]

    if sample_count > 0 and sample_count < total_pixels:
        rng = np.random.default_rng(seed)
        sample_idx = rng.choice(total_pixels, size=sample_count, replace=False)
        pixels_in = pixels_in[sample_idx]
        pixels_out = pixels_out[sample_idx]

    node_idx = np.rint(np.clip(pixels_in, 0.0, 1.0) * (size - 1)).astype(np.int32)
    flat_idx = (node_idx[:, 0] * size + node_idx[:, 1]) * size + node_idx[:, 2]

    sums = np.zeros((size * size * size, 3), dtype=np.float64)
    counts = np.zeros(size * size * size, dtype=np.int64)
    np.add.at(sums, flat_idx, pixels_out)
    np.add.at(counts, flat_idx, 1)

    lut = identity_lut(size).reshape(-1, 3).astype(np.float64)
    occupied = counts > 0
    lut[occupied] = sums[occupied] / counts[occupied, None]
    return lut.reshape(size, size, size, 3).astype(np.float32), counts.reshape(
        size, size, size
    )


def apply_lut_trilinear(image: np.ndarray, lut: np.ndarray) -> np.ndarray:
    size = lut.shape[0]
    coords = np.clip(image, 0.0, 1.0) * (size - 1)
    lo = np.floor(coords).astype(np.int32)
    hi = np.clip(lo + 1, 0, size - 1)
    frac = coords - lo

    r0, g0, b0 = lo[..., 0], lo[..., 1], lo[..., 2]
    r1, g1, b1 = hi[..., 0], hi[..., 1], hi[..., 2]
    fr, fg, fb = frac[..., 0:1], frac[..., 1:2], frac[..., 2:3]

    c000 = lut[r0, g0, b0]
    c001 = lut[r0, g0, b1]
    c010 = lut[r0, g1, b0]
    c011 = lut[r0, g1, b1]
    c100 = lut[r1, g0, b0]
    c101 = lut[r1, g0, b1]
    c110 = lut[r1, g1, b0]
    c111 = lut[r1, g1, b1]

    c00 = c000 * (1.0 - fb) + c001 * fb
    c01 = c010 * (1.0 - fb) + c011 * fb
    c10 = c100 * (1.0 - fb) + c101 * fb
    c11 = c110 * (1.0 - fb) + c111 * fb
    c0 = c00 * (1.0 - fg) + c01 * fg
    c1 = c10 * (1.0 - fg) + c11 * fg
    return np.clip(c0 * (1.0 - fr) + c1 * fr, 0.0, 1.0).astype(np.float32)


def error_heatmap(target: np.ndarray, reconstruction: np.ndarray) -> np.ndarray:
    delta_e = delta_e_76(target, reconstruction)
    scale = np.percentile(delta_e, 99)
    if scale <= 0:
        scale = 1.0
    norm = np.clip(delta_e / scale, 0.0, 1.0)

    heat = np.zeros((*norm.shape, 3), dtype=np.float32)
    heat[..., 0] = norm
    heat[..., 1] = np.clip(1.0 - np.abs(norm - 0.5) * 2.0, 0.0, 1.0)
    heat[..., 2] = 1.0 - norm
    return heat


def _to_pil(image: np.ndarray) -> Image.Image:
    data = np.clip(np.rint(image * 255.0), 0, 255).astype(np.uint8)
    return Image.fromarray(data, mode="RGB")


def _load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    names = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        if bold
        else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


def _fit_on_canvas(image: np.ndarray, size: tuple[int, int]) -> Image.Image:
    thumb = _to_pil(image)
    thumb.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, (244, 244, 244))
    offset = ((size[0] - thumb.width) // 2, (size[1] - thumb.height) // 2)
    canvas.paste(thumb, offset)
    return canvas


def _text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def _draw_wrapped_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    max_width: int,
    line_spacing: int = 4,
) -> int:
    x, y = xy
    lines: list[str] = []
    for raw_line in text.splitlines():
        words = raw_line.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            candidate = f"{line} {word}"
            if _text_width(draw, candidate, font) <= max_width:
                line = candidate
            else:
                lines.append(line)
                line = word
        lines.append(line)

    line_h = draw.textbbox((0, 0), "Ag", font=font)[3]
    for line in lines:
        draw.text((x, y), line, fill=fill, font=font)
        y += line_h + line_spacing
    return y


def make_lut_summary_image(
    original: np.ndarray,
    target: np.ndarray,
    results: list[dict],
    output_path: Path,
    title: str,
    subtitle: str = "",
) -> None:
    """Create a visual sheet comparing Flux target, LUT reconstructions and errors."""
    if not results:
        return

    thumb_w, thumb_h = 276, 184
    pad = 22
    gap = 12
    label_h = 74
    title_h = 92
    cols = 2 + len(results)
    sheet_w = pad * 2 + cols * thumb_w + (cols - 1) * gap
    sheet_h = title_h + pad + 2 * (label_h + thumb_h) + gap + pad

    sheet = Image.new("RGB", (sheet_w, sheet_h), (252, 252, 252))
    draw = ImageDraw.Draw(sheet)
    title_font = _load_font(28, bold=True)
    subtitle_font = _load_font(15)
    label_font = _load_font(17, bold=True)
    metric_font = _load_font(13)

    draw.text((pad, 24), title, fill=(20, 20, 20), font=title_font)
    if subtitle:
        _draw_wrapped_text(
            draw,
            (pad, 60),
            subtitle,
            subtitle_font,
            (75, 75, 75),
            sheet_w - pad * 2,
        )

    y1 = title_h + pad
    y2 = y1 + label_h + thumb_h + gap

    top_items = [
        {
            "title": "Originale input",
            "metrics": "Foto di partenza usata come input image-to-image.",
            "image": original,
        },
        {
            "title": "Target FLUX",
            "metrics": "Riferimento da approssimare con una LUT globale.",
            "image": target,
        },
    ]
    for result in results:
        metrics = result["metrics"]
        top_items.append(
            {
                "title": f"LUT {result['lut_size']}",
                "metrics": (
                    f"PSNR {metrics['rgb_psnr']} | SSIM {metrics['luma_ssim']}\n"
                    f"dE mean {metrics['delta_e_mean']} | p95 {metrics['delta_e_p95']}"
                ),
                "image": result["reconstruction"],
            }
        )

    bottom_items = [
        {
            "title": "Originale vs FLUX",
            "metrics": "Mostra quanto il diffusion target si discosta dall'input.",
            "image": error_heatmap(target, original),
        },
        {
            "title": "Legenda errori",
            "metrics": (
                "Le heatmap a destra misurano l'errore LUT vs FLUX.\n"
                "Blu = basso, verde = medio, rosso = alto."
            ),
            "image": None,
        },
    ]
    for result in results:
        metrics = result["metrics"]
        bottom_items.append(
            {
                "title": f"Errore LUT {result['lut_size']}",
                "metrics": (
                    f"RGB MAE {metrics['rgb_mae']} px | "
                    f"celle {metrics['occupied_ratio']}"
                ),
                "image": result["heatmap"],
            }
        )

    def draw_item(item: dict, col: int, y: int) -> None:
        x = pad + col * (thumb_w + gap)
        draw.rounded_rectangle(
            (x, y, x + thumb_w, y + label_h + thumb_h),
            radius=6,
            fill=(255, 255, 255),
            outline=(224, 224, 224),
        )
        draw.text((x + 10, y + 9), item["title"], fill=(22, 22, 22), font=label_font)
        if item["image"] is not None:
            _draw_wrapped_text(
                draw,
                (x + 10, y + 35),
                item["metrics"],
                metric_font,
                (80, 80, 80),
                thumb_w - 20,
                line_spacing=2,
            )
        image_y = y + label_h
        if item["image"] is None:
            draw.rectangle(
                (x, image_y, x + thumb_w, image_y + thumb_h),
                fill=(246, 246, 246),
                outline=(232, 232, 232),
            )
            _draw_wrapped_text(
                draw,
                (x + 18, image_y + 26),
                item["metrics"],
                metric_font,
                (70, 70, 70),
                thumb_w - 36,
            )
        else:
            sheet.paste(_fit_on_canvas(item["image"], (thumb_w, thumb_h)), (x, image_y))

    for col, item in enumerate(top_items):
        draw_item(item, col, y1)
    for col, item in enumerate(bottom_items):
        draw_item(item, col, y2)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)


def compute_metrics(target: np.ndarray, reconstruction: np.ndarray) -> dict:
    delta_e = delta_e_76(target, reconstruction)
    rgb_abs = np.abs(target - reconstruction)
    luma_target = rgb_to_luma(target)
    luma_reconstruction = rgb_to_luma(reconstruction)
    return {
        "rgb_mae": round(float(rgb_abs.mean() * 255.0), 3),
        "rgb_psnr": round(psnr(target, reconstruction), 3),
        "luma_ssim": round(simple_ssim(luma_target, luma_reconstruction), 4),
        "delta_e_mean": round(float(delta_e.mean()), 3),
        "delta_e_median": round(float(np.median(delta_e)), 3),
        "delta_e_p95": round(float(np.percentile(delta_e, 95)), 3),
    }


def write_metrics(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def cleanup_previous_outputs(output_dir: Path, save_arrays: bool) -> None:
    generated_patterns = [
        "original.png",
        "target.png",
        "metadata.json",
        "diffusion_target_metadata.json",
        "lut_*_baseline.png",
        "lut_*_baseline_deltae_heatmap.png",
        "lut_*_baseline.npy",
        "lut_*_counts.npy",
    ]
    if not save_arrays:
        generated_patterns.extend(["data/lut_*.npy", "data/lut_*_counts.npy"])

    for pattern in generated_patterns:
        for path in output_dir.glob(pattern):
            if path.is_file():
                path.unlink()


def run_experiment(
    original_path: Path,
    target_path: Path,
    output_dir: Path,
    lut_sizes: list[int],
    sample_count: int,
    seed: int,
    save_arrays: bool = False,
) -> list[dict]:
    original = load_rgb(original_path)
    target = load_rgb(target_path)
    height, width = target.shape[:2]
    if original.shape[:2] != target.shape[:2]:
        original = resize_to(original, width, height)

    output_dir.mkdir(parents=True, exist_ok=True)
    cleanup_previous_outputs(output_dir, save_arrays=save_arrays)

    original_copy_path = output_dir / "original_input.png"
    target_copy_path = output_dir / "flux_target.png"
    summary_path = output_dir / "summary.png"
    save_rgb(original_copy_path, original)
    save_rgb(target_copy_path, target)

    rows = []
    visual_results = []
    metadata = {
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source_original_path": str(original_path),
        "source_flux_target_path": str(target_path),
        "output_original_copy_path": str(original_copy_path),
        "output_flux_target_copy_path": str(target_copy_path),
        "output_dir": str(output_dir),
        "width": width,
        "height": height,
        "sample_count": sample_count,
        "seed": seed,
        "method": "baseline_mean_nearest_node_identity_empty_trilinear_apply",
        "lut_sizes": lut_sizes,
        "arrays_saved": save_arrays,
    }

    target_metadata_path = target_path.with_suffix(".json")
    if target_metadata_path.exists():
        metadata["target_metadata"] = json.loads(
            target_metadata_path.read_text(encoding="utf-8")
        )

    for size in lut_sizes:
        lut, counts = fit_lut_mean(original, target, size, sample_count, seed)
        reconstruction = apply_lut_trilinear(original, lut)
        heatmap = error_heatmap(target, reconstruction)

        reconstruction_path = output_dir / f"lut_{size}_reconstruction.png"
        heatmap_path = output_dir / f"lut_{size}_error_vs_flux.png"

        save_rgb(reconstruction_path, reconstruction)
        save_rgb(heatmap_path, heatmap)

        lut_data_path = ""
        counts_data_path = ""
        if save_arrays:
            data_dir = output_dir / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            lut_path = data_dir / f"lut_{size}.npy"
            counts_path = data_dir / f"lut_{size}_counts.npy"
            np.save(lut_path, lut)
            np.save(counts_path, counts)
            lut_data_path = str(lut_path)
            counts_data_path = str(counts_path)

        occupied_cells = int(np.count_nonzero(counts))
        total_cells = int(counts.size)
        occupied_ratio = occupied_cells / total_cells
        samples_per_occupied = (
            float(counts.sum() / occupied_cells) if occupied_cells else 0.0
        )
        metrics = {
            **compute_metrics(target, reconstruction),
            "occupied_ratio": round(occupied_ratio, 5),
        }
        row = {
            "method": "baseline_mean",
            "lut_size": size,
            "sample_count": int(min(sample_count, original.reshape(-1, 3).shape[0])),
            "occupied_cells": occupied_cells,
            "total_cells": total_cells,
            "occupied_ratio": metrics["occupied_ratio"],
            "samples_per_occupied_cell": round(samples_per_occupied, 3),
            **metrics,
            "original_copy_path": str(original_copy_path),
            "flux_target_copy_path": str(target_copy_path),
            "reconstruction_path": str(reconstruction_path),
            "heatmap_path": str(heatmap_path),
            "summary_path": str(summary_path),
            "lut_data_path": lut_data_path,
            "counts_data_path": counts_data_path,
        }
        rows.append(row)
        visual_results.append(
            {
                "lut_size": size,
                "reconstruction": reconstruction,
                "heatmap": heatmap,
                "metrics": metrics,
            }
        )

    write_metrics(output_dir / "metrics.csv", rows)
    write_json(output_dir / "data" / "experiment_metadata.json", metadata)
    prompt_label = metadata.get("target_metadata", {}).get("prompt_key", target_path.stem)
    make_lut_summary_image(
        original=original,
        target=target,
        results=visual_results,
        output_path=summary_path,
        title=f"LUT vs FLUX - {target_path.parent.name} / {prompt_label}",
        subtitle="Confronto tra target diffusion e ricostruzioni ottenute con LUT globali.",
    )

    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fit and apply baseline 3D LUTs for a prepared original/target pair."
    )
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--lut-sizes", type=int, nargs="+", default=[17, 33])
    parser.add_argument("--sample-count", type=int, default=200000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--save-arrays",
        action="store_true",
        help="Save fitted LUT/count arrays under data/. Disabled by default to keep outputs readable.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = run_experiment(
        original_path=args.original,
        target_path=args.target,
        output_dir=args.output_dir,
        lut_sizes=args.lut_sizes,
        sample_count=args.sample_count,
        seed=args.seed,
        save_arrays=args.save_arrays,
    )
    for row in rows:
        print(
            f"lut={row['lut_size']} "
            f"psnr={row['rgb_psnr']} "
            f"ssim={row['luma_ssim']} "
            f"dE_mean={row['delta_e_mean']} "
            f"occupied={row['occupied_ratio']}"
        )
    print(f"Output written to: {args.output_dir}")
