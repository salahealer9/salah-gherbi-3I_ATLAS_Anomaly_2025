#!/usr/bin/env python3
"""
watch_mpc_colors_plot_v7_2.py
3I/ATLAS (C/2019 Y4) — MPC Color Evolution, Solar Comparison, and Filter Availability Timeline
Author: Salah-Eddin Gherbi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import re

FILTERS = ["g", "r", "o", "v", "c"]
COMBOS = [("g", "r"), ("g", "o"), ("r", "o")]
SOLAR_COLORS = {"g-r": 0.44, "g-o": 0.62, "r-o": 0.18}
PERIHELION = pd.Timestamp("2025-10-29", tz="UTC")

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def fractional_day_to_datetime(year, month, day_frac):
    day_int = int(day_frac)
    frac = day_frac - day_int
    base = pd.Timestamp(f"{year}-{month:02d}-{day_int:02d}", tz="UTC")
    return base + pd.to_timedelta(frac * 24, unit="h")

def parse_mpc(path="I3.txt"):
    lines = Path(path).read_text().splitlines()
    data = []
    for line in lines:
        if not line.startswith("0003I") or not re.search(r"C2025", line):
            continue
        m = re.search(r"C(2025)\s(\d{2})\s(\d{2}\.\d+)", line)
        if not m:
            continue
        y, mth, d = int(m[1]), int(m[2]), float(m[3])
        magm = re.search(r"(\d{2}\.\d{2})([A-Za-z])", line)
        if not magm:
            continue
        mag = float(magm[1])
        flt = magm[2].lower()
        data.append({
            "date": fractional_day_to_datetime(y, mth, d),
            "mag": mag,
            "filter": flt
        })
    df = pd.DataFrame(data)
    df["night"] = df["date"].dt.floor("D")
    return df

def build_pairs(df, window_days=1):
    tol = pd.Timedelta(days=window_days)
    pairs = []
    for night in df["night"].unique():
        sub = df[(df["night"] >= night - tol) & (df["night"] <= night + tol)]
        for f1, f2 in COMBOS:
            m1 = sub[sub["filter"] == f1]["mag"].mean()
            m2 = sub[sub["filter"] == f2]["mag"].mean()
            if np.isnan(m1) or np.isnan(m2):
                continue
            pairs.append({"date": night, "pair": f"{f1}-{f2}", "color": m1 - m2})
    return pd.DataFrame(pairs)

# ------------------------------------------------------------
# 🔍 New Function — Filter Availability Timeline
# ------------------------------------------------------------
def analyze_filter_timeline(df, log_lines):
    print("\n📅 === FILTER AVAILABILITY TIMELINE ===")
    log_lines.append("\n📅 === FILTER AVAILABILITY TIMELINE ===")

    for f in FILTERS:
        sub = df[df["filter"] == f]
        if not sub.empty:
            d0, d1 = sub["date"].min().date(), sub["date"].max().date()
            line = f"  {f}: {len(sub)} obs from {d0} → {d1}"
        else:
            line = f"  {f}: — none —"
        print(line)
        log_lines.append(line)

    # Optional: Check July orange coverage
    july_o = df[(df["filter"] == "o") & (df["date"].dt.month == 7)]
    if not july_o.empty:
        mag_range = (july_o["mag"].min(), july_o["mag"].max())
        print(f"\n🔍 July Orange Filter: {len(july_o)} obs, mag {mag_range[0]:.2f}–{mag_range[1]:.2f}")
        log_lines.append(f"🔍 July Orange Filter: {len(july_o)} obs, mag {mag_range[0]:.2f}–{mag_range[1]:.2f}")
    else:
        print("\n⚠️ No July orange data found.")
        log_lines.append("⚠️ No July orange data found.")

    return log_lines

# ------------------------------------------------------------
# Plot + Timeline (fixed)
# ------------------------------------------------------------
def plot_colors(pairs, df):
    log_lines = []
    # 🧭 New: run timeline on raw photometry (not pairs)
    log_lines = analyze_filter_timeline(df, log_lines)

    plt.figure(figsize=(9, 5))
    for pair in pairs["pair"].unique():
        sub = pairs[pairs["pair"] == pair].sort_values("date")
        plt.plot(sub["date"], sub["color"], "o-", label=pair)

    xmax = pairs["date"].max() + pd.Timedelta(days=5)
    for pair, solar_val in SOLAR_COLORS.items():
        plt.axhline(solar_val, color="red", linestyle=":", alpha=0.6)
        plt.text(xmax, solar_val, f"☉ {pair}={solar_val:.2f}", color="red",
                 fontsize=8, va="center", ha="left", backgroundcolor="white")

    plt.ylabel("Color Index (mag)")
    plt.xlabel("Date (UTC, 2025)")
    plt.title("3I/ATLAS — Color Evolution & Filter Activity Timeline")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("I3_Color_Trend_v7_2.png", dpi=200)
    print("✅ Saved: I3_Color_Trend_v7_2.png")
    log_lines.append("✅ Saved: I3_Color_Trend_v7_2.png")

    Path("I3_Color_Statistics.txt").write_text("\n".join(log_lines))
    print("🗒️  Updated log with filter diagnostics.")


# ------------------------------------------------------------
# Run
# ------------------------------------------------------------
if __name__ == "__main__":
    df = parse_mpc("I3.txt")
    df = df[(df["date"] >= "2025-07-01") & (df["date"] <= "2025-12-31")]
    pairs = build_pairs(df, window_days=1)
    out = Path("I3_Color_Alerts.csv")
    pairs.to_csv(out, index=False)
    print(f"✅ Saved {len(pairs)} color pairs → {out}")
    # ✅ FIX: pass both pairs and df
    plot_colors(pairs, df)
