# Decision log

Every architecture and scope decision, with the reasoning, so Joe can explain choices and later sessions do
not relitigate them. Newest at the bottom. Provisional decisions are marked and get confirmed or reversed
with a dated line.

## 2026-10-23

1. **Own repository, sibling of `shorts`.** The project lives in `/home/user/realestate` here and
   `/root/projects/realestate` on the VPS, never inside the `shorts` folder. Reason: different product,
   different rules; the `shorts` CLAUDE.md governs that folder and its five chats. Repo name `realestate` is
   plain and renamable (GitHub keeps redirects).
2. **Research before code.** All six research workstreams run first, in parallel, as twelve focused
   research passes (two for WS1, three for WS2, two for WS3, one for WS4, three for WS5, one for WS6), each
   writing sourced notes with [PRIMARY] / [SECONDARY] / [CLAIMED] / [INFERENCE] labels, then one written
   deliverable per workstream. No POC code until Joe signs off the success criteria and WS1 to WS3 have
   landed (Joe's two rules: success criteria first; research 1 to 3 before locking the architecture).
3. **The cloud session cannot reach the VPS.** This container has no SSH client or key and HTTPS-only egress;
   the VPS is only known as the `ssh vps` alias on Joe's Mac. So the VPS session is created by a one-command
   script Joe runs (`scripts/vps-setup.sh`), modelled on `shorts/scripts/add-phone-session.sh`, and GitHub is
   the sync between the two. Until the GitHub repo exists (the Claude GitHub app may not create repos: 403), the work stays in
   this container; a temporary branch in the `shorts` repo was tried and blocked by the session's permission
   rules (pointing git at another repo), which was respected. Key documents go to Joe as files in chat at each
   milestone until the push is possible.
4. **API billing is per session, by service file only.** Joe wants the $200 API credit used first; the
   `shorts` rule forbids the API key anywhere Claude Code reads it. Resolution: the key, if Joe stores it, is
   written to `/srv/realestate/secrets/claude-code.env` (root, 0600) and read only through a systemd drop-in
   for `claude-remote@realestate`. No shell profile, no global Claude settings, no other session sees it.
   Off until Joe stores the key.
5. **Checkpoints are first-class.** Every human or licensed step in the product is a stored record (who must
   act, the legal or practical reason, the decision). The deal timeline and the human-in-the-loop map are
   generated from these records. Reason: the brief demands that every hurdle be visible in the demo; a hand-
   drawn map would drift from the software.
6. **Fictional demo data.** The demo house and people are invented (a real town, an invented address) unless
   Joe supplies a consenting real property. Reason: PII and courtesy; also lets the demo be shown to anyone.
7. **Provisional stack (to confirm after WS1 to WS3):** Python 3.12, FastAPI, Jinja2 templates with HTMX for
   interactivity, SQLite, the official Anthropic SDK, no JavaScript build toolchain. Reasons: the VPS is
   2 vCPU, 8 GB and short on disk, and already runs Python tooling (`uv`) for `shorts`; server-rendered
   screens are the clearest way to show each step and each AI action; Python modules map cleanly onto the
   modular architecture the brief asks for. React or a Node toolchain would cost disk and build complexity
   for little demo gain. Revisit only if the research changes the shape of the product.
8. **Spend tracking in two layers.** The POC logs every model call (module, tokens, cost) to a local file and
   rolls it up into `docs/SPEND-LOG.md`; session-level spend comes from the Anthropic Console per key. The
   research done in this cloud session runs on Joe's Max plan and cannot be charged to the credit from here.
9. **Disk is a hard guard, not a reason to do less.** The setup script refuses to install with under 3 GB
   free and warns under 6 GB; the session checks `df` at start and before any install (`scripts/disk-check.sh`)
   and warns Joe in `PROGRESS.md` and directly. Depth of work is never reduced for disk; Joe frees space or
   upgrades.
10. **The VPS session does the work; the cloud session only bootstraps.** Joe (2026-10-23): all of this
    project's work is to run on the API credit. The cloud session cannot be billed to it, so after the in-
    flight research notes land and are pushed, the writing, planning and building move to the VPS session,
    which runs on the key. `docs/HANDOVER.md` is the baton. The cloud session resumes only if Joe says so.
11. **Lifeboat branch, with permission.** Joe allowed GitHub use; the work is pushed to `realestate-lifeboat`
    in the `shorts` repo (the app cannot create repos). It is a parking spot, not a home: `scripts/repoint-
    origin.sh` moves the VPS clone to `EarthToJoe/realestate` once Joe creates it, and the branch is deleted.
12. **Chat session on claude.ai, heavy work on the API key (2026-10-23, evening).** Joe's two wishes, reach
    the session from the Claude app and bill the credit, collide inside one process: Claude Code disables
    Remote Control while `ANTHROPIC_API_KEY` is set (observed on the VPS: "claude.ai connectors are disabled").
    Resolution: the interactive session runs on the claude.ai login (`scripts/session-billing.sh off`) and
    launches headless jobs with `scripts/api-run.sh`, each billed to the key and cost-logged per workstream
    tag; the POC app bills the key directly. The chat's own orchestration is the only Max usage.
13. **hughesnode is the home base for everything Joe sees (2026-10-23, night).** Joe: "start using hughesnode
    as a home base for reviews you need me to see. it'll also be the place where demos are performed, user
    tests are performed, etc. It's often easiest if you provide me a link." Files on the VPS are hard to get
    to his phone; a link is not. So `https://realestate.hughesnode.com` (private, house login) is the project's
    own address. Today it is a static review home: `scripts/publish-review.sh` renders `docs/` and
    `research_notes/` as phone-readable pages, and git hooks (`scripts/install-hooks.sh`) republish it after
    every commit and pull. When the POC is built it moves in at the same address (the hughesnode project's type
    changes from static to docker), with the review pages kept alongside the demo, so Joe has one bookmark.
    The existing `review` and `demo` hughesnode apps belong to other projects and are not used.
14. **Demo house: Joe's real address, labelled New York flow (2026-10-23, provisional).** Joe chose 4910 John
    Ticer Dr, Alexandria, VA, which replaces decision 6's fictional house. The product's legal steps are New
    York's, so every state-specific screen carries a "New York rules (launch market)" label; the alternative
    (the same house's details placed in a Hudson Valley town) stays a one-line switch (Q12). Only property
    facts are used, never an owner's name; the house's facts come from the official City of Alexandria
    assessment record or from Joe, never from a portal.
15. **Schedule set by the meeting, about 2026-10-30 (Joe, Q5).** Research, plan and executive summary over
    the weekend; the architecture spec and traceability are written as soon as WS1 to WS3 land, before
    sign-off, because they are planning, not code; the build runs 2026-10-25 to 10-28 once Joe signs off;
    Joe clicks through on hughesnode 2026-10-28; polish 2026-10-29. One API key for everything (Q10: "No"
    to separate keys).
16. **The father-in-law wants to be broker and lawyer in the same deals; the plan does not assume he can
    (2026-10-23).** Joe (Q4d): "Yes, if possible." The early research says NY bar ethics opinions bar it
    except in a narrow fixed-fee, written-consent form. The plan keeps the provisional structure (broker of
    record, not either party's lawyer) until a dedicated memo, written after the WS2 deliverable, sets out
    his options, risks and the out-of-state questions (Q11) for Joe to share with him.
17. **Success criteria signed off (Joe, 2026-10-23: "i sign off").** The POC is built to
    `docs/SUCCESS-CRITERIA.md` as written, with decision 14's demo house. Decision 14 is confirmed, no longer
    provisional (Joe: "thats fine"). Code starts once the WS1 to WS3 deliverables land and the architecture
    spec and traceability are written from them (Joe's sequencing rule).
18. **Demo house moves to New York: 146 Rt 292, Holmes, NY 12531 (Joe, 2026-10-23).** Joe sent this Dutchess
    County address after the Virginia/New York snag was raised (Q12); it replaces decision 14's Alexandria
    address, so every legal step is New York's with no "launch market" label needed. Property facts and
    comparable sales come from Dutchess County, town assessor and New York State records, never a portal; no
    owner's name is stored. The Alexandria data job was stopped after two minutes (about $1, estimated).
19. **Spending discipline after a fast start (Joe, 2026-10-23: "we're spending extraordinarily fast", "be
    judicious about spending still").** The first wave (seven research jobs at xhigh effort, some with four
    helper agents each re-reading large contexts) used about $125 of the $200 credit in 35 minutes; the cost is
    mostly cache reads of big contexts over many turns, not the AI's writing. From now on: every job has a hard
    cap (`--budget`, default $8), runs at `high` effort, reads the six deliverables and handoffs rather than the
    1 MB of notes, and uses no helper agents unless the brief says so; the runner refuses any job that would cut
    into a **$15 reserve** kept for the POC's own model calls at demo time. Remaining credit goes to the plan,
    the executive summary, the father-in-law memo, the architecture spec and one fact-check pass. The POC build
    does not fit in what is left: Joe decides in the morning whether it runs on the Max plan (his original order
    was credit first, then Max) or on more API credit.
20. **Stack locked, models chosen (2026-10-23, from `docs/specs/poc-architecture.md`).** Decision 7 holds
    (Python 3.12, FastAPI, Jinja2 + HTMX, SQLite, Anthropic SDK, no JS build), plus SQLAlchemy, WeasyPrint,
    docxtpl, structlog, nh3, Bulma, Driver.js and Leaflet; one Docker app at realestate.hughesnode.com with the
    review pages kept. Haiku 5.5 for intake, fair-housing review, inbox and buyer side; Sonnet 5.5 for pricing,
    listing copy, counter-offer, contract and business campaign; about $0.16 per live demo run, replay mode for
    rehearsals and tests, live calls stop at $12 so the $15 reserve holds. Provisional, Joe to confirm (spec
    section 11): the contract draft (success criterion 7) is shown in the seller's attorney's workspace, because
    neither the brokerage nor the software may draft a contract of sale (WS2); the brokerage side stops at the
    accepted-offer memo. The meeting runs on a recorded replay by default, with a live switch.
21. **The original idea stands: software that completely replaces the seller's agent and the buyer's agent, and
    drafts the contract (Joe, 2026-10-23: "Keep the original idea, that is what I said I would build. I can pare it
    back on the future if need be. The idea is the idea. Completely replace the real estate agents.").** This
    reverses the reshaping written overnight into the plan, the executive summary and the architecture spec
    (section 0 and 11): the "attorney-run flat-fee brokerage with software doing the paperwork" pitch (Q19), the
    broker approval gates, and the contract shown in the seller's attorney's workspace (Q24, decision 20). The
    research findings do not change and are not softened: New York law today requires a licensed broker for the
    core agent acts (WS2 section 1), only a lawyer may draft a contract for another (L21, L22), and three kill tests
    failed (ASSUMPTIONS). They are now reported as the hurdles the original idea has to clear, not as reasons to
    change it; paring back is Joe's call, later. In the demo the AI does every agent act on both sides, including
    negotiating and drafting the contract. The seller and the buyer make their own decisions, as any agent's
    clients do. Wherever New York law today requires a licensed person or a lawyer, the screen shows a red "NY law
    today" marker with the rule and a link to the finding; the marker does not stop the flow (the brief: "Every
    step where a human or a license is still required should be visible in the demo itself so it illustrates the
    hurdles"). MLS entry stays a "human required" step because no listing-input API exists (WS3): a fact about
    the MLS, not a design choice. The free-inspection add-on was the father-in-law's idea for evaluation, not
    "the idea"; WS6's recommendation stands provisionally (Q43).
22. **Billing: the API credit first, then the Max plan (Joe, 2026-10-23: "Do as much as you can with the api
    credit before moving to use the plan").** Answers Q26. `scripts/api-run.sh` now runs each job on the credit
    while at least $2 is left above the $15 reserve, trimming the job's cap to what is left, then runs jobs on the
    Max login (no key in the job's environment); a job that hits "credit balance too low" switches all later jobs
    to Max. `spend.jsonl` marks every run `api` or `max` (Max costs are notional). The $15 reserve stays because
    the Max plan cannot pay for the app's own API calls at the meeting. The build starts as soon as the
    architecture spec is revised for decision 21 (2026-10-23), not 10-25, since this answer was the only blocker.
23. **One record type with five kinds replaces the checkpoint model (2026-10-23, architecture spec revised for
    decision 21).** Every step record carries a `kind`: `client_decision` (the seller's or buyer's own decision;
    the only kind that blocks), `law_marker` (an agent act the AI did where NY law today requires a licensed broker
    or a lawyer; red, recorded, never blocks), `human_required` (a practical step with no software route, such as
    MLS keying or a notary; the Presenter records a simulated completion), `third_party` (planned) and `automated`
    (logged AI acts with no legal issue). The overnight CP numbers are kept where a step survives, new records are
    CP-25 to CP-35, and all marker texts live in one catalogue file that a test checks against the traceability
    matrix. Why: decision 21 needs the markers to be real, counted records (SC "Checkpoints are real objects") while
    leaving the flow to the clients' decisions only; one table keeps the timeline and hurdle map built from records.
    The personas become Seller, Buyer and Presenter; the Broker and Attorney personas are removed.
24. **Two AI agents with an information wall (2026-10-23).** Because the AI represents both the seller and the
    buyer in the demo deal (offer B comes from the firm's own buyer), the seller's AI and the buyer's AI are
    separate contexts: each model call is built by `AgentContext(side)` from that side's instructions, messages and
    offers only, and a test fails if the buyer's confidential limits reach a seller-side call or the reverse. Both
    clients consent to dual agency (CP-17, L13); the CP-30 marker states that New York's designated-agent route
    needs two licensees under the broker (F51). Why: an agent owes its client confidentiality (F84), and the demo
    should show the AI keeping it rather than one model seeing both sides' bottom lines.
25. **The identity block names no invented broker (2026-10-23, provisional, Joe to confirm: spec section 11 item 6).**
    Every page and message carries the firm's name, office and phone (L10) and the line "Licensed broker of record:
    required by NY law; none in this demonstration", with a standing "NY law today" marker (CP-35: L2 to L5, F73 to
    F75). Why: decision 21 removes the human broker from the demo; inventing a licensed person would hide the
    hurdle the brief asks to show. Alternative: the father-in-law's name as a placeholder, only with his consent.
26. **No attorney-approval clause in the demo's offers or contract (2026-10-23, provisional, Joe to confirm: spec
    section 11 item 5).** Offers carry "not binding until a formal contract is signed by both" (L24, which protects
    the parties); the contract draft has no attorney-approval contingency, and every page is labelled
    "DEMONSTRATION. Drafted by software for the parties. NY law today: only a lawyer may draft a contract of sale
    for another (L21, L22)". The product never says a lawyer is unnecessary (L23). Why: the attorney-approval
    wording comes from the broker's narrow fill-in privilege (L22), which software drafting a whole contract does
    not fit anyway, and adding it would put lawyers back in the loop by contract, against decision 21.
27. **Hosting: realestate is a docker-type hughesnode project; the keys are mounted read-only (2026-10-23, BUILD-1).**
    `hn` supports per-project `VOLUMES` in `hn.conf`, so the container mounts `/srv/realestate/secrets` read-only
    at `/run/secrets/realestate` (model key, `PII_KEY`, `DB_KEY`), `/srv/realestate/data` at `/data`, and the
    review pages' `public/` folder read-only at `/review`. No `app.env` is used; no secret is in the image, the
    repo, a compose label or a log. `public/` did not move, so `scripts/publish-review.sh` is unchanged and every
    review link keeps its address; the app serves the POC at `/` and falls through to the review files for
    everything else (`/index.html` is still the review home). Changes go through `scripts/hosting.sh` (prepare,
    trial, docker, redeploy, static, check), which touches only `/srv/hughesnode/apps/realestate` and
    `/srv/realestate`; `hn.conf.static.bak` allows a one-command return to the static type. The container runs as
    root inside so it can read the root-only key files (mode 600) without loosening them; no-new-privileges is set
    by `hn`. One uvicorn worker, not two: the log masker learns each person's values in-process, and SQLite with
    one demo user does not need a second worker.
28. **Try-first results (2026-10-23, BUILD-1; spec section 1).** Adopted: WeasyPrint in the image (T1), SQLCipher
    for the whole database when a `DB_KEY` secret exists, on top of the Fernet PII columns (T2), Driver.js with
    htmx (T4, slice 4), Leaflet with a static SVG fallback (T7), pyHanko seal (T8, slice 3, still first to cut),
    the PII token round trip (T6). Fallbacks: python-statemachine skipped for the record-derived gates (T3:
    refusals could not say which decision is missing or why, and it duplicates record state); FEMA flood zone
    stays a fixture because FEMA's server does not answer from the VPS (T5; the Census geocoder works).
29. **Replays are committed files, not a table; the hosted app replays first (2026-10-23, BUILD-1).** Recorded model
    answers live in `replays/<request-hash>.json` (masked before hashing and recording; a grep for the personas' names, e-mails and
    phones finds none), so they survive the demo reset, ship in the image and rehearse at no cost.
    The spend log (`model_call`) also survives "Start demo". The hosted app runs in replay mode: the demo-house
    inputs replay (badge "AI: replay of the run recorded ..."); any changed input goes live once and is recorded.
    Locally, `make run` is live when the key is readable, otherwise replay.
30. **Pricing is arithmetic in code; the model explains and advises (2026-10-23, BUILD-2).** Eight Dutchess sales
    from the fixture are adjusted toward the subject at rates printed on the screen (date, living area, finished
    basement, lot capped at 3 acres of difference, age, rooms, central air, garage, and −8% for a style other than
    the subject's raised ranch, from the two raised-ranch sales' lower price a foot). Comps over 25% gross
    adjustment or over 3 miles are flagged weak; the range spans the adjusted prices of the rest ($615,000 to
    $730,000; indicated $660,000). The model never does the arithmetic: it writes the method, names weak comps and
    recommends a price (Sonnet: $675,000), with the CP-25 marker. The rates are ours [INFERENCE], labelled, and
    Q46 asks for local ones. The net sheet uses the NY transfer tax (0.4%) and labelled estimates.
    *Note 2026-10-23 (BUILD-3):* that range and the $675,000 sat above all three cross-checks in
    `docs/specs/demo-house.md` section 4, which a Dutchess broker would test. Rates re-examined against the
    fixture's evidence: time cut to +2% a year (the sales show no trend after the equalisation-rate move, which
    falls before most of them); the finished basement is now adjusted only between same-style sales (the −8% style
    rate was measured on raised ranches with finished lower levels, so adjusting both counted it twice, +$21,000 on
    five sales); lot cut to $2,500 an acre (the 6.55-acre sale had the lowest price a foot). The screen now shows
    the three cross-checks (A $649,782, B $617,652, C $610,864) beside the adjusted sales ($635,000 weighted;
    $590,000 to $700,000), reconciles them half and half (reconciled value $625,000), and the range runs from the
    lower to the higher of the four, rounded: **$610,000 to $650,000**, the same as the demo-house research. The
    model must say which adjustments push its figure away from the cross-checks (prompt `recommend.v2`). Sonnet
    now recommends **$640,000**: above the reconciled value for the pond, the updates and the lot, below the top
    for no central air, no garage, oil heat and state-route frontage. Replays re-recorded.
31. **The fair-housing gate needs both passes (2026-10-23, BUILD-2).** Copy is "passed" only when no block finding
    stands *and* the model review ran; a replay miss or the spend cap leaves the gate shut rather than letting the
    rules alone decide. `require_pass` checks the newest result is for exactly the current version and text (hash),
    so editing after a check always needs a re-check. Warn findings are rewritten by the AI (rule `fix`) and shown
    with its choice. The AI's fixed version prefers the model's rewrite when the rules pass it, else the rules' own
    fix (replace the phrase, or drop the sentence). The same gate serves messages in slice 3.
32. **Module name `listing_copy`, not `copy` (2026-10-23, BUILD-2).** A package named `copy` would shadow Python's
    standard `copy` module; the spec's `copy` module is `app/modules/listing_copy/`. Routes are still `/copy`.
33. **Slice 2 models (2026-10-23, BUILD-2).** After a live side-by-side on the demo house
    (`docs/build/model-side-by-side-slice2.md`): Sonnet 5.5 stays on pricing advice and listing copy (more specific,
    attributes seller facts; about $0.08 more a run), Haiku 5.5 on the fair-housing review; `copy.draft` gets
    8,000 output tokens after Haiku was cut off at 4,000. The channel board has no model call: every card is built
    from the connector stubs and the records, so its honesty does not depend on a model.
34. **The demo walks the buyer's side before the offers, and the demo seller's PCDS answers are one click
    (2026-10-23, BUILD-3).** Offer B in step 6 comes from the firm's own buyer, whom the buyer's AI advises and who
    approves the offer in step 8; and the buyer's reply to the seller's counter is approved on step 8's offer
    screen. So the walk is steps 1 to 5, then 8, then 6 and 7. `steps.yaml` holds that order, `DEMO-SCRIPT.md`
    says it, and the step list on screen stays in number order. The spec's wording ("step 8 shows the same deal from
    the buyer's side") was a flashback; making the buyer's decisions live is truer to SC8 (the buyer approves) than
    replaying them. Separately, the PCDS is the full 56-question form. The fictional demo seller's answers sit in
    `seed/personas.yaml` and the seller persona can submit them in one click: that is the seller's own act (only the
    seller persona can do it, and the record service refuses anyone else). Every field on the form still starts
    blank, and the answers are labelled fiction, not statements about the real house. Why: a 12-to-15-minute demo
    cannot type 56 answers, and the rule (L43; RPL §466) is that the software never fills the seller's form, which
    this keeps. Alternative: answer it by hand on screen (still possible).
35. **The counter carries terms, inside the seller's decision (2026-10-23, BUILD-3).** CP-12 now records, for a
    counter, the price, the lowest price the AI may agree, the counter's closing, the closing range the AI may agree,
    the longest inspection and mortgage-commitment periods, and whether the buyer's requests may stay. Code
    (`offers.outside_decision`) refuses any counter or agreement outside it: price below the floor or above the
    counter, closing outside the range, longer periods, a smaller deposit, other financing, new contingencies,
    unagreed or new requests, any seller credit. The seller's AI answers the buyer's side on its own: it agrees a
    reply inside the decision, counters again inside it otherwise, and opens a new CP-12 for the seller when nothing
    inside it is left. Concessions beyond these (repairs, credits) go back to the seller; that is post-inspection
    negotiation (CP-34, planned).
36. **Opus 5.5 drafts the contract; prompt `draft.v2` (2026-10-23, BUILD-3).** The spec's side-by-side
    (`docs/build/model-side-by-side-slice3.md`) had an independent close reading of both drafts on the same deal.
    It found Opus decisively better on New York mechanics: GOL §5-1311, the transfer-tax forms and no mansion tax,
    the deed covenants, the escrow terms, buyer protection on a withdrawn commitment, and certificate-of-occupancy
    searches. Sonnet had errors a lawyer would flag at once, such as the buyer having to close even if the lender
    refuses to fund. Both v1 drafts leaked the software's words and Opus invented numbers. `draft.v2` gives the
    disclosures in contract terms, keeps the software out, and asks for blanks instead of invented numbers. Opus
    costs about $0.10 more a live run and is used nowhere else. The contract call streams, because the SDK refuses
    a blocking call that might pass 10 minutes. Other slice-3 tasks run on Sonnet: offers advice, both sides'
    negotiation advice and the inbox replies, all read closely; the buyer's search alert runs on Haiku.
37. **Offer A is realistic weaker paper (2026-10-23, BUILD-3).** In the first recorded run the seller's AI rightly
    preferred the outside offer, which was then simply better ($630,000, 20% down), so the walk never reached the
    two AIs negotiating with each other. Offer A is now a common kind of weaker offer: 10% down, a 75-day closing
    and a contingency on the sale of the buyer's current home. On that paper the seller's AI advises countering
    offer B, and the walk follows the AI's own suggestion. The recorder and the live walk read the suggested offer
    and figures from the screen rather than hard-coding them.
38. **The information wall is enforced in code and on screen (2026-10-23, BUILD-3).** Every buyer-side model call
    is built from `AgentContext(buyer)`, the buyer's own state and public records, and never reads the seller's
    instructions or decision. Seller-side calls see offer B only as its terms. A test walks the whole demo and
    checks every model request by side, so no buyer limit, note or name reaches a seller-side call and no seller
    floor, lowest price or motivation reaches a buyer-side call. On screen, the buyer's private limit is hidden from
    the seller persona, and the seller's advice and decision are hidden from the buyer persona. The Presenter sees
    both, so the wall can be shown.
39. **A step link never redirects; the Presenter can fast-forward and "decide as" a client (2026-10-23,
    BUILD-FIX).** Joe, on his phone, could not get past step 1: after Start demo every later step answered a silent
    redirect to the intake, and later steps bounced again until a client decision was made under a persona nothing
    on screen mentioned. Now:
    - Every step screen renders. When it waits for something, a gate card says what is missing, on which step,
      who must do it, with a button to go there. The service-layer gates and their tests are unchanged.
    - The demo's walk is one list of milestones in walk order (`app/demo/walk.py`), each with a "done?" check and a
      "play" that makes the same choices as `scripts/live-flow.sh` through the same service calls the screens use.
      The gate card and the fast-forward both read it, so they cannot disagree.
    - "Fast-forward the demo to here" (the card and the step list, Presenter only) plays the missing milestones
      on the recorded replays ($0). Each client decision is recorded as the client's (the record service still
      checks the persona). Chosen over replaying HTTP clicks inside the app, which would need a second client and
      HTML scraping for the offer figures.
    - "Decide as the seller/buyer" on each client-decision card switches the persona in one tap and returns to the
      same card. The Presenter deciding directly is still refused (403).
    - Start demo asks first. On a phone a numbered step bar sits at the top, buttons are at least 44 px and nothing
      scrolls sideways, checked on every screen at 390 px by `scripts/phone-check.py`.
40. **The screens lead with the outcome; the working and the codes are folded (2026-10-23, BUILD-UX).** From the UI
    audit (`docs/build/ui-audit-2026-10-23.md`, Joe: "It looks weird, and it is not user friendly"). Every screen
    now opens with its result in plain English and one primary action; tables, drafts and records sit in "Show the
    working" folds. The presenter's script moved behind a "Presenter notes" button (a bottom sheet, closed by
    default; slice 4's guided mode builds on it). Each "NY law today" note leads with one plain sentence from a new
    `plain` field in `app/records/catalogue.yaml`; the rule, who must act, what the AI did, the codes and the
    research link sit under "Why". Nothing behavioural changed: every marker, decision, gate, record and refusal
    still renders and is recorded, and the tests only had selectors updated (the badge's `data-mode`, the notes'
    `id="presenter-notes"`). Display helpers in `app/humanize.py` (Eastern time, Yes/No, decisions in words) change
    the screen only. The contract screen now shows the parties' fictional names, and each view is access-logged like
    the PDF; masking stays for model calls and logs. Kept Bulma and the no-build rule (decision 7) with the system
    font stack, so nothing new is vendored; one accent (green ink) plus the three meaning colours. `tzdata` joins
    the requirements so Eastern time works in the slim image.
41. **The guided demo drives the presenter-notes layer; the narration never goes back on the audience's screen
    (2026-10-23, BUILD-4).** SC11's "narration card on each screen" is the presenter notes of decision 40, filled from
    `app/demo/steps.yaml` (say, point at, do, markers) with the presenter's controls first: **Next** (the following
    screen in walk order), **Do this screen for me** (plays that screen's taps through `app/demo/walk.py`, the same
    plays as fast-forward, on the recorded replays; each client decision still recorded as the client's) and
    **Spotlight** (Driver.js over the elements the script names, with short code-free captions the audience may read).
    Start demo turns the guided demo on: the notes open on every screen until the presenter closes them, which is
    remembered on that device. The notes open from the chrome (the phone's sticky step bar, "Notes"; the laptop's
    sticky step list, "Presenter notes"), so no button floats over the content any more (Joe's review: it hid the last
    lines). Chosen over a separate tour mode, which would have duplicated the gate cards, fast-forward and "decide as"
    the demo already has.
42. **Steps are numbered on screen in the order the demo walks them (2026-10-23, BUILD-4; Q47, the chat session's
    provisional call).** 1 Intake ... 5 Communications, 6 Buyer side, 7 Offers, 8 Contract, 9 Timeline, 10 Marketing
    the business. The step list, the phone bar, the gate cards, the timeline's cards, the screens' cross-references
    and `docs/DEMO-SCRIPT.md` all use these numbers. Records, routes, tests and the success criteria keep the SC
    numbers (`n` in steps.yaml; `shown` is the place in the walk); the demo script gives the mapping once. Tab titles
    are short ("Offers · Hudson Valley AI Realty"): the old ones ended "(demonstration)", which a phone cut to a
    stray ")".
43. **Step 10 adds a claims check and code-only notices to the fair-housing gate (2026-10-23, BUILD-4).** The firm's
    own advertising passes the same fair-housing pipeline as listing copy (CP-26) and a claims check in code: no
    "licensed" (CP-35: there is no broker of record), no "replaces your agent" or lawyer (L54), never "you do not need
    a lawyer" (L23), no reviews or testimonials, no guarantees; savings figures warn. The demo's planted headline is
    the claim the idea invites, "The AI that replaces your agent and your lawyer": the check refuses it. That is a
    hurdle reported, not the idea reshaped: advertising law bars the claim while New York still requires a licensed
    broker and the parties may always have lawyers. The landing page's notices (identity and broker-of-record line,
    fair-housing notice link, DOS-2156, AI-use notice, consent line) are added by code, never written by the model,
    and checked present before publishing. Ad targeting is chosen from an allowed list only (housing category, place by
    a 15-mile radius, everyone 18 and over, no interests or audiences); every blocked criterion is refused in code and
    logged (L38). The campaign's model context is the firm's config only: no deal, no property, no person. The
    founder is a placeholder token (Q49).
44. **The road to closing is one planned record per item, dated from the signed contract (2026-10-23, BUILD-4).**
    CP-22 (appraisal, mortgage commitment, title) and CP-23 (walkthrough, closing) became per-item codes, so the
    timeline lists all eight planned steps (with CP-20 escrow, CP-21 inspection and the planned CP-34 repairs marker),
    written at intake and dated on screen from the contract's signing and the agreed offer's periods. Per-item records
    written on another step now carry that step (a notice to the buyer is step 8, a campaign pass step 10), so each
    step's card counts what happened on it. The hurdle map groups each step's records by code with how often
    (CP-09 once per message), and the agent-acts log lists every act the AI did that NY law reserves, in order.
45. **Erase honours the request now and states the three-year rule (2026-10-23, BUILD-4).** "People and their data"
    exports everything about a person as JSON and erases a person's personal fields on request (documents never
    stored names, so they render "[erased]"); a tombstone keeps the transaction facts, and the erase is an audit event.
    New York requires a brokerage to keep its transaction records three years (L17), which pulls the other way: the
    confirm screen says so plainly. Provisional for production: erase marketing and other data at once, the signed
    records when the period ends (Q50). Only the firm (the Presenter) or the person may open a record: the seller
    never opens the buyer's, nor the buyer the seller's.
46. **The demo's fees follow WS4, and the founder placeholder is a styled fill-in (2026-10-23, BUILD-POLISH).** The
    chat session's review of slice 4 found `config/brokerage.yaml` charging $4,995 on each side while the executive
    summary, the plan and WS4 use $4,500 for the seller and $3,500 for the buyer, paid at closing on the broker-only
    route. The father-in-law reads both, so the config now carries WS4's figures (`flat_fee_usd` 4500,
    `buyer_fee_usd` 3500, each text still "demonstration figure" and "fees are not set by law and are negotiable"),
    and the pricing net sheet reads the number from config instead of a constant. Every model request that carried the
    fee or a figure derived from it was re-recorded (8 live calls, $0.3149): the firm's campaign and its four
    fair-housing reviews, and the seller's offer advice, whose "seller keeps" figures moved by $495. The new advice
    suggests a $635,000 counter (was $634,000), so the recorded deal now agrees at **$630,000** (was $629,000) and the
    buyer's counter advice and the Opus contract draft were re-recorded too. The eight superseded replays are deleted.
    Second, "[Founder's name]" in brackets read as a bug on the landing page: the campaign now renders the [FOUNDER]
    token as a dotted fill-in chip labelled "Founder's name" with the tooltip "Named once the founder agrees; see Q49".
    Q49's rule stands: no real person is named without consent. The campaign has no PDF; the chip is the only rendering.
47. **One path, one button (2026-10-23, BUILD-PATH; Joe: "it needs to be made more user friendly and simple, and
    self explanatory").** The sale is a single path of screens walked in order (`app/demo/steps.yaml`). Every screen
    ends in one sticky action bar: "← Back" on the left, one primary button on the right, always in the same place
    and the only "next" on the screen. The button comes from the walk (`app/demo/path.py`, `primary`), never from a
    template: while the screen has something to do it does the next undone milestone, worded for what it does ("Let
    the AI price the house", "Seller: list at $625,000"); when nothing is left it reads "Continue: <next screen>".
    Removed: the side panel's Next, the notes' Next, the step bar's arrows, the screen tabs and every hard-coded
    "Next:" button, so two "nexts" can no longer disagree. A secondary choice (decline, accept as offered) is a quiet
    button beside the primary. A button whose press makes the AI work disables itself and reads "The AI is working…"
    (`app/static/app.js`). After every action the next page opens with a one-line confirmation of what happened
    (a cookie read once, never stored). **The AI does its own work as soon as what it waits for is done**: after each
    client decision, the AI's next acts run at once, up to the next decision a client or a person must make (the
    "pump"), so the visitor presses only the clients' decisions, the one simulated person's step and Continue. Each
    AI act is still its own record, shown on its own screen with its "Show the working" folds; if one cannot run
    (a recorded demo meets a new situation, or the spend cap), the confirmation says so in plain words and the bar
    offers the AI's own button. Every action redirects to its screen (Post/Redirect/Get), and a GET to an action's
    address lands on its screen, never on `{"detail":"Method Not Allowed"}`. Borrowed from the GOV.UK Design System
    (MIT; patterns only, not its look): question pages (a Back link at the top of every page, one Continue button
    aligned left, the browser's Back keeps working, never ask twice and pre-fill what is known), check answers (a
    Change link beside every answer; changed pages show what was entered before) and the task list (honest statuses:
    done, in progress, not started).
48. **Nothing is lost, and everything can be changed (2026-10-23, BUILD-PATH).** Every form re-opens filled in with
    what was saved: the seller's intake, the buyer's intake, the buyer's offer, the counter, the seller's disclosure
    answers. Sending step 1 again updates the same house and the same deal, never a second one: contact details at
    once (nothing else redone), the house's address or facts only after a confirm that names exactly what will be
    redone (`walk.DEPS`, `path.change_plan`). Typing and then leaving by any link, button or the browser asks "Leave
    without saving?". Every client decision shows a "Change" link once made: the confirm names what re-opens ("the
    listing copy (step 5)"), then only that re-opens: **records are superseded, never deleted** (`records.supersede`,
    `records.reopen`; a new pending record replaces the old, which stays on the timeline as "changed"), module state
    is cleared for the undone milestones only, and the change itself is an event on the timeline ("Changes"). There is
    no fallback to resetting the demo. Pages are sent `Cache-Control: no-store`, so the browser's Back shows the page
    as saved now. In a recorded demo, every free figure (the price, the buyer's offer, the counter's figures and
    limits, the buyer's reply, the house and the buyer's needs) is the recorded one, with one line saying so; a
    different figure is refused in plain words before anything is saved or any model asked, with "Put the recorded
    figure back" (`app/demo/recorded.py`), so the deal is never stuck. With the live AI any figure works within the
    $12 cap.
49. **You play the seller and the buyer; the AI does everything else (2026-10-23, BUILD-PATH; Q51).** "View as
    Presenter / Seller / Buyer" is off the main screens. Every client-decision button is always active and names whose
    decision it is ("Seller: acknowledge the agency form", "Buyer: send this offer"); pressing it records the decision
    as that client's (the form field `as`). The record service still refuses a decision recorded for the wrong client
    or by anyone else, and **the AI never records a client decision**: the AI's endpoints and the pump call no
    decision function, which a test proves by walking the whole sale with `records.decide` forbidden while the AI
    works. SC impact: the old guarantee "a Presenter's attempt to decide for the seller is refused (403)" is replaced
    by "a decision is recorded as the client the button names; a decision sent as the buyer, the presenter or the AI
    is refused (403); the AI's own endpoints and plays cannot decide" (`tests/test_demo_usability.py`). The persona
    stays in the code for the access log and "People and their data", and "View as" moved to the menu. The
    information wall stays visible: on the buyer's sign-up, the buyer's offer and the offers, a panel "What each side's
    AI can see" shows the two sides next to each other (the buyer's ceiling shown on the buyer's side, hidden on the
    seller's). Said once, on the home page and step 1's line: "You play the seller and the buyer. The amber buttons
    are their decisions. The AI does everything else."
50. **The visitor's layer is the default; the presenter's is opt-in (2026-10-23, BUILD-PATH).** Anyone who opens
    the link sees the product only: no presenter notes, no "Guided demo · screen 6 of 20", no fast-forward icons, no
    "Do this screen for me", no record codes outside the "Why" folds. Each screen opens with one or two plain
    sentences for the visitor (`explain` in steps.yaml, written for the audience, separate from the presenter's
    "say"). Forms open pre-filled with the demo house and the demo buyer, with "Clear the form to type your own".
    "I'm presenting" in the menu (a cookie kept a year on that device) turns on the presenter's notes (a drawer
    beside the content on a laptop, which narrows the content column; a bottom sheet that starts closed on a phone),
    "Do this screen for me", the spotlight and skip ahead (in the menu and on the "not yet" card), and the demo
    devices (plant a violation, a bolder headline, a refused ad target, a counter by hand) in a "Presenter's tools"
    fold. Decisions the demo plays for a client are marked "(played by the demo)" on their card and on the timeline
    (`checkpoint.played`, added to existing databases by a one-column migration in `db.create_all`). One clock (deal
    times only; a recording's time is in the tooltip) and one counter ("Step n of 11").
51. **The path, the chrome and the ending (2026-10-23, BUILD-PATH).** Eleven steps of the sale, then the finale,
    then one more thing (20 screens before):

    | Step | Screen (route) | Built from |
    |---|---|---|
    | 1 | The seller signs up (`/intake`) | Address and facts |
    | 2 | The AI researches the house (`/intake/profile`) | Property profile + disclosure checklist |
    | 3 | The seller hires the firm (`/intake/onboarding`) | Seller onboarding |
    | 4 | The price (`/pricing`) | Comparable sales + the AI's price advice |
    | 5 | The listing (`/copy`) | Drafts and the fair-housing check + MLS pre-check and package |
    | 6 | On the market (`/channels`) | Marketing plan |
    | 7 | Enquiries and showings (`/inbox`) | Communications |
    | 8 | The buyer signs up (`/buyer`) | Buyer intake + search and alerts + tour and dual-agency consent |
    | 9 | The buyer's offer (`/buyer/offer`) | The buyer's offer |
    | 10 | The seller decides (`/offers`) | Offers, with the negotiation and the buyer's replies |
    | 11 | The contract (`/contract`) | Contract draft and signing + the seller's disclosure form |
    | Finale | The whole sale, start to finish (`/timeline`) | Deal timeline |
    | After | One more thing: how the firm finds sellers (`/brand`) | The firm's campaign + who sees the ad |

    Old routes redirect to their new screen and anchor (`steps.yaml` `merged`), so the review pages, the tests and
    any saved link still land. The step list is a progress list: done ✓, "You are here", in progress, or not
    started; a done step opens with its saved state; a not-started step opens the "not yet" card naming the step that
    is missing. Step 1 is done once the seller has saved it; the seller's disclosure form belongs to the contract step.
    Chrome: a one-line demonstration notice, a slim top bar (brand, "Step 3 of 11 · The price" on a phone, the menu),
    the progress list on a laptop with only "Start over" under it; the footer is one line (the firm's demonstration
    name and "No licensed broker of record (New York law requires one)" with its link). The spend, the research link,
    the data link, "Recorded run" and "View as" are in the menu. Each screen carries the visitor's line, the outcome,
    the one decision or action, the red and grey notes that belong to it, and "Show the working" folds. "Recorded on
    the deal timeline; it does not stop the flow" is said once (home and finale); every "NY law today" marker still
    renders on its screen and is still recorded. The finale says what the visitor just saw, with the totals, and
    offers "Start over", "Read the plan" and "One more thing". Marketing the firm comes after the finale, not as a
    step of the sale; SC10 stays met.
