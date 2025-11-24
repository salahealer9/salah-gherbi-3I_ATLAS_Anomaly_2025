#!/usr/bin/env python3
"""
atlas_delta_v_from_optical_proxy.py

Estimate Δv and lateral displacement at Jupiter from the optical-acceleration
proxy for 3I/ATLAS (C/2025 N1), using the data in:

    I3_Optical_Acceleration_Data.csv

Expected columns:
    date, days_from_perihelion, mag, inv_mag, inv_mag_smooth,
    accel_proxy, accel_proxy_scaled

Author: Salah-Eddin Gherbi
"""

import pandas as pd
import numpy as np

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------
CSV_FILE = "I3_Optical_Acceleration_Data.csv"

# Choose which column to treat as the proxy:
PROXY_COL = "accel_proxy_scaled"
# If you want the raw one instead, set:
# PROXY_COL = "accel_proxy"

# Active window (UTC) – adjust as you like
# This covers your two main peaks plus a margin
ACTIVE_START = "2025-09-01"
ACTIVE_END   = "2025-11-21"

# Target total Δv over active window (m/s), based on NG parameter A1 etc.
# You can experiment with values in the ~8–30 m/s range.
TARGET_DELTA_V = 8.0  # m/s

# Hyperbolic excess speed (m/s)
V_INF = 6.0e4  # ~60 km/s

# Distance from perihelion to Jupiter encounter (m)
AU = 1.495978707e11
L_TO_JUPITER = 5.0 * AU   # ~5 AU

# Jet orientation angles (deg) relative to velocity vector
JET_ANGLES_DEG = [30, 60, 90]

# Output file for enriched time series
OUT_CSV = "I3_Optical_Acceleration_DeltaV.csv"

# -------------------------------------------------------------------
# 1) LOAD DATA
# -------------------------------------------------------------------
df = pd.read_csv(CSV_FILE)

# Parse dates (with timezone)
df["date"] = pd.to_datetime(df["date"], utc=True)
df = df.sort_values("date").reset_index(drop=True)

if PROXY_COL not in df.columns:
    raise RuntimeError(f"Proxy column '{PROXY_COL}' not found in CSV. "
                       f"Available columns: {list(df.columns)}")

# Rename proxy column for convenience
df["proxy"] = df[PROXY_COL].astype(float)

# Compute time steps in seconds
df["dt_sec"] = df["date"].diff().dt.total_seconds()

# For the first entry, approximate dt as median of later steps
if np.isnan(df["dt_sec"].iloc[0]):
    df.loc[0, "dt_sec"] = df["dt_sec"].iloc[1:].median()

# -------------------------------------------------------------------
# 2) SELECT ACTIVE WINDOW & CALIBRATE PROXY SCALE
# -------------------------------------------------------------------
mask_active = (df["date"] >= ACTIVE_START) & (df["date"] <= ACTIVE_END)
df_active = df.loc[mask_active].copy()

if df_active.empty:
    raise RuntimeError("Active window selection returned no data; "
                       "check ACTIVE_START and ACTIVE_END.")

# We want: sum( k * proxy_i * dt_i ) ≈ TARGET_DELTA_V
# => k = TARGET_DELTA_V / sum( proxy_i * dt_i )
sum_proxy_dt = (df_active["proxy"] * df_active["dt_sec"]).sum()

if sum_proxy_dt == 0:
    raise RuntimeError("Sum of proxy * dt is zero; "
                       "proxy may be zero or constant in active window.")

k = TARGET_DELTA_V / sum_proxy_dt  # m/s^2 per proxy-unit
print(f"[INFO] Using proxy column: {PROXY_COL}")
print(f"[INFO] Calibration factor k = {k:.3e} m/s^2 per proxy-unit.")

# Apply to full time series
df["accel_m_s2"] = k * df["proxy"]

# -------------------------------------------------------------------
# 3) INTEGRATE TO GET CUMULATIVE Δv(t)
# -------------------------------------------------------------------
df["delta_v_m_s"] = df["accel_m_s2"] * df["dt_sec"]
df["cum_delta_v_m_s"] = df["delta_v_m_s"].cumsum()

total_delta_v_active = df.loc[mask_active, "delta_v_m_s"].sum()
print(f"[INFO] Total Δv over active window [{ACTIVE_START} → {ACTIVE_END}] "
      f"≈ {total_delta_v_active:.2f} m/s (target was {TARGET_DELTA_V:.2f} m/s).")

# -------------------------------------------------------------------
# 4) ESTIMATE LATERAL SHIFT AT JUPITER FOR DIFFERENT JET ANGLES
# -------------------------------------------------------------------
results = []

for angle_deg in JET_ANGLES_DEG:
    angle_rad = np.deg2rad(angle_deg)
    dv_total = total_delta_v_active
    dv_perp = dv_total * np.sin(angle_rad)  # transverse component

    delta_b_m = (dv_perp / V_INF) * L_TO_JUPITER
    delta_b_km = delta_b_m / 1e3

    results.append((angle_deg, dv_total, dv_perp, delta_b_km))

print("\n[RESULTS] Lateral displacement at Jupiter due to NG Δv:")
print("Angle (deg) | Δv_total (m/s) | Δv_perp (m/s) | Δb (km)")
for angle_deg, dv_total, dv_perp, delta_b_km in results:
    print(f"{angle_deg:11.0f} | {dv_total:13.3f} | {dv_perp:12.3f} | {delta_b_km:9.0f}")

# -------------------------------------------------------------------
# 5) SAVE ENRICHED TIME SERIES
# -------------------------------------------------------------------
df.to_csv(OUT_CSV, index=False)
print(f"\n[INFO] Saved enriched time series with Δv to: {OUT_CSV}")
