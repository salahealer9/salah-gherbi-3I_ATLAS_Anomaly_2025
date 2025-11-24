#!/usr/bin/env python3
"""
color_evolution_I3_ATLAS_v2.py
-------------------------------------------------
Analyzes color evolution of 3I/ATLAS (C/2019 Y4)
and computes:
  • Linear trend slope (mag/day)
  • Approx. spectral gradient (%/100 nm)

Requires: pandas, numpy, matplotlib
"""

import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import linregress

# ----------------------------------------------------------
# Step 1 — Parse MPC photometry
# ----------------------------------------------------------
fname = "I3.txt"
print(f"📂 Parsing MPC photometry from {fname}...")

pattern = re.compile(
    r"C(2025\s+\d{2}\s+\d+\.\d+).*?(-?\d+\.\d+)\s*([grcVoB])"
)

records = []
with open(fname, "r") as f:
    for line in f:
        m = pattern.search(line)
        if m:
            date_str, mag, filt = m.groups()
            parts = date_str.strip().split()
            y, mth, dfrac = int(parts[0]), int(parts[1]), float(parts[2])
            try:
                jd_base = datetime(y, mth, int(dfrac))
                date = jd_base + pd.to_timedelta((dfrac % 1) * 24, unit='h')
            except Exception:
                date = np.nan
            records.append((date, float(mag), filt))

df = pd.DataFrame(records, columns=["date", "mag", "filter"]).dropna()
df["date_night"] = df["date"].dt.floor("D")
print(f"✅ Parsed {len(df)} photometric points across {df['filter'].nunique()} filters.")

# ----------------------------------------------------------
# Step 2 — Nightly averages
# ----------------------------------------------------------
avg = df.groupby(["date_night", "filter"])["mag"].mean().reset_index()

# ----------------------------------------------------------
# Step 3 — Build color indices
# ----------------------------------------------------------
pairs = []
for d in avg["date_night"].unique():
    sub = avg[avg["date_night"] == d]
    f = list(sub["filter"])
    if "g" in f and "r" in f:
        pairs.append((d, "g-r", sub.loc[sub["filter"]=="g","mag"].values[0] - sub.loc[sub["filter"]=="r","mag"].values[0]))
    if "g" in f and "o" in f:
        pairs.append((d, "g-o", sub.loc[sub["filter"]=="g","mag"].values[0] - sub.loc[sub["filter"]=="o","mag"].values[0]))
    if "c" in f and "o" in f:
        pairs.append((d, "c-o", sub.loc[sub["filter"]=="c","mag"].values[0] - sub.loc[sub["filter"]=="o","mag"].values[0]))

color_df = pd.DataFrame(pairs, columns=["date","color","value"]).sort_values("date")
color_df.to_csv("I3_Color_Evolution_v2.csv", index=False)
print(f"📊 Saved: I3_Color_Evolution_v2.csv")

# ----------------------------------------------------------
# Step 4 — Fit linear trends
# ----------------------------------------------------------
print("\n📈 Color evolution trends:")
trend_rows = []
λ = {"g":475, "r":620, "o":650, "c":550}  # nm, approximate centers

def spec_gradient(delta_mag, λ1, λ2):
    # Convert mag difference to reflectance slope (%/100 nm)
    ratio = 10**(0.4*delta_mag)
    return ((ratio-1)/(λ2-λ1))*1e4*100  # per 100 nm

for col in color_df["color"].unique():
    sub = color_df[color_df["color"]==col]
    if len(sub)<3: continue
    x = (sub["date"] - sub["date"].min()).dt.days
    slope, intercept, r, p, se = linregress(x, sub["value"])
    trend_rows.append([col, slope, r, p])

    # derive spectral gradient at mid-color
    band1, band2 = col.split("-")
    mean_color = sub["value"].mean()
    grad = spec_gradient(mean_color, λ[band1], λ[band2])
    print(f"  {col:4s}: slope={slope:+.4f} mag/day,  R²={r**2:.3f},  spectral≈{grad:+.1f}%/100 nm")

# ----------------------------------------------------------
# Step 5 — Plot
# ----------------------------------------------------------
plt.figure(figsize=(8,5))
for col in color_df["color"].unique():
    sub = color_df[color_df["color"]==col]
    plt.plot(sub["date"], sub["value"], "o-", label=col)

plt.axhline(0, color="gray", linestyle="--", alpha=0.4)
plt.gca().invert_yaxis()
plt.title("Color Evolution of 3I/ATLAS (C/2019 Y4) — 2025")
plt.ylabel("Color Index (mag)")
plt.xlabel("Date (2025)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("I3_Color_Evolution_v2.png", dpi=200)
print("✅ Saved: I3_Color_Evolution_v2.png")

print("\nDone — trend analysis complete.")
