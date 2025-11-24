#!/usr/bin/env python3
"""
color_validation_I3_ATLAS_v2_2.py
---------------------------------
Color-evolution validation for 3I/ATLAS (C/2019 Y4), Sep–Oct 2025.

• Parses MPC file I3.txt (photometry lines starting with '0003I' and 'C2025').
• Builds nightly per-filter magnitudes PER MPC STATION (obs code), then
  forms color pairs (g–r, g–o, r–o) using same-night data with ±1 day tolerance
  but still within the SAME station to minimize calibration drift.
• Fetches phase angle (alpha) for those nights from JPL Horizons (@399 geocenter).
• Regressions:
    - Color vs time (OLS; Theil–Sen if scikit-learn available)
    - Color vs phase angle (OLS; Theil–Sen if available)
• Outputs:
    - I3_Color_Validated.csv
    - I3_Color_Validated.png

Dependencies: pandas, numpy, matplotlib, astroquery (for Horizons)
Optional: scikit-learn (for robust Theil–Sen)
"""

import re
import sys
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---- Optional robust fit (Theil–Sen) ----
HAVE_SKLEARN = False
try:
    from sklearn.linear_model import TheilSenRegressor
    HAVE_SKLEARN = True
except Exception:
    HAVE_SKLEARN = False

# ---- Horizons for phase angle ----
try:
    from astroquery.jplhorizons import Horizons
    HAVE_HORIZONS = True
except Exception:
    HAVE_HORIZONS = False

# -----------------------------
# Configuration
# -----------------------------
MPC_FILE = "I3.txt"
START = pd.Timestamp("2025-09-01", tz="UTC")
END   = pd.Timestamp("2025-10-31", tz="UTC")
FILTERS = ["g", "r", "o"]  # we’ll form g–r, g–o, r–o
PAIR_LIST = [("g", "r"), ("g", "o"), ("r", "o")]
PAIR_LABELS = {"g-r": "g–r", "g-o": "g–o", "r-o": "r–o"}
PAIR_COLORS = {"g-r": "tab:blue", "g-o": "tab:orange", "r-o": "tab:green"}
DATE_TOLERANCE = pd.Timedelta(days=1)

# -----------------------------
# Helpers
# -----------------------------
def frac_day_to_ts(month: int, day_float: float) -> pd.Timestamp:
    """MPC dates are like '09 04.273606'. Convert to UTC timestamp."""
    d_int = int(day_float)
    frac = day_float - d_int
    base = pd.Timestamp(f"2025-{month:02d}-{d_int:02d} 00:00:00", tz="UTC")
    return base + pd.to_timedelta(frac * 24, unit="h")

def parse_mpc_photometry(mpc_path: str) -> pd.DataFrame:
    """
    Parse lines like:
    0003I ... C2025 09 04.273606 ... 16.29gV#0K4fE55
                                   ^^^^^^^^
    Extract month, day.frac, magnitude, filter (g/r/o/c/v), and obs code (last 3).
    """
    rows = []
    with open(mpc_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if not line.startswith("0003I"):
                continue
            if "C2025" not in line:
                continue

            # date fragment
            m = re.search(r"C2025\s+(\d{2})\s+(\d{2}\.\d+)", line)
            if not m:
                continue
            month = int(m.group(1))
            dayf  = float(m.group(2))

            # magnitude + filter (e.g., '16.29g' or '14.85o')
            mm = re.search(r"(\d{2}\.\d{2})([grcVoB])", line)
            if not mm:
                continue
            mag = float(mm.group(1))
            flt = mm.group(2).lower()

            # observatory code: last 3 alphanumerics on the line
            oc = "UNK"
            mcode = re.search(r"([A-Za-z0-9]{3})\s*$", line.strip())
            if mcode:
                oc = mcode.group(1)

            ts = frac_day_to_ts(month, dayf)

            rows.append({
                "date_utc": ts, "month": month, "dayf": dayf,
                "mag": mag, "filter": flt, "obs_code": oc
            })

    df = pd.DataFrame(rows)
    # Limit to desired filters
    df = df[df["filter"].isin(FILTERS)].copy()
    return df

def nightly_station_means(df: pd.DataFrame) -> pd.DataFrame:
    """Bin to local 'night' (UTC day) per station & filter."""
    df = df.copy()
    df["night"] = df["date_utc"].dt.floor("D")
    g = df.groupby(["obs_code", "night", "filter"], as_index=False)["mag"].agg(["mean", "count", "std"])
    g = g.reset_index().rename(columns={"mean": "mag_mean", "count": "n", "std": "mag_std"})
    return g

def build_color_pairs(nightly: pd.DataFrame) -> pd.DataFrame:
    """
    Form color pairs within the SAME obs_code.
    Same-night pairs first; if missing, allow ±1 day match.
    """
    out = []

    # Work station by station
    for oc, sub in nightly.groupby("obs_code"):
        sub = sub.copy().sort_values("night")
        # Pivot to have columns per filter for easy same-night pairing
        piv = sub.pivot_table(index="night", columns="filter", values="mag_mean", aggfunc="mean")

        # Same-night pairs
        for (f1, f2) in PAIR_LIST:
            lbl = f"{f1}-{f2}"
            if (f1 in piv.columns) and (f2 in piv.columns):
                same = piv[[f1, f2]].dropna()
                for dt, row in same.iterrows():
                    out.append({"obs_code": oc, "night": dt, "pair": lbl,
                                "color": float(row[f1] - row[f2]),
                                "pair_mode": "same-night"})

        # ±1 day tolerance (only if not same-night)
        # Build a long format for nearest-night search
        for (f1, f2) in PAIR_LIST:
            lbl = f"{f1}-{f2}"
            # dates where pair already exists (avoid duplicates)
            have_dates = {r["night"] for r in out if r["obs_code"] == oc and r["pair"] == lbl and r["pair_mode"] == "same-night"}

            # candidate nights with f1
            n1 = sub[sub["filter"] == f1][["night", "mag_mean"]].rename(columns={"mag_mean": "m1"})
            # candidate nights with f2
            n2 = sub[sub["filter"] == f2][["night", "mag_mean"]].rename(columns={"mag_mean": "m2"})

            for dt1, m1 in n1.itertuples(index=False):
                if dt1 in have_dates:
                    continue  # already have same-night
                # search for f2 within ±1 day
                close = n2[(n2["night"] >= dt1 - DATE_TOLERANCE) & (n2["night"] <= dt1 + DATE_TOLERANCE)]
                if not close.empty:
                    # pick the nearest night in absolute difference
                    close["absdiff"] = (close["night"] - dt1).abs()
                    row2 = close.sort_values("absdiff").iloc[0]
                    out.append({
                        "obs_code": oc, "night": dt1, "pair": lbl,
                        "color": float(m1 - row2["m2"]),
                        "pair_mode": "±1day"
                    })

    if not out:
        return pd.DataFrame(columns=["obs_code", "night", "pair", "color", "pair_mode"])

    pairs_df = pd.DataFrame(out).sort_values(["obs_code", "night", "pair"]).reset_index(drop=True)
    return pairs_df

def fetch_phase_angles(dates_utc: list) -> pd.DataFrame:
    """Fetch phase angle alpha (deg) from Horizons @399 (geocenter) for given dates."""
    if not HAVE_HORIZONS:
        print("⚠️  astroquery.jplhorizons not available — skipping phase angles.")
        return pd.DataFrame({"night": dates_utc, "phase_deg": [np.nan]*len(dates_utc)})

    # Horizons expects strings in UTC; give a small range to ensure coverage
    t_start = (min(dates_utc) - pd.Timedelta(hours=1)).strftime("%Y-%m-%d")
    t_stop  = (max(dates_utc) + pd.Timedelta(hours=1)).strftime("%Y-%m-%d")

    try:
        # Use the un-split parent solution ID (matches earlier usage)
        obj = Horizons(id="90004574", location="@399",
                       epochs={"start": t_start, "stop": t_stop, "step": "1d"})
        eph = obj.ephemerides()
        # alpha column is the phase angle (Sun-Target-Observer)
        tbl = pd.DataFrame({
            "night": pd.to_datetime(eph["datetime_str"]),
            "phase_deg": np.array(eph["alpha"], dtype=float)
        })
        tbl["night"] = tbl["night"].dt.tz_localize("UTC").dt.floor("D")
        return tbl[["night", "phase_deg"]].drop_duplicates("night")
    except Exception as e:
        print(f"⚠️  Horizons phase-angle fetch failed: {e}")
        return pd.DataFrame({"night": dates_utc, "phase_deg": [np.nan]*len(dates_utc)})

def fit_and_report(x, y, label):
    """Run OLS (always) and Theil–Sen (if available). Return dict of results."""
    out = {}
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    good = np.isfinite(x) & np.isfinite(y)
    x = x[good]; y = y[good]
    if len(x) < 2:
        return None

    # OLS
    coeffs = np.polyfit(x, y, 1)
    fit = np.poly1d(coeffs)
    r2 = np.corrcoef(y, fit(x))[0, 1] ** 2 if len(x) > 1 else np.nan
    out["ols_slope"] = coeffs[0]
    out["ols_intercept"] = coeffs[1]
    out["ols_r2"] = r2

    # Robust
    if HAVE_SKLEARN and len(x) >= 3:
        try:
            model = TheilSenRegressor(random_state=0)
            model.fit(x.reshape(-1, 1), y)
            out["ts_slope"] = float(model.coef_[0])
            out["ts_intercept"] = float(model.intercept_)
        except Exception:
            out["ts_slope"] = np.nan
            out["ts_intercept"] = np.nan
    else:
        out["ts_slope"] = np.nan
        out["ts_intercept"] = np.nan

    print(f"  ▸ {label}: OLS slope={out['ols_slope']:+.5f}, R²={out['ols_r2']:.3f}"
          + (f" | Theil–Sen={out['ts_slope']:+.5f}" if np.isfinite(out['ts_slope']) else ""))

    return out

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    print("📂 Parsing MPC photometry…")
    df = parse_mpc_photometry(MPC_FILE)
    if df.empty:
        print("❌ No usable MPC photometry found.")
        sys.exit(1)

    # Restrict time range
    df = df[(df["date_utc"] >= START) & (df["date_utc"] <= END)].copy()
    print(f"✅ Kept {len(df)} measurements between {START.date()} and {END.date()}")

    # Nightly per-station means
    nightly = nightly_station_means(df)
    if nightly.empty:
        print("❌ No nightly station-averaged data.")
        sys.exit(1)

     # Optionially merge all stations
    MERGE_STATIONS = True
    if MERGE_STATIONS:
        nightly["obs_code"] = "ALL"

    # Build color pairs
    pairs = build_color_pairs(nightly)
    if pairs.empty:
        print("❌ No color pairs could be formed (try widening tolerance).")
        sys.exit(1)

    # Fetch phase angles and merge
    nights = sorted(pairs["night"].unique())
    phase_tbl = fetch_phase_angles(nights)
    pairs = pairs.merge(phase_tbl, on="night", how="left")

    # Save table
    out_csv = "I3_Color_Validated.csv"
    pairs_out = pairs.copy()
    pairs_out["night_iso"] = pairs_out["night"].dt.strftime("%Y-%m-%d")
    pairs_out = pairs_out[["night_iso", "obs_code", "pair", "pair_mode", "color", "phase_deg"]]
    pairs_out.to_csv(out_csv, index=False)
    print(f"📊 Saved: {out_csv}  ({len(pairs_out)} rows)")

    # ------------- Plotting -------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)

    # Panel A: color vs date
    ax = axes[0]
    for key in ["g-r", "g-o", "r-o"]:
        sub = pairs[pairs["pair"] == key]
        if sub.empty: 
            continue
        ax.scatter(sub["night"], sub["color"], s=28, alpha=0.9,
                   label=f"{PAIR_LABELS[key]} ({sub['pair_mode'].value_counts().to_dict()})",
                   color=PAIR_COLORS.get(key, None))
        # OLS fit (days since first)
        x = (sub["night"] - sub["night"].min()).dt.days.values
        y = sub["color"].values
        if len(sub) >= 2:
            coeffs = np.polyfit(x, y, 1)
            xx = np.linspace(x.min(), x.max(), 100)
            yy = np.poly1d(coeffs)(xx)
            ax.plot(sub["night"].min() + pd.to_timedelta(xx, unit="D"),
                    yy, linestyle="--", linewidth=1)

    ax.set_title("Color vs Time (Sep–Oct 2025)")
    ax.set_xlabel("Date (UTC)")
    ax.set_ylabel("Color index (mag)")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    # mag-style y (no invert here; these are colors)

    # Panel B: color vs phase angle
    ax2 = axes[1]
    for key in ["g-r", "g-o", "r-o"]:
        sub = pairs[pairs["pair"] == key].dropna(subset=["phase_deg"])
        if sub.empty:
            continue
        ax2.scatter(sub["phase_deg"], sub["color"], s=28, alpha=0.9,
                    label=PAIR_LABELS[key], color=PAIR_COLORS.get(key, None))
        if len(sub) >= 2:
            coeffs = np.polyfit(sub["phase_deg"].values, sub["color"].values, 1)
            xx = np.linspace(sub["phase_deg"].min(), sub["phase_deg"].max(), 100)
            yy = np.poly1d(coeffs)(xx)
            ax2.plot(xx, yy, linestyle="--", linewidth=1)

    ax2.set_title("Color vs Phase Angle (α) — JPL Horizons @399")
    ax2.set_xlabel("Phase angle α (deg)")
    ax2.set_ylabel("Color index (mag)")
    ax2.grid(alpha=0.3)
    ax2.legend(fontsize=8)

    out_png = "I3_Color_Validated.png"
    fig.suptitle("3I/ATLAS (C/2019 Y4) — Validated Color Trends (Station-constrained, ±1 day)", fontsize=12)
    fig.savefig(out_png, dpi=200)
    print(f"🖼️ Saved: {out_png}")

    # ---- Console summary (fits) ----
    print("\n=== Regression summaries ===")
    for key in ["g-r", "g-o", "r-o"]:
        sub = pairs[pairs["pair"] == key]
        if sub.empty:
            continue
        # vs time
        x_t = (sub["night"] - sub["night"].min()).dt.days.values
        y = sub["color"].values
        res_t = fit_and_report(x_t, y, f"{PAIR_LABELS[key]} vs time")
        # vs phase
        subp = sub.dropna(subset=["phase_deg"])
        if len(subp) >= 2:
            res_p = fit_and_report(subp["phase_deg"].values, subp["color"].values,
                                   f"{PAIR_LABELS[key]} vs phase")
