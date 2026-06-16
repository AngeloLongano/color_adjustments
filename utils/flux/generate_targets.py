import argparse
import json
import subprocess
from pathlib import Path
import sys
import time
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.common.image_io import read_config

# ==========================================
# CONFIGURATION
# ==========================================

SEED = 0
IRIS_DIR = Path("flux_model/iris.c")
IRIS_BIN = IRIS_DIR / "iris"

MODEL_DICT = {
    "flux-klein-4b": {
        "path": IRIS_DIR / "flux-klein-4b",
        "extra_args": ["-s", "4"],
    },
    "flux-klein-4b-base": {
        "path": IRIS_DIR / "flux-klein-4b-base",
        "extra_args": ["-s", "10", "--linear"],
    },
}

RUN_SETTINGS = {
    "preview": {
        "width": 384,
        "height": 256,
        "output_dir": "images_flux/preview",
        "save_log": False,
    },
    "targets": {
        "width": 1008,
        "height": 672,
        "output_dir": "images_flux/target",
        "save_log": True,
    },
}

INPUT_DIR = "images"
DEFAULT_IMAGES_CONFIG = Path("configs/images.yaml")
DEFAULT_PROMPTS_CONFIG = Path("configs/prompts.yaml")

# ==========================================
# SCRIPT
# ==========================================


def load_json(path: Path) -> dict:
    return read_config(path)


def get_images_to_process(image_keys: list[str] | str):
    input_dir_path = Path(INPUT_DIR)
    if image_keys == "all":
        # Cerca tutti i png nelle immagini normalizzate.
        return [p for p in input_dir_path.glob("*.png")]
    else:
        paths = [resolve_prepared_image(input_dir_path, img) for img in image_keys]
        missing = [path for path in paths if not path.exists()]
        if missing:
            missing_text = "\n".join(f"- {path}" for path in missing)
            raise FileNotFoundError(
                "Prepared input images are missing. Run `just prepare-images` first, "
                "or remove those keys from configs/images.yaml selected_images:\n"
                f"{missing_text}"
            )
        return paths


def resolve_prepared_image(input_dir: Path, value: str) -> Path:
    image_name = Path(value)
    if image_name.suffix:
        return input_dir / image_name

    direct = input_dir / f"{value}.png"
    if direct.exists():
        return direct

    matches = sorted(input_dir.glob(f"L[1-4]_{value}.png"))
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ValueError(f"Multiple prepared images match '{value}': {matches}")

    return direct


def images_from_config(config: dict, selection: str) -> list[str]:
    if selection == "all":
        keys = list(config.get("candidate_images", {}).keys())
    else:
        keys = config.get(selection)
    if not isinstance(keys, list):
        raise ValueError(f"Selection '{selection}' is not a list in images config")
    return [str(key) for key in keys]


def parse_args() -> argparse.Namespace:
    prompt_dict = load_json(DEFAULT_PROMPTS_CONFIG)
    parser = argparse.ArgumentParser(
        description="Generate Flux image-to-image previews or final targets."
    )
    parser.add_argument("--run-type", choices=RUN_SETTINGS.keys())
    parser.add_argument("--models", nargs="+", choices=MODEL_DICT.keys())
    parser.add_argument("--prompts", nargs="+", choices=prompt_dict.keys())
    parser.add_argument(
        "--images",
        nargs="+",
        help="Prepared image filenames or keys from configs/images.yaml.",
    )
    parser.add_argument(
        "--images-config",
        type=Path,
        default=DEFAULT_IMAGES_CONFIG,
    )
    parser.add_argument(
        "--prompts-config",
        type=Path,
        default=DEFAULT_PROMPTS_CONFIG,
    )
    parser.add_argument(
        "--image-selection",
        help="Config list to use, for example selected_images.",
    )
    return parser.parse_args()


def build_run_config(args: argparse.Namespace) -> tuple[dict, dict]:
    config = load_json(args.images_config)
    prompt_dict = load_json(args.prompts_config)
    run_config = {
        "run_type": args.run_type or config["run_type"],
        "models": args.models or config["models"],
        "prompts": args.prompts or config["prompts"],
        "images": config["selected_images"],
    }
    if args.image_selection:
        run_config["images"] = images_from_config(config, args.image_selection)
    elif args.images:
        run_config["images"] = args.images

    unknown_prompts = sorted(set(run_config["prompts"]) - set(prompt_dict))
    if unknown_prompts:
        raise KeyError(f"Unknown prompt ids in config: {unknown_prompts}")

    return run_config, prompt_dict


def iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def format_duration(seconds: float) -> str:
    total_seconds = max(0, int(round(seconds)))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def run_generation(run_config: dict, prompt_dict: dict) -> None:
    if not IRIS_BIN.exists():
        print(
            f"Errore: l'eseguibile {IRIS_BIN} non esiste. "
            f"Esegui 'make mps' in {IRIS_DIR}/"
        )
        return

    run_type = run_config["run_type"]
    settings = RUN_SETTINGS[run_type]

    images_to_process = get_images_to_process(run_config["images"])
    if not images_to_process:
        print(f"Nessuna immagine trovata in {INPUT_DIR}.")
        return

    print(f"=== Avvio generazione ({run_type}) ===")
    print(f"Immagini: {len(images_to_process)}")
    print(f"Modelli: {run_config['models']}")
    print(f"Prompts: {run_config['prompts']}")
    print(f"Seed: {SEED}")
    print(f"Risoluzione: {settings['width']}x{settings['height']}")
    print("======================================\n")

    for img_path in images_to_process:
        img_name_no_ext = img_path.stem

        # Crea la cartella di output per l'immagine
        out_img_dir = Path(settings["output_dir"]) / img_name_no_ext
        out_img_dir.mkdir(parents=True, exist_ok=True)

        for model_key in run_config["models"]:
            model_info = MODEL_DICT[model_key]

            for prompt_key in run_config["prompts"]:
                prompt_text = prompt_dict[prompt_key]
                model_path = Path(model_info["path"])

                for seed in [SEED]:
                    # Nome file stabile, con modello sempre incluso anche se il batch usa un solo modello.
                    model_suffix = f"_{model_key}"

                    out_filename = f"{prompt_key}_s{seed}{model_suffix}.png"
                    out_filepath = out_img_dir / out_filename
                    log_filepath = (
                        out_img_dir / f"{prompt_key}_s{seed}{model_suffix}.log"
                    )
                    metadata_filepath = (
                        out_img_dir / f"{prompt_key}_s{seed}{model_suffix}.json"
                    )

                    print(
                        f"Elaborazione: {img_name_no_ext} | Modello: {model_key} | Prompt: {prompt_key} | Seed: {seed}"
                    )

                    cmd = [
                        str(IRIS_BIN),
                        "-d",
                        str(model_path),
                        "-i",
                        str(img_path),
                        "-W",
                        str(settings["width"]),
                        "-H",
                        str(settings["height"]),
                        "-S",
                        str(seed),
                        "-p",
                        prompt_text,
                        "-o",
                        str(out_filepath),
                        "-v",
                    ]

                    # Aggiungi parametri specifici del modello (es. steps)
                    cmd.extend(model_info["extra_args"])

                    # Eseguiamo il comando mostrando l'output in tempo reale
                    start_time = time.monotonic()
                    started_at = iso_now()
                    metadata = {
                        "image": str(img_path),
                        "output": str(out_filepath),
                        "model_key": model_key,
                        "model_path": str(model_path),
                        "prompt_key": prompt_key,
                        "prompt_text": prompt_text,
                        "seed": seed,
                        "run_type": run_type,
                        "width": settings["width"],
                        "height": settings["height"],
                        "started_at": started_at,
                        "ended_at": None,
                        "duration_seconds": None,
                        "duration_hms": None,
                        "return_code": None,
                        "status": "running",
                        "command": cmd,
                    }
                    try:
                        log_file = (
                            open(log_filepath, "w") if settings["save_log"] else None
                        )

                        # Colori ANSI per distinguere l'output di iris (Ciano + Opaco)
                        PREFIX = "\033[96m[IRIS]\033[0m \033[2m"
                        SUFFIX = "\033[0m"

                        process = subprocess.Popen(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True,
                            bufsize=1,
                        )

                        for line in process.stdout:
                            if log_file:
                                log_file.write(line)
                            # Stampa la linea rimuovendo il newline finale, e aggiungendo i colori
                            print(f"{PREFIX}{line.rstrip()}{SUFFIX}", flush=True)

                        process.wait()
                        elapsed_seconds = time.monotonic() - start_time

                        if log_file:
                            log_file.close()

                        metadata["ended_at"] = iso_now()
                        metadata["duration_seconds"] = round(elapsed_seconds, 3)
                        metadata["duration_hms"] = format_duration(elapsed_seconds)
                        metadata["return_code"] = process.returncode
                        metadata["status"] = (
                            "completed" if process.returncode == 0 else "failed"
                        )
                        metadata_filepath.write_text(
                            json.dumps(metadata, indent=2, ensure_ascii=True) + "\n",
                            encoding="utf-8",
                        )

                        print(
                            f"  [Tempo] {metadata['duration_hms']} ({metadata['duration_seconds']} s)"
                        )

                        if process.returncode != 0:
                            print(
                                f"  \033[91m[Errore]\033[0m Comando fallito con codice {process.returncode}."
                            )

                    except Exception as e:
                        elapsed_seconds = time.monotonic() - start_time
                        metadata["ended_at"] = iso_now()
                        metadata["duration_seconds"] = round(elapsed_seconds, 3)
                        metadata["duration_hms"] = format_duration(elapsed_seconds)
                        metadata["status"] = "exception"
                        metadata["error"] = str(e)
                        metadata_filepath.write_text(
                            json.dumps(metadata, indent=2, ensure_ascii=True) + "\n",
                            encoding="utf-8",
                        )
                        print(
                            f"  \033[91m[Eccezione]\033[0m Errore durante l'esecuzione del modello: {e}"
                        )


def main():
    run_config, prompt_dict = build_run_config(parse_args())
    run_generation(run_config, prompt_dict)

    print("\n=== Generazione completata ===")


if __name__ == "__main__":
    main()
