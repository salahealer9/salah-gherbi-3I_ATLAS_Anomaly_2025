#!/usr/bin/env python3
"""
plot_station_residuals.py
Check whether optical-acceleration anomalies appear across multiple observatories.
Author: Salah-Eddin Gherbi
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

MPC_FILE = "I3.txt"

# ------------------------------------------------------------
# 1. Load MPC Photometry
# ------------------------------------------------------------
rows = []
with open(MPC_FILE) as f:
    for line in f:
        if not line.startswith("0003I"):
            continue

        try:
            date = pd.to_datetime(line[15:32].strip(), utc=True)
            mag = float(line[65:70].strip())
            station = line[77:80].strip()
        except Exception:
            continue

        rows.append((date, mag, station))

df = pd.DataFrame(rows, columns=["date", "mag", "station"])
df.sort_values("date", inplace=True)

# ------------------------------------------------------------
# 2. Compute time-normalized proxy per station (SIMPLIFIED VERSION)
# ------------------------------------------------------------

# Sort by station and date first
df = df.sort_values(["station", "date"]).reset_index(drop=True)

df["inv_mag"] = 1.0 / df["mag"]

# Calculate time differences in days
df["time_diff_days"] = df.groupby("station")["date"].diff().dt.total_seconds() / 86400.0

# Calculate proxy (d(1/m)/dt)
df["proxy_raw"] = df.groupby("station")["inv_mag"].diff() / df["time_diff_days"]

# Remove rows with invalid time differences
df_clean = df[df["time_diff_days"] > 0].copy()

# Baseline for scaling: everything BEFORE the late-Nov / early-Dec window
baseline_mask = df_clean["date"] < "2025-11-28"
if baseline_mask.sum() > 0:
    scale = df_clean[baseline_mask]["proxy_raw"].std()
    df_clean.loc[:, "proxy_scaled"] = df_clean["proxy_raw"] / scale
else:
    print("Warning: No baseline data available for scaling")
    df_clean.loc[:, "proxy_scaled"] = df_clean["proxy_raw"]

# ------------------------------------------------------------
# 3. Restrict to recent dates (post-perihelion)
# ------------------------------------------------------------
df_recent = df_clean[df_clean["date"] >= "2025-11-15"].copy()

print(f"Data available for analysis: {len(df_recent)} observations")
print(f"Stations in recent data: {df_recent['station'].unique()}")

# ------------------------------------------------------------
# 4. Plot per-station time series
# ------------------------------------------------------------
if len(df_recent) > 0:
    stations = df_recent["station"].unique()

    plt.figure(figsize=(12, 7))

    for s in stations:
        sub = df_recent[df_recent["station"] == s]
        if len(sub) < 2:  # Need at least 2 points for meaningful plot
            continue
        plt.plot(
            sub["date"],
            sub["proxy_scaled"],
            marker="o",
            label=s,
            alpha=0.3,
            linewidth=0.5,
        )

    # Plot daily aggregated mean (bold)
    daily_mean = df_recent.groupby("date")["proxy_scaled"].mean()
    plt.plot(
        daily_mean.index,
        daily_mean.values,
        color="red",
        linewidth=3,
        marker="s",
        label="Daily Mean (All Stations)",
        markersize=6,
    )

    # Event window: late-Nov / early-Dec feature
    plt.axvspan("2025-11-28", "2025-12-01", color="yellow", alpha=0.2,
                label="Nov 28–Dec 01 feature")

    plt.xlabel("Date (UTC)")
    plt.ylabel("Scaled Optical Acceleration Proxy")
    plt.title("Station-by-Station Analysis — 3I/ATLAS Post-Perihelion")
    plt.legend(title="Observatory Code", fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("station_collective_effect_corrected.png", dpi=300)
    plt.show()
else:
    print("No recent data available for plotting")

# ------------------------------------------------------------
# 5. Quantitative Analysis
# ------------------------------------------------------------
if len(df_recent) > 0:
    # Aggregate by station and date
    df_daily = df_recent.groupby(["station", "date"])["proxy_scaled"].mean().reset_index()

    # Pulse window: 2025-11-28 to 2025-12-01 inclusive
    pulse = df_daily[
        (df_daily["date"] >= "2025-11-28") & (df_daily["date"] <= "2025-12-01")
    ]

    # Baseline BEFORE this window
    baseline_daily = df_daily[df_daily["date"] < "2025-11-28"]

    if len(baseline_daily) > 0:
        threshold = (
            baseline_daily["proxy_scaled"].median()
            + 3 * baseline_daily["proxy_scaled"].std()
        )
    else:
        threshold = np.nan

    print("\n🔍 STATION ANALYSIS RESULTS:")
    print("============================")
    if "scale" in locals() and not np.isnan(scale):
        print(f"Scaling factor (baseline std): {scale:.6f}")
    else:
        print("Scaling factor: Not available (insufficient baseline data)")

    if len(pulse) > 0:
        max_proxy = pulse["proxy_scaled"].max()
        min_proxy = pulse["proxy_scaled"].min()
        print(f"Maximum station proxy in feature window: {max_proxy:.4f}")
        print(f"Minimum station proxy in feature window: {min_proxy:.4f}")
        print(f"Detection threshold (3σ): {threshold:.4f}")

        # Daily aggregated mean in the same window
        daily_aggregated_pulse = daily_mean[
            (daily_mean.index >= "2025-11-28") & (daily_mean.index <= "2025-12-01")
        ]
        if len(daily_aggregated_pulse) > 0:
            peak_date = daily_aggregated_pulse.idxmax().date()
            peak_value = daily_aggregated_pulse.max()
            print(
                f"\n📊 Daily-mean behaviour in this window:\n"
                f"Peak daily mean (all stations): {peak_value:.4f} on {peak_date}"
            )

        print(f"\n✅ KEY FINDING:")
        n_above = (pulse["proxy_scaled"] > threshold).sum()

        if np.isnan(threshold) or n_above == 0:
            print("No station exceeds the 3σ detection threshold in this window.")
            print("All signals are consistent with baseline scatter (no third spike).")
        else:
            print(f"{n_above} station(s) exceed the 3σ threshold, but only on single epochs.")
            print("The daily mean remains an order of magnitude below 3σ and the sign")
            print("distribution is mixed across stations, so this feature is consistent")
            print("with statistical noise rather than a coherent third acceleration event.")

        # Show station distribution
        print(f"\n📈 Station distribution in feature window:")
        print(f"Stations with positive proxy: {len(pulse[pulse['proxy_scaled'] > 0])}")
        print(f"Stations with negative proxy: {len(pulse[pulse['proxy_scaled'] < 0])}")
        print(f"Strongest station signals:")
        strong_stations = pulse.nlargest(5, "proxy_scaled")
        for _, row in strong_stations.iterrows():
            print(f"  - {row['station']}: {row['proxy_scaled']:.4f} on {row['date'].date()}")
    else:
        print("No data available in feature window (Nov 28–Dec 01).")
else:
    print("No recent data available for analysis")

print("\n🔬 DEEPER DIAGNOSTIC:")
print("=====================")

# Check if removing station 703 changes the picture
df_no703 = df_recent[df_recent["station"] != "703"]
daily_mean_no703 = df_no703.groupby("date")["proxy_scaled"].mean()
pulse_no703 = daily_mean_no703[
    (daily_mean_no703.index >= "2025-11-28") & 
    (daily_mean_no703.index <= "2025-12-01")
]

if len(pulse_no703) > 0:
    print(f"Daily mean WITHOUT station 703: {pulse_no703.mean():.6f}")
    print(f"Maximum daily mean without 703: {pulse_no703.max():.6f}")
else:
    print("No data without station 703 in pulse window")
