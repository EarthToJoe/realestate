#!/usr/bin/env bash
# Moves this clone from the temporary lifeboat branch in the shorts repo to the real repo, and pushes.
# Run once, after EarthToJoe/realestate exists (private, empty):  bash scripts/repoint-origin.sh
# Uses the same URL scheme (SSH or HTTPS) and therefore the same credentials as the shorts checkout.
set -euo pipefail
cd "$(dirname "$0")/.."
SHORTS_URL=$(git -C /root/projects/shorts remote get-url origin)
REAL=${SHORTS_URL/shorts/realestate}          # same host and scheme, repo name swapped
echo "Shorts remote: $SHORTS_URL"
echo "New remote:    $REAL"
if ! git ls-remote -q "$REAL" >/dev/null 2>&1; then
  echo "Cannot reach $REAL." >&2
  echo "Either the repo does not exist yet, or this VPS's GitHub key is a deploy key limited to shorts." >&2
  if [ -f /root/.ssh/id_ed25519.pub ] || [ -f /root/.ssh/id_rsa.pub ]; then
    echo "If it is a deploy key, add this public key to the new repo (Settings, Deploy keys, Add, allow write):" >&2
    cat /root/.ssh/id_ed25519.pub /root/.ssh/id_rsa.pub 2>/dev/null >&2
  fi
  exit 1
fi
git remote set-url origin "$REAL"
git checkout -q -B main
# The cloud session may already have pushed to the new repo; take its commits first (fast-forward only).
if git fetch -q origin main 2>/dev/null; then git merge -q --ff-only origin/main || { echo "Local and remote main diverged; ask the session to merge." >&2; exit 1; }; fi
git push -u origin main
echo "origin is now $REAL; main pushed. The lifeboat branch in shorts can be deleted with:"
echo "  git push $SHORTS_URL --delete realestate-lifeboat"
