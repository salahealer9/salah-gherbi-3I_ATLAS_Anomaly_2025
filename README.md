# 🪐 3I/ATLAS (C/2025 N1) — Automated Peak Detection, Δv Correction, Spectroscopic Anomaly (Ni/Fe), and Station-Consistency Validation (Version 2.6) — December 2025
📦 **Version 2.6 released:** Automated peak detection, corrected Δv timing, Ni/Fe compositional anomaly integration, extended MPC photometry to 2025-12-01, and full station-level validation of late-November noise features.
🧭 Includes updated Δv modelling, chromatic evolution, IAI extension (Aₓ), and complete cryptographic reproducibility pipeline.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17477597.svg)](https://doi.org/10.5281/zenodo.17477597)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17793630.svg)](https://doi.org/10.5281/zenodo.17793630)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![OpenTimestamps Verified](https://img.shields.io/badge/Data%20Integrity-OpenTimestamps-orange)](https://opentimestamps.org)
[![Reproducible Research](https://img.shields.io/badge/Reproducible%20Research-YES-brightgreen)](#reproducibility)
[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/salah-gherbi/3I_ATLAS_Anomaly_2025/main)

---

# 🌌 Overview

This repository contains the complete photometric, chromatic, and Δv‑based dynamical anomaly analysis for the interstellar object **3I/ATLAS (C/2025 N1)**.

Version 2.6 integrates:

*   Automated detection of optical‑acceleration peaks
*   Corrected Δv timing (first peak = 2025‑09‑09, day −50)
*   Latest MPC photometry through 2025‑12‑01 (4,960 lines)
*   Updated colour–brightness timeline
*   Full station‑level, time‑normalised consistency analysis
*   Incorporation of Ni/Fe spectroscopic anomaly into the IAI (Aₓ)
*   Regenerated Δv and anomaly figures
*   Fully updated LaTeX manuscript + reproducible pipeline
*   Updated proof bundle (SHA‑256 + GPG + OpenTimestamps)

---

## 🚀 What’s New in Version 2.6

### ⭐ 1. Automated Peak Detection
The Δv and acceleration scripts no longer rely on manually‑entered dates. Peaks are now found directly from the MPC‑derived acceleration dataset.
*   First pre‑perihelion peak: 2025‑09‑09
*   Second peak: 2025‑10‑02
*   Auto‑annotated in all Δv plots

### ⭐ 2. Corrected Δv Timing
The corrected −50‑day peak shifts all Δv accumulation, ∆b geometry, and anomaly sequencing.
*   Both 8 m/s and 25 m/s Δv regimes updated.

### ⭐ 3. Spectroscopic Anomaly Component (Aₓ)
From Gemini GMOS + VLT UVES papers (Nov 2025):
*   Weak CN, C₂, C₃ detection
*   Ni/Fe enrichment ≳ Solar System comet norms
*   Added as 5th anomaly axis in the Interstellar Anomaly Index (IAI)
*   Updated IAI: ≈ 0.94

### ⭐ 4. Station‑Consistency Test
A new pipeline (`plot_station_residuals.py`) evaluates whether late‑November pulses are real dynamical events.
*   **Results:**
    *   No station surpasses 3σ
    *   Mixed signs
    *   No temporal clustering
    *   Aggregated bumps = photometric noise, not physical acceleration

### ⭐ 5. Updated Figures
*   New Δv overlay, dual Δv panels
*   Updated acceleration timeline
*   New colour–brightness 2025‑12‑01 figure
*   Regenerated IAI component plots with Aₓ

### ⭐ 6. Extended MPC Photometry
Now includes data through 2025‑12‑01.

### ⭐ 7. Updated Manuscript
**LaTeX v2.6:**
*   Corrected peak timing
*   Added spectroscopic anomaly discussion
*   Added station‑consistency appendix
*   Updated all figures and references

---

# 📁 Repository Structure (Updated for v2.6)

```kotlin
3I_ATLAS_Anomaly_2025/
│
├── data/
│   ├── I3.txt
│   ├── I3_Optical_Acceleration_Data.csv
│   ├── I3_Color_Alerts_*.csv
│   └── I3_Color_Statistics_*.txt
│
├── figures/
│   ├── I3_Optical_Acceleration_Trend_v2.png
│   ├── I3_Optical_Color_Correlation_postperi.png
│   ├── I3_Optical_Acceleration_DeltaV_Figure.png
│   ├── I3_Optical_Acceleration_DeltaV_8_vs_25.png
│   ├── I3_Optical_Acceleration_DeltaV_Overlay.png
│   ├── atlas_anomaly_components.png
│   ├── iai_vs_eccentricity.png
│   └── station_collective_effect_corrected.png
│
├── scripts/
│   ├── atlas_optical_acceleration_v2.py
│   ├── atlas_optical_color_correlation_v1.py
│   ├── atlas_delta_v_from_optical_proxy.py
│   ├── atlas_optical_dv_dual.py
│   ├── plot_atlas_optical_accel_deltav.py
│   ├── plot_station_residuals.py
│   ├── atlas_anomaly_index.py
│   └── iai_vs_eccentricity.py
│
├── manifests/
│   ├── manifest_v2_6.txt
│   ├── manifest_v2_6.txt.sha256
│   ├── manifest_v2_6.txt.asc
│   └── manifest_v2_6.txt.ots
│
├── proof_bundle/
│   └── I3_ATLAS_ProofBundle_20251202_1804.zip
│
├── 3I_ATLAS_Anomaly_2025.tex
├── README_PROOF_v2_6.md
└── RUN_LOG.md
```

---

# 🔍 Scientific Highlights (v2.6)

# 🔍 Scientific Highlights (v2.6)

Version 2.6 introduces major scientific refinements to the 3I/ATLAS anomaly framework, combining updated MPC photometry, fully automated Δv peak detection, new spectroscopic constraints, and an advanced station‑consistency validation pipeline. Collectively, these additions make this the most accurate, internally consistent, and forensically reproducible release to date.

## ⭐ Corrected Peak Timing & Automated Detection

*   The first major pre‑perihelion acceleration spike is now placed at **2025‑09‑09 (day −50)** rather than the earlier assumed date of 2025‑09‑10.
*   A new automated algorithm identifies peaks directly from MPC‑derived physical acceleration, eliminating manual choices and ensuring future updates remain self‑consistent.

## ⭐ Revised Δv Interpretation

Δv models (8 m/s minimal and 25 m/s photometric) have been fully regenerated with corrected timing, yielding updated predictions for ATLAS’s potential encounter geometry with Jupiter. More than 90% of integrated impulse still originates from the two known early pulses.

## ⭐ Ni/Fe Spectroscopic Anomaly Added to IAI (Aₓ)

Newly published Gemini GMOS and VLT/UVES spectra reveal:

*   weak CN–C₂–C₃ gas emission
*   Ni/Fe enrichment exceeding Solar System comet norms

This deviation is now included as a fifth anomaly axis **Aₓ** in the Interstellar Anomaly Index.  
The updated index is **IAI ≈ 0.94**, placing ATLAS among the most anomalous small bodies ever recorded.

## ⭐ Post‑Perihelion Evolution Updated Through 2025‑12‑01

Brightness and colour indices now extend into December 2025.  
The *g*-band dimming of **Δg ≈ +1.5 mag** since perihelion indicates steady fading with **no signs of a third activation event**.

## ⭐ Station‑Consistency Validation (New)

A new dedicated pipeline evaluates whether late‑November anomalies are physical or instrumental.

**Findings:**

*   0 stations exceed the 3σ threshold
*   mixed‑sign behaviour
*   no temporal coherence

**Result:** late‑November bumps are photometric noise, not dynamical impulses.

## ⭐ Updated Manuscript and Figures

All Δv plots, colour–brightness panels, anomaly figures, tables, and LaTeX references have been corrected and expanded.  
A new appendix documents the station‑consistency test in detail.

---

## ▶️ How to Reproduce the Full v2.6 Pipeline

### 1. Install Dependencies

```bash
pip install pandas numpy matplotlib scipy
```

**or**

```bash
conda env create -f environment.yml
conda activate atlas2025
```

### 2. Run Core Analysis

```bash
python atlas_optical_acceleration_v2.py
python atlas_optical_color_correlation_v1.py
```

### 3. Run Δv Modelling

```bash
python atlas_delta_v_from_optical_proxy.py
python plot_atlas_optical_accel_deltav.py
python atlas_optical_dv_dual.py
```

### 4. Compute IAI

```bash
python atlas_anomaly_index.py
python iai_vs_eccentricity.py
```

### 5. Station Consistency Test

```bash
python plot_station_residuals.py
```

### 6. Seal the Release (Optional)

```bash
./protect_atlas_v2_6.sh manifest_v2_6.txt
```

### 🔐 Cryptographic Verification
here is bash:
sha256sum -c manifest_v2_6.txt
gpg --verify manifest_v2_6.txt.asc
ots verify manifest_v2_6.txt.ots

All files are timestamped on the Bitcoin blockchain via OpenTimestamps.

---

## 📄 Citation (Version 2.6)

**Gherbi, Salah-Eddin** (2025).  
*3I/ATLAS (C/2025 N1): PAutomated Peak Detection, Δv Correction, Ni/Fe Integration & Station-Consistency Validation.*  
Zenodo. [https://doi.org/10.5281/zenodo.17793630](https://doi.org/10.5281/zenodo.17793630) 

**Concept DOI** (all versions):  
[doi:10.5281/zenodo.17477597](https://doi.org/10.5281/zenodo.17477597)

---

## 📜 License

All files are released under Creative Commons Attribution 4.0 International (CC BY 4.0).  
Attribution required for reuse; derivatives permitted with citation.

---

## Contact

**Salah-Eddin Gherbi**  
Independent Researcher — United Kingdom  
📧 [salahealer@gmail.com]  
🔗 [https://orcid.org/0009-0005-4017-1095]

---

**Repository:** [https://github.com/salahealer9/salah-gherbi-3I_ATLAS_Anomaly_2025](https://github.com/salahealer9/salah-gherbi-3I_ATLAS_Anomaly_2025)     
**Zenodo DOI (v2.6):** [https://doi.org/10.5281/zenodo.17793630](https://doi.org/10.5281/zenodo.17793630)  
**Concept DOI (all versions):** [https://doi.org/10.5281/zenodo.17477597](https://doi.org/10.5281/zenodo.17477597)

