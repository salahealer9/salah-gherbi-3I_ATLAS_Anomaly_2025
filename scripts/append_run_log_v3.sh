#!/usr/bin/env bash
# ============================================================
# append_run_log_v2.sh
# Salah-Eddin Gherbi — Extended run log index (v3 with perihelion summary)
# ============================================================
# Appends a new entry into RUN_LOG.md with detailed color-trend and perihelion diagnostics
# ------------------------------------------------------------
set -euo pipefail
export TZ=Europe/London

LOG="RUN_LOG.md"
DATE=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
PERIHELION="2025-10-29T00:00:00Z"

# --- find latest key files ---
LAST_PROOF=$(ls -1t I3_Color_Proof_*.txt 2>/dev/null | head -n1 || echo "—")
LAST_PNG=$(ls -1t I3_Color_Brightness_Timeline_*.png 2>/dev/null | head -n1 || echo "—")
LAST_CSV=$(ls -1t I3_Color_Alerts_*.csv 2>/dev/null | head -n1 || echo "—")
HASH=$(sha256sum I3.txt | awk '{print $1}')

# ------------------------------------------------------------
#  Compute color statistics vs Solar
# ------------------------------------------------------------
SOLAR_GR=0.440
SOLAR_GO=0.620
SOLAR_RO=0.180
NOTES="⚠️ No CSV data available."

if [ -f "$LAST_CSV" ]; then
  analyze_color () {
    local pair=$1 solar=$2
    awk -F, -v pair="$pair" -v solar="$solar" '
      $2==pair {
        sum+=$3; sum2+=$3*$3; n++
        if($1 < "2025-10-29") pre++ ; else post++
      }
      END {
        if(n>1){
          mean=sum/n
          std=sqrt((sum2/n)-(mean*mean))
          diff=mean-solar
          sigma=(std>0)?diff/std:0
          trend=(diff<0)?"BLUER":((diff>0)?"REDDER":"NEUTRAL")
          printf "%-4s: %.3f ± %.3f (Δ=%+.3f, %.1fσ → %s) | pre=%d post=%d\n", pair, mean, std, diff, sigma, trend, pre, post
        }
      }' "$LAST_CSV"
  }

  SUM_GR=$(analyze_color "g-r" $SOLAR_GR)
  SUM_GO=$(analyze_color "g-o" $SOLAR_GO)
  SUM_RO=$(analyze_color "r-o" $SOLAR_RO)

  # --- Determine global perihelion coverage summary ---
  PRE=$(awk -F, '$1 < "2025-10-29" {n++} END{print n+0}' "$LAST_CSV")
  POST=$(awk -F, '$1 >= "2025-10-29" {n++} END{print n+0}' "$LAST_CSV")
  PHASE_MSG="Perihelion: ${PERIHELION} → pre=$PRE, post=$POST"
  if (( POST == 0 )); then
    PHASE_MSG="$PHASE_MSG ⚠️ No post-perihelion data yet."
  fi

  NOTES="📊 === Solar Comparison Summary ===\n$SUM_GR$SUM_GO$SUM_RO\n$PHASE_MSG"
fi

# ------------------------------------------------------------
#  Prepare log header if missing
# ------------------------------------------------------------
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

# ------------------------------------------------------------
#  Append new entry with summary block
# ------------------------------------------------------------
{
  echo "| $DATE | \`$HASH\` | $LAST_PROOF | $LAST_CSV | $LAST_PNG | See below |"
  echo ""
  echo "\`\`\`"
  echo -e "$NOTES"
  echo "\`\`\`"
  echo ""
} >> "$LOG"

echo "✅ Logged analysis entry → $LOG"
