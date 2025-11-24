#!/usr/bin/env python3
"""
watch_mpc_colors_plot_v7_9.py
3I/ATLAS (C/2019 Y4) — MPC Color Evolution, Brightness Timeline,
Solar Baselines, Filter Activity, and Pre/Post-Perihelion Δ Analysis.

Includes archival metadata for reproducibility and Zenodo curation.
Author: Salah-Eddin Gherbi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
import re
import hashlib
from datetime import datetime, timezone

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
FILTERS = ["g", "r", "o", "v", "c"]
COLORS = {"g": "green", "r": "red", "o": "orange", "v": "purple", "c": "gray"}
COMBOS = [("g", "r"), ("g", "o"), ("r", "o")]
SOLAR_COLORS = {"g-r": 0.44, "g-o": 0.62, "r-o": 0.18}
PERIHELION = pd.Timestamp("2025-10-29", tz="UTC")

# ------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------
def fractional_day_to_datetime(year, month, day_frac):
    """Convert MPC fractional day to UTC datetime."""
    day_int = int(day_frac)
    frac = day_frac - day_int
    base = pd.Timestamp(f"{year}-{month:02d}-{day_int:02d}", tz="UTC")
    return base + pd.to_timedelta(frac * 24, unit="h")

def file_sha256(path):
    """Compute SHA-256 checksum of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def parse_mpc(path="I3.txt"):
    """Parse MPC photometry for object 3I/ATLAS."""
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
    """Build color pairs within ±window_days."""
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
# Δ Analysis and Statistics
# ------------------------------------------------------------
def analyze_color_differences(pairs, perihelion, source_file):
    """Compute pre/post-perihelion color changes and export with metadata."""
    stats = []
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    sha256sum = file_sha256(source_file) if Path(source_file).exists() else "N/A"

    header_lines = [
        "### 3I/ATLAS (C/2019 Y4) Color Statistics",
        f"Generated: {timestamp}",
        f"Source file: {source_file}",
        f"SHA-256: {sha256sum}",
        f"Perihelion: {perihelion.date()}",
        f"Analyst: Salah-Eddin Gherbi (Quantum Blueprint Project)",
        "------------------------------------------------------------",
        "pair\tmean_pre\tmean_post\tdelta\tsigma\ttrend"
    ]

    print("\n📊 === Pre/Post-Perihelion Color Summary ===")
    for pair in pairs["pair"].unique():
        sub = pairs[pairs["pair"] == pair]
        pre = sub[sub["date"] < perihelion]["color"]
        post = sub[sub["date"] > perihelion]["color"]
        mean_pre = pre.mean()
        mean_post = post.mean()
        std_pre = pre.std()
        std_post = post.std()

        if pre.empty or post.empty:
            print(f"⚠️  {pair}: Missing {'pre' if pre.empty else 'post'}-perihelion data.")
            stats.append((pair, mean_pre, mean_post, np.nan, np.nan, "insufficient"))
            continue

        delta = mean_post - mean_pre
        pooled_std = np.sqrt((std_pre**2 + std_post**2) / 2)
        sigma = abs(delta / pooled_std) if pooled_std > 0 else np.nan
        trend = "bluer" if delta < 0 else "redder"
        print(f" {pair:>4}: pre={mean_pre:.3f} post={mean_post:.3f} Δ={delta:+.3f} ({sigma:.1f}σ) → {trend}")
        stats.append((pair, mean_pre, mean_post, delta, sigma, trend))

    # Save output
    stats_df = pd.DataFrame(stats, columns=["pair", "mean_pre", "mean_post", "delta", "sigma", "trend"])
    outpath = Path("I3_Color_Statistics_v7_9.txt")
    with open(outpath, "w") as f:
        f.write("\n".join(header_lines) + "\n")
        stats_df.to_csv(f, sep="\t", index=False)
    print(f"🗒️  Saved: {outpath}")
    return stats_df

# ------------------------------------------------------------
# Plotting
# ------------------------------------------------------------
def plot_colors_and_brightness(pairs, df, stats):
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(9, 6), sharex=True,
        gridspec_kw={"height_ratios": [3, 1.2]}
    )

    # --- COLOR EVOLUTION ---
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
    for i, f in enumerate(["g", "r", "o"]):
        sub = df[df["filter"] == f]
        if sub.empty:
            continue
        ybar = ybar_base - i * bar_height * 1.5
        ax1.hlines(ybar, sub["date"].min(), sub["date"].max(),
                   color=COLORS[f], linewidth=6, alpha=0.7)
        ax1.text(sub["date"].min(), ybar, f"{f}-band active",
                 fontsize=8, va="center", ha="left",
                 color="black", backgroundcolor="white")

    # --- BRIGHTNESS PANEL ---
    g_data = df[df["filter"] == "g"].groupby("night")["mag"].median().reset_index()
    if not g_data.empty:
        g_data["flux_rel"] = 10 ** (-0.4 * (g_data["mag"] - g_data["mag"].min()))
        ax2.plot(g_data["night"], g_data["flux_rel"], "o-", color="green", label="g-band flux")
        ax2.set_ylabel("Rel. Flux (g)")
        ax2.grid(alpha=0.3)
        ax2b = ax2.twinx()
        ax2b.plot(g_data["night"], g_data["mag"], color="gray", alpha=0.4)
        ax2b.invert_yaxis()
        ax2b.set_ylabel("Apparent g (mag)", color="gray")
        ax2b.tick_params(axis="y", labelcolor="gray")

    ax2.set_xlabel("Date (UTC, 2025)")
    ax2.legend(loc="upper left")

    # --- PERIHELION ---
    peri = PERIHELION
    peri_start, peri_end = peri - pd.Timedelta(days=5), peri + pd.Timedelta(days=5)
    for ax in (ax1, ax2):
        ax.axvline(peri, color="magenta", linestyle="--", linewidth=1.2, alpha=0.7)
        ax.axvspan(peri_start, peri_end, color="magenta", alpha=0.10, zorder=0)
        ax.text(peri + pd.Timedelta(days=2),
                ax.get_ylim()[0] + 0.05 * (ax.get_ylim()[1] - ax.get_ylim()[0]),
                "Perihelion (Oct 29)", color="magenta", fontsize=8,
                va="bottom", ha="left")

    # --- Δ ANNOTATIONS ---
    text_y = ymax - 0.05 * (ymax - ymin)
    for i, row in stats.iterrows():
        if pd.isna(row["delta"]):
            continue
        color = "blue" if row["delta"] < 0 else "darkred"
        label = f"{row['pair']}: Δ={row['delta']:+.3f} ({row['sigma']:.1f}σ) → {row['trend']}"
        ax1.text(peri_end + pd.Timedelta(days=5),
                 text_y - i * 0.05 * (ymax - ymin),
                 label, fontsize=8, color=color, va="center", ha="left")

    # --- X-AXIS ---
    ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax2.xaxis.set_minor_locator(mdates.WeekdayLocator(interval=1))
    for label in ax2.get_xticklabels():
        label.set_rotation(35)
        label.set_ha("right")

    plt.tight_layout(rect=[0, 0.03, 1, 0.98])
    plt.savefig("I3_Color_Trend_v7_9.png", dpi=300)
    plt.close(fig)
    print("✅ Saved: I3_Color_Trend_v7_9.png")

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
if __name__ == "__main__":
    mpc_file = "I3.txt"
    df = parse_mpc(mpc_file)
    df = df[(df["date"] >= "2025-07-01") & (df["date"] <= "2025-12-31")]
    pairs = build_pairs(df, window_days=1)
    pairs.to_csv("I3_Color_Alerts.csv", index=False)
    print(f"✅ Saved {len(pairs)} color pairs → I3_Color_Alerts.csv")

    stats = analyze_color_differences(pairs, PERIHELION, mpc_file)
    plot_colors_and_brightness(pairs, df, stats)
