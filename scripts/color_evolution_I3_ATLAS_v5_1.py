#!/usr/bin/env python3
"""
color_evolution_I3_ATLAS_v5_1.py
Extended version — allows ±1 day tolerance for cross-filter color pairing.
Analyzes September–October 2025 MPC photometry of 3I/ATLAS (C/2019 Y4)
to detect possible post-conjunction blueing.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from datetime import timedelta

# ----------------------------------------------------------
# Step 1 — Parse MPC file
# ----------------------------------------------------------
print("📂 Parsing MPC photometry from I3.txt...")
with open("I3.txt") as f:
    lines = f.readlines()

data = []
for line in lines:
    if not re.match(r"^0003I", line):
        continue
    if not re.search(r"C2025", line):
        continue
    try:
        date_str = re.search(r"C2025\s(\d{2})\s(\d{2}\.\d+)", line)
        if not date_str:
            continue
        month, day = int(date_str.group(1)), float(date_str.group(2))
        mag_match = re.search(r"(\d{2}\.\d{2})([grcVoB])", line)
        if not mag_match:
            continue
        mag = float(mag_match.group(1))
        flt = mag_match.group(2)
        data.append({"month": month, "day": day, "mag": mag, "filter": flt})
    except Exception:
        continue

df = pd.DataFrame(data)
# --- Convert MPC fractional days to proper datetime ---
def fractional_day_to_datetime(month, day_frac):
    """Convert MPC-style day with fractional part (e.g. 09 04.2736) into UTC datetime."""
    day_int = int(day_frac)
    frac = day_frac - day_int
    base_date = pd.Timestamp(f"2025-{month:02d}-{day_int:02d}")
    # fraction of day → hours, minutes, seconds
    return base_date + pd.to_timedelta(frac * 24, unit="h")

df["date_night"] = [
    fractional_day_to_datetime(m, d) for m, d in zip(df["month"], df["day"])
]
df = df.dropna(subset=["date_night"])


# ----------------------------------------------------------
# Step 2 — Filter to Sept–Oct 2025
# ----------------------------------------------------------
start, end = pd.Timestamp("2025-09-01"), pd.Timestamp("2025-10-31")
df = df[(df["date_night"] >= start) & (df["date_night"] <= end)]
print(f"✅ Filtered to {len(df)} data points between {start.date()} and {end.date()}")

# ----------------------------------------------------------
# Step 3 — Build color pairs (same or nearby observation night)
# ----------------------------------------------------------
df["filter"] = df["filter"].str.lower().str.strip()  # normalize filters
valid_filters = ["g", "r", "o", "c", "v"]

pairs = []
for date in sorted(df["date_night"].unique()):
    nightly = df[df["date_night"] == date]
    if len(nightly) < 2:
        continue

    for f1 in valid_filters:
        for f2 in valid_filters:
            if f1 >= f2:
                continue
            d1 = nightly[nightly["filter"] == f1]
            d2 = nightly[nightly["filter"] == f2]
            if len(d1) and len(d2):
                color_val = float(d1["mag"].mean() - d2["mag"].mean())
                pairs.append({
                    "date_night": date,
                    "pair": f"{f1}-{f2}",
                    "color_index": color_val
                })

colors = pd.DataFrame(pairs)
print(f"✅ Built {len(colors)} color pairs across filters: {colors['pair'].unique()}")


# ----------------------------------------------------------
# Step 4 — Build color pairs within ±1 day tolerance
# ----------------------------------------------------------
tol = pd.Timedelta(days=1)
pairs = []

for d in avg["date_night"].unique():
    sub = avg[np.abs(avg["date_night"] - d) <= tol]
    f = list(sub["filter"])
    # g–r
    if "g" in f and "r" in f:
        gmag = sub.loc[sub["filter"]=="g","mag"].mean()
        rmag = sub.loc[sub["filter"]=="r","mag"].mean()
        pairs.append((d, "g-r", gmag - rmag))
    # g–o
    if "g" in f and "o" in f:
        gmag = sub.loc[sub["filter"]=="g","mag"].mean()
        omag = sub.loc[sub["filter"]=="o","mag"].mean()
        pairs.append((d, "g-o", gmag - omag))
    # r–o (proxy if no g data)
    if "r" in f and "o" in f:
        rmag = sub.loc[sub["filter"]=="r","mag"].mean()
        omag = sub.loc[sub["filter"]=="o","mag"].mean()
        pairs.append((d, "r-o", rmag - omag))

colors = pd.DataFrame(pairs, columns=["date_night","pair","color_index"])
colors = colors.sort_values("date_night")
colors.to_csv("I3_Color_Evolution_v5_1.csv", index=False)
print(f"📊 Saved: I3_Color_Evolution_v5_1.csv ({len(colors)} color pairs)")

# ----------------------------------------------------------
# Step 5 — Fit linear regression for each color index (robust)
# ----------------------------------------------------------
plt.figure(figsize=(8, 5))
for pair in colors["pair"].unique():
    sub = colors[colors["pair"] == pair].dropna()
    if len(sub) < 3:
        print(f"⚠️  Skipping {pair}: insufficient data ({len(sub)} pts)")
        continue

    x = (sub["date_night"] - sub["date_night"].min()).dt.days.values
    y = sub["color_index"].values

    # Guard against degenerate data
    if np.all(y == y[0]) or np.ptp(x) == 0:
        print(f"⚠️  Skipping {pair}: constant or invalid values")
        continue

    try:
        coeffs = np.polyfit(x, y, 1)
        fit = np.poly1d(coeffs)
        r2 = np.corrcoef(y, fit(x))[0, 1] ** 2
        slope = coeffs[0]
        plt.scatter(sub["date_night"], y, label=f"{pair} ({slope:+.4f} mag/day)")
        plt.plot(sub["date_night"], fit(x), "--")
        print(f"  {pair:>4} : slope={slope:+.5f} mag/day | R²={r2:.3f}")
    except Exception as e:
        print(f"⚠️  Skipped {pair} due to fit error: {e}")

plt.title("3I/ATLAS — Color Evolution (Sep–Oct 2025, ±1 day pairing)")
plt.ylabel("Color Index (mag)")
plt.xlabel("Date (2025)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("I3_Color_Evolution_v5_1.png", dpi=200)
print("✅ Saved: I3_Color_Evolution_v5_1.png")
print("✅ Done — regression and spectral trends complete.")
