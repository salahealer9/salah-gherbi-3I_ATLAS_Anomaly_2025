#!/bin/bash
set -euo pipefail

FILE=${1:-}

if [ -z "$FILE" ]; then
  echo "Usage: $0 <manifest-file>"
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "Error: file '$FILE' not found."
  exit 1
fi

# ------------------------------------------------------------
# Clean up old proof files so we can safely recreate them
# ------------------------------------------------------------
for ext in sha256 asc ots; do
  if [ -f "$FILE.$ext" ]; then
    echo "🧹 Removing existing $FILE.$ext"
    rm -f "$FILE.$ext"
  fi
done

# ------------------------------------------------------------
# Recreate checksum, signature, and OpenTimestamps proof
# ------------------------------------------------------------
echo "🔐 Protecting $FILE"

sha256sum "$FILE" > "$FILE.sha256"
gpg --armor --detach-sign "$FILE"
ots stamp "$FILE"

echo "=== Protection complete ==="
echo "$FILE.sha256"
echo "$FILE.asc"
echo "$FILE.ots"

