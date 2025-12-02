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
import glob

from matplotlib.dates import DateFormatter
POST_DAYS = 12          # how many days after perihelion to shade
N_LABEL_LAST = 3        # annotate last N post-perihelion points

# === Load optical brightness/acceleration data ===
opt = pd.read_csv("I3_Optical_Acceleration_Data.csv", parse_dates=["date"])  # if saved from v2
opt = opt.sort_values("date")

def split_pre_post(df, time_col="date", peri=None):
    pre = df[df[time_col] < peri].copy()
    post = df[df[time_col] >= peri].copy()
    return pre, post

def annotate_last(ax, df, xcol, ycol, n=N_LABEL_LAST, fmt="%b-%d"):
    if df.empty: return
    tail = df.tail(n)
    for _, r in tail.iterrows():
        ax.annotate(r[xcol].strftime(fmt),
                    xy=(r[xcol], r[ycol]),
                    xytext=(6,6), textcoords="offset points",
                    fontsize=7, bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.6))

# === Load color index data ===

try:
    # Automatically pick the latest colour-alert CSV
    alert_files = sorted(glob.glob("I3_Color_Alerts_*.csv"))
    if len(alert_files) == 0:
        raise FileNotFoundError("No I3_Color_Alerts_*.csv files found in current directory.")

    color_file = alert_files[-1]  # most recent file
    print(f"🎨 Using colour-alert file: {color_file}")

    color = pd.read_csv(color_file, parse_dates=["date"])
    color = color[color["pair"].isin(["g-o", "r-o"])]

    color["color_smooth"] = (
        color.groupby("pair")["color"]
        .transform(lambda x: x.rolling(3, center=True, min_periods=1).mean())
    )

except Exception as e:
    print(f"⚠️ Colour correlation overlay disabled: {e}")
    color = None


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
# Split pre/post
opt_pre, opt_post = split_pre_post(opt, "date", perihelion)

# Brightness (1/mag)
ax1.plot(opt_pre["date"], opt_pre["inv_mag_smooth"],
         color="tab:blue", lw=1.8, label="Optical Brightness (1/mag) — pre")
ax1.plot(opt_post["date"], opt_post["inv_mag_smooth"],
         color="tab:blue", lw=2.2, linestyle="--", marker="o", ms=3,
         label="Optical Brightness (1/mag) — post")

# Acceleration (scaled)
ax1_twin = ax1.twinx()
ax1_twin.plot(opt_pre["date"], opt_pre["accel_proxy"],
              color="tab:red", lw=1.2, label="Optical Acceleration (scaled) — pre")
ax1_twin.plot(opt_post["date"], opt_post["accel_proxy"],
              color="tab:red", lw=1.6, linestyle="--", marker="s", ms=3,
              label="Optical Acceleration (scaled) — post")

# Shaded windows
ax1.axvspan(window_start, window_end, color="cyan", alpha=0.12, label="Pre-perihelion accel window")
ax1.axvspan(perihelion, perihelion + pd.Timedelta(days=POST_DAYS),
            color="orange", alpha=0.08, label=f"Post-perihelion (+{POST_DAYS} d)")

# Perihelion marker
ax1.axvline(perihelion, color="magenta", linestyle="--", lw=1)
ax1.text(perihelion + pd.Timedelta(days=1), ax1.get_ylim()[0]+0.02*(ax1.get_ylim()[1]-ax1.get_ylim()[0]),
         "Perihelion\n2025-10-29", color="magenta", fontsize=8)

# Format x-axis
ax1.xaxis.set_major_formatter(DateFormatter("%b-%d"))
for tick in ax1.get_xticklabels():
    tick.set_rotation(30); tick.set_ha("right")

# Merge legends from both axes
l1, t1 = ax1.get_legend_handles_labels()
l2, t2 = ax1_twin.get_legend_handles_labels()
ax1.legend(l1 + l2, t1 + t2, loc="upper left", fontsize=8)
ax1.set_title("Optical Activity Timeline")
ax1.set_ylabel("Relative Brightness (1/mag)", color="tab:blue")
ax1_twin.set_ylabel("Scaled Optical Acceleration", color="tab:red")

# ------------------------------------------------------------
# RIGHT PANEL — Color Evolution (show truth clearly)
# ------------------------------------------------------------
# Show ALL g-o data since r-o is from different epoch
# Use g-o as primary color tracer post-perihelion
color_go = color[color["pair"] == "g-o"].sort_values("date")
go_pre, go_post = split_pre_post(color_go, "date", perihelion)

# Plot pre vs post with different styles
ax2.plot(go_pre["date"], go_pre["color_smooth"], "-o", color="green", lw=1.2, ms=3, label="g–o (pre)")
ax2.plot(go_post["date"], go_post["color_smooth"], "--o", color="green", lw=1.8, ms=4, label="g–o (post)")

# Windows + perihelion
ax2.axvspan(window_start, window_end, color="cyan", alpha=0.12, label="Pre-perihelion accel window")
ax2.axvspan(perihelion, perihelion + pd.Timedelta(days=POST_DAYS),
            color="orange", alpha=0.08, label=f"Post-perihelion (+{POST_DAYS} d)")
ax2.axvline(perihelion, color="magenta", linestyle="--", lw=1)

# Annotate last few post-perihelion points
annotate_last(ax2, go_post, "date", "color_smooth")

# Optional: solar reference line
solar_go = 0.620
ax2.axhline(solar_go, color="gray", ls=":", alpha=0.7)
ax2.text(ax2.get_xlim()[1], solar_go, "☉ g–o = 0.62", va="center", ha="right", fontsize=8, color="gray")

# Cosmetics
ax2.set_xlabel("Date (UTC, 2025)")
ax2.set_ylabel("g–o Color Index (mag)")
ax2.set_title("Chromatic Evolution (pre vs post)")
ax2.legend(fontsize=8)
ax2.grid(alpha=0.3)
ax2.xaxis.set_major_formatter(DateFormatter("%b-%d"))
for tick in ax2.get_xticklabels():
    tick.set_rotation(30); tick.set_ha("right")

# --- Fix overlapping x-axis dates ---
for ax in [ax1, ax2]:
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right", fontsize=8)
    ax.xaxis.set_major_formatter(
        plt.matplotlib.dates.DateFormatter("%b-%d")
    )

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

# ===== Console: post-perihelion deltas =====
if not opt_post.empty:
    # nearest post-perihelion day
    peri_row = opt.iloc[(opt["date"] - perihelion).abs().values.argmin()]
    last_row = opt_post.iloc[-1]
    dm = (1/last_row["inv_mag_smooth"]) - (1/peri_row["inv_mag_smooth"])
    # Convert 1/mag back to mag for an intuitive delta estimate
    print("\n=== Post-perihelion quick summary ===")
    print(f"Perihelion (nearest) date: {peri_row['date']:%Y-%m-%d}, proxy mag≈{1/peri_row['inv_mag_smooth']:.2f}")
    print(f"Latest date:               {last_row['date']:%Y-%m-%d}, proxy mag≈{1/last_row['inv_mag_smooth']:.2f}")
    print(f"Δmag (latest - peri):      {dm:+.2f}  (positive = fainter)")
if not go_post.empty and len(go_post) >= 2:
    dcolor = go_post["color_smooth"].iloc[-1] - go_post["color_smooth"].iloc[0]
    print(f"Δ(g–o) post window:        {dcolor:+.2f} mag  (positive = reddening)")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("I3_Optical_Color_Correlation_postperi.png", dpi=250)
print("✅ Saved: I3_Optical_Color_Correlation_postperi.png")
