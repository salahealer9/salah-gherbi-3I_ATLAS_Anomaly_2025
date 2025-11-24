#!/usr/bin/env python3
"""
atlas_optical_acceleration.py
3I/ATLAS — Compare photometric (optical) acceleration with
non-gravitational acceleration epoch (JPL solution by Farnocchia, 2025-10-29).
Author: Salah-Eddin Gherbi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
MPC_FILE = "I3.txt"              # your current MPC photometry file
OUT_FIG = "I3_Optical_Acceleration_Trend.png"
PERIHELION = pd.Timestamp("2025-10-29", tz="UTC")
A1_NGA = 1.662e-6  # au/day^2 from JPL solution
A1_MS2 = A1_NGA * 1.496e11 / (86400**2)  # convert to m/s^2
A1_MS2_MM = A1_MS2 * 1e3  # mm/s^2 for label convenience

# ------------------------------------------------------------
# Step 1 — Parse photometric brightness (magnitude vs date)
# ------------------------------------------------------------
def parse_mpc_photometry(path):
    import re
    data = []
    with open(path) as f:
        for line in f:
            if not line.startswith("0003I"):
                continue
            m = re.search(r"C2025\s(\d{2})\s(\d{2}\.\d+)", line)
            if not m:
                continue
            month = int(m.group(1))
            dayf = float(m.group(2))
            magm = re.search(r"(\d{2}\.\d{2})([A-Za-z])", line)
            if not magm:
                continue
            mag = float(magm.group(1))
            date = pd.Timestamp(2025, month, int(dayf), tz="UTC") + pd.to_timedelta((dayf % 1) * 24, unit="h")
            data.append({"date": date, "mag": mag})
    df = pd.DataFrame(data)
    df = df.sort_values("date").reset_index(drop=True)
    return df

df = parse_mpc_photometry(MPC_FILE)
print(f"✅ Parsed {len(df)} observations from {df['date'].min().date()} to {df['date'].max().date()}")

# ------------------------------------------------------------
# Step 2 — Compute brightness derivative (optical acceleration proxy)
# ------------------------------------------------------------
df["dm_dt"] = df["mag"].diff() / df["date"].diff().dt.days
df["inv_mag"] = 1 / df["mag"]  # inverse magnitude proxy for brightness
df["inv_mag_smooth"] = df["inv_mag"].rolling(7, center=True, min_periods=1).mean()
df["accel_proxy"] = df["inv_mag_smooth"].diff() / df["date"].diff().dt.days

# DEBUG: check value ranges
print("\n=== Optical Acceleration Diagnostics ===")
print(df[["date", "inv_mag_smooth", "accel_proxy"]].tail(10))
print(f"Acceleration range: {df['accel_proxy'].min():.3e} → {df['accel_proxy'].max():.3e}")


# ------------------------------------------------------------
# Step 3 — Plot
# ------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(10,5))
ax2 = ax1.twinx()

ax1.plot(df["date"], df["inv_mag_smooth"], color="tab:blue", lw=1.8, label="Optical Brightness (1/mag)")
ax2.plot(df["date"], df["accel_proxy"], color="tab:red", lw=1.2, label="Optical Acceleration (dL/dt)")

# perihelion marker
ax1.axvline(PERIHELION, color="magenta", linestyle="--", lw=1.3, alpha=0.7)
ax1.text(PERIHELION + pd.Timedelta(days=1), df["inv_mag_smooth"].min(),
         "Perihelion / NGA detection\n(2025-10-29)\nA₁≈1.66×10⁻⁶ au/d²\n≈{:.3f} mm/s²".format(A1_MS2_MM),
         color="magenta", fontsize=8, va="bottom", ha="left")

ax1.set_ylabel("Relative Brightness (1/mag)", color="tab:blue")
ax2.set_ylabel("Optical Acceleration Proxy", color="tab:red")
ax1.set_xlabel("Date (2025)")
ax1.set_title("3I/ATLAS — Optical vs Non-Gravitational Acceleration")
ax1.grid(alpha=0.3)

# legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.tight_layout()
plt.savefig(OUT_FIG, dpi=250)
print(f"✅ Saved: {OUT_FIG}")
