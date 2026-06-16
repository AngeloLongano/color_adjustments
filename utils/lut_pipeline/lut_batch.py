import argparse
import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.common.image_io import read_json
from utils.lut_pipeline.lut import run_experiment


def find_original(target_path: Path, metadata: dict, originals_dir: Path) -> Path:
    image_from_metadata = metadata.get("image")
    if image_from_metadata:
        candidate = Path(image_from_metadata)
        if candidate.exists():
            return candidate

    image_id = target_path.parent.name
    candidate = originals_dir / f"{image_id}.png"
    if candidate.exists():
        return candidate

    raise FileNotFoundError(f"Original image not found for {target_path}")


def prompt_id_for(target_path: Path, metadata: dict) -> str:
    prompt_key = metadata.get("prompt_key")
    if prompt_key:
        return str(prompt_key)

    stem = target_path.stem
    marker = "_s"
    if marker in stem:
        return stem.split(marker, 1)[0]
    return stem


def iter_targets(targets_dir: Path):
    yield from sorted(targets_dir.glob("*/*.png"))


def write_summary(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run baseline LUT experiments for all diffusion targets."
    )
    parser.add_argument(
        "--targets-dir",
        type=Path,
        default=Path("images_flux/target"),
    )
    parser.add_argument(
        "--originals-dir",
        type=Path,
        default=Path("images"),
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("images_lut"),
    )
    parser.add_argument("--lut-sizes", type=int, nargs="+", default=[17, 33, 65])
    parser.add_argument("--sample-count", type=int, default=200000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--save-arrays",
        action="store_true",
        help="Save fitted LUT/count arrays under each experiment data/ directory.",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("images_lut/summary_all.csv"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    all_rows = []
    targets = list(iter_targets(args.targets_dir))

    for index, target_path in enumerate(targets, start=1):
        metadata = read_json(target_path.with_suffix(".json"))
        image_id = target_path.parent.name
        prompt_id = prompt_id_for(target_path, metadata)
        original_path = find_original(target_path, metadata, args.originals_dir)
        output_dir = args.output_root / image_id / prompt_id

        print(f"[{index}/{len(targets)}] {image_id}/{prompt_id}")
        rows = run_experiment(
            original_path=original_path,
            target_path=target_path,
            output_dir=output_dir,
            lut_sizes=args.lut_sizes,
            sample_count=args.sample_count,
            seed=args.seed,
            save_arrays=args.save_arrays,
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

    write_summary(args.summary, all_rows)
    print(f"Summary written to: {args.summary}")
