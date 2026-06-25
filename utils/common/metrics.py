import math

import numpy as np
from skimage.color import deltaE_ciede2000, rgb2lab
from skimage.metrics import structural_similarity


def ensure_float01(arr: np.ndarray) -> np.ndarray:
    arr = arr.astype(np.float64, copy=False)
    if arr.size and np.nanmax(arr) > 1.5:
        arr = arr / 255.0
    return np.clip(arr, 0.0, 1.0)


def rgb_to_luma(arr: np.ndarray, linearize: bool = False) -> np.ndarray:
    arr = ensure_float01(arr)
    if linearize:
        arr = srgb_to_linear(arr)
    return 0.2126 * arr[..., 0] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 2]


def gradient_magnitude(gray: np.ndarray) -> np.ndarray:
    gy, gx = np.gradient(gray)
    return np.sqrt(gx * gx + gy * gy)


def pearson_corr(a: np.ndarray, b: np.ndarray) -> float:
    av = a.reshape(-1).astype(np.float64)
    bv = b.reshape(-1).astype(np.float64)
    av -= av.mean()
    bv -= bv.mean()
    denom = np.linalg.norm(av) * np.linalg.norm(bv)
    if denom == 0:
        return 0.0
    return float(np.dot(av, bv) / denom)


def ssim_metric(a: np.ndarray, b: np.ndarray) -> float:
    a = ensure_float01(a)
    b = ensure_float01(b)
    if a.shape != b.shape:
        raise ValueError(f"SSIM requires equal shapes, got {a.shape} and {b.shape}")
    channel_axis = -1 if a.ndim == 3 and a.shape[-1] in {3, 4} else None
    return float(
        structural_similarity(
            a,
            b,
            data_range=1.0,
            channel_axis=channel_axis,
        )
    )


def srgb_to_linear(arr: np.ndarray) -> np.ndarray:
    return np.where(arr <= 0.04045, arr / 12.92, ((arr + 0.055) / 1.055) ** 2.4)


def delta_e_2000(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    lab_a = rgb2lab(ensure_float01(a))
    lab_b = rgb2lab(ensure_float01(b))
    return deltaE_ciede2000(lab_a, lab_b)


def psnr(a: np.ndarray, b: np.ndarray, data_range: float = 1.0) -> float:
    a = a.astype(np.float64, copy=False)
    b = b.astype(np.float64, copy=False)
    mse = float(np.mean((a - b) ** 2))
    if mse == 0:
        return math.inf
    return 10 * math.log10((data_range**2) / mse)
