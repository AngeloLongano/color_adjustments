from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
import sys

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.common.image_io import read_config


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
DEFAULT_INPUT_DIR = Path("downloads")
DEFAULT_OUTPUT_DIR = Path("images")
DEFAULT_TARGET_SIZE = (1008, 672)
LEVEL_NUMBER_RE = re.compile(r"^(L[1-4]_\d+)(?:_|$)")
SUPPORTED_LEVEL_RE = re.compile(r"^(L[1-4])(?:_candidate)?$")


@dataclass(frozen=True)
class PrepareResult:
    image_key: str
    level: str
    source_file: str
    output_file: str
    source_width: int
    source_height: int
    crop_left: int
    crop_top: int
    crop_right: int
    crop_bottom: int
    crop_width: int
    crop_height: int
    target_width: int
    target_height: int
    output_format: str


def parse_size(value: str) -> tuple[int, int]:
    normalized = value.lower().replace("x", " ")
    parts = normalized.split()
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("Size must look like 1008x672.")

    try:
        width, height = int(parts[0]), int(parts[1])
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Size must contain integer values.") from exc

    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("Size values must be positive.")

    return width, height


def center_crop_box(width: int, height: int, target_width: int, target_height: int) -> tuple[int, int, int, int]:
    target_ratio = target_width / target_height
    current_ratio = width / height

    if current_ratio > target_ratio:
        crop_height = height
        crop_width = round(height * target_ratio)
    else:
        crop_width = width
        crop_height = round(width / target_ratio)

    crop_width = min(crop_width, width)
    crop_height = min(crop_height, height)

    left = (width - crop_width) // 2
    top = (height - crop_height) // 2
    right = left + crop_width
    bottom = top + crop_height

    return left, top, right, bottom


def compact_output_stem(source_path: Path) -> str:
    match = LEVEL_NUMBER_RE.match(source_path.stem)
    if match:
        return match.group(1)
    return source_path.stem


def clean_output_stem(image_key: str, level: str) -> str:
    return f"{level}_{image_key}"


def output_path_for(
    image_key: str,
    level: str,
    output_dir: Path,
    output_format: str,
) -> Path:
    suffix = ".jpg" if output_format == "jpg" else ".png"
    return output_dir / f"{clean_output_stem(image_key, level)}{suffix}"


def validate_unique_outputs(
    selected: list[tuple[str, str, Path]],
    output_dir: Path,
    output_format: str,
) -> None:
    output_names = [
        output_path_for(image_key, level, output_dir, output_format).name
        for image_key, level, _ in selected
    ]
    duplicates = sorted(
        name
        for name in set(output_names)
        if output_names.count(name) > 1
    )
    if duplicates:
        joined = ", ".join(duplicates)
        raise ValueError(f"Output name collision: {joined}")


def prepare_image(
    image_key: str,
    level: str,
    source_path: Path,
    output_dir: Path,
    target_size: tuple[int, int],
    output_format: str,
    jpeg_quality: int,
    dry_run: bool,
) -> PrepareResult:
    target_width, target_height = target_size

    with Image.open(source_path) as raw_img:
        img = ImageOps.exif_transpose(raw_img).convert("RGB")
        source_width, source_height = img.size

        crop_box = center_crop_box(
            source_width,
            source_height,
            target_width,
            target_height,
        )
        cropped = img.crop(crop_box)
        resized = cropped.resize(target_size, Image.Resampling.LANCZOS)

        output_path = output_path_for(image_key, level, output_dir, output_format)

        if not dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)
            if output_format == "png":
                resized.save(output_path, format="PNG", optimize=True)
            else:
                resized.save(
                    output_path,
                    format="JPEG",
                    quality=jpeg_quality,
                    optimize=True,
                    subsampling=0,
                )

    left, top, right, bottom = crop_box
    return PrepareResult(
        image_key=image_key,
        level=level,
        source_file=source_path.name,
        output_file=output_path.name,
        source_width=source_width,
        source_height=source_height,
        crop_left=left,
        crop_top=top,
        crop_right=right,
        crop_bottom=bottom,
        crop_width=right - left,
        crop_height=bottom - top,
        target_width=target_width,
        target_height=target_height,
        output_format=output_format,
    )


def write_manifest(manifest_path: Path, rows: list[PrepareResult]) -> None:
    if not rows:
        return

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(PrepareResult.__dataclass_fields__.keys())

    with manifest_path.open("w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def iter_image_paths(input_dir: Path) -> list[Path]:
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {input_dir}")

    return sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS
    )


def read_config_selection(config_path: Path, selection: str) -> list[str]:
    config = read_config(config_path)
    if selection == "all":
        values = list(config.get("candidate_images", {}).keys())
    else:
        values = config.get(selection)
    if not isinstance(values, list):
        raise ValueError(f"Selection '{selection}' is not a list in {config_path}")
    return [str(value) for value in values]


def compact_level(value: str) -> str:
    match = SUPPORTED_LEVEL_RE.match(value)
    if not match:
        raise ValueError(f"Unsupported level value: {value}")
    return match.group(1)


def read_classification_levels(classification_path: Path) -> dict[str, str]:
    if not classification_path.exists():
        raise FileNotFoundError(f"Classification CSV not found: {classification_path}")

    levels: dict[str, str] = {}
    with classification_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            file_name = row.get("file")
            suggested_level = row.get("suggested_level")
            if not file_name or not suggested_level:
                continue
            try:
                levels[Path(file_name).stem] = compact_level(suggested_level)
            except ValueError:
                continue
    return levels


def selected_image_paths(
    input_dir: Path,
    image_keys: list[str],
    levels: dict[str, str],
) -> list[tuple[str, str, Path]]:
    available = {path.stem: path for path in iter_image_paths(input_dir)}
    selected = []
    missing = []
    missing_levels = []

    for image_key in image_keys:
        source_path = available.get(image_key)
        if source_path is None:
            missing.append(image_key)
            continue
        level = levels.get(image_key)
        if level is None:
            missing_levels.append(image_key)
            continue
        selected.append((image_key, level, source_path))

    if missing:
        raise FileNotFoundError(
            "Selected images not found in "
            f"{input_dir}: {', '.join(sorted(missing))}"
        )
    if missing_levels:
        raise KeyError(
            "Selected images missing from classification CSV: "
            f"{', '.join(sorted(missing_levels))}"
        )
    return selected


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert selected source images to a common size for diffusion/LUT experiments."
    )
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--config", type=Path, default=Path("configs/images.yaml"))
    parser.add_argument("--selection", default="selected_images")
    parser.add_argument("--classification", type=Path, default=Path("images/classification.csv"))
    parser.add_argument("--size", type=parse_size, default=DEFAULT_TARGET_SIZE)
    parser.add_argument("--format", choices=("png", "jpg"), default="png")
    parser.add_argument("--jpeg-quality", type=int, default=95)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    image_keys = read_config_selection(args.config, args.selection)
    levels = read_classification_levels(args.classification)
    selected = selected_image_paths(args.input_dir, image_keys, levels)
    if not selected:
        print(f"No supported images found in {args.input_dir}.")
        return
    validate_unique_outputs(selected, args.output_dir, args.format)

    rows = [
        prepare_image(
            image_key=image_key,
            level=level,
            source_path=path,
            output_dir=args.output_dir,
            target_size=args.size,
            output_format=args.format,
            jpeg_quality=args.jpeg_quality,
            dry_run=args.dry_run,
        )
        for image_key, level, path in selected
    ]

    manifest_path = args.output_dir / "manifest.csv"
    if not args.dry_run:
        write_manifest(manifest_path, rows)

    print("PREPARAZIONE IMMAGINI")
    print("=" * 80)
    print(f"Input        : {args.input_dir}")
    print(f"Output       : {args.output_dir}")
    print(f"Formato      : {args.format}")
    print(f"Target size  : {args.size[0]}x{args.size[1]}")
    print(f"Selection    : {args.selection} ({args.config})")
    print(f"Classif. CSV : {args.classification}")
    print(f"Immagini     : {len(rows)}")
    if args.dry_run:
        print("Modalita'    : dry run, nessun file scritto")
    else:
        print(f"Manifest     : {manifest_path}")
    print()

    for row in rows:
        print(
            f"- {row.source_file} -> {row.output_file} "
            f"({row.source_width}x{row.source_height} -> "
            f"crop {row.crop_width}x{row.crop_height} -> "
            f"{row.target_width}x{row.target_height})"
        )


if __name__ == "__main__":
    main()
