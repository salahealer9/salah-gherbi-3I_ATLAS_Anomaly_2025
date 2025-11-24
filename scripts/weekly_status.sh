#!/bin/bash
# ============================================================
# weekly_status.sh — 3I/ATLAS watcher weekly heartbeat
# ============================================================

BASE="$HOME/test/3I_ATLAS_Anomaly_2025"
TO="salahealer@gmail.com"

RUNLOG="$BASE/RUN_LOG.md"
I3FILE="$BASE/I3.txt"
HASHFILE="$BASE/I3_hash.txt"

# helper: UTC timestamp
ts() { date -u +"%Y-%m-%d %H:%M:%S UTC"; }

# last 7 days window (UTC)
CUTOFF=$(date -u -d "7 days ago" +"%s")

# counts from RUN_LOG.md (lines that look like table entries starting with '| 20')
WEEK_COUNT=0
if [ -f "$RUNLOG" ]; then
  WEEK_COUNT=$(awk -v cutoff="$CUTOFF" -F'|' '
    # format: | 2025-10-31 18:27:38 UTC | hash | ...
    $2 ~ /^[[:space:]]*[0-9]{4}-[0-9]{2}-[0-9]{2}/ {
      gsub(/^[[:space:]]+|[[:space:]]+$/,"",$2);
      # convert to epoch
      cmd = "date -u -d \"" $2 "\" +%s";
      cmd | getline t; close(cmd);
      if (t >= cutoff) c++;
    }
    END { print c+0 }
  ' "$RUNLOG")
fi

# latest artifacts
LAST_PROOF=$(ls -1t "$BASE"/I3_Color_Proof_*.txt 2>/dev/null | head -n1)
LAST_PNG=$(ls -1t "$BASE"/I3_Color_Brightness_Timeline_*.png 2>/dev/null | head -n1)
LAST_CSV=$(ls -1t "$BASE"/I3_Color_Alerts_*.csv 2>/dev/null | head -n1)

# current/known hash
CUR_HASH="(none)"
[ -f "$I3FILE" ] && CUR_HASH=$(sha256sum "$I3FILE" | awk '{print $1}')
[ -f "$HASHFILE" ] && CUR_HASH=$(cat "$HASHFILE")

# compose body
BODY=$(cat <<EOF
Weekly status for 3I/ATLAS watcher

• Time: $(ts)
• Last 7 days pipeline runs in RUN_LOG.md: $WEEK_COUNT
• Current I3.txt hash: $CUR_HASH

Most recent artifacts:
• Proof: $( [ -n "$LAST_PROOF" ] && basename "$LAST_PROOF" || echo "—" )
• Plot:  $( [ -n "$LAST_PNG" ]   && basename "$LAST_PNG"   || echo "—" )
• CSV:   $( [ -n "$LAST_CSV" ]   && basename "$LAST_CSV"   || echo "—" )

Notes:
– This is an automated heartbeat. If no runs occurred, MPC likely didn’t publish new lines or hashes didn’t change.
– Full details remain in RUN_LOG.md.
EOF
)

SUBJECT="📬 3I/ATLAS Weekly Status — $(date -u +%Y-%m-%d)"
if [ -f "$LAST_PNG" ]; then
  echo "$BODY" | mail -s "$SUBJECT" -a "$LAST_PNG" "$TO"
else
  echo "$BODY" | mail -s "$SUBJECT" "$TO"
fi
