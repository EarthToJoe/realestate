# API spend log (per workstream)

Where the $200 credit (expires 2026-11-08) goes. Two sources:
1. **The POC's own model calls**: logged by the app to `app/data/spend.jsonl` (module, tokens in/out, cost,
   time) and rolled up here by `scripts/spend-summary.sh` (to be written with the POC).
2. **The Claude Code session on the VPS**: once it runs on the API key, the Anthropic Console usage page shows
   it per key; totals are copied here by hand at each milestone.

The research done in the **cloud** session on day 1 ran on Joe's Max plan and does not draw on the credit; Joe
has since asked that everything run on the credit, so from the VPS session onward every line here is credit spend.

| Date | Workstream | What | Tokens in | Tokens out | Cost (USD) | Source |
|---|---|---|---|---|---|---|
| 2026-10-23 | WS1 to WS6 | Twelve research passes (cloud session) | n/a | n/a | 0 against the credit (Max plan) | cloud session |

**Running total against the credit: $0.00**
