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
