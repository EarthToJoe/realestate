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
