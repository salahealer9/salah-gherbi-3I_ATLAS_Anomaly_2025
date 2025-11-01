#!/usr/bin/env python3
"""
atlas_optical_color_correlation_v1.py
Composite diagnostic: 3I/ATLAS optical acceleration vs. color evolution.
Author: Salah-Eddin Gherbi  |  ORCID 0009-0005-4017-1095
Repository: https://github.com/salahealer9/salah-gherbi-3I_ATLAS_Anomaly_2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Load optical brightness/acceleration data ===
opt = pd.read_csv("I3_Optical_Acceleration_Data.csv", parse_dates=["date"])  # if saved from v2
opt = opt.sort_values("date")

# === Load color index data ===
color = pd.read_csv("I3_Color_Alerts_20251031_1848.csv", parse_dates=["date"])
color = color[color["pair"].isin(["g-o", "r-o"])]
color["color_smooth"] = (
    color.groupby("pair")["color"]
    .transform(lambda x: x.rolling(3, center=True, min_periods=1).mean())
)

# === Define perihelion and acceleration window ===
# FIX: Add timezone to all hardcoded dates
perihelion = pd.Timestamp("2025-10-29", tz="UTC")  # ← ADD tz="UTC"
window_start = pd.Timestamp("2025-09-08", tz="UTC")  # ← ADD tz="UTC"
window_end   = pd.Timestamp("2025-09-16", tz="UTC")  # ← ADD tz="UTC"

# ------------------------------------------------------------
# FIGURE SETUP
# ------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), sharey=False)
fig.suptitle("3I/ATLAS — Pre-Perihelion Optical Acceleration & Color Evolution", fontsize=13, weight="bold")

# ------------------------------------------------------------
# LEFT PANEL — Brightness vs Optical Acceleration
# ------------------------------------------------------------
ax1.plot(opt["date"], opt["inv_mag_smooth"], color="tab:blue", lw=1.8, label="Optical Brightness (1/mag)")
ax1_twin = ax1.twinx()
ax1_twin.plot(opt["date"], opt["accel_proxy"], color="tab:red", lw=1.2, label="Optical Acceleration (scaled)")

# Cyan shaded early-acceleration window
ax1.axvspan(window_start, window_end, color="cyan", alpha=0.12, label="Acceleration window")

# Perihelion marker
ax1.axvline(perihelion, color="magenta", linestyle="--", lw=1)
ax1.text(perihelion + pd.Timedelta(days=3), ax1.get_ylim()[0]+0.0005,
         "Perihelion\n2025-10-29", color="magenta", fontsize=8)

ax1.set_xlabel("Date (UTC, 2025)")
ax1.set_ylabel("Relative Brightness (1/mag)", color="tab:blue")
ax1_twin.set_ylabel("Scaled Optical Acceleration", color="tab:red")

# Legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8)

ax1.set_title("Optical Activity Timeline")

# ------------------------------------------------------------
# RIGHT PANEL — Color Evolution (show truth clearly)
# ------------------------------------------------------------
# Show ALL g-o data since r-o is from different epoch
sub = color[color["pair"] == "g-o"].sort_values("date")

ax2.plot(sub["date"], sub["color_smooth"], "o-", color="green", lw=1.5, 
         label="g–o color index", markersize=4)

# Add July early-phase window (bluing epoch)
ax2.axvspan(pd.Timestamp("2025-07-01", tz="UTC"),
            pd.Timestamp("2025-07-31", tz="UTC"),
            color="blue", alpha=0.08, label="Early Bluing (July)")

# Highlight the acceleration window and the reddening
ax2.axvspan(window_start, window_end, color="cyan", alpha=0.12, 
           label="Acceleration window\n(g–o reddening)")

# Mark the reddening trend with annotation
accel_g_o = sub[(sub["date"] >= window_start) & (sub["date"] <= window_end)]
if len(accel_g_o) > 1:
    reddening_trend = accel_g_o["color_smooth"].iloc[-1] - accel_g_o["color_smooth"].iloc[0]
    ax2.annotate(f"Reddening: Δ = {reddening_trend:+.2f} mag", 
                xy=(window_start + (window_end-window_start)/2, accel_g_o["color_smooth"].mean()),
                xytext=(10, 20), textcoords="offset points", 
                bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.7),
                arrowprops=dict(arrowstyle="->"), fontsize=8)

ax2.axvline(perihelion, color="magenta", linestyle="--", lw=1, alpha=0.7)
ax2.text(perihelion, ax2.get_ylim()[0], "Perihelion", 
         color="magenta", fontsize=7, rotation=90, va="bottom")

ax2.set_xlabel("Date (UTC, 2025)")
ax2.set_ylabel("g–o Color Index (mag)")
ax2.set_title("Color Evolution: Reddening During Acceleration")
ax2.legend(fontsize=8)
ax2.grid(alpha=0.3)

# --- Fix overlapping x-axis dates ---
for ax in [ax1, ax2]:
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right", fontsize=8)
    ax.xaxis.set_major_formatter(
        plt.matplotlib.dates.DateFormatter("%b-%d")
    )

# === DEBUG: Check what's happening with color data ===
print("🔍 COLOR DATA DIAGNOSTICS:")
print(f"Total g-o points: {len(color[color['pair']=='g-o'])}")
print(f"Total r-o points: {len(color[color['pair']=='r-o'])}")

# Check the date range in your filtered data
mask = (color["date"] >= pd.Timestamp("2025-08-25", tz="UTC")) & (color["date"] <= pd.Timestamp("2025-09-25", tz="UTC"))
sub = color[mask]
print(f"Points in zoomed range: {len(sub)}")
print(f"g-o in range: {len(sub[sub['pair']=='g-o'])}")
print(f"r-o in range: {len(sub[sub['pair']=='r-o'])}")

# Check g-o values during your acceleration window
accel_mask = (sub["date"] >= window_start) & (sub["date"] <= window_end)
g_o_in_window = sub[(sub["pair"] == "g-o") & accel_mask]
print(f"g-o values during acceleration window:")
print(g_o_in_window[["date", "color", "color_smooth"]].to_string())

# Find where r–o data actually exists
print("📅 r–o date range:")
r_o_dates = color[color["pair"] == "r-o"]["date"]
print(f"From {r_o_dates.min()} to {r_o_dates.max()}")

# Expand your right panel to include ALL available data
mask = (color["date"] >= pd.Timestamp("2025-07-01", tz="UTC")) & (color["date"] <= pd.Timestamp("2025-10-31", tz="UTC"))

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("I3_Optical_Color_Correlation.png", dpi=250)
print("✅ Saved: I3_Optical_Color_Correlation.png")