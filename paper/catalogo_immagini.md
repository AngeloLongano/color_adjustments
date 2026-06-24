---
title-meta: "Catalogo immagini sperimentali"
author-meta: "Angelo Longano"
lang: "it"
toc: true
numbersections: false
colorlinks: true
geometry: "a4paper,margin=1.2cm,landscape"
fontsize: 10pt
header-includes:
  - \usepackage{xcolor}
  - \usepackage{graphicx}
  - \usepackage{float}
  - \setlength{\parindent}{0pt}
  - \setlength{\parskip}{0.35em}
---

# Catalogo immagini sperimentali

Appendice visiva generata automaticamente dagli asset della pipeline. Le immagini sono inserite una per blocco, senza crop e con aspect ratio preservato.

Data generazione: 2026-06-24

\clearpage

\clearpage
\thispagestyle{empty}
\vspace*{0.22\textheight}
\begin{center}
{\Huge\bfseries Prompt usati}
\vspace{0.8cm}

{\Large Le quattro richieste di color grading applicate a tutte le immagini.}
\vspace{0.9cm}

\textcolor[HTML]{2563EB}{\rule{0.52\textwidth}{1.1pt}}
\end{center}
\clearpage

# Prompt usati

- `p01_warm_cinematic`: same photograph, preserve exact scene structure and object shapes, warm cinematic color grading, golden highlights, slightly warm shadows, natural realistic colors, no new objects, no texture changes
- `p02_teal_orange`: same photograph, preserve exact scene structure and object shapes, cinematic teal and orange color grade, cool teal shadows, warm orange highlights, realistic photography, no new objects, no texture changes
- `p03_cold_winter_grade`: same photograph, preserve exact scene structure and object shapes, cold winter color grading, cool blue shadows, desaturated colors, crisp atmosphere, realistic photography, no snow, no new objects, no texture changes
- `p04_faded_matte`: same photograph, preserve exact scene structure and object shapes, faded matte film color grade, muted saturation, soft contrast, slightly lifted shadows, realistic photography, no new objects, no texture changes

\clearpage

\clearpage
\thispagestyle{empty}
\vspace*{0.22\textheight}
\begin{center}
{\Huge\bfseries Originali preparati}
\vspace{0.8cm}

{\Large Immagini di partenza gia' ridimensionate dalla pipeline.}
\vspace{0.9cm}

\textcolor[HTML]{2563EB}{\rule{0.52\textwidth}{1.1pt}}
\end{center}
\clearpage

# Originali preparati

## L1_foglia

File sorgente: `foglia.tif`  
File preparato: `images/L1_foglia.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images/L1_foglia.png}\\[2pt]
{\small L1\_foglia - L1 - foglia - 1008x672px}
\end{center}

\clearpage

## L2_roccia

File sorgente: `roccia.tif`  
File preparato: `images/L2_roccia.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images/L2_roccia.png}\\[2pt]
{\small L2\_roccia - L2 - roccia - 1008x672px}
\end{center}

\clearpage

## L2_fiori

File sorgente: `fiori.tif`  
File preparato: `images/L2_fiori.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images/L2_fiori.png}\\[2pt]
{\small L2\_fiori - L2 - fiori - 1008x672px}
\end{center}

\clearpage

## L3_ragazzi

File sorgente: `ragazzi.tif`  
File preparato: `images/L3_ragazzi.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images/L3_ragazzi.png}\\[2pt]
{\small L3\_ragazzi - L3 - ragazzi - 1008x672px}
\end{center}

\clearpage

## L4_citta

File sorgente: `citta.tif`  
File preparato: `images/L4_citta.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images/L4_citta.png}\\[2pt]
{\small L4\_citta - L4 - citta - 1008x672px}
\end{center}

\clearpage

## L4_bracciali

File sorgente: `bracciali.tif`  
File preparato: `images/L4_bracciali.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images/L4_bracciali.png}\\[2pt]
{\small L4\_bracciali - L4 - bracciali - 1008x672px}
\end{center}

\clearpage

## L2_tramonto_mare

File sorgente: `tramonto_mare.jpg`  
File preparato: `images/L2_tramonto_mare.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images/L2_tramonto_mare.png}\\[2pt]
{\small L2\_tramonto\_mare - L2 - tramonto\_mare - 1008x672px}
\end{center}

\clearpage

## L2_tramonto_lago

File sorgente: `tramonto_lago.jpg`  
File preparato: `images/L2_tramonto_lago.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images/L2_tramonto_lago.png}\\[2pt]
{\small L2\_tramonto\_lago - L2 - tramonto\_lago - 1008x672px}
\end{center}

\clearpage

\clearpage
\thispagestyle{empty}
\vspace*{0.22\textheight}
\begin{center}
{\Huge\bfseries Target FLUX}
\vspace{0.8cm}

{\Large Risultati image-to-image generati per ogni coppia immagine-prompt.}
\vspace{0.9cm}

\textcolor[HTML]{2563EB}{\rule{0.52\textwidth}{1.1pt}}
\end{center}
\clearpage

# Target generati da FLUX

## L1_foglia

### p01_warm_cinematic

File: `images_flux/target/L1_foglia/p01_warm_cinematic_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L1_foglia/p01_warm_cinematic_s0_flux-klein-4b-base.png}\\[2pt]
{\small L1\_foglia / p01\_warm\_cinematic - 1008x672px}
\end{center}

\clearpage

### p02_teal_orange

File: `images_flux/target/L1_foglia/p02_teal_orange_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L1_foglia/p02_teal_orange_s0_flux-klein-4b-base.png}\\[2pt]
{\small L1\_foglia / p02\_teal\_orange - 1008x672px}
\end{center}

\clearpage

### p03_cold_winter_grade

File: `images_flux/target/L1_foglia/p03_cold_winter_grade_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L1_foglia/p03_cold_winter_grade_s0_flux-klein-4b-base.png}\\[2pt]
{\small L1\_foglia / p03\_cold\_winter\_grade - 1008x672px}
\end{center}

\clearpage

### p04_faded_matte

File: `images_flux/target/L1_foglia/p04_faded_matte_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L1_foglia/p04_faded_matte_s0_flux-klein-4b-base.png}\\[2pt]
{\small L1\_foglia / p04\_faded\_matte - 1008x672px}
\end{center}

\clearpage

## L2_roccia

### p01_warm_cinematic

File: `images_flux/target/L2_roccia/p01_warm_cinematic_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_roccia/p01_warm_cinematic_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_roccia / p01\_warm\_cinematic - 1008x672px}
\end{center}

\clearpage

### p02_teal_orange

File: `images_flux/target/L2_roccia/p02_teal_orange_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_roccia/p02_teal_orange_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_roccia / p02\_teal\_orange - 1008x672px}
\end{center}

\clearpage

### p03_cold_winter_grade

File: `images_flux/target/L2_roccia/p03_cold_winter_grade_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_roccia/p03_cold_winter_grade_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_roccia / p03\_cold\_winter\_grade - 1008x672px}
\end{center}

\clearpage

### p04_faded_matte

File: `images_flux/target/L2_roccia/p04_faded_matte_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_roccia/p04_faded_matte_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_roccia / p04\_faded\_matte - 1008x672px}
\end{center}

\clearpage

## L2_fiori

### p01_warm_cinematic

File: `images_flux/target/L2_fiori/p01_warm_cinematic_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_fiori/p01_warm_cinematic_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_fiori / p01\_warm\_cinematic - 1008x672px}
\end{center}

\clearpage

### p02_teal_orange

File: `images_flux/target/L2_fiori/p02_teal_orange_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_fiori/p02_teal_orange_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_fiori / p02\_teal\_orange - 1008x672px}
\end{center}

\clearpage

### p03_cold_winter_grade

File: `images_flux/target/L2_fiori/p03_cold_winter_grade_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_fiori/p03_cold_winter_grade_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_fiori / p03\_cold\_winter\_grade - 1008x672px}
\end{center}

\clearpage

### p04_faded_matte

File: `images_flux/target/L2_fiori/p04_faded_matte_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_fiori/p04_faded_matte_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_fiori / p04\_faded\_matte - 1008x672px}
\end{center}

\clearpage

## L3_ragazzi

### p01_warm_cinematic

File: `images_flux/target/L3_ragazzi/p01_warm_cinematic_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L3_ragazzi/p01_warm_cinematic_s0_flux-klein-4b-base.png}\\[2pt]
{\small L3\_ragazzi / p01\_warm\_cinematic - 1008x672px}
\end{center}

\clearpage

### p02_teal_orange

File: `images_flux/target/L3_ragazzi/p02_teal_orange_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L3_ragazzi/p02_teal_orange_s0_flux-klein-4b-base.png}\\[2pt]
{\small L3\_ragazzi / p02\_teal\_orange - 1008x672px}
\end{center}

\clearpage

### p03_cold_winter_grade

File: `images_flux/target/L3_ragazzi/p03_cold_winter_grade_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L3_ragazzi/p03_cold_winter_grade_s0_flux-klein-4b-base.png}\\[2pt]
{\small L3\_ragazzi / p03\_cold\_winter\_grade - 1008x672px}
\end{center}

\clearpage

### p04_faded_matte

File: `images_flux/target/L3_ragazzi/p04_faded_matte_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L3_ragazzi/p04_faded_matte_s0_flux-klein-4b-base.png}\\[2pt]
{\small L3\_ragazzi / p04\_faded\_matte - 1008x672px}
\end{center}

\clearpage

## L4_citta

### p01_warm_cinematic

File: `images_flux/target/L4_citta/p01_warm_cinematic_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L4_citta/p01_warm_cinematic_s0_flux-klein-4b-base.png}\\[2pt]
{\small L4\_citta / p01\_warm\_cinematic - 1008x672px}
\end{center}

\clearpage

### p02_teal_orange

File: `images_flux/target/L4_citta/p02_teal_orange_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L4_citta/p02_teal_orange_s0_flux-klein-4b-base.png}\\[2pt]
{\small L4\_citta / p02\_teal\_orange - 1008x672px}
\end{center}

\clearpage

### p03_cold_winter_grade

File: `images_flux/target/L4_citta/p03_cold_winter_grade_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L4_citta/p03_cold_winter_grade_s0_flux-klein-4b-base.png}\\[2pt]
{\small L4\_citta / p03\_cold\_winter\_grade - 1008x672px}
\end{center}

\clearpage

### p04_faded_matte

File: `images_flux/target/L4_citta/p04_faded_matte_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L4_citta/p04_faded_matte_s0_flux-klein-4b-base.png}\\[2pt]
{\small L4\_citta / p04\_faded\_matte - 1008x672px}
\end{center}

\clearpage

## L4_bracciali

### p01_warm_cinematic

File: `images_flux/target/L4_bracciali/p01_warm_cinematic_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L4_bracciali/p01_warm_cinematic_s0_flux-klein-4b-base.png}\\[2pt]
{\small L4\_bracciali / p01\_warm\_cinematic - 1008x672px}
\end{center}

\clearpage

### p02_teal_orange

File: `images_flux/target/L4_bracciali/p02_teal_orange_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L4_bracciali/p02_teal_orange_s0_flux-klein-4b-base.png}\\[2pt]
{\small L4\_bracciali / p02\_teal\_orange - 1008x672px}
\end{center}

\clearpage

### p03_cold_winter_grade

File: `images_flux/target/L4_bracciali/p03_cold_winter_grade_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L4_bracciali/p03_cold_winter_grade_s0_flux-klein-4b-base.png}\\[2pt]
{\small L4\_bracciali / p03\_cold\_winter\_grade - 1008x672px}
\end{center}

\clearpage

### p04_faded_matte

File: `images_flux/target/L4_bracciali/p04_faded_matte_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L4_bracciali/p04_faded_matte_s0_flux-klein-4b-base.png}\\[2pt]
{\small L4\_bracciali / p04\_faded\_matte - 1008x672px}
\end{center}

\clearpage

## L2_tramonto_mare

### p01_warm_cinematic

File: `images_flux/target/L2_tramonto_mare/p01_warm_cinematic_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_tramonto_mare/p01_warm_cinematic_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_tramonto\_mare / p01\_warm\_cinematic - 1008x672px}
\end{center}

\clearpage

### p02_teal_orange

File: `images_flux/target/L2_tramonto_mare/p02_teal_orange_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_tramonto_mare/p02_teal_orange_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_tramonto\_mare / p02\_teal\_orange - 1008x672px}
\end{center}

\clearpage

### p03_cold_winter_grade

File: `images_flux/target/L2_tramonto_mare/p03_cold_winter_grade_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_tramonto_mare/p03_cold_winter_grade_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_tramonto\_mare / p03\_cold\_winter\_grade - 1008x672px}
\end{center}

\clearpage

### p04_faded_matte

File: `images_flux/target/L2_tramonto_mare/p04_faded_matte_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_tramonto_mare/p04_faded_matte_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_tramonto\_mare / p04\_faded\_matte - 1008x672px}
\end{center}

\clearpage

## L2_tramonto_lago

### p01_warm_cinematic

File: `images_flux/target/L2_tramonto_lago/p01_warm_cinematic_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_tramonto_lago/p01_warm_cinematic_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_tramonto\_lago / p01\_warm\_cinematic - 1008x672px}
\end{center}

\clearpage

### p02_teal_orange

File: `images_flux/target/L2_tramonto_lago/p02_teal_orange_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_tramonto_lago/p02_teal_orange_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_tramonto\_lago / p02\_teal\_orange - 1008x672px}
\end{center}

\clearpage

### p03_cold_winter_grade

File: `images_flux/target/L2_tramonto_lago/p03_cold_winter_grade_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_tramonto_lago/p03_cold_winter_grade_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_tramonto\_lago / p03\_cold\_winter\_grade - 1008x672px}
\end{center}

\clearpage

### p04_faded_matte

File: `images_flux/target/L2_tramonto_lago/p04_faded_matte_s0_flux-klein-4b-base.png`  
Dimensioni: 1008x672px

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.78\textheight,keepaspectratio]{images_flux/target/L2_tramonto_lago/p04_faded_matte_s0_flux-klein-4b-base.png}\\[2pt]
{\small L2\_tramonto\_lago / p04\_faded\_matte - 1008x672px}
\end{center}

\clearpage

\clearpage
\thispagestyle{empty}
\vspace*{0.22\textheight}
\begin{center}
{\Huge\bfseries Risultati LUT}
\vspace{0.8cm}

{\Large Per ogni target viene mostrata la migliore ricostruzione LUT selezionata per Delta E medio.}
\vspace{0.9cm}

\textcolor[HTML]{2563EB}{\rule{0.52\textwidth}{1.1pt}}
\end{center}
\clearpage

# Risultati LUT: migliore ricostruzione per Delta E medio

Questa sezione mette in evidenza il risultato principale del fitting: per ogni target FLUX viene mostrata la variante LUT migliore secondo il Delta E medio.

## L1_foglia / p01_warm_cinematic

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_median\_trilinear} $(LUT=65^3, fit=median, apply=trilinear)$\\
PSNR RGB: \textbf{26.312} \quad SSIM luminanza: \textbf{0.974} \quad Delta E medio: \textbf{6.319} \quad Delta E p95: \textbf{18.870}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L1_foglia/p01_warm_cinematic/lut_65_median_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L1\_foglia / p01\_warm\_cinematic}
\end{center}

\clearpage

## L1_foglia / p02_teal_orange

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{27.181} \quad SSIM luminanza: \textbf{0.970} \quad Delta E medio: \textbf{5.451} \quad Delta E p95: \textbf{14.669}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L1_foglia/p02_teal_orange/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L1\_foglia / p02\_teal\_orange}
\end{center}

\clearpage

## L1_foglia / p03_cold_winter_grade

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{27.019} \quad SSIM luminanza: \textbf{0.972} \quad Delta E medio: \textbf{5.297} \quad Delta E p95: \textbf{13.993}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L1_foglia/p03_cold_winter_grade/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L1\_foglia / p03\_cold\_winter\_grade}
\end{center}

\clearpage

## L1_foglia / p04_faded_matte

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{24.612} \quad SSIM luminanza: \textbf{0.975} \quad Delta E medio: \textbf{7.836} \quad Delta E p95: \textbf{17.801}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L1_foglia/p04_faded_matte/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L1\_foglia / p04\_faded\_matte}
\end{center}

\clearpage

## L2_fiori / p01_warm_cinematic

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{27.973} \quad SSIM luminanza: \textbf{0.994} \quad Delta E medio: \textbf{5.480} \quad Delta E p95: \textbf{15.933}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_fiori/p01_warm_cinematic/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_fiori / p01\_warm\_cinematic}
\end{center}

\clearpage

## L2_fiori / p02_teal_orange

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{24.870} \quad SSIM luminanza: \textbf{0.991} \quad Delta E medio: \textbf{6.075} \quad Delta E p95: \textbf{19.120}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_fiori/p02_teal_orange/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_fiori / p02\_teal\_orange}
\end{center}

\clearpage

## L2_fiori / p03_cold_winter_grade

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{28.356} \quad SSIM luminanza: \textbf{0.992} \quad Delta E medio: \textbf{5.584} \quad Delta E p95: \textbf{16.709}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_fiori/p03_cold_winter_grade/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_fiori / p03\_cold\_winter\_grade}
\end{center}

\clearpage

## L2_fiori / p04_faded_matte

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{26.469} \quad SSIM luminanza: \textbf{0.990} \quad Delta E medio: \textbf{6.133} \quad Delta E p95: \textbf{16.319}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_fiori/p04_faded_matte/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_fiori / p04\_faded\_matte}
\end{center}

\clearpage

## L2_roccia / p01_warm_cinematic

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_median\_trilinear} $(LUT=65^3, fit=median, apply=trilinear)$\\
PSNR RGB: \textbf{20.388} \quad SSIM luminanza: \textbf{0.951} \quad Delta E medio: \textbf{11.163} \quad Delta E p95: \textbf{36.610}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_roccia/p01_warm_cinematic/lut_65_median_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_roccia / p01\_warm\_cinematic}
\end{center}

\clearpage

## L2_roccia / p02_teal_orange

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{25.873} \quad SSIM luminanza: \textbf{0.988} \quad Delta E medio: \textbf{7.870} \quad Delta E p95: \textbf{24.861}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_roccia/p02_teal_orange/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_roccia / p02\_teal\_orange}
\end{center}

\clearpage

## L2_roccia / p03_cold_winter_grade

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{22.162} \quad SSIM luminanza: \textbf{0.948} \quad Delta E medio: \textbf{9.525} \quad Delta E p95: \textbf{25.415}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_roccia/p03_cold_winter_grade/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_roccia / p03\_cold\_winter\_grade}
\end{center}

\clearpage

## L2_roccia / p04_faded_matte

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{23.203} \quad SSIM luminanza: \textbf{0.971} \quad Delta E medio: \textbf{8.913} \quad Delta E p95: \textbf{24.307}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_roccia/p04_faded_matte/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_roccia / p04\_faded\_matte}
\end{center}

\clearpage

## L2_tramonto_lago / p01_warm_cinematic

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_median\_nearest} $(LUT=65^3, fit=median, apply=nearest)$\\
PSNR RGB: \textbf{21.087} \quad SSIM luminanza: \textbf{0.957} \quad Delta E medio: \textbf{6.889} \quad Delta E p95: \textbf{28.995}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_tramonto_lago/p01_warm_cinematic/lut_65_median_nearest_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_tramonto\_lago / p01\_warm\_cinematic}
\end{center}

\clearpage

## L2_tramonto_lago / p02_teal_orange

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{24.069} \quad SSIM luminanza: \textbf{0.962} \quad Delta E medio: \textbf{5.281} \quad Delta E p95: \textbf{18.814}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_tramonto_lago/p02_teal_orange/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_tramonto\_lago / p02\_teal\_orange}
\end{center}

\clearpage

## L2_tramonto_lago / p03_cold_winter_grade

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{25.677} \quad SSIM luminanza: \textbf{0.957} \quad Delta E medio: \textbf{3.851} \quad Delta E p95: \textbf{14.689}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_tramonto_lago/p03_cold_winter_grade/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_tramonto\_lago / p03\_cold\_winter\_grade}
\end{center}

\clearpage

## L2_tramonto_lago / p04_faded_matte

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{22.698} \quad SSIM luminanza: \textbf{0.971} \quad Delta E medio: \textbf{7.703} \quad Delta E p95: \textbf{18.722}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_tramonto_lago/p04_faded_matte/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_tramonto\_lago / p04\_faded\_matte}
\end{center}

\clearpage

## L2_tramonto_mare / p01_warm_cinematic

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{23.281} \quad SSIM luminanza: \textbf{0.964} \quad Delta E medio: \textbf{9.339} \quad Delta E p95: \textbf{24.701}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_tramonto_mare/p01_warm_cinematic/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_tramonto\_mare / p01\_warm\_cinematic}
\end{center}

\clearpage

## L2_tramonto_mare / p02_teal_orange

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{25.123} \quad SSIM luminanza: \textbf{0.979} \quad Delta E medio: \textbf{7.405} \quad Delta E p95: \textbf{22.239}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_tramonto_mare/p02_teal_orange/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_tramonto\_mare / p02\_teal\_orange}
\end{center}

\clearpage

## L2_tramonto_mare / p03_cold_winter_grade

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{26.421} \quad SSIM luminanza: \textbf{0.976} \quad Delta E medio: \textbf{4.862} \quad Delta E p95: \textbf{15.154}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_tramonto_mare/p03_cold_winter_grade/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_tramonto\_mare / p03\_cold\_winter\_grade}
\end{center}

\clearpage

## L2_tramonto_mare / p04_faded_matte

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{23.521} \quad SSIM luminanza: \textbf{0.960} \quad Delta E medio: \textbf{6.784} \quad Delta E p95: \textbf{18.047}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_tramonto_mare/p04_faded_matte/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_tramonto\_mare / p04\_faded\_matte}
\end{center}

\clearpage

## L3_ragazzi / p01_warm_cinematic

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{26.840} \quad SSIM luminanza: \textbf{0.990} \quad Delta E medio: \textbf{5.574} \quad Delta E p95: \textbf{17.836}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L3_ragazzi/p01_warm_cinematic/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L3\_ragazzi / p01\_warm\_cinematic}
\end{center}

\clearpage

## L3_ragazzi / p02_teal_orange

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{26.486} \quad SSIM luminanza: \textbf{0.990} \quad Delta E medio: \textbf{6.185} \quad Delta E p95: \textbf{22.272}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L3_ragazzi/p02_teal_orange/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L3\_ragazzi / p02\_teal\_orange}
\end{center}

\clearpage

## L3_ragazzi / p03_cold_winter_grade

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{24.447} \quad SSIM luminanza: \textbf{0.984} \quad Delta E medio: \textbf{6.819} \quad Delta E p95: \textbf{22.521}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L3_ragazzi/p03_cold_winter_grade/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L3\_ragazzi / p03\_cold\_winter\_grade}
\end{center}

\clearpage

## L3_ragazzi / p04_faded_matte

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{23.375} \quad SSIM luminanza: \textbf{0.978} \quad Delta E medio: \textbf{7.971} \quad Delta E p95: \textbf{21.942}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L3_ragazzi/p04_faded_matte/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L3\_ragazzi / p04\_faded\_matte}
\end{center}

\clearpage

## L4_bracciali / p01_warm_cinematic

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{22.550} \quad SSIM luminanza: \textbf{0.968} \quad Delta E medio: \textbf{9.258} \quad Delta E p95: \textbf{30.293}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L4_bracciali/p01_warm_cinematic/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L4\_bracciali / p01\_warm\_cinematic}
\end{center}

\clearpage

## L4_bracciali / p02_teal_orange

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{23.360} \quad SSIM luminanza: \textbf{0.945} \quad Delta E medio: \textbf{7.684} \quad Delta E p95: \textbf{26.059}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L4_bracciali/p02_teal_orange/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L4\_bracciali / p02\_teal\_orange}
\end{center}

\clearpage

## L4_bracciali / p03_cold_winter_grade

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{22.874} \quad SSIM luminanza: \textbf{0.940} \quad Delta E medio: \textbf{9.821} \quad Delta E p95: \textbf{27.014}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L4_bracciali/p03_cold_winter_grade/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L4\_bracciali / p03\_cold\_winter\_grade}
\end{center}

\clearpage

## L4_bracciali / p04_faded_matte

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{22.795} \quad SSIM luminanza: \textbf{0.967} \quad Delta E medio: \textbf{8.343} \quad Delta E p95: \textbf{22.464}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L4_bracciali/p04_faded_matte/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L4\_bracciali / p04\_faded\_matte}
\end{center}

\clearpage

## L4_citta / p01_warm_cinematic

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{22.141} \quad SSIM luminanza: \textbf{0.968} \quad Delta E medio: \textbf{8.157} \quad Delta E p95: \textbf{27.783}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L4_citta/p01_warm_cinematic/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L4\_citta / p01\_warm\_cinematic}
\end{center}

\clearpage

## L4_citta / p02_teal_orange

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{25.738} \quad SSIM luminanza: \textbf{0.985} \quad Delta E medio: \textbf{5.890} \quad Delta E p95: \textbf{19.582}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L4_citta/p02_teal_orange/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L4\_citta / p02\_teal\_orange}
\end{center}

\clearpage

## L4_citta / p03_cold_winter_grade

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_median\_trilinear} $(LUT=65^3, fit=median, apply=trilinear)$\\
PSNR RGB: \textbf{18.279} \quad SSIM luminanza: \textbf{0.908} \quad Delta E medio: \textbf{12.163} \quad Delta E p95: \textbf{33.863}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L4_citta/p03_cold_winter_grade/lut_65_median_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L4\_citta / p03\_cold\_winter\_grade}
\end{center}

\clearpage

## L4_citta / p04_faded_matte

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{23.718} \quad SSIM luminanza: \textbf{0.974} \quad Delta E medio: \textbf{7.027} \quad Delta E p95: \textbf{17.358}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L4_citta/p04_faded_matte/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L4\_citta / p04\_faded\_matte}
\end{center}

\clearpage
