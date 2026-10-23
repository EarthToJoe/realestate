# Progress (daily summary, newest first)

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
