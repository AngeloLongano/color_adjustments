import json
from pathlib import Path

import numpy as np
import yaml
from PIL import Image


def load_rgb(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.float32) / 255.0


def save_rgb(path: Path, image: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = np.clip(np.rint(image * 255.0), 0, 255).astype(np.uint8)
    Image.fromarray(data).save(path)


def resize_to(image: np.ndarray, width: int, height: int) -> np.ndarray:
    data = np.clip(np.rint(image * 255.0), 0, 255).astype(np.uint8)
    resized = Image.fromarray(data).resize((width, height), Image.Resampling.BICUBIC)
    return np.asarray(resized, dtype=np.float32) / 255.0


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def read_config(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text) or {}
    return json.loads(text)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
