#!/usr/bin/env bash
# Rolls /srv/realestate/spend.jsonl (one line per api-run job) into a per-tag table printed to stdout.
# Paste or append the table into docs/SPEND-LOG.md at each milestone.
python3 - <<'PYEOF'
import json, collections, os
p = "/srv/realestate/spend.jsonl"
if not os.path.exists(p): print("no runs yet"); raise SystemExit
tot = collections.defaultdict(lambda: [0, 0.0, 0, 0])
for line in open(p):
    r = json.loads(line); t = tot[r.get("tag", "general")]
    t[0] += 1; t[1] += r.get("cost_usd") or 0; t[2] += r.get("input") or 0; t[3] += r.get("output") or 0
print("| Tag | Runs | Cost (USD) | Tokens in | Tokens out |\n|---|---|---|---|---|")
g = 0.0
for k, (n, c, i, o) in sorted(tot.items()):
    g += c; print(f"| {k} | {n} | {c:.2f} | {i:,} | {o:,} |")
print(f"\n**Total headless-job spend against the credit: ${g:.2f}** (the POC app's own calls and Console totals are added separately)")
PYEOF
