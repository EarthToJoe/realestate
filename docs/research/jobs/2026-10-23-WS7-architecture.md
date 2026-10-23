# Your job: POC architecture spec and traceability matrix (headless, 2026-10-23; hard budget cap: be economical)

Joe signed off `docs/SUCCESS-CRITERIA.md` (the finish line) and workstreams 1 to 3 have landed. Write the two
planning documents the build starts from. **No code. No state-changing git commands. Write only the two files
below.** Read selectively (grep for the tables and sections named; do not read `research_notes/`).

## Read
- `docs/SUCCESS-CRITERIA.md` (all), `docs/OUT-OF-SCOPE.md`, `docs/TRACEABILITY.md` (skeleton),
  `docs/DECISIONS.md` decisions 5 to 8 and 13 to 19 (stack, checkpoints, hughesnode, demo house in Holmes NY,
  spending discipline: the demo's own model calls must be cheap; $15 is reserved for them through the meeting).
- `docs/research/WS1-agent-functions.md`: the inventory tables (F1 to F89, class per function) and "Counts and
  the true bottleneck list".
- `docs/research/WS2-legal-licensing.md`: "10. The constraint table" (L1 to L62) and "11. Where the human and
  licensed checkpoints sit".
- `docs/research/WS3-listing-data-access.md`: "What the proof of concept automates, stubs and skips".
- `docs/research/handoff/WS1.md`, `WS2.md`, `WS3.md` (traceability items), `WS7.md` (the "What already exists"
  table and the candidates to try), and `docs/specs/demo-house.md` if it exists (the demo house's data shape).

## Write `docs/specs/poc-architecture.md`
1. **What already exists** (per /root/projects/CLAUDE.md): the WS7 table, with adopt / adapt / borrow ideas /
   skip and why, and which candidates the build tries on a real example before committing.
2. **Stack, locked**: confirm or change provisional decision 7 (Python 3.12, FastAPI, Jinja2 + HTMX, SQLite,
   Anthropic SDK, no JS build) with reasons from the research; deployment as a Docker app at
   https://realestate.hughesnode.com (hughesnode type docker, house login in front; the existing review pages
   kept at the same address); the VPS has 2 vCPU, 8 GB RAM, ~21 GB free disk.
3. **Module map**: each success-criteria step (1 to 11) → module → screens → what the AI does on screen →
   the checkpoint that ends it. Modules sit behind stable interfaces (model provider, MLS/portal connectors as
   stubs with "human required here: <reason, L-ID>" markers).
4. **Data model**: property (fields tagged by source), people (PII-marked fields), deal, offer, checkpoint
   (who must act, why with F-ID and L-ID, decision, time), message, document, disclosure, audit log, access log,
   spend log.
5. **Fair-housing pipeline**: a rules file (federal + NY protected classes, steering, NY extras) + a model
   review pass + broker approval gate; the fixture set (at least 30 allowed and disallowed phrases) and its test.
6. **PII design**: minimisation per step, fields sent to the model, access log, export and delete, no PII in logs.
7. **Model use and cost**: which Claude model per module (check current model IDs and prices in the
   claude-api skill or Anthropic docs; favour the cheapest model that meets demo quality, and cache fixed
   prompts), estimated cost per full demo run; a cached "demo replay" mode so rehearsals cost nothing.
8. **Demo mode**: the guided walkthrough, narration cards, the 12 to 15 minute run, and how
   `docs/DEMO-SCRIPT.md` stays in step.
9. **Build order**: four build days (2026-10-25 to 10-28), each a vertical slice with acceptance checks tied to
   success-criteria items, ending with Joe's click-through on hughesnode on 10-28; what to cut first if late.
10. **Risks** to the build and how each is handled.

## Write `docs/TRACEABILITY.md` (replace the skeleton)
One table: `Feature (module / screen) | Success criterion # | Agent functions (F-IDs) replaced or assisted |
Legal constraints respected (L-IDs) | Checkpoint (who acts, why) | Status (planned)`. Every success-criteria step
appears; no orphan features. Below it: the 21 "Human or licence required" F-IDs, each mapped to the checkpoint
that shows it in the demo or marked "not in the POC: <reason>".

Final reply (under 10 lines): the locked stack, models per module with cost per demo run, build order headline,
and anything you think Joe must decide.
