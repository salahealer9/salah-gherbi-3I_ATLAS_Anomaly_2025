#!/bin/bash
# ============================================================
# check_mpc_update.sh — MPC watcher with email + popup notice
# ============================================================
# Author: Salah-Eddin Gherbi
# Purpose: Automatically detect new MPC data for 3I/ATLAS,
#          run analysis pipeline, and email results.
# ------------------------------------------------------------

URL="https://www.minorplanetcenter.net/tmp2/3I.txt"
LOCAL_FILE="$HOME/test/3I_ATLAS_Anomaly_2025/I3.txt"
HASH_FILE="$HOME/test/3I_ATLAS_Anomaly_2025/I3_hash.txt"
UPDATE_SCRIPT="$HOME/test/3I_ATLAS_Anomaly_2025/update_I3_data.sh"
TO="salahealer@gmail.com"

# ------------------------------------------------------------
# Timestamp helper
# ------------------------------------------------------------
timestamp_utc() {
  date -u +"%Y-%m-%d %H:%M:%S UTC"
}

# ------------------------------------------------------------
# Simple notification (email + optional popup)
# ------------------------------------------------------------
notify() {
  local subject="$1"
  local body="$2"
  printf "%s\n" "$body" | mail -s "$subject" "$TO" || true
  command -v notify-send >/dev/null 2>&1 && notify-send "$subject" "$body"
}

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
curl -s -L "$URL" -o "$LOCAL_FILE.new"
if [ $? -ne 0 ] || [ ! -s "$LOCAL_FILE.new" ]; then
  notify "⚠️ 3I/ATLAS watcher: download failed" \
         "Could not fetch I3.txt from MPC at $(timestamp_utc)."
  exit 1
fi

if [ -f "$HASH_FILE" ]; then
  old_hash=$(cat "$HASH_FILE")
  new_hash=$(sha256sum "$LOCAL_FILE.new" | cut -d' ' -f1)

  if [ "$old_hash" != "$new_hash" ]; then
    mv "$LOCAL_FILE.new" "$LOCAL_FILE"
    echo "$new_hash" > "$HASH_FILE"

    # --------------------------------------------------------
    # A. Notify new data detected
    # --------------------------------------------------------
    notify "🚀 3I/ATLAS Update Detected — $(timestamp_utc)" \
"New MPC dataset retrieved from:
$URL

Hash changed:
Old: ${old_hash:-N/A}
New: $new_hash

Launching analysis pipeline (update_I3_data.sh)...
You will receive another email when processing completes."

    # --------------------------------------------------------
    # B. Run full pipeline
    # --------------------------------------------------------
    if bash "$UPDATE_SCRIPT"; then
      LAST_PROOF=$(ls -1t "$HOME"/test/3I_ATLAS_Anomaly_2025/I3_Color_Proof_*.txt 2>/dev/null | head -n1)
      LAST_PNG=$(ls -1t "$HOME"/test/3I_ATLAS_Anomaly_2025/I3_Color_Brightness_Timeline_*.png 2>/dev/null | head -n1)
      LAST_CSV=$(ls -1t "$HOME"/test/3I_ATLAS_Anomaly_2025/I3_Color_Alerts_*.csv 2>/dev/null | head -n1)

      # ------------------------------------------------------
      # C. Enhanced success email with attachment
      # ------------------------------------------------------
      SUBJECT="✅ 3I/ATLAS Pipeline Complete — $(timestamp_utc)"
      BODY=$(cat <<EOF
Analysis and verification completed successfully.

Output summary:
 • Proof: $(basename "$LAST_PROOF")
 • Plot:  $(basename "$LAST_PNG")
 • CSV:   $(basename "$LAST_CSV")

All results are GPG-signed and blockchain-sealed.
Run log entry recorded in RUN_LOG.md.

📍 Timestamp: $(timestamp_utc)
EOF
)
      if [ -f "$LAST_PNG" ]; then
        echo "$BODY" | mail -s "$SUBJECT" -A "$LAST_PNG" "$TO"
      else
        echo "$BODY" | mail -s "$SUBJECT" "$TO"
      fi
      command -v notify-send >/dev/null 2>&1 && \
        notify-send "✅ 3I/ATLAS Update Complete" "Results sent by email with plot attachment."
    else
      notify "❌ 3I/ATLAS Pipeline Error — $(timestamp_utc)" \
             "The update pipeline reported a failure. Check RUN_LOG.md and $UPDATE_SCRIPT."
    fi

  else
    rm "$LOCAL_FILE.new"
    echo "[$(timestamp_utc)] No new MPC data."
    # Uncomment below if you also want an email when unchanged
    # notify "ℹ️ 3I/ATLAS: No new MPC data" "Hash unchanged: $new_hash"
  fi

else
  # ----------------------------------------------------------
  # First-time initialization
  # ----------------------------------------------------------
  mv "$LOCAL_FILE.new" "$LOCAL_FILE"
  sha256sum "$LOCAL_FILE" | cut -d' ' -f1 > "$HASH_FILE"
  notify "🪶 3I/ATLAS watcher initialized" \
         "Tracking started at $(timestamp_utc).
Initial hash: $(cat "$HASH_FILE")"
fi
