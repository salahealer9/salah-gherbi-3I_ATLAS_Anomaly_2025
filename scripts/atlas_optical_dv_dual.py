#!/usr/bin/env python3
"""
atlas_optical_dv_dual.py

From the 3I/ATLAS optical-acceleration data, compute:
- two calibrated Δv(t) curves (8 m/s and 25 m/s total over the active window)
- the corresponding lateral displacement Δb at Jupiter for several jet angles
- a dual-panel plot comparing the cumulative Δv(t) in both scalings.

Expected CSV: I3_Optical_Acceleration_Data.csv
Columns used:
    date, days_from_perihelion, accel_proxy_scaled

Author: Salah-Eddin Gherbi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------
CSV_FILE = "I3_Optical_Acceleration_Data.csv"

# Column with your optical acceleration proxy
PROXY_COL = "accel_proxy_scaled"

# Active window for integrating Δv (perihelion-era anomaly)
ACTIVE_START = "2025-09-01"
ACTIVE_END   = "2025-11-21"

# Two target Δv values (m/s)
DV_TARGETS = [8.0, 25.0]

# Hyperbolic excess speed and distance to Jupiter encounter
V_INF = 6.0e4  # m/s ~ 60 km/s
AU = 1.495978707e11
L_TO_JUPITER = 5.0 * AU  # m (~5 AU)

# Jet angles (deg)
JET_ANGLES_DEG = [30, 60, 90]

# Output figure
OUT_FIG = "I3_Optical_Acceleration_DeltaV_8_vs_25.png"

# -------------------------------------------------------------------
# 1) LOAD DATA
# -------------------------------------------------------------------
df = pd.read_csv(CSV_FILE)

# Parse dates
df["date"] = pd.to_datetime(df["date"], utc=True)
df = df.sort_values("date").reset_index(drop=True)

if PROXY_COL not in df.columns:
    raise RuntimeError(
        f"Proxy column '{PROXY_COL}' not found. Available: {list(df.columns)}"
    )

df["proxy"] = df[PROXY_COL].astype(float)

# Time step in seconds
df["dt_sec"] = df["date"].diff().dt.total_seconds()
if np.isnan(df["dt_sec"].iloc[0]):
    df.loc[0, "dt_sec"] = df["dt_sec"].iloc[1:].median()

# Active window mask
mask_active = (df["date"] >= ACTIVE_START) & (df["date"] <= ACTIVE_END)
if not mask_active.any():
    raise RuntimeError("Active window select returned no rows. Check dates.")

# -------------------------------------------------------------------
# 2) FUNCTION TO CALIBRATE TO A GIVEN Δv
# -------------------------------------------------------------------
def calibrate_to_delta_v(df, mask_active, target_dv, label):
    """
    Returns:
      accel_m_s2_<label>, delta_v_m_s_<label>, cum_delta_v_m_s_<label>, total_dv
    """
    sub = df.loc[mask_active]

    sum_proxy_dt = (sub["proxy"] * sub["dt_sec"]).sum()
    if sum_proxy_dt == 0:
        raise RuntimeError("Sum(proxy * dt) is zero in active window.")

    k = target_dv / sum_proxy_dt  # m/s^2 per proxy unit

    accel_col = f"accel_m_s2_{label}"
    dv_col = f"delta_v_m_s_{label}"
    cum_col = f"cum_delta_v_m_s_{label}"

    df[accel_col] = k * df["proxy"]
    df[dv_col] = df[accel_col] * df["dt_sec"]
    df[cum_col] = df[dv_col].cumsum()

    total_dv = df.loc[mask_active, dv_col].sum()
    print(f"[INFO] {label}: k = {k:.3e} m/s^2 per proxy-unit, "
          f"total Δv_active ≈ {total_dv:.2f} m/s (target {target_dv:.2f})")

    return total_dv, accel_col, dv_col, cum_col

# -------------------------------------------------------------------
# 3) CALIBRATE FOR BOTH 8 m/s AND 25 m/s
# -------------------------------------------------------------------
dv_results = {}  # label -> (target_dv, total_dv, cum_col)

for target in DV_TARGETS:
    label = f"{int(target)}"
    total_dv, accel_col, dv_col, cum_col = calibrate_to_delta_v(
        df, mask_active, target, label
    )
    dv_results[label] = {
        "target": target,
        "total": total_dv,
        "cum_col": cum_col,
    }

# -------------------------------------------------------------------
# 4) COMPUTE LATERAL SHIFTS FOR EACH CASE
# -------------------------------------------------------------------
print("\n[RESULTS] Lateral displacement at Jupiter:")
for label, info in dv_results.items():
    target = info["target"]
    total_dv = info["total"]
    print(f"\nΔv case: {target:.1f} m/s")
    print("Angle (deg) | Δv_total (m/s) | Δv_perp (m/s) | Δb (km)")
    for angle_deg in JET_ANGLES_DEG:
        angle_rad = np.deg2rad(angle_deg)
        dv_perp = total_dv * np.sin(angle_rad)
        delta_b_m = (dv_perp / V_INF) * L_TO_JUPITER
        delta_b_km = delta_b_m / 1e3
        print(f"{angle_deg:11.0f} | {total_dv:13.3f} | "
              f"{dv_perp:12.3f} | {delta_b_km:9.0f}")

# -------------------------------------------------------------------
# 5) PLOT DUAL-PANEL CUMULATIVE Δv(t)
# -------------------------------------------------------------------
x = df["days_from_perihelion"]

fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# 8 m/s panel
ax = axes[0]
cum8 = df[dv_results["8"]["cum_col"]]
ax.plot(x, cum8, lw=2, label="Cumulative Δv(t), total ≈ 8 m/s")
ax.axvline(0, color="black", lw=1, linestyle="--")
ax.set_ylabel("Δv (m/s)")
ax.set_title("Minimal case: Δv_total ≈ 8 m/s")
ax.legend(loc="upper left")

# 25 m/s panel
ax = axes[1]
cum25 = df[dv_results["25"]["cum_col"]]
ax.plot(x, cum25, lw=2, label="Cumulative Δv(t), total ≈ 25 m/s")
ax.axvline(0, color="black", lw=1, linestyle="--")
ax.set_ylabel("Δv (m/s)")
ax.set_xlabel("Days from Perihelion (2025-10-29)")
ax.set_title("Photometric-inferred case: Δv_total ≈ 25 m/s")
ax.legend(loc="upper left")

plt.tight_layout()
plt.savefig(OUT_FIG, dpi=300)
print(f"\n[INFO] Saved figure to {OUT_FIG}")

# -------------------------------------------------------------------
# Overlay both Δv curves on one panel
# -------------------------------------------------------------------
plt.figure(figsize=(10,5))
plt.plot(x, cum8, label="Δv_total ≈ 8 m/s", lw=2)
plt.plot(x, cum25, label="Δv_total ≈ 25 m/s", lw=2)
plt.axvline(0, color="black", lw=1, linestyle="--")
plt.xlabel("Days from Perihelion (2025-10-29)")
plt.ylabel("Cumulative Δv (m/s)")
plt.title("Overlay: 8 m/s vs 25 m/s Calibrations")
plt.legend()
plt.tight_layout()
plt.savefig("I3_Optical_Acceleration_DeltaV_Overlay.png", dpi=300)
print("[INFO] Saved overlay figure to I3_Optical_Acceleration_DeltaV_Overlay.png")
