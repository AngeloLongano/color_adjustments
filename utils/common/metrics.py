import math

import numpy as np


def rgb_to_luma(arr: np.ndarray) -> np.ndarray:
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


def simple_ssim(a: np.ndarray, b: np.ndarray) -> float:
    a = a.astype(np.float64)
    b = b.astype(np.float64)
    c1 = 0.01**2
    c2 = 0.03**2
    mu_a = a.mean()
    mu_b = b.mean()
    var_a = a.var()
    var_b = b.var()
    cov = ((a - mu_a) * (b - mu_b)).mean()
    numerator = (2 * mu_a * mu_b + c1) * (2 * cov + c2)
    denominator = (mu_a * mu_a + mu_b * mu_b + c1) * (var_a + var_b + c2)
    if denominator == 0:
        return 1.0
    return float(numerator / denominator)


def srgb_to_linear(arr: np.ndarray) -> np.ndarray:
    return np.where(arr <= 0.04045, arr / 12.92, ((arr + 0.055) / 1.055) ** 2.4)


def rgb_to_lab(arr: np.ndarray) -> np.ndarray:
    rgb = srgb_to_linear(arr)
    matrix = np.array(
        [
            [0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1191920, 0.9503041],
        ],
        dtype=np.float32,
    )
    xyz = rgb @ matrix.T
    white = np.array([0.95047, 1.0, 1.08883], dtype=np.float32)
    xyz = xyz / white

    epsilon = 216 / 24389
    kappa = 24389 / 27
    f = np.where(xyz > epsilon, np.cbrt(xyz), (kappa * xyz + 16) / 116)

    lab = np.empty_like(xyz)
    lab[..., 0] = 116 * f[..., 1] - 16
    lab[..., 1] = 500 * (f[..., 0] - f[..., 1])
    lab[..., 2] = 200 * (f[..., 1] - f[..., 2])
    return lab


def delta_e_76(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.linalg.norm(rgb_to_lab(a) - rgb_to_lab(b), axis=-1)


def psnr(a: np.ndarray, b: np.ndarray) -> float:
    mse = float(np.mean((a - b) ** 2))
    if mse == 0:
        return math.inf
    return 10 * math.log10(1.0 / mse)

