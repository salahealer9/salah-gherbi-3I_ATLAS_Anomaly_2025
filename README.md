# 🪐 3I/ATLAS (C/2019 Y4) — Photometric Anomaly 2025
📦 **Version 2.4 released:** Extended Photometry, Revised Pre-Perihelion Peak, and Post-Perihelion Deceleration  
🧪 Includes NOT Morphological Validation, full MPC photometry to 2025-11-13, and updated cryptographic proofs.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17477597.svg)](https://doi.org/10.5281/zenodo.17477597)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17609914.svg)](https://doi.org/10.5281/zenodo.17609914)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![OpenTimestamps Verified](https://img.shields.io/badge/Data%20Integrity-OpenTimestamps-orange)](https://opentimestamps.org)
[![Reproducible Research](https://img.shields.io/badge/Reproducible%20Research-YES-brightgreen)](#reproducibility)
[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/salah-gherbi/3I_ATLAS_Anomaly_2025/main)

---

## Overview

This repository contains the full photometric and chromatic analysis of the interstellar object **3I/ATLAS (C/2025 N1)** spanning **4,413 Minor Planet Center observations** from **2025-05-08 → 2025-11-13**.

The analysis reveals:

- ✔️ **A revised pre-perihelion optical activity peak**  
  **2025-10-02 (±1 day)**, derived from the time derivative of the inverse magnitude.

- ✔️ **A strong reddening event in \( g - o \)**  
  \( \Delta(g-o) \approx +0.7 \) mag during July–Sept, coincident with the optical acceleration.

- ✔️ **A post-perihelion deceleration phase**  
  Observed between 2025-11-01 and 11-13.

- ✔️ **No cometary tail or fragmentation**  
  Confirmed independently by the 2.6-m Nordic Optical Telescope (2025-11-09).

- ✔️ **Complete cryptographic provenance**  
  All datasets, figures, CSVs, and scripts are sealed with:
  - SHA-256 manifests
  - GPG signatures
  - Bitcoin-anchored OpenTimestamps proofs

Version 2.4 supersedes v2.3 and presents the most complete optical record of 3I/ATLAS to date.

---

## Contents

| File / Folder                          | Description |
|----------------------------------------|-------------|
| `I3.txt`                               | Full MPC photometry (4,413 lines) |
| `I3_Optical_Acceleration_Data.csv`     | Photometric activity proxy |
| `I3_Color_Alerts_*.csv`                | Colour-index pairs (g–o, r–o) |
| `I3_Color_Statistics_*.txt`            | Monthly/epochal colour analysis |
| `I3_Optical_Acceleration_Trend_v2.png` | Updated optical acceleration plot |
| `I3_Optical_Color_Correlation.png`     | Pre-perihelion optical–chromatic coupling |
| `I3_Optical_Color_Correlation_postperi.png` | Post-perihelion deceleration |
| `NOTpictures.pdf`                      | 4-panel NOT morphology analysis |
| `atlas_optical_acceleration_v2.py`     | Activity proxy extractor |
| `atlas_optical_color_correlation_v1.py`| Optical–colour coupling analysis |
| `watch_mpc_colors_plot_v8_4.py`        | Colour-index extraction + alerts |
| `update_I3_data.sh`                    | Automated MPC fetch + manifest + proofs |
| `RUN_LOG.md`                           | Full timestamped run history (SHA-256 + OTS) |
| `*_proof.txt, .asc, .ots`              | Cryptographic proofs |

---

## 🔍 Scientific Results (v2.4)

### ⭐ 1. Pre-Perihelion Optical Acceleration Peak

- Peak detected at **2025-10-02**
- Photometric activity increases smoothly from **July → Oct**
- Acceleration proxy rises by **~10⁻³ (scaled units)**

### ⭐ 2. Colour Reddening (July–Sept)

| Month | Mean g–o | Δ vs Solar | Interpretation |
|-------|----------|------------|----------------|
| July  | 0.61     | ~0         | Neutral / icy reflection |
| Aug   | 0.94     | +0.32      | Dust/organic activation |
| Sept  | 1.34     | +0.72      | Peak reddening |

### ⭐ 3. Post-Perihelion Deceleration (Nov)

- Optical acceleration turns **negative**
- Magnitude increases by **+0.07 mag** since perihelion
- Represents declining activity + dust coma clearing

### ⭐ 4. NOT Morphology (2025-11-09)

- No tail
- No coma asymmetry
- No fragmentation
- Stellar point-source morphology

→ Confirms a short-lived, transient activity incompatible with a typical comet.

---

## ▶️ Reproducing the Analysis

Full pipeline:

```bash
./update_I3_data.sh
python atlas_optical_acceleration_v2.py
python atlas_optical_color_correlation_v1.py
```

This generates:

Colour alerts
Optical acceleration data
Pre/post-perihelion plots
New manifest + signatures
OpenTimestamps Bitcoin anchoring

Requirements:

```bash
pip install pandas numpy matplotlib scipy
```

---

## 🔐 Data Integrity & Blockchain Verification

Each analysis run creates the following verification files:

### 📄 Generated Files
- **`manifest_v2_4.txt`** - SHA-256 hashes of all data files
- **`manifest_v2_4.txt.asc`** - GPG signature file
- **`manifest_v2_4.txt.ots`** - Bitcoin timestamp proof via OpenTimestamps
- **`RUN_LOG.md`** - Complete audit trail with timestamps

### ✅ Verification Commands

#### Verify SHA-256 checksums
```bash
sha256sum -c manifest_v2_4.txt
```

#### Verify GPG signature authenticity
```bash
gpg --verify manifest_v2_4.txt.asc
```

#### Verify Bitcoin blockchain timestamp
```bash
ots verify manifest_v2_4.txt.ots
```

Any alteration will invalidate the hashes and cause verification to fail.
The manifest and its .ots proofs ensure permanent, blockchain-verifiable authenticity (timestamp ≈ 2025-11-14 UTC).

---

## 📄 Citation (Version 2.4)

Gherbi, Salah-Eddin (2025).
*3I/ATLAS Photometric–Chromatic Anomaly (2025): Extended Photometry and Post-Perihelion Deceleration.*
Zenodo. DOI: 10.5281/zenodo.17609914

Concept DOI (all versions):
10.5281/zenodo.17477597

---

## License

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
**Zenodo DOI (v2.4):** [https://doi.org/10.5281/zenodo.17609914](https://doi.org/10.5281/zenodo.17609914)  
**Concept DOI (all versions):** [https://doi.org/10.5281/zenodo.17477597](https://doi.org/10.5281/zenodo.17477597)

