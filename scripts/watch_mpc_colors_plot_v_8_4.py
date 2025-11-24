#!/usr/bin/env python3
"""
watch_mpc_colors_plot_v8_4.py
3I/ATLAS (C/2019 Y4) — MPC Color Evolution + Brightness Timeline
with Solar Baselines, Perihelion Marker, and Blockchain Proof Manifest.

This version merges the scientific richness of v7.9
(color evolution + brightness overlays)
with the archival and cryptographic rigor of v8.3.

Author: Salah-Eddin Gherbi
ORCID: https://orcid.org/0009-0005-4017-1095
Repository: https://github.com/salahealer9/salah-gherbi-3I_ATLAS_Anomaly_2025
Zenodo DOI: (pending — to be minted after verification)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
import re, hashlib
from datetime import datetime, timezone

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
FILTERS = ["g", "r", "o", "v", "c"]
COLORS = {"g": "green", "r": "red", "o": "orange", "v": "purple", "c": "gray"}
COMBOS = [("g", "r"), ("g", "o"), ("r", "o")]
SOLAR_COLORS = {"g-r": 0.44, "g-o": 0.62, "r-o": 0.18}
PERIHELION = pd.Timestamp("2025-10-29", tz="UTC")

VERSION = "v8.4"
ORCID = "https://orcid.org/0009-0005-4017-1095"
REPO = "https://github.com/salahealer9/salah-gherbi-3I_ATLAS_Anomaly_2025"
ZENODO_DOI = "pending — to be minted after verification"

# ------------------------------------------------------------
# Utilities
# ------------------------------------------------------------
def utc_tag():
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

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
# Analysis + Proof
# ------------------------------------------------------------
def analyze_color_differences(pairs, perihelion, source_file, tag):
    stats = []
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    sha256_in = sha256sum(source_file) if Path(source_file).exists() else "N/A"

    header = [
        f"### 3I/ATLAS (C/2019 Y4) Color Statistics — {VERSION}",
        f"Generated: {timestamp}",
        f"UTC Tag: {tag}",
        f"Source: {source_file}",
        f"SHA-256: {sha256_in}",
        f"Perihelion: {perihelion.date()}",
        f"Author: Salah-Eddin Gherbi",
        f"ORCID: {ORCID}",
        f"Repository: {REPO}",
        f"Zenodo DOI: {ZENODO_DOI}",
        "------------------------------------------------------------",
        "pair\tmean_pre\tmean_post\tdelta\tsigma\ttrend"
    ]

    print("\n📊 === Pre/Post-Perihelion Color Summary ===")
    for pair in pairs["pair"].unique():
        sub = pairs[pairs["pair"] == pair]
        pre = sub[sub["date"] < perihelion]["color"]
        post = sub[sub["date"] > perihelion]["color"]
        mean_pre, mean_post = pre.mean(), post.mean()
        std_pre, std_post = pre.std(), post.std()

        if pre.empty or post.empty:
            print(f"⚠️ {pair}: Missing {'pre' if pre.empty else 'post'}-perihelion data.")
            stats.append((pair, mean_pre, mean_post, np.nan, np.nan, "insufficient"))
            continue

        delta = mean_post - mean_pre
        pooled_std = np.sqrt((std_pre**2 + std_post**2) / 2)
        sigma = abs(delta / pooled_std) if pooled_std > 0 else np.nan
        trend = "bluer" if delta < 0 else "redder"
        print(f" {pair:>4}: pre={mean_pre:.3f} post={mean_post:.3f} Δ={delta:+.3f} ({sigma:.1f}σ) → {trend}")
        stats.append((pair, mean_pre, mean_post, delta, sigma, trend))

    stats_df = pd.DataFrame(stats, columns=["pair","mean_pre","mean_post","delta","sigma","trend"])
    stats_path = Path(f"I3_Color_Statistics_{tag}.txt")
    with open(stats_path, "w") as f:
        f.write("\n".join(header) + "\n")
        stats_df.to_csv(f, sep="\t", index=False)
    print(f"🗒️ Saved: {stats_path}")
    return stats_df, stats_path, sha256_in

# ------------------------------------------------------------
# Plot (dual-panel: color + brightness)
# ------------------------------------------------------------
def plot_colors_and_brightness(pairs, df, tag):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7), sharex=True,
                                   gridspec_kw={'height_ratios':[3,2]})
    # --- COLOR EVOLUTION ---
    for pair in pairs["pair"].unique():
        sub = pairs[pairs["pair"] == pair].sort_values("date")
        ax1.plot(sub["date"], sub["color"], "o-", label=pair)

    xmax = pairs["date"].max() + pd.Timedelta(days=5)
    for pair, solar_val in SOLAR_COLORS.items():
        ax1.axhline(solar_val, color="red", linestyle=":", alpha=0.6)
        ax1.text(xmax, solar_val, f"☉ {pair}={solar_val:.2f}", color="red",
                 fontsize=8, va="center", ha="left", backgroundcolor="white")

    ax1.axvline(PERIHELION, color="magenta", linestyle="--", linewidth=1.2)
    ax1.text(PERIHELION + pd.Timedelta(days=2), ax1.get_ylim()[0],
             "Perihelion (Oct 29)", color="magenta", fontsize=8, va="bottom")
    ax1.set_ylabel("Color Index (mag)")
    ax1.set_title(f"3I/ATLAS — Color & Brightness Evolution ({VERSION}, {tag})")
    ax1.grid(alpha=0.3)
    ax1.legend()

    # --- BRIGHTNESS TIMELINE ---
    for f in ["g","r","o"]:
        sub = df[df["filter"] == f].groupby("night")["mag"].mean().reset_index()
        if not sub.empty:
            ax2.plot(sub["night"], sub["mag"], "o-", color=COLORS[f], label=f"{f}-band")
    ax2.axvline(PERIHELION, color="magenta", linestyle="--", linewidth=1.0)
    ax2.set_ylabel("Mean Brightness (mag)")
    ax2.invert_yaxis()
    ax2.grid(alpha=0.3)
    ax2.legend()

    # --- X-axis formatting ---
    locator = mdates.AutoDateLocator(maxticks=8)
    ax2.xaxis.set_major_locator(locator)
    ax2.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    plt.setp(ax2.get_xticklabels(), rotation=30, ha="right")

    plt.tight_layout()
    plot_path = f"I3_Color_Brightness_Timeline_{tag}.png"
    plt.savefig(plot_path, dpi=300)
    plt.close(fig)
    print(f"✅ Saved: {plot_path}")
    return plot_path

# ------------------------------------------------------------
# Proof Manifest
# ------------------------------------------------------------
def write_proof_manifest(source_file, sha_in, stats_file, pairs_file, plot_file, tag):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    manifest = Path(f"I3_Color_Proof_{tag}.txt")
    with open(manifest, "w") as f:
        f.write("### 3I/ATLAS (C/2019 Y4) — Color Analysis Proof Manifest\n")
        f.write(f"Version: {VERSION}\nGenerated: {timestamp}\nUTC Tag: {tag}\n")
        f.write(f"Author: Salah-Eddin Gherbi\nORCID: {ORCID}\nRepository: {REPO}\n")
        f.write(f"Zenodo DOI: {ZENODO_DOI}\nPrimary Input: {source_file}\n")
        f.write(f"SHA-256 (I3.txt): {sha_in}\n\n")
        for file in [stats_file, pairs_file, plot_file]:
            if Path(file).exists():
                f.write(f"{file}\t{sha256sum(file)}\n")
        f.write("\nTo verify integrity:\n")
        f.write(f" ots stamp I3_Color_Proof_{tag}.txt\n ots verify I3_Color_Proof_{tag}.txt.ots\n")
    print(f"🔏 Proof manifest created: I3_Color_Proof_{tag}.txt")

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
if __name__ == "__main__":
    tag = utc_tag()
    src = "I3.txt"
    df = parse_mpc(src)
    df = df[(df["date"] >= "2025-07-01") & (df["date"] <= "2025-12-31")]

    pairs = build_pairs(df, window_days=1)
    pairs_path = f"I3_Color_Alerts_{tag}.csv"
    pairs.to_csv(pairs_path, index=False)
    print(f"✅ Saved {len(pairs)} color pairs → {pairs_path}")

    stats, stats_path, sha_in = analyze_color_differences(pairs, PERIHELION, src, tag)
    plot_path = plot_colors_and_brightness(pairs, df, tag)
    write_proof_manifest(src, sha_in, stats_path, pairs_path, plot_path, tag)
