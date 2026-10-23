# API spend log (per workstream)

Where the $200 credit (expires 2026-11-08) goes. Three sources:
1. **The POC's own model calls**: logged by the app to `app/data/spend.jsonl` (module, tokens in/out, cost,
   time) and rolled up here by `scripts/spend-summary.sh` (to be written with the POC).
2. **Headless jobs on the VPS** (`scripts/api-run.sh`): one line per run in `/srv/realestate/spend.jsonl`, rolled
   up per workstream tag by `scripts/spend-summary.sh` and pasted here at each milestone.
3. **The Anthropic Console usage page** for the key, as the cross-check.

The research done in the **cloud** session on day 1 ran on Joe's Max plan and does not draw on the credit; Joe
has since asked that everything run on the credit, so from the VPS session onward every line here is credit spend.

| Date | Workstream | What | Tokens in | Tokens out | Cost (USD) | Source |
|---|---|---|---|---|---|---|
| 2026-10-23 | WS1 to WS6 | Twelve research passes (cloud session) | n/a | n/a | 0 against the credit (Max plan) | cloud session |
| 2026-10-23 | setup | Smoke test of the headless job pipeline (VPS) | 2 turns | | 0.08 | api-run |

| 2026-10-23 | WS4 | Gap fill + cost-model deliverable | | | 10.18 | api-run |
| 2026-10-23 | WS5 | Gap fill + competitors, first run (helpers stopped by the wait ceiling; nothing written) | | | 23.21 | api-run |
| 2026-10-23 | WS7 | Gap fill, POC building blocks | | | 8.29 | api-run |
| 2026-10-23 | WS7 | Demo-house data for Alexandria, stopped after 2 min when the address changed | | | ~1.00 (estimated) | transcript |
| 2026-10-23 | WS1, WS2, WS3, WS6, WS5 resume, Holmes data | Still running at 03:57; estimated from transcripts so far: WS3 ~27.8, WS2 ~13.5, WS1 ~9.1, WS6 ~8.3, WS5 resume ~7.6, web searches ~7 | | | ~73 (estimated) | transcripts |

**Running total against the credit: $42.76 logged, about $125 including the running jobs' use so far** (2026-10-23
03:57 UTC). Estimates use per-token prices fitted from finished jobs' own cost breakdowns (they reproduce WS4 and
WS7 to the cent). The Anthropic Console is the cross-check. Decision 19 sets the caps from here.
