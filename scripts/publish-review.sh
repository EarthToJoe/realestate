#!/usr/bin/env bash
# Publishes the repo's documents to https://realestate.hughesnode.com (house login) for Joe to read on his phone.
#   bash scripts/publish-review.sh
# Run automatically by the git post-commit and post-merge hooks (scripts/install-hooks.sh), so the site follows
# every commit. Static files only: no restart, no container rebuild.
set -euo pipefail
PROJ=/root/projects/realestate
OUT=/srv/hughesnode/apps/realestate/public
[ -d "$OUT" ] || { echo "No hughesnode project yet: hn new realestate --type static" >&2; exit 1; }
uv run --quiet --no-project --with 'markdown==3.7' python3 "$PROJ/scripts/publish_review.py" "$OUT"
