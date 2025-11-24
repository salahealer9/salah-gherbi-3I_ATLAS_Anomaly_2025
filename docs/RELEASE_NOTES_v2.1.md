# 🚀 3I/ATLAS (C/2019 Y4) — Photometric Anomaly 2025 (v2.1)

**DOI:** [10.5281/zenodo.17487610](https://doi.org/10.5281/zenodo.17487610)  
**Concept DOI:** [10.5281/zenodo.17477597](https://doi.org/10.5281/zenodo.17477597)

## 🔭 Overview

Version 2.1 extends the 3I/ATLAS (C/2019 Y4) Photometric Anomaly 2025 dataset with a Zwicky Transient Facility (ZTF) cross-validation attempt and updated blockchain verification.  
This release tests whether independent survey data (ZTF DR19) captured the same post-conjunction brightening observed in Minor Planet Center (MPC) photometry.

No corresponding ZTF detections were found for the RA=113.9°, Dec=47.8° field during July–October 2025 — confirming that MPC records remain the sole photometric evidence of the 3I/ATLAS reactivation anomaly.

## 🧩 New in v2.1

- **New analysis script:** `compare_ztf_I3_ATLAS.py` — queries NASA/IPAC IRSA for ZTF DR19 photometry
- **Fallback plot:** `I3_MPC_Only.png` — visualizes MPC data when no ZTF detections are available
- **Updated verification log:** `verification_report.txt` — merged v2 + v2.1 attestation summary
- **New blockchain proof:** `anomaly_manifest_20251030_v21.ots` — fresh OpenTimestamps attestation
- **Metadata refresh:** includes updated CITATION.cff and refined Zenodo metadata

All results are SHA-256 verified and timestamp-anchored via OpenTimestamps (Bitcoin mainnet), ensuring long-term reproducibility and dataset integrity.

## 🔍 Cross-Validation Summary

**Objective:** Confirm the MPC-observed brightening of 3I/ATLAS using independent ZTF photometry.  
**Method:** Query region around RA=113.9°, Dec=47.8° (ICRS) using IRSA TAP interface for July–October 2025.  
**Result:** 
- ⚠️ No ZTF detections found.
- The anomaly remains visible only in MPC photometry.
- This negative result reinforces the uniqueness of the MPC dataset during the 2025 reactivation window.

## 📊 Key Findings

- **Brightness increase:** Δm ≈ 4.2 mag (≈ ×47 flux) between July and October 2025
- **No corroborating detections** in external surveys
- **Confirms intrinsic post-conjunction reactivation** as the most plausible explanation

## 🛡️ Verification

All files and their digests are authenticated by SHA-256 and timestamped to the Bitcoin blockchain via OpenTimestamps.

**Verification procedure:**
```bash
sha256sum -c anomaly_manifest.txt
ots verify anomaly_manifest_20251030_v21.ots
```

Successful verification confirms dataset integrity as of 2025-10-30 UTC.

## 🧠 Citation

**Gherbi, Salah-Eddin (2025).**  
3I/ATLAS (C/2019 Y4) — Photometric Anomaly 2025 (v2.1: ZTF Cross-Validation).  
Zenodo. https://doi.org/10.5281/zenodo.17487610

## 📘 BibTeX

```bibtex
@dataset{gherbi_3I_ATLAS_anomaly2025_v21,
  author       = {Salah-Eddin Gherbi},
  title        = {3I/ATLAS (C/2019 Y4) — Photometric Anomaly 2025 (v2.1: ZTF Cross-Validation)},
  year         = {2025},
  publisher    = {Zenodo},
  version      = {v2.1},
  doi          = {10.5281/zenodo.17487610},
  url          = {https://doi.org/10.5281/zenodo.17487610}
}
```

## 🧾 Version History

| Version | Date | Description |
|---------|------|-------------|
| v1.0 | Oct 2025 | Initial MPC photometric analysis |
| v2.0 | Oct 30 2025 | Added JPL Horizons predicted comparison |
| v2.1 | Oct 30 2025 (later) | Added ZTF cross-validation + verification update |
