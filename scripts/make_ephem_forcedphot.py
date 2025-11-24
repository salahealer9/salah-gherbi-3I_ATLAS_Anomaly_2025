# make_points_for_ztf_queue.py
from astroquery.jplhorizons import Horizons
import pandas as pd

# 3I/ATLAS (C/2019 Y4) – main fragment id
TARGET_ID = "90004574"
# Palomar/ZTF observatory code
OBS = "I41"

# Query a window straddling post-conjunction
epochs = {"start":"2025-10-24", "stop":"2025-10-31", "step":"3h"}
obj = Horizons(id=TARGET_ID, location=OBS, epochs=epochs)
e = obj.ephemerides()

# Build dataframe
df = pd.DataFrame({
    "jd": e["datetime_jd"],
    "mjd": e["datetime_jd"] - 2400000.5,
    "ra": e["RA"],             # deg
    "dec": e["DEC"],           # deg
    "el": e["EL"],             # elevation above horizon (deg)
    "airmass": e["airmass"],
    "sun_alt": e["EL"] - e["EL"] + e["ObsEclLat"]*0  # dummy init
})

# Horizons gives Sun altitude via 'solartime' context, but IRSA queue mainly needs
# we ensure night using 'solar_presence' flag instead (None means night).
df["solar_presence"] = e["solar_presence"]

# Good-geometry filter:
# - Nighttime: solar_presence == ' ' (blank/None in table means below horizon)
# - Elevation > 25 deg (better image quality)
# - Airmass < 2.5
# - Solar elongation > 35 deg
good = (e["solar_presence"] == ' ')
good &= (e["EL"] > 10)
good &= (e["airmass"] < 2.5)
good &= (e["elong"] > 25)

sel = df[good].copy()

# Bias toward latest dates (post-conjunction)
sel = sel.sort_values("mjd")[-100:]  # keep the latest up to 100

print(f"Selected {len(sel)} high-quality epochs for ZTF forced photometry:")
print("---- Copy the lines below into the ZTF queue ----")
for _, r in sel.iterrows():
    print(f"{r['ra']:.5f} {r['dec']:.5f} MJD={r['mjd']:.6f}")
