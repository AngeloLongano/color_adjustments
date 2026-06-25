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

Data generazione: 2026-06-25

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

{\Large Per ogni target viene mostrata la migliore ricostruzione LUT selezionata per Delta E CIEDE2000 medio.}
\vspace{0.9cm}

\textcolor[HTML]{2563EB}{\rule{0.52\textwidth}{1.1pt}}
\end{center}
\clearpage

# Risultati LUT: migliore ricostruzione per Delta E CIEDE2000 medio

Questa sezione mette in evidenza il risultato principale del fitting: per ogni target FLUX viene mostrata la variante LUT migliore secondo il Delta E CIEDE2000 medio.

## L1_foglia / p01_warm_cinematic

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_median\_trilinear} $(LUT=65^3, fit=median, apply=trilinear)$\\
PSNR RGB: \textbf{26.312} \quad SSIM: \textbf{0.834} \quad Delta E medio: \textbf{4.096} \quad Delta E p95: \textbf{12.133}
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
PSNR RGB: \textbf{27.181} \quad SSIM: \textbf{0.875} \quad Delta E medio: \textbf{3.708} \quad Delta E p95: \textbf{9.957}
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
PSNR RGB: \textbf{27.019} \quad SSIM: \textbf{0.832} \quad Delta E medio: \textbf{2.952} \quad Delta E p95: \textbf{8.369}
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
PSNR RGB: \textbf{24.612} \quad SSIM: \textbf{0.564} \quad Delta E medio: \textbf{5.240} \quad Delta E p95: \textbf{12.519}
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
PSNR RGB: \textbf{27.973} \quad SSIM: \textbf{0.868} \quad Delta E medio: \textbf{3.482} \quad Delta E p95: \textbf{9.931}
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
PSNR RGB: \textbf{24.870} \quad SSIM: \textbf{0.841} \quad Delta E medio: \textbf{3.828} \quad Delta E p95: \textbf{11.733}
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
PSNR RGB: \textbf{28.356} \quad SSIM: \textbf{0.883} \quad Delta E medio: \textbf{3.090} \quad Delta E p95: \textbf{9.067}
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
PSNR RGB: \textbf{26.469} \quad SSIM: \textbf{0.682} \quad Delta E medio: \textbf{4.275} \quad Delta E p95: \textbf{10.911}
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
PSNR RGB: \textbf{20.388} \quad SSIM: \textbf{0.689} \quad Delta E medio: \textbf{7.116} \quad Delta E p95: \textbf{23.282}
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
PSNR RGB: \textbf{25.873} \quad SSIM: \textbf{0.720} \quad Delta E medio: \textbf{5.796} \quad Delta E p95: \textbf{19.137}
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
PSNR RGB: \textbf{22.162} \quad SSIM: \textbf{0.743} \quad Delta E medio: \textbf{5.480} \quad Delta E p95: \textbf{15.563}
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
PSNR RGB: \textbf{23.203} \quad SSIM: \textbf{0.674} \quad Delta E medio: \textbf{6.338} \quad Delta E p95: \textbf{17.557}
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
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{21.981} \quad SSIM: \textbf{0.827} \quad Delta E medio: \textbf{4.562} \quad Delta E p95: \textbf{16.600}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L2_tramonto_lago/p01_warm_cinematic/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L2\_tramonto\_lago / p01\_warm\_cinematic}
\end{center}

\clearpage

## L2_tramonto_lago / p02_teal_orange

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{24.069} \quad SSIM: \textbf{0.857} \quad Delta E medio: \textbf{3.543} \quad Delta E p95: \textbf{12.433}
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
PSNR RGB: \textbf{25.677} \quad SSIM: \textbf{0.882} \quad Delta E medio: \textbf{2.542} \quad Delta E p95: \textbf{9.331}
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
PSNR RGB: \textbf{22.698} \quad SSIM: \textbf{0.492} \quad Delta E medio: \textbf{5.962} \quad Delta E p95: \textbf{14.340}
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
PSNR RGB: \textbf{23.281} \quad SSIM: \textbf{0.739} \quad Delta E medio: \textbf{6.173} \quad Delta E p95: \textbf{16.498}
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
PSNR RGB: \textbf{25.123} \quad SSIM: \textbf{0.775} \quad Delta E medio: \textbf{4.842} \quad Delta E p95: \textbf{14.701}
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
PSNR RGB: \textbf{26.421} \quad SSIM: \textbf{0.816} \quad Delta E medio: \textbf{2.547} \quad Delta E p95: \textbf{8.403}
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
PSNR RGB: \textbf{23.521} \quad SSIM: \textbf{0.687} \quad Delta E medio: \textbf{4.834} \quad Delta E p95: \textbf{13.854}
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
Variante migliore: \texttt{lut\_65\_median\_trilinear} $(LUT=65^3, fit=median, apply=trilinear)$\\
PSNR RGB: \textbf{26.529} \quad SSIM: \textbf{0.855} \quad Delta E medio: \textbf{3.925} \quad Delta E p95: \textbf{12.551}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L3_ragazzi/p01_warm_cinematic/lut_65_median_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L3\_ragazzi / p01\_warm\_cinematic}
\end{center}

\clearpage

## L3_ragazzi / p02_teal_orange

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{26.486} \quad SSIM: \textbf{0.824} \quad Delta E medio: \textbf{3.901} \quad Delta E p95: \textbf{13.913}
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
PSNR RGB: \textbf{24.447} \quad SSIM: \textbf{0.863} \quad Delta E medio: \textbf{4.210} \quad Delta E p95: \textbf{14.238}
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
PSNR RGB: \textbf{23.375} \quad SSIM: \textbf{0.665} \quad Delta E medio: \textbf{5.687} \quad Delta E p95: \textbf{15.429}
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
PSNR RGB: \textbf{22.550} \quad SSIM: \textbf{0.803} \quad Delta E medio: \textbf{5.690} \quad Delta E p95: \textbf{17.875}
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
PSNR RGB: \textbf{23.360} \quad SSIM: \textbf{0.769} \quad Delta E medio: \textbf{5.676} \quad Delta E p95: \textbf{18.678}
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
PSNR RGB: \textbf{22.874} \quad SSIM: \textbf{0.763} \quad Delta E medio: \textbf{4.926} \quad Delta E p95: \textbf{13.995}
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
PSNR RGB: \textbf{22.795} \quad SSIM: \textbf{0.721} \quad Delta E medio: \textbf{5.994} \quad Delta E p95: \textbf{16.466}
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
Variante migliore: \texttt{lut\_65\_median\_trilinear} $(LUT=65^3, fit=median, apply=trilinear)$\\
PSNR RGB: \textbf{21.948} \quad SSIM: \textbf{0.822} \quad Delta E medio: \textbf{5.705} \quad Delta E p95: \textbf{19.182}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L4_citta/p01_warm_cinematic/lut_65_median_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L4\_citta / p01\_warm\_cinematic}
\end{center}

\clearpage

## L4_citta / p02_teal_orange

\begin{center}
\setlength{\fboxsep}{8pt}
\fbox{\begin{minipage}{0.88\textwidth}
\textbf{Risultato ottenuto}\\[3pt]
Variante migliore: \texttt{lut\_65\_weighted\_mean\_trilinear} $(LUT=65^3, fit=weighted\_mean, apply=trilinear)$\\
PSNR RGB: \textbf{25.738} \quad SSIM: \textbf{0.813} \quad Delta E medio: \textbf{4.122} \quad Delta E p95: \textbf{13.422}
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
PSNR RGB: \textbf{18.279} \quad SSIM: \textbf{0.693} \quad Delta E medio: \textbf{8.610} \quad Delta E p95: \textbf{25.493}
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
PSNR RGB: \textbf{23.718} \quad SSIM: \textbf{0.850} \quad Delta E medio: \textbf{5.545} \quad Delta E p95: \textbf{14.198}
\end{minipage}}
\end{center}

\begin{center}
\includegraphics[width=0.98\textwidth,height=0.62\textheight,keepaspectratio]{images_lut/L4_citta/p04_faded_matte/lut_65_weighted_mean_trilinear_reconstruction.png}\\[2pt]
{\small Ricostruzione LUT best - L4\_citta / p04\_faded\_matte}
\end{center}

\clearpage
