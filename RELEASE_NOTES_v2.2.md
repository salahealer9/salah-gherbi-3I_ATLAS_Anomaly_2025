# 🚀 3I/ATLAS (C/2025 N1) — Photometric–Chromatic Anomaly (v2.2)

**DOI:** [10.5281/zenodo.17503806](https://doi.org/10.5281/zenodo.17503806)  
**Concept DOI:** [10.5281/zenodo.17477597](https://doi.org/10.5281/zenodo.17477597)

---

## 🔭 Overview

Version **2.2** marks the most comprehensive update of the *3I/ATLAS (C/2025 N1)* investigation, introducing an integrated analysis of **optical acceleration** and **chromatic evolution** derived from Minor Planet Center (MPC) photometry (4,280 observations; May–October 2025).  

A pre-perihelion acceleration event was detected around **2025-09-10**, approximately **50 days before perihelion**, accompanied by a **reddening of Δ(g–o) ≈ +0.57 mag**.  
This temporal coincidence suggests a physical transition in 3I/ATLAS’s activity — possibly outgassing, dust emission, or compositional change — though the underlying mechanism remains open for investigation.

---

## 🧩 New in v2.2

- **New optical acceleration pipeline:** `atlas_optical_acceleration_v2.py`  
  → extracts brightness-rate derivatives and identifies the pre-perihelion acceleration spike.

- **Joint color–acceleration correlation:** `atlas_optical_color_correlation_v1.py`  
  → overlays color reddening (g–o) and acceleration window; exported composite figure.

- **Updated color pipeline:** `watch_mpc_colors_plot_v8_4.py`  
  → improved solar reference comparison and per-filter diagnostics.

- **Automated update system:** `update_I3_data.sh`  
  → one-command MPC retrieval, backup, OpenTimestamps sealing, and GPG signing.

- **Full cryptographic proof bundle:** `I3_ATLAS_ProofBundle_20251101_2112.zip`  
  → includes .asc (GPG) and .ots (Bitcoin) attestations for every analysis file.

- **LaTeX manuscript:** `3I_ATLAS_Anomaly_2025.pdf`  
  → complete versioned preprint with all figures and references.

---

## 📊 Key Findings

| Parameter | Value | Interpretation |
|------------|--------|----------------|
| Optical acceleration peak | 2025-09-10 | Pre-perihelion surge (~ 50 days early) |
| Scaled amplitude | −2.7 × 10⁻³ (relative units) | Consistent with non-gravitational activity |
| Δ(g–o) color shift | +0.57 mag | Reddening during acceleration window |
| Brightening amplitude | Δm ≈ 4.2 mag (~ × 47 flux) | Over ~90 days, exceeding geometric expectation |

Together, these results identify the first photometric–chromatic signature of non-gravitational acceleration in 3I/ATLAS — detected directly from ground-based MPC photometry before orbital modeling.

---

## 🛡️ Verification

All datasets and figures are cryptographically protected and timestamp-anchored via **OpenTimestamps (Bitcoin mainnet)** and signed with **GPG** for author authenticity.

**Proof verification example:**
```bash
sha256sum -c I3_Color_Proof_20251031_1848.txt
ots verify I3_Color_Proof_20251031_1848.txt.ots
gpg --verify I3_Color_Proof_20251031_1848.txt.asc
```
Successful verification confirms dataset integrity as of 2025-11-01 UTC.

## 🧠 Citation

**Gherbi, Salah-Eddin (2025).**  
3I/ATLAS (C/2019 Y4) — Photometric Anomaly 2025 (v2.1: ZTF Cross-Validation).  
Zenodo. [https://doi.org/10.5281/zenodo.17503806](https://doi.org/10.5281/zenodo.17503806)

## 📘 BibTeX

```bibtex
@dataset{gherbi_3I_ATLAS_anomaly2025_v22,
  author       = {Salah-Eddin Gherbi},
  title        = {3I/ATLAS (C/2025 N1) — Photometric–Chromatic Anomaly: Optical Acceleration Analysis and Timestamped Dataset},
  year         = {2025},
  publisher    = {Zenodo},
  version      = {v2.2},
  doi          = {10.5281/zenodo.17503806},
  url          = {https://doi.org/10.5281/zenodo.17503806}
}
```

## 🧾 Version History

| Version | Date | Description |
|---------|------|-------------|
| v1.0 | Oct 2025 | Initial MPC photometric analysis |
| v2.0 | Oct 30 2025 | Added JPL Horizons comparison |
| v2.1 | Oct 30 2025 (later) | ZTF cross-validation + proof consolidation |
| v2.2 | Nov 1 2025 | Optical acceleration + color-correlation study + full timestamped archive |

## 🔗 Repository

**GitHub** — [salah-gherbi-3I_ATLAS_Anomaly_2025](https://github.com/salahealer9/salah-gherbi-3I_ATLAS_Anomaly_2025)
