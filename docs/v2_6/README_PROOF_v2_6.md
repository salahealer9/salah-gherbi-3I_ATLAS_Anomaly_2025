# 📄 README_PROOF_v2_6 — Release Notes & Verification
## 🌌 Version 2.6 — Automated Peak Detection, Corrected Δv Timing & Updated IAI

## 📌 DOI
10.5281/zenodo.17793630 
Concept DOI: 10.5281/zenodo.17477597

Version 2.6 refines the Δv-based dynamical interpretation of **3I/ATLAS (C/2025 N1)** by correcting the timing of the first major acceleration spike and introducing *automated peak detection* across all optical–acceleration and Δv plots. All Δv figures and geometric interpretations are now fully data-driven and remain internally consistent as MPC photometry updates.

This release also incorporates new Gemini/GMOS and VLT/UVES spectroscopy, including weak CN–C₂–C₃ detections and a statistically significant **Ni/Fe enrichment**, now encoded in the fifth Interstellar Anomaly Index component **Aₓ**.

---

## ✅ Key Scientific Updates in v2.6

### **1. Corrected Pre-Perihelion Peak Timing**
Reprocessing the MPC dataset (2025-05-08 → 2025-11-21) shifts the earliest acceleration maximum:

**2025-09-10 → 2025-09-09 (day −50)**

This correction improves:
- Δv integrations  
- Jupiter-encounter geometry analyses  
- Anomaly sequencing  

---

### **2. Fully Automated Peak Detection**
New pipeline features:
- No hand-coded peak dates  
- Peaks identified directly from smoothed acceleration curves  
- Automatic vertical annotations in Δv and acceleration plots  
- Reproducible for future photometric updates  

---

### **3. Updated Python Scripts**
Three scripts now auto-detect the latest colour file and incorporate noise-window analysis:

- `atlas_optical_acceleration_v2.py`  
- `atlas_optical_color_correlation_v1.py`  
- `plot_station_residuals.py` (new multi-window noise validation)

---

### **4. Updated Figures**
Regenerated using corrected peaks and extended dataset:

- `I3_Optical_Acceleration_DeltaV_Figure.png`  
- `I3_Optical_Acceleration_DeltaV_Overlay.png`  
- `I3_Optical_Acceleration_Trend_v2.png`  
- `I3_Optical_Acceleration_DeltaV_8_vs_25.png`  
- `I3_Optical_Color_Correlation_postperi.png`  
- `station_collective_effect_corrected.png`

---

### **5. New Figure: Post-Perihelion g-Band Fading**
Added:

- `I3_Color_Brightness_Timeline_20251202_1102.png`

This figure illustrates the strong monotonic fading after perihelion and supports the negative optical-acceleration interpretation.

---

### **6. Expanded Interstellar Anomaly Index (IAI)**
A fifth anomaly component is added:

- **Aₓ — compositional anomaly**  
  - Encodes Ni/Fe enrichment and unusual gas-phase nickel behaviour  
  - Updated index: **IAI ≈ 0.94**

---

### **7. Manuscript Updates**
v2.6 modifies the LaTeX source:

- Updated Section 4.3 and anomaly components table  
- Added Ni/Fe paragraph in Discussion  
- Updated all Δv figures and captions  
- Corrected peak dates in text and figures  
- Added post-perihelion g-band fading subsection  
- Added station-consistency appendix and summary table  

---

## **8. Station-Consistency Validation of Late-November Features**

The expanded MPC dataset (now **4,699–4,960 observations** depending on cutoff) revealed two small post-perihelion fluctuations:

1. **Nov 22–25 window**  
2. **Nov 28–Dec 01 window**

A new time-normalised station-level analysis confirms that *neither feature* exhibits the coherent multi-station signature expected for physical activity.

### **Window 1 — Nov 22–25**
- Uses 11 independent stations  
- All values remain **within ±3σ** of pre-11/22 baseline  
- Mixed positive and negative signs  
- Max station significance: **0.6σ**  
- Daily mean uplift (~26.6×10⁻³) arises from many *uncorrelated small offsets*, not a real event  

### **Window 2 — Nov 28–Dec 01**
- Dataset extended to **2025-12-01**  
- Apparent peak entirely dominated by station **703**  
- Daily mean: **+0.4×10⁻³**, near zero  
- Not multi-station  
- Fully consistent with random noise  

### **Conclusion**
Both late-November features are statistically consistent with **photometric noise**, not physical acceleration.  
They remain **excluded** from:
- Δv integration  
- Peak-detection framework  
- Anomaly classification (IAI)  

Support:  
- `station_collective_effect_corrected.png`  
- `plot_station_residuals.py`

---

## 🆕 Files Added or Modified in v2.6

### **Updated Analysis Scripts**
- `plot_atlas_optical_accel_deltav.py` (auto-detects peaks)  
- `atlas_delta_v_from_optical_proxy.py`  
- `atlas_optical_dv_dual.py`  

### **Additional Scripts**
- `atlas_anomaly_components.py`  
- `plot_station_residuals.py`  

### **Updated Figures**
- `I3_Optical_Acceleration_DeltaV_Figure.png`  

### **New Figures**
- `atlas_anomaly_components.png`  
- `station_collective_effect_corrected.png`  
- `I3_Color_Brightness_Timeline_20251202_1200.png`

### **Documentation**
- `3I_ATLAS_Anomaly_2025.tex` (all v2.6 revisions)  
- `README_PROOF_v2_6.md`  
- `manifest_v2_6.txt`

---

## 🔐 Reproducibility, Integrity & Audit Trail

All v2.6 materials are cryptographically sealed using:

- **SHA-256 checksums**  
- **GPG detached signatures (.asc)**  
- **OpenTimestamps Bitcoin proofs (.ots)**  

Verification:

```bash
sha256sum -c manifest_v2_6.txt
gpg --verify manifest_v2_6.txt.asc
ots verify manifest_v2_6.txt.ots
```

Every run is logged in:
- `RUN_LOG.md`

Proof bundle stored as:
- `I3_ATLAS_ProofBundle_YYYYMMDD_HHMM.zip`

# 📁 Included in v2.6 Release Package

## Data
*   **`I3.txt`** — MPC photometry
*   **`I3_Optical_Acceleration_Data.csv`**
*   **`I3_Color_Statistics_*.txt`**

## Figures
*   Updated Δv figures
*   IAI component diagram
*   Eccentricity–IAI comparison

## Code
*   All Δv, IAI, colour, and acceleration pipelines
*   Peak-detection utilities
*   Station-consistency analysis

## Proof
*   `manifest_v2_6.txt`
*   `manifest_v2_6.sha256`
*   `manifest_v2_6.asc`
*   `manifest_v2_6.ots`

## ✔️ Version Notes
**v2.6 supersedes v2.5 and should be cited for:**
*   corrected acceleration peak timing
*   Δv-based dynamical interpretation
*   automated peak-detection framework
*   Ni/Fe compositional anomaly integration
*   updated Interstellar Anomaly Index
*   new station-consistency validation

This release continues the project’s commitment to open, timestamp-verified, reproducible research, with all data, code, and proofs publicly archived.





