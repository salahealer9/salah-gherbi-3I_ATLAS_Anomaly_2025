#!/usr/bin/env python3
"""
atlas_optical_acceleration_v2.py
3I/ATLAS — Optical vs Non-Gravitational Acceleration
Author: Salah-Eddin Gherbi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------
MPC_FILE = "I3.txt"
OUT_FIG = "I3_Optical_Acceleration_Trend_v2.png"
PERIHELION = pd.Timestamp("2025-10-29", tz="UTC")
A1_NGA = 1.662e-6  # au/day²
A1_MS2 = A1_NGA * 1.496e11 / (86400**2)
A1_MS2_MM = A1_MS2 * 1e3  # mm/s²

# ------------------------------------------------------------
# Parse MPC photometry (IMPROVED VERSION)
# ------------------------------------------------------------

rows = []
with open(MPC_FILE) as f:
    for line in f:
        if not line.startswith("0003I"):
            continue
        m = re.search(r"2025\s(\d{2})\s(\d{2}\.\d+)", line)
        if not m:
            continue
        month = int(m.group(1))
        dayf = float(m.group(2))
        
        # IMPROVED MAGNITUDE PARSING WITH VALIDATION
        mag = None
        parts = line.split()
        
        if len(parts) >= 2:
            potential_mag = parts[-2]
            
            # Check if this looks like a real magnitude (not coordinates)
            if (potential_mag.replace('.', '').isdigit() and 
                len(potential_mag) <= 5 and  # Magnitudes are usually 4-5 chars like "12.3"
                float(potential_mag) >= 8 and  # Realistic comet magnitudes
                float(potential_mag) <= 20):
                
                mag = float(potential_mag)
            
            # Additional check: if the "magnitude" looks like coordinates, discard it
            elif (potential_mag.replace('.', '').isdigit() and 
                  (float(potential_mag) > 20 or float(potential_mag) < 8)):
                
                # This is likely coordinates, not magnitude - check if magnitude is actually missing
                # Look for pattern: coordinates then immediately observatory code = missing magnitude
                obs_code = parts[-1]
                if (len(obs_code) >= 7 and obs_code[0].isalpha() and 
                    any(c.isdigit() for c in obs_code)):
                    
                    # Pattern: [coordinates] [observatory] with no magnitude in between
                    # This means magnitude is missing
                    mag = None

        day_int = int(dayf)
        frac_day = dayf - day_int
        date = pd.Timestamp(2025, month, day_int, tz="UTC") + pd.to_timedelta(frac_day * 24, unit="h")
        rows.append({"date": date, "mag": mag})

df = pd.DataFrame(rows)
df = df.sort_values("date").reset_index(drop=True)
print(f"✅ Parsed {len(df)} MPC observations ({df['date'].min().date()} → {df['date'].max().date()})")

# ------------------------------------------------------------
# Bin data by day (avoid minute-level dt explosions)
# ------------------------------------------------------------
df["day"] = df["date"].dt.floor("D")

# 🎯 DEBUG: Check what data we're actually grouping
print(f"🔍 Before grouping: {len(df)} total, {df['mag'].notna().sum()} with magnitudes")
print(f"📅 Date range with magnitudes: {df[df['mag'].notna()]['date'].min()} → {df[df['mag'].notna()]['date'].max()}")

df_with_mag = df[df['mag'].notna()].copy()
df_daily = df_with_mag.groupby("day")["mag"].mean().reset_index()
df_daily.rename(columns={"day": "date"}, inplace=True)

# Compute optical proxies
df_daily["inv_mag"] = 1 / df_daily["mag"]
df_daily["inv_mag_smooth"] = df_daily["inv_mag"].rolling(3, center=True, min_periods=1).mean()

# Derivative (optical acceleration proxy)
df_daily["accel_proxy"] = df_daily["inv_mag_smooth"].diff() / df_daily["date"].diff().dt.days
df_daily = df_daily.replace([np.inf, -np.inf], np.nan).dropna(subset=["accel_proxy"])

print(f"Acceleration range: {df_daily['accel_proxy'].min():.3e} → {df_daily['accel_proxy'].max():.3e}")

# ------------------------------------------------------------
# Plot
# ------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(10,5))
ax2 = ax1.twinx()

ax1.plot(df_daily["date"], df_daily["inv_mag_smooth"], color="tab:blue", lw=1.8, label="Optical Brightness (1/mag)")

# Rescale acceleration so it fits visually
scale = df_daily["inv_mag_smooth"].max() * 0.3 / df_daily["accel_proxy"].abs().max()
ax2.plot(df_daily["date"], df_daily["accel_proxy"] * scale, color="tab:red", lw=1.3, alpha=0.8, label="Optical Acceleration (scaled)")

# Mark perihelion / NGA detection
ax1.axvline(PERIHELION, color="magenta", linestyle="--", lw=1.2, alpha=0.8)
ax1.text(PERIHELION + pd.Timedelta(days=1), df_daily["inv_mag_smooth"].min(),
         f"Perihelion / NGA detection\n2025-10-29\nA₁≈1.66×10⁻⁶ au/d² ≈ {A1_MS2_MM:.3f} mm/s²",
         color="magenta", fontsize=8, va="bottom", ha="left")

ax1.set_ylabel("Relative Brightness (1/mag)", color="tab:blue")
ax2.set_ylabel("Scaled Optical Acceleration", color="tab:red")
ax1.set_xlabel("Date (2025)")
ax1.set_title("3I/ATLAS — Optical vs Non-Gravitational Acceleration")
ax1.grid(alpha=0.3)

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

# ------------------------------------------------------------
# Detect first significant acceleration peak before perihelion
# ------------------------------------------------------------
peak_idx = df_daily["accel_proxy"].abs().idxmax()
peak_date = df_daily.loc[peak_idx, "date"]
peak_val = df_daily.loc[peak_idx, "accel_proxy"]
print(f"🔍 Max optical acceleration at {peak_date.date()} : {peak_val:.3e} (scaled units)")
if peak_date < PERIHELION:
    print("⚡ Detected pre-perihelion acceleration surge — consistent with early activity.")
else:
    print("📉 Acceleration peak occurs post-perihelion — likely response to solar heating.")

# ------------------------------------------------------------
# Mark the revised A_opt peak on the plot
# ------------------------------------------------------------

ax1.axvline(peak_date, color="gray", linestyle="--", lw=1.0, alpha=0.8)
ax1.text(
    peak_date + pd.Timedelta(days=1),
    df_daily["inv_mag_smooth"].max() * 0.9,
    f"Revised A_opt peak\n{peak_date.date()}",
    fontsize=7,
    color="gray",
    va="top",
    ha="left",
)

# ------------------------------------------------------------
# Optional overlay: color index correlation (e.g., r–o or g–o)
# ------------------------------------------------------------
try:
    color_file = "I3_Color_Alerts_20251105_2037.csv"  # Updated to your latest file
    color_df = pd.read_csv(color_file, parse_dates=["date"])
    color_df = color_df[color_df["pair"].isin(["r-o", "g-o"])]

    # Smooth by 3-day rolling mean for stability
    color_df["color_smooth"] = (
        color_df.groupby("pair")["color"]
        .transform(lambda x: x.rolling(3, center=True, min_periods=1).mean())
    )

    ax3 = ax1.twinx()  # third y-axis on right
    color_palette = {"r-o": "orange", "g-o": "green"}
    offset = (df_daily["inv_mag_smooth"].max() * 0.25)  # vertical shift for readability

    for i, pair in enumerate(color_df["pair"].unique()):
        sub = color_df[color_df["pair"] == pair].sort_values("date")
        ax3.plot(sub["date"], sub["color_smooth"] - i * 0.2,  # offset slightly
                 color=color_palette[pair], lw=1.2,
                 label=f"{pair} color index (×1)")

    ax3.set_ylabel("Color index (mag)", color="gray")
    ax3.tick_params(axis="y", colors="gray")
    ax3.spines["right"].set_position(("outward", 60))

    # Annotate possible resonance window
    ax1.axvspan(pd.Timestamp("2025-09-09", tz="UTC"),
                pd.Timestamp("2025-09-11", tz="UTC"),
                color="cyan", alpha=0.1, label="g-o reddening window")

    lines3, labels3 = ax3.get_legend_handles_labels()
    ax1.legend(lines1 + lines2 + lines3,
               labels1 + labels2 + labels3,
               loc="upper left", fontsize=8)
    print("🎨 Added color overlay (r–o / g–o).")
except Exception as e:
    print(f"⚠️ Could not add color overlay: {e}")

from matplotlib.dates import DateFormatter
ax1.xaxis.set_major_formatter(DateFormatter("%b-%d"))
plt.setp(ax1.get_xticklabels(), rotation=30, ha="right", fontsize=8)

plt.tight_layout()
plt.savefig(OUT_FIG, dpi=250)
print(f"✅ Saved: {OUT_FIG}")

# === Export acceleration dataset for cross-analysis ===
out_csv = "I3_Optical_Acceleration_Data.csv"

# Calculate days from perihelion for easier analysis
df_daily["days_from_perihelion"] = (df_daily["date"] - PERIHELION).dt.days

optical_df = pd.DataFrame({
    "date": df_daily["date"],
    "days_from_perihelion": df_daily["days_from_perihelion"],
    "mag": df_daily["mag"], 
    "inv_mag": df_daily["inv_mag"],
    "inv_mag_smooth": df_daily["inv_mag_smooth"],
    "accel_proxy": df_daily["accel_proxy"],
    "accel_proxy_scaled": df_daily["accel_proxy"] * scale  # Same scaling as plot
})

optical_df.to_csv(out_csv, index=False)
print(f"💾 Exported {len(optical_df)} days of optical acceleration data → {out_csv}")