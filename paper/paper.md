---
title-meta: "Approssimazione tramite 3D LUT di trasformazioni cromatiche image-to-image generate da diffusion model"
author-meta: "Angelo Longano"
date-meta: "20 giugno 2026"
lang: "it"
toc: false
numbersections: true
colorlinks: true
linkcolor: "blue"
urlcolor: "blue"
geometry: "margin=2.5cm"
fontsize: 11pt
header-includes:
  - \usepackage{xcolor}
  - \usepackage{graphicx}
  - \usepackage{float}
  - \setlength{\parindent}{0pt}
  - \setlength{\parskip}{0.55em}
---

\begin{titlepage}
\thispagestyle{empty}
\centering
\vspace*{0.25cm}

{\Huge\bfseries Color Adjustments\\[0.25cm]}
{\LARGE Approssimazione LUT di trasformazioni diffusion image-to-image\\[0.35cm]}
{\large Studio sperimentale su color mapping globali stimati caso per caso\\[0.45cm]}

\textcolor[HTML]{2563EB}{\rule{0.78\textwidth}{1.3pt}}

\vspace{0.5cm}

\includegraphics[width=0.62\textwidth,height=0.37\textheight,keepaspectratio]{images_flux/target_grid.jpg}

\vspace{0.45cm}

\begin{minipage}{0.84\textwidth}
\centering
\normalsize
Relazione tecnica sul confronto tra target prodotti da FLUX.2 in modalità
image-to-image e ricostruzioni ottenute applicando all'immagine originale
3D LUT stimate separatamente per ogni coppia originale-target.

\vspace{0.35cm}

Progetto realizzato per il corso di Computer Graphics della Laurea Magistrale
in Informatica, tenuto dal Prof. Fabio Pellacini presso l'Università degli
Studi di Modena e Reggio Emilia.
\end{minipage}

\vspace{0.45cm}

{\large\bfseries Angelo Longano\\[0.15cm]}
{\large Laurea Magistrale in Informatica - Unimore\\[0.15cm]}
{\large 20 giugno 2026}

\vspace*{0.3cm}
\end{titlepage}

\tableofcontents
\newpage

# Abstract

Questo progetto studia quanto della trasformazione cromatica prodotta da un
diffusion model image-to-image sia approssimabile con una 3D LUT. Nel testo,
per "trasformazione cromatica" si intende la componente di color grading del
target, non l'intero intervento generativo del modello. La domanda non è se
una LUT possa sostituire un modello generativo, ma se il target generato dal
modello contenga una componente spiegabile come semplice mappatura globale del
colore.

Sono state selezionate immagini fotografiche con difficoltà crescente, poi
preprocessate alla stessa risoluzione. Sono stati definiti quattro prompt di
color grading e, per ogni immagine e prompt, è stato generato un target con
FLUX.2 Klein tramite l'implementazione locale `iris.c`. Per ogni coppia
originale-target sono state campionate corrispondenze pixel-per-pixel e sono
state stimate più 3D LUT con dimensioni, metodi di fitting e interpolazioni
diverse. Le LUT sono state applicate all'immagine originale e la ricostruzione
è stata confrontata con il target FLUX.

Il confronto usa metriche in punti diversi della pipeline: selezione delle
immagini, controllo dei target FLUX e valutazione finale delle ricostruzioni
LUT. Le metriche principali sono PSNR RGB, SSIM standard multicanale,
Delta E CIEDE2000 e copertura della griglia LUT. I risultati mostrano
che una LUT stimata caso per caso approssima bene i target in cui FLUX applica
prevalentemente un color grading globale. La qualità peggiora quando il modello
modifica texture, dettagli locali, materiali o regioni semanticamente distinte.
In media la variante migliore per Delta E è `65^3 weighted_mean trilinear`,
mentre `33^3` risulta un compromesso più robusto tra accuratezza e copertura
della griglia.

# Introduzione

Una 3D LUT rappresenta una trasformazione del tipo:

$$
f: RGB_{in} \rightarrow RGB_{out}
$$

Il valore di uscita dipende solo dal colore del pixel. La posizione del pixel,
la struttura della scena e il significato dell'oggetto non sono osservabili
dalla LUT. Questo limite è anche il motivo per cui le LUT sono strumenti
efficaci e controllabili per il color grading: applicano una trasformazione
globale, coerente e computazionalmente economica.

In questo lavoro il termine "globale" indica solo questo vincolo: la LUT non
usa informazione spaziale o semantica e implementa una funzione `RGB -> RGB`.
Ogni LUT è però stimata separatamente per una specifica trasformazione
image-to-image, cioè per una particolare combinazione di immagine originale,
prompt e target diffusion. Non viene costruita una LUT unica per prompt, né
una LUT riutilizzabile su tutto il dataset.

Un diffusion model image-to-image ha invece accesso al contenuto visivo
dell'immagine e al testo del prompt. Anche quando il prompt chiede di preservare
la scena, il modello potrebbe modificare texture, materiali, ombre, dettagli o
piccole strutture locali. La trasformazione prodotta può quindi essere in parte
cromatica e in parte generativa. Non abbiamo totale controllo su questo.

La domanda sperimentale del progetto è:

$$
I_{target}^{diffusion} \simeq LUT(I_{originale}) \ ?
$$

Se la risposta è positiva, la trasformazione generata è compatibile con un
color mapping globale. Se la risposta è negativa, gli errori della LUT
indicano che il modello ha introdotto una componente spaziale, strutturale o
semantica non rappresentabile come semplice funzione `RGB -> RGB`.

In questo senso la LUT è usata anche come strumento di analisi. Separando ciò
che è approssimabile come trasformazione cromatica globale da ciò che resta
fuori dal modello LUT, gli errori aiutano a localizzare regioni in cui il target
FLUX non è spiegato bene da una funzione globale del colore. In molti casi
queste regioni sono compatibili con differenze legate a contenuto, posizione o
semantica della scena, anche se la metrica da sola non prova la causa.

# Pipeline sperimentale

La pipeline parte da un insieme di immagini candidate definite in
`configs/images.yaml`. Le candidate vengono scaricate, analizzate con metriche
euristiche di complessità cromatica e visiva, e classificate in livelli L1-L4.
Da questa analisi viene scelto manualmente un sottoinsieme finale, progettato
per coprire casi semplici, texture naturali, persone/materiali percettivamente
delicati e scene semanticamente dense.

La classificazione L1-L4 nasce prima come ipotesi sperimentale: ho definito
quattro livelli pensando a dove un diffusion model e una LUT globale avrebbero
potuto comportarsi in modo diverso. In un secondo momento questa idea è stata
resa parzialmente deterministica con uno script di ranking basato su metriche
cromatiche e strutturali. La scelta finale delle immagini è quindi un mix tra
criterio automatico e valutazione manuale: le metriche aiutano a ordinare le
candidate, ma non decidono da sole il valore sperimentale di una scena.

Tutte le immagini selezionate vengono convertite in RGB, ritagliate e
ridimensionate a `1008x672`. L'allineamento è importante perché il fitting
della LUT usa coppie di pixel corrispondenti: il colore dell'originale in una
posizione `(x,y)` viene associato al colore del target FLUX nella stessa
posizione. Per ogni immagine vengono poi generati quattro target image-to-image,
uno per prompt di color grading.

Prima dell'analisi LUT, i target vengono controllati rispetto all'originale. Lo
scopo è distinguere i target ancora interpretabili come color adjustment da
quelli in cui FLUX ha introdotto cambiamenti generativi troppo forti. Questo
controllo non è un filtro automatico della pipeline: tutti i target finali
presenti in `images_flux/target/` vengono comunque elaborati dalla fase LUT. Le
etichette di qualità servono invece a interpretare i risultati e a separare i
casi adatti allo studio dai casi in cui l'errore della LUT riflette modifiche
content-aware del modello.

La fase LUT campiona quindi coppie `RGB_originale -> RGB_target`, stima diverse
LUT, applica ogni LUT all'immagine originale e confronta la ricostruzione con il
target diffusion tramite metriche e confronto visivo.

I comandi principali sono esposti tramite `just`:

```bash
just prepare-images
just generate-targets
just evaluate-targets
just flux-target-grid
just lut-all
just report-assets
just catalog
just check
```

Nel workspace usato per il paper sono presenti 8 immagini preparate, 32 target
FLUX finali, 32 casi immagine/prompt per la LUT e 576 righe metriche, ottenute
da 18 varianti LUT per ciascun caso.

Oltre alla relazione principale è stato generato anche un catalogo visuale in
`paper/catalogo_immagini.pdf`, con il relativo sorgente Markdown in
`paper/catalogo_immagini.md`. Il catalogo raccoglie originali, target FLUX e
migliori ricostruzioni LUT in formato più esteso, così da permettere una
verifica visiva più approfondita dei test senza appesantire il paper.

![Panoramica dei target FLUX finali. Ogni riga corrisponde a una immagine, ogni colonna a un prompt di color grading.](images_flux/target_grid.jpg){ width=82% }

# Dataset e livelli di difficoltà

Le immagini principali provengono dal MIT-Adobe FiveK Dataset, scelto perché
è un dataset usato in letteratura per image processing e photo enhancement e
contiene fotografie realistiche adatte a esperimenti di color adjustment. Sono
state aggiunte due immagini da Unsplash per testare casi con forti gradienti
cromatici continui, in particolare tramonti.

La classificazione L1-L4 è euristica. Il codice misura proprietà come
complessità cromatica, entropia colore normalizzata, concentrazione dei colori
dominanti, edge density, texture score, crop loss rispetto al formato `3:2`,
risoluzione e un indice euristico di complessità. Queste misure servono per
ordinare e scremare le candidate, ma non riconoscono davvero la semantica della
scena. La scelta finale delle 8 immagini resta quindi sperimentale e visiva.

Le soglie L1-L4 vanno lette come regole di ordinamento, non come classi
semantiche forti. La tabella seguente riporta i range usati nello script di
classificazione (`utils/data/quality.py`). Per compattezza, nella tabella uso
queste sigle:

- `C`: `color_complexity_score`, cioè numero di celle RGB occupate nella
  quantizzazione `16^3`;
- `H`: `color_entropy_norm`, cioè entropia normalizzata della distribuzione dei
  colori quantizzati;
- `D`: `dominant_color_concentration_%`, cioè percentuale coperta dai colori
  dominanti;
- `E`: `edge_density`, cioè frazione di pixel con gradiente sopra soglia;
- `T`: `texture_score`, cioè misura euristica della variazione locale dei
  gradienti.

| Liv. | Caso | Range euristici usati |
|---|---:|---|
| L1 | unico | `C < 250`, `H < 0.45`, `D > 55`, `E < 0.08` |
| L2 | 1 | `C >= 430`, `H >= 0.44`, `D <= 55`, `E < 0.09`, `T < 0.065` |
| L2 | 2 | `C >= 400`, `H >= 0.38`, `D <= 55`, `E < 0.03`, `T < 0.035` |
| L3 | unico | `220 <= C <= 650`, `0.38 <= H <= 0.70`, `E >= 0.05` |
| L4 | 1 | `C >= 600`, `E >= 0.10`, `T >= 0.06` |
| L4 | 2 | `C >= 500`, `E >= 0.18` |
| L4 | 3 | `C >= 550`, `E >= 0.09`, `T >= 0.06` |
| incerto | fallback | immagini che non soddisfano nessuno dei casi precedenti |

Nel codice L4 viene controllato prima di L3, perché una scena urbana o molto
densa può avere entropia cromatica non estrema ma restare difficile per una
LUT. L2 non richiede entropia massima: fotografie naturali con ombre, cielo o
sfondi ampi possono essere casi cromaticamente interessanti anche con entropia
intermedia. L3 indica complessità intermedia/alta e possibili oggetti delicati,
ma presenza di persone, pelle o materiali sensibili viene confermata
visivamente.

Per rendere verificabile la classificazione, questa tabella mostra i valori
principali delle immagini finali:

| Immagine | Livello | C | H | D | E | T |
|---|---|---:|---:|---:|---:|---:|
| `L1_foglia` | L1 | 213 | 0.345 | 59.80 | 0.0153 | 0.0258 |
| `L2_fiori` | L2 | 749 | 0.546 | 25.68 | 0.0505 | 0.0461 |
| `L2_roccia` | L2 | 556 | 0.443 | 48.38 | 0.0863 | 0.0495 |
| `L2_tramonto_lago` | L2 | 432 | 0.392 | 50.92 | 0.0106 | 0.0241 |
| `L2_tramonto_mare` | L2 | 603 | 0.464 | 35.41 | 0.0298 | 0.0338 |
| `L3_ragazzi` | L3 | 399 | 0.452 | 50.67 | 0.0728 | 0.0523 |
| `L4_citta` | L4 | 587 | 0.410 | 55.84 | 0.0909 | 0.0604 |
| `L4_bracciali` | L4 | 1246 | 0.452 | 45.95 | 0.2243 | 0.0925 |

Alcuni casi mostrano bene perché la scelta non è puramente automatica:
`L2_fiori`, ad esempio, ha alta complessità cromatica ma struttura non estrema;
`L3_ragazzi` è importante soprattutto per il contenuto percettivamente delicato;
`L4_citta` e `L4_bracciali` sono stress test per densità di bordi, materiali e
regioni con significato diverso.

| Livello | Idea sperimentale | Immagini usate |
|---|---|---|
| L1 | pochi colori dominanti, regioni semplici | `L1_foglia` |
| L2 | molti colori o texture, ma semantica moderata | `L2_fiori`, `L2_roccia`, `L2_tramonto_lago`, `L2_tramonto_mare` |
| L3 | persone, pelle o materiali percettivamente delicati | `L3_ragazzi` |
| L4 | scena complessa con oggetti e materiali diversi | `L4_citta`, `L4_bracciali` |

Le immagini sono state convertite, ritagliate e ridimensionate a `1008x672`.
Questo allineamento è necessario per campionare coppie colore pixel-per-pixel e
per calcolare metriche tra target diffusion e output LUT.

# Modello generativo e prompt

I target sono stati generati con FLUX.2 Klein tramite l'implementazione locale
`flux_model/iris.c`, scritta da Salvatore Sanfilippo / antirez e inclusa nel
repository come codice esterno vendorizzato. La scelta permette di eseguire la
generazione localmente, senza dipendere da API esterne, e rende espliciti seed,
risoluzione, steps e prompt.

| Parametro | Valore |
|---|---|
| Implementazione | `flux_model/iris.c` |
| Modello | `flux-klein-4b-base` |
| Path modello locale | `flux_model/iris.c/flux-klein-4b-base` |
| Seed | `0` |
| Risoluzione | `1008x672` |
| Steps | `10` |
| Scheduler | `--linear` |
| Input image-to-image | immagine di riferimento passata con `-i/--input` |
| Output | `images_flux/target/` |

Questi valori sono quelli salvati nei metadata dei target finali: la
configurazione corrente usa l'eseguibile `flux_model/iris.c/iris`, il modello
locale `flux_model/iris.c/flux-klein-4b-base`, il seed `-S 0`, `-s 10`,
`--linear` e output in `images_flux/target/`. Il codice supporta anche
`flux-klein-4b`, ma i risultati finali del paper usano `flux-klein-4b-base`.
Nelle prime prove, documentate nelle note di progetto, `flux-klein-4b`
risultava meno conservativo: in alcuni casi modificava troppo il contenuto,
fino ad alterare o rimuovere persone e dettagli importanti. Per questo è stata
scelta la configurazione più conservativa, più coerente con un esperimento in
cui il target deve restare vicino all'originale e variare soprattutto nel
colore.

La CLI usata non espone un parametro numerico di image-to-image
strength/denoise. Nell'implementazione `iris.c`, l'immagine passata con `-i`
viene usata come riferimento tramite in-context conditioning: il modello genera
il target usando prompt e token visuali dell'immagine di riferimento.

Sono stati usati quattro prompt, formulati per preservare struttura e oggetti e
per applicare soprattutto un grading cromatico:

| Prompt | Obiettivo |
|---|---|
| `p01_warm_cinematic` | grading caldo cinematografico, luci dorate e ombre calde |
| `p02_teal_orange` | look teal and orange, ombre fredde e luci calde |
| `p03_cold_winter_grade` | look freddo/invernale, ombre blu e colori desaturati |
| `p04_faded_matte` | look film matte, saturazione ridotta e contrasto morbido |

Il testo completo dei prompt è in `configs/prompts.yaml`. Tutti i prompt
contengono vincoli espliciti come preservare struttura, forme e oggetti, e non
introdurre nuove texture.

# Generazione e controllo dei target

Per ogni immagine e per ogni prompt è stato generato un target image-to-image.
Il target ideale per questo studio è un'immagine in cui la struttura resta
allineata all'originale e la variazione riguarda soprattutto il colore.

La pipeline distingue preview e target finali. Le preview sono generazioni
rapide a `384x256`, salvate in `images_flux/preview/`, usate per controllare
visivamente prompt, stabilità del contenuto e comportamento del modello prima
di validare l'esperimento completo. I risultati quantitativi del paper non sono
calcolati sulle preview, ma sui target finali a `1008x672`, salvati in
`images_flux/target/`.

In pratica il modello non è vincolato a una trasformazione puramente cromatica.
Anche con prompt conservativi può modificare texture, materiali, ombre,
dettagli e regioni locali. Per questo i target sono stati controllati con una
prima valutazione `originale vs target`, salvata in
`images_flux/i2i_quality_targets.csv`. Queste metriche servono a capire quanto
il target sia ancora interpretabile come color adjustment, ma la metrica
principale del progetto resta `target diffusion vs ricostruzione LUT`.

Questa distinzione è essenziale: la ricostruzione LUT non viene valutata
rispetto all'immagine originale, ma rispetto al target FLUX. L'errore misura
quindi quanto la trasformazione generativa sia approssimabile da una mappatura
cromatica globale stimata per quella specifica coppia originale-target.

![Controllo di qualità dei target image-to-image rispetto agli originali. La griglia aiuta a individuare casi in cui FLUX ha modificato troppo la struttura.](images_flux/i2i_quality_targets_grid.jpg){ width=82% }

# Metodo LUT

La 3D LUT viene stimata da coppie di pixel corrispondenti:

$$
RGB_{originale}(x,y) \rightarrow RGB_{target}(x,y)
$$

Per ogni caso sono stati campionati fino a `200000` pixel. Nei metodi `mean` e
`median`, ogni campione viene associato al nodo della griglia più vicino al suo
RGB di input; nel metodo `weighted_mean`, invece, il contributo viene
distribuito sui nodi vicini con pesi coerenti con l'interpolazione trilineare.
Sono state testate tre dimensioni:

```text
17^3, 33^3, 65^3
```

e tre strategie di fitting:

| Metodo | Descrizione |
|---|---|
| `mean` | media dei colori target associati a un nodo |
| `median` | mediana, più robusta agli outlier |
| `weighted_mean` | media pesata, più stabile quando i campioni sono distribuiti tra nodi vicini |

L'applicazione della LUT è stata provata con `nearest` e `trilinear`.
L'interpolazione trilineare è importante per evitare discontinuità visibili
tra colori vicini, soprattutto nei gradienti.

Ogni caso produce quindi:

```text
3 dimensioni LUT x 3 fit method x 2 apply method = 18 varianti
```

Il limite strutturale è chiaro: se due pixel hanno RGB simile nell'originale
ma il diffusion model li trasforma diversamente perché appartengono a oggetti
diversi, una LUT globale deve mediare tra le due richieste.

# Metriche

Le metriche sono usate in tre punti diversi della pipeline, con significati
diversi. Non tutte misurano "qualità" nello stesso senso: alcune servono a
scegliere immagini sperimentalmente utili, altre a controllare se un target
generativo è adatto allo studio, e solo l'ultimo gruppo misura direttamente la
ricostruzione LUT.

| Punto della pipeline | Confronto | Scopo |
|---|---|---|
| Selezione immagini | immagine candidata analizzata da sola | stimare varietà cromatica e complessità visiva per costruire i livelli L1-L4 |
| Controllo target FLUX | originale vs target FLUX | verificare se il target resta vicino alla scena originale e cambia soprattutto il colore |
| Valutazione LUT | target FLUX vs ricostruzione LUT | misurare quanto il target generativo sia approssimabile da una 3D LUT globale |

Nel progetto, salvo diversa indicazione, `RGB` indica valori sRGB codificati e
normalizzati in `[0,1]`. La LUT è fittata e applicata in questo spazio; la
conversione in CIELAB viene usata solo per calcolare il Delta E CIEDE2000.

## Metriche per la selezione delle immagini

La classificazione L1-L4 usa metriche euristiche calcolate sulle immagini
candidate prima della generazione FLUX:

- `color_complexity_score`
  - Calcolo: conta quante celle RGB sono occupate dopo una quantizzazione
    `16^3`.
  - Lettura: minimo 1, massimo teorico 4096; valori più alti indicano più
    varietà cromatica.
  - Perché è stata scelta: distingue immagini con pochi colori dominanti da
    scene cromaticamente ricche.

- `color_entropy_norm`
  - Calcolo: misura l'entropia normalizzata della distribuzione dei colori
    quantizzati.
  - Lettura: range `0-1`; valori più alti indicano colori più distribuiti e
    meno concentrati.
  - Perché è stata scelta: evita di confondere molte celle sparse con una vera
    distribuzione cromatica ampia.

- `dominant_color_concentration_%`
  - Calcolo: misura la percentuale di pixel coperta dai colori dominanti.
  - Lettura: range `0-100`; valori più alti indicano che pochi colori dominano
    l'immagine.
  - Perché è stata scelta: identifica i casi L1, dove una LUT globale dovrebbe
    essere favorita.

- `edge_density`
  - Calcolo: misura la frazione di pixel con gradiente sopra soglia.
  - Lettura: range `0-1`; valori più alti indicano più bordi e dettagli.
  - Perché è stata scelta: stima la complessità strutturale che può rendere
    fragile il confronto pixel-per-pixel.

- `texture_score`
  - Calcolo: usa la deviazione standard della magnitudine dei gradienti come
    indicatore di dettaglio locale.
  - Lettura: non ha un limite superiore pratico fisso; valori più alti indicano
    più dettaglio locale.
  - Perché è stata scelta: aiuta a individuare texture naturali, materiali e
    scene più difficili.

Queste metriche non sono usate come benchmark scientifico autonomo. Servono a
rendere meno arbitraria la scelta delle immagini e a coprire livelli crescenti
di difficoltà; la selezione finale resta manuale perché contenuto, pelle,
materiali e semantica non sono catturati in modo affidabile da queste misure.

## Metriche per il controllo dei target FLUX

Dopo la generazione image-to-image, ogni target viene confrontato con
l'originale. In questo punto della pipeline un valore "migliore" non significa
sempre "più vicino possibile": un target identico all'originale sarebbe stabile
ma inutile, mentre un target troppo diverso potrebbe contenere cambiamenti
strutturali non rappresentabili da una LUT.

- `edge_correlation`
  - Calcolo: correlazione di Pearson tra le mappe di gradiente della luminanza
    di originale e target.
  - Lettura: range `-1` a `1`; valori più vicini a `1` indicano bordi più
    allineati.
  - Perché è stata scelta: controlla se FLUX ha conservato la struttura
    principale della scena.

- `ssim`
  - Calcolo: SSIM standard di `skimage.metrics.structural_similarity`, usata su
    immagini RGB multicanale.
  - Lettura: il valore ideale è `1`; valori più alti indicano struttura e
    contrasto più simili localmente.
  - Perché è stata scelta: segnala cambiamenti forti di struttura, contrasto o
    contenuto.

- `rgb_mae`
  - Calcolo: errore assoluto medio tra originale e target sui canali RGB,
    riportato in scala `0-255`.
  - Lettura: il minimo è `0`; valori più bassi indicano colori più vicini
    all'originale.
  - Perché è stata scelta: dà una misura semplice dell'entità media del
    cambiamento RGB.

- `rgb_psnr`
  - Calcolo: rapporto segnale/rumore derivato dall'MSE RGB tra originale e
    target.
  - Lettura: è espresso in dB; valori più alti indicano immagini più simili,
    infinito se identiche.
  - Perché è stata scelta: aiuta a individuare target troppo lontani o troppo
    simili all'originale.

- `delta_e_mean`, `delta_e_median`, `delta_e_p95`
  - Calcolo: differenza cromatica CIEDE2000 tra originale e target dopo
    conversione in CIELAB.
  - Lettura: valori non negativi; valori più alti indicano cambiamento
    cromatico più forte.
  - Perché sono state scelte: misurano se il prompt ha prodotto un cambiamento
    colore reale e se esistono code locali forti.

Queste metriche producono un'etichetta di supporto (`candidate`,
`weak_color_change`, `possible_semantic_change`, `check_content_change`). Le
etichette non sono un filtro automatico: aiutano a leggere i risultati LUT,
perché un errore alto su un target già sospetto può dipendere da cambiamenti
generativi oltre il solo colore.

La classificazione è euristica e viene applicata in ordine nello script
`utils/flux/target_eval.py`:

- `check_content_change`
  - Condizione: `edge_correlation < 0.70` oppure `ssim < 0.45`.
  - Significato: il target è strutturalmente troppo lontano dall'originale. La
    differenza non sembra solo cromatica, quindi il caso va controllato
    visivamente prima di interpretare l'errore LUT.

- `weak_color_change`
  - Condizione: se il target non è già `check_content_change` e
    `delta_e_mean < 4.0`.
  - Significato: il contenuto è abbastanza stabile, ma il cambiamento cromatico
    medio è debole. Il target può essere poco informativo perché FLUX ha
    modificato troppo poco l'immagine.

- `possible_semantic_change`
  - Condizione: se il target non è già nei casi precedenti,
    `delta_e_p95 > 55.0` e `edge_correlation < 0.82`.
  - Significato: la media può essere accettabile, ma esistono errori cromatici
    locali molto forti insieme a un allineamento dei bordi non ottimale. È un
    indizio di possibile modifica locale o semantica.

- `candidate`
  - Condizione: nessuna delle condizioni precedenti è attiva.
  - Significato: il target è considerato adatto allo studio LUT, perché conserva
    abbastanza la struttura e presenta un cambiamento cromatico non troppo
    debole né evidentemente localizzato.

## Metriche per la valutazione LUT

La valutazione principale del progetto confronta la ricostruzione LUT con il
target FLUX:

$$
errore = I_{target}^{FLUX} - LUT(I_{originale})
$$

Questa è una valutazione descrittiva caso-per-caso: ogni LUT viene stimata su
una specifica coppia originale-target e poi confrontata con lo stesso target.
Il risultato risponde alla domanda "quanto questo target è descrivibile da una
LUT globale?", non alla domanda "quanto questa LUT generalizza a nuove immagini
o nuovi prompt".

- `rgb_psnr`
  - Calcolo: PSNR tra target FLUX e ricostruzione LUT nello spazio sRGB
    normalizzato.
  - Lettura: è espresso in dB; valori più alti indicano ricostruzione più vicina
    pixel-per-pixel, infinito se identica.
  - Perché è stata scelta: misura l'errore globale RGB ed è una metrica
    richiesta/attesa per questo tipo di confronto.

- `ssim`
  - Calcolo: SSIM standard di `skimage.metrics.structural_similarity`, usata su
    immagini RGB multicanale.
  - Lettura: il valore ideale è `1`; valori più alti indicano migliore
    somiglianza strutturale locale.
  - Perché è stata scelta: controlla se la LUT mantiene struttura, contrasto e
    coerenza locale del target.

- `delta_e_mean`
  - Calcolo: media della differenza cromatica CIEDE2000 in CIELAB.
  - Lettura: il minimo è `0`; valori più bassi indicano errore cromatico medio
    minore.
  - Perché è stata scelta: è la metrica principale per scegliere la migliore
    variante LUT, perché il problema studiato è cromatico.

- `delta_e_median`
  - Calcolo: mediana della differenza cromatica CIEDE2000 in CIELAB.
  - Lettura: il minimo è `0`; valori più bassi indicano errore tipico minore.
  - Perché è stata scelta: descrive l'errore tipico ed è più robusta della
    media rispetto a pochi errori molto forti.

- `delta_e_p95`
  - Calcolo: 95-esimo percentile della differenza cromatica CIEDE2000.
  - Lettura: il minimo è `0`; valori più bassi indicano meno errori locali
    estremi.
  - Perché è stata scelta: evidenzia fallimenti localizzati che la media può
    nascondere.

- `occupied_ratio`
  - Calcolo: frazione di nodi/celle LUT che ricevono campioni o contributi
    durante il fitting.
  - Lettura: range `0-1`; valori più alti indicano una griglia più coperta, ma
    non una qualità visiva necessariamente migliore.
  - Perché è stata scelta: aiuta a interpretare sparsità e affidabilità del
    fitting, soprattutto per griglie grandi.

Il Delta E usato è CIEDE2000, calcolato in CIELAB tramite `skimage.color`: è
una formula percettivamente più accurata della distanza euclidea semplice in
Lab ed è quindi più difendibile come metrica cromatica finale. Per `mean` e
`median`, `occupied_ratio` indica i nodi associati a
campioni tramite nearest node; per `weighted_mean`, un campione può distribuire
contributo sugli otto nodi vicini, quindi il valore indica nodi che hanno
ricevuto peso.

Le metriche non sostituiscono l'analisi visiva. PSNR e SSIM possono essere
buoni anche se esistono errori localizzati percepibili, per esempio su pelle,
insegne o riflessi. Per questo ogni esperimento salva anche originale, target,
ricostruzione, heatmap, `summary.png` e `best_summary.png`.

# Risultati

La lettura dei risultati segue quattro passaggi: difficoltà delle immagini,
qualità dei target FLUX, confronto quantitativo tra varianti LUT e casi
qualitativi. Questa organizzazione evita di trattare le metriche LUT come un
numero isolato: prima si valuta se il target generato è adatto allo studio,
poi si misura quanto una LUT riesce ad approssimarlo.

## Difficoltà delle immagini e qualità dei target

La tabella dei livelli L1-L4 mostra che il dataset non è scelto solo per
estetica, ma per coprire difficoltà sperimentali diverse: regioni quasi
uniformi, texture naturali, pelle, materiali, riflessi, scene urbane e
gradienti continui. Le metriche di classificazione cromatica e visiva aiutano a
ordinare le candidate, mentre la scelta finale resta manuale perché la
semantica non è catturata in modo affidabile dalle sole misure automatiche.

La griglia dei target FLUX permette invece di verificare se ogni target è
ancora leggibile come color adjustment. Nel CSV
`images_flux/i2i_quality_targets.csv`, 16 target risultano `candidate`, 11
`possible_semantic_change` e 5 `check_content_change`. Queste etichette non
escludono automaticamente un caso, ma avvisano che in alcune immagini il
diffusion model ha introdotto differenze strutturali o semantiche che una LUT
non può recuperare.

## Effetto della dimensione LUT

La tabella riporta le metriche medie sui 32 casi e su tutte le varianti con la
stessa dimensione LUT.

| LUT size | PSNR medio | SSIM | Delta E medio | Delta E p95 | Occupied ratio |
|---:|---:|---:|---:|---:|---:|
| 17 | 23.388 | 0.7382 | 5.744 | 16.306 | 0.1495 |
| 33 | 23.910 | 0.7552 | 5.171 | 15.180 | 0.0926 |
| 65 | 23.716 | 0.7443 | 4.995 | 15.209 | 0.0541 |

Il passaggio da `17^3` a `33^3` migliora PSNR, SSIM e Delta E. Il passaggio a
`65^3` riduce ancora il Delta E medio, ma non migliora PSNR e SSIM medi. Inoltre
l'occupied ratio diminuisce: la griglia è più fine, ma molte celle restano non
osservate. Per questo `33^3` è un buon compromesso interpretativo, mentre
`65^3` può dare il miglior risultato numerico sui casi più coperti dai
campioni.

## Effetto di fitting e interpolazione

La variante migliore in media secondo Delta E medio è risultata:

```text
lut_65_weighted_mean_trilinear
```

| Variante | PSNR | SSIM | Delta E medio | Delta E p95 | Occupied ratio |
|---|---:|---:|---:|---:|---:|
| migliore | 24.387 | 0.7744 | 4.836 | 14.316 | 0.0776 |

L'interpolazione trilineare è generalmente preferibile al nearest neighbor
perché produce transizioni più continue. La media pesata funziona bene perché
stabilizza il contributo dei campioni nella griglia. La mediana resta utile nei
casi con outlier o modifiche locali incoerenti, come `L1_foglia / p01` e
`L4_citta / p03`.

## Migliori casi per immagine

La tabella seguente mostra, per ogni immagine, il prompt migliore secondo Delta
E CIEDE2000 medio tra le varianti disponibili. Nei casi elencati la variante migliore è
`65^3 weighted_mean trilinear`.

| Immagine | Prompt | PSNR | SSIM | Delta E |
|---|---|---:|---:|---:|
| `L1_foglia` | `p03` | 27.019 | 0.8323 | 2.952 |
| `L2_fiori` | `p03` | 28.356 | 0.8832 | 3.090 |
| `L2_roccia` | `p03` | 22.162 | 0.7431 | 5.480 |
| `L2_tramonto_lago` | `p03` | 25.677 | 0.8824 | 2.542 |
| `L2_tramonto_mare` | `p03` | 26.421 | 0.8164 | 2.547 |
| `L3_ragazzi` | `p02` | 26.486 | 0.8240 | 3.901 |
| `L4_bracciali` | `p03` | 22.874 | 0.7631 | 4.926 |
| `L4_citta` | `p02` | 25.738 | 0.8130 | 4.122 |

La lettura qualitativa dei casi è diversa: `L1_foglia` è il caso semplice,
`L2_fiori` e i tramonti mostrano trasformazioni cromatiche coerenti,
`L2_roccia` introduce texture naturale, `L3_ragazzi` rende visibili errori su
pelle e volti, mentre `L4_bracciali` e `L4_citta` stressano dettagli, riflessi,
insegne e materiali diversi.

## Casi in cui la LUT funziona bene

`L1_foglia`, `L2_fiori` e i due tramonti mostrano il comportamento atteso
quando FLUX produce soprattutto un grading globale. La LUT ricostruisce bene il
look complessivo e gli errori restano distribuiti in modo moderato.

![Caso semplice: `L1_foglia / p03_cold_winter_grade`. La migliore LUT riproduce bene il target freddo perché la scena contiene pochi cluster cromatici dominanti.](images_lut/L1_foglia/p03_cold_winter_grade/best_summary.png){ width=110% }

![Caso ricco ma ancora favorevole: `L2_fiori / p01_warm_cinematic`. La trasformazione è cromaticamente varia, ma resta abbastanza coerente nello spazio RGB.](images_lut/L2_fiori/p01_warm_cinematic/best_summary.png){ width=110% }

## Confronto visivo tra metodi LUT

Il confronto quantitativo tra varianti non è solo formale. Le figure
`summary.png` mostrano la stessa regione ricostruita con sei combinazioni
`17^3`: righe per metodo di fitting (`mean`, `median`, `weighted_mean`) e
colonne per applicazione (`nearest`, `trilinear`). Sono utili perché isolano
zone in cui le varianti divergono molto, anche quando le metriche medie sono
vicine.

Nel caso `L1_foglia / p02_teal_orange`, il vantaggio dell'interpolazione
trilineare è visibile sul gambo e sulle venature: `nearest` introduce bordi
scalettati e piccoli salti cromatici, mentre `trilinear` mantiene una
transizione più continua. Tra le varianti `17^3` mostrate, la migliore è
`weighted_mean_trilinear` con Delta E medio `4.093`; `weighted_mean_nearest`
sale a `4.256` e mostra una definizione meno pulita del gambo. Il dato numerico
non è enorme, ma la differenza visiva è chiara.

![Confronto tra metodi LUT su `L1_foglia / p02_teal_orange`. L'interpolazione `trilinear` conserva meglio la continuità del gambo e riduce le discontinuità visibili rispetto a `nearest`.](images_lut/L1_foglia/p02_teal_orange/summary.png){ width=92% }

`L2_fiori / p02_teal_orange` mostra invece un caso in cui la lettura visiva può
divergere dalla metrica del crop. Nel confronto `17^3`, la variante evidenziata
dalla figura è `median_nearest`, con Delta E medio `4.709`, ma la resa visiva
presenta posterizzazione e bordi cromatici più evidenti. Le versioni
trilineari appaiono più continue sui petali e sulle foglie, anche quando non
sono le migliori nel singolo valore medio mostrato dal crop. Questo conferma
che le metriche aiutano a ordinare, ma non sostituiscono l'ispezione visiva.

![Confronto tra metodi LUT su `L2_fiori / p02_teal_orange`. Alcune varianti favorite dalla metrica locale producono una resa più posterizzata; le versioni `trilinear` sono visivamente più continue.](images_lut/L2_fiori/p02_teal_orange/summary.png){ width=92% }

Nel caso `L2_roccia / p03_cold_winter_grade`, la differenza principale è tra
ricostruzioni rumorose e ricostruzioni più lisce. Sul crop `17^3`,
`median_trilinear` ottiene il Delta E medio più basso (`6.159`), ma la lettura
complessiva del caso conferma il vantaggio delle varianti pesate e trilineari
quando la griglia è più fine: nella valutazione completa la migliore variante
è `65^3 weighted_mean trilinear`, con Delta E medio `5.480`. La roccia resta
difficile perché il target contiene molte variazioni locali della texture.

![Confronto tra metodi LUT su `L2_roccia / p03_cold_winter_grade`. Le varianti `nearest` amplificano rumore e discontinuità sulla texture; l'interpolazione trilineare produce una superficie più leggibile.](images_lut/L2_roccia/p03_cold_winter_grade/summary.png){ width=92% }

Un caso come `L4_bracciali / p01_warm_cinematic` è interessante per il motivo
opposto: pur essendo ricco di colori, riflessi e materiali, molte regioni hanno
separazioni cromatiche nette. Le varianti LUT restano quindi abbastanza simili
tra loro. La difficoltà non è il numero di colori in assoluto, ma la presenza
di colori simili che il modello potrebbe trasformare diversamente in base al
materiale o alla posizione.

## Test sui gradienti cromatici continui

I tramonti sono un test specifico sui gradienti. L'ipotesi iniziale era che
sfumature continue di cielo e acqua potessero mettere in crisi una griglia LUT
discreta. Una LUT campiona lo spazio RGB su una griglia finita: se la griglia è
troppo grossolana o l'interpolazione è inadeguata, gradienti regolari possono
mostrare banding, discontinuità o errori visibili nelle sfumature.

I risultati sono migliori del previsto: con interpolazione trilineare e griglie
`65^3`, le transizioni restano abbastanza morbide. Il caso
`L2_tramonto_lago` isola soprattutto cielo, acqua e foschia, quindi è utile per
osservare sfumature ampie e regolari. `L2_tramonto_mare` è stato aggiunto come
caso più sfidante: oltre al tramonto contiene nuvole, onde, riflessi e dettagli
fini, quindi combina gradienti continui e variazioni locali più dense.

Questo suggerisce che, per questi target, la trasformazione di FLUX sui
gradienti è ancora abbastanza liscia nello spazio RGB. Il caso non dimostra che
ogni gradiente sia facile per una LUT, ma mostra che una griglia fine e una
buona interpolazione possono rappresentare bene trasformazioni cromatiche
continue quando non intervengono modifiche semantiche forti.

![Test sui gradienti: `L2_tramonto_lago / p03_cold_winter_grade`. L'errore resta contenuto nonostante cielo e acqua contengano transizioni continue.](images_lut/L2_tramonto_lago/p03_cold_winter_grade/best_summary.png){ width=110% }

![Test sui gradienti con dettagli più fitti: `L2_tramonto_mare / p03_cold_winter_grade`. La scena contiene tramonto, nuvole, onde e riflessi: la LUT mantiene bene il grading freddo, ma il caso è più sfidante perché le sfumature continue convivono con molte variazioni locali.](images_lut/L2_tramonto_mare/p03_cold_winter_grade/best_summary.png){ width=110% }

## Casi intermedi

`L2_roccia` e `L3_ragazzi` mostrano che una buona metrica non elimina la
necessità di analisi visiva. La roccia contiene texture naturale e variazioni
locali; i ragazzi introducono pelle, volti e abiti. In questi casi piccoli
spostamenti cromatici possono essere più visibili, anche quando Delta E e PSNR
restano accettabili.

![Caso percettivamente delicato: `L3_ragazzi / p01_warm_cinematic`. La LUT approssima il grading globale, ma pelle e volti rendono visibili differenze locali.](images_lut/L3_ragazzi/p01_warm_cinematic/best_summary.png){ width=110% }

## Casi limite

I casi limite sono scelti con due criteri: metriche peggiori e valore
interpretativo della figura. Il peggior caso per PSNR, Delta E medio e Delta E
p95 è `L4_citta / p03_cold_winter_grade`. Il valore SSIM più basso tra le
migliori varianti si trova invece in `L2_tramonto_lago / p04_faded_matte`, dove
la trasformazione matte altera fortemente contrasto e struttura locale pur
restando cromaticamente interpretabile. `L4_bracciali` e `L4_citta` sono
comunque i casi più utili per mostrare il limite strutturale della LUT globale:
materiali, dettagli, insegne, vetri, riflessi e ombre possono essere trattati
da FLUX in modo localmente diverso. Una LUT globale non può distinguere due
pixel con RGB simile ma contenuto diverso.

![Caso con materiali e dettagli minuti: `L4_bracciali / p02_teal_orange`. Gli errori si concentrano su riflessi, bordi e piccoli oggetti.](images_lut/L4_bracciali/p02_teal_orange/best_summary.png){ width=110% }

`L2_roccia / p01_warm_cinematic` è istruttivo per un motivo diverso: non è
una scena semanticamente complessa come la città, ma la texture naturale della
roccia produce errori locali marcati. La migliore variante ha Delta E p95
`23.282`, e mostra che anche una scena senza persone o oggetti urbani può
essere difficile quando il target introduce variazioni locali non uniformi.

![Caso limite su texture naturale: `L2_roccia / p01_warm_cinematic`. La metrica Delta E p95 evidenzia errori localizzati sulle variazioni fini della superficie.](images_lut/L2_roccia/p01_warm_cinematic/best_summary.png){ width=110% }

Il fallimento più istruttivo è `L4_citta / p03_cold_winter_grade`: anche la
migliore variante ha PSNR `18.279`, SSIM `0.6929`, Delta E medio `8.610` e
Delta E p95 `25.493`. La heatmap mostra errori su insegne, bordi, finestre,
persone e regioni urbane dense. Il problema non è solo la precisione della LUT:
il target diffusion contiene modifiche locali e semantiche.

![Caso limite: `L4_citta / p03_cold_winter_grade`. La LUT riproduce parte del look freddo, ma fallisce dove il target FLUX modifica dettagli locali e strutture urbane.](images_lut/L4_citta/p03_cold_winter_grade/best_summary.png){ width=110% }

# Discussione

I risultati confermano la distinzione centrale del progetto. Quando il diffusion
model produce soprattutto un color grading globale, una 3D LUT è sufficiente a
spiegare gran parte della trasformazione. Questo accade nei casi con pochi
cluster cromatici, con mapping coerente nello spazio RGB o con gradienti
continui trattati in modo regolare.

Quando invece il target contiene modifiche content-aware, la LUT fallisce in
modo prevedibile. Il vincolo è matematico: due pixel con lo stesso RGB di
partenza devono ricevere lo stesso RGB trasformato. Un diffusion model può
invece usare posizione, contesto e semantica, quindi può trasformare in modo
diverso colori simili appartenenti a cielo, pelle, muro, insegna, vestito o
riflesso.

Le metriche sono coerenti con questa interpretazione, ma non bastano da sole.
PSNR e SSIM favoriscono fedeltà pixel-per-pixel e somiglianza strutturale;
Delta E CIEDE2000 misura meglio l'errore cromatico; le heatmap mostrano dove
l'errore si concentra.
Il valore dell'esperimento sta proprio nell'usare insieme queste informazioni:
le metriche ordinano i casi, le figure spiegano perché la LUT funziona o
fallisce.

# Limiti

Il lavoro ha alcuni limiti importanti:

- la LUT è globale e non usa informazione spaziale;
- il fitting assume corrispondenza pixel-per-pixel tra originale e target;
- se FLUX cambia la struttura della scena, il confronto diventa meno
  interpretabile;
- la SSIM standard resta una metrica strutturale, non un giudizio percettivo
  completo;
- il dataset è piccolo e pensato come studio sperimentale, non come benchmark
  esaustivo;
- i risultati dipendono dal modello locale, dai prompt e dal seed;

Possibili estensioni includono LUT locali o mascherate semanticamente, fitting
regolarizzato, confronto con regressori colore continui, valutazione su più
seed e un set più ampio di immagini.

# Conclusione

Una 3D LUT stimata per una specifica coppia originale-target può approssimare
una parte significativa della trasformazione prodotta da un diffusion model
image-to-image, ma solo quando questa trasformazione è prevalentemente un
color grading globale. Nei casi semplici o cromaticamente coerenti, la
ricostruzione LUT è vicina al target FLUX e le metriche confermano una buona
fedeltà.

La LUT non può invece rappresentare trasformazioni spaziali, strutturali o
semantiche. Quando FLUX modifica texture, materiali, pelle, oggetti o dettagli
urbani, l'errore della LUT aumenta e si concentra in regioni interpretabili
visivamente.

La risposta alla domanda iniziale è quindi parziale ma chiara: una LUT globale
nel senso `RGB -> RGB`, stimata caso per caso, spiega bene la componente
cromatica globale del target diffusion, ma non la componente generativa o
content-aware. Proprio per questo il confronto è utile: separa ciò che è
color adjustment da ciò che richiede informazione sul contenuto dell'immagine.

# Riproducibilità e crediti

I dati principali usati dal paper sono:

| File | Contenuto |
|---|---|
| `configs/images.yaml` | immagini candidate e sottoinsieme selezionato |
| `configs/prompts.yaml` | prompt di color grading |
| `images_flux/i2i_quality_targets.csv` | qualità target FLUX rispetto agli originali |
| `images_lut/summary_all.csv` | metriche complete LUT |
| `images_lut/metrics_by_lut_size.csv` | aggregazione per dimensione LUT |
| `images_lut/metrics_by_variant.csv` | aggregazione per variante LUT |
| `images_lut/best_by_delta_e.csv` | migliore variante per ogni caso secondo Delta E |
| `paper/catalogo_immagini.md` / `paper/catalogo_immagini.pdf` | catalogo visuale completo dei test |

Codice e asset esterni citati:

- `flux_model/iris.c`: implementazione locale di FLUX.2 in C di Salvatore
  Sanfilippo / antirez, usata come dipendenza esterna vendorizzata;
- FLUX.2 Klein / `flux-klein-4b-base`, modello usato per generare i target;
- MIT-Adobe FiveK Dataset, usato per `foglia`, `roccia`, `citta`, `fiori`,
  `bracciali` e `ragazzi`;
- Unsplash, usato per `tramonto_mare`
  (`https://unsplash.com/photos/JE01L3hB0GQ`) e `tramonto_lago`
  (`https://unsplash.com/photos/qkfxBc2NQ18`).
