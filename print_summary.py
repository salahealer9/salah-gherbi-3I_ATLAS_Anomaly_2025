#!/usr/bin/env python3
"""
3I/ATLAS (C/2019 Y4) – Automated Photometric Summary
Parses I3.txt directly, extracts magnitudes and dates,
groups by month, and prints statistical summary + sample.
"""

import re
import pandas as pd
from datetime import datetime

def parse_i3_txt(filename="I3.txt"):
    """Parse MPC-format I3.txt into DataFrame (date, ra, dec, mag)."""
    pattern = re.compile(
        r"0003I\s+[A-Za-z0-9]+\s+(\d{4}) (\d{2}) (\d{2})\.(\d+)"
        r"\s+([0-9\s\.]+)([+-][0-9\s\.]+)\s+([0-9\.]+)"
    )
    rows = []
    with open(filename) as f:
        for line in f:
            if line.startswith("0003I"):
                parts = re.findall(r"(\d{4}) (\d{2}) (\d{2})\.(\d+)", line)
                if not parts:
                    continue
                y, m, d, frac = parts[0]
                frac_day = float("0." + frac)
                date = datetime.strptime(f"{y}-{m}-{d}", "%Y-%m-%d") \
                        .replace(hour=int(frac_day * 24),
                                 minute=int((frac_day * 24 * 60) % 60))
                mag_match = re.search(r"\s([0-9]{1,2}\.[0-9])\s+[A-Z]", line)
                mag = float(mag_match.group(1)) if mag_match else None
                if mag and 5.0 < mag < 25.0:
                   rows.append((date, mag))

    return pd.DataFrame(rows, columns=["date", "mag"])

def summarize(df):
    df["month"] = df["date"].dt.to_period("M")
    summary = df.groupby("month")["mag"].agg(["count","mean","min","max","std"])
    return summary

def print_summary(summary, df):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    print("="*60)
    print(f"3I/ATLAS (C/2019 Y4) — Photometric Anomaly Summary")
    print(f"Generated: {now}")
    print("="*60, "\n")
    print("Monthly Photometric Summary\n")
    print(summary.to_string(float_format=lambda x: f"{x:6.2f}"))
    print("\n--- Phase Comparison ---")
    try:
        july = summary.loc["2025-07"]
        octo = summary.loc["2025-10"]
        delta = july["mean"] - octo["mean"]
        flux = 10 ** (0.4 * delta)
        print(f"Δm = {delta:.2f} mag  →  flux increase ×{flux:.1f}")
    except KeyError:
        print("Not all months found for comparison.")
    print("\nSample observations:")
    print(df.head(5).to_string(index=False))
    print("\nVerification (OpenTimestamps):")
    print("File: anomaly_manifest_20251029_1648.ots")
    print("Run: ots verify anomaly_manifest_20251029_1648.ots")
    print("="*60)

def main():
    df = parse_i3_txt()
    if df.empty:
        print("No valid observations found in I3.txt.")
        return

    summary = summarize(df)
    print_summary(summary, df)

    # --- Save summary CSV ---
    summary.to_csv("I3_monthly_summary.csv")
    print("✅ Saved monthly summary to I3_monthly_summary.csv")

    # --- Generate light-curve plot ---
    import matplotlib.pyplot as plt
    summary["mean"].plot(marker="o", title="3I/ATLAS Monthly Brightness 2025")
    plt.gca().invert_yaxis()  # brighter = lower magnitude
    plt.xlabel("Month")
    plt.ylabel("Mean magnitude (V)")
    plt.tight_layout()
    plt.savefig("I3_lightcurve.png", dpi=200)
    print("✅ Saved plot to I3_lightcurve.png")



if __name__ == "__main__":
    main()
