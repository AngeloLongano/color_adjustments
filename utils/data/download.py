import argparse
from pathlib import Path
import sys
from urllib.parse import urlparse
from urllib.request import urlretrieve

from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.common.image_io import read_config


CONTENT_TYPE_SUFFIXES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/tiff": ".tif",
    "image/webp": ".webp",
}

PIL_FORMAT_SUFFIXES = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "TIFF": ".tif",
    "WEBP": ".webp",
}


def suffix_from_url(url: str) -> str:
    return Path(urlparse(url).path).suffix.lower()


def suffix_from_headers(headers) -> str:
    if headers is None:
        return ""
    content_type = headers.get_content_type()
    return CONTENT_TYPE_SUFFIXES.get(content_type, "")


def suffix_from_image(path: Path) -> str:
    try:
        with Image.open(path) as image:
            return PIL_FORMAT_SUFFIXES.get(image.format or "", "")
    except (OSError, UnidentifiedImageError):
        return ""


def normalize_extension(path: Path, suffix: str) -> Path:
    if path.suffix or not suffix:
        return path

    renamed_path = path.with_suffix(suffix)
    if renamed_path.exists():
        return renamed_path

    path.rename(renamed_path)
    print(f"rename: {path} -> {renamed_path}")
    return renamed_path


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
        suffix = suffix_from_url(url)
        output_path = output_dir / key
        if suffix:
            output_path = output_path.with_suffix(suffix)

        if output_path.exists() and not overwrite:
            output_path = normalize_extension(
                output_path,
                suffix_from_image(output_path),
            )
            print(f"skip existing: {output_path}")
        else:
            print(f"download: {key} -> {output_path}")
            _, headers = urlretrieve(url, output_path)
            output_path = normalize_extension(
                output_path,
                suffix_from_headers(headers) or suffix_from_image(output_path),
            )
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
