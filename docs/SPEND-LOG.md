# API spend log (per workstream)

Where the $200 credit (expires 2026-11-08) goes. Three sources:
1. **The POC's own model calls**: logged by the app in its `model_call` table (module, task, model, tokens in /
   cache write / cache read / out, cost, time, live or replay); the footer of every screen shows the live total
   against the $12 cap. A roll-up script comes with slice 4; until then the rows are copied here by hand.
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

## The POC app's own model calls

| Date | Where | Task | Model | Tokens in / cache write / out | Cost (USD) | Why |
|---|---|---|---|---|---|---|
| 2026-10-23 | local, `scripts/record-replays.py` | intake.infer_gaps | claude-haiku-5-5 | 2,637 / 1,195 / 924 | 0.000875 | Prove the live provider; record the demo-house replay |
| 2026-10-23 | local, `scripts/record-replays.py` | probe.mask_roundtrip (T6) | claude-haiku-5-5 | 406 / 0 / 123 | 0.000102 | Try-first check T6 (PII tokens round trip) |

| 2026-10-23 | local, `scripts/slice2-models.py compare` | pricing.recommend, copy.draft (Haiku run), 6 fairhousing.review, intake | claude-haiku-5-5 | 12,339 in, 3,095 cache write, 19,613 cache read / 12,478 out | 0.008056 | Side-by-side, Haiku arm |
| 2026-10-23 | local, `scripts/slice2-models.py compare` | pricing.recommend, copy.draft (Sonnet run), 6 fairhousing.review (Haiku), intake | claude-sonnet-5-5 + Haiku | 12,334 in, 2,943 cache write, 19,765 cache read / 9,447 out | 0.086444 | Side-by-side, Sonnet arm |
| 2026-10-23 | local, `scripts/slice2-models.py record` | the steps 2 to 4 demo run (9 calls, replays committed) | Sonnet + Haiku | not kept (run database rebuilt by the replay check) | 0.0829 | Replays the hosted demo uses |
| 2026-10-23 | local, `pytest --live` | fairhousing.review on 58 fixture phrases | claude-haiku-5-5 | not kept (pytest temp database) | ~0.02 (estimate) | Fixture replays; A8 measurement |
| 2026-10-23 | local, first compare attempt | Haiku copy.draft cut off at 4,000 tokens (raised; not logged) | claude-haiku-5-5 | ~4,000 out | ~0.004 (estimate) | Led to `max_tokens` 8,000 |

**App live spend so far: about $0.20** (slice 1 $0.001; slice 2 about $0.20, $0.18 of it logged by the app and the
rest estimated as marked) of the $12 app cap (inside the $15 demo reserve). The hosted app answers the demo house,
steps 1 to 4, from the recorded replays at no cost (its footer reads $0.0000); tests use the fake provider.

## 2026-10-23, morning: original idea re-spec and build slice 1 (credit, then Max: decision 22)

| Tag | What | Cost (USD) | Billed to |
|---|---|---|---|
| RESPEC-A | Architecture spec, traceability and out-of-scope revised for decision 21 | 2.58 | API credit |
| RESPEC-B | Executive summary, plan, assumptions, questions rewritten around the original idea; contract-route research | 4.31 | API credit |
| BUILD-1 | Slice 1: skeleton, Step 1 Intake, first timeline, docker hosting, T1 to T8 | 8.31 | API credit |
| setup | Smoke test of a job on the Max login | 0.00 notional | Max plan |
| BUILD-2 | Slice 2: pricing, listing copy and the fair-housing pipeline (39/39 planted phrases caught), marketing plan | 8.43 | API credit |
| BUILD-3 | Slice 3, first half: pricing reconciled with the demo-house research ($610k to $650k), Step 5 Communications, Step 6 Offers | 3.95 | API credit |
| BUILD-3 | Slice 3, second half (running): Step 7 Contract, Step 8 Buyer side; resumed with its context | running | Max plan |

**Credit after BUILD-1: $171.26 spent; $15 reserved for the demo's own calls; $13.74 left for BUILD-2.** The app's
own live calls so far: $0.001 (two Haiku calls recording the replay).

**The credit is used down to its reserve (2026-10-23, 11:47 UTC).** Headless jobs: $183.64 of $200. The app's own
live calls so far: about $0.35 (recording replays). That leaves about $16 on the key: the $15 reserve for the demo's
live calls at the meeting, and $1.36 the runner will not start a job with. From here every job runs on the Max plan
(decision 22); `scripts/spend-summary.sh` shows their notional cost separately.
