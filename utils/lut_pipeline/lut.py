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
from utils.common.metrics import delta_e_2000, psnr, ssim_metric

DEFAULT_FIT_METHODS = ["mean", "median", "weighted_mean"]
DEFAULT_APPLY_METHODS = ["nearest", "trilinear"]


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


def _sample_pixel_pairs(
    original: np.ndarray,
    target: np.ndarray,
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
    return pixels_in, pixels_out


def _nearest_node_indices(pixels_in: np.ndarray, size: int) -> tuple[np.ndarray, np.ndarray]:
    node_idx = np.rint(np.clip(pixels_in, 0.0, 1.0) * (size - 1)).astype(np.int32)
    flat_idx = (node_idx[:, 0] * size + node_idx[:, 1]) * size + node_idx[:, 2]
    return node_idx, flat_idx


def fit_lut_median(
    original: np.ndarray,
    target: np.ndarray,
    size: int,
    sample_count: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    pixels_in, pixels_out = _sample_pixel_pairs(original, target, sample_count, seed)
    _, flat_idx = _nearest_node_indices(pixels_in, size)

    lut = identity_lut(size).reshape(-1, 3).astype(np.float64)
    counts = np.bincount(flat_idx, minlength=size * size * size).astype(np.int64)
    occupied = np.flatnonzero(counts)

    order = np.argsort(flat_idx)
    sorted_idx = flat_idx[order]
    sorted_out = pixels_out[order]
    starts = np.searchsorted(sorted_idx, occupied, side="left")
    stops = np.searchsorted(sorted_idx, occupied, side="right")
    for node, start, stop in zip(occupied, starts, stops):
        lut[node] = np.median(sorted_out[start:stop], axis=0)

    return lut.reshape(size, size, size, 3).astype(np.float32), counts.reshape(
        size, size, size
    )


def fit_lut_weighted_mean(
    original: np.ndarray,
    target: np.ndarray,
    size: int,
    sample_count: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    pixels_in, pixels_out = _sample_pixel_pairs(original, target, sample_count, seed)
    coords = np.clip(pixels_in, 0.0, 1.0) * (size - 1)
    lo = np.floor(coords).astype(np.int32)
    hi = np.clip(lo + 1, 0, size - 1)
    frac = coords - lo

    sums = np.zeros((size * size * size, 3), dtype=np.float64)
    weights = np.zeros(size * size * size, dtype=np.float64)
    counts = np.zeros(size * size * size, dtype=np.int64)

    for dr in (0, 1):
        r = hi[:, 0] if dr else lo[:, 0]
        wr = frac[:, 0] if dr else 1.0 - frac[:, 0]
        for dg in (0, 1):
            g = hi[:, 1] if dg else lo[:, 1]
            wg = frac[:, 1] if dg else 1.0 - frac[:, 1]
            for db in (0, 1):
                b = hi[:, 2] if db else lo[:, 2]
                wb = frac[:, 2] if db else 1.0 - frac[:, 2]
                weight = wr * wg * wb
                flat_idx = (r * size + g) * size + b
                weighted_out = pixels_out * weight[:, None]
                np.add.at(sums, flat_idx, weighted_out)
                np.add.at(weights, flat_idx, weight)
                np.add.at(counts, flat_idx, weight > 0)

    lut = identity_lut(size).reshape(-1, 3).astype(np.float64)
    occupied = weights > 0
    lut[occupied] = sums[occupied] / weights[occupied, None]
    return lut.reshape(size, size, size, 3).astype(np.float32), counts.reshape(
        size, size, size
    )


def fit_lut(
    original: np.ndarray,
    target: np.ndarray,
    size: int,
    sample_count: int,
    seed: int,
    fit_method: str,
) -> tuple[np.ndarray, np.ndarray]:
    if fit_method == "mean":
        return fit_lut_mean(original, target, size, sample_count, seed)
    if fit_method == "median":
        return fit_lut_median(original, target, size, sample_count, seed)
    if fit_method == "weighted_mean":
        return fit_lut_weighted_mean(original, target, size, sample_count, seed)
    raise ValueError(f"Unknown LUT fit method: {fit_method}")


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


def apply_lut_nearest(image: np.ndarray, lut: np.ndarray) -> np.ndarray:
    size = lut.shape[0]
    node_idx = np.rint(np.clip(image, 0.0, 1.0) * (size - 1)).astype(np.int32)
    return np.clip(
        lut[node_idx[..., 0], node_idx[..., 1], node_idx[..., 2]], 0.0, 1.0
    ).astype(np.float32)


def apply_lut(image: np.ndarray, lut: np.ndarray, apply_method: str) -> np.ndarray:
    if apply_method == "nearest":
        return apply_lut_nearest(image, lut)
    if apply_method == "trilinear":
        return apply_lut_trilinear(image, lut)
    raise ValueError(f"Unknown LUT apply method: {apply_method}")


def error_heatmap(target: np.ndarray, reconstruction: np.ndarray) -> np.ndarray:
    delta_e = delta_e_2000(target, reconstruction)
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


def _zoom_crop_on_canvas(
    image: np.ndarray,
    crop_box: tuple[int, int, int, int],
    size: tuple[int, int],
) -> Image.Image:
    crop = _to_pil(image).crop(crop_box)
    return crop.resize(size, Image.Resampling.NEAREST)


def _best_disagreement_crop(
    results: list[dict],
    aspect_ratio: float,
) -> tuple[int, int, int, int]:
    reconstructions = [result["reconstruction"] for result in results]
    if not reconstructions:
        return (0, 0, 1, 1)

    stack = np.stack(reconstructions, axis=0)
    height, width = stack.shape[1:3]
    mean = stack.mean(axis=0, keepdims=True)
    score = np.mean(np.abs(stack - mean), axis=(0, 3))

    crop_w = min(max(width // 6, 96), width)
    crop_h = min(max(int(round(crop_w / aspect_ratio)), 64), height)
    crop_w = min(crop_w, max(1, int(round(crop_h * aspect_ratio))))

    if crop_w >= width or crop_h >= height:
        return (0, 0, width, height)

    integral = np.pad(score, ((1, 0), (1, 0)), mode="constant")
    integral = integral.cumsum(axis=0).cumsum(axis=1)
    window_sums = (
        integral[crop_h:, crop_w:]
        - integral[:-crop_h, crop_w:]
        - integral[crop_h:, :-crop_w]
        + integral[:-crop_h, :-crop_w]
    )
    y, x = np.unravel_index(np.argmax(window_sums), window_sums.shape)
    return (int(x), int(y), int(x + crop_w), int(y + crop_h))


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

    thumb_w, thumb_h = 220, 146
    pad = 22
    gap = 12
    title_h = 96
    overview_h = 208
    header_h = 34
    row_h = thumb_h + 28
    variant_w = 205
    metrics_w = 230
    image_w = thumb_w
    error_w = thumb_w
    sheet_w = pad * 2 + variant_w + image_w + error_w + metrics_w + gap * 3
    sheet_h = title_h + overview_h + header_h + len(results) * row_h + pad

    sheet = Image.new("RGB", (sheet_w, sheet_h), (252, 252, 252))
    draw = ImageDraw.Draw(sheet)
    title_font = _load_font(28, bold=True)
    subtitle_font = _load_font(15)
    label_font = _load_font(16, bold=True)
    metric_font = _load_font(13)
    small_font = _load_font(12)

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

    overview_y = title_h
    overview_items = [
        ("Originale input", original, "Foto di partenza."),
        ("Target FLUX", target, "Riferimento da approssimare."),
        (
            "Originale vs FLUX",
            error_heatmap(target, original),
            "Errore tra input e target.",
        ),
    ]
    overview_thumb = (260, 174)
    for col, (label, image, note) in enumerate(overview_items):
        x = pad + col * (overview_thumb[0] + gap)
        draw.rounded_rectangle(
            (x, overview_y, x + overview_thumb[0], overview_y + overview_h - 16),
            radius=6,
            fill=(255, 255, 255),
            outline=(224, 224, 224),
        )
        draw.text((x + 10, overview_y + 8), label, fill=(22, 22, 22), font=label_font)
        draw.text((x + 10, overview_y + 31), note, fill=(80, 80, 80), font=small_font)
        sheet.paste(_fit_on_canvas(image, overview_thumb), (x, overview_y + 52))

    table_y = title_h + overview_h
    x_variant = pad
    x_reconstruction = x_variant + variant_w + gap
    x_heatmap = x_reconstruction + image_w + gap
    x_metrics = x_heatmap + error_w + gap
    headers = [
        (x_variant, "Variante LUT"),
        (x_reconstruction, "Ricostruzione"),
        (x_heatmap, "Errore vs FLUX"),
        (x_metrics, "Metriche"),
    ]
    for x, label in headers:
        draw.text((x, table_y + 8), label, fill=(25, 25, 25), font=label_font)

    for row_index, result in enumerate(results):
        y = table_y + header_h + row_index * row_h
        fill = (255, 255, 255) if row_index % 2 == 0 else (248, 248, 248)
        draw.rounded_rectangle(
            (pad - 8, y, sheet_w - pad + 8, y + row_h - 8),
            radius=6,
            fill=fill,
            outline=(228, 228, 228),
        )

        variant = result.get("variant", f"lut_{result['lut_size']}")
        variant_text = (
            f"{variant}\n"
            f"size {result['lut_size']}\n"
            f"fit: {result.get('fit_method', '-')}\n"
            f"apply: {result.get('apply_method', '-')}"
        )
        _draw_wrapped_text(
            draw,
            (x_variant, y + 16),
            variant_text,
            metric_font,
            (40, 40, 40),
            variant_w,
            line_spacing=2,
        )

        sheet.paste(
            _fit_on_canvas(result["reconstruction"], (image_w, thumb_h)),
            (x_reconstruction, y + 10),
        )
        sheet.paste(
            _fit_on_canvas(result["heatmap"], (error_w, thumb_h)),
            (x_heatmap, y + 10),
        )

        metrics = result["metrics"]
        metric_text = (
            f"PSNR: {metrics['rgb_psnr']}\n"
            f"SSIM: {metrics['ssim']}\n"
            f"Delta E mean: {metrics['delta_e_mean']}\n"
            f"Delta E p95: {metrics['delta_e_p95']}\n"
            f"RGB MAE: {metrics['rgb_mae']} px\n"
            f"Occupied: {metrics['occupied_ratio']}"
        )
        _draw_wrapped_text(
            draw,
            (x_metrics, y + 16),
            metric_text,
            metric_font,
            (55, 55, 55),
            metrics_w,
            line_spacing=2,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)


def make_lut17_method_grid(
    original: np.ndarray,
    target: np.ndarray,
    results: list[dict],
    output_path: Path,
    title: str,
    subtitle: str = "",
) -> None:
    lut17_results = [result for result in results if int(result["lut_size"]) == 17]
    if not lut17_results:
        return

    by_method = {
        (result.get("fit_method"), result.get("apply_method")): result
        for result in lut17_results
    }
    best_result = min(lut17_results, key=lambda result: result["metrics"]["delta_e_mean"])
    fit_methods = ["mean", "median", "weighted_mean"]
    apply_methods = ["nearest", "trilinear"]

    thumb_w, thumb_h = 620, 414
    pad = 30
    gap = 18
    title_h = 104
    row_label_w = 180
    cell_label_h = 76
    header_h = 42
    sheet_w = pad * 2 + row_label_w + len(apply_methods) * thumb_w + gap * 2
    sheet_h = (
        title_h
        + header_h
        + len(fit_methods) * (thumb_h + cell_label_h + gap)
        + pad
    )

    sheet = Image.new("RGB", (sheet_w, sheet_h), (252, 252, 252))
    draw = ImageDraw.Draw(sheet)
    title_font = _load_font(28, bold=True)
    subtitle_font = _load_font(15)
    label_font = _load_font(16, bold=True)
    metric_font = _load_font(13)
    crop_box = _best_disagreement_crop(lut17_results, thumb_w / thumb_h)

    draw.text((pad, 24), title, fill=(20, 20, 20), font=title_font)
    if subtitle:
        _draw_wrapped_text(
            draw,
            (pad, 60),
            f"{subtitle} Crop automatico ingrandito nella zona dove le varianti divergono di piu'.",
            subtitle_font,
            (75, 75, 75),
            sheet_w - pad * 2,
        )

    table_y = title_h
    for col, apply_method in enumerate(apply_methods):
        x = pad + row_label_w + gap + col * (thumb_w + gap)
        draw.text((x, table_y + 8), apply_method, fill=(25, 25, 25), font=label_font)

    for row_index, fit_method in enumerate(fit_methods):
        y = table_y + header_h + row_index * (thumb_h + cell_label_h + gap)
        draw.text((pad, y + 18), fit_method, fill=(25, 25, 25), font=label_font)

        for col, apply_method in enumerate(apply_methods):
            x = pad + row_label_w + gap + col * (thumb_w + gap)
            result = by_method.get((fit_method, apply_method))
            is_best = result is best_result
            outline = (24, 118, 72) if is_best else (224, 224, 224)
            width = 5 if is_best else 1
            draw.rounded_rectangle(
                (x, y, x + thumb_w, y + thumb_h + cell_label_h),
                radius=6,
                fill=(255, 255, 255),
                outline=outline,
                width=width,
            )
            if result is None:
                _draw_wrapped_text(
                    draw,
                    (x + 14, y + 22),
                    "Risultato non disponibile.",
                    metric_font,
                    (90, 90, 90),
                    thumb_w - 28,
                )
                continue

            sheet.paste(
                _zoom_crop_on_canvas(
                    result["reconstruction"],
                    crop_box,
                    (thumb_w, thumb_h),
                ),
                (x, y),
            )
            metrics = result["metrics"]
            best_prefix = "BEST LUT17 | " if is_best else ""
            metric_text = (
                f"{best_prefix}PSNR {metrics['rgb_psnr']} | SSIM {metrics['ssim']}\n"
                f"Delta E mean {metrics['delta_e_mean']} | p95 {metrics['delta_e_p95']}"
            )
            _draw_wrapped_text(
                draw,
                (x + 10, y + thumb_h + 9),
                metric_text,
                metric_font,
                (55, 55, 55),
                thumb_w - 20,
                line_spacing=2,
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)


def make_best_lut_summary_image(
    original: np.ndarray,
    target: np.ndarray,
    result: dict,
    output_path: Path,
    title: str,
    subtitle: str = "",
) -> None:
    thumb_w, thumb_h = 480, 320
    pad = 30
    gap = 18
    title_h = 108
    label_h = 88
    sheet_w = pad * 2 + 4 * thumb_w + 3 * gap
    sheet_h = title_h + label_h + thumb_h + pad

    sheet = Image.new("RGB", (sheet_w, sheet_h), (252, 252, 252))
    draw = ImageDraw.Draw(sheet)
    title_font = _load_font(28, bold=True)
    subtitle_font = _load_font(15)
    label_font = _load_font(16, bold=True)
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

    metrics = result["metrics"]
    items = [
        ("Originale input", "Foto di partenza.", original),
        ("Target FLUX", "Riferimento diffusion.", target),
        (
            "Migliore LUT",
            (
                f"{result.get('variant', 'best')}\n"
                f"PSNR {metrics['rgb_psnr']} | dE {metrics['delta_e_mean']}"
            ),
            result["reconstruction"],
        ),
        (
            "Heatmap errore",
            "Blu basso, verde medio, rosso alto.",
            result["heatmap"],
        ),
    ]

    y = title_h
    for col, (label, note, image) in enumerate(items):
        x = pad + col * (thumb_w + gap)
        draw.rounded_rectangle(
            (x, y, x + thumb_w, y + label_h + thumb_h),
            radius=6,
            fill=(255, 255, 255),
            outline=(224, 224, 224),
        )
        draw.text((x + 10, y + 9), label, fill=(22, 22, 22), font=label_font)
        _draw_wrapped_text(
            draw,
            (x + 10, y + 34),
            note,
            metric_font,
            (70, 70, 70),
            thumb_w - 20,
            line_spacing=2,
        )
        sheet.paste(_fit_on_canvas(image, (thumb_w, thumb_h)), (x, y + label_h))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)


def compute_metrics(target: np.ndarray, reconstruction: np.ndarray) -> dict:
    delta_e = delta_e_2000(target, reconstruction)
    rgb_abs = np.abs(target - reconstruction)
    return {
        "rgb_mae": round(float(rgb_abs.mean() * 255.0), 3),
        "rgb_psnr": round(psnr(target, reconstruction), 3),
        "ssim": round(ssim_metric(target, reconstruction), 4),
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
        "lut_*_reconstruction.png",
        "lut_*_error_vs_flux.png",
        "metrics.csv",
        "summary.png",
        "best_summary.png",
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
    fit_methods: list[str] | None = None,
    apply_methods: list[str] | None = None,
) -> list[dict]:
    if fit_methods is None:
        fit_methods = DEFAULT_FIT_METHODS
    if apply_methods is None:
        apply_methods = DEFAULT_APPLY_METHODS

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
    best_summary_path = output_dir / "best_summary.png"
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
        "method": "nearest_node_or_weighted_fit_identity_empty_configurable_apply",
        "lut_sizes": lut_sizes,
        "fit_methods": fit_methods,
        "apply_methods": apply_methods,
        "arrays_saved": save_arrays,
    }

    target_metadata_path = target_path.with_suffix(".json")
    if target_metadata_path.exists():
        metadata["target_metadata"] = json.loads(
            target_metadata_path.read_text(encoding="utf-8")
        )

    for size in lut_sizes:
        for fit_method in fit_methods:
            lut, counts = fit_lut(
                original,
                target,
                size,
                sample_count,
                seed,
                fit_method,
            )

            lut_data_path = ""
            counts_data_path = ""
            if save_arrays:
                data_dir = output_dir / "data"
                data_dir.mkdir(parents=True, exist_ok=True)
                lut_path = data_dir / f"lut_{size}_{fit_method}.npy"
                counts_path = data_dir / f"lut_{size}_{fit_method}_counts.npy"
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

            for apply_method in apply_methods:
                variant = f"lut_{size}_{fit_method}_{apply_method}"
                reconstruction = apply_lut(original, lut, apply_method)
                heatmap = error_heatmap(target, reconstruction)

                reconstruction_path = output_dir / f"{variant}_reconstruction.png"
                heatmap_path = output_dir / f"{variant}_error_vs_flux.png"

                save_rgb(reconstruction_path, reconstruction)
                save_rgb(heatmap_path, heatmap)

                metrics = {
                    **compute_metrics(target, reconstruction),
                    "occupied_ratio": round(occupied_ratio, 5),
                }
                row = {
                    "method": f"{fit_method}_{apply_method}",
                    "fit_method": fit_method,
                    "apply_method": apply_method,
                    "variant": variant,
                    "lut_size": size,
                    "sample_count": int(
                        min(sample_count, original.reshape(-1, 3).shape[0])
                    ),
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
                    "best_summary_path": str(best_summary_path),
                    "lut_data_path": lut_data_path,
                    "counts_data_path": counts_data_path,
                }
                rows.append(row)
                visual_results.append(
                    {
                        "lut_size": size,
                        "fit_method": fit_method,
                        "apply_method": apply_method,
                        "variant": variant,
                        "reconstruction": reconstruction,
                        "heatmap": heatmap,
                        "metrics": metrics,
                    }
                )

    write_metrics(output_dir / "metrics.csv", rows)
    write_json(output_dir / "data" / "experiment_metadata.json", metadata)
    prompt_label = metadata.get("target_metadata", {}).get("prompt_key", target_path.stem)
    make_lut17_method_grid(
        original=original,
        target=target,
        results=visual_results,
        output_path=summary_path,
        title=f"LUT vs FLUX - {target_path.parent.name} / {prompt_label}",
        subtitle="LUT 17: confronto tra metodi di fitting e applicazione.",
    )
    best_result = min(visual_results, key=lambda result: result["metrics"]["delta_e_mean"])
    make_best_lut_summary_image(
        original=original,
        target=target,
        result=best_result,
        output_path=best_summary_path,
        title=f"Best LUT - {target_path.parent.name} / {prompt_label}",
        subtitle="Migliore variante selezionata per Delta E medio.",
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
    parser.add_argument("--fit-methods", nargs="+", default=DEFAULT_FIT_METHODS)
    parser.add_argument("--apply-methods", nargs="+", default=DEFAULT_APPLY_METHODS)
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
        fit_methods=args.fit_methods,
        apply_methods=args.apply_methods,
    )
    for row in rows:
        print(
            f"lut={row['lut_size']} "
            f"fit={row['fit_method']} "
            f"apply={row['apply_method']} "
            f"psnr={row['rgb_psnr']} "
            f"ssim={row['ssim']} "
            f"dE_mean={row['delta_e_mean']} "
            f"occupied={row['occupied_ratio']}"
        )
    print(f"Output written to: {args.output_dir}")


if __name__ == "__main__":
    main()
