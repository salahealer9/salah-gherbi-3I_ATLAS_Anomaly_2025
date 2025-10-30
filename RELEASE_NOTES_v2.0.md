# 🚀 3I/ATLAS (C/2019 Y4) — Photometric Anomaly 2025 (v2.0)

**DOI:** 10.5281/zenodo.17483027  
**Concept DOI:** 10.5281/zenodo.17477597

## 🔭 Overview

Version 2 extends the original 3I/ATLAS (C/2019 Y4) Photometric Anomaly 2025 dataset with a cross-comparison against NASA JPL Horizons predicted magnitudes (Tmag).  
This release quantitatively tests the anomaly's persistence by comparing observed MPC photometry with modelled brightness values across July–October 2025.

## 🧩 New in v2.0

- New analysis script: `compare_horizons_anomaly.py`
- Residual table: `I3_Horizons_Residuals.csv`
- New figures:
  - `I3_Horizons_Residuals.png`
  - `I3_ATLAS_Horizons_Normalized.png`
- Manifest update: rehashed and timestamped (`anomaly_manifest_20251030_ots.ots`)
- Enhanced reproducibility: includes `environment.yml` and `requirements.txt`
- All outputs cryptographically verified (SHA-256 + OpenTimestamps blockchain proofs)

## 📊 Key Findings

The cross-analysis confirms a sustained brightness excess of **Δm ≈ 4.2 mag (≈ ×47 flux)** between July and October 2025 — a value far exceeding geometric illumination expectations derived from Horizons.

The residuals consistently indicate intrinsic physical activity, likely due to surface reactivation or volatile release following solar conjunction.

## 🧠 Citation

**Gherbi, Salah-Eddin (2025).**  
3I/ATLAS (C/2019 Y4) — Photometric Anomaly 2025 (v2.0: JPL Horizons Comparison).  
Zenodo. https://doi.org/10.5281/zenodo.17483027

## 📘 BibTeX

```bibtex
@dataset{gherbi_3I_ATLAS_anomaly2025_v21,
  author       = {Salah-Eddin Gherbi},
  title        = {3I/ATLAS (C/2019 Y4) — JPL Horizons Comparison},
  year         = {2025},
  publisher    = {Zenodo},
  version      = {v2.1},
  doi          = {10.5281/zenodo.17483027},
  url          = {https://doi.org/10.5281/zenodo.17483027}
}
```

## 🛡️ Verification

All data files, figures, and scripts are SHA-256–verified and timestamp-anchored to the Bitcoin blockchain via OpenTimestamps for permanent, reproducible authenticity.
