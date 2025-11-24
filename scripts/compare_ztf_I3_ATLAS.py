#!/usr/bin/env python3
"""
compare_ztf_I3_ATLAS.py
Cross-validation of MPC vs ZTF photometry for C/2019 Y4 (3I/ATLAS)
Uses IRSA TAP interface (astroquery ≥ 0.4.10) — no IrsaTap import needed.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy import units as u
from astroquery.ipac.irsa import Irsa
import warnings
warnings.filterwarnings("ignore")

# --- Parameters ---
target_name = "C/2019 Y4 (ATLAS)"
start_date = "2025-07-01"
end_date   = "2025-10-30"
coord_comet = SkyCoord(ra=113.9*u.deg, dec=47.8*u.deg, frame="icrs")

print(f"\n📊 Loading MPC data for {target_name}...")
mpc = pd.read_csv("I3_clean.csv")
mpc["date"] = pd.to_datetime(mpc["date"], errors="coerce")
mpc = mpc[(mpc["date"] >= start_date) & (mpc["date"] <= end_date)]
mpc["month"] = mpc["date"].dt.to_period("M")
mpc_monthly = mpc.groupby("month")["mag"].agg(["mean", "std", "count"]).reset_index()

# --- Attempt ZTF cross-validation via IRSA TAP ---
print(f"\n🔭 Querying ZTF (via IRSA TAP) near {target_name} (RA={coord_comet.ra.deg:.2f}°, Dec={coord_comet.dec.deg:.2f}°)...")

adql_query = f"""
SELECT obsjd, ra, dec, magpsf, sigmapsf, filtercode
FROM ztf_dr19.photometry
WHERE CONTAINS(
    POINT('ICRS', ra, dec),
    CIRCLE('ICRS', {coord_comet.ra.deg}, {coord_comet.dec.deg}, 0.05)
)=1
"""

ztf_table = None
try:
    result = Irsa.query_tap(adql_query)
    ztf_table = result.to_table()
    print(f"✅ Retrieved {len(ztf_table)} ZTF rows from IRSA TAP.")
except Exception as e:
    print(f"⚠️ IRSA TAP query failed: {e}")
    print("💡 Continuing with MPC data only.")
    ztf_table = None

# --- Process ZTF results (if available) ---
if ztf_table is not None and len(ztf_table) > 0:
    df_ztf = ztf_table.to_pandas()

    # Convert Julian dates → calendar
    if "obsjd" in df_ztf.columns:
        df_ztf["date"] = pd.to_datetime(df_ztf["obsjd"], unit="D", origin="julian", errors="coerce")
    else:
        print("⚠️ Missing obsjd column — skipping ZTF processing.")
        df_ztf = pd.DataFrame()

    df_ztf = df_ztf[(df_ztf["date"] >= start_date) & (df_ztf["date"] <= end_date)]
    df_ztf["month"] = df_ztf["date"].dt.to_period("M")

    # Convert g/r to V-band equivalents
    if "filtercode" in df_ztf.columns:
        def to_V(row):
            if row["filtercode"] == "zg":
                return row["magpsf"] + 0.2
            elif row["filtercode"] == "zr":
                return row["magpsf"] - 0.1
            return row["magpsf"]
        df_ztf["mag_V"] = df_ztf.apply(to_V, axis=1)
    else:
        df_ztf["mag_V"] = df_ztf["magpsf"]

    ztf_monthly = df_ztf.groupby("month")["mag_V"].agg(["mean", "std", "count"]).reset_index()

    # Merge datasets
    merged = pd.merge(mpc_monthly, ztf_monthly, on="month", how="outer", suffixes=("_mpc", "_ztf"))
    merged = merged.sort_values("month")
    merged.to_csv("I3_ZTF_Merged.csv", index=False)

    # --- Plot comparison ---
    plt.figure(figsize=(8, 5))
    plt.errorbar(merged["month"].astype(str), merged["mean_mpc"], yerr=merged["std_mpc"],
                 fmt="o-", color="gold", label="MPC (observed)", markersize=8, linewidth=2, capsize=4)
    plt.errorbar(merged["month"].astype(str), merged["mean_ztf"], yerr=merged["std_ztf"],
                 fmt="s--", color="steelblue", label="ZTF DR19 (independent)", markersize=6, linewidth=2, capsize=4)
    plt.gca().invert_yaxis()
    plt.title("3I/ATLAS Brightness Comparison — MPC vs ZTF DR19 (2025)")
    plt.xlabel("Month (2025)")
    plt.ylabel("Mean magnitude (V-equiv.)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("I3_ZTF_Comparison.png", dpi=200)
    print("✅ Saved: I3_ZTF_Comparison.png and I3_ZTF_Merged.csv")

else:
    # --- MPC-only fallback ---
    print("⚠️ No ZTF data available; plotting MPC brightness only.")
    plt.figure(figsize=(8, 5))
    plt.errorbar(mpc_monthly["month"].astype(str), mpc_monthly["mean"],
                 yerr=mpc_monthly["std"], fmt="o-", color="red",
                 label="MPC (observed)", markersize=8, linewidth=2, capsize=4)
    plt.gca().invert_yaxis()
    plt.title("3I/ATLAS Brightness Trend — MPC Data Only (2025)")
    plt.xlabel("Month (2025)")
    plt.ylabel("Mean magnitude (V)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("I3_MPC_Only.png", dpi=200)
    print("✅ Saved: I3_MPC_Only.png (MPC data only)")

# --- Summary ---
print("\n📈 MPC Brightness Trend (July–Oct 2025):")
print(f"   {mpc_monthly['mean'].iloc[0]:.2f} → {mpc_monthly['mean'].iloc[-1]:.2f} mag "
      f"(Δm = {mpc_monthly['mean'].iloc[0] - mpc_monthly['mean'].iloc[-1]:.2f} mag)")
