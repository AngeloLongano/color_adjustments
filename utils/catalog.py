from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from typing import Iterable

import yaml
from PIL import Image


DEFAULT_OUTPUT = Path("paper/catalogo_immagini.md")


def write_catalog_markdown(
    output_path: Path = DEFAULT_OUTPUT,
    images_dir: Path = Path("images"),
    flux_dir: Path = Path("images_flux/target"),
    lut_dir: Path = Path("images_lut"),
    prompts_path: Path = Path("configs/prompts.yaml"),
) -> Path:
    prompts = _read_prompts(prompts_path)
    originals = _read_manifest_images(images_dir / "manifest.csv", images_dir)
    best_rows = _read_best_lut_rows(lut_dir)

    lines: list[str] = []
    lines.extend(_front_matter())
    lines.extend(
        [
            "# Catalogo immagini sperimentali",
            "",
            (
                "Appendice visiva generata automaticamente dagli asset della "
                "pipeline. Le immagini sono inserite una per blocco, senza "
                "crop e con aspect ratio preservato."
            ),
            "",
            f"Data generazione: {date.today().isoformat()}",
            "",
            "\\clearpage",
            "",
        ]
    )

    lines.extend(
        _section_break(
            "Prompt usati",
            "Le quattro richieste di color grading applicate a tutte le immagini.",
        )
    )
    lines.extend(_prompts_section(prompts))
    lines.extend(
        _section_break(
            "Originali preparati",
            "Immagini di partenza gia' ridimensionate dalla pipeline.",
        )
    )
    lines.extend(_originals_section(originals))
    lines.extend(
        _section_break(
            "Target FLUX",
            "Risultati image-to-image generati per ogni coppia immagine-prompt.",
        )
    )
    lines.extend(_flux_section(originals, prompts, flux_dir))
    lines.extend(
        _section_break(
            "Risultati LUT",
            (
                "Per ogni target viene mostrata la migliore ricostruzione LUT "
                "selezionata per Delta E CIEDE2000 medio."
            ),
        )
    )
    lines.extend(_best_lut_section(best_rows))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output_path


def _front_matter() -> list[str]:
    return [
        "---",
        'title-meta: "Catalogo immagini sperimentali"',
        'author-meta: "Angelo Longano"',
        'lang: "it"',
        "toc: true",
        "numbersections: false",
        "colorlinks: true",
        'geometry: "a4paper,margin=1.2cm,landscape"',
        "fontsize: 10pt",
        "header-includes:",
        "  - \\usepackage{xcolor}",
        "  - \\usepackage{graphicx}",
        "  - \\usepackage{float}",
        "  - \\setlength{\\parindent}{0pt}",
        "  - \\setlength{\\parskip}{0.35em}",
        "---",
        "",
    ]


def _section_break(title: str, subtitle: str) -> list[str]:
    return [
        "\\clearpage",
        "\\thispagestyle{empty}",
        "\\vspace*{0.22\\textheight}",
        "\\begin{center}",
        f"{{\\Huge\\bfseries {_latex_escape(title)}}}",
        "\\vspace{0.8cm}",
        "",
        f"{{\\Large {_latex_escape(subtitle)}}}",
        "\\vspace{0.9cm}",
        "",
        "\\textcolor[HTML]{2563EB}{\\rule{0.52\\textwidth}{1.1pt}}",
        "\\end{center}",
        "\\clearpage",
        "",
    ]


def _read_prompts(path: Path) -> dict[str, str]:
    with path.open(encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    return {str(key): " ".join(str(value).split()) for key, value in data.items()}


def _read_manifest_images(manifest_path: Path, images_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with manifest_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            path = images_dir / row["output_file"]
            if not path.exists():
                continue
            rows.append(
                {
                    "image_id": path.stem,
                    "image_key": row["image_key"],
                    "level": row["level"],
                    "path": path.as_posix(),
                    "source_file": row["source_file"],
                    "size": _image_size_label(path),
                }
            )
    return rows


def _read_best_lut_rows(lut_dir: Path) -> list[dict[str, str]]:
    best_path = lut_dir / "best_by_delta_e.csv"
    if best_path.exists():
        with best_path.open(newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        return sorted(rows, key=lambda row: (row["image_id"], row["prompt_id"]))

    summary_path = lut_dir / "summary_all.csv"
    if not summary_path.exists():
        return []

    best_by_case: dict[tuple[str, str], dict[str, str]] = {}
    with summary_path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            key = (row["image_id"], row["prompt_id"])
            current = best_by_case.get(key)
            if current is None or _float(row["delta_e_mean"]) < _float(
                current["delta_e_mean"]
            ):
                best_by_case[key] = row
    return [best_by_case[key] for key in sorted(best_by_case)]


def _originals_section(originals: Iterable[dict[str, str]]) -> list[str]:
    lines = ["# Originali preparati", ""]
    for row in originals:
        caption = (
            f"{row['image_id']} - {row['level']} - "
            f"{row['image_key']} - {row['size']}"
        )
        lines.extend(
            [
                f"## {row['image_id']}",
                "",
                f"File sorgente: `{row['source_file']}`  ",
                f"File preparato: `{row['path']}`  ",
                f"Dimensioni: {row['size']}",
                "",
                _image(row["path"], caption, "0.98\\textwidth", "0.78\\textheight"),
                "",
                "\\clearpage",
                "",
            ]
        )
    return lines


def _flux_section(
    originals: Iterable[dict[str, str]],
    prompts: dict[str, str],
    flux_dir: Path,
) -> list[str]:
    lines = ["# Target generati da FLUX", ""]
    prompt_ids = list(prompts)

    for original in originals:
        image_id = original["image_id"]
        lines.extend([f"## {image_id}", ""])
        for prompt_id in prompt_ids:
            target_path = _find_flux_target(flux_dir, image_id, prompt_id)
            if target_path is None:
                lines.extend([f"### {prompt_id}", "", "Target non trovato.", ""])
                continue

            caption = f"{image_id} / {prompt_id} - { _image_size_label(target_path) }"
            lines.extend(
                [
                    f"### {prompt_id}",
                    "",
                    f"File: `{target_path.as_posix()}`  ",
                    f"Dimensioni: {_image_size_label(target_path)}",
                    "",
                    _image(
                        target_path.as_posix(),
                        caption,
                        "0.98\\textwidth",
                        "0.78\\textheight",
                    ),
                    "",
                    "\\clearpage",
                    "",
                ]
            )
    return lines


def _best_lut_section(rows: Iterable[dict[str, str]]) -> list[str]:
    lines = [
        "# Risultati LUT: migliore ricostruzione per Delta E CIEDE2000 medio",
        "",
        (
            "Questa sezione mette in evidenza il risultato principale del "
            "fitting: per ogni target FLUX viene mostrata la variante LUT "
            "migliore secondo il Delta E CIEDE2000 medio."
        ),
        "",
    ]
    for row in rows:
        title = f"{row['image_id']} / {row['prompt_id']}"
        reconstruction_path = row.get("reconstruction_path", "")

        lines.extend(
            [
                f"## {title}",
                "",
                _result_box(row),
                "",
            ]
        )

        if reconstruction_path and Path(reconstruction_path).exists():
            lines.extend(
                [
                    _image(
                        reconstruction_path,
                        f"Ricostruzione LUT best - {title}",
                        "0.98\\textwidth",
                        "0.62\\textheight",
                    ),
                    "",
                ]
            )

        lines.extend(["\\clearpage", ""])
    return lines


def _find_flux_target(flux_dir: Path, image_id: str, prompt_id: str) -> Path | None:
    image_dir = flux_dir / image_id
    matches = sorted(image_dir.glob(f"{prompt_id}_*.png"))
    return matches[0] if matches else None


def _metrics_line(row: dict[str, str]) -> str:
    return (
        f"Best: `{row.get('variant', 'n/a')}`; "
        f"PSNR RGB: {_fmt(row.get('rgb_psnr'))}; "
        f"SSIM: {_fmt(row.get('ssim', row.get('luma_ssim')))}; "
        f"Delta E medio: {_fmt(row.get('delta_e_mean'))}; "
        f"Delta E p95: {_fmt(row.get('delta_e_p95'))}."
    )


def _result_box(row: dict[str, str]) -> str:
    variant = _latex_escape(row.get("variant", "n/a"))
    lut_size = _latex_escape(row.get("lut_size", "n/a"))
    fit_method = _latex_escape(row.get("fit_method", "n/a"))
    apply_method = _latex_escape(row.get("apply_method", "n/a"))
    return "\n".join(
        [
            "\\begin{center}",
            "\\setlength{\\fboxsep}{8pt}",
            "\\fbox{\\begin{minipage}{0.88\\textwidth}",
            "\\textbf{Risultato ottenuto}\\\\[3pt]",
            f"Variante migliore: \\texttt{{{variant}}} "
            f"$(LUT={lut_size}^3, fit={fit_method}, apply={apply_method})$\\\\",
            (
                f"PSNR RGB: \\textbf{{{_fmt(row.get('rgb_psnr'))}}} \\quad "
                f"SSIM: \\textbf{{{_fmt(row.get('ssim', row.get('luma_ssim')))}}} \\quad "
                f"Delta E medio: \\textbf{{{_fmt(row.get('delta_e_mean'))}}} \\quad "
                f"Delta E p95: \\textbf{{{_fmt(row.get('delta_e_p95'))}}}"
            ),
            "\\end{minipage}}",
            "\\end{center}",
        ]
    )


def _prompts_section(prompts: dict[str, str]) -> list[str]:
    lines = ["# Prompt usati", ""]
    for prompt_id, prompt in prompts.items():
        lines.extend([f"- `{prompt_id}`: {prompt}"])
    lines.extend(["", "\\clearpage", ""])
    return lines


def _image(path: str, caption: str, width: str, height: str) -> str:
    return "\n".join(
        [
            "\\begin{center}",
            f"\\includegraphics[width={width},height={height},keepaspectratio]{{{path}}}\\\\[2pt]",
            f"{{\\small {_latex_escape(caption)}}}",
            "\\end{center}",
        ]
    )


def _image_size_label(path: Path) -> str:
    with Image.open(path) as image:
        return f"{image.width}x{image.height}px"


def _float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("inf")


def _fmt(value: str | None) -> str:
    if value is None or value == "":
        return "n/a"
    try:
        return f"{float(value):.3f}"
    except ValueError:
        return value


def _latex_escape(text: str) -> str:
    replacements = {
        "\\": "\\textbackslash{}",
        "&": "\\&",
        "%": "\\%",
        "$": "\\$",
        "#": "\\#",
        "_": "\\_",
        "{": "\\{",
        "}": "\\}",
        "~": "\\textasciitilde{}",
        "^": "\\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)
