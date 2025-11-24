#!/usr/bin/env python3
"""
color_evolution_I3_ATLAS.py
---------------------------------
Derives color indices (e.g. g-o, c-o) for 3I/ATLAS (C/2019 Y4)
from MPC observation file (I3.txt).

✅ Works directly on MPC-format lines (C2025 …)
✅ Detects multiple filters: g, r, c, o, V, B
✅ Computes nightly averages per filter
✅ Derives color indices for near-simultaneous observations
✅ Plots color evolution over time

Author: Salah-Eddin Gherbi
Version: 1.0 — November 2025
"""

import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ----------------------------------------------------------
# Step 1 — Parse MPC file
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
            try:
                # convert to datetime
                parts = date_str.strip().split()
                y, mth, dfrac = int(parts[0]), int(parts[1]), float(parts[2])
                jd_base = datetime(y, mth, int(dfrac))
                date = jd_base + pd.to_timedelta((dfrac % 1) * 24, unit='h')
            except Exception:
                date = np.nan
            records.append((date, float(mag), filt))

df = pd.DataFrame(records, columns=["date", "mag", "filter"])
df = df.dropna()
df["month"] = df["date"].dt.to_period("M")
print(f"✅ Parsed {len(df)} photometric points across {df['filter'].nunique()} filters.")

# ----------------------------------------------------------
# Step 2 — Compute nightly averages per filter
# ----------------------------------------------------------
df["date_night"] = df["date"].dt.floor("D")
avg = df.groupby(["date_night", "filter"])["mag"].agg(["mean", "std", "count"]).reset_index()

# ----------------------------------------------------------
# Step 3 — Compute color indices
# ----------------------------------------------------------
pairs = []
for d in avg["date_night"].unique():
    sub = avg[avg["date_night"] == d]
    filters = list(sub["filter"])
    # only compute if both g and o exist
    if "g" in filters and "o" in filters:
        gmag = sub[sub["filter"] == "g"]["mean"].values[0]
        omag = sub[sub["filter"] == "o"]["mean"].values[0]
        pairs.append((d, "g-o", gmag - omag))
    if "c" in filters and "o" in filters:
        cmag = sub[sub["filter"] == "c"]["mean"].values[0]
        omag = sub[sub["filter"] == "o"]["mean"].values[0]
        pairs.append((d, "c-o", cmag - omag))
    if "g" in filters and "r" in filters:
        gmag = sub[sub["filter"] == "g"]["mean"].values[0]
        rmag = sub[sub["filter"] == "r"]["mean"].values[0]
        pairs.append((d, "g-r", gmag - rmag))

color_df = pd.DataFrame(pairs, columns=["date", "color", "value"])
color_df = color_df.sort_values("date")
color_df.to_csv("I3_Color_Evolution.csv", index=False)
print(f"📊 Saved color indices to I3_Color_Evolution.csv")

# ----------------------------------------------------------
# Step 4 — Plot
# ----------------------------------------------------------
plt.figure(figsize=(8, 5))
for col in color_df["color"].unique():
    subset = color_df[color_df["color"] == col]
    plt.plot(subset["date"], subset["value"], "o-", label=col)

plt.axhline(0, color="gray", linestyle="--", alpha=0.5)
plt.gca().invert_yaxis()
plt.title("Color Evolution of 3I/ATLAS (C/2019 Y4) — 2025")
plt.ylabel("Color Index (mag)")
plt.xlabel("Date (2025)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("I3_Color_Evolution.png", dpi=200)
print("✅ Saved plot: I3_Color_Evolution.png")

print("\nDone. Inspect the CSV and plot to see if (g–o) or (c–o) decreased over time (bluer trend).")
