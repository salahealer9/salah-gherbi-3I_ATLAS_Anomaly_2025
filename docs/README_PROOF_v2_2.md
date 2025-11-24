# 🪶 3I/ATLAS Photometric–Chromatic Anomaly (v2.2)
### Salah-Eddin Gherbi  
Independent Researcher, United Kingdom  
ORCID: [0009-0005-4017-1095](https://orcid.org/0009-0005-4017-1095)  
GitHub Repository: [salah-gherbi-3I_ATLAS_Anomaly_2025](https://github.com/salahealer9/salah-gherbi-3I_ATLAS_Anomaly_2025)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17503806.svg)](https://doi.org/10.5281/zenodo.17503806)

---

## 🔖 DOI & Citation
**Zenodo Record:**  
> *3I/ATLAS Photometric–Chromatic Anomaly (2025): Timestamped Dataset and Optical Acceleration Analysis*

**Cite this dataset:**
```bibtex
@dataset{gherbi_2025_3I_ATLAS,
  author = {Gherbi, Salah-Eddin},
  title = {3I/ATLAS Photometric–Chromatic Anomaly (2025): Timestamped Dataset and Optical Acceleration Analysis},
  year = {2025},
  publisher = {Zenodo},
  version = {2.2},
  doi = {10.5281/zenodo.17503806},
  url = {https://doi.org/10.5281/zenodo.17503806}
}
```

# 📦 Contents of the Proof Bundle

| Category | Files | Description |
|----------|-------|-------------|
| **Manifests** | `I3_ATLAS_Proof_*.txt`, `.asc`, `.ots`, `manifest_v2_2.txt` | Verification manifests and blockchain proofs |
| **Core Scripts** | `watch_mpc_colors_plot_v8_4.py`, `atlas_optical_acceleration_v2.py`, `atlas_optical_color_correlation_v1.py`, `update_I3_data.sh`, `append_run_log_v3.sh` | Reproducible analysis pipeline |
| **Automation** | `check_mpc_update.sh`, `cleanup_old_runs.sh`, `weekly_status.sh` | Automated MPC watcher, cleanup, and reporting |
| **Data Files** | `I3.txt`, `I3_Color_Alerts_*.csv`, `I3_Optical_Acceleration_Data.csv`, `I3_Color_Statistics_*.txt`, `RUN_LOG.md` | Raw and derived data |
| **Figures** | `I3_Optical_Acceleration_Trend_v2.png`, `I3_Optical_Color_Correlation.png`, `I3_Optical_Color_Correlation_postperi.png` | Optical and chromatic diagnostics |
| **Documentation** | `README_PROOF_v2_2.md`, `CITATION.cff`, `3I_ATLAS_Anomaly_2025.tex` | Documentation, citation, and manuscript |

## 🧩 Version Summary

**Version 2.2** — Post-Perihelion Update (Nov 2025)

- Integrates chromatic correlation between optical acceleration and colour indices
- Adds post-perihelion dataset (Oct 31 → Nov 04) parsed from MPC revisions  
- Includes enhanced ZIP proof bundle (with manifest + metadata)
- Extends reproducibility pipeline with autonomous MPC watcher + email alerts
- All materials timestamped and signed via OpenTimestamps + GPG

### Previous versions

| Version | Date | Key features |
|---------|------|--------------|
| v2.1 | Oct 2025 | ZTF DR19 cross-validation + blockchain proof refresh |
| v2.0 | Oct 2025 | JPL Horizons comparison + first OpenTimestamp integration |
| v1.0 | Oct 2025 | Initial MPC photometric anomaly detection |

---

## 🔐 Verification Instructions

### 1. Verify hash integrity
```bash
sha256sum -c I3_ATLAS_Proof_YYYYMMDD_HHMM.txt
```

All listed files should return OK.


### 2. Verify digital signature
```bash
gpg --verify I3_ATLAS_Proof_YYYYMMDD_HHMM.txt.asc I3_ATLAS_Proof_YYYYMMDD_HHMM.txt
```

Should display: Good signature from "Salah-Eddin Gherbi (Discovery Harmonic Quantization...)"

### 3. Verify blockchain timestamp
```bash
ots verify I3_ATLAS_Proof_YYYYMMDD_HHMM.txt.ots
```

A successful verification anchors the proof to a confirmed Bitcoin block.

### 4. Reproduce analysis
```bash
python atlas_optical_acceleration_v2.py
python atlas_optical_color_correlation_v1.py
```

---

# 📜 Summary Statement

This bundle represents the cryptographically authenticated and fully reproducible record of the 3I/ATLAS (C/2025 N1) photometric–chromatic anomaly.  
It documents:

- **Optical acceleration spike** detected ≈ 2025-09-10 (±2 days)
- **Concurrent g–o reddening** Δ ≈ +0.57 mag during that interval
- **50-day early detection** before JPL's non-gravitational term (A₁ ≈ 1.6 × 10⁻⁶ au d⁻²)
- **Full OpenTimestamp + GPG verification chain** ensuring temporal authenticity
- All scripts and data are publicly archived under **CC BY-NC 4.0** and independently verifiable

## 🕰️ Historical Integrity Chain

| Date (UTC) | Version | Manifest | Proof Bundle | Notes |
|------------|---------|----------|--------------|-------|
| 2025-10-31 | v2.1 | `I3_ATLAS_Proof_20251031_1848.txt` | `I3_ATLAS_ProofBundle_20251031_1848.zip` | ZTF cross-validation |
| 2025-11-01 → 04 | v2.2 | `I3_ATLAS_Proof_20251101_2112.txt` etc. | `I3_ATLAS_ProofBundle_20251101_2112.zip` | Full dataset + post-perihelion update |

## 🧠 Notes for Reproducibility

- **Source**: Minor Planet Center (MPC) photometry only (`I3.txt`)
- **Environment**: Python 3 + pandas, numpy, matplotlib
- **No external calibration** or proprietary inputs
- **All scripts timestamp-verified** on execution (`RUN_LOG.md`)
- **New data detection automated** via cron-triggered watcher (`check_mpc_update.sh`)

## 📊 Key Findings

- **Persistent photometric–chromatic coupling** in 3I/ATLAS
- **Strong pre-perihelion acceleration + reddening event** (Δ ≈ +0.57 mag)
- **No ZTF detections** → MPC photometry remains primary evidence
- **Post-perihelion continuation** of the brightening trend under monitoring

*Prepared automatically via `protect_atlas_v2_2.sh` on 2025-11-01 and updated 2025-11-04.*  
**Author**: Salah-Eddin Gherbi — Independent Researcher, United Kingdom