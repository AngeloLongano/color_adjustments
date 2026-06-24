set shell := ["bash", "-cu"]

download-images:
    uv run python main.py download

classify-images:
    uv run python main.py classify

prepare-images:
    uv run python main.py prepare

generate-previews:
    uv run python main.py generate-previews

evaluate-preview:
    uv run python main.py evaluate-preview

generate-targets:
    uv run python main.py generate-targets

flux:
    caffeinate -dimsu uv run python main.py generate-targets

evaluate-targets:
    uv run python main.py evaluate-targets

flux-grid:
    uv run python main.py flux-grid

flux-target-grid:
    uv run python main.py flux-grid --flux-dir images_flux/target --output images_flux/target_grid.jpg

lut-all:
    uv run python main.py lut

report-assets:
    uv run python main.py report

pipeline:
    uv run python main.py pipeline

check:
    uv run python -c "import yaml; yaml.safe_load(open('configs/images.yaml'))"
    uv run python -c "import yaml; yaml.safe_load(open('configs/prompts.yaml'))"
    uv run python -m compileall -q main.py utils

check-assets:
    test -f images_flux/target_grid.jpg
    test -f images_flux/i2i_quality_targets_grid.jpg
    test -f images_lut/metrics_by_lut_size.csv
    test -f images_lut/metrics_by_variant.csv
    test -f images_lut/best_by_delta_e.csv
    test -f images_lut/L1_foglia/p03_cold_winter_grade/best_summary.png
    test -f images_lut/L2_fiori/p01_warm_cinematic/best_summary.png
    test -f images_lut/L2_tramonto_lago/p03_cold_winter_grade/best_summary.png
    test -f images_lut/L3_ragazzi/p01_warm_cinematic/best_summary.png
    test -f images_lut/L4_bracciali/p02_teal_orange/best_summary.png
    test -f images_lut/L4_citta/p03_cold_winter_grade/best_summary.png

paper-pdf:
    pandoc paper/paper.md --pdf-engine=xelatex -V documentclass=article -V geometry:margin=2.5cm --resource-path=.:paper -o paper/paper.pdf

paper: check-assets paper-pdf

catalog-md:
    uv run python main.py catalog

catalog-pdf: catalog-md
    pandoc paper/catalogo_immagini.md --pdf-engine=xelatex -V documentclass=article --resource-path=. -o paper/catalogo_immagini.pdf

catalog: catalog-pdf
