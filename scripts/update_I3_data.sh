#!/usr/bin/env bash
# ============================================================
# update_I3_data.sh
# Salah-Eddin Gherbi — Automated MPC update + pipeline runner
# ============================================================

echo "🌐 Fetching latest 3I/ATLAS MPC data..."
curl -s -L "https://www.minorplanetcenter.net/tmp2/3I.txt" -o I3.txt

if [ $? -ne 0 ] || [ ! -s I3.txt ]; then
  echo "❌ Failed to download I3.txt — check your network or MPC link."
  exit 1
fi

echo "✅ Downloaded latest I3.txt ($(wc -l < I3.txt) lines)"

# ============================================================
# 🔍 Detect if new data lines were added since last run
# ============================================================
if [ -f "I3_previous_hash.txt" ]; then
  old_hash=$(cat I3_previous_hash.txt)
else
  old_hash=""
fi

new_hash=$(sha256sum I3.txt | awk '{print $1}')

if [ "$new_hash" = "$old_hash" ]; then
  echo "🟡 No new MPC data detected — skipping analysis."
  echo "    (File hash unchanged: $new_hash)"
  exit 0
else
  echo "🆕 New data detected — continuing analysis."
  echo "$new_hash" > I3_previous_hash.txt
fi

echo "---------------------------------------------"
echo "📆 Last dataset hash: $old_hash"
echo "📆 Current dataset hash: $new_hash"
echo "---------------------------------------------"

mkdir -p backup
if [ -f I3.txt ]; then
  cp I3.txt "backup/I3_$(date -u +%Y%m%d_%H%M).txt"
fi

set -euo pipefail
export MPLBACKEND=Agg
export TZ=Europe/London

REPO="$HOME/test/3I_ATLAS_Anomaly_2025"
VENV="$HOME/book4/venv/bin/activate"
SCRIPT="watch_mpc_colors_plot_v_8_4.py"
DATE=$(date -u +"%Y%m%d_%H%M%S")

cd "$REPO"
source "$VENV"

echo "🚀 Starting MPC data update and analysis: $DATE"
echo "---------------------------------------------"

# 1️⃣ BACKUP
if [ -f I3.txt ]; then
  cp I3.txt "I3_backup_${DATE}.txt"
  echo "🗄️  Backup created: I3_backup_${DATE}.txt"
fi

# 2️⃣ FETCH NEW DATA (manual or remote)
if [ -f I3_new.txt ]; then
  echo "📥 Found local file I3_new.txt → appending to master"
  cat I3_new.txt >> I3.txt
  rm -f I3_new.txt
else
  echo "⚠️ No local I3_new.txt found — skipping download step"
fi

# 3️⃣ CLEAN DUPLICATES
sort I3.txt | uniq > I3_clean.tmp && mv I3_clean.tmp I3.txt
echo "🧹 Cleaned duplicate lines → I3.txt refreshed"

# 4️⃣ VERIFY FILE HEALTH
LINES=$(grep -c "^0003I" I3.txt || true)
echo "✅ $LINES total MPC records found in I3.txt"

# 5️⃣ RUN THE MAIN PIPELINE
echo "⚙️  Running analysis pipeline..."
python3 "$SCRIPT"

# 6️⃣ FIND THE LATEST PROOF MANIFEST
PROOF=$(ls -1t I3_Color_Proof_*.txt 2>/dev/null | head -n1 || true)
if [ -n "$PROOF" ]; then
  echo "🔏 Found proof manifest: $PROOF"

  # --- Check for existing timestamp before sealing ---
  if [ -f "$PROOF.ots" ]; then
    echo "🟢 Timestamp already exists → skipping reseal"
    echo "- $(date -u +'%F %T') UTC: Timestamp already existed for $PROOF" >> RUN_LOG.md
  else
    ots stamp "$PROOF" && echo "✅ OpenTimestamps sealed"
    echo "- $(date -u +'%F %T') UTC: Timestamp created for $PROOF" >> RUN_LOG.md
  fi

  # --- Sign the proof (always fresh GPG signature) ---
  gpg --armor --sign "$PROOF" && echo "✍️  GPG signature created"
  echo "- $(date -u +'%F %T') UTC: GPG signature created for $PROOF" >> RUN_LOG.md

else
  echo "⚠️  No proof manifest found — skipping sealing"
  echo "- $(date -u +'%F %T') UTC: No proof manifest found (skipped)" >> RUN_LOG.md
fi

# 7️⃣ OPTIONAL — CREATE ZIP BUNDLE (enhanced for v2.2+)
if [ -n "$PROOF" ]; then
  ZIP="I3_ATLAS_ProofBundle_${DATE}.zip"
  echo "🗜️  Creating full proof bundle (v2.2 layout)..."

  zip -r "$ZIP" \
    I3_Color_Alerts_*.csv \
    I3_Color_Statistics_*.txt \
    I3_Color_Brightness_Timeline_*.png \
    I3_Optical_Acceleration_Trend*.png \
    I3_Optical_Color_Correlation*.png \
    "$PROOF" "$PROOF".ots "$PROOF".asc \
    RUN_LOG.md CITATION.cff README_PROOF*.md manifest_v2_2.txt \
    2>/dev/null || true

  echo "📦 Proof bundle created: $ZIP"
  echo "🧾 Included: All CSV, TXT, PNG (including post-perihelion), Proofs + Metadata"
fi


echo "✨ Done — all new data processed, verified, and sealed."
echo "-------------------------------------------------------------"

# 8️⃣ Append to RUN_LOG.md with color summary
./append_run_log_v3.sh