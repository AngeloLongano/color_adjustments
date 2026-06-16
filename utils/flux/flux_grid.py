from __future__ import annotations

import argparse
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.flux.generate_targets import resolve_prepared_image
from utils.common.image_io import read_config


DEFAULT_IMAGES_CONFIG = Path("configs/images.yaml")
DEFAULT_INPUT_DIR = Path("images")
DEFAULT_FLUX_DIR = Path("images_flux/preview")
DEFAULT_OUTPUT = Path("images_flux/preview_grid.jpg")


def prompt_label(prompt_id: str) -> str:
    parts = prompt_id.split("_", 1)
    if len(parts) == 2 and parts[0].startswith("p"):
        return f"{parts[0]}\n{parts[1].replace('_', ' ')}"
    return prompt_id.replace("_", " ")


def fit_image(path: Path, size: tuple[int, int]) -> Image.Image:
    image = Image.open(path).convert("RGB")
    image.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, (245, 245, 245))
    ox = (size[0] - image.width) // 2
    oy = (size[1] - image.height) // 2
    canvas.paste(image, (ox, oy))
    return canvas


def missing_tile(size: tuple[int, int], text: str) -> Image.Image:
    image = Image.new("RGB", size, (238, 238, 238))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.rectangle((0, 0, size[0] - 1, size[1] - 1), outline=(170, 40, 40), width=2)
    draw.text((10, 10), text, fill=(120, 20, 20), font=font)
    return image


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    *,
    fill: tuple[int, int, int] = (25, 25, 25),
    font: ImageFont.ImageFont,
) -> None:
    lines = text.splitlines() or [text]
    line_boxes = [draw.textbbox((0, 0), line, font=font) for line in lines]
    line_heights = [bbox[3] - bbox[1] for bbox in line_boxes]
    total_h = sum(line_heights) + max(0, len(lines) - 1) * 3
    y = box[1] + (box[3] - box[1] - total_h) // 2
    for line, bbox, line_h in zip(lines, line_boxes, line_heights, strict=True):
        line_w = bbox[2] - bbox[0]
        x = box[0] + (box[2] - box[0] - line_w) // 2
        draw.text((x, y), line, fill=fill, font=font)
        y += line_h + 3


def find_flux_output(
    flux_dir: Path,
    image_id: str,
    prompt_id: str,
    *,
    model: str | None,
    seed: int,
) -> Path | None:
    image_dir = flux_dir / image_id
    if not image_dir.exists():
        return None

    preferred = (
        image_dir / f"{prompt_id}_s{seed}_{model}.png" if model else None
    )
    if preferred and preferred.exists():
        return preferred

    seed_matches = sorted(image_dir.glob(f"{prompt_id}_s{seed}_*.png"))
    if seed_matches:
        return seed_matches[0]

    matches = sorted(image_dir.glob(f"{prompt_id}_*.png"))
    if matches:
        return matches[0]

    return None


def build_flux_grid(
    *,
    images_config: Path = DEFAULT_IMAGES_CONFIG,
    input_dir: Path = DEFAULT_INPUT_DIR,
    flux_dir: Path = DEFAULT_FLUX_DIR,
    output_path: Path = DEFAULT_OUTPUT,
    image_selection: str = "selected_images",
    prompts: list[str] | None = None,
    model: str | None = None,
    seed: int = 0,
    thumb_size: tuple[int, int] = (240, 160),
) -> list[Path]:
    config = read_config(images_config)
    image_keys = config.get(image_selection)
    if not isinstance(image_keys, list):
        raise ValueError(f"Selection '{image_selection}' is not a list in {images_config}")

    prompt_ids = prompts or config.get("prompts")
    if not isinstance(prompt_ids, list) or not prompt_ids:
        raise ValueError(f"No prompts configured in {images_config}")
    prompt_ids = [str(prompt_id) for prompt_id in prompt_ids]

    models = config.get("models")
    if model is None and isinstance(models, list) and len(models) == 1:
        model = str(models[0])

    font = ImageFont.load_default()
    pad = 10
    header_h = 46
    row_label_h = 24
    thumb_w, thumb_h = thumb_size
    cols = ["original"] + prompt_ids
    rows = [(str(key), resolve_prepared_image(input_dir, str(key))) for key in image_keys]

    sheet_w = len(cols) * thumb_w + (len(cols) + 1) * pad
    sheet_h = header_h + len(rows) * (row_label_h + thumb_h + pad) + pad
    sheet = Image.new("RGB", (sheet_w, sheet_h), "white")
    draw = ImageDraw.Draw(sheet)

    for col_index, col in enumerate(cols):
        x = pad + col_index * (thumb_w + pad)
        label = "originale" if col == "original" else prompt_label(col)
        draw_centered_text(
            draw,
            (x, pad, x + thumb_w, pad + header_h - 6),
            label,
            font=font,
        )

    missing: list[Path] = []
    for row_index, (image_key, original_path) in enumerate(rows):
        image_id = original_path.stem
        y = header_h + row_index * (row_label_h + thumb_h + pad)

        draw.text((pad, y), image_id, fill=(25, 25, 25), font=font)

        original_tile = (
            fit_image(original_path, thumb_size)
            if original_path.exists()
            else missing_tile(thumb_size, f"missing\n{original_path}")
        )
        if not original_path.exists():
            missing.append(original_path)
        sheet.paste(original_tile, (pad, y + row_label_h))

        for prompt_index, prompt_id in enumerate(prompt_ids, start=1):
            x = pad + prompt_index * (thumb_w + pad)
            flux_path = find_flux_output(
                flux_dir,
                image_id,
                prompt_id,
                model=model,
                seed=seed,
            )
            if flux_path is None:
                missing_path = flux_dir / image_id / f"{prompt_id}_s{seed}.png"
                tile = missing_tile(thumb_size, f"missing\n{prompt_id}")
                missing.append(missing_path)
            else:
                tile = fit_image(flux_path, thumb_size)
            sheet.paste(tile, (x, y + row_label_h))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=92)
    return missing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a grid with originals and Flux transformations."
    )
    parser.add_argument("--images-config", type=Path, default=DEFAULT_IMAGES_CONFIG)
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--flux-dir", type=Path, default=DEFAULT_FLUX_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--image-selection", default="selected_images")
    parser.add_argument("--prompts", nargs="+")
    parser.add_argument("--model")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--thumb-width", type=int, default=240)
    parser.add_argument("--thumb-height", type=int, default=160)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    missing = build_flux_grid(
        images_config=args.images_config,
        input_dir=args.input_dir,
        flux_dir=args.flux_dir,
        output_path=args.output,
        image_selection=args.image_selection,
        prompts=args.prompts,
        model=args.model,
        seed=args.seed,
        thumb_size=(args.thumb_width, args.thumb_height),
    )
    print(f"Flux grid written to: {args.output}")
    if missing:
        print(f"Missing files/placeholders: {len(missing)}")
        for path in missing:
            print(f"- {path}")


if __name__ == "__main__":
    main()
