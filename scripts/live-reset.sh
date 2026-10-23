#!/usr/bin/env bash
# Resets the shared live deal to the start of the demo (as "Start demo" does), so Joe begins with Start demo; every
# step is then one tap away with fast-forward. Prints the live model spend from the page footer.
#   bash scripts/live-reset.sh
set -euo pipefail
BASE=${1:-https://realestate.hughesnode.com}
AUTH=(-u ":$(cat /srv/realestate/secrets/HOUSE_PASSWORD)")   # house login, blank username; never in the repo
OUT=$(mktemp)
curl -s "${AUTH[@]}" -X POST "$BASE/demo/reset" -o /dev/null -w "reset -> HTTP %{http_code}\n"
curl -s "${AUTH[@]}" "$BASE/brand" -o "$OUT" -w "step 10 after the reset -> HTTP %{http_code}\n"
grep -q 'id="gate-card"' "$OUT" && echo "ok   the deal is at the start (step 10 shows its gate card)"
grep -o 'Live model spend so far \$[0-9.]*' "$OUT" | head -1
rm -f "$OUT"
