#!/usr/bin/env bash
# ============================================================
# append_run_log_v2.sh
# Salah-Eddin Gherbi — Extended run log index
# ============================================================
# Appends a new entry into RUN_LOG.md with color-trend summary
# ------------------------------------------------------------
set -euo pipefail
export TZ=Europe/London

LOG="RUN_LOG.md"
DATE=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

# find latest key files
LAST_PROOF=$(ls -1t I3_Color_Proof_*.txt 2>/dev/null | head -n1 || echo "—")
LAST_PNG=$(ls -1t I3_Color_Brightness_Timeline_*.png 2>/dev/null | head -n1 || echo "—")
LAST_CSV=$(ls -1t I3_Color_Alerts_*.csv 2>/dev/null | head -n1 || echo "—")
HASH=$(sha256sum I3.txt | awk '{print $1}')

# --- extract mean colors from CSV if available ---
NOTES="—"
if [ -f "$LAST_CSV" ]; then
  # compute mean color per pair using awk
  MEAN_GO=$(awk -F, '/g-o/{sum+=$3; n++} END{if(n>0) printf "%.3f", sum/n}' "$LAST_CSV" 2>/dev/null || echo "—")
  MEAN_GR=$(awk -F, '/g-r/{sum+=$3; n++} END{if(n>0) printf "%.3f", sum/n}' "$LAST_CSV" 2>/dev/null || echo "—")
  MEAN_RO=$(awk -F, '/r-o/{sum+=$3; n++} END{if(n>0) printf "%.3f", sum/n}' "$LAST_CSV" 2>/dev/null || echo "—")
  NOTES="Δ(g-o)=${MEAN_GO}, Δ(g-r)=${MEAN_GR}, Δ(r-o)=${MEAN_RO}"
fi

echo "🪶 Updating run log for $DATE"

# create header if missing
if [ ! -f "$LOG" ]; then
  cat <<EOF > "$LOG"
# 🧭 3I/ATLAS Photometric Analysis — Run Log Index
Author: Salah-Eddin Gherbi  
Repository: [GitHub](https://github.com/salahealer9/salah-gherbi-3I_ATLAS_Anomaly_2025)  
ORCID: [0009-0005-4017-1095](https://orcid.org/0009-0005-4017-1095)  

Each entry records an analysis session with associated files, hashes, and blockchain proofs.

| Date (UTC) | SHA256 of I3.txt | Proof Manifest | CSV | Timeline Plot | Color Summary |
|-------------|------------------|----------------|-----|----------------|----------------|
EOF
fi

# append the new entry
echo "| $DATE | \`$HASH\` | $LAST_PROOF | $LAST_CSV | $LAST_PNG | $NOTES |" >> "$LOG"

echo "✅ Logged analysis entry → $LOG"
