#!/usr/bin/env python3
"""
color_evolution_I3_ATLAS_v4.py
-------------------------------------------------
Filtered to post-conjunction phase: July–September 2025
Computes:
  ✓ Nightly color indices (g–r, g–o, c–o)
  ✓ Linear trends (mag/day)
  ✓ Spectral gradients (%/100 nm)
  ✓ Annotated regression plot
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
                date = jd_base + pd.to_timedelta((dfrac % 1) * 24, unit="h")
            except Exception:
                date = np.nan
            records.append((date, float(mag), filt))

df = pd.DataFrame(records, columns=["date", "mag", "filter"]).dropna()
df["date_night"] = df["date"].dt.floor("D")

# ----------------------------------------------------------
# Step 2 — Filter to September–October 2025
# ----------------------------------------------------------
start, end = pd.Timestamp("2025-09-01"), pd.Timestamp("2025-10-31")
df = df[(df["date_night"] >= start) & (df["date_night"] <= end)]
print(f"✅ Filtered to {len(df)} data points between {start.date()} and {end.date()}")


# ----------------------------------------------------------
# Step 3 — Nightly averages
# ----------------------------------------------------------
avg = df.groupby(["date_night", "filter"])["mag"].mean().reset_index()

# ----------------------------------------------------------
# Step 4 — Build color indices
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
color_df.to_csv("I3_Color_Evolution_v4.csv", index=False)
print(f"📊 Saved: I3_Color_Evolution_v4.csv")

# ----------------------------------------------------------
# Step 5 — Trend + spectral slope
# ----------------------------------------------------------
print("\n📈 Color evolution trends (Jul–Sep 2025):")
λ = {"g":475, "r":620, "o":650, "c":550}  # nm centers

def spec_gradient(delta_mag, λ1, λ2):
    ratio = 10**(0.4*delta_mag)
    return ((ratio - 1) / (λ2 - λ1)) * 1e4 * 100  # % per 100 nm

plt.figure(figsize=(9,6))
colors = {"g-r":"royalblue", "g-o":"darkorange", "c-o":"mediumseagreen"}

for col in color_df["color"].unique():
    sub = color_df[color_df["color"]==col]
    if len(sub) < 3:
        continue

    x = (sub["date"] - sub["date"].min()).dt.days
    y = sub["value"]
    slope, intercept, r, p, se = linregress(x, y)
    fit_y = intercept + slope*x

    band1, band2 = col.split("-")
    mean_color = y.mean()
    grad = spec_gradient(mean_color, λ[band1], λ[band2])

    print(f"  {col:4s}: slope={slope:+.5f} mag/day | R²={r**2:.3f} | spectral≈{grad:+.1f}%/100 nm")

    plt.plot(sub["date"], y, "o-", color=colors.get(col,"gray"), label=f"{col}")
    plt.plot(sub["date"], fit_y, "--", color=colors.get(col,"gray"), alpha=0.6)

    xpos = sub["date"].iloc[len(sub)//2]
    ypos = np.interp(xpos.toordinal(), sub["date"].map(lambda d: d.toordinal()), fit_y)
    plt.text(xpos, ypos+0.05, f"{slope:+.4f} mag/day", fontsize=8, color=colors.get(col,"gray"))

# ----------------------------------------------------------
# Step 6 — Plot styling
# ----------------------------------------------------------
plt.axhline(0, color="gray", linestyle="--", alpha=0.4)
plt.gca().invert_yaxis()
plt.title("Color Evolution of 3I/ATLAS (C/2019 Y4) — Jul–Sep 2025")
plt.ylabel("Color Index (mag)")
plt.xlabel("Date (2025)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("I3_Color_Evolution_v4.png", dpi=220)
print("✅ Saved: I3_Color_Evolution_v4.png")

print("\n✅ Done — filtered regression and spectral trends complete.")
