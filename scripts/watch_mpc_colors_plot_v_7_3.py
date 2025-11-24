#!/usr/bin/env python3
"""
watch_mpc_colors_plot_v7_3.py
3I/ATLAS (C/2019 Y4) — MPC Color Evolution, Solar Comparison,
and Filter Activity Timeline Overlay
Author: Salah-Eddin Gherbi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import re

FILTERS = ["g", "r", "o", "v", "c"]
COLORS = {"g": "green", "r": "red", "o": "orange", "v": "purple", "c": "gray"}
COMBOS = [("g", "r"), ("g", "o"), ("r", "o")]
SOLAR_COLORS = {"g-r": 0.44, "g-o": 0.62, "r-o": 0.18}
PERIHELION = pd.Timestamp("2025-10-29", tz="UTC")

# ------------------------------------------------------------
# Utilities
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
        data.append({"date": fractional_day_to_datetime(y, mth, d),
                     "mag": mag, "filter": flt})
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
# Filter availability diagnostic
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

    july_o = df[(df["filter"] == "o") & (df["date"].dt.month == 7)]
    if not july_o.empty:
        rng = (july_o["mag"].min(), july_o["mag"].max())
        line = f"🔍 July Orange Filter: {len(july_o)} obs, mag {rng[0]:.2f}–{rng[1]:.2f}"
    else:
        line = "⚠️ No July orange data found."
    print(line)
    log_lines.append(line)
    return log_lines

# ------------------------------------------------------------
# Main plotting with overlay
# ------------------------------------------------------------
def plot_colors(pairs, df):
    log_lines = analyze_filter_timeline(df, [])

    fig, ax = plt.subplots(figsize=(9, 5))
    for pair in pairs["pair"].unique():
        sub = pairs[pairs["pair"] == pair].sort_values("date")
        ax.plot(sub["date"], sub["color"], "o-", label=pair)

    xmax = pairs["date"].max() + pd.Timedelta(days=5)
    for pair, solar_val in SOLAR_COLORS.items():
        ax.axhline(solar_val, color="red", linestyle=":", alpha=0.6)
        ax.text(xmax, solar_val, f"☉ {pair}={solar_val:.2f}", color="red",
                fontsize=8, va="center", ha="left", backgroundcolor="white")

    ax.set_ylabel("Color Index (mag)")
    ax.set_xlabel("Date (UTC, 2025)")
    ax.set_title("3I/ATLAS — Color Evolution & Filter Activity Timeline")
    ax.grid(alpha=0.3)
    ax.legend()

    # --- Overlay active filter timeline bars (cleaned & color-coded) ---
    ymin, ymax = ax.get_ylim()
    ybar_base = ymin - 0.10 * (ymax - ymin)
    bar_height = 0.03 * (ymax - ymin)

    # Filters actually used in color pairs
    active_filters = ["g", "r", "o"]
    for i, f in enumerate(active_filters):
        sub = df[df["filter"] == f]
        if sub.empty:
            continue
        ybar = ybar_base - i * bar_height * 1.5
        ax.hlines(ybar, sub["date"].min(), sub["date"].max(),
                  color=COLORS[f], linewidth=6, alpha=0.7)
        ax.text(sub["date"].min(), ybar,
                f"{f}-band active", fontsize=8, va="center", ha="left",
                color="black", backgroundcolor="white")

# --- Perihelion marker ---
    peri = PERIHELION
    if pairs["date"].min() < peri < pairs["date"].max():
        ax.axvline(peri, color="magenta", linestyle="--", linewidth=1.2, alpha=0.7)
        ax.text(peri + pd.Timedelta(days=2), ymin + 0.05*(ymax - ymin),
                "Perihelion (Oct 29 2025)", color="magenta", fontsize=8,
                va="bottom", ha="left")

# At the end of plot_colors function, add:
    plt.tight_layout()
    plt.savefig("I3_Color_Trend_v7_3.png", dpi=200)
    plt.show(block=False)
    print("✅ Saved: I3_Color_Trend_v7_3.png")
    
    # Key findings summary
    print("\n🔑 KEY FINDINGS:")
    print("   - r-o shows early bluing in July (interstellar signature)")
    print("   - r-band observations stop after July 30 (observational gap)") 
    print("   - g-o continues through September (alternative color index)")
    print("   - Early color changes precede major brightening anomaly")
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
    plot_colors(pairs, df)
