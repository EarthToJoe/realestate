#!/usr/bin/env bash
# Moves this clone from the temporary lifeboat branch in the shorts repo to the real repo, and pushes.
# Run once, after EarthToJoe/realestate exists (private, empty):  bash scripts/repoint-origin.sh
set -euo pipefail
cd "$(dirname "$0")/.."
REAL=https://github.com/EarthToJoe/realestate.git
git ls-remote -q "$REAL" >/dev/null 2>&1 || { echo "Cannot reach $REAL yet (does it exist? is git logged in?)." >&2; exit 1; }
git remote set-url origin "$REAL"
git checkout -q -B main
git push -u origin main
echo "origin is now $REAL; main pushed. The lifeboat branch in shorts can be deleted:"
echo "  git push https://github.com/EarthToJoe/shorts.git --delete realestate-lifeboat"
