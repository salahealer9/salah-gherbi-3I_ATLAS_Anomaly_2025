#!/bin/bash
# =============================================================
# cleanup_old_runs.sh — archival cleanup for 3I/ATLAS pipeline
# Author: Salah-Eddin Gherbi
# Purpose: Keep recent verified runs, archive older ones safely
# =============================================================

cd ~/test/3I_ATLAS_Anomaly_2025 || exit

echo "🧹 Starting cleanup and archival process — $(date -u)"

# === Create archive folder if missing ===
mkdir -p archive

# === Move older proof bundles (>10 latest) into monthly archives ===
echo "📦 Archiving old proof bundles..."
ls -1t I3_ATLAS_ProofBundle_*.zip 2>/dev/null | tail -n +11 | while read -r file; do
    month=$(echo "$file" | cut -c19-24)  # Extract YYYYMM
    tarfile="archive/proofbundles_${month}.tar.gz"
    tar -rf "$tarfile" "$file" 2>/dev/null || tar -cf "$tarfile" "$file"
    rm -f "$file"
    echo "  → archived $file → $tarfile"
done

# === Move older backups (>10 latest) into monthly archives ===
echo "📦 Archiving old backups..."
ls -1t I3_backup_*.txt 2>/dev/null | tail -n +11 | while read -r file; do
    month=$(echo "$file" | cut -c11-16)
    tarfile="archive/backups_${month}.tar.gz"
    tar -rf "$tarfile" "$file" 2>/dev/null || tar -cf "$tarfile" "$file"
    rm -f "$file"
    echo "  → archived $file → $tarfile"
done

# === Remove intermediate files older than 14 days ===
echo "🗑️ Cleaning intermediate CSVs older than 14 days..."
find . -name "I3_Color_Alerts_*.csv" -type f -mtime +14 -print -delete

# === Summary ===
echo "✅ Cleanup complete."
echo "   Latest 10 proof bundles and backups retained."
echo "   Older runs safely archived under ./archive/"
