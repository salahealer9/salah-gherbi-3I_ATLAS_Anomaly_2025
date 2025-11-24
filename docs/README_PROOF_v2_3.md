# 🪶 3I/ATLAS Photometric–Chromatic Anomaly (v2.3)
### Salah-Eddin Gherbi  
Independent Researcher, United Kingdom  
ORCID: [0009-0005-4017-1095](https://orcid.org/0009-0005-4017-1095)  
GitHub Repository: [salah-gherbi-3I_ATLAS_Anomaly_2025](https://github.com/salahealer9/salah-gherbi-3I_ATLAS_Anomaly_2025)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17538229.svg)](https://doi.org/10.5281/zenodo.17538229)

---

## 🔖 DOI & Citation
**Zenodo Record:**  
> *3I/ATLAS Photometric–Chromatic Anomaly (2025): Spectral Transition and Post-Perihelion Evolution (v2.3)*

**Cite this dataset:**
```bibtex
@dataset{gherbi_2025_3I_ATLAS_v23,
  author    = {Salah-Eddin Gherbi},
  title     = {3I/ATLAS Photometric–Chromatic Anomaly (2025): Spectral Transition and Post-Perihelion Evolution},
  year      = {2025},
  publisher = {Zenodo},
  version   = {2.3},
  doi       = {10.5281/zenodo.17538229},
  url       = {https://doi.org/10.5281/zenodo.17538229}
}
```
---

# 📦 Contents of the Proof Bundle

| Category | Files | Description |
|----------|-------|-------------|
| **Manifests** | `I3_ATLAS_Proof_20251105_XXXX.txt`, `.asc`, `.ots` | Hash verification & blockchain proofs |
| **Core Scripts** | `watch_mpc_colors_plot_v8_4.py`, `atlas_optical_acceleration_v2.py`, `atlas_optical_color_correlation_v1.py`, `update_I3_data.sh`, `append_run_log_v3.sh` | Verified analysis pipeline |
| **Data Files** | `I3.txt`, `I3_Color_Alerts_*.csv`, `I3_Optical_Acceleration_Data.csv`, `I3_Color_Statistics_*.txt`, `RUN_LOG.md` | Raw & processed MPC data |
| **Figures** | `I3_Optical_Acceleration_Trend_v2.png`, `I3_Optical_Color_Correlation.png` | Key results visualization |
| **Paper** | `3I_ATLAS_Anomaly_2025.tex`, `metadata.json` | Final manuscript & structured metadata |

---

## 🧩 Version Summary

**Version 2.3** (this release):

- Integrates new MPC data through 2025-11-04, extending analysis beyond perihelion
- Adds new paper section: "Post-Perihelion Update (November 2025)"
- Includes refined Spectral Transition and Colour Evolution analysis with monthly breakdown
- Fixes pipeline execution flow (`append_run_log_v3.sh`)
- Updates parsing logic for new MPC observation formats (e.g., KB, KC, WEV036 codes)
- Regenerated all manifests and OpenTimestamp proofs for full reproducibility

### Previous versions:

- **v2.2** — Integrated full chromatic correlation + manuscript finalization
- **v2.1** — ZTF DR19 cross-validation, MPC-only confirmation
- **v2.0** — JPL Horizons alignment and first blockchain timestamp integration
- **v1.0** — Raw MPC photometry analysis and brightening detection

---

## 🌈 Spectral Transition Summary

| Month (2025) | Mean (g–o) | Relative to Solar (0.62) | Interpretation |
|--------------|------------|--------------------------|----------------|
| July | 0.61 | ≈ 0 | Neutral / reflective (ice-dominated) |
| August | 0.94 | +0.32 | Reddening onset — dust activation |
| September | 1.34 | +0.72 | Peak reddening — maximum outgassing |
| October–November | — | — | Expected bluish relaxation (coma dispersal) |

**Interpretation:**  
3I/ATLAS evolved from **neutral → red → fading**, tracing a full spectral activity cycle.  
The reddening coincided with the optical acceleration spike (2025-09-10), and the subsequent decline (2025-11-03) suggests post-perihelion relaxation.  
This spectral sequence serves as a unique fingerprint of dust-rich interstellar material responding to solar irradiation.

---

# 🔐 Verification Instructions

## 1. Verify hash integrity
```bash
sha256sum -c I3_ATLAS_Proof_20251105_XXXX.txt
```

## 2. Verify digital signature
```bash
gpg --verify I3_ATLAS_Proof_20251105_XXXX.txt.asc I3_ATLAS_Proof_20251105_XXXX.txt
```

It should show:
```bash
Good signature from "Salah-Eddin Gherbi (Discovery Harmonic Quantization…)"
```

## 3. Verify blockchain timestamp
```bash
ots verify I3_ATLAS_Proof_20251105_XXXX.txt.ots
Successful verification anchors this proof to a confirmed Bitcoin block.
```

## 4. Reproduce analysis
```bash
python atlas_optical_acceleration_v2.py
python atlas_optical_color_correlation_v1.py
```

---

# 📜 Summary Statement

This archive represents the complete, timestamp-verified record of the 3I/ATLAS (C/2025 N1) photometric-chromatic analysis through November 2025, including the transition from pre-perihelion brightening to post-perihelion fading.  
It provides the first evidence that an interstellar object exhibits a full spectral evolution cycle — **neutral → red → fading** — under solar heating.

All results are secured by cryptographic proofs (SHA-256 + OpenTimestamps + GPG) ensuring independent auditability.

## 🕰️ Historical Integrity Chain

| Date (UTC) | Version | Manifest | ZIP Bundle | Notes |
|------------|---------|----------|-------------|-------|
| 2025-10-31 | v2.1 | `I3_ATLAS_Proof_20251031_1848.txt` | `proof_bundle/I3_ATLAS_ProofBundle_20251031_1848.zip` | ZTF cross-validation |
| 2025-11-01 | v2.2 | `I3_ATLAS_Proof_20251101_2112.txt` | `proof_bundle/I3_ATLAS_ProofBundle_20251101_2112.zip` | Full dataset + paper |
| 2025-11-05 | v2.3 | `I3_ATLAS_Proof_20251105_XXXX.txt` | `proof_bundle/I3_ATLAS_ProofBundle_20251105_XXXX.zip` | Post-perihelion update + spectral transition |

---

## 🧠 Notes for Reproducibility

- All observations derive exclusively from **public MPC photometry** (`I3.txt`)
- Scripts use only **open-source Python libraries**: pandas, numpy, matplotlib
- **No proprietary calibration** or external survey data applied
- Every analysis stage is **cryptographically verifiable** and fully timestamped

---

## 📊 Key Findings

- **Optical acceleration spike**: 2025-09-10 ± 2 days
- **Maximum reddening**: Δ(g–o) ≈ +0.7 mag
- **Acceleration reversal**: 2025-11-03 → coma fading
- **Expected bluish relaxation**: indicative of post-activity dispersal
- **First complete photometric-chromatic cycle** detected for an interstellar object

*Prepared automatically via `protect_atlas_v2_3.sh` on 2025-11-05 UTC.*  
**Author**: Salah-Eddin Gherbi — Independent Researcher, United Kingdom
