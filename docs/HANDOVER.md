# Handover to the VPS session (read this first)

You are the **realestate** Remote Control session on Joe's VPS, in `/root/projects/realestate`. Joe wants
all of this project's work billed to his $200 API credit (expires 2026-11-08). Because Remote Control is
disabled when an API key sits in the chat session's environment, the split is: **you orchestrate on the
claude.ai login; every substantial task runs as a headless job via `bash scripts/api-run.sh --tag WS<n>
"<prompt>"`, billed to the credit and cost-logged.** Write each job's prompt as a complete brief (goal, files
to read, file to write, method file to follow, done-when), since the job starts with only CLAUDE.md and the
prompt. Review what comes back, commit, push, repeat.

## What the cloud session did on 2026-10-23 (day 1)

- Read Joe's brief (`docs/BRIEF.md`, verbatim) and wrote the living documents in `docs/`.
- Launched thirteen research passes in the cloud (two for WS1, three for WS2, two for WS3, one for WS4, three
  for WS5, one for WS6, one "what already exists" pass for the POC, called WS7). All thirteen finished on 2026-10-23 and their
  sourced notes are committed in `research_notes/<workstream>/` (thirteen files, about 1 MB in total, every
  claim labelled and dated). Each file ends its sections with explicit Gaps; see the search-budget note below.
- Could not reach the VPS (no SSH from the cloud) and could not create the GitHub repo (the Claude GitHub
  app lacks that permission: 403). With Joe's permission the work was pushed to the temporary branch
  `realestate-lifeboat` in the `shorts` repo; `scripts/repoint-origin.sh` moves this clone to the real repo
  once Joe creates `EarthToJoe/realestate`.

| Workstream | Notes expected in `research_notes/` |
|---|---|
| WS1 | `WS1 NY agent functions/licensing_curriculum_and_duties.md`, `.../transaction_tasks_and_timeline.md` |
| WS2 | `WS2 NY legal hurdles/licensing_law_entities_compensation.md`, `.../contracts_upl_ethics_esign.md`, `.../fair_housing_disclosures_ai_privacy.md` |
| WS3 | `WS3 Listing and data access/portals.md`, `.../mls_access.md` |
| WS4 | `WS4 Cost model/costs_and_revenue_benchmarks.md` |
| WS5 | `WS5 Competitors/national_inventory.md`, `.../hudson_valley_market_and_locals.md`, `.../why_attempts_failed_and_niche_evidence.md` |
| WS6 | `WS6 Free inspection/pre_listing_inspection.md` |
| WS7 | `WS7 POC building blocks/what_already_exists.md` |

## Known weakness of the cloud research: web-search budget

At least two cloud passes reported that the session's shared web-search budget ran out mid-task; they fell
back to fetching known URLs directly and listed what they could not check under "Gaps" in their notes
(for example Zillow pages returned bot-blocks and are cited by URL for the attorney to open). Before step 3,
read each notes file's Gaps sections and run short gap-filling passes with your own fresh search budget,
appending findings to the same files under a dated "Gap fill" heading.

## What to do next, in order

1. `bash scripts/disk-check.sh`. Record the result in `docs/PROGRESS.md`. Warn Joe if under 6 GB.
2. `git pull` (the cloud session keeps committing research notes as they land). Check the table above.
3. **Write the six deliverables**, one per workstream, in `docs/research/WS1-agent-functions.md`,
   `WS2-legal-licensing.md`, `WS3-listing-data-access.md`, `WS4-cost-model.md`, `WS5-competitors.md`,
   `WS6-free-inspection.md`. Method: `docs/research/method/report-writer.md`. Each answers the workstream's
   exact ask in `docs/BRIEF.md`, keeps the source labels, and does not soften. WS1 must give every function an
   ID (F1, F2, ...) and a classification (fully automatable / partially / human or licence required); WS2 must
   give every constraint an ID (L1, L2, ...). Those IDs feed `docs/TRACEABILITY.md`. Launch one `scripts/api-run.sh --tag WS<n>` job per workstream, in parallel (`&` then `wait`), so the
   writing bills the credit and your own context stays clean.
4. Update `docs/ASSUMPTIONS.md`: a dated status line per assumption, saying which kill criteria were hit,
   dodged or still open, with a link to the deliverable.
5. Write `docs/PLAN.md` (phases, costs, open questions, human-in-the-loop map) and
   `docs/EXECUTIVE-SUMMARY.md` (one document for the father-in-law: plain, sober, with the hurdles named).
6. Commit and push at each of the steps above. Update `docs/PROGRESS.md` daily and `docs/SPEND-LOG.md` at each
   milestone (Console usage for this session's key, plus the app's own call log once it exists).
7. **Do not write POC code** until Joe has replied `SIGN-OFF` on `docs/SUCCESS-CRITERIA.md` (check
   `docs/QUESTIONS-FOR-JOE.md`) and WS1 to WS3 are written. Then: write `docs/specs/poc-architecture.md`
   with a "What already exists" table from the WS7 notes, lock the stack (provisional choice in
   `docs/DECISIONS.md` item 7), fill `docs/TRACEABILITY.md`, and build to the success criteria, with
   `docs/DEMO-SCRIPT.md` kept in step with the screens.
8. Keep `docs/QUESTIONS-FOR-JOE.md` current: note a question, make a provisional choice, keep moving.

## The build (from 2026-10-23)

Slices 1 to 3 are live (BUILD-1 to BUILD-3): steps 1 to 9 except step 10 (business marketing, slice 4), docker
type on hughesnode. The demo is walked 1 to 5, then 8 (buyer side), 6 and 7 (decision 34). See `README.md` ("The
demo app") for the code map and commands, the architecture spec section 9 for what each slice must pass, and
decisions 27 to 29 for hosting, try-first results and replays. After changing code: `make test`, commit,
`bash scripts/hosting.sh redeploy`, `bash scripts/live-flow.sh` (it walks steps 1 to 8), and for screen changes
`scripts/phone-check.py https://realestate.hughesnode.com` (390 px). A new step or decision also needs its
milestone in `app/demo/walk.py` (`WALK` and `NEEDS`), or its gate card and fast-forward will not know it
(decision 39). The live flow ends with the shared deal walked to the signed contract: leave it that way for Joe's
links. New model tasks go in
`config/models.yaml`; record the whole walk's replays with `scripts/slice3-models.py record` (it runs the steps 1
to 4 path of `scripts/slice2-models.py` first; replay first, misses live and recorded into `replays/`).

## Rules that are easy to forget

- Joe sees things by link: `https://realestate.hughesnode.com` (house login), republished on every commit
  (decision 13). Send him the page link, not a file path.

- Never touch `/root/projects/shorts`. Never put the API key anywhere but the files `secret-set.sh` writes.
- Joe reads on his phone: short, plain, exact commands.
- Thoroughness over cost; `/clear` between unrelated tasks.
