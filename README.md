# 🪐 3I/ATLAS (C/2019 Y4) — Photometric Anomaly 2025
📦 **Version 2.1 released:** Includes ZTF cross-validation and updated verification (October 2025)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17477597.svg)](https://doi.org/10.5281/zenodo.17477597)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![OpenTimestamps Verified](https://img.shields.io/badge/Data%20Integrity-OpenTimestamps-orange)](https://opentimestamps.org)
[![Reproducible Research](https://img.shields.io/badge/Reproducible%20Research-YES-brightgreen)](#reproducibility)
[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/salah-gherbi/3I_ATLAS_Anomaly_2025/main)

---

## Overview

This repository contains the dataset and analysis associated with the **photometric brightening anomaly** of *3I/ATLAS (C/2019 Y4)* observed between **July and October 2025**.  
The raw photometric data were extracted from the **Minor Planet Center (MPC)** file `I3.txt` and processed using `print_summary.py` to generate monthly brightness statistics and light-curve figures.

The object exhibited a steady increase in brightness of **Δm ≈ 4.2 mag** (≈ ×47 flux), far exceeding geometric expectations.  
All results are **cryptographically verified** and timestamp-anchored via the **Bitcoin blockchain** using **OpenTimestamps**.

---

## Contents

| File | Description |
|------|-------------|
| `I3.txt` | Raw MPC observation records for 3I/ATLAS (C/2019 Y4) |
| `I3_clean.csv` | Parsed observation table (date, RA, Dec, magnitude) |
| `I3_monthly_summary.csv` | Monthly photometric statistics |
| `I3_lightcurve.png` | Light-curve plot of mean magnitude vs month |
| `I3_ATLAS_Dual_Anomaly.png` | Comparative July–October brightness diagram |
| `I3_ATLAS_Horizons_Normalized.png` | Observed vs JPL Horizons normalized comparison |
| `compare_horizons_anomaly.py` | Comparison script for MPC vs JPL predicted magnitudes |
| `compare_ztf_I3_ATLAS.py` | Attempted MPC vs ZTF DR19 cross-validation |
| `I3_MPC_Only.png` | Fallback plot when no ZTF detections found |
| `anomaly_manifest.txt` | SHA-256 checksum manifest |
| `anomaly_manifest_20251030_v21.ots` | Current blockchain proof |
| `verification_report.txt` | Consolidated integrity verification log |

---

## Results Summary

| Month (2025) | Mean Mag | Std | Count | Notes |
|---------------|-----------|------|--------|--------|
| July | 17.30 ± 1.0 | 1594 | Baseline faint phase |
| August | 16.34 ± 0.6 | 836 | Gradual brightening |
| September | 15.01 ± 0.8 | 246 | Continued increase |
| October | 13.11 ± 0.6 | 15 | Post-conjunction reactivation |

**Δm = 4.19 mag → Flux increase ≈ ×47.5**

This sustained brightening exceeds geometric expectations and suggests **intrinsic physical activity**, likely volatile release or reactivation following solar conjunction.

---

## Reproducibility

Re-run the full analysis:

```bash
python3 print_summary.py
```

Outputs:

- I3_monthly_summary.csv (monthly stats)
- I3_lightcurve.png (light-curve figure)
- printed summary in terminal

Requirements:

```bash
pip install pandas matplotlib
```

---

## Verification & Integrity

All files are protected by SHA-256 checksums and timestamp-anchored via OpenTimestamps.

```bash
sha256sum -c anomaly_manifest.txt
ots verify anomaly_manifest.txt.ots
```

Any alteration will invalidate the hashes and cause verification to fail.
The manifest and its .ots proofs ensure permanent, blockchain-verifiable authenticity (timestamp ≈ 2025-10-29 UTC).

---

## Integrity Footer (SHA-256 Hashes)

| File | SHA-256 |
|------|---------|
| `I3.txt` | `4da6ddcb94a7c7cba37ac226133ce0f1fd36acc34fa2a6a12ff2c77d61bfab35` |
| `I3_clean.csv` | `b5102800a8b520438bb7a4640ae8bb09605ba1a15df1b92e515f880be3cf724e` |
| `I3_monthly_summary.csv` | `e3182f0d46c9a75f8fdd5c971b44443fe85ac4029feda9fde2e6db04a587a2d8` |
| `I3_lightcurve.png` | `20f671c9e68720bbd0dc0bb27690ed99fe420e7f1b5f0e9df4b8609edc913991` |
| `I3_ATLAS_Dual_Anomaly.png` | `49ae2fd2cd7c7432117ddbeded171c071d7a92930427c010522e6087e97327ac` |
| `print_summary.py` | `599f3f619e2567b077a06442028e42f77caa69e5b1d9a030fb83084aa0c426eb` |
| `README.md` | `271b71c869c1c93d4690325b1fac99bf8eaf120b3b64daeb6edcacb5bea1cce6` |
| `anomaly_manifest.txt` | `407edd3de659dc5dc78eaf255579d5bde527767822f5b93c877d5dc896e8a2a6` |
| `anomaly_manifest.txt.ots` | `1ce7b697d307fe30ba8a5e22773ada63f696e51783526cb69fd02309b2b37830` |

---

## Citation

Gherbi, Salah-Eddin (2025).  
**3I/ATLAS (C/2019 Y4) — Photometric Anomaly 2025 (v2.1: ZTF Cross-Validation).**  
**Zenodo DOI (v2.1):** [https://doi.org/10.5281/zenodo.17487610](ttps://doi.org/10.5281/zenodo.17487610)  
**Concept DOI:** [https://doi.org/10.5281/zenodo.17477597](https://doi.org/10.5281/zenodo.17477597)

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
**Zenodo DOI (v2.1):** [https://doi.org/10.5281/zenodo.17487610](ttps://doi.org/10.5281/zenodo.17487610)
**Concept DOI (all versions):** [https://doi.org/10.5281/zenodo.17477597](https://doi.org/10.5281/zenodo.17477597)

