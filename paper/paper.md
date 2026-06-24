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

Il confronto usa metriche sia per caratterizzare immagini e target, sia per
valutare le ricostruzioni: PSNR RGB, SSIM semplificata su luminanza, Delta E
CIE76 e copertura della griglia LUT. I risultati mostrano che una LUT stimata
caso per caso approssima bene i target in cui FLUX applica prevalentemente un
color grading globale. La qualità peggiora quando il modello modifica texture,
dettagli locali, materiali o regioni semanticamente distinte. In media la
variante migliore per Delta E è `65^3 weighted_mean trilinear`, mentre `33^3`
risulta un compromesso più robusto tra accuratezza e copertura della griglia.

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
fuori dal modello LUT, gli errori aiutano a localizzare dove FLUX usa contenuto,
posizione o semantica della scena.

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

Anche le soglie L1-L4 vanno lette come euristiche, non come classi semantiche
forti. La corrispondenza tra metriche e descrizione dei livelli è intenzionale
ma non perfetta: `color_complexity_score`, entropia, concentrazione dei colori
dominanti, edge density e texture score misurano proprietà utili, ma non
capiscono se una regione rappresenta pelle, vetro, un'insegna o un materiale
delicato. Nel codice L4 viene controllato prima di L3, perché una scena urbana
o molto densa può avere entropia cromatica non estrema ma restare difficile
per una LUT. L2 non richiede entropia massima: fotografie naturali con ombre,
cielo o sfondi ampi possono essere casi cromaticamente interessanti anche con
entropia intermedia. L3 indica complessità intermedia/alta e possibili oggetti
delicati, ma presenza di persone, pelle o materiali sensibili viene confermata
visivamente.

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

La valutazione principale confronta la ricostruzione LUT con il target FLUX:

$$
errore = I_{target}^{FLUX} - LUT(I_{originale})
$$

Sono state usate queste metriche:

| Metrica | Ruolo |
|---|---|
| `rgb_psnr` | errore pixel-per-pixel sul colore RGB |
| `luma_ssim` | similarità strutturale semplificata sulla luminanza |
| `delta_e_mean`, `delta_e_median`, `delta_e_p95` | errore cromatico percettivo medio, mediano e al 95 percentile |
| `occupied_ratio` | frazione di celle LUT osservate dai campioni |

PSNR e Delta E sono calcolati su immagini normalizzate in `[0,1]`; di
conseguenza il data range del PSNR è `1.0`. Il Delta E usato è CIE76: i
valori RGB sRGB vengono linearizzati, convertiti in XYZ con bianco D65 e poi in
Lab. La SSIM implementata è una misura globale semplificata sulla luminanza,
non una SSIM windowed completa; è utile per confrontare la coerenza strutturale
generale, ma non va letta come giudizio percettivo completo. L'`occupied_ratio`
non misura qualità visiva: indica quanta parte della griglia LUT è stata
effettivamente osservata dai campioni, quindi aiuta a interpretare sparsità e
robustezza del fitting.

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

| LUT size | PSNR medio | SSIM luma | Delta E medio | Delta E p95 | Occupied ratio |
|---:|---:|---:|---:|---:|---:|
| 17 | 23.388 | 0.9635 | 8.657 | 24.306 | 0.1495 |
| 33 | 23.910 | 0.9672 | 7.789 | 22.710 | 0.0926 |
| 65 | 23.716 | 0.9666 | 7.574 | 22.983 | 0.0541 |

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

| Variante | PSNR | SSIM luma | Delta E medio | Delta E p95 | Occupied ratio |
|---|---:|---:|---:|---:|---:|
| migliore | 24.387 | 0.9701 | 7.284 | 21.434 | 0.0776 |

L'interpolazione trilineare è generalmente preferibile al nearest neighbor
perché produce transizioni più continue. La media pesata funziona bene perché
stabilizza il contributo dei campioni nella griglia. La mediana resta utile nei
casi con outlier o modifiche locali incoerenti, come `L1_foglia / p01` e
`L4_citta / p03`.

## Migliori casi per immagine

La tabella seguente mostra, per ogni immagine, il prompt migliore secondo Delta
E medio tra le varianti disponibili. Nei casi elencati la variante migliore è
`65^3 weighted_mean trilinear`.

| Immagine | Prompt | PSNR | SSIM | Delta E |
|---|---|---:|---:|---:|
| `L1_foglia` | `p03` | 27.019 | 0.9719 | 5.297 |
| `L2_fiori` | `p01` | 27.973 | 0.9939 | 5.480 |
| `L2_roccia` | `p02` | 25.873 | 0.9875 | 7.870 |
| `L2_tramonto_lago` | `p03` | 25.677 | 0.9570 | 3.851 |
| `L2_tramonto_mare` | `p03` | 26.421 | 0.9760 | 4.862 |
| `L3_ragazzi` | `p01` | 26.840 | 0.9897 | 5.574 |
| `L4_bracciali` | `p02` | 23.360 | 0.9447 | 7.684 |
| `L4_citta` | `p02` | 25.738 | 0.9848 | 5.890 |

La lettura qualitativa dei casi è diversa: `L1_foglia` è il caso semplice,
`L2_fiori` e i tramonti mostrano trasformazioni cromatiche coerenti,
`L2_roccia` introduce texture naturale, `L3_ragazzi` rende visibili errori su
pelle e volti, mentre `L4_bracciali` e `L4_citta` stressano dettagli, riflessi,
insegne e materiali diversi.

## Casi in cui la LUT funziona bene

`L1_foglia`, `L2_fiori` e i due tramonti mostrano il comportamento atteso
quando FLUX produce soprattutto un grading globale. La LUT ricostruisce bene il
look complessivo e gli errori restano distribuiti in modo moderato.

![Caso semplice: `L1_foglia / p03_cold_winter_grade`. La migliore LUT riproduce bene il target freddo perché la scena contiene pochi cluster cromatici dominanti.](images_lut/L1_foglia/p03_cold_winter_grade/best_summary.png){ width=100% }

![Caso ricco ma ancora favorevole: `L2_fiori / p01_warm_cinematic`. La trasformazione è cromaticamente varia, ma resta abbastanza coerente nello spazio RGB.](images_lut/L2_fiori/p01_warm_cinematic/best_summary.png){ width=100% }

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
`weighted_mean_trilinear` con Delta E medio `6.015`; `weighted_mean_nearest`
sale a `6.264` e mostra una definizione meno pulita del gambo. Il dato numerico
non è enorme, ma la differenza visiva è chiara.

![Confronto tra metodi LUT su `L1_foglia / p02_teal_orange`. L'interpolazione `trilinear` conserva meglio la continuità del gambo e riduce le discontinuità visibili rispetto a `nearest`.](images_lut/L1_foglia/p02_teal_orange/summary.png){ width=92% }

`L2_fiori / p02_teal_orange` mostra invece un caso in cui la lettura visiva può
divergere dalla metrica del crop. Nel confronto `17^3`, la variante evidenziata
dalla figura è `median_nearest`, con Delta E medio `7.48`, ma la resa visiva
presenta posterizzazione e bordi cromatici più evidenti. Le versioni
trilineari appaiono più continue sui petali e sulle foglie, anche quando non
sono le migliori nel singolo valore medio mostrato dal crop. Questo conferma
che le metriche aiutano a ordinare, ma non sostituiscono l'ispezione visiva.

![Confronto tra metodi LUT su `L2_fiori / p02_teal_orange`. Alcune varianti favorite dalla metrica locale producono una resa più posterizzata; le versioni `trilinear` sono visivamente più continue.](images_lut/L2_fiori/p02_teal_orange/summary.png){ width=92% }

Nel caso `L2_roccia / p03_cold_winter_grade`, la differenza principale è tra
ricostruzioni rumorose e ricostruzioni più lisce. Sul crop `17^3`,
`median_trilinear` ottiene il Delta E medio più basso (`10.593`), ma la lettura
complessiva del caso conferma il vantaggio delle varianti pesate e trilineari
quando la griglia è più fine: nella valutazione completa la migliore variante
è `65^3 weighted_mean trilinear`, con Delta E medio `9.525`. La roccia resta
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
`65^3`, le transizioni restano abbastanza morbide. Questo suggerisce che, per
questi target, la trasformazione di FLUX sui gradienti è ancora abbastanza
liscia nello spazio RGB. Il caso non dimostra che ogni gradiente sia facile per
una LUT, ma mostra che una griglia fine e una buona interpolazione possono
rappresentare bene trasformazioni cromatiche continue quando non intervengono
modifiche semantiche forti.

![Test sui gradienti: `L2_tramonto_lago / p03_cold_winter_grade`. L'errore resta contenuto nonostante cielo e acqua contengano transizioni continue.](images_lut/L2_tramonto_lago/p03_cold_winter_grade/best_summary.png){ width=100% }

## Casi intermedi

`L2_roccia` e `L3_ragazzi` mostrano che una buona metrica non elimina la
necessità di analisi visiva. La roccia contiene texture naturale e variazioni
locali; i ragazzi introducono pelle, volti e abiti. In questi casi piccoli
spostamenti cromatici possono essere più visibili, anche quando Delta E e PSNR
restano accettabili.

![Caso percettivamente delicato: `L3_ragazzi / p01_warm_cinematic`. La LUT approssima il grading globale, ma pelle e volti rendono visibili differenze locali.](images_lut/L3_ragazzi/p01_warm_cinematic/best_summary.png){ width=100% }

## Casi limite

I casi limite sono scelti con due criteri: metriche peggiori e valore
interpretativo della figura. Il peggior caso per PSNR, SSIM e Delta E medio è
`L4_citta / p03_cold_winter_grade`. Il peggior Delta E p95 è invece
`L2_roccia / p01_warm_cinematic`, dove texture naturale e variazioni locali
producono errori molto concentrati. `L4_bracciali` e `L4_citta` sono comunque i
casi più utili per mostrare il limite strutturale della LUT globale: materiali,
dettagli, insegne, vetri, riflessi e ombre possono essere trattati da FLUX in
modo localmente diverso. Una LUT globale non può distinguere due pixel con RGB
simile ma contenuto diverso.

![Caso con materiali e dettagli minuti: `L4_bracciali / p02_teal_orange`. Gli errori si concentrano su riflessi, bordi e piccoli oggetti.](images_lut/L4_bracciali/p02_teal_orange/best_summary.png){ width=100% }

`L2_roccia / p01_warm_cinematic` è istruttivo per un motivo diverso: non è
una scena semanticamente complessa come la città, ma la texture naturale della
roccia produce errori locali molto marcati. È il caso peggiore per Delta E p95
tra le migliori varianti, con valore `36.610`, e mostra che anche una scena
senza persone o oggetti urbani può essere difficile quando il target introduce
variazioni locali non uniformi.

![Caso limite su texture naturale: `L2_roccia / p01_warm_cinematic`. La metrica Delta E p95 evidenzia errori localizzati sulle variazioni fini della superficie.](images_lut/L2_roccia/p01_warm_cinematic/best_summary.png){ width=100% }

Il fallimento più istruttivo è `L4_citta / p03_cold_winter_grade`: anche la
migliore variante ha PSNR `18.279`, SSIM `0.9084`, Delta E medio `12.163` e
Delta E p95 `33.863`. La heatmap mostra errori su insegne, bordi, finestre,
persone e regioni urbane dense. Il problema non è solo la precisione della LUT:
il target diffusion contiene modifiche locali e semantiche.

![Caso limite: `L4_citta / p03_cold_winter_grade`. La LUT riproduce parte del look freddo, ma fallisce dove il target FLUX modifica dettagli locali e strutture urbane.](images_lut/L4_citta/p03_cold_winter_grade/best_summary.png){ width=100% }

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
PSNR e SSIM favoriscono fedeltà pixel-per-pixel e struttura luminosa; Delta E
misura meglio l'errore cromatico; le heatmap mostrano dove l'errore si concentra.
Il valore dell'esperimento sta proprio nell'usare insieme queste informazioni:
le metriche ordinano i casi, le figure spiegano perché la LUT funziona o
fallisce.

# Limiti

Il lavoro ha alcuni limiti importanti:

- la LUT è globale e non usa informazione spaziale;
- il fitting assume corrispondenza pixel-per-pixel tra originale e target;
- se FLUX cambia la struttura della scena, il confronto diventa meno
  interpretabile;
- la SSIM usata è una misura su luminanza, non un giudizio percettivo completo;
- il dataset è piccolo e pensato come studio sperimentale, non come benchmark
  esaustivo;
- i risultati dipendono dal modello locale, dai prompt e dal seed;
- le immagini Unsplash richiedono attribuzione esterna se usate in una
  distribuzione pubblica del PDF.

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

La generazione del PDF è pensata per essere eseguita dalla root del repository:

```bash
pandoc paper/paper.md \
  --pdf-engine=xelatex \
  -V documentclass=article \
  -V geometry:margin=2.5cm \
  --resource-path=.:paper \
  -o paper/paper.pdf
```
