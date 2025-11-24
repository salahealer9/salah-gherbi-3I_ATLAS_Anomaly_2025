import pandas as pd
from astroquery.jplhorizons import Horizons
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Step 1: Load your MPC photometry
# ------------------------------------------------------------
df = pd.read_csv("I3_clean.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

start_date = df["date"].min().strftime("%Y-%m-%d")
end_date   = df["date"].max().strftime("%Y-%m-%d")

print(f"Querying JPL Horizons for range: {start_date} to {end_date}")

# ------------------------------------------------------------
# Step 2: Query daily ephemerides (no long URI!)
# ------------------------------------------------------------
obj = Horizons(
    id="90004574",             # Primary nucleus of C/2019 Y4 (ATLAS)
    location="@399",           # Earth-based apparent magnitude
    epochs={"start": start_date,
            "stop":  end_date,
            "step": "1d"}
)



eph = obj.ephemerides()

# Automatically detect magnitude column
mag_key = None
for key in ["V", "Vmag", "Tmag", "Nmag", "APmag"]:
    if key in eph.colnames:
        mag_key = key
        break
if not mag_key:
    raise KeyError("No magnitude column found in JPL Horizons response.")

geo = pd.DataFrame({
    "date": pd.to_datetime(eph["datetime_str"]),
    "r": eph["r"],
    "delta": eph["delta"],
    "phase": eph["alpha"],
    "pred_mag": eph[mag_key],
})
print(f"✅ Using magnitude column: {mag_key}")

# ------------------------------------------------------------
# Step 3: Merge with MPC data (nearest date)
# ------------------------------------------------------------
merged = pd.merge_asof(df.sort_values("date"), geo.sort_values("date"), on="date")

# ------------------------------------------------------------
# Step 4: Compute residuals (observed - predicted)
# ------------------------------------------------------------
merged["residual"] = merged["mag"] - merged["pred_mag"]

# ------------------------------------------------------------
# Step 5: Print summary
# ------------------------------------------------------------
print("\n=== Residual Analysis (Observed - Predicted) ===")
print(merged["residual"].describe())

# ------------------------------------------------------------
# Step 6: Plot residuals
# ------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.plot(merged["date"], merged["residual"], "o-", label="Brightness residual (obs - pred)")
plt.axhline(0, color="gray", linestyle="--", alpha=0.6)
plt.title("3I/ATLAS (C/2019 Y4) — Brightness Residual vs JPL Horizons Prediction")
plt.ylabel("Δm (Observed - Predicted)")
plt.xlabel("Date (UTC)")
plt.gca().invert_yaxis()
plt.legend()
plt.tight_layout()
plt.savefig("I3_Horizons_Residuals.png", dpi=200)
plt.show()

merged.to_csv("I3_Horizons_Residuals.csv", index=False)
print("\n✅ Saved residual analysis to I3_Horizons_Residuals.csv and I3_Horizons_Residuals.png")

# Observed monthly mean magnitudes
obs = pd.read_csv("I3_monthly_summary.csv")
obs["month"] = pd.to_datetime(obs["month"])
obs_means = obs[["month", "mean"]].rename(columns={"mean": "obs_mag"})

# Predicted monthly mean magnitudes from JPL Horizons
geo["month"] = geo["date"].dt.to_period("M").dt.to_timestamp()
pred_means = geo.groupby("month")["pred_mag"].mean().reset_index()
pred_means = pred_means.rename(columns={"pred_mag": "pred_mag"})

# Merge and normalize both so July starts at zero
merged = pd.merge(obs_means, pred_means, on="month", how="inner")
merged["obs_norm"] = merged["obs_mag"] - merged["obs_mag"].iloc[0]
merged["pred_norm"] = merged["pred_mag"] - merged["pred_mag"].iloc[0]

plt.figure(figsize=(8,4))
plt.plot(merged["month"], merged["pred_norm"], "o--", color="gray", label="Predicted (JPL Horizons)")
plt.plot(merged["month"], merged["obs_norm"], "o-", color="gold", label="Observed (MPC)")
plt.gca().invert_yaxis()  # brighter = down
plt.title("3I/ATLAS (C/2019 Y4) — Normalized Brightness Evolution (2025)")
plt.xlabel("Month (2025)")
plt.ylabel("Δm relative to July (mag)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("I3_ATLAS_Horizons_Normalized.png", dpi=300)
plt.show()

print("✅ Saved normalized comparison to I3_ATLAS_Horizons_Normalized.png")
