import argparse
from pathlib import Path
import sys
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.common.image_io import read_config


def filename_from_url(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def selected_keys(config: dict, selection: str) -> list[str]:
    if selection == "all":
        return list(config["candidate_images"].keys())
    values = config.get(selection)
    if not isinstance(values, list):
        raise ValueError(f"Selection '{selection}' is not a list in config.")
    return values


def download_images(
    config_path: Path,
    output_dir: Path,
    selection: str,
    overwrite: bool,
) -> list[Path]:
    config = read_config(config_path)
    candidates = config.get("candidate_images", {})
    output_dir.mkdir(parents=True, exist_ok=True)

    downloaded = []
    for key in selected_keys(config, selection):
        if key not in candidates:
            raise KeyError(f"Image key '{key}' missing from candidate_images.")
        url = candidates[key]
        source_name = filename_from_url(url)
        suffix = Path(source_name).suffix
        output_path = output_dir / key
        if suffix:
            output_path = output_path.with_suffix(suffix)

        if output_path.exists() and not overwrite:
            print(f"skip existing: {output_path}")
        else:
            print(f"download: {key} -> {output_path}")
            urlretrieve(url, output_path)
        downloaded.append(output_path)

    return downloaded


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download configured MIT-Adobe FiveK candidate images."
    )
    parser.add_argument("--config", type=Path, default=Path("configs/images.yaml"))
    parser.add_argument("--output-dir", type=Path, default=Path("downloads"))
    parser.add_argument(
        "--selection",
        default="all",
        help="Config list to download, or 'all'.",
    )
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = download_images(
        config_path=args.config,
        output_dir=args.output_dir,
        selection=args.selection,
        overwrite=args.overwrite,
    )
    print(f"Images ready: {len(paths)}")
