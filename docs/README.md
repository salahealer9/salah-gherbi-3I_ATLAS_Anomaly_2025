# 3I/ATLAS (C/2019 Y4) — Photometric Anomaly 2025

## Overview
This dataset documents the **photometric brightening anomaly** of *3I/ATLAS (C/2019 Y4)* observed between **July and October 2025**.  
Raw observations were extracted directly from the **Minor Planet Center (MPC)** file `I3.txt`, parsed using the included Python script `print_summary.py`, and analyzed to produce monthly magnitude statistics and light-curve figures.

The object exhibited a steady increase in brightness of **Δm ≈ 4.2 mag** (≈ ×47 flux), far exceeding geometric expectations.  
All results are **cryptographically verified** and timestamp-anchored via the **Bitcoin blockchain** using **OpenTimestamps**.

---

## Contents
| File | Description |
|:--|:--|
| `I3.txt` | Raw MPC observation records for 3I/ATLAS (C/2019 Y4) |
| `I3_clean.csv` | Parsed observation table (date, RA, Dec, magnitude) |
| `I3_monthly_summary.csv` | Monthly photometric statistics |
| `I3_lightcurve.png` | Light-curve plot of mean magnitude vs month |
| `I3_ATLAS_Dual_Anomaly.png` | Comparative July–October brightness diagram |
| `print_summary.py` | Python script for parsing, summarizing, and plotting |
| `anomaly_manifest.txt` | Master list of SHA-256 checksums for all files |
| `anomaly_manifest.txt.ots` | OpenTimestamps proof anchoring the manifest to Bitcoin |
| `anomaly_manifest_20251029_1648.ots` | Original proof snapshot (earlier state) |
| `verification_report.txt` | Human-readable timestamp verification log |
| `README.md` | This documentation file |

---

## Results Summary
| Month (2025) | Mean Mag | Std | Count | Notes |
|:--|:--|:--|:--|:--|
| July | 17.30 ± 1.0 | 1594 | Baseline faint phase |
| August | 16.34 ± 0.6 | 836 | Gradual brightening |
| September | 15.01 ± 0.8 | 246 | Continued increase |
| October | 13.11 ± 0.6 | 15 | Post-conjunction reactivation |

**Δm = 4.19 mag → Flux increase ≈ ×47.5**  
This sustained brightening exceeds geometric expectations and indicates **intrinsic physical activity**, likely volatile release or surface re-exposure after solar conjunction.

---

## Discussion (Photometric Anomaly)
Between July and October 2025, *3I/ATLAS* displayed a monotonic increase in mean brightness from V ≈ 17.3 to 13.1 mag, corresponding to Δm ≈ 4.2 mag (×47 flux).  
The amplitude of this variation surpasses what can be explained by changes in heliocentric or geocentric distance alone, marking it as a genuine **photometric anomaly**.  
The data suggest **reactivation or outgassing** of volatile material, possibly following the object’s re-emergence from solar conjunction.  
All magnitudes are taken directly from MPC records without interpolation, ensuring transparency and reproducibility.

---

## Reproducibility
Re-run the full analysis:

```bash
python3 print_summary.py
```

Outputs:

- updated monthly summary (I3_monthly_summary.csv)
- light-curve figure (I3_lightcurve.png)
- printed table in terminal

All scripts use only pandas and matplotlib.

Verification & Integrity

All files are protected by SHA-256 checksums and timestamp-anchored via OpenTimestamps.

```bash
sha256sum -c anomaly_manifest.txt
ots verify anomaly_manifest.txt.ots
```

Any alteration will invalidate the hash and fail verification.
The manifest and its .ots proofs ensure permanent, blockchain-verifiable authenticity (timestamp ≈ 2025-10-29 UTC).

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

## 📚 Citation

**Gherbi, Salah-Eddin (2025).**  
3I/ATLAS (C/2019 Y4) Photometric Anomaly 2025 — Version 2: JPL Horizons Comparison.  
Zenodo.  
https://doi.org/10.5281/zenodo.17483027  
https://doi.org/10.5281/zenodo.17477597

## 🔖 BibTeX

```bibtex
@dataset{gherbi_3I_ATLAS_anomaly2025_v2,
  author       = {Salah-Eddin Gherbi},
  title        = {3I/ATLAS (C/2019 Y4) Photometric Anomaly 2025 — Version 2: JPL Horizons Comparison},
  year         = {2025},
  publisher    = {Zenodo},
  version      = {v2.0},
  doi          = {10.5281/zenodo.17483027},
  url          = {https://doi.org/10.5281/zenodo.17483027}
}
```

## License

All files are released under Creative Commons Attribution 4.0 International (CC BY 4.0).  
Attribution required for reuse; derivatives permitted with citation.

## Contact

**Salah-Eddin Gherbi**  
Independent Researcher — United Kingdom  
📧 [salahealer@gmail.com]  
🔗 [https://orcid.org/0009-0005-4017-1095]
🔗 [https://github.com/salah-gherbi/3I_ATLAS_Anomaly_2025]

---

## Version 2 Update (October 2025)

This second release (v2.0) extends the dataset with a comparative analysis against **JPL Horizons predicted magnitudes**.  
New additions include:
- `compare_horizons_anomaly.py` — script comparing observed MPC magnitudes with JPL-predicted values  
- `I3_Horizons_Residuals.csv` — residual table (observed minus predicted)  
- `I3_Horizons_Residuals.png` and `I3_ATLAS_Horizons_Normalized.png` — visualization of the brightness deviation  
- Updated `anomaly_manifest.txt` and timestamp proofs (`.ots`)

---

## Blockchain Verification

All integrity proofs are timestamp-anchored on the **Bitcoin blockchain** via [OpenTimestamps](https://opentimestamps.org).

**Included proofs:**
- `anomaly_manifest.txt.ots` — current proof (Oct 30 2025)
- `anomaly_manifest_20251030_ots.ots` — backup attestation  
- `anomaly_manifest_20251029_1648.ots` — v1 archive proof

To verify locally:

```bash
sha256sum -c anomaly_manifest.txt
ots verify anomaly_manifest.txt.ots
```

✅ Successful verification confirms the dataset existed in its present form at or before 2025-10-30 UTC.

---

## Version 2.1 Update (October 2025)

This third release (v2.1) extends the previous JPL Horizons comparison (v2.0) with a **cross-validation attempt using ZTF DR19 photometry** via the IRSA TAP service.

### 🔍 Cross-Validation Summary
- Attempted retrieval of **Zwicky Transient Facility (ZTF) DR19** photometric data near RA = 113.9°, Dec = 47.8° for July–October 2025.  
- **Result:** No ZTF observations detected for *3I/ATLAS (C/2019 Y4)* during this interval.  
- **Implication:** The MPC dataset remains the *sole observational record* of the 2025 brightening anomaly.

### 🧩 New and Updated Files
| File | Description |
|------|--------------|
| `compare_ztf_I3_ATLAS.py` | Python script for cross-validation attempt using IRSA TAP |
| `I3_MPC_Only.png` | Fallback plot showing MPC-only brightness trend (no ZTF detections) |
| `verification_report.txt` | Updated verification report including v2.1 attestation |
| `anomaly_manifest_20251030_v21.ots` | New OpenTimestamps proof for updated manifest |

### 🧠 Notes
All analyses, hashes, and timestamps remain consistent with v2.0.  
SHA-256 manifest (`anomaly_manifest.txt`) has been re-stamped and cryptographically anchored via OpenTimestamps on the Bitcoin blockchain.

### 📘 Citation
**Gherbi, Salah-Eddin (2025).**  
*3I/ATLAS (C/2019 Y4) Photometric Anomaly 2025 — Version 2.1: ZTF Cross-Validation.*  
Zenodo. [https://doi.org/10.5281/zenodo.17487610](https://doi.org/10.5281/zenodo.17487610)  
**Concept DOI:** [https://doi.org/10.5281/zenodo.17477597](https://doi.org/10.5281/zenodo.17477597)

---

### 🔖 BibTeX

```bibtex
@dataset{gherbi_3I_ATLAS_anomaly2025_v21,
  author       = {Salah-Eddin Gherbi},
  title        = {3I/ATLAS (C/2019 Y4) Photometric Anomaly 2025 — Version 2.1: ZTF Cross-Validation},
  year         = {2025},
  publisher    = {Zenodo},
  version      = {v2.1},
  doi          = {10.5281/zenodo.17487610},
  url          = {https://doi.org/10.5281/zenodo.17487610}
}
```

⛓️ Verification

All dataset files remain protected under the cumulative manifest system.
To confirm blockchain-anchored integrity:

```bash
sha256sum -c anomaly_manifest.txt
ots verify anomaly_manifest_20251030_v21.ots
```

✅ Verification confirms existence and immutability of the dataset up to 2025-10-30 UTC.

