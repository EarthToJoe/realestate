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
| 2026-10-23 | local, `scripts/slice2-models.py record` (BUILD-3) | steps 2 to 4 re-recorded after the pricing fix (10 calls) | Sonnet + Haiku | not kept | 0.0964 | Pricing reconciled with the demo-house research |
| 2026-10-23 | local (BUILD-3, first half) | steps 5 and 6 recorded (9 calls) | Sonnet + Haiku | not kept | 0.0240 | Replays for the first steps 5 and 6 |
| 2026-10-23 | hosted, `scripts/live-flow.sh` (BUILD-3, first half) | replay misses on steps 5 and 6 went live | Sonnet + Haiku | not kept | 0.0295 | The live walk before those replays shipped |
| 2026-10-23 | local, `scripts/slice3-models.py record`, run 1 | buyer.alert, buyer.offer_advise, offers.advise, 2 fairhousing.review | Sonnet + Haiku | 3,397 in / 6,238 out | 0.0486 | Walk took offer A; the contract call was refused by the SDK (not billed) |
| 2026-10-23 | local, `scripts/slice3-models.py record`, run 2 | offers.advise, buyer.counter_advise, contract.draft (Sonnet) | claude-sonnet-5-5 | 2,741 in / 19,832 out | 0.2109 | After offer A was made realistic weaker paper |
| 2026-10-23 | local, `scripts/slice3-models.py compare` | contract.draft (Opus, `draft.v1`) | claude-opus-5-5 | 1,587 in / 14,114 out | 0.2976 | The spec's Opus/Sonnet contract side-by-side |
| 2026-10-23 | local, `scripts/slice3-models.py record`, run 3 | contract.draft (Opus, `draft.v2`) | claude-opus-5-5 | 1,595 in / 12,841 out | 0.2731 | The shipped contract replay (decision 36) |
| 2026-10-23 | local, `scripts/slice4-models.py record` (BUILD-4) | brand.campaign (Sonnet) and 4 fairhousing.review (Haiku): step 10's replays | Sonnet + Haiku | not kept (the run database was rebuilt by the next run; the script now keeps a ledger) | ~0.01 (estimate from the slice-2 per-call measurements) | Replays for step 10, so the whole demo runs at $0 |
| 2026-10-23 | local, `scripts/slice4-models.py record` (BUILD-POLISH) | offers.advise, buyer.counter_advise (Sonnet), contract.draft (Opus), brand.campaign (Sonnet), 4 fairhousing.review (Haiku) | Opus + Sonnet + Haiku | 4,163 in / 18,216 out | 0.3149 | Fees set to WS4 ($4,500 / $3,500); every request that carried them re-recorded (decision 46) |

**App live spend after the fee fix (BUILD-POLISH): about $1.52** (the fee fix re-recorded 8 calls for $0.3149, decision 46; the hosted app still $0.0295). **After slice 4: about $1.20** (slice 4 added about $0.01, the step-10 recording; the hosted app's own live calls are $0.0295 in all, rolled up below). Before slice 4: **about $1.19** (slice 1 $0.001; slice 2 about $0.20; slice 3 $0.98: the pricing fix
$0.10, steps 5 and 6 $0.05, the slice-3 recordings and the contract side-by-side $0.83) of the $12 app cap (inside
the $15 demo reserve on the API key). The hosted app answers the whole demo walk, steps 1 to 8, from the recorded
replays at no cost: a local replay-mode walk of `scripts/live-flow.sh` ends at $0.0000. Tests use the fake
provider. A fully live run of the walk would cost about $0.50 (the Opus contract about $0.27 of it) [INFERENCE: summed from the logged calls].

<!-- app-spend:begin -->

### The app's own calls, rolled up by `scripts/app-spend.py` (2026-10-23 15:23 UTC)

**Hosted app** (`model_call` in the container's database, every call since it was created):

| Mode | Calls | Cost (USD) |
|---|---|---|
| live | 9 | 0.0295 |
| replay | 657 | 0.0000 |

Live calls on the hosted app, by task:

| Task | Model | Calls | In | Cache write | Cache read | Out | Cost (USD) |
|---|---|---|---|---|---|---|---|
| fairhousing.review | claude-haiku-5-5 | 7 | 962 | 3,095 | 18,570 | 1,607 | 0.0015 |
| inbox.reply | claude-sonnet-5-5 | 1 | 633 | 713 | 0 | 692 | 0.0100 |
| offers.advise | claude-sonnet-5-5 | 1 | 369 | 1,169 | 0 | 1,438 | 0.0180 |

**Hosted live spend: $0.0295** of the $12 app cap (the footer of every page shows the same figure).

**Local recordings logged by `scripts/slice4-models.py`** (8 live calls): $0.3149.

<!-- app-spend:end -->

## 2026-10-23, morning: original idea re-spec and build slice 1 (credit, then Max: decision 22)

| Tag | What | Cost (USD) | Billed to |
|---|---|---|---|
| RESPEC-A | Architecture spec, traceability and out-of-scope revised for decision 21 | 2.58 | API credit |
| RESPEC-B | Executive summary, plan, assumptions, questions rewritten around the original idea; contract-route research | 4.31 | API credit |
| BUILD-1 | Slice 1: skeleton, Step 1 Intake, first timeline, docker hosting, T1 to T8 | 8.31 | API credit |
| setup | Smoke test of a job on the Max login | 0.00 notional | Max plan |
| BUILD-2 | Slice 2: pricing, listing copy and the fair-housing pipeline (39/39 planted phrases caught), marketing plan | 8.43 | API credit |
| BUILD-3 | Slice 3, first half: pricing reconciled with the demo-house research ($610k to $650k), Step 5 Communications, Step 6 Offers | 3.95 | API credit |
| BUILD-3 | Slice 3, second half: full PCDS form, Step 8 Buyer side, the offers rework, Step 7 Contract, models, replays, live walk; resumed with its context | notional (see `scripts/spend-summary.sh`) | Max plan |
| BUILD-FIX | Demo usability fix: gate cards instead of redirects, fast-forward, "Decide as", phone layout; app live spend $0 (all replays) | see `scripts/spend-summary.sh` | as the runner chose (decision 22) |
| BUILD-UX | Redesign from the UI audit (Joe: "looks weird, not user friendly"; "so crowded"): results first, notes hidden, phone-first | see `scripts/spend-summary.sh` | Max plan |
| BUILD-4 | Slice 4: step 10, guided demo, finished timeline, PII export and delete, walk-order numbering, end-to-end browser run, polish; app live spend about $0.01 (step 10's replays) | see `scripts/spend-summary.sh` | as the runner chose (decision 22) |
| BUILD-POLISH | Content fixes from the slice-4 review: fees match the plan ($4,500 / $3,500), founder placeholder as a styled chip; app live spend $0.3149 (8 re-recorded replays) | see `scripts/spend-summary.sh` | as the runner chose (decision 22) |

**Credit after BUILD-1: $171.26 spent; $15 reserved for the demo's own calls; $13.74 left for BUILD-2.** The app's
own live calls so far: $0.001 (two Haiku calls recording the replay).

**The credit is used down to its reserve (2026-10-23, 11:47 UTC).** Headless jobs: $183.64 of $200. The app's own
live calls so far: about $0.35 (recording replays). That leaves about $16 on the key: the $15 reserve for the demo's
live calls at the meeting, and $1.36 the runner will not start a job with. From here every job runs on the Max plan
(decision 22); `scripts/spend-summary.sh` shows their notional cost separately.

**End of day 1 (2026-10-23, 15:20 UTC), the whole build:** API credit $183.64 on jobs plus about $1.6 of the app's own
recordings, so about $14.7 is left on the key for the meeting's live calls (the hosted demo replays at $0). Max plan,
notional: BUILD-3 second half $21.95, BUILD-UX $10.22, BUILD-4 $18.92, BUILD-FIX $6.73, BUILD-POLISH $2.84; total
$60.66 (what the API would have charged; the plan bills nothing extra).

**2026-10-24, BUILD-PATH (the one-path rebuild, decisions 47 to 51):** Max plan, notional about $75 (the job and five
parallel sub-agents for the screens). No live model calls: no request was re-recorded; the replay lookup now ignores
database row ids, so the recorded answers cover the new order of steps. The app's own spend is unchanged.
