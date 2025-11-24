#!/usr/bin/env python3
"""
watch_mpc_colors.py
Detect NEW color pairs (g–r, g–o, r–o, etc.) for 3I/ATLAS (C/2019 Y4) from MPC I3.txt.

- Default: reads local I3.txt in the current folder
- Optional: --url https://... to fetch I3.txt from the web
- Pairs are built for the same night and (optionally) ±N-day tolerance
- New findings are appended to I3_Color_Alerts.csv and printed to console
- State is tracked in .mpc_color_state.json so you only see *new* pairs

Usage examples:
  python watch_mpc_colors.py
  python watch_mpc_colors.py --window 1
  python watch_mpc_colors.py --url https://example/I3.txt --window 2
"""

import argparse, re, json, sys, hashlib
from datetime import timedelta
from pathlib import Path

import pandas as pd

try:
    import requests
except ImportError:
    requests = None

# ------------------------- CLI -------------------------
def get_args():
    p = argparse.ArgumentParser(description="Watch MPC I3.txt for new 3I/ATLAS color pairs.")
    p.add_argument("--file", default="I3.txt", help="Local MPC file path (default: I3.txt)")
    p.add_argument("--url", default=None, help="Optional URL to fetch I3.txt instead of local file")
    p.add_argument("--window", type=int, default=1, help="±days tolerance for cross-night pairing (default: 1)")
    p.add_argument("--start", default="2025-07-01", help="Start date (UTC) for filtering (YYYY-MM-DD)")
    p.add_argument("--end",   default="2025-12-31", help="End date (UTC) for filtering (YYYY-MM-DD)")
    return p.parse_args()

# ------------------------- Helpers -------------------------
FILTERS = ["g", "r", "o", "c", "v", "B", "V", "R", "I"]  # MPC tags seen in your file; normalize to lower-case later

def fractional_day_to_datetime(year: int, month: int, day_frac: float) -> pd.Timestamp:
    day_int = int(day_frac)
    frac = day_frac - day_int
    base = pd.Timestamp(f"{year}-{month:02d}-{day_int:02d}", tz="UTC")
    return base + pd.to_timedelta(frac * 24, unit="h")

def load_text(args) -> str:
    if args.url:
        if requests is None:
            print("❌ 'requests' not installed; either install it or use --file.", file=sys.stderr)
            sys.exit(1)
        r = requests.get(args.url, timeout=30)
        r.raise_for_status()
        return r.text
    else:
        return Path(args.file).read_text(encoding="utf-8", errors="ignore")

def parse_mpc_i3(text: str) -> pd.DataFrame:
    rows = []
    for line in text.splitlines():
        # Only 3I lines
        if not line.startswith("0003I"):
            continue
        # Look for C2025 mm dd.ddddd
        m_date = re.search(r"C(20\d{2})\s(\d{2})\s(\d{2}\.\d+)", line)
        if not m_date:
            continue
        year  = int(m_date.group(1))
        month = int(m_date.group(2))
        day   = float(m_date.group(3))

        # Look for magnitude + filter (e.g., "17.83rU" "16.03gV" etc.)
        m_mag = re.search(r"(\d{2}\.\d{2})([A-Za-z])", line)
        if not m_mag:
            continue
        mag = float(m_mag.group(1))
        flt = m_mag.group(2)

        # Obs code at line end (e.g., "#0K4gE55" or similar)
        m_obs = re.search(r"#\S+$", line)
        obs = m_obs.group(0)[1:] if m_obs else ""

        tstamp = fractional_day_to_datetime(year, month, day)

        rows.append({
            "date_utc": tstamp,
            "year": year,
            "month": month,
            "day_frac": day,
            "mag": mag,
            "filter": flt,
            "obs": obs
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    # Normalize filter tags
    df["filter"] = df["filter"].str.strip()
    df["filter_norm"] = df["filter"].str.lower().replace({
        "B":"b","V":"v","R":"r","I":"i"
    })

    # Keep only filters we can use
    df = df[df["filter_norm"].isin([f.lower() for f in FILTERS])]
    return df

def build_color_pairs(df: pd.DataFrame, window_days: int) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["date_center","pair","color","n_pts","span_days","phase_deg","obs_set"])

    # phase angle is rarely present; set NaN (you can join Horizons later if desired)
    df = df.sort_values("date_utc").copy()

    pairs = []
    tol = pd.Timedelta(days=window_days)

    # compress nightly by filter (mean per night)
    df["night"] = df["date_utc"].dt.floor("D")
    nightly = (
        df.groupby(["night", "filter_norm"], as_index=False)
          .agg(mag=("mag","mean"), n=("mag","count"), obs_set=("obs", lambda x: ",".join(sorted(set(x)))))
    )

    nights = nightly["night"].unique()
    for center in nights:
        sub = nightly[ (nightly["night"] >= center - tol) & (nightly["night"] <= center + tol) ]
        have = dict(sub.groupby("filter_norm")["mag"].mean())

        # candidate pairs we care about
        combos = [("g","r"),("g","o"),("r","o"),("g","v"),("r","v")]
        for f1,f2 in combos:
            if f1 in have and f2 in have:
                cval = have[f1] - have[f2]  # color index (mag)
                # points used & span
                involved = sub[sub["filter_norm"].isin([f1,f2])]
                n_pts = int(involved["n"].sum())
                span_days = (involved["night"].max() - involved["night"].min()).days
                obs_join = ",".join(sorted(set(",".join(involved["obs_set"]).split(","))))
                pairs.append({
                    "date_center": center,
                    "pair": f"{f1}-{f2}",
                    "color": float(cval),
                    "n_pts": n_pts,
                    "span_days": span_days,
                    "phase_deg": pd.NA,  # placeholder
                    "obs_set": obs_join
                })

    out = pd.DataFrame(pairs).sort_values(["date_center","pair"])
    return out

def digest_rows(df: pd.DataFrame) -> str:
    # small fingerprint so we can detect new discoveries
    h = hashlib.sha256()
    for _, r in df.iterrows():
        h.update(f"{r['date_center']:%Y-%m-%d}|{r['pair']}|{r['color']:.4f}".encode())
    return h.hexdigest()

# ------------------------- Main -------------------------
def main():
    args = get_args()

    # Load MPC
    try:
        text = load_text(args)
    except Exception as e:
        print(f"❌ Unable to load MPC text: {e}")
        sys.exit(1)

    df = parse_mpc_i3(text)
    if df.empty:
        print("⚠️ No usable MPC photometry parsed for 3I/ATLAS.")
        sys.exit(0)

    # Date window
    START = pd.Timestamp(args.start, tz="UTC")
    END   = pd.Timestamp(args.end, tz="UTC")
    df = df[(df["date_utc"] >= START) & (df["date_utc"] <= END)].copy()
    print(f"📂 Parsed {len(df)} photometric points in window {START.date()} → {END.date()}")

    # Build pairs
    pairs = build_color_pairs(df, args.window)
    if pairs.empty:
        print("ℹ️ No color pairs found (try increasing --window).")
        sys.exit(0)

    # State / de-dup
    state_path = Path(".mpc_color_state.json")
    if state_path.exists():
        state = json.loads(state_path.read_text())
        prev_digest = state.get("digest", "")
    else:
        state = {}
        prev_digest = ""

    # Only NEW pairs vs last run
    current_digest = digest_rows(pairs)
    if current_digest == prev_digest:
        print("✅ No new color pairs since last run.")
        sys.exit(0)

    # Persist & append CSV
    out_csv = Path("I3_Color_Alerts.csv")
    if out_csv.exists():
        prev = pd.read_csv(out_csv, parse_dates=["date_center"])
        combined = pd.concat([prev, pairs], ignore_index=True).drop_duplicates(subset=["date_center","pair","color"])
    else:
        combined = pairs

    combined.sort_values(["date_center","pair"]).to_csv(out_csv, index=False)

    # Save state
    state["digest"] = current_digest
    state["last_run_iso"] = pd.Timestamp.utcnow().isoformat()
    state_path.write_text(json.dumps(state, indent=2))

    # Pretty print NEW content (last few rows)
    print("\n🌈 New color pairs detected (latest):")
    latest = pairs.tail(10).copy()
    latest["date_center"] = latest["date_center"].dt.strftime("%Y-%m-%d")
    for _, r in latest.iterrows():
        print(f"  {r['date_center']}  {r['pair']:>4}  = {r['color']:+.3f} mag  "
              f"(n={int(r['n_pts'])}, span={int(r['span_days'])}d)")

    print(f"\n📝 Appended to {out_csv.name}")
    print("💡 Interpretation: more negative g–r or g–o → bluer; more positive → redder.")

if __name__ == "__main__":
    main()
