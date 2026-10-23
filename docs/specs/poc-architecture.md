# POC architecture spec

**Status:** written 2026-10-23 (headless job), after Joe signed off `docs/SUCCESS-CRITERIA.md` and WS1 to WS3
landed; **revised 2026-10-23 for decision 21** (Joe: "Keep the original idea ... Completely replace the real estate
agents"). The overnight version designed the demo around a working broker and an attorney (broker approval gates,
"the AI never sets the price", "no message leaves without a human", the contract in the seller's attorney's
workspace); this revision removes those gates and personas and puts "NY law today" markers where they stood. This is
the document the build (Friday 2026-10-23 evening to Tuesday 10-27) works from. Traceability is in
`docs/TRACEABILITY.md`.

**Sources used:** `docs/SUCCESS-CRITERIA.md` (SC, as amended for decision 21), `docs/BRIEF.md` ("The idea",
"Demo-ability", workstream 7), `docs/OUT-OF-SCOPE.md`, `docs/DECISIONS.md` (D5 to D8, D13 to D22),
`docs/research/WS1-agent-functions.md` (F1 to F89), `docs/research/WS2-legal-licensing.md` (L1 to L62, sections 2,
10 and 11), `docs/research/WS3-listing-data-access.md` ("What the proof of concept automates, stubs and skips"),
`docs/research/handoff/WS1.md`, `WS2.md`, `WS3.md` (traceability items, WS3-C/D/R IDs), `WS7.md` (the "What already
exists" table). `docs/specs/demo-house.md` does not exist yet; section 4 defines the shape the demo-house data must
take. Model prices are from Anthropic's pricing page, read 2026-10-23 [PRIMARY]. No new web research in the
revision: it is a design change from existing findings.

---

## 0. Four things that shape the design (read first)

1. **The design follows the brief's idea (decision 21).** The AI is the agent on both sides and does every agent
   act: it accepts the listing, advises on price, writes, checks and publishes the marketing, answers and sends
   messages (sending simulated), schedules showings, presents offers and advises, negotiates counters with the other
   side, drafts the contract and rider, coordinates to closing and markets the business. **The seller and the buyer
   make their own decisions**, as any agent's clients do (sign the listing or buyer agreement, choose the list
   price, accept / counter / reject, approve their offer, give consents, complete their own Property Condition
   Disclosure); those stay blocking. **Wherever New York law today requires a licensed person or a lawyer, a red
   "NY law today" marker** names the rule in one plain sentence, who the law says must act, the F- and L-IDs and a
   link to the finding; it is recorded and counted on the timeline and **does not stop the flow** (the brief: "Every
   step where a human or a license is still required should be visible in the demo itself so it illustrates the
   hurdles"). Marker text is written as the research states the rule, never softened.
2. **The software drafts the contract for the parties, in the product's own contract step.** There is no attorney
   persona or attorney workspace. The step carries the marker: *drafting a contract of sale for another is the
   practice of law in New York; only a lawyer may do it, and a company may not practise law at all (L21, Judiciary
   Law §§478, 484, 495); a broker may only fill non-legal facts into a form marked subject to each party's attorney's
   approval (L22, AG Op. 96-F11); and Hudson Valley custom is that the seller's attorney drafts (L25, custom, not
   law).* Every page of the draft is labelled (section 3, step 7). The product never tells anyone they do not need a
   lawyer (L23); that is the software complying with a rule, like the fair-housing checker, not a lawyer in the loop.
3. **The demo house is a real address (146 Rt 292, Holmes, NY 12531, D18), so every piece of listing copy carries a
   "DEMONSTRATION: not a listing, not for sale through this firm, no owner authority" mark.** Marketing a property
   without the owner's written authority is itself a rule (L9) and the copy names a firm (L10). The flyer, social
   posts and portal text are watermarked in the HTML and the PDF; nothing is ever sent. No owner name is stored; no
   portal photos or copy are used (CLAUDE.md research rules; WS3-R8).
4. **WS3 found no listing-input API for OneKey MLS or any portal.** So MLS entry is a visible "human required" step,
   a fact about the MLS, not a design choice: the AI prepares a complete, rule-checked listing package for the
   licensed MLS participant (or the participant's registered Administrative User) who keys it in (WS3-C1), and
   portals are shown as fed from the MLS (WS3-C4, C8 to C10, C12). Other practical "human required" steps stay for the
   same reason: notary and wet-ink items, and third parties (inspector, appraiser, lender, title, escrow holder).

---

## 1. What already exists

Checked 2026-10-23 by WS7 (licences and versions from the publishers' pages or registries; detail in the WS7
notes, sections G1 to G14). Decision column: what the POC does with each. Unchanged by decision 21 except where a
row mentioned approvals or attorneys.

| Candidate | Building block | Licence / cost | Decision | Why |
|---|---|---|---|---|
| FastAPI 0.161.1 + Jinja2 3.1.6 + uvicorn 0.54.0 | Web app, server-rendered screens | MIT / BSD; free | **Adopt** | Decision 7; current; each step is a plain page that shows its own AI work |
| htmx 2.0.11 (+ jinja2-fragments 1.12.0) | Partial updates without a JS build | 0BSD / MIT; free | **Adopt** (vendored file) | No build step; 4.0 is not `latest` until 2027 |
| Bulma 1.0.4 | CSS | MIT; free | **Adopt** | CSS-only, maintained (Pico is unmaintained); step list and timeline are ~50 lines of our own CSS |
| Anthropic Python SDK 2.1.0 (structured outputs, `messages.parse`) | Every AI step | Apache-2.0; per token | **Adopt** | One schema-checked call per AI step, logged as a visible AI action |
| Claude Agent SDK 0.2.173 | Agent loop with tool approvals | MIT file, Anthropic terms | **Borrow ideas** (`can_use_tool`, deny hooks) | ~130 MB, built for coding agents; the POC needs single calls whose every act is a visible, recorded step |
| PydanticAI 2.60.0 / LangGraph 1.2.16 | Human-in-the-loop frameworks | MIT; free | **Borrow ideas** (deferred tools, interrupt and resume) | Client-decision gates must be enforced server-side anyway; extra layer between screen and call |
| python-statemachine 3.2.2 (or transitions 0.9.3) | Deal states and decision guards | MIT; free | **Try first**, provisional hand-roll | Records already drive the timeline; adopt only if the day-1 try saves code |
| SpiffWorkflow 3.2.0 | BPMN engine | LGPLv3 | **Skip** | Far more machinery than 11 steps need |
| HumanLayer | Approval service | n/a | **Skip** | Pivoted to a coding IDE |
| ArkansasONE MLS list (Mar 2026), OneKey list, NYC CCHR examples, DOS-2156, HUD 1995 memo | Fair-housing rule content | Publishers' copyright; free to read | **Borrow ideas**; write our own rules | No authoritative list exists (HUD 2024 guidance withdrawn effective 2025-09-17); lists conflict |
| Zillow fair-housing-guardrail + FairHome dataset | Classifier and test data | OpenRAIL-S; data by request | **Borrow ideas** (stop list + classifier + prompt) | PyTorch-scale; an API model does the review; dataset request deferred (Q-WS7-5) |
| FairProp-AI, debary-mcp-compliance, real-estate-pack | Community checkers | MIT / Apache | **Skip** | 0 to 11 stars, unverified |
| docxtpl 0.20.2 (python-docx 1.2.0) | Editable DOCX of the contract draft | LGPL-2.1 (MIT); free | **Adopt** | The parties (or anyone they choose) can edit in Word; used unmodified as a library |
| WeasyPrint 70.0 | PDF of flyer, disclosures, contract | BSD; free | **Adopt, try first** | Reuses the Jinja HTML; needs Pango ≥ 1.44 (inside the Docker image, so the host's Pango no longer matters) |
| pypdf 6.21.2 / ReportLab 5.1.0 | PDF merge / fallback | BSD; free | **Adopt pypdf**; ReportLab fallback | Permissive, current |
| PyMuPDF 2.0, borb 3.0.9 | PDF | AGPL | **Skip** | AGPL in a product |
| docassemble 1.10.14 | Guided interviews, document assembly | MIT; free | **Borrow ideas** | Needs 4 GB RAM and 40 GB disk host |
| NY statutory forms (RPL §443 agency form, RPL §462 PCDS, DOS-2156, EPA lead-paint) | Disclosure templates | Statute text / federal; free | **Adapt** (render from statute text) | DOS still serves a 2023 PCDS with the repealed $500 credit; generate from current §462 |
| NYSAR statewide purchase agreement | Contract form | Member-only | **Borrow structure only** in POC | Text not public (Q-WS7-1, Q-WS7-2) |
| Bar-association Residential Contract of Sale (11-2000) | Contract structure | No licence visible | **Borrow ideas** (section headings only) | Structure is not protected expression; clauses would be |
| pyHanko 0.38.0 | Tamper-evident seal on simulated signing | MIT; free | **Try first**; first thing cut if late | Nice proof of integrity; "beta" |
| DocuSeal 3.3.3, BoldSign, Dropbox Sign, DocuSign, Documenso, OpenSign | E-signature | AGPL or paid | **Skip in POC**; production comparison | OneKey's TransactionDesk/AuthentiSign may be included in membership (unconfirmed) |
| presidio-anonymizer 2.2.364 | PII masking | MIT; free | **Adapt** (our own regex recognisers; no spaCy) | Demo data is fictional and structured; we know which fields are PII |
| sqlcipher3 0.6.4 | SQLite encryption at rest | Zlib + BSD-style; free | **Try first** (15 min, day 1); fallback Fernet columns | Wheel on 3.12 and SQLAlchemy dialect fit unverified |
| cryptography 50.0.2 (Fernet) | Field encryption | Apache/BSD; free | **Adopt** | PII columns encrypted whatever happens with sqlcipher |
| Append-only `events` table with hash chain (sqlite-chronicle pattern) | Audit, access and AI-action log | Pattern; free | **Adopt pattern, build ours** | One record family shows every AI action and every client decision |
| structlog 26.1.0 | Application logs without PII | MIT/Apache; free | **Adopt** | Processor masks PII before writing |
| nh3 0.3.7 | Sanitise model output | MIT; free | **Adopt** | Model output is untrusted input for HTML and PDF |
| Langfuse / Arize Phoenix | LLM tracing | MIT core / Elastic | **Skip** | ~17.5 GiB RAM; our own call log is the visible log |
| Anthropic Usage and Cost Admin API | Spend reconciliation | Free | **Adopt if** an org Admin key exists (Q-WS7-4) | Per-call usage from the SDK already gives per-module cost |
| Driver.js 1.10.2 | Spotlight in guided demo | MIT; free | **Adopt, try first** with HTMX swaps | Only current MIT tour library; cut before narration cards |
| Shepherd.js / Intro.js | Product tour | AGPL / commercial | **Skip** | Licence cost; Driver.js is free |
| Arcade / Storylane | Recorded click-through | SaaS | **Skip** (maybe a leave-behind later) | The live app is the demo |
| RESO Data Dictionary 2.0 (~40-field subset) + UPI 2.0 | Property field names, parcel ID | RESO EULA, royalty-free | **Adopt** | Free; eases later MLS work; listing package in OneKey field order |
| RESO Offer Management standard | Offer fields | RESO | **Borrow ideas** (read before building the offers table) | Industry names for offer terms |
| reso-tools / web-api-commander | RESO validation | RESO EULA | **Skip** | Node/Java; POC does not speak RESO Web API |
| usaddress 0.5.16 (scourgify after licence check) | Address parsing at intake | MIT | **Adopt** usaddress | Normalises the intake address |
| Census Geocoder / NYS Geocoder | Address to coordinates and county | Public | **Adopt behind an interface**; demo uses stored fixture | Call the Census API directly (wrapper is GPLv3) |
| FEMA NFHL, NYS Tax Parcels, Open NY assessment rolls | Public-record facts | Public data | **Borrow later**; FEMA point query **try first** | Shown as "public record" tags; never used to help fill the seller's PCDS |
| Leaflet 1.9.4 + OSM tiles | Map | BSD-2 / ODbL | **Adopt** (vendored) with a static-image fallback | OSM forbids bulk/offline use; meeting may lack internet (Q-WS7-3) |
| MapLibre / OpenLayers | Vector maps | BSD | **Skip** | Heavier, no demo gain |
| Chatwoot CE / Cal.com | Inbox / scheduler | MIT / AGPL | **Skip; borrow inbox layout** | Each adds Postgres and Redis |
| pytest 9.1.1 + Playwright 1.64.1 (`--only-shell`) | Tests, headless end-to-end run | MIT / Apache | **Adopt** | Headless shell avoids ~281 MB Chromium |
| promptfoo / inspect-ai / deepeval | LLM eval harness | MIT / Apache | **Skip** | pytest covers the 40+ fixtures |
| EspoCRM / Krayin / Twenty | Whole-product baseline | AGPL / MIT | **Skip** | Generic CRM screens hide the split between AI acts, client decisions and the acts NY law reserves, which *is* the demo |
| AleksNeStu/ai-real-estate-assistant | Reference AI real estate app | MIT | **Borrow ideas** (simulated-response demo mode) | Too large to adopt; confirms the replay idea |
| Ocusell List (OneKey) | MLS entry with AI remarks and rule checks | Proprietary, free to members | **Production path** for the human MLS entry | Not an API; shown as the tool behind CP-08 |

**Could one of them be our baseline?** No single product is. The candidates that come closest (a CRM, docassemble,
Chatwoot) each hide the one thing the demo exists to show, the line between what the AI does, what the client
decides and where New York law today reserves the act, and each is heavier than the VPS allows. So we adopt
libraries, not a product, and build only what is ours: the record model, the fair-housing rules, the NY-specific flow
and the screens.

**Tried on a real example before committing (slice 1, time-boxed to 2 hours total):**

| # | Try | Pass condition | If it fails | Result (2026-10-23, BUILD-1; script in `scripts/try/`) |
|---|---|---|---|---|
| T1 | WeasyPrint 70.0 inside the Docker image (Debian Pango) | 10-page contract HTML renders to PDF under 5 s | ReportLab for the flyer; contract as DOCX + HTML print view | **Pass.** 30 pages in 1.06 s inside the image (1.31 s on the host); image 477 MB. Adopted. |
| T2 | sqlcipher3 0.6.4 with SQLAlchemy | create, encrypt, reopen | Plain SQLite + Fernet-encrypted PII columns (planned anyway) | **Pass.** Wheel installs on 3.12; file encrypted on disk, reopens with the key, wrong key refused. Adopted: with a `DB_KEY` secret (the server) the whole database is SQLCipher; Fernet PII columns stay; locally plain SQLite. |
| T3 | python-statemachine on the deal lifecycle | fewer lines and clearer guards than ~80 lines hand-rolled | Hand-roll (provisional default) | **Fail, fallback taken (hand-roll).** It works (50 lines for 7 states), but a refused transition only says "Can't Sign listing when in Intake", not which client decision is missing and why; it holds a second copy of state the records already hold; and its single linear state does not fit decisions that run in parallel (the PCDS, the buyer side). The record service's `require()` (12 lines) gives the code, the rule and whose decision it is. |
| T4 | Driver.js tour across two HTMX swaps | spotlight survives the swap | Narration cards only | **Pass.** Spotlight on the swap container (the app's pattern: stable `hx-target`, innerHTML swap) survives two swaps with the popover shown; a spotlight on an element the swap replaces needs re-pinning on `htmx:afterSettle` (one line), then also passes. Adopt in slice 4. |
| T5 | FEMA NFHL point query + Census geocoder on 146 Rt 292 | returns zone and county | Use the stored fixture; connector stays a stub | **Partial, fallback taken.** Census geocoder matches "146 RTE 292, HOLMES, NY, 12531", Dutchess County. FEMA's NFHL server did not answer from the VPS (no connection, as during the demo-house job). Fixture kept; connector stays a stub. |
| T6 | Regex masker on a sample buyer message, model call, re-insert | names, e-mail, phone never reach the request body | Drop free-text from the model context | **Pass.** Live Haiku call: the request held only `[BUYER_1]`, `[BUYER_1_EMAIL]`, `[BUYER_1_PHONE]`; the reply used the tokens; real values were put back only in the rendered text. Test `test_t6_tokenize_roundtrip_keeps_pii_out_of_the_request`. |
| T7 | Leaflet + OSM + static fallback | map renders; fallback image shows offline | Static image only | **Pass.** Headless Chromium: 6 OSM tiles loaded online; with tile requests blocked, the static SVG fallback (pin, address, coordinates) shows after 3 tile errors. No tiles are stored (OSM policy). |
| T8 | pyHanko seal on a generated PDF | a reader flags an edit | Cut (first item on the cut list) | **Pass.** pyHanko 0.38.0 seals a WeasyPrint PDF with a self-signed demo certificate: `intact=True`; one byte changed after sealing: `intact=False`. Keep for slice 3 (still first on the cut list). |

---

## 2. Stack, locked

**Decision 7 is confirmed, with additions; decision 21 changes the flow, not the stack.** The product is a sequence
of screens over one small database, with single model calls rather than an autonomous agent loop: each AI act is one
visible, recorded step, and each step that waits does so only for the seller's or the buyer's own decision. That
shape is exactly what server-rendered Python does well.

| Layer | Choice | Reason from the research |
|---|---|---|
| Language | Python 3.12 (already on the VPS with `uv`) | WS7: ~200 MB of permissive packages; A11 dodged |
| Web | FastAPI + Jinja2 + htmx (vendored), Bulma CSS, no JS build | Each SC step is its own visible screen; htmx shows "AI thinking → result → marker" without a SPA |
| Data | SQLite (one file) via SQLAlchemy 2.0 ORM; Fernet on PII columns; sqlcipher3 if T2 passes; no migrations tool (the POC rebuilds from seed) | One database for all PII (SC "PII"); fits 8 GB RAM and the disk |
| Model | Anthropic Python SDK behind a `ModelProvider` interface; structured outputs (Pydantic schemas) | SC "swapping the model provider changes no screen" |
| Documents | WeasyPrint (PDF), docxtpl (editable DOCX), pypdf | WS7 table |
| Logs | structlog with a PII-masking processor; own append-only `events` table | SC "PII kept out of application logs"; one record family for audit |
| Sanitising | nh3 on every model output before HTML or PDF | Model output is untrusted |
| Demo | Driver.js (vendored), Leaflet (vendored) | Only MIT tour library; offline fallback for the map |
| Tests | pytest + Playwright headless shell | SC "fast test suite including an end-to-end demo run" |
| Not used | Node toolchain, React, Postgres, Redis, agent frameworks, vector stores | Disk and build complexity; every AI act must be a single visible, recorded call; WS3-D6 forbids persistent embeddings of MLS data anyway |

**Deployment.** One Docker image (`python:3.12-slim` + Pango/HarfBuzz for WeasyPrint, ~450 MB estimated
[INFERENCE]), one container, uvicorn with 2 workers (2 vCPU). hughesnode project `realestate` changes type from
`static` to `docker` (D13); the house login stays in front at the Traefik gate, so the app adds no login of its own
and accepts whatever the gate passes (CLAUDE.md house-password rule). Inside the app, a **persona switcher** has
three personas: **Seller**, **Buyer** and **Presenter**. Client-decision buttons are enabled only for the client
whose decision it is (the check is server-side, so the Presenter or the Buyer cannot accept an offer for the seller
even by crafting a request). The Presenter can trigger AI acts ("Let the AI do this"), simulated third-party events
and simulated "human required" completions, but never a client decision. There is no Broker or Attorney persona
(decision 21).

- Volumes: `/srv/realestate/data` (SQLite file, replay cache, generated PDFs), `/srv/realestate/secrets` read-only
  (`ANTHROPIC_API_KEY`, `PII_KEY`), and the review pages directory read-only.
- **Review pages kept at the same address.** `scripts/publish-review.sh` writes to
  `/srv/hughesnode/apps/realestate/public`. The app serves the POC at `/` (step list home with a "Review documents"
  link) and mounts that directory as static files so existing links such as `/docs-success-criteria.html` keep
  working; "NY law today" markers link to these pages. Slice 1 checks with `hn help` how a docker-type project lays
  out its directory; if `public/` moves, `OUT=` in `publish-review.sh` is updated in the same commit.
- **Local run, one command:** `uv run --with-requirements requirements.txt uvicorn app.main:app` (wrapped as
  `make run`), or `docker compose up`. Without a key, the app starts in replay mode.
- Resource budget: ~250 MB RAM at rest, SQLite file under 50 MB, image under 600 MB; disk check before the build.

---

## 3. Module map

Each module is a Python package `app/modules/<name>/` with `routes.py` (screens), `service.py` (logic),
`prompts/` (versioned prompt files) and `schemas.py` (Pydantic output schemas). Modules talk only through these
interfaces, so a stub can be replaced by a real connector without touching a screen:

| Interface | POC implementation | Later |
|---|---|---|
| `ModelProvider.generate(task, schema, context)` | `AnthropicProvider`, `ReplayProvider` (recorded outputs), `FakeProvider` (tests) | another vendor |
| `AgentContext(side)` | Builds the model context for the **seller's AI** or the **buyer's AI** from side-scoped fields only (information wall, decision 24) | designated-agent walls in production |
| `PublicRecordConnector` | `FixtureRecords` (demo-house JSON, comps JSON) | Open NY assessment rolls, NYS parcels, FEMA |
| `MLSConnector.submit(listing)` | `StubMLS` returns `HumanRequired(reason, who, f_ids, l_ids, link)` | only if OneKey ever offers an input API |
| `PortalConnector.status(listing)` | `SimulatedPortals` ("fed from OneKey in about 24 to 48 h") | none needed: portals syndicate from MLS |
| `IDXConnector.search(criteria)` | `FictionalListings` (live query per session, no stored embeddings, WS3-D6) | MLS Grid IDX after licence and AI addendum |
| `MessageTransport.send(msg)` | `Outbox` (marks "sent (simulated)") | e-mail/SMS provider with consent checks (L50 to L52) |
| `SignatureProvider.sign(doc, party)` | `SimulatedSign` (+ pyHanko seal if T8 passes) | TransactionDesk/AuthentiSign or DocuSeal |

**Three on-screen components, one per record kind that needs one** (all rendered from the record, never hand-placed):

- **"NY law today"** (red): the rule in one plain sentence, who the law says must act (licensed broker or attorney),
  the F- and L-IDs, a link to the finding on the review site (for example
  `https://realestate.hughesnode.com/docs-research-ws2-legal-licensing.html`), and the line "Recorded on the
  timeline; does not stop the flow".
- **"Human required here"** (grey, with a hand icon): the practical reason no software route exists, who must act,
  the IDs and the link (for example `.../docs-research-ws3-listing-data-access.html` for MLS entry).
- **"Your decision"** (amber): the choice in plain words with the AI's advice beside it; buttons enabled only for
  the client whose decision it is; the next step waits for it.

### Record model (replaces the overnight checkpoint model)

One record type, the **checkpoint record**, carries a `kind`. The CP numbers of the overnight spec are kept wherever
the step survives, so `docs/TRACEABILITY.md` stays stable; new records are CP-25 onward.

| Kind | Meaning | Blocking? | Who acts in the product | Timeline colour |
|---|---|---|---|---|
| `client_decision` | The seller's or buyer's own decision, as any agent's client makes it | **Yes**: the service layer refuses the next step's action until it is decided | Seller or buyer | Amber |
| `law_marker` | An agent act the AI did where NY law today requires a licensed person (**L**) or a lawyer (**A**) | No | AI (the law says L or A) | Red |
| `human_required` | A practical step with no software route (MLS keying, notary, someone at the door) | No in the demo: the Presenter records a simulated completion; downstream cards read it | A person outside the product | Grey, "Human required" badge |
| `third_party` | Inspector, appraiser, lender, title, escrow holder; planned steps | No (planned) | Third party | Grey |
| `automated` | A logged AI act with no NY-law issue (notices delivered, fair-housing pass, scheduling, document assembly) | No (the fair-housing gate is enforced in code, see section 5) | AI | Blue |

Marker and record texts live in one file, `app/records/catalogue.yaml` (code, kind, step, actor, law_actor, rule
sentence, who, F-IDs, L-IDs, WS3 IDs, link). The service writes records from it; a test fails if any `law_marker`
or `human_required` entry lacks a rule sentence, a who, at least one F-ID, at least one L-ID (or WS3 ID) and a link,
or if any CP code is missing from `docs/TRACEABILITY.md`.

### Step-by-step map

**Who acts** = who performs the step in the product. Records end or accompany the step (catalogue below). "Marker"
means a red "NY law today" marker.

| SC # | Module | Screens | Who acts | What the AI does on screen | Records and markers |
|---|---|---|---|---|---|
| 1 Intake | `intake` | Address + facts form ("Use demo house"); Property profile; Disclosure checklist; Seller onboarding | AI; seller decides | Parses the address; pulls fixture public-record facts; fills gaps it can infer (e.g. "likely septic: no municipal sewer on this road" → tagged *inferred*, with reason); every field shows a source chip: Seller / Public record / Inferred. Builds the disclosure checklist (PCDS, lead paint if built before 1978, agricultural district, four RPL §242 questions). Sends the fair-housing notice, agency form and "not legal services" notice (logged). Gives the listing presentation (services, flat fee, timeline; F5, F7), runs a conflicts check and **accepts the listing**; generates the listing agreement with the six-point exclusive-listing explanation (L14). | CP-24 automated (notices, F8; L39, L12, L29); CP-01 seller acknowledges agency form (F9; L12); **CP-02 marker L**: accepting a listing for another for a fee is a licensed broker's act (F12; L1, L5); CP-03 seller signs the listing agreement; no marketing until it is stored (F13; L9, L14, L34); CP-04 seller completes the PCDS; the software never pre-fills it (F15; L43) |
| 2 Pricing | `pricing` | Comparable sales table; Adjustments; Suggested range; AI's recommended price and reasoning; Net sheet; Seller's price choice | AI advises; seller decides | Code computes adjustments (size, lot, age, condition, date) from ≥3 Dutchess comps; the model writes the method in plain words, flags weak comps and **recommends a list price with its reasoning**. Labelled "Comparative market analysis, not an appraisal" (F21; WS3-D5). | **CP-25 marker L**: advising the seller on price is the listing agent's fiduciary duty; unlicensed help, people or software, may only prepare the analysis, and what software does is the broker's act (F22; L6, L18; WS3-D5); CP-05 **seller chooses the list price** (F22, F24; L9; WS3-R9) |
| 3 Listing copy | `copy` + `fairhousing` | Drafts (MLS remarks, portal description, 3 social posts, flyer); Fair-housing check panel; MLS rule pre-check; Publish | AI | Writes all copy from the profile; checker runs visibly: rule hits highlighted with rule ID, class, legal basis and a fixed version; "Plant a violation" demo button inserts "perfect for a young family, steps from the church" and shows it caught; the AI applies the fix; re-check passes. MLS pre-check: required fields, no compensation in remarks, not "free" (WS3-R6, R7). **The AI marks passing copy "ready to publish"**; copy with any block finding cannot be marked. | CP-26 automated (fair-housing pass per artifact; F78, F81; L36, L37, L61); **CP-06 marker L**: only the broker may place advertising and must approve each ad; what software does is the broker's act (F26, F76; L10, L18, L36) |
| 4 Marketing plan | `channels` | Channel board | AI; seller decides; human required for MLS keying | Fills each card's status from the connectors: OneKey MLS **human required** (with the prepared package in OneKey field order); Zillow / Realtor.com / Redfin / Homes.com / OneKeyMLS.com "fed from the MLS"; firm website held by the Clear Cooperation clock (automated, WS3-R1); social "drafted and scheduled"; Google Business Profile draft; photos, sign, lockbox "vendor booking"; open house "owner hosts". Each marker links to its research finding. | CP-07 seller signs the marketing-exposure choice and authorisations (cooperating brokers, lockbox, photographer) (F32, F38; L9; WS3-R2, R3); **CP-08 human required**: no listing-input API; a licensed MLS participant or registered Administrative User keys the listing, and the participant stays responsible for every field (F28, F85; L16; WS3-C1, OneKey Rules 205, 320) |
| 5 Communications | `inbox` | Seller's fact sheet and authority; Shared inbox; Thread; Showing scheduler; Feedback log; Outbox | AI answers and sends; seller decides only the seller's decisions | Seller approves the fact sheet and the AI's authority first. Simulated enquiries arrive; **the AI answers and sends on its own** ("sent (simulated)") from the approved facts, within the seller's authority. Every outgoing message passes the fair-housing check and carries the firm's identity block (L10); first substantive contact gets the agency form and fair-housing notice (CP-24). Questions only the seller can answer ("would the seller take X?", a showing outside the seller's windows) become a decision card for the seller; nothing else reaches them. Legal questions get "I can't give legal advice; you may ask your own lawyer" (L23); school or neighbourhood questions get neutral official links only (L37). Discloses known material facts from the PCDS and fact sheet to the other side (F83). Books showings within 24 h (WS3-R4) after checking the buyer agreement (L15): an owner-hosted showing or a self-guided tour. Summarises feedback (F42). | CP-27 **seller approves the fact sheet and the AI's authority** (blocking: no reply leaves before it) (F33, F84; L9, L18); **CP-09 marker L**, one per outgoing message that discusses the listing with a prospect, negotiates or advises: negotiating for another is a licensed act, and DOS treated discussing listings with prospects as salesperson activity (F2, F33, F48; L1, L6, L18; DOS v. Ardelean via WS1); CP-29 automated (showing scheduled, access and feedback requests; F37, F42; L15; WS3-R4); CP-10 **human required**: someone must open the door; the owner may show their own home, not acting "for another" (F39, F40; L19 [INFERENCE]); **CP-28 marker L** for a self-guided tour: NY has not decided whether an unaccompanied buyer tour is a licensed showing; DOS treated an unlicensed person showing listings as unlicensed activity; OneKey lockbox keys and PINs may not be lent (F39; L19, L15; WS3-R4, Rule 405.8) |
| 6 Offers | `offers` | Offer comparison table; Net sheets; AI's advice on each offer; Seller decision; Negotiation thread | AI presents, advises and negotiates; seller decides | Two offers: A from an outside buyer's agent (simulated other firm), B from the firm's own buyer (step 8). Code builds the comparison and net sheets (F46, F65); the model **presents every offer and advises** with reasoning (price, contingencies, dates, risk). After the seller decides, the seller's AI **negotiates the counter with the buyer's side**: a counter inside the seller's decision is sent (simulated); code checks price and terms against the seller's decision and authority and sends anything outside back to the seller. Offer papers carry "not binding until a formal contract is signed by both" (L24). | **CP-11 marker L**: presenting offers and advising on them is a licensed broker's act (F45, F47; L1, L18); CP-12 **seller decides**: accept, counter or reject (F47; L24); **CP-13 marker L**, one record per side: negotiating price, terms and concessions for another is a licensed act (F48, F49; L1, L18) |
| 7 Contract | `contract` | Accepted-offer memorandum; Contract draft + rider; Side-by-side with the standard form's structure; Disclosures attached; Signing map; Signing | AI drafts; seller and buyer sign | Memorandum sent to both parties (F50). The model **drafts a NY-style contract of sale and rider** pre-filled from intake and the accepted offer, in the product's own contract step; the side-by-side lists the bar-association long form's section headings against the draft's with a one-line note per difference; disclosures attached (PCDS, lead paint, ag district, §242 notices); signing is blocked until the PCDS is delivered (L43). Signing map: e-signable (L34) vs wet ink or notary (deed acknowledgment, POA with two witnesses, L35; smoke-detector affidavit at conveyance, L45). Every page of the draft (HTML, PDF, DOCX) carries: "DEMONSTRATION. Drafted by software for the parties. NY law today: only a lawyer may draft a contract of sale for another (L21, L22)." The product never says a lawyer is unnecessary (L23). | CP-32 automated (memorandum sent, disclosures attached; F50, F59; L43, L44, L46, L60); **CP-14 marker A**: drafting a contract for another is the practice of law in NY; companies may not practise law; brokers may only fill non-legal facts into a form subject to each party's attorney's approval; Hudson Valley custom is the seller's attorney drafts (F52; L21, L22, L25); CP-15 **human required**: wet ink and notary items at closing (F67; L35, L45); CP-33 **seller and buyer sign the contract** (simulated e-sign; F59; L24, L34, L43) |
| 8 Buyer side | `buyer` | Buyer intake + representation disclosure; Search alerts; Tour request; Offer advice, draft and approval | AI is the buyer's agent; buyer decides | Guided intake (needs, budget, pre-approval status, no protected-class questions; F6, F18, F19); the AI **takes the buyer on as a client** and records the agency relationship; agency form and fair-housing notice sent; search over fictional listings with no steering filters (L37) and alerts; tour request blocked until the buyer agreement is signed (L15), then booked as a self-guided tour or an owner-hosted showing; because the buyer wants the firm's own listing, the dual-agency consent screen appears for both clients. The buyer's AI (separate context, decision 24) **advises on offer price and terms and drafts the offer** from the buyer's answers; after the seller's counter it advises the buyer and negotiates the reply. Step 8 shows the same deal from the buyer's side: the screens the buyer used before and during step 6. | **CP-30 marker L**: taking on a client and deciding the agency relationship are the broker's acts; designated agents must be two licensees under the broker (F11, F12, F51; L1, L5, L13); CP-16 **buyer acknowledges the agency form and signs the buyer agreement** before any tour (F9, F17; L12, L15); CP-17 **seller and buyer consent to dual agency** in writing (F11, F51; L13); **CP-31 marker L**: advising the buyer on price and terms is the buyer's agent's fiduciary duty; unlicensed help may only prepare it (F23, F44; L6, L18, L22); CP-18 **buyer approves the offer** and, later, the reply to the counter (F44; L24); CP-28 / CP-10 for the tour; CP-13 (buyer side) for the negotiation |
| 9 Deal timeline | `timeline` | Deal dashboard; Hurdle map; Agent-acts log | display only | No model call. Built only from checkpoint records and the deal's step table: one row per step, the AI's work shown blue, and one chip per record in its colour: **AI did it** (blue), **the seller or buyer decided** (amber), **NY law today: licensed broker or lawyer** (red), **third party / human required** (grey). Each chip shows status, who acted, when and the reason. Future steps (deposit escrow, inspection and repair negotiation, mortgage, appraisal, title, walkthrough, closing) are planned records with third parties named. Header counts: markers recorded (by L and A), client decisions, human-required steps, third-party steps. The **hurdle map** lists every red marker with its rule, who the law says must act and the link, grouped by step. The **agent-acts log** lists every AI agent act with its marker: what a supervising broker would review (F75). | Displays all records; CP-20 to CP-23 and CP-34 as planned; **CP-35 marker L** (standing, at the top of the timeline and in the identity block): a brokerage must be licensed through a broker who really controls it and supervises all unlicensed staff and systems; unlicensed brokerage is a crime and earns no fee (F73, F74, F75; L2, L3, L4, L5) |
| 10 Marketing the business | `brand` | Campaign drafts (landing page, one local ad, one seller lead magnet); Fair-housing panel; Targeting panel | AI | Drafts and publishes (simulated) the brokerage's own campaign naming the firm and the founder (F1, F3, F4); same fair-housing pipeline; targeting panel shows only allowed criteria (no age, family, ZIP or lookalike targeting, L38); AI-use and fair-housing notices on the landing page (L40, L55); no deceptive AI claims (L54). | CP-26 automated (fair-housing pass); **CP-19 marker L**: only the broker may place advertising and must approve each ad (F1, F76; L10, L18, L38) |
| 11 Demo mode | `demo` | "Start demo" home; narration card on every screen; step list down the side | Presenter | Loads the demo house and personas, walks steps 1 to 10, shows a narration card per screen, AI live or replay (labelled). | Ends at the timeline recap and hurdle map |

### Checkpoint catalogue

Kind: **CD** client_decision (blocking), **LM** law_marker (non-blocking), **HR** human_required, **TP** third_party,
**AU** automated. "Law says": **L** licensed broker (or sponsored licensee), **A** attorney. "Planned" = shown on
the timeline, not acted in the demo. Records marked "per item" are written once per message, artifact or side.

| CP | Record | Kind | Who acts in the product | Law says | Why (F-ID; L-ID / WS3) | Step |
|---|---|---|---|---|---|---|
| CP-01 | Seller acknowledges the agency disclosure | CD | Seller | | F9; L12 | 1 |
| CP-02 | AI accepts the listing after a conflicts check | LM | AI | L | F12; L1, L5 | 1 |
| CP-03 | Seller signs the listing agreement (exclusive-listing explanation shown) | CD | Seller | | F13, F7; L9, L14, L34 | 1 |
| CP-04 | Seller completes the PCDS (the software does not help fill it) | CD | Seller | | F15, F59; L43 | 1 |
| CP-05 | Seller chooses the list price | CD | Seller | | F22, F24; L9; WS3-R9 | 2 |
| CP-06 | AI marks advertising "ready to publish" (copy, flyer, posts) | LM | AI | L | F26, F76; L10, L18, L36 | 3 |
| CP-07 | Seller signs the marketing-exposure choice and authorisations | CD | Seller | | F32, F38; L9; WS3-R2, R3 | 4 |
| CP-08 | Listing keyed into OneKey from the AI's package | HR | Licensed MLS participant or registered Administrative User | (L) | F28, F85; L16; WS3-C1 | 4 |
| CP-09 | AI sends a message that discusses the listing, negotiates or advises (per item) | LM | AI | L | F2, F33, F48; L1, L6, L18 | 5 |
| CP-10 | Owner-hosted showing or open house: someone opens the door | HR | Seller (owner) | | F39, F40; L19; WS3-R4 | 5, 8 |
| CP-11 | AI presents every offer and advises the seller | LM | AI | L | F45, F47; L1, L18 | 6 |
| CP-12 | Seller decides: accept, counter or reject | CD | Seller | | F47; L24 | 6 |
| CP-13 | AI negotiates the counter with the other side (per side) | LM | AI | L | F48, F49; L1, L18 | 6, 8 |
| CP-14 | AI drafts the contract of sale and rider | LM | AI | A | F52; L21, L22, L25 | 7 |
| CP-15 | Wet ink / notary items at closing (deed acknowledgment, POA, smoke-detector affidavit) | HR | Notary; the parties | | F67; L35, L45 | 7 |
| CP-16 | Buyer acknowledges the agency form and signs the buyer agreement before tours | CD | Buyer | | F9, F17; L12, L15; WS3-R5 | 8 |
| CP-17 | Seller and buyer consent to dual agency | CD | Seller and buyer | | F11, F51; L13 | 8 |
| CP-18 | Buyer approves the offer (and the reply to a counter) (per item) | CD | Buyer | | F44; L24 | 8 |
| CP-19 | AI publishes the brokerage campaign (simulated) | LM | AI | L | F1, F76; L10, L18, L38, L40 | 10 |
| CP-20 | Deposit into escrow (planned) | TP | Escrow holder (custom: the seller's attorney) | | F55; L25 | 9 |
| CP-21 | Inspection (planned) | TP | Licensed home inspector | | F56, F57 | 9 |
| CP-22 | Mortgage commitment, appraisal, title (planned) | TP | Lender, appraiser, title company | | F60, F61, F62 | 9 |
| CP-23 | Walkthrough and closing; commission paid (planned) | TP | Title company, lender, notary; the parties | | F66, F67, F68; L35 | 9 |
| CP-24 | Notices delivered at first contact: fair-housing, agency form, not-legal-services (per item) | AU | AI | | F8, F10; L39, L12, L29 | 1, 5, 8 |
| CP-25 | AI advises the seller on list price | LM | AI | L | F22; L6, L18; WS3-D5 | 2 |
| CP-26 | Fair-housing check passed (per artifact or message) | AU | AI | | F78, F81; L36, L37, L58, L61 | 3, 5, 10 |
| CP-27 | Seller approves the fact sheet and the AI's authority | CD | Seller | | F33, F84; L9, L18 | 5 |
| CP-28 | AI arranges a self-guided tour | LM | AI | L | F39; L19, L15; WS3-R4 | 5, 8 |
| CP-29 | AI schedules a showing; sends access and feedback requests | AU | AI | | F37, F42; L15; WS3-R4 | 5, 8 |
| CP-30 | AI takes on the buyer as a client and records the agency relationship | LM | AI | L | F11, F12, F51; L1, L5, L13 | 8 |
| CP-31 | AI advises the buyer on offer price and terms and drafts the offer | LM | AI | L | F23, F44; L6, L18, L22 | 8 |
| CP-32 | Accepted-offer memorandum sent; disclosures attached to the contract | AU | AI | | F50, F59; L43, L44, L46, L60 | 7 |
| CP-33 | Seller and buyer sign the contract (simulated e-sign) | CD | Seller and buyer | | F59; L24, L34, L43 | 7 |
| CP-34 | AI negotiates repairs or credits after inspection and writes them into the contract (planned) | LM | AI | L + A | F58, F64; L1, L21 | 9 |
| CP-35 | No licensed broker of record supervises this firm (standing) | LM | AI (the firm) | L | F73, F74, F75; L2, L3, L4, L5 | 9 (and every page footer) |

**Counts by kind:** 11 client decisions, 13 "NY law today" markers (11 licensed broker, 1 attorney, 1 both), 3 human
required, 4 third party, 4 automated: 35 codes. In one demo run the per-item records (CP-09, CP-13, CP-18, CP-24,
CP-26) add more records under the same codes; the timeline header counts both codes and records.

Gates the service layer enforces (each refuses the action and says why): no marketing before CP-03 (L9); no copy
before CP-05; no "ready to publish" with a block finding (section 5); no AI reply before CP-27; no tour before
CP-16 (L15); no offer from the firm's buyer on the firm's listing before CP-17 (L13); no counter outside CP-12's
decision; no contract signing before the PCDS is delivered (CP-04, CP-32; L43). Markers never gate anything.

---

## 4. Data model

SQLAlchemy models; every column carries `info={"source": ...}` or `info={"pii": <category>}`. A field registry
built from that metadata drives the source chips, the masking, the access log and the export.

| Table | Key fields | Notes |
|---|---|---|
| `property` | id, upi (RESO UPI 2.0), address parts, county, municipality, school district, ~40 RESO-named facts (beds, baths, living area, lot, year built, heating, water, sewer, zoning, taxes, assessed value, flood zone, ag district flag, lead-paint flag) | Each fact stored as `property_fact(property_id, field, value, source ∈ {seller, public_record, inferred}, source_ref, confidence, inferred_reason, updated_at)`. No owner name, ever. |
| `person` | id, role (seller, buyer, other-agent, third-party), **PII**: legal name, e-mail, phone, mailing address, pre-approval amount, lender; non-PII: persona label | PII columns Fernet-encrypted; fictional people only (SC). No broker or attorney persons (decision 21). |
| `deal` | id, property_id, side (listing / buyer), status, current step, list price, accepted offer id, brokerage config id | One brokerage, brand in `config/brokerage.yaml` (name, office address, phone, broker-of-record line per decision 25). |
| `client_instructions` | id, deal_id, **side** (seller / buyer), fact sheet (seller), authority (JSON: price floor, terms the AI may concede, showing windows), confidential notes (motivation, maximum price) | Side-scoped: `AgentContext(side)` reads only its own side's rows (decision 24). Set by CP-27 (seller) and the buyer's intake. |
| `offer` | id, deal_id, buyer person_id, price, deposit, financing type, contingencies (JSON), closing date, concessions, status, legend_version, round | Field names borrowed from RESO Offer Management. |
| `checkpoint` | id, deal_id, code (CP-xx), step, **kind** (client_decision / law_marker / human_required / third_party / automated), actor (ai / seller / buyer / third_party / human), law_actor (L / A / L+A / null), side (seller / buyer / both), rule_text, who_text, reason, f_ids, l_ids, ws3_ids, research_link, blocking (bool, true only for client_decision), status (pending / done / declined / simulated / planned), decision, decided_by persona, decided_at, attached_to (entity type and id, e.g. a message) | The timeline, hurdle map and agent-acts log read only this table and the step table. |
| `message` | id, deal_id, thread_id, direction, channel, from/to person ids, side, body_masked, body (PII, encrypted), drafted_by (AI / seller / buyer), disclosures_attached, identity_block_present, fair_housing_result_id, law_marker checkpoint id (nullable), simulated_sent_at | No message reaches "sent (simulated)" without a passing fair-housing result; messages that discuss the listing, negotiate or advise link their CP-09 record. |
| `document` | id, deal_id, kind (listing agreement, buyer agreement, agency form, dual-agency consent, DOS-2156, PCDS, lead paint, memorandum, contract draft, rider, flyer), version, file path, generated_by, needs_wet_ink, needs_notary, signed_by (JSON), seal_hash, label_version | Contract pages carry the label from section 3, step 7. |
| `disclosure` | id, deal_id, person_id, kind (agency L12, fair-housing L39, not-legal-services L29, PCDS L43, lead paint L44, ag district L46, §242 L60), trigger, delivered_at, acknowledged_at, refused_declaration | Shows statutory timing on the timeline. |
| `copy_artifact` + `fair_housing_result` | text, channel, version; findings (rule id, class, span, tier, source rules/model), fixed text, passed | Kept for the discrimination-complaint window (L61). |
| `events` (audit log) | seq, ts, actor, kind (ai_action / client_decision / system), entity, entity_id, summary, prev_hash, hash | Append-only (SQLite triggers forbid UPDATE/DELETE); hash chain. |
| `access_log` | ts, persona, person_id, fields viewed, purpose, route | Written on every render of PII. |
| `model_call` (spend log) | ts, module, task, side, model, input / cache-write / cache-read / output tokens, cost_usd, latency_ms, mode (live / replay / fake), prompt_version, request_hash | Rolled up by `scripts/app-spend.py` into `docs/SPEND-LOG.md`. No prompt or response bodies here. |
| `replay_cache` | request_hash, module, task, response JSON, recorded_at | Inputs are masked before hashing, so it holds no PII. |

**Demo-house data shape** (for the demo-house data job; `seed/demo_house.json`): the `property_fact` rows above
with `source` and `source_ref` (assessor record URL, NYS ORPTS sale record, FEMA panel), plus
`seed/comps.json`: at least 5 arm's-length Dutchess County sales within ~18 months and a few miles, each with
sale date, price, beds, baths, living area, lot, year built, source_ref. Public records only, never a portal
(D18). Personas, enquiries, the seller's authority, the buyer's confidential limits and offers live in
`seed/personas.yaml` (fictional).

---

## 5. Fair-housing pipeline

**Rules file** `app/fairhousing/rules.yaml`, our own text (no authoritative list exists; WS7 G1). Each rule: `id`,
`patterns` (regex, word-boundary, case-insensitive), `class`, `tier` (block / warn), `basis` (L-ID and citation),
`explanation` (plain words), `suggestion` (neutral rewrite). Categories:

- **Federal classes** (42 U.S.C. §3604(c), L36): race, colour, religion, sex, disability, familial status, national
  origin.
- **New York classes** (Executive Law §296(5), L36; 15 classes [INFERENCE from WS2; verify the list against the
  statute text when writing the file]): race, creed, colour, national origin, citizenship or immigration status,
  sex, sexual orientation, gender identity or expression, age, disability, marital status, familial status,
  military status, lawful source of income (L59), status as a victim of domestic violence.
- **Steering** (L37, 19 NYCRR 175.17(b)): school quality claims, neighbourhood composition, "safe"/"crime" talk,
  "exclusive", "family neighbourhood", directing people to areas.
- **NY extras:** source-of-income ("no Section 8", "vouchers not accepted"), blockbusting in seller solicitations
  (L41), disparate effect (L58: rules that sort people need a justification).
- **Warn tier (context-dependent, MLS stricter than HUD's 1995 memo):** "mother-in-law suite", "walking distance",
  "master bedroom", "his and hers", "bachelor pad", "near church" (warn, not block: describing a landmark is
  allowed; preference is not).
- **Ad-targeting rules** (L38) are a separate list applied to the targeting panel (step 10), not to text.

**Pipeline** (`app/fairhousing/check.py`), run on every piece of copy and every outgoing message:

1. **Rules pass** (deterministic, instant): every hit with rule ID, class, span, tier, basis.
2. **Model review pass** (Haiku 5.5, structured output): the rules summary is the cached system prompt; the model
   looks for what regex misses (implied preference, coded language, steering by implication) and returns findings
   in the same schema plus a corrected version that keeps the meaning.
3. **Merge and show**: on screen, side by side: original with highlights, findings list, fixed version. "Apply fix"
   re-runs both passes. Any **block** finding stops the copy or message from being published or sent. This gate is
   the software complying with the law, not a human approval; it is enforced in the service layer.
4. **Publish or send** (CP-06 / CP-19 / CP-09): when no block finding stands, the AI marks the copy "ready to
   publish" or sends the message (simulated), writes the CP-26 pass record and, where the act is one NY law today
   reserves, the red marker record. Warn findings are shown with the AI's choice (kept or rewritten) and its reason.
   Results are stored (L61 retention).

**Fixture set** `tests/fixtures/fair_housing.yaml`: **at least 40 phrases** (target 50), each with `text`, `expected`
(allowed / disallowed / warn), `class`, `rule`. Coverage: every federal and NY class at least once; steering;
source of income; warn-tier terms; and allowed look-alikes that must not be flagged. Examples:

| Phrase | Expected |
|---|---|
| "Perfect for a young family" | disallowed (familial status, age) |
| "Steps from the church" | warn: landmark OK; flag only with preference wording |
| "Ideal for Christian buyers" | disallowed (creed) |
| "No Section 8" | disallowed (lawful source of income) |
| "Great schools, safe neighbourhood" | disallowed (steering) |
| "Adults only, quiet community" | disallowed (familial status) |
| "Not suitable for wheelchairs" | disallowed (disability); allowed rewrite: "three steps to the entrance" |
| "English speakers preferred" | disallowed (national origin) |
| "Perfect bachelor pad" | disallowed (sex, marital status) |
| "Mother-in-law suite" | warn; suggest "accessory apartment" |
| "Three bedrooms, two baths, 1.2-acre lot" | allowed |
| "Near the Metro-North station" | allowed |
| "Family room with fireplace" | allowed (look-alike) |
| "Walk-in closet in the primary bedroom" | allowed |
| "Close to Whaley Lake" | allowed |

**Tests** (`tests/test_fair_housing.py`):
- `test_rules_fixture` (always, no network): every *disallowed* phrase marked `rules_must_catch: true` is caught by
  rules alone; no *allowed* phrase is blocked by rules.
- `test_pipeline_fixture` (replay by default; `--live` re-records, ~$0.02): rules + model catch **100%** of
  disallowed phrases; at most **10%** of allowed phrases flagged (warns count as flags). This is the measurement A8's
  kill criterion needs; the result goes into `docs/ASSUMPTIONS.md`.
- `test_planted_violation_demo`: the demo's planted sentence is caught with the named rule and the fixed version
  passes.
- `test_no_unchecked_send`: no message or artifact reaches "sent (simulated)" or "ready to publish" without a passing
  `fair_housing_result` (now that the AI sends on its own, this test replaces the human gate as the guarantee).

**Result (2026-10-23, BUILD-2).** Rules file `app/fairhousing/rules.yaml`, version `FH-RULES 2026-10-23.1`: 25 rules
(20 block, 5 warn) covering the 7 federal and 15 NY classes, steering, blockbusting and source of income; the NY
class list is the one WS2 records for Executive Law §296(5) (not re-read against the statute text in this job).
Fixture set: **58 phrases** (39 disallowed, of which 36 the rules must catch and 3 coded phrases only the model is
expected to catch; 5 warn; 14 allowed look-alikes). Rules alone: 36/36 caught, 0/14 allowed flagged, 5/5 warns
warn. **Rules + Haiku 5.5 review (live, then replayed): recall 100% (39/39), allowed flagged 0% (0/14).** The
demo's planted sentence is caught (FH-FAM-01 block, FH-REL-02 warn), the AI's fixed version passes, and only then
can it be marked ready. A model pass that does not run (replay miss, spend cap) leaves the gate shut. Caveat: the
set is our own; an outside set (Zillow's FairHome data, Q-WS7-5) is still to come.

---

## 6. PII design

| Principle | How |
|---|---|
| Fictional people only | Seed personas; the real demo house carries no owner name (D18). |
| One database, fields marked | `info={"pii": category}` on columns; registry built at start-up; PII columns Fernet-encrypted (`/srv/realestate/secrets/PII_KEY`). |
| Minimise per step | Intake: seller name and contact only. Pricing, copy, channels, timeline: **no PII at all**. Inbox: sender label and message. Offers: buyer label, price, terms. Contract: names and addresses only in the rendered contract, not in the model call. Buyer: needs and budget, no protected-class questions. |
| Fields sent to the model | Each module declares a `model_context()` whitelist; a test fails if a PII-registry field appears in any request. Names become tokens (`[SELLER_1]`, `[BUYER_2]`), e-mail and phone are regex-masked, and real values are re-inserted only in the rendered output. Contract draft uses tokens; the DOCX fill puts names in after the call. Assume Anthropic keeps API inputs up to 30 days (Q-WS7-4). |
| Information wall between the two AI agents | `AgentContext(side)` reads only that side's `client_instructions`, messages and offers; a test fails if the buyer's confidential limits appear in any seller-side request or the seller's floor in any buyer-side request (decision 24; F51, F84 confidentiality). |
| Access log | Every render of a PII field writes `access_log` (persona, person, fields, purpose, route). A "Who viewed this person" panel on the person page. |
| Export | `GET /people/{id}/export` → JSON of every PII field, messages, documents and access-log rows for that person. |
| Delete | `POST /people/{id}/delete` → PII fields erased and documents redacted; a tombstone keeps non-personal transaction facts with "retained 3 years (L17)"; the erase itself is an audit event. |
| No PII in logs | structlog processor drops registry fields and masks e-mail/phone patterns; the end-to-end test greps the log file for every seeded persona name, e-mail and phone and fails on any hit. |
| Model output | Sanitised with nh3 before HTML or PDF. |

---

## 7. Model use and cost

Prices per million tokens, Anthropic pricing page, read 2026-10-23 [PRIMARY]:

| Model (ID) | Input | 5-min cache write | Cache read | Output |
|---|---|---|---|---|
| Haiku 5.5 (`claude-haiku-5-5`), prompts ≤100k tokens | $0.10 | $0.125 | $0.01 | $0.50 |
| Sonnet 5.5 (`claude-sonnet-5-5`) | $2 | $2.50 | $0.10 | $10 |
| Opus 5.5 (`claude-opus-5-5`) | $4 | $5 | $0.20 | $20 |

**Rule: Haiku 5.5 unless the output is the thing the father-in-law reads closely.** Decision 21 adds reads-closely
outputs (offer advice, both sides' negotiation, the finished contract draft), so those go to Sonnet 5.5. Model per
task is in `config/models.yaml`, so slice 1's side-by-side can move any task up or down without code changes.

| Module / task | Model | Calls per run | Tokens per call (in / out, est.) | Est. cost per run |
|---|---|---|---|---|
| Intake: infer gaps, explain inferences | Haiku 5.5 | 1 | 3k / 1k | $0.001 |
| Pricing: method in plain words, recommended price and reasoning | Sonnet 5.5 | 1 | 4k / 1.5k | $0.023 |
| Listing copy: MLS, portal, 3 social, flyer text | Sonnet 5.5 | 1 | 3k / 2.5k | $0.031 |
| Fair-housing model review (copy, every outgoing message, campaign, re-checks) | Haiku 5.5 | ~14 | 2.5k (cached rules) / 0.6k | $0.005 |
| Inbox: replies within the seller's authority, feedback summary | Haiku 5.5 | ~6 | 2k / 0.5k | $0.003 |
| Offers (seller's AI): present and advise on the offers; counter and negotiation message | Sonnet 5.5 | 2 | 4k / 1.5k | $0.046 |
| Buyer (buyer's AI): intake summary, search explanation | Haiku 5.5 | 2 | 2k / 0.6k | $0.001 |
| Buyer (buyer's AI): offer advice and draft; advice and reply on the counter | Sonnet 5.5 | 2 | 3k / 1k | $0.032 |
| Contract: draft + rider + side-by-side notes | Sonnet 5.5 | 1 | 8k / 8k | $0.096 |
| Business campaign | Sonnet 5.5 | 1 | 2k / 1.5k | $0.019 |
| **Full live demo run** | | **~31** | | **≈ $0.26, call it $0.35 with retries** |

[INFERENCE: token counts are estimates; the `model_call` table replaces them with real numbers in slice 2.]
**Measured in slice 2 (demo house, live):** pricing (Sonnet) 5.5k in / 2.3k out, $0.038; copy (Sonnet) 2.6k in /
3.7k out, $0.046; fair-housing review (Haiku) about 260 in + 3k cached / 400 out, $0.0003 a call. Slice 2's side-by-
side kept Sonnet for pricing and copy (`docs/build/model-side-by-side-slice2.md`).
**Change from the overnight spec:** about $0.26 a run instead of $0.16, because the AI now advises on and negotiates
both sides (three more Sonnet calls) and the contract is the product's finished draft, not a draft for an attorney
(longer output). Not material to the plan: the $15 reserve (D19) still covers ~40 live runs, and the $12 app cap
~34. Fixed prompts (module instructions, the rules summary, the brokerage config) go first in each request with
`cache_control` so repeated calls read them at a tenth of the input price. **Slice 3 tries Opus 5.5 on the contract
side by side with Sonnet 5.5** (the most scrutinised page in front of a lawyer); if it is clearly better it moves
up, adding ~$0.10 a run. Opus is not used elsewhere.

**Spend guard:** the app refuses live calls once its own logged spend passes `SPEND_CAP_USD` (default $12),
and shows the running total in the footer.

**Demo replay mode (rehearsals cost nothing):** `ReplayProvider` answers from `replay_cache` keyed by the masked
request hash. One live run records every response; rehearsals, tests and the meeting (if the room has no internet,
Q-WS7-3) replay them with the same "thinking" animation. A badge always says which: **"AI: live"** or **"AI:
replay of the run recorded <date>"**; never pass a replay off as live. Replay misses fall back to live (if a key and
internet exist) or to a clear "not recorded" card.

---

## 8. Demo mode

- **One source of truth:** `app/demo/steps.yaml`, one entry per screen: step number, title, route, narration
  text (what to say, ~40 to 60 words, including what each red marker on the screen means), what to click, Driver.js
  spotlight selectors, target time.
- **Narration card** (collapsible panel on each screen) and the **step list** down the side both render from
  `steps.yaml`; the active step and finished records are ticked, and each step shows its count of red markers.
- **`docs/DEMO-SCRIPT.md` is generated** from `steps.yaml` by `scripts/gen-demo-script.py`; a test fails if the
  committed file differs from a fresh generation or if any step route has no entry. That is how script and screens
  stay one for one (SC11).
- **"Start demo"** resets the database to the seed, sets the persona to Presenter, chooses replay or live, and opens
  step 1. When a client decision is due, the persona switches automatically with a banner ("Now acting as: the
  seller"), then back to Presenter.
- **Timing, 14 minutes:** intro 0.5; 1 Intake 1.5; 2 Pricing 1.5; 3 Listing copy 2.0; 4 Marketing plan 1.0;
  5 Communications 1.5; 6 Offers 1.5; 7 Contract 1.5; 8 Buyer side 1.5; 9 Timeline and hurdle map 1.0; 10 Business
  0.5. A headless Playwright run measures click-path time; a rehearsal with a human measures talk time.
- Every screen shows the DEMONSTRATION mark (section 0, point 3).

---

## 9. Build order

The build starts **today, Friday 2026-10-23, as soon as this spec is committed** (decision 22: the billing answer was
the only blocker). It runs as headless jobs under `scripts/api-run.sh`, on the API credit while it lasts above the
$15 reserve and then on the Max plan (decision 22). Four vertical slices, each running end to end on hughesnode by
the end of its slot. Acceptance checks name the amended SC item they prove.

| Slot | Slice | Acceptance checks |
|---|---|---|
| **1, Fri 10-23 evening to Sat 10-24** | Try-first checks T1 to T8 (2 h cap). Skeleton: layout, step list, persona switcher (Seller, Buyer, Presenter), data model, record service with the five kinds and `catalogue.yaml`, the three components, events / access / model_call tables, `ModelProvider` (live, replay, fake), `AgentContext(side)`, structlog masking, brokerage config with the CP-35 identity block, demo-house seed. **Step 1 Intake** and a first **Step 9 Timeline** from real records. Dockerfile; switch hughesnode type to docker; review pages still served. | SC1: profile with source chips in under 5 min of clicks; CP-01, CP-03, CP-04 block as client decisions, CP-02 shows its red marker with rule, who, IDs and a working link, CP-24 is recorded; all appear on the timeline in their colours (SC9 seed); catalogue test passes; `make run` works locally; URL loads behind the house login; `/docs-success-criteria.html` still loads. |
| **2, Sun 10-25** | **Step 2 Pricing**, **Step 3 Listing copy** with the full fair-housing pipeline, rules file and 40+ fixtures, flyer PDF; **Step 4 Marketing plan** with connector stubs and "human required" markers. Model side-by-side settles `models.yaml`. | SC2 (≥3 comps, method, range, AI's recommended price with reasoning, CP-25 marker, CP-05 seller chooses and blocks copy until chosen); SC3 (planted violation caught with rule and fix; corrected copy passes; only passing copy is marked "ready to publish", by the AI; CP-06 marker); SC4 (every channel card honest; CP-08 "human required" links to WS3); fixture tests pass, including `test_no_unchecked_send` (SC under the hood). |
| **3, Mon 10-26** | **Step 5 Communications**, **Step 6 Offers**, **Step 7 Contract** (memorandum, draft + rider, DOCX + PDF with page labels, side-by-side, disclosures, signing map, simulated signing), **Step 8 Buyer side**. Opus/Sonnet contract side-by-side. | SC5 (CP-27 before any reply; the AI answers and sends on its own, "sent (simulated)"; only seller decisions reach the seller; disclosures at first contact; firm name on every outgoing message; a showing scheduled, owner-hosted (CP-10) and self-guided (CP-28 marker); feedback logged; CP-09 on each message that discusses the listing, negotiates or advises); SC6 (≥2 offers, AI advises with reasoning, CP-11 marker, seller decides CP-12, AI negotiates the counter CP-13 with the buyer's side, counter outside the decision refused by code); SC7 (draft, rider, side-by-side, PCDS attached, CP-14 marker stating L21 plainly, wet-ink / notary items marked CP-15, no attorney screen or persona anywhere); SC8 (four buyer screens; CP-16 blocks tours; CP-17 consent; AI drafts and negotiates as the buyer's agent, CP-31 marker; CP-18 buyer approves); information-wall test passes. |
| **4, Tue 10-27** | **Step 10 Business marketing**; **Step 11 Demo mode** (steps.yaml, narration cards, Driver.js, generated DEMO-SCRIPT.md); timeline finished with planned records, hurdle map, agent-acts log and header counts; PII export and delete; Playwright headless end-to-end; record the replay run; spend roll-up into `docs/SPEND-LOG.md`; traceability statuses updated. | SC10 (campaign fair-housing-checked, CP-19 marker, targeting panel); SC11 (Start demo walks 1 to 10, script matches screens, 12 to 15 min); SC9 complete (every step coloured AI / client decided / NY law today / third party, from records only; hurdle map lists every marker); PII tests (no PII in logs, model-context whitelist, export, delete); full test suite green. |
| **Wed 10-28** | **Joe clicks through on hughesnode** (afternoon); fixes from his notes the same day where small. | Joe's click-through notes logged in `docs/PROGRESS.md`. |
| **Thu 10-29** | Polish from Joe's notes (D15). | |

**Cut first if late (in this order):** pyHanko seal → Driver.js spotlights (narration cards stay) → Leaflet map
(static image) → flyer as PDF (HTML print view instead) → sqlcipher (Fernet columns stay) → Opus contract trial →
self-guided tour as a scheduler option (its CP-28 marker shown on the scheduler card, not acted) → live mode at the
meeting (replay only) → contract side-by-side reduced to section headings with one-line notes.
**Never cut:** client-decision gates, "NY law today" markers with their reasons and links, the fair-housing checker
and its fixtures, "human required" markers for MLS keying, the timeline built from records, narration cards, the
PII baseline, traceability.

---

## 10. Risks

| Risk | Effect | Handling |
|---|---|---|
| A lawyer (the father-in-law) watches software draft a contract of sale for the parties (L21, L22) | It reads as unauthorised practice of law, in front of the person whose licence the plan relies on | The CP-14 marker states the law plainly, as WS2 does, with the link; the plan's launch path says what would have to change for this to be lawful; every page of the draft is labelled "DEMONSTRATION. Drafted by software ... NY law today: only a lawyer may draft a contract of sale for another"; nothing is ever sent or signed for real |
| The demo is "pitched as autonomous" (K4, L18) | A broker or lawyer in the room reads it as a plan to break the licensing law | It is the brief's idea, shown with every reserved act marked red and counted; the hurdle map is the honest summary; the narration says the markers are today's law, reported, not hidden |
| The AI negotiates beyond the seller's authority | Wrong counter in the demo | Authority stored as structured limits (CP-27); code checks every counter's price and terms against CP-12 and the authority before sending; anything outside goes back to the seller as a decision |
| Information leaks between the seller's AI and the buyer's AI | Breach of the confidentiality an agent owes (F51, F84) | `AgentContext(side)`; side-scoped tables; information-wall test |
| Fair-housing checker misses a phrase in the live demo, now that the AI publishes and sends without a human | Embarrassing in front of a broker; A8 kill criterion | Rules + model; 100% recall on the fixture set; planted violations are fixtures; `test_no_unchecked_send`; replay mode makes the demo deterministic |
| Demo-house data incomplete (no comps from public records in time) | SC2 weak | Comps job runs before slice 2; fallback: clearly labelled illustrative comps, flagged on screen and in the script |
| Real address mistaken for a listing (L9, L10) | Owner complaint; advertising rule | DEMONSTRATION mark everywhere; nothing sent; no owner name; no portal photos |
| WeasyPrint/Pango in the image | No PDFs | T1 in slice 1; ReportLab / HTML print fallback |
| hughesnode type switch breaks the review pages | Joe loses his document links, and markers link to them | Mount `public/` in the app; check `/docs-*.html` as a slice-1 acceptance test; keep the static type until the container passes |
| No internet in the meeting room (Q-WS7-3) | Live calls and map fail | Replay mode default for the meeting; static map fallback; app runs locally on the laptop with one command |
| Spend overrun | Eats the $15 reserve | Haiku default; caching; app spend cap $12; replay for rehearsals and tests |
| Five slots for 11 screens and more AI acts | Missed click-through | Vertical slices; cut list above; Joe sees partial slices daily on hughesnode |
| Model output with unsafe HTML or prompt-injection text from simulated enquiries | Broken pages, wrong replies sent by the AI | nh3 sanitising; enquiries are fixed seed text; the AI replies only from the fact sheet and authority; fair-housing check on every message; nothing is really sent |
| PII leaks into logs or prompts | Breaks SC PII baseline | Registry-driven masking; whitelist test; log grep test |
| Model IDs or prices change | Cost or breakage | IDs and prices in config; `model_call` logs real cost |
| Disk on the VPS | Build stalls | `scripts/disk-check.sh` before the image build; image under 600 MB |
| Pending laws (L20 public marketing; L42 AI disparate-impact audits; L62 AI notices) | Rules shift | Shown as "pending" notes on the relevant screens; rules file versioned |

---

## 11. Decisions for Joe

1. **Step 7 framing: answered by decision 21.** The software drafts the contract for the parties in the product's
   own contract step, with the "NY law today" marker (L21, L22, L25). No attorney workspace.
2. **Who pays for the build: answered by decision 22.** API credit first (above the $15 reserve), then the Max plan.
   The demo's own calls stay on the key, inside the $15 reserve.
3. **Live or replay at the meeting.** Provisional: replay by default (recorded the day before, labelled), with a
   live switch if the room has good internet.
4. **Contract structure** (Q-WS7-2): provisional bar-association long-form section structure, own wording.
5. **Attorney-approval wording on offers and the contract** (decision 26). Provisional: offers carry only "not
   binding until a formal contract is signed by both" (L24); the contract draft has **no** attorney-approval
   contingency, because the idea is no lawyer in the loop; its labels state the law (L21, L22) and it never says a
   lawyer is unnecessary (L23). Alternative: add the customary attorney-approval clause, which puts lawyers back in
   by contract.
6. **Who the identity block names as broker of record** (decision 25). Provisional: the firm's name, office and phone,
   plus "Licensed broker of record: required by NY law; none in this demonstration" with the CP-35 marker, rather
   than inventing a licensed person. Alternative: a placeholder for the father-in-law's name (only with his consent).
