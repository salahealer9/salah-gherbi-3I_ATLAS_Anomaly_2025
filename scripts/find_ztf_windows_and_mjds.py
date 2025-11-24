#!/usr/bin/env python3
from astroquery.jplhorizons import Horizons
import pandas as pd
import numpy as np

# --- Parameters you can tweak ---
OBS = "I41"  # Palomar/ZTF
START = "2025-11-01"
STOP  = "2025-12-31"
STEP  = "30m"  # half-hour sampling
EL_MIN = 20.0
ELONG_MIN = 25.0

print(f"Querying Horizons for {START} → {STOP} @ {OBS} ...")
obj = Horizons(id="90004574", location=OBS,
               epochs={"start": START, "stop": STOP, "step": STEP})
e = obj.ephemerides()

# Convert to DataFrame
df = e.to_pandas()

# Keep only true night (exclude any daylight/twilight keywords)
sp = df["solar_presence"].astype(str).str.lower()
is_night = ~sp.str.contains("day|civil|nautical|twilight", case=False, na=False)

# Apply visibility cuts
good = (
    is_night &
    (df["EL"] >= EL_MIN) &
    (df["elong"] >= ELONG_MIN)
)

vis = df.loc[good, ["datetime_str","datetime_jd","EL","elong","RA","DEC","r","delta"]].copy()
vis = vis.rename(columns={
    "datetime_str":"utc",
    "datetime_jd":"jd",
})
# MJD = JD - 2400000.5
vis["mjd"] = vis["jd"] - 2400000.5

# Keep unique nights (first few per night) so you don’t flood the queue
vis["date"] = pd.to_datetime(vis["utc"].str.split().str[0])
vis = vis.sort_values("utc")

# Show a small sample per night (e.g., up to 5 epochs)
out = []
for d, sub in vis.groupby("date"):
    out.append(sub.head(5))
vis_sample = pd.concat(out) if out else vis

# Save and print
cols = ["mjd","RA","DEC","EL","elong","r","delta","utc"]
vis_sample["ra_deg"] = vis_sample["RA"].astype(float)
vis_sample["dec_deg"] = vis_sample["DEC"].astype(float)
final = vis_sample[["mjd","ra_deg","dec_deg","EL","elong","r","delta","utc"]].reset_index(drop=True)
final.to_csv("ZTF_forcedphot_candidates.csv", index=False)

print("\n=== Candidate epochs for ZTF forced photometry (I41) ===")
if final.empty:
    print("No viable night-time windows in this range/thresholds.")
else:
    print(final.head(30).to_string(index=False))
    print(f"\nSaved: ZTF_forcedphot_candidates.csv  (rows: {len(final)})")

# Also emit a minimal 3-column block ready to paste into the ZTF queue
if not final.empty:
    block = final[["mjd","ra_deg","dec_deg"]].copy()
    block.columns = ["mjd","ra","dec"]
    print("\n---- Copy the lines below into the ZTF queue ----")
    for _, r in block.iterrows():
        print(f"{r.mjd:.6f} {r.ra:.5f} {r.dec:.5f}")
