import argparse
import csv
from pathlib import Path
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.flux.generate_targets import resolve_prepared_image
from utils.common.image_io import load_rgb, read_config, read_json, resize_to
from utils.common.metrics import (
    delta_e_2000,
    gradient_magnitude,
    pearson_corr,
    psnr,
    rgb_to_luma,
    ssim_metric,
)


def find_original(generated_path: Path, metadata: dict, originals_dir: Path) -> Path:
    image_from_metadata = metadata.get("image")
    if image_from_metadata:
        candidate = Path(image_from_metadata)
        if candidate.exists():
            return candidate

    image_id = generated_path.parent.name
    candidate = originals_dir / f"{image_id}.png"
    if candidate.exists():
        return candidate

    raise FileNotFoundError(f"Original image not found for {generated_path}")


def decision_hint(
    edge_corr: float,
    ssim: float,
    delta_e_mean: float,
    delta_e_p95: float,
) -> str:
    if edge_corr < 0.70 or ssim < 0.45:
        return "check_content_change"
    if delta_e_mean < 4.0:
        return "weak_color_change"
    if delta_e_p95 > 55.0 and edge_corr < 0.82:
        return "possible_semantic_change"
    return "candidate"


def evaluate_pair(original_path: Path, generated_path: Path) -> dict:
    generated = load_rgb(generated_path)
    original = load_rgb(original_path)
    height, width = generated.shape[:2]
    if original.shape[:2] != generated.shape[:2]:
        original = resize_to(original, width, height)

    original_luma = rgb_to_luma(original)
    generated_luma = rgb_to_luma(generated)
    original_edges = gradient_magnitude(original_luma)
    generated_edges = gradient_magnitude(generated_luma)
    delta_e = delta_e_2000(original, generated)

    rgb_abs = np.abs(original - generated)
    edge_corr = pearson_corr(original_edges, generated_edges)
    ssim = ssim_metric(original, generated)
    delta_e_mean = float(delta_e.mean())
    delta_e_p95 = float(np.percentile(delta_e, 95))

    return {
        "width": width,
        "height": height,
        "edge_correlation": round(edge_corr, 4),
        "ssim": round(ssim, 4),
        "rgb_mae": round(float(rgb_abs.mean() * 255.0), 3),
        "rgb_psnr": round(psnr(original, generated), 3),
        "delta_e_mean": round(delta_e_mean, 3),
        "delta_e_median": round(float(np.median(delta_e)), 3),
        "delta_e_p95": round(delta_e_p95, 3),
        "decision_hint": decision_hint(edge_corr, ssim, delta_e_mean, delta_e_p95),
    }


def iter_generated_images(experiments_dir: Path):
    yield from sorted(experiments_dir.glob("*/*.png"))


def evaluate_directory(experiments_dir: Path, originals_dir: Path) -> list[dict]:
    rows = []
    for generated_path in iter_generated_images(experiments_dir):
        metadata = read_json(generated_path.with_suffix(".json"))
        original_path = find_original(generated_path, metadata, originals_dir)
        metrics = evaluate_pair(original_path, generated_path)
        rows.append(
            {
                "image_id": generated_path.parent.name,
                "generated_file": generated_path.name,
                "original_path": str(original_path),
                "generated_path": str(generated_path),
                "model_key": metadata.get("model_key", ""),
                "prompt_key": metadata.get("prompt_key", ""),
                "seed": metadata.get("seed", ""),
                **metrics,
                "human_decision": "",
                "notes": "",
            }
        )
    return rows


def write_csv(rows: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        output_path.write_text("", encoding="utf-8")
        return

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def prompt_label(prompt_id: str) -> str:
    parts = prompt_id.split("_", 1)
    if len(parts) == 2 and parts[0].startswith("p"):
        return f"{parts[0]}\n{parts[1].replace('_', ' ')}"
    return prompt_id.replace("_", " ")


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    *,
    fill: tuple[int, int, int],
    font: ImageFont.ImageFont,
    line_gap: int = 3,
) -> None:
    lines = text.splitlines() or [text]
    boxes = [draw.textbbox((0, 0), line, font=font) for line in lines]
    heights = [box_[3] - box_[1] for box_ in boxes]
    total_h = sum(heights) + max(0, len(lines) - 1) * line_gap
    y = box[1] + (box[3] - box[1] - total_h) // 2
    for line, text_box, height in zip(lines, boxes, heights, strict=True):
        width = text_box[2] - text_box[0]
        x = box[0] + (box[2] - box[0] - width) // 2
        draw.text((x, y), line, fill=fill, font=font)
        y += height + line_gap


def image_order_from_config(
    images_config: Path,
    originals_dir: Path,
    image_selection: str,
    rows: list[dict],
) -> list[str]:
    config = read_config(images_config)
    image_keys = config.get(image_selection)
    if isinstance(image_keys, list):
        image_ids = []
        for key in image_keys:
            path = resolve_prepared_image(originals_dir, str(key))
            image_ids.append(path.stem)
        return image_ids
    return sorted({str(row["image_id"]) for row in rows})


def prompt_order_from_config(images_config: Path, rows: list[dict]) -> list[str]:
    config = read_config(images_config)
    prompt_ids = config.get("prompts")
    if isinstance(prompt_ids, list):
        return [str(prompt_id) for prompt_id in prompt_ids]
    return sorted({str(row["prompt_key"]) for row in rows if row.get("prompt_key")})


def decision_color(decision: str) -> tuple[int, int, int]:
    if decision == "candidate":
        return (226, 245, 229)
    if decision == "weak_color_change":
        return (242, 242, 242)
    if decision == "possible_semantic_change":
        return (255, 241, 214)
    if decision == "check_content_change":
        return (253, 226, 226)
    return (245, 245, 245)


def format_quality_cell(row: dict | None) -> str:
    if row is None:
        return "missing"
    return (
        f"{row['decision_hint']}\n"
        f"edge: {row['edge_correlation']}\n"
        f"ssim: {row['ssim']}\n"
        f"psnr: {row['rgb_psnr']} dB\n"
        f"mae: {row['rgb_mae']}\n"
        f"dE mean: {row['delta_e_mean']}\n"
        f"dE p95: {row['delta_e_p95']}"
    )


def write_quality_grid(
    rows: list[dict],
    output_path: Path,
    *,
    images_config: Path = Path("configs/images.yaml"),
    originals_dir: Path = Path("images"),
    image_selection: str = "selected_images",
    cell_size: tuple[int, int] = (240, 160),
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()
    pad = 10
    header_h = 46
    row_label_h = 24
    cell_w, cell_h = cell_size

    image_ids = image_order_from_config(images_config, originals_dir, image_selection, rows)
    prompt_ids = prompt_order_from_config(images_config, rows)
    row_by_key = {
        (str(row["image_id"]), str(row["prompt_key"])): row
        for row in rows
        if row.get("prompt_key")
    }
    cols = ["original"] + prompt_ids

    sheet_w = len(cols) * cell_w + (len(cols) + 1) * pad
    sheet_h = header_h + len(image_ids) * (row_label_h + cell_h + pad) + pad
    sheet = Image.new("RGB", (sheet_w, sheet_h), "white")
    draw = ImageDraw.Draw(sheet)

    for col_index, col in enumerate(cols):
        x = pad + col_index * (cell_w + pad)
        label = "originale" if col == "original" else prompt_label(col)
        draw_centered_text(
            draw,
            (x, pad, x + cell_w, pad + header_h - 6),
            label,
            fill=(25, 25, 25),
            font=font,
        )

    for row_index, image_id in enumerate(image_ids):
        y = header_h + row_index * (row_label_h + cell_h + pad)
        draw.text((pad, y), image_id, fill=(25, 25, 25), font=font)

        original_box = (pad, y + row_label_h, pad + cell_w, y + row_label_h + cell_h)
        draw.rectangle(original_box, fill=(245, 245, 245), outline=(210, 210, 210))
        draw_centered_text(
            draw,
            original_box,
            f"originale\n{image_id}",
            fill=(35, 35, 35),
            font=font,
        )

        for prompt_index, prompt_id in enumerate(prompt_ids, start=1):
            x = pad + prompt_index * (cell_w + pad)
            box = (x, y + row_label_h, x + cell_w, y + row_label_h + cell_h)
            row = row_by_key.get((image_id, prompt_id))
            fill = decision_color(str(row["decision_hint"])) if row else (238, 238, 238)
            outline = (190, 190, 190) if row else (170, 40, 40)
            draw.rectangle(box, fill=fill, outline=outline)
            draw_centered_text(
                draw,
                (box[0] + 8, box[1] + 8, box[2] - 8, box[3] - 8),
                format_quality_cell(row),
                fill=(25, 25, 25) if row else (120, 20, 20),
                font=font,
            )

    sheet.save(output_path, quality=92)


def print_summary(rows: list[dict]) -> None:
    print(f"Evaluated images: {len(rows)}")
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["decision_hint"]] = counts.get(row["decision_hint"], 0) + 1

    for label, count in sorted(counts.items()):
        print(f"- {label}: {count}")

    candidates = [row for row in rows if row["decision_hint"] == "candidate"]
    candidates = sorted(
        candidates,
        key=lambda row: (
            row["image_id"],
            -float(row["edge_correlation"]),
            abs(float(row["delta_e_mean"]) - 18.0),
        ),
    )
    if candidates:
        print("\nTop candidate hints:")
        for row in candidates[:12]:
            print(
                f"- {row['image_id']} {row['generated_file']} "
                f"edge={row['edge_correlation']} "
                f"ssim={row['ssim']} "
                f"dE={row['delta_e_mean']}"
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate image-to-image preview/target quality with structural and color-change metrics."
    )
    parser.add_argument(
        "--experiments-dir",
        type=Path,
        default=Path("images_flux/preview"),
        help="Directory containing one subdirectory per image with generated PNG files.",
    )
    parser.add_argument(
        "--originals-dir",
        type=Path,
        default=Path("images"),
        help="Directory containing prepared original PNG files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("images_flux/i2i_quality_preview.csv"),
        help="CSV output path.",
    )
    parser.add_argument(
        "--grid-output",
        type=Path,
        help="Optional JPEG grid with decision hints and metrics.",
    )
    parser.add_argument(
        "--images-config",
        type=Path,
        default=Path("configs/images.yaml"),
        help="Config used to order selected images and prompts in the grid.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = evaluate_directory(args.experiments_dir, args.originals_dir)
    write_csv(rows, args.output)
    if args.grid_output:
        write_quality_grid(
            rows,
            args.grid_output,
            images_config=args.images_config,
            originals_dir=args.originals_dir,
        )
    print_summary(rows)
    print(f"\nCSV written to: {args.output}")
    if args.grid_output:
        print(f"Grid written to: {args.grid_output}")
