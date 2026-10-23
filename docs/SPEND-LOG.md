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
| 2026-10-23 | WS1 to WS7, memo, architecture, fact-check, plan | Night of 2026-10-23, all logged per job; see the table below | | | | api-run |

## Per-workstream totals (2026-10-23, end of night; `scripts/spend-summary.sh`)

| Tag | Runs | Cost (USD) | Tokens in | Tokens out |
|---|---|---|---|---|
| FACTCHECK | 1 | 2.16 | 164 | 50,435 |
| PLAN | 1 | 3.50 | 52 | 57,999 |
| WS1 | 1 | 11.80 | 174 | 166,160 |
| WS2 | 2 | 25.96 | 98 | 50,274 |
| WS3 | 1 | 36.28 | 56 | 103,798 |
| WS4 | 1 | 10.18 | 174 | 140,245 |
| WS5 | 2 | 36.40 | 206 | 174,381 |
| WS6 | 1 | 11.42 | 240 | 154,364 |
| WS7 | 4 | 18.30 | 556 | 319,922 |
| setup | 1 | 0.08 | 4 | 310 |

**Total headless-job spend against the credit: $156.07** (the POC app's own calls and Console totals are added separately)

What the tags cover: WS1 to WS6 = gap fill and deliverable per workstream (WS2 also the father-in-law memo, $1.04;
WS5 = first run $23.21 whose helpers were cut off, plus the resume $13.19); WS7 = POC building-blocks gap fill
$8.29, Alexandria data stopped ~$1.00 (estimated), Holmes house data $7.48, architecture and traceability $1.52;
FACTCHECK = independent check on Sonnet; PLAN = assumptions, questions, plan and executive summary.

**Running total against the credit: $156.07** of $200; **about $44 left, of which $15 is reserved** for the demo's
own model calls (decision 19). Cross-check: the Anthropic Console usage page.
