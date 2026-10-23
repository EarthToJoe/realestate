# Progress (daily summary, newest first)

## 2026-10-23 (day 1), morning: the original idea stands; build unblocked

**Joe's answers:** "Keep the original idea, that is what I said I would build. I can pare it back on the future if
need be. The idea is the idea. Completely replace the real estate agents." (decision 21) and "Do as much as you can
with the api credit before moving to use the plan." (decision 22).

**What changed:**
- The product is the brief's idea again: the AI is the agent on both sides and drafts the contract. The research
  findings stand unchanged; they become hurdles shown in the demo as red "NY law today" markers (where a licence
  or lawyer is required today), not gates and not a reshaped business.
- Success criteria amended to match (steps 2, 3, 5, 6, 7, 8, 9); Q19, Q24 and Q26 answered; Q43 (inspection) added.
- `scripts/api-run.sh` runs jobs on the credit until about $2 is left above the $15 demo reserve, then on the Max
  login by itself; spend is logged per run as `api` or `max`. Tested on Max.
- To-do 35ccf6 (billing) done; a7c7fb (send the memo) on hold until the summary is rewritten.

**Running now (credit):** RESPEC-A revises the architecture spec, traceability and out-of-scope list for the original
idea and re-dates the build to start today; RESPEC-B rewrites the executive summary, plan, assumption statuses and
questions around it. The build follows as soon as RESPEC-A lands.

**Disk:** 19 GB free.

## 2026-10-23 (day 1), end of night: research, plan and summary done

**Done tonight (all on hughesnode, house login: https://realestate.hughesnode.com):**
- Six research deliverables, each with a gap fill, a coverage audit and primary-source checks of its key claims:
  WS1 (89 agent functions: 22 automatable, 46 partly, 21 licence or human), WS2 (62 legal constraints), WS3
  (listing access: a person keys each listing into OneKey; portals follow free), WS4 (lean year one ~$8.2k,
  break-even 2 closings; realistic ~$62.6k, 25), WS5 (~70 competitors; closest LocQube, none local), WS6 (drop the
  free inspection as pitched; capped seller-hired pilot).
- Independent fact-check on a different model: ~60 checks, 8 corrections in place; the fixed-fee route to being
  seller's lawyer and broker together is confirmed (NYSBA Ops. 1015, 1117).
- Memo for the father-in-law; POC architecture spec and traceability matrix (stack locked, ~$0.16 per live demo
  run); demo-house data for 146 Rt 292, Holmes NY (8 comparables, $610k to $650k broker-review range).
- `ASSUMPTIONS.md` statuses, `PLAN.md`, `EXECUTIVE-SUMMARY.md`, questions Q13 to Q42 with a "start here" triage.

**Kill criteria, plainly:** A3 (no lawyer), A6 (buyer tours with no human) and A9 (free inspection as pitched) are
hit; K1 partly (sellers save about a third when the buyer has an agent); K2 open but hit the day the firm must buy
customers; K4 hit only if pitched as "replaces the agent"; K7 hit only in the full build-out. New top risk: A12,
whether his network still produces listings after ten years away. The venture survives as a narrower, seller-first,
attorney-brokered flat-fee firm; the first test is ten seller calls.

**Incidents, fixed:** background helpers cut off by the headless wait limit (WS5, salvaged and resumed); an in-place
edit of the job runner broke cost logging for running jobs (logged by hand; runner now edit-safe); a resumed job
double-counted its first run (corrected; logger fixed); first wave spent ~$125 in 35 minutes (caps, high effort and
a $15 demo reserve since).

**Disk:** 21 GB free (checked at start; nothing large written since).

**Spend:** $156.07 of $200; $15 reserved for the demo; about $29 usable.

**Waiting on Joe:** Q26 (build on Max or add credit; #1 on his to-do list). Then the build starts (2026-10-25 plan).

## 2026-10-23 (day 1, VPS session), late night: night plan

**Signed off:** success criteria (Joe: "i sign off"). **Demo house:** 146 Rt 292, Holmes, NY 12531 (decision 18).
**Joe's answers** to Q4 to Q10 are in `QUESTIONS-FOR-JOE.md`; the meeting is about 2026-10-30.

**Spend warning (decision 19).** About $125 of the $200 credit went in the first 35 minutes. Every job is now
capped and leaner, and $15 is held back for the demo's own AI calls. The build does not fit in what is left;
Joe chooses Max or more credit in the morning (on his to-do list).

**Night plan, in order (each step only when the one before has landed):**
1. Research jobs still running finish: WS1, WS2, WS3, WS6, the resumed WS5, the Holmes house data. Log, review,
   commit, publish each. Salvage and resume any that lose helpers (WS3, WS2 at risk), within the cap.
2. One lean job (cap $10): assumptions status lines, consolidated questions from all handoffs, `docs/PLAN.md`
   and `docs/EXECUTIVE-SUMMARY.md`, reading only the deliverables and handoffs.
3. One small job (cap $4): plain memo for the father-in-law on being broker and lawyer, and on running a NY
   brokerage from out of state (Q4d, Q11).
4. One job (cap $8): `docs/specs/poc-architecture.md` with the "what already exists" table, and
   `docs/TRACEABILITY.md` from the F-IDs and L-IDs.
5. One fact-check pass (cap $5): the load-bearing claims across all six reports, by a job that did not write them.
6. Stop there and wait for Joe's billing answer before any build work.

## 2026-10-23 (day 1, VPS session), night

**Disk:** 21 GB free of 96 GB (79% used). Fine; no action needed.

**Repo:** origin is `github.com/EarthToJoe/realestate`; pulled to `3b9352b`. All thirteen notes files present.

**Pipeline checked:** API key works (rate limits are high, so parallel jobs are safe); a smoke job through
`scripts/api-run.sh` ran on Opus 5.5 and logged its cost (8 cents, tag `setup`).

**Launched (running now, all billed to the credit):** seven headless jobs in parallel, one per workstream.
WS1 to WS6 each (a) audit their notes against the brief's full ask, (b) re-check the 10 to 20 claims their
conclusions rest on against primary sources, (c) fill the gaps with a fresh search budget, appended to the
notes under "Gap fill (2026-10-23, VPS session)", then (d) write the deliverable in `docs/research/` and a
handoff file in `docs/research/handoff/`. WS7 does (a) to (c) for the POC building blocks only. Joe's standard,
added to every brief: "extensive and not piece and parcel; comprehensive, accurate, focused on the right
things." The exact briefs are saved in `docs/research/jobs/`.

**Next:** review each deliverable as it lands, commit it, post spend per workstream; then assumptions status
(step 4), the plan and the executive summary (step 5).

## 2026-10-23 (day 1, cloud session), end of day

**Research notes complete.** All thirteen passes finished and are committed (about 1 MB of sourced notes).
Every pass reported that the session's shared web-search budget ran out part-way; each file lists its gaps
rather than guessing, and the handover tells the VPS session to fill them with a fresh budget first.

**What the research says, in one paragraph.** The costs of running the brokerage are small (year one about
$9,000 to $13,600 fixed). The binding constraints are legal and structural: only a licensed broker may
perform the licensed acts and that person must be the actor (RPL 440, 442-d); an unlicensed co-founder may
own equity but may not be paid per deal (RPL 442); a lawyer may not be lawyer and broker in the same deal
(fifteen NYSBA opinions through 2024), and only lawyers may draft contract terms (Judiciary Law 484, 495;
DOS memo LI04), so "the lawyer is out of the loop" is not available as a drafting model and becomes "the
lawyer step is pre-filled, faster and cheaper"; every portal ingests from the MLS and no NY MLS offers a
listing-input API, so MLS entry is a licensed-human step and MLS membership (OneKey plus the Ulster,
Columbia and Greene board's MLS) needs a real broker licence plus Realtor membership; the free inspection as
proposed (unlicensed friend, brokerage-paid, "buyer skips") is unlawful and unsound, while a narrow seller-
engaged licensed version works; every venture-scale discount brokerage in the US has died, been absorbed or
reverted, killed by customer-acquisition cost and no cost advantage, not by consumers rejecting low fees;
and local trust is real but attaches to a person giving broad service, with two-thirds of sellers picking a
referred or prior agent. Kill criteria K1 to K9 are written in the WS5c notes. The assumptions table in
`ASSUMPTIONS.md` gets its dated status lines when the deliverables are written.

**VPS session live (evening):** Joe ran the setup command; the `realestate` session is up on the API key. From its
first prompt it works from `docs/HANDOVER.md`; the cloud session is done.

**Handover.** Per Joe's instruction that all work runs on the API credit, the writing of the six deliverables,
the plan and the executive summary moves to the VPS session (`docs/HANDOVER.md`), which Joe starts with one
command (`QUESTIONS-FOR-JOE.md` Q2). The cloud session stops active work here unless Joe says "continue here".

## 2026-10-23 (day 1, cloud session), morning

**Done**
- Project created as its own git repo, with Joe's brief saved verbatim (`docs/BRIEF.md`).
- Twelve research passes launched across the six workstreams; each writes sourced notes to `research_notes/`
  and will be turned into one deliverable per workstream in `docs/research/`.
- Living documents written: success criteria (draft for sign-off), riskiest assumptions with kill criteria,
  decision log, questions for Joe, out-of-scope list, traceability skeleton, spend log.
- One-command VPS setup written (`scripts/vps-setup.sh`), with disk guard and per-session API billing option.

**Joe's answers (later on day 1):** use GitHub (permission given); all work on the API credit. Result: the work
is pushed to the `realestate-lifeboat` branch of the shorts repo; the VPS session, once Joe runs the one
command, takes over on the API key (`docs/HANDOVER.md`). The thirteen research passes in flight stay on Max.

**Blocked or waiting on Joe**
- GitHub repo `EarthToJoe/realestate` must be created by Joe (the Claude GitHub app got a 403 creating it).
  A temporary branch in the `shorts` repo was blocked by permissions, so the work lives in this container until
  the repo exists; key documents are sent to Joe as files meanwhile.
- VPS session needs Joe to run one command (see `QUESTIONS-FOR-JOE.md` Q2).
- Success criteria need sign-off before any POC code.

**Disk**: cannot be checked from here; the setup script checks it first thing on the VPS.

**Next**
- Turn research notes into the six deliverables; write the plan and the executive summary; update the
  assumptions table against the kill criteria; then, with sign-off and WS1 to WS3 in hand, lock the
  architecture and build the POC.
