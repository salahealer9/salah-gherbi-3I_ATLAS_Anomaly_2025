# 🪐 3I/ATLAS (C/2025 N1) — Photometric–Chromatic Anomaly & Δv-Based Dynamics (Version 2.5)
📦 **Version 2.5 released:** Interstellar Anomaly Index (IAI), Δv-based dynamical assessment, extended post-perihelion photometry, and full reproducibility pipeline.
🧭 Includes dual Δv impulse modelling (8 m/s minimal vs 25 m/s photometric), updated optical/chromatic diagnostics, and complete cryptographic sealing.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17477597.svg)](https://doi.org/10.5281/zenodo.17477597)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17692904.svg)](https://doi.org/10.5281/zenodo.17692904)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![OpenTimestamps Verified](https://img.shields.io/badge/Data%20Integrity-OpenTimestamps-orange)](https://opentimestamps.org)
[![Reproducible Research](https://img.shields.io/badge/Reproducible%20Research-YES-brightgreen)](#reproducibility)
[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/salah-gherbi/3I_ATLAS_Anomaly_2025/main)

---

# 🌌 Overview

This repository hosts the complete photometric, chromatic, and dynamical anomaly analysis for the interstellar object **3I/ATLAS (C/2025 N1)**.

Version 2.5 extends the dataset to **2025-11-21**, comprising **4,580 MPC observations**, refined colour indices, Δv modelling, and the introduction of the **Interstellar Anomaly Index (IAI ≈ 0.95)**.

## Major results include:

- **Two sharp pre-perihelion activity spikes** (2025-09-10 & 2025-10-02) dominating the non-gravitational impulse
- **Dual Δv calibration**:
  - **8 m/s minimal** (sufficient for Loeb's ~10⁵ km Jupiter-approach geometry)
  - **25 m/s photometric** (consistent with the fitted non-gravitational parameter A₁)
- **Colour reddening event** Δ(g-o) ≈ 0.7 mag prior to perihelion
- **Stable, dust-free post-perihelion morphology** (confirmed by Nordic Optical Telescope, 2025-11-09)
- **First Interstellar Anomaly Index (IAI)** combining photometric, chromatic, dynamical, and morphological anomalies
- **Full cryptographic verification** (SHA-256 + GPG + OpenTimestamps)

Version 2.5 supersedes v2.4 and is the definitive preprint companion dataset.

---

# 📁 Repository Structure (Updated for v2.5)

## Core Data

| File | Description |
|------|-------------|
| `I3.txt` | Full MPC photometry (2025-05-08 → 2025-11-21) |
| `I3_Optical_Acceleration_Data.csv` | Time series for optical acceleration proxy |
| `I3_Color_Alerts_*.csv` | Filtered colour events |
| `I3_Color_Statistics_*.txt` | Solar reference deltas & epoch summaries |

## Figures (Updated)

**Main Analysis:**
- `I3_Optical_Acceleration_Trend_v2.png`
- `I3_Optical_Color_Correlation.png`
- `I3_Optical_Color_Correlation_postperi.png`

**Δv Analysis Figures:**
- `I3_Optical_Acceleration_DeltaV_Figure.png`
- `I3_Optical_Acceleration_DeltaV_8_vs_25.png`
- `I3_Optical_Acceleration_DeltaV_Overlay.png`

**IAI Figures:**
- `atlas_anomaly_components.png`
- `iai_vs_eccentricity.png`

## Analysis Scripts (v2.5)

**Core Analysis:**
- `atlas_optical_acceleration_v2.py`
- `atlas_optical_color_correlation_v1.py`
- `atlas_anomaly_index.py`
- `iai_vs_eccentricity.py`

**Δv Tools:**
- `atlas_delta_v_from_optical_proxy.py`
- `atlas_optical_dv_dual.py`
- `plot_atlas_optical_accel_deltav.py`

## Pipeline / Automation
- `update_I3_data.sh` — MPC sync + manifest + proofs
- `append_run_log_v3.sh` — Append cryptographic audit entries
- `protect_atlas_v2_5.sh` — Seal manifests for v2.5
- `RUN_LOG.md`

## Manifests & Proofs
- `manifest_v2_5.txt`
- `manifest_v2_5.txt.sha256`
- `manifest_v2_5.txt.asc`
- `manifest_v2_5.txt.ots`
- `I3_ATLAS_ProofBundle_YYYYMMDD_HHMM.zip`

---

# 🔍 Scientific Highlights (v2.5)

## 1. Dual Δv-Based Dynamical Assessment

Two calibrated regimes:

| Regime | Δv | Use |
|--------|----|-----|
| **Minimal** | 8 m/s | Matches Loeb's ∼10⁵ km Jupiter shift |
| **Photometric** | 25 m/s | Matches A₁ & optical acceleration amplitude |

Both models show that **>90% of impulse** originates from two transient pre-perihelion events.

## 2. Interstellar Anomaly Index (IAI ≈ 0.95)

The IAI synthesises:
- Photometric anomaly
- Chromatic anomaly  
- Dynamical anomaly
- Morphological anomaly

ATLAS ranks near the **extreme upper end** of known interstellar objects.

## 3. Extended Post-Perihelion Evolution
- Smooth fading to 2025-11-21
- Negative optical acceleration
- No additional outbursts
- Morphology remains point-like

---

# ▶️ How to Reproduce the Full v2.5 Analysis

Version 2.5 of the 3I/ATLAS analysis is fully reproducible using the Python scripts and pipeline tools provided in this repository. All outputs (CSV, PNG, manifests) are regenerated exactly as in the published release.

## 1. Install Dependencies

```bash
pip install pandas numpy matplotlib scipy
```

Or use the environment file:

```bash
conda env create -f environment.yml
conda activate atlas2025
```

## 2. Update Data From the MPC

Fetch the latest I3.txt, generate SHA-256 manifests, and timestamp everything:

```bash
./update_I3_data.sh
```

This performs:
- MPC fetch
- checksum generation  
- GPG signing
- OpenTimestamps anchoring
- logging into RUN_LOG.md

## 3. Generate Optical & Chromatic Diagnostics

```bash
python atlas_optical_acceleration_v2.py
python atlas_optical_color_correlation_v1.py
```

Outputs:
- I3_Optical_Acceleration_Data.csv
- I3_Optical_Acceleration_Trend_v2.png
- I3_Optical_Color_Correlation.png
- I3_Optical_Color_Correlation_postperi.png

## 4. Perform Δv-Based Dynamical Analysis (v2.5 Addition)

```bash
python atlas_delta_v_from_optical_proxy.py
python plot_atlas_optical_accel_deltav.py
python atlas_optical_dv_dual.py
```

Produces:
- I3_Optical_Acceleration_DeltaV_Figure.png
- I3_Optical_Acceleration_DeltaV_8_vs_25.png
- I3_Optical_Acceleration_DeltaV_Overlay.png
- printed Δb(km) tables for both 8 m/s and 25 m/s

## 5. Compute the Interstellar Anomaly Index (IAI)

```bash
python atlas_anomaly_index.py
python iai_vs_eccentricity.py
```

Outputs:
- atlas_anomaly_components.png
- iai_vs_eccentricity.png

## 6. Seal the Results (Optional but Recommended)

To reproduce the v2.5 cryptographic archival:

```bash
./protect_atlas_v2_5.sh manifest_v2_5.txt
```

This generates:
- manifest_v2_5.txt.sha256
- manifest_v2_5.txt.asc
- manifest_v2_5.txt.ots

All cryptographic events are logged in RUN_LOG.md.

---

# 🔐 Cryptographic Verification

All critical outputs are authenticated using:

- **SHA-256 digest manifests**
- **GPG detached signatures** 
- **Bitcoin-anchored timestamps** via OpenTimestamps

## Verify with:

```bash
sha256sum -c manifest_v2_5.txt
gpg --verify manifest_v2_5.txt.asc
ots verify manifest_v2_5.txt.ots
```

### ✅ Verification Commands

#### Verify SHA-256 checksums
```bash
sha256sum -c manifest_v2_5.txt
```

#### Verify GPG signature authenticity
```bash
gpg --verify manifest_v2_5.txt.asc
```

#### Verify Bitcoin blockchain timestamp
```bash
ots verify manifest_v2_5.txt.ots
```

Any alteration will invalidate the hashes and cause verification to fail.
The manifest and its .ots proofs ensure permanent, blockchain-verifiable authenticity (timestamp ≈ 2025-11-24 UTC).

---

## 📄 Citation (Version 2.5)

**Gherbi, Salah-Eddin** (2025).  
*3I/ATLAS (C/2025 N1): Photometric–Chromatic Anomaly, Δv-Based Dynamics, and Interstellar Anomaly Index.*  
Zenodo. [doi:10.5281/zenodo.17692904](https://doi.org/10.5281/zenodo.17692904)

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
**Zenodo DOI (v2.5):** [https://doi.org/10.5281/zenodo.17692904](https://doi.org/10.5281/zenodo.17692904)  
**Concept DOI (all versions):** [https://doi.org/10.5281/zenodo.17477597](https://doi.org/10.5281/zenodo.17477597)

