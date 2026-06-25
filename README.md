# Color Adjustments: diffusion image-to-image e 3D LUT

Repository per lo studio sperimentale di una domanda di Computer Graphics:

> Quanto della trasformazione cromatica prodotta da un diffusion model
> image-to-image puo' essere approssimato da una 3D LUT globale?

Il progetto genera target ricolorati con FLUX.2, stima una 3D LUT separata per
ogni coppia immagine originale / target diffusion, applica la LUT
all'originale e confronta la ricostruzione con il target. L'obiettivo non e'
sostituire il modello generativo, ma capire quando il suo output e' spiegabile
come una trasformazione globale `RGB -> RGB` e quando invece contiene modifiche
spaziali, strutturali o semantiche.

La relazione completa e' in [`paper/paper.md`](paper/paper.md) e
[`paper/paper.pdf`](paper/paper.pdf).

## Esempio

Per ogni immagine selezionata vengono generati quattro target image-to-image,
uno per prompt di color grading. La griglia seguente mostra i target finali:
righe per immagine, colonne per prompt.

![Target FLUX finali](images_flux/target_grid.jpg)

Prima del fitting LUT i target vengono controllati rispetto agli originali, per
capire se FLUX ha conservato abbastanza struttura e contenuto da rendere il caso
interpretabile come color adjustment.

![Controllo qualita' target image-to-image](images_flux/i2i_quality_targets_grid.jpg)

La fase LUT campiona coppie di pixel corrispondenti, stima piu' varianti di 3D
LUT, applica la trasformazione all'originale e confronta target FLUX e
ricostruzione. Questo caso semplice mostra una trasformazione fredda ben
approssimata da una LUT globale.

![Caso favorevole: L1_foglia / p03](images_lut/L1_foglia/p03_cold_winter_grade/best_summary.png)

Nei casi semanticamente o strutturalmente piu' complessi, gli errori si
concentrano su texture, riflessi, insegne, persone, bordi e dettagli locali:
sono proprio le componenti che una LUT globale non puo' rappresentare.

![Caso limite: L4_citta / p03](images_lut/L4_citta/p03_cold_winter_grade/best_summary.png)

## Pipeline

La pipeline segue questi passaggi:

1. scarica e prepara immagini candidate;
2. classifica le immagini in livelli sperimentali L1-L4;
3. genera target FLUX image-to-image con prompt di color grading;
4. valuta la stabilita' dei target rispetto agli originali;
5. campiona coppie `RGB_originale -> RGB_target`;
6. stima 3D LUT con piu' dimensioni e metodi di fitting;
7. applica le LUT all'immagine originale;
8. confronta target diffusion e ricostruzione LUT con PSNR, SSIM e Delta E;
9. genera CSV, ranking, contact sheet e figure per la relazione.

Nel workspace usato per il paper sono presenti:

- 8 immagini preparate a `1008x672`;
- 4 prompt di color grading;
- 32 target FLUX finali;
- 18 varianti LUT per ciascun caso immagine/prompt;
- 576 righe metriche complessive in `images_lut/summary_all.csv`.

## File principali

- `paper/paper.md`: relazione tecnica principale.
- `paper/paper.pdf`: PDF generato dalla relazione.
- `paper/catalogo_immagini.md` e `paper/catalogo_immagini.pdf`: catalogo
  visuale esteso con originali, target e migliori ricostruzioni.
- `configs/images.yaml`: immagini candidate e immagini finali selezionate.
- `configs/prompts.yaml`: prompt di color grading usati con FLUX.
- `main.py`: entry point CLI della pipeline.
- `utils/data/`: download, classificazione e preparazione immagini.
- `utils/flux/`: generazione target, griglie e valutazione image-to-image.
- `utils/lut_pipeline/`: fitting, applicazione e report delle 3D LUT.
- `images/`: immagini selezionate e preprocessate.
- `images_flux/target/`: target FLUX finali e metadati.
- `images_lut/`: ricostruzioni LUT, metriche, heatmap e summary.
- `flux_model/iris.c/`: implementazione esterna vendorizzata usata per FLUX.

## Setup

Il progetto usa `uv` per gestire ambiente e dipendenze.

```bash
uv venv
source .venv/bin/activate
uv sync
```

Per rigenerare `paper/paper.pdf` e `paper/catalogo_immagini.pdf` servono anche
`pandoc` e una distribuzione LaTeX con `xelatex` disponibile nel `PATH`.

La generazione FLUX richiede inoltre l'eseguibile e il modello locale dentro
`flux_model/iris.c/`, in particolare la configurazione usata nel paper:

```text
flux_model/iris.c/iris
flux_model/iris.c/flux-klein-4b-base
```

## Comandi Just

Elenco completo:

```bash
just --list
```

Pipeline dati e immagini:

```bash
just download-images
just classify-images
just prepare-images
```

Generazione e controllo dei target FLUX:

```bash
just generate-previews
just evaluate-preview
just generate-targets
just evaluate-targets
just flux-target-grid
```

Fitting LUT e report:

```bash
just lut-all
just report-assets
```

Relazione e catalogo:

```bash
just paper
just catalog
```

Validazione leggera di configurazioni e codice:

```bash
just check
```

## CLI

I target `just` richiamano `main.py`. Se serve invocare direttamente la CLI:

```bash
uv run python main.py prepare
uv run python main.py generate-targets
uv run python main.py evaluate-targets
uv run python main.py lut
uv run python main.py report
```

La lista dei comandi disponibili e':

```bash
uv run python main.py --help
```

## Metodo LUT

Ogni LUT e' stimata da coppie di pixel allineati:

```text
RGB_originale(x, y) -> RGB_target_FLUX(x, y)
```

Per ogni caso vengono campionati fino a `200000` pixel e vengono provate:

- dimensioni `17^3`, `33^3`, `65^3`;
- fitting `mean`, `median`, `weighted_mean`;
- applicazione `nearest` e `trilinear`.

La variante migliore in media secondo Delta E CIEDE2000 nel paper e':

```text
65^3 weighted_mean trilinear
```

Sui 32 casi finali questa variante ottiene in media PSNR `24.387`, SSIM
`0.7744`, Delta E medio `4.836` e Delta E p95 `14.316`.

## Risultato sperimentale

I risultati confermano una distinzione netta:

- quando FLUX produce soprattutto un color grading globale, la LUT ricostruisce
  bene il target;
- quando FLUX modifica texture, materiali, pelle, riflessi, dettagli urbani o
  regioni semanticamente diverse, l'errore della LUT aumenta;
- una LUT globale non puo' distinguere due pixel con lo stesso RGB di partenza
  ma significato o posizione diversi.

La conclusione del paper e' quindi parziale ma chiara: una 3D LUT globale,
stimata caso per caso, spiega bene la componente cromatica globale del target
diffusion, ma non la componente generativa o content-aware.

## Crediti e materiali di terze parti

I target image-to-image sono stati generati con FLUX.2 Klein tramite
`flux_model/iris.c`, implementazione locale di Salvatore Sanfilippo / antirez
inclusa come dipendenza esterna vendorizzata. La repository originale e':
https://github.com/antirez/iris.c. Il codice in `flux_model/` non e' parte
originale della pipeline del progetto.

Le immagini principali provengono dal MIT-Adobe FiveK Dataset. Le due immagini
di tramonto provengono da Unsplash:

- `tramonto_mare`: https://unsplash.com/photos/JE01L3hB0GQ
- `tramonto_lago`: https://unsplash.com/photos/qkfxBc2NQ18

Gli asset generati in `images_flux/`, `images_lut/` e `paper/` sono artefatti
di esperimento e documentazione.

## Nota sull'implementazione

Implementazione della pipeline, organizzazione degli esperimenti,
documentazione e parte della relazione sono stati sviluppati con assistenza di
strumenti di programmazione automatica.
