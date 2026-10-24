# Progress (daily summary, newest first)

## 2026-10-24 (day 2), small hours: the demo rebuilt as one path (BUILD-PATH)

**Joe's complaint, fixed:** going back keeps everything. Every form re-opens filled in, sending step 1 again
updates the same sale, typing then leaving asks "Leave without saving?", and every decision has a Change link that
names what it re-opens (decisions 47 to 51).

**What changed:**
- 20 screens in 10 steps became **11 steps, a finale ("The whole sale, start to finish") and "one more thing"** (how
  the firm finds sellers).
- Every screen ends in **one action bar**: Back, and one button that does the next thing or says "Continue".
- **You play the seller and the buyer** (amber buttons); the AI does everything else on its own, at once (Q51).
- The presenter's tools (notes, Do this screen for me, skip ahead) only after "I'm presenting" in the menu.

**Measured (browser, recorded answers, no key):** 29 presses from Start to the finale at laptop and phone width;
the button is on screen without scrolling on every screen; the phone's chrome is 80 px; at most one primary and two
other buttons on any screen. Report: `docs/build/e2e-demo-run.md`; screenshots: `docs/build/screens/one-path/`.

**Live:** deployed; `scripts/live-flow.sh` walks the whole sale on the live site and leaves it reset.

**Disk: 4 GB free, under the 6 GB warning line** (other projects keep growing). Under 3 GB, builds stop.

## 2026-10-23 (day 1), late evening: Joe's click-through, a whole-site audit, and a rebuild under way

**Joe's notes:**

> "the demo doesnt save any of the information when you go back a step … it needs to be made more user friendly
> and simple, and self explanatory … the user simplicity needs to improve drastically"

and "audit the whole website for issues".

**Causes confirmed:**
- No "Next" control saves what is on the screen.
- Step 1 re-opens empty once sent.
- Sending step 1 again silently starts a second deal.
- No decision can be changed.

**The audit:** `docs/build/site-audit-2026-10-23.md`, published under "Demo build". It is the chat session's own
walk of all 20 screens at both widths plus scripted checks, and a separate first-time-visitor review
(`docs/build/audit-fresh-eyes-2026-10-23.md`, AUDIT-FRESH, $11.78 notional on Max).

**Two jobs are running on the Max plan:**
- **BUILD-PATH** (`docs/build/jobs/2026-10-23-one-path.md`, decisions 47 to 51): one path of about 12 screens with
  one button each. Nothing typed or decided is lost, and everything can be changed. The visitor plays the seller and
  the buyer. The presenter's tools are opt-in, and the demo ends on a finale.
- **BUILD-SITE** (`docs/build/jobs/2026-10-23-review-site.md`): the research site's links, phone layout, tables of
  contents, and an index that opens on the demo.

**Disk:** 7 GB free, down from 11 because of other projects' growth. It is near the 6 GB warning line.

## 2026-10-23 (day 1), end of day: the demo is built, five days early

**State:** all ten steps and the guided demo are live at https://realestate.hughesnode.com (house login): press
**Start demo**, then use the Presenter notes' Next and "Do this screen for me". 165 tests pass; a browser walk of every
screen at phone and laptop width passes; the hosted demo replays recorded AI answers at $0. The chat session reviewed
the screens itself after Joe's "looks weird, not user friendly" and "so crowded": the audit, the redesign and two
rounds of fixes followed (docs/build/ui-audit-2026-10-23.md).

**Waiting on Joe:** to-do #1, make the public GitHub repo private and say "change it" or "keep it" for the house
password (it was in two scripts for about 2.5 hours; removed); the click-through (any time before the meeting; it was
planned for 10-28); the father-in-law package (to-do); Q45 to Q50 have defaults.

**Next:** fixes from Joe's click-through; a timed rehearsal; the meeting about 2026-10-30.

**Disk:** 11 GB free (shared caches and build images; two stale realestate images removed).

## 2026-10-23 (day 1), night: two content fixes from the slice-4 review (BUILD-POLISH)

- **The fees now match the plan:** $4,500 for the seller, $3,500 for the buyer, paid at closing (WS4's figures, as
  in the executive summary and the plan), on the intake services card, the pricing and offers net sheets, the buyer
  agreement and the firm's campaign. No screen or recorded AI answer says $4,995 any more (decision 46).
- **Knock-on in the recorded run:** with the new "seller keeps" figures the AI suggests a $635,000 counter, so the
  deal now agrees at **$630,000** (was $629,000); the contract draft was re-recorded to match. 8 live calls, $0.3149;
  the hosted demo still runs on recorded answers at $0 (hosted live total unchanged at $0.0295).
- **"[Founder's name]" no longer looks like a bug:** the landing page shows a dotted "Founder's name" fill-in with
  the tooltip "Named once the founder agrees; see Q49". Nobody is named without consent (Q49).
- **Checks:** 165 tests pass (including the browser run of the guided demo on replays with no key);
  `scripts/live-flow.sh` passes on the live site; 15 affected screenshots re-shot in `docs/build/screens/slice4/`.
  The live deal is reset to the start. Disk: 13 GB free.

## 2026-10-23 (day 1), night: slice 4, the demo is complete (BUILD-4)

All ten steps are built and live at https://realestate.hughesnode.com (house login). The live deal is reset to the
start: press **Start demo**; any step is one tap away with ⏩ (fast-forward).
- **Step 10, marketing the business:** the AI writes the firm's landing page, a local ad and a free seller's guide;
  each passes the fair-housing check and a check on claims. "The AI that replaces your agent and your lawyer" is
  refused: advertising law bars that claim while the law still needs them (a hurdle, reported). The ad reaches people
  by place only; targeting by age is refused by code. Publishing records the red note: only a licensed broker may
  place the firm's ads (decision 43).
- **Guided demo:** Start demo opens notes on every screen with **Next**, **Do this screen for me** and
  **Spotlight**; close them and they stay closed. On a phone they sit behind "Notes" in the top bar; on a laptop
  under the step list. Nothing floats over the content any more (decision 41).
- **Steps numbered in the order the demo walks them** (6 Buyer side, 7 Offers, 8 Contract), and short tab titles
  ("Offers · Hudson Valley AI Realty") (Q47, decision 42).
- **The timeline is finished:** the road to closing (escrow, inspection, repairs, appraisal, mortgage, title,
  walkthrough, closing) dated from the signing, the hurdle map with every red note, and a list of everything the AI
  did that NY law reserves (decision 44).
- **People and their data:** export any person's data, erase it (the screen states the three-year records rule,
  Q50), and see who viewed it.
- **Polish from the review:** codes off the screens, the profile's counts agree, the offers, channels and disclosure
  form open on their outcome with details folded.
- **Checks:** 163 tests pass, including a headless browser run of the whole guided demo on recorded answers with no
  key (`scripts/e2e-demo.py`: 20 screens at phone and laptop width, no problems). `scripts/live-flow.sh` (all ten
  steps) and `scripts/phone-check.py` pass on the live site. Estimated length with the narration: 14.6 minutes
  (`docs/build/e2e-demo-run.md`). 47 screenshots in `docs/build/screens/slice4/`. App live spend: about $0.01 to record
  step 10; the hosted app's live total is still $0.0295 of its $12 cap. Disk: 11 GB free.

## 2026-10-23 (day 1), night: the screens redesigned from the UI audit (BUILD-UX)

Joe: "It looks weird, and it is not user friendly." Every finding in `docs/build/ui-audit-2026-10-23.md` is worked
through; its new "Fixed" section lists what changed per finding and what is left (decision 40). Live at
https://realestate.hughesnode.com (house login).
- **Each screen leads with its result** in plain English ("The AI suggests listing at $640,000"; "Signed by both
  parties (simulated)") and one main button; tables, drafts and records are folded under "Show the working".
- **The presenter's script is hidden** behind a "Presenter notes" button, bottom right.
- **"NY law today" notes are one plain sentence** with a "Why" fold for the rule, the codes and the research link.
  Every note, decision, gate and record still renders and is recorded.
- **People and data read like a product:** names on the contract, "Both consented", Yes/No, Eastern times.
- **Phone first:** a compact step bar, no sideways scrolling, tables stacked as cards, 44 px buttons, 16 px text.
  The contract went from 21,088 to 4,245 px tall on a phone and the timeline from 18,167 to 4,001.
- **Plain chrome:** "View as" Presenter / Seller / Buyer, "Recorded run", "Start over", research link in the footer.
- **Checks:** 137 tests pass (four selectors updated, no behaviour changed); `scripts/live-flow.sh` and
  `scripts/phone-check.py` pass on the live site; the after screenshots are in `docs/build/screens/after/`. The
  live deal is left walked through every built step. App live spend unchanged. Disk: 14 GB free.

## 2026-10-23 (day 1), late: the demo works from a phone (BUILD-FIX)

Joe could not get past step 1 on his phone: after **Start demo** every other step link silently bounced back to
the intake. Fixed and live at https://realestate.hughesnode.com (decision 39):
- **Every step link opens its own screen.** When a step needs an earlier one, a card says what is missing, on
  which step, who does it (the AI, the seller or the buyer), with a button to go there.
- **"Fast-forward the demo to here"** on that card and under each step in the step list (Presenter only). It plays
  the earlier steps exactly as the demo script does, on the recorded AI answers ($0). Each seller or buyer
  decision is recorded as theirs.
- **"Decide as the seller" (or buyer)** on every decision card: one tap switches persona and returns to the card.
  The Presenter still cannot decide for a client.
- **Start demo asks first**, then opens step 1 with one line saying what to press.
- **Phone:** numbered step bar at the top of every screen, buttons at least 44 px, nothing scrolls sideways, and
  the narration starts folded.
- **Checks:** 137 tests pass (19 new). `scripts/live-flow.sh` now also checks every step link after a reset (all
  200, none redirects) and a fast-forward to the signed contract; it passes on the live site.
  `scripts/phone-check.py` passes every screen at 390 px, locally and live. App live spend unchanged ($0 added).
  The live deal is left walked through every built step. Disk: 16 GB free.

## 2026-10-23 (day 1), evening: slice 3 is live (contract and buyer side added)

**See it:** https://realestate.hughesnode.com (house login). Press **Start demo** and walk steps 1 to 5, then
**8** (buyer side), then 6 (offers) and 7 (contract): the buyer's offer comes before the offers screen
(decision 34, Q47). `docs/DEMO-SCRIPT.md` says what to click and say on each screen.

**Built (BUILD-3, second half):**
- **The full Property Condition Disclosure Statement:** the current 56-question form (effective 2025-07-01), read
  from the enacted bill text. Every field starts blank, and only the seller can submit it. The fictional demo
  seller's answers can be submitted in one click, as the seller, and are labelled fiction.
- **Step 8 Buyer side, four screens:**
  - **Intake:** asks no question about family, religion or any other protected trait. The AI takes the buyer on as
    a client under a red marker and sends the notices and a buyer agreement with a negotiable fee.
  - **Search:** facts-only filters and an AI alert.
  - **Tour:** refused until the buyer agreement is signed. Both clients consent in writing to dual agency.
  - **Offer:** the buyer's AI advises and drafts the offer (red marker). The buyer approves it, and it becomes
    offer B.
- **Step 6 reworked:**
  - The seller's counter now sets terms as well as price (closing range, inspection and mortgage periods,
    requests), and code refuses anything outside them.
  - The seller's AI and the buyer's AI negotiate. In the recorded run, the seller counters at $634,000 and lets
    the AI go down to $628,000. The buyer approves a reply of $629,000, and the seller's AI agrees on its own.
  - A test checks every model call of the whole run, and neither AI ever sees the other side's limits.
- **Step 7 Contract:**
  - The AI sends the accepted-offer memorandum.
  - Opus drafts the contract of sale and a rider in the order of the bar-association long form. A side-by-side
    note covers each of its 28 paragraphs.
  - Code checks the draft against the deal, and refuses any wording that says a lawyer is unnecessary.
  - The red marker states the law plainly and names the lawful route at launch, with a link to the plan.
  - Signing is refused until the seller's disclosure statement is done.
  - A signing map shows the deed's notary, the power-of-attorney witnesses and the detector affidavit.
  - Both parties sign (simulated).
  - The PDF (17 pages) and the DOCX carry the label on every page.
- **Models:** Opus drafts the contract after a side-by-side found it decisively better on New York mechanics
  (decision 36, Q48). The other new tasks run on Sonnet, and the buyer's search alert on Haiku.
- **Checks:** 118 tests pass. `scripts/live-flow.sh` walks steps 1 to 8 on the live site, and every check passes.
  The walk replays at no cost.
- **App spend:** the app's own live spend for slice 3 was $0.98, all on recording. Disk: 18 GB free.
- **Next:** slice 4 (step 10, demo mode, timeline finish, PII export and delete, Playwright, spend roll-up).

## 2026-10-23 (day 1), late: pricing fixed; slice 3 half built (Communications and Offers live)

**See it:** https://realestate.hughesnode.com (house login): steps 2, 5 and 6.

- **Pricing now matches the demo-house research.** The screen shows the three cross-checks (median price a foot
  $649,782; same style $617,652; town assessment ratio $610,864) beside the adjusted sales ($635,000). Range
  **$610,000 to $650,000**, reconciled value $625,000; the AI recommends **$640,000** and names the adjustments
  that push away from the cross-checks. Three demonstration rates were re-examined and changed (time, basement,
  lot); decision 30 note, Q46.
- **Step 5 Communications:** the seller approves the fact sheet and the AI's authority first (CP-27); eight
  simulated enquiries; the AI answers and sends on its own, fair-housing checked, identity block on every message,
  agency form at first contact, CP-09 per message; owner-hosted showing (CP-10) and self-guided tour (CP-28);
  only a price question and an out-of-hours showing reach the seller; feedback logged.
- **Step 6 Offers:** two offers compared with net sheets; the AI presents and advises (CP-11); the seller counters
  and sets the lowest price the AI may agree (CP-12); the AI negotiates to agreement at $636,000 (CP-13); a
  counter outside the seller's decision is refused by code.
- **Not yet:** Step 7 Contract and Step 8 Buyer side (the build job ran out of budget; it resumes from here).
  The firm's-own-buyer offer is a fixture until step 8 exists. The AI's offer advice may suggest changing terms
  (closing date, test deadline); the counter in this build changes price only.
- Live walk (`scripts/live-flow.sh`) passes steps 1 to 6 on the site; 81 tests pass. App live spend in this job:
  $0.10 + $0.02 recording and $0.03 on the hosted walk. Disk: 19 GB free.

## 2026-10-23 (day 1), evening: slice 2 is live (pricing, listing copy with the fair-housing checker, marketing plan)

**See it:** https://realestate.hughesnode.com (house login). Press **Start demo**, do step 1, then steps 2 to 4 in
the step list; `docs/DEMO-SCRIPT.md` says what to click and say on each screen.

**Built (BUILD-2):**
- **Step 2 Pricing:** eight real Dutchess County sales from public records, each adjusted toward the house in code at
  rates shown on the screen; weak sales flagged; range $615,000 to $730,000. The AI explains the method in plain
  words and recommends $675,000 with its reasoning, under a red "NY law today" marker (price advice is a licensed
  broker's duty). Net sheet. The seller chooses the price; the copy step refuses to start until they do. Labelled
  "Comparative market analysis, not an appraisal".
- **Step 3 Listing copy:** the AI writes MLS remarks, a portal description, three social posts and a one-page flyer
  (PDF, DEMONSTRATION on every page). Every piece goes through the **fair-housing checker**: our written rules for
  every federal and New York protected class, steering and blockbusting, then a model review for coded language.
  "Plant a violation" adds "Perfect for a young family, steps from the church": caught with rule, class, legal basis
  and a fixed version; the AI applies the fix, the re-check passes, and only then can the AI mark it "ready to
  publish" (red marker: placing ads is a broker's act). MLS pre-check (no contact details, compensation or "free")
  and the listing package in OneKey order.
- **Step 4 Marketing plan:** a board of honest channel cards. OneKey MLS is "human required" (no input API; a
  licensed MLS participant keys it from the AI's package), linked to the WS3 finding; Zillow, Realtor.com, Redfin,
  Homes.com and OneKeyMLS.com are "fed from the MLS"; the firm's site waits for the MLS entry (Clear Cooperation);
  social, Google, photos, sign, lockbox and open house each say who does them. The seller signs the exposure choice
  and authorisations.

**Checked:** 65 fast tests (fake model), including `test_no_unchecked_send` and the fair-housing fixtures; the whole
of steps 1 to 4 walked on the live site by `scripts/live-flow.sh` (all checks OK, the AI replaying at $0).
**Fair-housing fixture result (assumption A8):** 58 phrases; rules + model caught **39 of 39** disallowed (100%) and
flagged **0 of 14** allowed. Passed on our own set; A8 stays open until messages (slice 3) and an outside set.

**Models:** live side-by-side on the demo house; Sonnet kept for price advice and copy, Haiku for the fair-housing
review (decision 33). **App's own live spend in slice 2: about $0.20** (side-by-side $0.09, recording the demo run
$0.08, recording the fixture set about $0.02, one cut-off Haiku run about $0.004); the hosted demo replays all of it
at no cost. Cap $12.

**Questions:** Q46 (the pricing adjustment rates are ours, labelled; a broker can replace them).
**Deferred:** screenshots and the Playwright run (Playwright is not installed yet; slice 4); OneKey's exact remarks
length limit (1,000 characters assumed, marked); the NY protected-class list was taken from WS2, not re-read against
the statute text in this job. **Next:** slice 3 (communications, offers, contract, buyer side). Disk: 19 GB free.

## 2026-10-23 (day 1), afternoon: slice 1 of the demo is live

**See it:** https://realestate.hughesnode.com (house login). Press **Start demo**. The review pages are where
they were: the "Review documents" link, `/index.html`, and every `/docs-*.html` address still work.

**Built (BUILD-1):** the app skeleton (step list, persona switcher Seller / Buyer / Presenter, the DEMONSTRATION
mark and the firm's identity block on every page), the record service with all 35 record codes from one catalogue
file, and the first two screens of the sale:
- **Step 1 Intake:** address and facts ("Use demo house"), property profile with a source chip on every fact
  (public record / seller / inferred by the AI, with its reason), disclosure checklist (lead paint and
  agricultural notice worked out as not needed; the seller's own disclosure form, never pre-filled), onboarding
  (three notices sent at first contact, agency form, listing presentation, conflicts check, the AI accepting the
  listing with its red "NY law today" marker, the listing agreement with the state's exclusive-listing explanation).
  The seller's decisions block: the agreement cannot be signed before the agency form, and nobody but the seller
  can make them (checked on the server).
- **Step 9 Deal timeline:** built only from the records, coloured AI / client decision / NY law today / third
  party, with header counts, the standing "no broker of record" marker and a first hurdle map.

**Checked:** 41 fast tests; the whole intake walked on the live site by `scripts/live-flow.sh` (profile with all
three chip kinds in 3 clicks; sign-before-agency refused; presenter refused a seller decision; timeline colours;
review page served). Try-first checks: 6 pass, T3 (state-machine library) and T5 (FEMA server unreachable) took
their fallbacks; results in the architecture spec, section 1.

**AI use so far:** two live Haiku calls, $0.00098, to prove the live connection and record the replay the site
uses; the demo house now replays at no cost. App cap $12.

**Questions raised (for `QUESTIONS-FOR-JOE.md`; another job is editing it now):** the firm's name. Provisional:
"Hudson Valley AI Realty", marked "demonstration name; not a licensed firm" (`config/brokerage.yaml`).

**Next:** slice 2 (pricing, listing copy with the fair-housing checker, marketing plan). Disk: 19 GB free.

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
