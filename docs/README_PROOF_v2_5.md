# 3I/ATLAS – Photometric–Chromatic Anomaly (2025)
## Version 2.5 – Release Notes (2025-11)

### 📌 DOI
**10.5281/zenodo.17692904**  
**Concept DOI: 10.5281/zenodo.17477597**

Version 2.5 delivers the most complete, reproducible, and multi-axis analysis of 3I/ATLAS (C/2025 N1) to date, integrating extended MPC photometry, refined post-perihelion behaviour, Δv-based dynamical analysis, and the first Interstellar Anomaly Index (IAI) quantifying multidimensional departures from cometary expectations.

This release finalises the preprint analysis chain and seals the entire dataset through SHA256 manifests, GPG signatures, and OpenTimestamps blockchain proofs.

---

# 🔄 Summary of Changes in v2.5

## 1. New Scientific Additions

### **Interstellar Anomaly Index (IAI)**
- A 4-component anomaly metric (Aₚ, A꜀, Aₐ, Aₘ) placing 3I/ATLAS at **IAI ≈ 0.95**, extreme among all known interstellar objects  
- Plots & code:
  - `atlas_anomaly_index.py` → `atlas_anomaly_components.png`
  - `iai_vs_eccentricity.py` → `iai_vs_eccentricity.png`

### **Δv-Based Dynamical Analysis (New in v2.5)**
- Conversion of optical–acceleration proxy into physical non–gravitational Δv(t)
- Two calibrated regimes:
  - **Minimal:** 8 m/s (Loeb Jupiter “fine-tune” threshold)
  - **Photometric:** 25 m/s (A₁-consistent, data-driven)
- New diagnostic figures:
  - `I3_Optical_Acceleration_DeltaV_Figure.png`
  - `I3_Optical_Acceleration_DeltaV_8_vs_25.png`
  - `I3_Optical_Acceleration_DeltaV_Overlay.png`
- New analysis scripts:
  - `atlas_delta_v_from_optical_proxy.py`
  - `atlas_optical_dv_dual.py`
  - `plot_atlas_optical_accel_deltav.py`

## 2. Extended Post-Perihelion Evolution

- MPC photometry extended to **2025-11-21** (4,580 observations)
- Smooth monotonic fading with stable negative optical acceleration
- No post-perihelion reactivation detected  
- Updated figures:
  - `I3_Optical_Color_Correlation_postperi.png`
  - `I3_Optical_Acceleration_Trend_v2.png`

## 3. Updated Research Paper

- Revised LaTeX manuscript: `3I_ATLAS_Anomaly_2025.tex`
- New and expanded sections:
  - Interstellar Anomaly Index
  - Δv scaling analysis and geometric implications
  - Extended colour–acceleration interpretation
  - Artificiality decision flowchart
- Updated figures & tables across the manuscript

## 4. Hardened Reproducibility Pipeline

- Updated “seal & protect” script: `protect_atlas_v2_5.sh`
- Full pipeline continuity preserved:
  - `update_I3_data.sh`
  - `append_run_log_v3.sh`
- All outputs cryptographically sealed through:
  - SHA256 manifest
  - GPG signature
  - OpenTimestamps anchoring

---

# 📁 Included Materials (v2.5 Release)

## **Raw & Processed Data**
- `I3.txt` — Raw MPC photometry  
- `I3_Color_Alerts_*.csv` — Filtered colour anomalies  
- `I3_Optical_Acceleration_Data.csv` — Optical acceleration proxy time series  
- `I3_Color_Statistics_*.txt` — Solar-baseline colour deltas  

## **Figures**
- Photometric & chromatic:
  - `I3_Optical_Acceleration_Trend_v2.png`
  - `I3_Optical_Color_Correlation.png`
  - `I3_Optical_Color_Correlation_postperi.png`
- IAI:
  - `atlas_anomaly_components.png`
  - `iai_vs_eccentricity.png`
- **Δv Analysis (new in v2.5):**
  - `I3_Optical_Acceleration_DeltaV_Figure.png`
  - `I3_Optical_Acceleration_DeltaV_8_vs_25.png`
  - `I3_Optical_Acceleration_DeltaV_Overlay.png`

## **Analysis Scripts**
- Photometry & colour pipeline:
  - `watch_mpc_colors_plot_v8_4.py`
  - `atlas_optical_acceleration_v2.py`
  - `atlas_optical_color_correlation_v1.py`
- IAI system:
  - `atlas_anomaly_index.py`
  - `iai_vs_eccentricity.py`
- **Δv system (new in v2.5):**
  - `atlas_delta_v_from_optical_proxy.py`
  - `atlas_optical_dv_dual.py`
  - `plot_atlas_optical_accel_deltav.py`

## **Pipeline Tools**
- `update_I3_data.sh`
- `append_run_log_v3.sh`

## **Manuscript & Documentation**
- `3I_ATLAS_Anomaly_2025.tex`
- `I3_ATLAS_v2_5_Analysis.pdf`
- `RUN_LOG.md`
- `README_PROOF_v2_5.md` (this file)

## **Proof Bundle**
- `I3_ATLAS_ProofBundle_YYYYMMDD_HHMM.zip`, containing:
  - `I3_ATLAS_Proof_*.txt` — SHA-256 manifest  
  - `I3_ATLAS_Proof_*.txt.asc` — GPG signature  
  - `I3_ATLAS_Proof_*.txt.ots` — OpenTimestamps proof  
  - All core scripts, figures, data files, LaTeX, and logs included in v2.5  

---

# 🔒 Reproducibility & Verification

All files in Version 2.5 are verifiably timestamped using:

- SHA-256 cryptographic hashes  
- GPG detached signatures  
- OpenTimestamps (anchored in Bitcoin blockchain)

### **Verification Commands**
```bash
sha256sum -c I3_ATLAS_Proof_*.txt
gpg --verify I3_ATLAS_Proof_*.txt.asc
ots verify I3_ATLAS_Proof_*.txt.ots
```

Each execution of the protection workflow (protect_atlas_v2_5.sh) appends a full audit entry to RUN_LOG.md, ensuring forensic-grade temporal integrity.

✔️ Version Notes

Version 2.5 supersedes v2.4 and establishes the most complete, timestamp-verified analysis of 3I/ATLAS currently available. It introduces a unified anomaly metric (IAI), incorporates all post-perihelion photometry, adds Δv-based dynamical interpretation, and seals the full reproducible pipeline under cryptographic verification.