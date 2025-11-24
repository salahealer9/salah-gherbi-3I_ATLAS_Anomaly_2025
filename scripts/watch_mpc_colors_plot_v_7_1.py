#!/usr/bin/env python3
"""
watch_mpc_colors_plot_v7.py
3I/ATLAS (C/2019 Y4) — Full MPC Color Evolution + Solar Comparison + Perihelion Test
Author: Salah-Eddin Gherbi
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import re
from datetime import datetime

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
# Main plotting and analysis
# ------------------------------------------------------------
def plot_colors(df):
    log_lines = []
    plt.figure(figsize=(9, 5))
    for pair in df["pair"].unique():
        sub = df[df["pair"] == pair].sort_values("date")
        plt.plot(sub["date"], sub["color"], "o-", label=pair)

    xmax = df["date"].max() + pd.Timedelta(days=5)
    for pair, solar_val in SOLAR_COLORS.items():
        plt.axhline(solar_val, color="red", linestyle=":", alpha=0.6)
        plt.text(xmax, solar_val, f"☉ {pair}={solar_val:.2f}", color="red",
                 fontsize=8, va="center", ha="left", backgroundcolor="white")

    events = {
        "Solar Conjunction\n(behind Sun)": ("2025-10-21", "deepskyblue"),
        "Perihelion\n(q=0.81 AU)": ("2025-10-29", "gold"),
        "Earth Close Approach\n(~0.56 AU)": ("2025-12-19", "limegreen"),
    }
    ymin, ymax = plt.ylim()
    for label, (date_str, color) in events.items():
        d = pd.Timestamp(date_str, tz="UTC")
        plt.axvline(d, color=color, ls="--", lw=1.2)
        plt.text(d + pd.Timedelta(days=1), ymax * 0.9, label, rotation=90,
                 va="top", ha="left", fontsize=8, color=color)

    plt.ylabel("Color Index (mag)")
    plt.xlabel("Date (UTC, 2025)")
    plt.title("3I/ATLAS — Color Evolution vs Solar Baseline & Key Events")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("I3_Color_Trend_v7.png", dpi=200)
    print("✅ Saved: I3_Color_Trend_v7.png")
    log_lines.append("✅ Saved: I3_Color_Trend_v7.png")

    # --- Solar comparison ---
    print("\n📊 === Solar Comparison Summary ===")
    log_lines.append("\n📊 === Solar Comparison Summary ===")
    for pair in df["pair"].unique():
        if pair not in SOLAR_COLORS:
            continue
        pair_data = df[df["pair"] == pair]["color"].dropna()
        if len(pair_data) < 3:
            continue
        solar_val = SOLAR_COLORS[pair]
        mean_color = pair_data.mean()
        std_color = pair_data.std()
        diff = mean_color - solar_val
        sigma = abs(diff) / std_color if std_color > 0 else np.nan
        trend = "BLUER" if diff < 0 else "REDDER"
        line = f"{pair:>4}: Mean={mean_color:.3f} ± {std_color:.3f} | Solar={solar_val:.3f}\n     Δ={diff:+.3f} ({sigma:.1f}σ) → {trend}"
        print(line)
        log_lines.append(line)

    # --- Individual per-pair evolution plots ---
    print("\n🎨 Generating per-color evolution plots...")
    log_lines.append("\n🎨 Generating per-color evolution plots...")
    for pair in df["pair"].unique():
        if pair not in SOLAR_COLORS:
            continue
        sub = df[df["pair"] == pair].sort_values("date")
        if len(sub) < 3:
            print(f"⚠️  Skipping {pair}: only {len(sub)} points")
            log_lines.append(f"⚠️  Skipping {pair}: only {len(sub)} points")
            continue
        plt.figure(figsize=(8, 4))
        plt.plot(sub["date"], sub["color"], "o-", color="steelblue", label=f"{pair} data")
        plt.axhline(SOLAR_COLORS[pair], color="red", ls="--",
                    label=f"Solar {pair}={SOLAR_COLORS[pair]:.2f}")
        plt.title(f"3I/ATLAS {pair.upper()} Color Evolution ({sub['date'].min().date()}→{sub['date'].max().date()})")
        plt.ylabel(f"{pair.upper()} (mag)")
        plt.xlabel("Date (UTC)")
        plt.grid(alpha=0.3)
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"I3_{pair}_evolution.png", dpi=150)
        plt.close()
        print(f"✅ Saved: I3_{pair}_evolution.png")
        log_lines.append(f"✅ Saved: I3_{pair}_evolution.png")

    # --- Perihelion r-o shift test ---
    r_o_data = df[df["pair"] == "r-o"].sort_values("date")
    if len(r_o_data) > 3:
        pre = r_o_data[r_o_data["date"] < PERIHELION]["color"]
        post = r_o_data[r_o_data["date"] >= PERIHELION]["color"]
        if len(pre) and len(post):
            pre_mean = pre.mean(); post_mean = post.mean()
            delta = post_mean - pre_mean
            trend = "BLUER" if delta < 0 else "REDDER"
            print("\n🔬 Perihelion Color Shift (r–o):")
            print(f"   Before perihelion: {pre_mean:.3f}")
            print(f"   After  perihelion: {post_mean:.3f}")
            print(f"   Δ (post - pre) = {delta:+.3f} mag → {trend}")
            log_lines += [
                "\n🔬 Perihelion Color Shift (r–o):",
                f"   Before perihelion: {pre_mean:.3f}",
                f"   After  perihelion:  {post_mean:.3f}",
                f"   Δ (post - pre) = {delta:+.3f} mag → {trend}"
            ]
        else:
            print("⚠️  Insufficient r–o data around perihelion.")
            log_lines.append("⚠️  Insufficient r–o data around perihelion.")
    else:
        print("⚠️  Not enough r–o data for perihelion comparison.")
        log_lines.append("⚠️  Not enough r–o data for perihelion comparison.")

    # --- Write log file ---
    log_path = Path("I3_Color_Statistics.txt")
    log_path.write_text("\n".join(log_lines))
    print(f"\n🗒️  Summary exported to: {log_path}")

# ------------------------------------------------------------
# Run
# ------------------------------------------------------------
if __name__ == "__main__":
    df = parse_mpc("I3.txt")
    df = df[(df["date"] >= "2025-07-01") & (df["date"] <= "2025-12-31")]
    pairs = build_pairs(df, window_days=1)
    if pairs.empty:
        print("⚠️ No color pairs found.")
        exit()
    out = Path("I3_Color_Alerts.csv")
    if out.exists():
        prev = pd.read_csv(out)
        if "date_center" in prev.columns:
            prev = prev.rename(columns={"date_center": "date"})
        prev["date"] = pd.to_datetime(prev["date"])
        combined = pd.concat([prev, pairs]).drop_duplicates(subset=["date", "pair", "color"])
    else:
        combined = pairs
    combined.to_csv(out, index=False)
    print(f"✅ Updated {out} with {len(pairs)} pairs.")
    plot_colors(combined)
