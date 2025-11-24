#!/usr/bin/env python3
"""
watch_mpc_colors_plot_v7_5.py
3I/ATLAS (C/2019 Y4) — MPC Color Evolution + Dual-Axis Brightness Timeline
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
# Utility: MPC parsing
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
# Main plotting (color + dual-axis brightness)
# ------------------------------------------------------------
def plot_colors_and_brightness(pairs, df):
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(9, 6), sharex=True,
        gridspec_kw={"height_ratios": [3, 1.2]}
    )

    # ---------------------- COLOR PANEL ----------------------
    for pair in pairs["pair"].unique():
        sub = pairs[pairs["pair"] == pair].sort_values("date")
        ax1.plot(sub["date"], sub["color"], "o-", label=pair)

    xmax = pairs["date"].max() + pd.Timedelta(days=5)
    for pair, solar_val in SOLAR_COLORS.items():
        ax1.axhline(solar_val, color="red", linestyle=":", alpha=0.6)
        ax1.text(xmax, solar_val, f"☉ {pair}={solar_val:.2f}", color="red",
                 fontsize=8, va="center", ha="left", backgroundcolor="white")

    ax1.set_ylabel("Color Index (mag)")
    ax1.set_title("3I/ATLAS — Color Evolution and Brightness Timeline")
    ax1.grid(alpha=0.3)
    ax1.legend()

    # --- Filter activity bars ---
    ymin, ymax = ax1.get_ylim()
    ybar_base = ymin - 0.10 * (ymax - ymin)
    bar_height = 0.03 * (ymax - ymin)
    active_filters = ["g", "r", "o"]
    for i, f in enumerate(active_filters):
        sub = df[df["filter"] == f]
        if sub.empty:
            continue
        ybar = ybar_base - i * bar_height * 1.5
        ax1.hlines(ybar, sub["date"].min(), sub["date"].max(),
                   color=COLORS[f], linewidth=6, alpha=0.7)
        ax1.text(sub["date"].min(), ybar, f"{f}-band active",
                 fontsize=8, va="center", ha="left",
                 color="black", backgroundcolor="white")

    # --- Perihelion marker on both panels ---
    peri = PERIHELION
    for ax in (ax1, ax2):
        ax.axvline(peri, color="magenta", linestyle="--", linewidth=1.2, alpha=0.7)
        ax.text(peri + pd.Timedelta(days=2),
                ax.get_ylim()[0] + 0.05 * (ax.get_ylim()[1] - ax.get_ylim()[0]),
                "Perihelion (Oct 29)", color="magenta", fontsize=8,
                va="bottom", ha="left")

    # ------------------- BRIGHTNESS PANEL --------------------
    g_data = df[df["filter"] == "g"].groupby("night")["mag"].median().reset_index()
    if not g_data.empty:
        g_data["flux_rel"] = 10 ** (-0.4 * (g_data["mag"] - g_data["mag"].min()))
        ax2.plot(g_data["night"], g_data["flux_rel"], "o-", color="green", label="g-band flux")
        ax2.set_ylabel("Rel. Flux (g)")
        ax2.grid(alpha=0.3)

        # --- Secondary y-axis for magnitude ---
        ax2b = ax2.twinx()
        ax2b.plot(g_data["night"], g_data["mag"], color="gray", alpha=0.4)
        ax2b.invert_yaxis()
        ax2b.set_ylabel("Apparent g (mag)", color="gray")
        ax2b.tick_params(axis="y", labelcolor="gray")

    ax2.set_xlabel("Date (UTC, 2025)")
    ax2.legend(loc="upper left")

    plt.tight_layout()
    plt.savefig("I3_Color_Trend_v7_5.png", dpi=300)
    plt.close(fig)
    print("✅ Saved: I3_Color_Trend_v7_5.png")


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
    plot_colors_and_brightness(pairs, df)
