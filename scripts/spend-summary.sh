#!/usr/bin/env bash
# Rolls /srv/realestate/spend.jsonl (one line per api-run job) into a per-tag table printed to stdout.
# Paste or append the table into docs/SPEND-LOG.md at each milestone.
python3 - <<'PYEOF'
import json, collections, os
p = "/srv/realestate/spend.jsonl"
if not os.path.exists(p): print("no runs yet"); raise SystemExit
tot = collections.defaultdict(lambda: [0, 0.0, 0, 0])
for line in open(p):
    r = json.loads(line); t = tot[(r.get("billing", "api"), r.get("tag", "general"))]
    t[0] += 1; t[1] += r.get("cost_usd") or 0; t[2] += r.get("input") or 0; t[3] += r.get("output") or 0
print("| Billed to | Tag | Runs | Cost (USD) | Tokens in | Tokens out |\n|---|---|---|---|---|---|")
g = collections.defaultdict(float)
for (b, k), (n, c, i, o) in sorted(tot.items()):
    g[b] += c; print(f"| {'API credit' if b == 'api' else 'Max plan'} | {k} | {n} | {c:.2f} | {i:,} | {o:,} |")
print(f"\n**Headless-job spend against the credit: ${g['api']:.2f}** (the POC app's own calls and Console totals are added separately)")
if g["max"]:
    print(f"\n**Run on the Max plan: ${g['max']:.2f} notional** (what the API would have charged; the plan bills nothing extra)")
PYEOF
