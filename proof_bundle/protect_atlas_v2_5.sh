#!/usr/bin/env bash
# ============================================================
# protect_atlas_v2_5.sh
# Salah-Eddin Gherbi — Cryptographic Archival Script (v2.5)
# ============================================================
# Creates a reproducible protection package for:
# 3I/ATLAS (C/2025 N1) — Photometric–Chromatic Anomaly Project
# Includes: SHA256 manifest → OpenTimestamp → GPG signature → ZIP proof bundle
# ============================================================

set -euo pipefail
export TZ=Europe/London

VERSION="v2.5"
DATE=$(date -u +"%Y%m%d_%H%M")
STAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
REPO="$HOME/test/3I_ATLAS_Anomaly_2025"
PROOF="I3_ATLAS_Proof_${DATE}.txt"
ZIP="I3_ATLAS_ProofBundle_${DATE}.zip"
LOG="RUN_LOG.md"

cd "$REPO"
mkdir -p proof_bundle manifests backup

echo "🚀 Protecting 3I/ATLAS Dataset — Release ${VERSION}"
echo "📅 Timestamp: ${STAMP}"
echo "---------------------------------------------"

# ------------------------------------------------------------
# 1️⃣ Generate SHA256 manifest
# ------------------------------------------------------------
{
  echo "# 3I/ATLAS Research Proof Manifest (${VERSION})"
  echo "Author: Salah-Eddin Gherbi"
  echo "Date: ${STAMP}"
  echo "----------------------------------"
  for f in \
    watch_mpc_colors_plot_v_8_4.py \
    atlas_optical_acceleration_v2.py \
    atlas_optical_color_correlation_v1.py \
    iai_vs_eccentricity.py \
    atlas_anomaly_index.py \
    atlas_delta_v_from_optical_proxy.py \
    atlas_optical_dv_dual.py \
    plot_atlas_optical_accel_deltav.py \
    update_I3_data.sh \
    append_run_log_v3.sh \
    I3.txt \
    I3_Color_Alerts_*.csv \
    I3_Optical_Acceleration_Data.csv \
    I3_Color_Statistics_*.txt \
    I3_Optical_Acceleration_Trend_v2.png \
    I3_Optical_Color_Correlation.png \
    I3_Optical_Color_Correlation_postperi.png \
    iai_vs_eccentricity.png \
    atlas_anomaly_components.png \
    I3_Optical_Acceleration_DeltaV_Figure.png \
    I3_Optical_Acceleration_DeltaV_8_vs_25.png \
    I3_Optical_Acceleration_DeltaV_Overlay.png \
    3I_ATLAS_Anomaly_2025.tex \
    I3_ATLAS_v2_5_Analysis.pdf \
    README_PROOF_v2_5.md \
    RUN_LOG.md; do
      [ -f "$f" ] && printf "%-55s %s\n" "$f" "$(sha256sum "$f" | awk '{print $1}')"
  done
} > "$PROOF"

echo "✅ Manifest created → $PROOF"

# ------------------------------------------------------------
# 2️⃣ OpenTimestamps blockchain sealing
# ------------------------------------------------------------
if command -v ots >/dev/null 2>&1; then
  ots stamp "$PROOF" && echo "✅ OpenTimestamps sealed → ${PROOF}.ots"
else
  echo "⚠️ OpenTimestamps not installed — skipping blockchain stamp"
fi

# ------------------------------------------------------------
# 3️⃣ GPG signature
# ------------------------------------------------------------
if command -v gpg >/dev/null 2>&1; then
  gpg --armor --sign "$PROOF" && echo "✍️  GPG signature created → ${PROOF}.asc"
else
  echo "⚠️ GPG not installed — skipping signature"
fi

# ------------------------------------------------------------
# 4️⃣ Create proof bundle
# ------------------------------------------------------------
zip -r "proof_bundle/$ZIP" \
  "$PROOF" "$PROOF".asc "$PROOF".ots 2>/dev/null || true

zip -ur "proof_bundle/$ZIP" \
  watch_mpc_colors_plot_v_8_4.py \
  atlas_optical_acceleration_v2.py \
  atlas_optical_color_correlation_v1.py \
  iai_vs_eccentricity.py \
  atlas_anomaly_index.py \
  atlas_delta_v_from_optical_proxy.py \
  atlas_optical_dv_dual.py \
  plot_atlas_optical_accel_deltav.py \
  update_I3_data.sh \
  append_run_log_v3.sh \
  I3.txt \
  I3_Color_Alerts_*.csv \
  I3_Optical_Acceleration_Data.csv \
  I3_Color_Statistics_*.txt \
  I3_Optical_Acceleration_Trend_v2.png \
  I3_Optical_Color_Correlation.png \
  I3_Optical_Color_Correlation_postperi.png \
  iai_vs_eccentricity.png \
  atlas_anomaly_components.png \
  I3_Optical_Acceleration_DeltaV_Figure.png \
  I3_Optical_Acceleration_DeltaV_8_vs_25.png \
  I3_Optical_Acceleration_DeltaV_Overlay.png \
  3I_ATLAS_Anomaly_2025.tex \
  I3_ATLAS_v2_5_Analysis.pdf \
  README_PROOF_v2_5.md \
  RUN_LOG.md

echo "📦 Proof bundle created → proof_bundle/$ZIP"

# ------------------------------------------------------------
# 5️⃣ Log update
# ------------------------------------------------------------
HASH=$(sha256sum I3.txt | awk '{print $1}')
{
  echo "| ${STAMP} | \`${HASH}\` | ${PROOF} | proof_bundle/${ZIP} | ${VERSION} – IAI + extended post-perihelion evolution protected |"
} >> "$LOG"

echo "✅ Logged protection entry → $LOG"
echo "✨ Protection complete (${VERSION})"
echo "-------------------------------------------------------------"
