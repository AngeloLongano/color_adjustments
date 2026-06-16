import argparse
from pathlib import Path
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import re

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
LEVEL_PREFIX_RE = re.compile(r"^L[1-4]_\d+_(.+)$")
RENAMED_LEVELS = {"L1", "L2", "L3", "L4"}


# ============================================================
# 1. Geometria: aspect ratio, crop loss, risoluzione
# ============================================================


def aspect_ratio_label(w, h):
    r = w / h

    known = {
        "1:1": 1.0,
        "4:3": 4 / 3,
        "3:2": 3 / 2,
        "16:9": 16 / 9,
    }

    best = min(known.items(), key=lambda x: abs(r - x[1]))
    return best[0], r, abs(r - best[1])


def crop_loss_to_ratio(w, h, target_ratio):
    """
    Percentuale di area persa se facciamo center crop verso target_ratio.
    """
    current = w / h

    if current > target_ratio:
        new_w = int(h * target_ratio)
        new_h = h
    else:
        new_w = w
        new_h = int(w / target_ratio)

    original_area = w * h
    cropped_area = new_w * new_h

    loss = 1 - cropped_area / original_area
    return round(loss * 100, 2)


def resize_loss_to_target(w, h, target_w, target_h):
    """
    Stima quanto bisogna ridimensionare l'immagine per arrivare alla target resolution.
    Non è una loss visiva, ma ci dice se l'immagine è molto più piccola o molto più grande.
    """
    target_pixels = target_w * target_h
    pixels = w * h

    return round(pixels / target_pixels, 2)


# ============================================================
# 2. Colore: complessità, entropia, colori dominanti
# ============================================================


def sample_pixels(img, sample_size=200_000, seed=42):
    arr = np.asarray(img.convert("RGB"))
    pixels = arr.reshape(-1, 3)

    if len(pixels) > sample_size:
        rng = np.random.default_rng(seed)
        idx = rng.choice(len(pixels), sample_size, replace=False)
        pixels = pixels[idx]

    return pixels


def color_complexity(img, sample_size=200_000, bins_per_channel=16):
    """
    Conta quanti bin RGB sono occupati.

    bins_per_channel=16 significa:
    - RGB viene discretizzato in 16 x 16 x 16 = 4096 celle
    - più celle occupate = immagine cromaticamente più varia
    """
    pixels = sample_pixels(img, sample_size=sample_size)

    step = 256 // bins_per_channel
    quantized = pixels // step

    unique_bins = np.unique(quantized, axis=0)
    score = len(unique_bins)

    return score


def color_entropy(img, sample_size=200_000, bins_per_channel=16):
    """
    Entropia della distribuzione dei colori quantizzati.

    Intuizione:
    - bassa entropia: pochi colori dominano molto
    - alta entropia: colori più distribuiti e vari
    """
    pixels = sample_pixels(img, sample_size=sample_size)

    step = 256 // bins_per_channel
    quantized = pixels // step

    # Convertiamo ogni colore quantizzato in un singolo indice
    idx = (
        quantized[:, 0] * bins_per_channel * bins_per_channel
        + quantized[:, 1] * bins_per_channel
        + quantized[:, 2]
    )

    counts = np.bincount(idx, minlength=bins_per_channel**3)
    probs = counts[counts > 0] / counts.sum()

    entropy = -np.sum(probs * np.log2(probs))

    # entropia massima teorica
    max_entropy = np.log2(bins_per_channel**3)

    normalized_entropy = entropy / max_entropy

    return round(float(entropy), 3), round(float(normalized_entropy), 3)


def dominant_colors(img, k=6, resize_to=160):
    """
    Trova i colori dominanti con quantizzazione semplice.
    Non usa clustering vero, ma è sufficiente per ispezione rapida.
    """
    small = img.convert("RGB")
    small.thumbnail((resize_to, resize_to))

    arr = np.asarray(small)
    pixels = arr.reshape(-1, 3)

    quantized = (pixels // 32) * 32
    colors, counts = np.unique(quantized, axis=0, return_counts=True)

    top_idx = np.argsort(counts)[::-1][:k]
    top_colors = colors[top_idx]
    top_counts = counts[top_idx]

    percentages = top_counts / counts.sum() * 100

    result = []
    for c, p in zip(top_colors, percentages):
        hex_color = "#{:02x}{:02x}{:02x}".format(*c)
        result.append(f"{hex_color} ({p:.1f}%)")

    return result


def dominant_color_concentration(img, k=5, resize_to=160):
    """
    Percentuale occupata dai primi k colori quantizzati.

    Utile perché:
    - L1 dovrebbe avere pochi colori dominanti forti
    - L2/L4 dovrebbero avere distribuzione più frammentata
    """
    small = img.convert("RGB")
    small.thumbnail((resize_to, resize_to))

    arr = np.asarray(small)
    pixels = arr.reshape(-1, 3)

    quantized = (pixels // 32) * 32
    colors, counts = np.unique(quantized, axis=0, return_counts=True)

    top_counts = np.sort(counts)[::-1][:k]
    concentration = top_counts.sum() / counts.sum() * 100

    return round(float(concentration), 2)


def colorfulness_score(img, sample_size=200_000):
    """
    Stima percettiva semplice della vividezza cromatica.

    E' utile per distinguere immagini con molti bin RGB ma quasi monocromatiche
    da immagini davvero ricche di colori.
    """
    pixels = sample_pixels(img, sample_size=sample_size).astype(np.float32)

    rg = pixels[:, 0] - pixels[:, 1]
    yb = 0.5 * (pixels[:, 0] + pixels[:, 1]) - pixels[:, 2]

    std_root = np.sqrt(np.var(rg) + np.var(yb))
    mean_root = np.sqrt(np.mean(rg) ** 2 + np.mean(yb) ** 2)

    return round(float(std_root + 0.3 * mean_root), 2)


def luminance_stats(img, sample_size=200_000):
    """
    Riassume la distribuzione di luminanza.

    Una grande quota di ombre puo' abbassare entropia e concentrazione colore,
    anche in scene semanticamente complesse.
    """
    pixels = sample_pixels(img, sample_size=sample_size).astype(np.float32) / 255.0
    luminance = 0.2126 * pixels[:, 0] + 0.7152 * pixels[:, 1] + 0.0722 * pixels[:, 2]

    shadow_fraction = np.mean(luminance < 0.12) * 100
    highlight_fraction = np.mean(luminance > 0.88) * 100

    return {
        "luminance_mean": round(float(np.mean(luminance)), 3),
        "shadow_fraction_%": round(float(shadow_fraction), 2),
        "highlight_fraction_%": round(float(highlight_fraction), 2),
    }


# ============================================================
# 3. Struttura visiva: bordi e texture
# ============================================================


def grayscale_array(img, resize_to=512):
    """
    Converte in grayscale e riduce dimensione per rendere le metriche leggere.
    """
    gray = ImageOps.grayscale(img)
    gray.thumbnail((resize_to, resize_to))

    arr = np.asarray(gray).astype(np.float32) / 255.0
    return arr


def edge_density(img, threshold=0.12):
    """
    Stima semplice della quantità di bordi usando gradienti numerici.

    Non è Canny, ma è sufficiente per confrontare immagini candidate.
    """
    arr = grayscale_array(img)

    gy, gx = np.gradient(arr)
    grad_mag = np.sqrt(gx**2 + gy**2)

    density = np.mean(grad_mag > threshold)

    return round(float(density), 4)


def texture_score(img):
    """
    Stima del dettaglio locale.

    Usiamo la deviazione standard dei gradienti:
    - bassa: immagine liscia, pochi dettagli
    - alta: molte texture, dettagli fini, oggetti complessi
    """
    arr = grayscale_array(img)

    gy, gx = np.gradient(arr)
    grad_mag = np.sqrt(gx**2 + gy**2)

    score = np.std(grad_mag)

    return round(float(score), 4)


# ============================================================
# 4. Classificazione euristica L1-L4
# ============================================================


def classify_candidate(color_score, entropy_norm, dominant_conc, edge_dens, texture):
    """
    Classificazione euristica.

    Attenzione:
    questa NON capisce il significato semantico dell'immagine.
    Serve solo per ordinare le candidate.
    """

    # L4 va controllato prima di L3: una scena urbana/affollata puo' avere
    # entropia cromatica media ma restare semanticamente difficile per una LUT.
    if (
        color_score >= 600
        and edge_dens >= 0.10
        and texture >= 0.06
    ) or (
        color_score >= 500
        and edge_dens >= 0.18
    ) or (
        color_score >= 550
        and edge_dens >= 0.09
        and texture >= 0.06
    ):
        return "L4_candidate"

    # L1: pochi colori, dominanti forti, pochi dettagli.
    if (
        color_score < 250
        and entropy_norm < 0.45
        and dominant_conc > 55
        and edge_dens < 0.08
    ):
        return "L1_candidate"

    # L2: ricchezza cromatica reale, ma struttura non estrema.
    # Non richiediamo entropia altissima: foto naturali con ombre o sfondi
    # ampi possono essere buoni casi L2 anche con entropia intorno a 0.44.
    if (
        color_score >= 430
        and entropy_norm >= 0.44
        and dominant_conc <= 55
        and edge_dens < 0.09
        and texture < 0.065
    ) or (
        color_score >= 400
        and entropy_norm >= 0.38
        and dominant_conc <= 55
        and edge_dens < 0.03
        and texture < 0.035
    ):
        return "L2_candidate"

    # L3: complessita' intermedia/alta, dettaglio localizzato,
    # possibile persona/oggetto delicato da confermare visivamente.
    if 220 <= color_score <= 650 and 0.38 <= entropy_norm <= 0.70 and edge_dens >= 0.05:
        return "L3_candidate"

    return "uncertain"


def complexity_index(color_score, entropy_norm, edge_dens, texture):
    """
    Indice unico solo per ordinamento.
    Non va presentato come metrica scientifica forte.
    """
    score = (
        0.40 * min(color_score / 800, 1.0)
        + 0.30 * entropy_norm
        + 0.20 * min(edge_dens / 0.15, 1.0)
        + 0.10 * min(texture / 0.10, 1.0)
    )

    return round(float(score), 3)


# ============================================================
# 5. Analisi cartella
# ============================================================


def analyze_image(path, target_resolution=(1008, 672)):
    img = Image.open(path)
    w, h = img.size

    closest_ratio, ratio, ratio_error = aspect_ratio_label(w, h)

    color_score = color_complexity(img)
    entropy, entropy_norm = color_entropy(img)
    dom_colors = dominant_colors(img)
    dom_conc = dominant_color_concentration(img)
    colorfulness = colorfulness_score(img)
    luminance = luminance_stats(img)

    edges = edge_density(img)
    texture = texture_score(img)

    suggested = classify_candidate(
        color_score=color_score,
        entropy_norm=entropy_norm,
        dominant_conc=dom_conc,
        edge_dens=edges,
        texture=texture,
    )

    comp_idx = complexity_index(
        color_score=color_score,
        entropy_norm=entropy_norm,
        edge_dens=edges,
        texture=texture,
    )

    target_w, target_h = target_resolution

    row = {
        "file": path.name,
        "width": w,
        "height": h,
        "megapixels": round((w * h) / 1_000_000, 2),
        "aspect_ratio": round(ratio, 4),
        "closest_ratio": closest_ratio,
        "ratio_error": round(ratio_error, 4),
        "orientation": "landscape" if w > h else "portrait" if h > w else "square",
        "crop_loss_1_1_%": crop_loss_to_ratio(w, h, 1.0),
        "crop_loss_4_3_%": crop_loss_to_ratio(w, h, 4 / 3),
        "crop_loss_3_2_%": crop_loss_to_ratio(w, h, 3 / 2),
        "crop_loss_16_9_%": crop_loss_to_ratio(w, h, 16 / 9),
        "resolution_scale_vs_target": resize_loss_to_target(w, h, target_w, target_h),
        "color_complexity_score": color_score,
        "color_entropy": entropy,
        "color_entropy_norm": entropy_norm,
        "dominant_color_concentration_%": dom_conc,
        "dominant_colors": ", ".join(dom_colors),
        "colorfulness_score": colorfulness,
        **luminance,
        "edge_density": edges,
        "texture_score": texture,
        "complexity_index": comp_idx,
        "suggested_level": suggested,
    }

    return row


def analyze_folder(folder, target_resolution=(1008, 672)):
    folder = Path(folder)
    rows = []

    for path in sorted(folder.iterdir()):
        if path.suffix.lower() not in IMAGE_EXTS:
            continue

        try:
            row = analyze_image(path, target_resolution=target_resolution)
            rows.append(row)

        except Exception as e:
            print(f"Errore con {path.name}: {e}")

    df = pd.DataFrame(rows)

    if len(df) == 0:
        return df

    df = df.sort_values(
        by=[
            "suggested_level",
            "complexity_index",
            "crop_loss_3_2_%",
        ],
        ascending=[True, True, True],
    )

    return df


def level_description(level):
    descriptions = {
        "L1_candidate": "pochi colori, regioni uniformi",
        "L2_candidate": "molti colori, difficolta' cromatica media",
        "L3_candidate": "complessita' intermedia/alta, dettagli delicati",
        "L4_candidate": "scena complessa, possibile stress test",
        "uncertain": "classificazione incerta, da ispezionare a mano",
    }

    return descriptions.get(level, "livello non riconosciuto")


def compact_level(level):
    return level.replace("_candidate", "")


def original_filename(name):
    """
    Rimuove un eventuale prefisso Lx_NN_ gia' generato dallo script.
    In questo modo il rename resta idempotente quando rilanciamo quality.py.
    """
    match = LEVEL_PREFIX_RE.match(name)
    if match:
        return match.group(1)
    return name


def rename_images_by_level(df, folder):
    """
    Rinomina le immagini classificate L1-L4 con formato:
    L<livello>_<progressivo>_<nome_originale>

    Le immagini uncertain restano senza prefisso di livello.
    """
    if df.empty:
        return []

    folder = Path(folder)
    sorted_df = df.copy()
    sorted_df["_original_file"] = sorted_df["file"].map(original_filename)
    sorted_df = sorted_df.sort_values(
        by=["suggested_level", "complexity_index", "crop_loss_3_2_%", "_original_file"],
        ascending=[True, True, True, True],
    )

    counters = {level: 0 for level in RENAMED_LEVELS}
    plan = []

    for _, row in sorted_df.iterrows():
        old_name = row["file"]
        level = compact_level(row["suggested_level"])
        base_name = original_filename(old_name)

        if level in RENAMED_LEVELS:
            counters[level] += 1
            new_name = f"{level}_{counters[level]:02d}_{base_name}"
        else:
            new_name = base_name

        plan.append((old_name, new_name))

    desired_names = [new_name for _, new_name in plan]
    if len(desired_names) != len(set(desired_names)):
        raise ValueError("Rename annullato: due immagini produrrebbero lo stesso nome.")

    existing_names = {path.name for path in folder.iterdir() if path.is_file()}
    old_names = {old_name for old_name, _ in plan}
    for old_name, new_name in plan:
        if old_name == new_name:
            continue
        if new_name in existing_names and new_name not in old_names:
            raise FileExistsError(
                f"Rename annullato: esiste gia' un file chiamato {new_name}."
            )

    changed = [(old_name, new_name) for old_name, new_name in plan if old_name != new_name]
    if not changed:
        return []

    temp_plan = []
    for index, (old_name, new_name) in enumerate(changed, start=1):
        old_path = folder / old_name
        temp_path = folder / f".quality_rename_tmp_{index}_{old_name}"
        while temp_path.exists():
            temp_path = folder / f".quality_rename_tmp_{index}_{temp_path.name}"

        old_path.rename(temp_path)
        temp_plan.append((temp_path, folder / new_name, old_name, new_name))

    renames = []
    for temp_path, new_path, old_name, new_name in temp_plan:
        temp_path.rename(new_path)
        renames.append((old_name, new_name))

    return renames


def apply_rename_map(df, renames):
    if df.empty or not renames:
        return df

    rename_map = dict(renames)
    renamed_df = df.copy()
    renamed_df["file"] = renamed_df["file"].map(lambda name: rename_map.get(name, name))
    return renamed_df


def metric_bar(value, max_value=1.0, width=18):
    ratio = 0 if max_value == 0 else value / max_value
    ratio = max(0.0, min(float(ratio), 1.0))
    filled = round(ratio * width)
    return "#" * filled + "-" * (width - filled)


def print_summary(df_sorted, output_csv, output_sorted_csv, target_resolution):
    target_w, target_h = target_resolution
    level_counts = df_sorted["suggested_level"].value_counts().sort_index()

    print()
    print("ANALISI IMMAGINI CANDIDATE")
    print("=" * 80)
    print(f"Immagini analizzate : {len(df_sorted)}")
    print(f"Target progetto     : {target_w}x{target_h}")
    print(f"CSV completo        : {output_csv}")
    print(f"CSV ordinato        : {output_sorted_csv}")
    print()
    print("Distribuzione livelli")
    print("-" * 80)
    for level, count in level_counts.items():
        print(f"- {compact_level(level):<10} {count:>3}  {level_description(level)}")


def print_compact_ranking(df_sorted):
    ranking = df_sorted.copy()
    ranking.insert(0, "#", range(1, len(ranking) + 1))
    ranking["level"] = ranking["suggested_level"].map(compact_level)

    columns = {
        "#": "#",
        "level": "level",
        "complexity_index": "complex",
        "crop_loss_3_2_%": "crop 3:2",
        "color_complexity_score": "colors",
        "color_entropy_norm": "entropy",
        "colorfulness_score": "colorful",
        "edge_density": "edges",
        "file": "file",
    }

    print()
    print("Classifica compatta")
    print("-" * 80)
    with pd.option_context(
        "display.max_columns",
        None,
        "display.width",
        140,
        "display.max_colwidth",
        42,
    ):
        print(ranking[list(columns.keys())].rename(columns=columns).to_string(index=False))


def print_image_card(index, row):
    level = row["suggested_level"]
    complexity = row["complexity_index"]
    entropy = row["color_entropy_norm"]
    dominant_conc = row["dominant_color_concentration_%"]
    edges = row["edge_density"]
    texture = row["texture_score"]

    print()
    print(f"[{index}] {row['file']}")
    print("-" * 80)
    print(f"Livello suggerito : {compact_level(level)} - {level_description(level)}")
    print(
        "Dimensioni        : "
        f"{row['width']}x{row['height']} px, "
        f"{row['megapixels']} MP, "
        f"{row['orientation']}, ratio vicino a {row['closest_ratio']}"
    )
    print(
        "Preparazione      : "
        f"crop 3:2 {row['crop_loss_3_2_%']}%, "
        f"scala vs target {row['resolution_scale_vs_target']}x"
    )
    print(
        "Complessita'      : "
        f"{complexity:.3f} [{metric_bar(complexity)}]"
    )
    print(
        "Colore            : "
        f"{row['color_complexity_score']} bin RGB, "
        f"entropia {entropy:.3f} [{metric_bar(entropy)}], "
        f"top colori {dominant_conc:.2f}%, "
        f"colorfulness {row['colorfulness_score']:.2f}"
    )
    print(
        "Luminanza         : "
        f"media {row['luminance_mean']:.3f}, "
        f"ombre {row['shadow_fraction_%']:.2f}%, "
        f"alte luci {row['highlight_fraction_%']:.2f}%"
    )
    print(
        "Struttura         : "
        f"bordi {edges:.4f} [{metric_bar(edges, max_value=0.15)}], "
        f"texture {texture:.4f} [{metric_bar(texture, max_value=0.10)}]"
    )
    print("Colori dominanti  :")
    for color in row["dominant_colors"].split(", "):
        print(f"  - {color}")


def print_legend():
    print()
    print("Legenda rapida")
    print("-" * 80)
    print("- complexity_index: indice euristico per ordinare le immagini, non metrica scientifica.")
    print("- crop 3:2: percentuale di area persa con center crop verso il formato scelto.")
    print("- entropy: distribuzione dei colori; alta significa colori piu' vari e meno dominanti.")
    print("- colorfulness: vividezza cromatica stimata; aiuta a leggere meglio i casi con molti bin RGB.")
    print("- luminanza: quota di ombre/alte luci; puo' spiegare entropia bassa in scene complesse.")
    print("- edges/texture: stima semplice della complessita' strutturale dell'immagine.")


def print_rename_report(renames):
    print()
    print("Rename immagini")
    print("-" * 80)

    if not renames:
        print("Nessun rename necessario.")
        return

    print(f"File rinominati: {len(renames)}")
    for old_name, new_name in renames:
        print(f"- {old_name} -> {new_name}")


def print_terminal_report(df, df_sorted, output_csv, output_sorted_csv, target_resolution, renames):
    """
    Stampa un report leggibile quando lo script viene eseguito da terminale.
    """
    if df.empty:
        print("Nessuna immagine analizzata.")
        print("Controlla che la cartella esista e contenga file immagine supportati.")
        return

    print_rename_report(renames)
    print_summary(df_sorted, output_csv, output_sorted_csv, target_resolution)
    print_compact_ranking(df_sorted)
    print()
    print("Schede immagini")
    print("=" * 80)
    for index, (_, row) in enumerate(df_sorted.iterrows(), start=1):
        print_image_card(index, row)
    print_legend()


# ============================================================
# 6. Uso
# ============================================================

def build_parser():
    parser = argparse.ArgumentParser(
        description="Analyze candidate images and write classification CSV files."
    )
    parser.add_argument("--input-dir", type=Path, default=Path("downloads"))
    parser.add_argument("--output-dir", type=Path, default=Path("images"))
    parser.add_argument(
        "--rename",
        action="store_true",
        help="Rename images in-place using the suggested L1-L4 level prefix.",
    )
    return parser


def main():
    args = build_parser().parse_args()
    folder = args.input_dir

    # Scegli una target resolution unica per il progetto.
    # 1008x672 mantiene il 3:2 ed e' multiplo di 16, comodo per pipeline diffusion.
    target_resolution = (1008, 672)

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    output_csv = output_dir / "classification.csv"
    output_sorted_csv = output_dir / "classification_sorted.csv"

    df = analyze_folder(folder, target_resolution=target_resolution)
    renames = rename_images_by_level(df, folder) if args.rename else []
    df = apply_rename_map(df, renames)
    df.to_csv(output_csv, index=False)

    if df.empty:
        df_sorted = df
    else:
        df_sorted = df.sort_values(
            by=["complexity_index", "crop_loss_3_2_%"], ascending=[True, True]
        )
    df_sorted.to_csv(output_sorted_csv, index=False)

    print_terminal_report(
        df=df,
        df_sorted=df_sorted,
        output_csv=output_csv,
        output_sorted_csv=output_sorted_csv,
        target_resolution=target_resolution,
        renames=renames,
    )


if __name__ == "__main__":
    main()
