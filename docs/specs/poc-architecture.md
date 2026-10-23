# POC architecture spec

**Status:** written 2026-10-23 (headless job), after Joe signed off `docs/SUCCESS-CRITERIA.md` and WS1 to WS3
landed. This is the document the build (2026-10-25 to 10-28) works from. Traceability is in `docs/TRACEABILITY.md`.

**Sources used:** `docs/SUCCESS-CRITERIA.md` (SC), `docs/OUT-OF-SCOPE.md`, `docs/DECISIONS.md` (D5 to D8, D13 to
D19), `docs/research/WS1-agent-functions.md` (F1 to F89), `docs/research/WS2-legal-licensing.md` (L1 to L62,
sections 2, 10 and 11), `docs/research/WS3-listing-data-access.md` ("What the proof of concept automates, stubs
and skips"), `docs/research/handoff/WS1.md`, `WS2.md`, `WS3.md` (traceability items, WS3-C/D/R IDs), `WS7.md`
(the "What already exists" table). `docs/specs/demo-house.md` does not exist yet; section 4 defines the shape the
demo-house data must take. Model prices are from Anthropic's pricing page, read 2026-10-23 [PRIMARY].

---

## 0. Three things that changed the design (read first)

1. **Step 7 cannot be "the brokerage's AI drafts the contract" as worded.** WS2 section 2: only lawyers may draft
   or be paid to prepare instruments affecting real estate, and a company may not render legal services at all
   (L21, Judiciary Law §§478, 484, 495); a broker may only fill non-legal facts into a fill-in form marked subject to
   each party's attorney's approval (L22, AG Op. 96-F11); and in the Hudson Valley the seller's attorney drafts
   (L25) [PRIMARY / SECONDARY via WS2]. The success criterion stays, but the screen is reframed: **the brokerage side
   produces only the accepted-offer memorandum (lawful fill-in, L22); the contract draft is produced in an
   "attorney workspace", a screen used by the seller's attorney persona, as that attorney's drafting tool**, labelled
   "Draft prepared for and at the direction of the seller's attorney. Not legal advice. The brokerage does not draft
   or charge for contracts." The attorney review checkpoint (CP-14) closes it. This is the honest version of SC7 and
   it is also the product's real pitch: a faster lawyer step, not no lawyer (WS2 A3 hit). **Joe decision 1** (section 11).
2. **The demo house is a real address (146 Rt 292, Holmes, NY 12531, D18), so every piece of listing copy must
   carry a "DEMONSTRATION: not a listing, not for sale through this firm, no owner authority" mark.** Marketing a
   property without the owner's written authority is itself a rule (L9) and the copy names a broker (L10). The
   flyer, social posts and portal text are watermarked in the HTML and the PDF; nothing is ever sent. No owner
   name is stored; no portal photos or copy are used (CLAUDE.md research rules; WS3-R8).
3. **WS3 found no listing-input API for OneKey MLS or any portal.** So the MLS step is a visible "licensed human
   required" checkpoint with a complete, rule-checked listing package prepared for the person who keys it in
   (WS3-C1), and portals are shown as fed from the MLS (WS3-C4, C8 to C10, C12). This is the demo's strongest
   hand-off moment, not a gap to hide.

---

## 1. What already exists

Checked 2026-10-23 by WS7 (licences and versions from the publishers' pages or registries; detail in the WS7
notes, sections G1 to G14). Decision column: what the POC does with each.

| Candidate | Building block | Licence / cost | Decision | Why |
|---|---|---|---|---|
| FastAPI 0.161.1 + Jinja2 3.1.6 + uvicorn 0.54.0 | Web app, server-rendered screens | MIT / BSD; free | **Adopt** | Decision 7; current; each step is a plain page that shows its own AI work |
| htmx 2.0.11 (+ jinja2-fragments 1.12.0) | Partial updates without a JS build | 0BSD / MIT; free | **Adopt** (vendored file) | No build step; 4.0 is not `latest` until 2027 |
| Bulma 1.0.4 | CSS | MIT; free | **Adopt** | CSS-only, maintained (Pico is unmaintained); step list and timeline are ~50 lines of our own CSS |
| Anthropic Python SDK 2.1.0 (structured outputs, `messages.parse`) | Every AI step | Apache-2.0; per token | **Adopt** | One schema-checked call per AI step, logged as a visible AI action |
| Claude Agent SDK 0.2.173 | Agent loop with tool approvals | MIT file, Anthropic terms | **Borrow ideas** (`can_use_tool`, deny hooks) | ~130 MB, built for coding agents; the POC needs single calls; an autonomous loop invites K4 |
| PydanticAI 2.60.0 / LangGraph 1.2.16 | Human-in-the-loop frameworks | MIT; free | **Borrow ideas** (deferred tools, interrupt and resume) | Approval must be enforced server-side anyway; extra layer between screen and call |
| python-statemachine 3.2.2 (or transitions 0.9.3) | Deal states and checkpoint guards | MIT; free | **Try first**, provisional hand-roll | Checkpoint records already drive the timeline; adopt only if the day-1 try saves code |
| SpiffWorkflow 3.2.0 | BPMN engine | LGPLv3 | **Skip** | Far more machinery than 11 steps need |
| HumanLayer | Approval service | n/a | **Skip** | Pivoted to a coding IDE |
| ArkansasONE MLS list (Mar 2026), OneKey list, NYC CCHR examples, DOS-2156, HUD 1995 memo | Fair-housing rule content | Publishers' copyright; free to read | **Borrow ideas**; write our own rules | No authoritative list exists (HUD 2024 guidance withdrawn effective 2025-09-17); lists conflict |
| Zillow fair-housing-guardrail + FairHome dataset | Classifier and test data | OpenRAIL-S; data by request | **Borrow ideas** (stop list + classifier + prompt) | PyTorch-scale; an API model does the review; dataset request deferred (Q-WS7-5) |
| FairProp-AI, debary-mcp-compliance, real-estate-pack | Community checkers | MIT / Apache | **Skip** | 0 to 11 stars, unverified |
| docxtpl 0.20.2 (python-docx 1.2.0) | Attorney-editable DOCX draft | LGPL-2.1 (MIT); free | **Adopt** | Attorneys edit Word; used unmodified as a library |
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
| Append-only `events` table with hash chain (sqlite-chronicle pattern) | Audit, access and AI-action log | Pattern; free | **Adopt pattern, build ours** | One record family shows every AI action and every human decision |
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
| promptfoo / inspect-ai / deepeval | LLM eval harness | MIT / Apache | **Skip** | pytest covers the 30+ fixtures |
| EspoCRM / Krayin / Twenty | Whole-product baseline | AGPL / MIT | **Skip** | Generic CRM screens hide the AI / human / licensed split, which *is* the demo |
| AleksNeStu/ai-real-estate-assistant | Reference AI real estate app | MIT | **Borrow ideas** (simulated-response demo mode) | Too large to adopt; confirms the replay idea |
| Ocusell List (OneKey) | MLS entry with AI remarks and rule checks | Proprietary, free to members | **Production path** for the human MLS entry | Not an API; shown as the tool behind CP-08 |

**Could one of them be our baseline?** No single product is. The candidates that come closest (a CRM, docassemble,
Chatwoot) each hide the one thing the demo exists to show, the line between AI work, human decisions and licensed
acts, and each is heavier than the VPS allows. So we adopt libraries, not a product, and build only what is ours:
the checkpoint model, the fair-housing rules, the NY-specific flow and the screens.

**Tried on a real example before committing (day 1, morning, time-boxed to 2 hours total):**

| # | Try | Pass condition | If it fails |
|---|---|---|---|
| T1 | WeasyPrint 70.0 inside the Docker image (Debian Pango) | 10-page contract HTML renders to PDF under 5 s | ReportLab for the flyer; contract as DOCX + HTML print view |
| T2 | sqlcipher3 0.6.4 with SQLAlchemy | create, encrypt, reopen | Plain SQLite + Fernet-encrypted PII columns (planned anyway) |
| T3 | python-statemachine on the deal lifecycle | fewer lines and clearer guards than ~80 lines hand-rolled | Hand-roll (provisional default) |
| T4 | Driver.js tour across two HTMX swaps | spotlight survives the swap | Narration cards only |
| T5 | FEMA NFHL point query + Census geocoder on 146 Rt 292 | returns zone and county | Use the stored fixture; connector stays a stub |
| T6 | Regex masker on a sample buyer message, model call, re-insert | names, e-mail, phone never reach the request body | Drop free-text from the model context |
| T7 | Leaflet + OSM + static fallback | map renders; fallback image shows offline | Static image only |
| T8 | pyHanko seal on a generated PDF | a reader flags an edit | Cut (first item on the cut list) |

---

## 2. Stack, locked

**Decision 7 is confirmed, with additions.** Nothing in WS1 to WS3 changed the shape of the product: it is a
sequence of screens, each ending at a human or licensed checkpoint, over one small database, with single model
calls rather than an autonomous agent. That shape is exactly what server-rendered Python does well.

| Layer | Choice | Reason from the research |
|---|---|---|
| Language | Python 3.12 (already on the VPS with `uv`) | WS7: ~200 MB of permissive packages; A11 dodged |
| Web | FastAPI + Jinja2 + htmx (vendored), Bulma CSS, no JS build | Each SC step is its own visible screen; htmx shows "AI thinking → draft → button" without a SPA |
| Data | SQLite (one file) via SQLAlchemy 2.0 ORM; Fernet on PII columns; sqlcipher3 if T2 passes; no migrations tool (the POC rebuilds from seed) | One database for all PII (SC "PII"); fits 8 GB RAM and the disk |
| Model | Anthropic Python SDK behind a `ModelProvider` interface; structured outputs (Pydantic schemas) | SC "swapping the model provider changes no screen" |
| Documents | WeasyPrint (PDF), docxtpl (DOCX for attorneys), pypdf | WS7 table; attorneys work in Word |
| Logs | structlog with a PII-masking processor; own append-only `events` table | SC "PII kept out of application logs"; one record family for audit |
| Sanitising | nh3 on every model output before HTML or PDF | Model output is untrusted |
| Demo | Driver.js (vendored), Leaflet (vendored) | Only MIT tour library; offline fallback for the map |
| Tests | pytest + Playwright headless shell | SC "fast test suite including an end-to-end demo run" |
| Not used | Node toolchain, React, Postgres, Redis, agent frameworks, vector stores | Disk, build complexity, K4 risk; WS3-D6 forbids persistent embeddings of MLS data anyway |

**Deployment.** One Docker image (`python:3.12-slim` + Pango/HarfBuzz for WeasyPrint, ~450 MB estimated
[INFERENCE]), one container, uvicorn with 2 workers (2 vCPU). hughesnode project `realestate` changes type from
`static` to `docker` (D13); the house login stays in front at the Traefik gate, so the app adds no login of its own
and accepts whatever the gate passes (CLAUDE.md house-password rule). Inside the app, a **persona switcher**
(Seller, Buyer, Broker, Seller's attorney) decides which checkpoint buttons are enabled; the check is server-side,
so a seller persona cannot approve an advertisement even by crafting a request.

- Volumes: `/srv/realestate/data` (SQLite file, replay cache, generated PDFs), `/srv/realestate/secrets` read-only
  (`ANTHROPIC_API_KEY`, `PII_KEY`), and the review pages directory read-only.
- **Review pages kept at the same address.** `scripts/publish-review.sh` writes to
  `/srv/hughesnode/apps/realestate/public`. The app serves the POC at `/` (step list home with a "Review documents"
  link) and mounts that directory as static files so existing links such as `/docs-success-criteria.html` keep
  working. Day 1 checks with `hn help` how a docker-type project lays out its directory; if `public/` moves,
  `OUT=` in `publish-review.sh` is updated in the same commit.
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
| `PublicRecordConnector` | `FixtureRecords` (demo-house JSON, comps JSON) | Open NY assessment rolls, NYS parcels, FEMA |
| `MLSConnector.submit(listing)` | `StubMLS` returns `HumanRequired(reason, f_ids, l_ids, link)` | only if OneKey ever offers an input API |
| `PortalConnector.status(listing)` | `SimulatedPortals` ("fed from OneKey in about 24 to 48 h") | none needed: portals syndicate from MLS |
| `IDXConnector.search(criteria)` | `FictionalListings` (live query per session, no stored embeddings, WS3-D6) | MLS Grid IDX after licence and AI addendum |
| `MessageTransport.send(msg)` | `Outbox` (marks "sent (simulated)") | e-mail/SMS provider with consent checks (L50 to L52) |
| `SignatureProvider.sign(doc, party)` | `SimulatedSign` (+ pyHanko seal if T8 passes) | TransactionDesk/AuthentiSign or DocuSeal |

Every stub that stands where a human or licence is required renders the same component: **"Human required here:
<reason>"** with the F-ID, L-ID and a link to the research finding on the review site (for example
`https://realestate.hughesnode.com/docs-research-ws3-listing-data-access.html`).

### Step-by-step map

AI = what the screen shows the model doing. CP = the checkpoint record that ends the step (catalogue below).

| SC # | Module | Screens | What the AI does on screen | Checkpoint(s) that end it |
|---|---|---|---|---|
| 1 Intake | `intake` | Address + facts form ("Use demo house" button); Property profile; Disclosure checklist; Seller onboarding | Parses the address; pulls fixture public-record facts; fills gaps it can infer (e.g. "likely septic: no municipal sewer on this road" → tagged *inferred*, with reason); every field shows a source chip: Seller / Public record / Inferred. Builds the disclosure checklist (PCDS, lead paint if built before 1978, agricultural district, four RPL §242 questions). Sends the fair-housing notice, agency form and "not legal services" notice automatically (logged). | CP-01 seller acknowledges agency form (F9, L12); CP-24 fair-housing notice delivered (F8, L39, automated); CP-02 broker accepts the listing (F12, L1, L5); CP-03 listing agreement signed (F13, L9, L14); CP-04 seller completes the PCDS themselves (F15, L43) |
| 2 Pricing | `pricing` | Comparable sales table; Adjustments; Suggested range; Net sheet | Code computes adjustments (size, lot, age, condition, date) from ≥3 Dutchess comps; the model writes the method in plain words and flags weak comps. Labelled "Comparative market analysis, not an appraisal". | CP-05 broker reviews valuation and advises; seller chooses list price (F21, F22, L1; WS3-D5) |
| 3 Listing copy | `copy` + `fairhousing` | Drafts (MLS remarks, portal description, 3 social posts, flyer); Fair-housing check panel; MLS rule pre-check; Approval | Writes all copy from the profile; checker runs visibly: rule hits highlighted with rule ID, class, legal basis and a fixed version; "Plant a violation" demo button inserts "perfect for a young family, steps from the church" and shows it caught; re-check passes. MLS pre-check: required fields, no compensation in remarks, not "free" (WS3-R6, R7). | CP-06 broker approves advertising before "ready to publish" (F26, F76, L10, L36) |
| 4 Marketing plan | `channels` | Channel board | Fills each card's status from the connectors: OneKey MLS **licensed human required** (with the prepared package); Zillow / Realtor.com / Redfin / Homes.com / OneKeyMLS.com "fed from the MLS"; firm website held by the Clear Cooperation clock; social "drafted and scheduled"; Google Business Profile draft; photos, sign, lockbox "vendor booking"; open house "licensee hosts". Each marker links to its research finding. | CP-07 seller signs marketing-exposure choice (F32, WS3-R2); CP-08 licensee keys listing into OneKey, broker approves (F28, L16, WS3-C1) |
| 5 Communications | `inbox` | Shared inbox; Thread; Showing scheduler; Feedback log; Outbox | Simulated enquiries arrive; the model drafts replies from the approved fact sheet only; escalates price, terms, legal and school/neighbourhood questions with the reason (L23, L37); attaches agency form and fair-housing notice at first substantive contact; stamps the broker identity block; books a showing within 24 h (WS3-R4) after checking the buyer agreement; summarises feedback. | CP-09 approve / edit / send on every outgoing message (F2, F33, F75, L5, L10, L18); CP-10 showing: licensee or owner opens the door (F39, L19) |
| 6 Offers | `offers` | Offer comparison table; Net sheets; Counter draft; Seller decision | Code builds the comparison and net sheets; the model drafts a counter with reasoning (price, contingencies, dates, risk), presented as a draft for the broker to advise on. The AI never accepts or rejects. Offer papers are fill-ins carrying "subject to each party's attorney's approval; not binding until a formal contract is signed" (L22, L24). | CP-11 broker presents every offer and advises (F45, F47, L1); CP-12 **seller decides** (F47, L24); CP-13 broker sends the approved counter (F48, F49, L18) |
| 7 Contract | `contract` | Accepted-offer memorandum (brokerage); Attorney workspace (seller's attorney persona): draft contract + rider, side-by-side with the standard form's structure, attached PCDS and disclosures; Signing map | Brokerage side: memorandum sent to both attorneys (F50). Attorney workspace: the model drafts a NY-style contract and rider pre-filled from intake and the accepted offer, at the attorney's request; side-by-side lists the bar-association long form's section headings against the draft's; disclosures attached (PCDS, lead paint, ag district, §242 notices). Items needing wet ink or a notary are marked (deed acknowledgment, POA; L35), and the smoke-detector affidavit at conveyance (L45). | CP-14 attorney review (F52, F53, L21, L22, L25); CP-15 wet-ink / notary items flagged for closing (L35) |
| 8 Buyer side | `buyer` | Buyer intake + representation disclosure; Search alerts; Tour request; Offer draft + approval | Guided intake (needs, budget, pre-approval status, no protected-class questions); agency form and fair-housing notice sent; search over fictional listings with no steering filters (L37) and alerts; tour request blocked until the buyer agreement is signed (L15); model drafts the offer from the buyer's answers (fill-in, L22). Because the buyer wants the firm's own listing, the dual-agency consent screen appears. | CP-16 buyer agency disclosure + buyer agreement before any tour (F9, F17, L12, L15); CP-17 agency relationship / dual-agency consent (F11, F51, L13); CP-18 **buyer approves the offer** (F44, L24); then CP-11 on the seller side |
| 9 Deal timeline | `timeline` | Deal dashboard; Human-in-the-loop map; Supervision log | No model call. Built only from checkpoint records and the deal's step table: each row coloured **AI** (blue), **Human** (amber), **Licensed or attorney** (red), with status, who acted, when and the reason. Future steps (deposit escrow, inspection, mortgage, appraisal, title, walkthrough, closing) are planned checkpoints with third parties named. Supervision log lists every broker approval (F75). | Display step; shows CP-20 to CP-23 as planned |
| 10 Marketing the business | `brand` | Campaign drafts (landing page, one local ad, one seller lead magnet); Fair-housing panel; Targeting panel | Drafts the brokerage's own campaign naming the broker and the founder (F1, F4); same fair-housing pipeline; targeting panel shows only allowed criteria (no age, family, ZIP or lookalike targeting, L38); AI-use and fair-housing notices on the landing page (L40, L55); no deceptive AI claims (L54). | CP-19 broker approves the campaign (F1, F76, L10) |
| 11 Demo mode | `demo` | "Start demo" home; narration card on every screen; step list down the side | Loads the demo house and personas, walks steps 1 to 10, shows a narration card per screen, AI live or replay (labelled). | Ends at the timeline recap |

### Checkpoint catalogue

Who: **L** = licensed broker (or sponsored licensee), **A** = attorney, **H** = seller or buyer, **T** = third party,
**AI** = automated and logged. "Planned" = shown on the timeline but not acted in the demo.

| CP | Checkpoint | Who | Why (F-ID; L-ID) | Step |
|---|---|---|---|---|
| CP-01 | Seller acknowledges agency disclosure | H | F9; L12 | 1 |
| CP-02 | Broker accepts the listing after a conflicts check | L | F12; L1, L5 | 1 |
| CP-03 | Listing agreement signed (seller and broker), exclusive-listing explanation shown | H + L | F13; L9, L14, L34 | 1 |
| CP-04 | Seller completes the PCDS (the software does not help fill it) | H | F15, F59; L43 | 1 |
| CP-05 | Broker reviews the valuation; seller picks the list price | L + H | F21, F22; L1, WS3-D5 | 2 |
| CP-06 | Broker approves advertising (copy, flyer, posts) | L | F26, F76; L10, L36 | 3 |
| CP-07 | Seller signs the marketing-exposure choice | H | F32; L9, WS3-R2 | 4 |
| CP-08 | Licensee keys the listing into OneKey; broker approves | L | F28; L16, L1, WS3-C1 | 4 |
| CP-09 | Approve / edit / send each outgoing message | L | F2, F33, F75; L5, L10, L18 | 5 |
| CP-10 | Showing: licensee or owner opens the door | L or H | F39; L19, WS3-R4 | 5, 8 |
| CP-11 | Broker presents every offer and advises | L | F45, F47; L1 | 6 |
| CP-12 | Seller decides: accept, counter or reject | H | F47; L24 | 6 |
| CP-13 | Broker sends the approved counter | L | F48, F49; L1, L18 | 6 |
| CP-14 | Seller's attorney drafts and reviews the contract | A | F52, F53; L21, L22, L25 | 7 |
| CP-15 | Wet ink / notary items at closing | A + notary | L35, L45 | 7 |
| CP-16 | Buyer agency disclosure and buyer agreement before tours | H + L | F9, F17; L12, L15 | 8 |
| CP-17 | Agency relationship recorded; dual-agency consent | L + H | F11, F51; L13 | 8 |
| CP-18 | Buyer approves the offer | H | F44; L24 | 8 |
| CP-19 | Broker approves the brokerage campaign | L | F1, F76; L10, L38, L40 | 10 |
| CP-20 | Deposit into seller's attorney's escrow (planned) | A | F55; L25 | 9 |
| CP-21 | Inspection, then repair negotiation (planned) | T + L | F56, F57, F58 | 9 |
| CP-22 | Mortgage commitment, appraisal, title (planned) | T | F60, F61, F62 | 9 |
| CP-23 | Closing and commission (planned) | A + T | F67, F68; L35 | 9 |
| CP-24 | Fair-housing notice delivered at first contact (automated) | AI | F8; L39 | 1, 5, 8 |

A checkpoint cannot be skipped: the service layer refuses the next step's action until the blocking checkpoint
has a decision (e.g. no tour booking before CP-16, no "ready to publish" before CP-06).

---

## 4. Data model

SQLAlchemy models; every column carries `info={"source": ...}` or `info={"pii": <category>}`. A field registry
built from that metadata drives the source chips, the masking, the access log and the export.

| Table | Key fields | Notes |
|---|---|---|
| `property` | id, upi (RESO UPI 2.0), address parts, county, municipality, school district, ~40 RESO-named facts (beds, baths, living area, lot, year built, heating, water, sewer, zoning, taxes, assessed value, flood zone, ag district flag, lead-paint flag) | Each fact stored as `property_fact(property_id, field, value, source ∈ {seller, public_record, inferred}, source_ref, confidence, inferred_reason, updated_at)`. No owner name, ever. |
| `person` | id, role (seller, buyer, broker, attorney, other-agent), **PII**: legal name, e-mail, phone, mailing address, pre-approval amount, lender; non-PII: persona label | PII columns Fernet-encrypted; fictional people only (SC). |
| `deal` | id, property_id, side (listing / buyer), status, current step, list price, accepted offer id, brokerage config id | One brokerage, brand in `config/brokerage.yaml` (name, licence no., office address, broker name). |
| `offer` | id, deal_id, buyer person_id, price, deposit, financing type, contingencies (JSON), closing date, concessions, status, legend_version | Field names borrowed from RESO Offer Management. |
| `checkpoint` | id, deal_id, code (CP-xx), step, actor_role, actor_class (AI / human / licensed / attorney / third party), reason text, f_ids, l_ids, research_link, status (pending / done / declined / planned), decision, decided_by persona, decided_at, blocking (bool) | The timeline and human-in-the-loop map read only this table. |
| `message` | id, deal_id, thread_id, direction, channel, from/to person ids, body_masked, body (PII, encrypted), drafted_by (AI / human), disclosures_attached, broker_block_present, fair_housing_result_id, approval checkpoint id, simulated_sent_at | No message reaches "sent (simulated)" without its CP-09 decision. |
| `document` | id, deal_id, kind (listing agreement, agency form, DOS-2156, PCDS, lead paint, memorandum, contract draft, rider, flyer), version, file path, generated_by, needs_wet_ink, needs_notary, signed_by (JSON), seal_hash | |
| `disclosure` | id, deal_id, person_id, kind (agency L12, fair-housing L39, not-legal-services L29, PCDS L43, lead paint L44, ag district L46, §242 L60), trigger, delivered_at, acknowledged_at, refused_declaration | Shows statutory timing on the timeline. |
| `copy_artifact` + `fair_housing_result` | text, channel, version; findings (rule id, class, span, tier, source rules/model), fixed text, passed | Kept for the discrimination-complaint window (L61). |
| `events` (audit log) | seq, ts, actor, kind (ai_action / human_decision / system), entity, entity_id, summary, prev_hash, hash | Append-only (SQLite triggers forbid UPDATE/DELETE); hash chain. |
| `access_log` | ts, persona, person_id, fields viewed, purpose, route | Written on every render of PII. |
| `model_call` (spend log) | ts, module, task, model, input / cache-write / cache-read / output tokens, cost_usd, latency_ms, mode (live / replay / fake), prompt_version, request_hash | Rolled up by `scripts/app-spend.py` into `docs/SPEND-LOG.md`. No prompt or response bodies here. |
| `replay_cache` | request_hash, module, task, response JSON, recorded_at | Inputs are masked before hashing, so it holds no PII. |

**Demo-house data shape** (for the demo-house data job; `seed/demo_house.json`): the `property_fact` rows above
with `source` and `source_ref` (assessor record URL, NYS ORPTS sale record, FEMA panel), plus
`seed/comps.json`: at least 5 arm's-length Dutchess County sales within ~18 months and a few miles, each with
sale date, price, beds, baths, living area, lot, year built, source_ref. Public records only, never a portal
(D18). Personas, enquiries and offers live in `seed/personas.yaml` (fictional).

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
   re-runs both passes. Any **block** finding stops the copy from reaching the approval gate.
4. **Broker approval gate** (CP-06 / CP-19 / CP-09): the broker sees the clean copy, the check result and the
   history; approves, edits (re-check runs) or rejects. Results are stored (L61 retention).

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

---

## 6. PII design

| Principle | How |
|---|---|
| Fictional people only | Seed personas; the real demo house carries no owner name (D18). |
| One database, fields marked | `info={"pii": category}` on columns; registry built at start-up; PII columns Fernet-encrypted (`/srv/realestate/secrets/PII_KEY`). |
| Minimise per step | Intake: seller name and contact only. Pricing, copy, channels, timeline: **no PII at all**. Inbox: sender label and message. Offers: buyer label, price, terms. Contract: names and addresses only in the attorney workspace render, not in the model call. Buyer: needs and budget, no protected-class questions. |
| Fields sent to the model | Each module declares a `model_context()` whitelist; a test fails if a PII-registry field appears in any request. Names become tokens (`[SELLER_1]`, `[BUYER_2]`), e-mail and phone are regex-masked, and real values are re-inserted only in the rendered output. Contract draft uses tokens; the DOCX fill puts names in after the call. Assume Anthropic keeps API inputs up to 30 days (Q-WS7-4). |
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

**Rule: Haiku 5.5 unless the output is the thing the father-in-law reads closely.** Model per module is in
`config/models.yaml`, so a day-1 side-by-side can move any task up or down without code changes.

| Module / task | Model | Calls per run | Tokens per call (in / out, est.) | Est. cost per run |
|---|---|---|---|---|
| Intake: infer gaps, explain inferences | Haiku 5.5 | 1 | 3k / 1k | $0.001 |
| Pricing: method in plain words | Sonnet 5.5 | 1 | 4k / 1.5k | $0.023 |
| Listing copy: MLS, portal, 3 social, flyer text | Sonnet 5.5 | 1 | 3k / 2.5k | $0.031 |
| Fair-housing model review (copy, messages, campaign, re-checks) | Haiku 5.5 | ~10 | 2.5k (cached rules) / 0.6k | $0.005 |
| Inbox: reply drafts, feedback summary | Haiku 5.5 | ~5 | 2k / 0.5k | $0.002 |
| Offers: counter draft and reasoning | Sonnet 5.5 | 1 | 3k / 1k | $0.016 |
| Contract: draft + rider (attorney workspace) | Sonnet 5.5 | 1 | 6k / 5k | $0.062 |
| Buyer: intake summary, search explanation, offer fill | Haiku 5.5 | 3 | 2k / 0.6k | $0.002 |
| Business campaign | Sonnet 5.5 | 1 | 2k / 1.5k | $0.019 |
| **Full live demo run** | | **~24** | | **≈ $0.16, call it $0.25 with retries** |

[INFERENCE: token counts are estimates; the `model_call` table replaces them with real numbers on day 2.]
The $15 reserve (D19) covers ~60 live runs. Fixed prompts (module instructions, the rules summary, the brokerage
config) go first in each request with `cache_control` so repeated calls read them at a tenth of the input price.
Opus 5.5 is not used; switching listing copy to it would roughly double that line (~$0.06).

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
  text (what to say, ~40 to 60 words), what to click, Driver.js spotlight selectors, target time.
- **Narration card** (collapsible panel on each screen) and the **step list** down the side both render from
  `steps.yaml`; the active step and finished checkpoints are ticked.
- **`docs/DEMO-SCRIPT.md` is generated** from `steps.yaml` by `scripts/gen-demo-script.py`; a test fails if the
  committed file differs from a fresh generation or if any step route has no entry. That is how script and screens
  stay one for one (SC11).
- **"Start demo"** resets the database to the seed, sets the persona to Seller, chooses replay or live, and opens
  step 1. Persona switches happen automatically when a checkpoint belongs to another role, with a banner ("Now
  acting as: the broker").
- **Timing, 14 minutes:** intro 0.5; 1 Intake 1.5; 2 Pricing 1.5; 3 Listing copy 2.0; 4 Marketing plan 1.0;
  5 Communications 1.5; 6 Offers 1.5; 7 Contract 1.5; 8 Buyer side 1.5; 9 Timeline 1.0; 10 Business 0.5. A headless
  Playwright run measures click-path time; a rehearsal with a human measures talk time.
- Every screen shows the DEMONSTRATION mark (section 0, point 2).

---

## 9. Build order

Four build days, each a vertical slice that runs end to end on hughesnode by the evening. Acceptance checks name
the SC item they prove. Billing for the build itself is Joe's call (D19; **Joe decision 2**).

| Day | Slice | Acceptance checks |
|---|---|---|
| **1, Sun 10-25** | Try-first checks T1 to T8 (2 h cap). Skeleton: layout, step list, persona switcher, data model, checkpoint service, events / access / model_call tables, `ModelProvider` (live, replay, fake), structlog masking, brokerage config, demo-house seed. **Step 1 Intake** and a first **Step 9 Timeline** from real checkpoint records. Dockerfile; switch hughesnode type to docker; review pages still served. | SC1: profile with source chips in under 5 min of clicks; CP-01 to CP-04 and CP-24 exist as records and appear on the timeline (SC9 seed); `make run` works locally; URL loads behind the house login; `/docs-success-criteria.html` still loads. |
| **2, Mon 10-26** | **Step 2 Pricing**, **Step 3 Listing copy** with the full fair-housing pipeline, rules file and 40+ fixtures, flyer PDF; **Step 4 Marketing plan** with connector stubs and "human required" markers. Day-1 model side-by-side settles `models.yaml`. | SC2 (≥3 comps, method, range, CP-05); SC3 (planted violation caught with rule and fix; corrected copy passes; CP-06 before "ready to publish"); SC4 (every channel card honest, markers link to findings); fixture test passes (SC under the hood). |
| **3, Tue 10-27** | **Step 5 Communications**, **Step 6 Offers**, **Step 7 Contract** (memorandum, attorney workspace, DOCX + PDF, side-by-side, disclosures, wet-ink markers), **Step 8 Buyer side**. | SC5 (no message leaves without CP-09; disclosures at first contact; broker name on every message); SC6 (≥2 offers, counter draft, seller decides); SC7 (draft, rider, side-by-side, PCDS attached, CP-14, notary/wet-ink marked); SC8 (four buyer screens, CP-16 blocks tours, CP-18). |
| **4, Wed 10-28** | **Step 10 Business marketing**; **Step 11 Demo mode** (steps.yaml, narration cards, Driver.js, generated DEMO-SCRIPT.md); timeline finished with planned checkpoints and supervision log; PII export and delete; Playwright headless end-to-end; record the replay run; spend roll-up into `docs/SPEND-LOG.md`; traceability statuses updated. **Joe clicks through on hughesnode in the afternoon.** | SC10; SC11 (Start demo walks 1 to 10, script matches screens, 12 to 15 min); SC9 complete; PII tests (no PII in logs, model-context whitelist, export, delete); full test suite green; Joe's click-through notes logged. |
| Thu 10-29 | Polish from Joe's notes (D15). | |

**Cut first if late (in this order):** pyHanko seal → Driver.js spotlights (narration cards stay) → Leaflet map
(static image) → flyer as PDF (HTML print view instead) → sqlcipher (Fernet columns stay) → live mode at the
meeting (replay only) → contract side-by-side reduced to section headings with one-line notes.
**Never cut:** checkpoint records and their gates, the fair-housing checker and its fixture test, "human required"
markers with reasons, the timeline built from records, narration cards, PII baseline, traceability.

---

## 10. Risks

| Risk | Effect | Handling |
|---|---|---|
| Step 7 reads as the company practising law (L21, L22) | Undercuts the product's legal story in front of a lawyer | Attorney-workspace framing (section 0); legends on every page of the draft; Joe decision 1 |
| Fair-housing checker misses a phrase in the live demo | Embarrassing in front of a broker; A8 kill criterion | Rules + model; 100% recall on the fixture set; planted violations are fixtures; replay mode makes the demo deterministic |
| Demo-house data incomplete (no comps from public records in time) | SC2 weak | Comps job runs before day 2; fallback: clearly labelled illustrative comps, flagged on screen and in the script |
| Real address mistaken for a listing (L9, L10) | Owner complaint; advertising rule | DEMONSTRATION mark everywhere; nothing sent; no owner name; no portal photos |
| WeasyPrint/Pango in the image | No PDFs | T1 on day 1; ReportLab / HTML print fallback |
| hughesnode type switch breaks the review pages | Joe loses his document links | Mount `public/` in the app; check `/docs-*.html` as a day-1 acceptance test; keep the static type until the container passes |
| No internet in the meeting room (Q-WS7-3) | Live calls and map fail | Replay mode default for the meeting; static map fallback; app runs locally on the laptop with one command |
| Spend overrun | Eats the $15 reserve | Haiku default; caching; app spend cap $12; replay for rehearsals and tests |
| Four days is tight for 11 screens | Missed click-through | Vertical slices; cut list above; Joe sees partial slices daily on hughesnode |
| Model output with unsafe HTML or prompt-injection text from simulated enquiries | Broken pages, wrong drafts | nh3 sanitising; the model drafts only; nothing is sent; every message gated by CP-09 |
| PII leaks into logs or prompts | Breaks SC PII baseline | Registry-driven masking; whitelist test; log grep test |
| Model IDs or prices change | Cost or breakage | IDs and prices in config; `model_call` logs real cost |
| Disk on the VPS | Build stalls | `scripts/disk-check.sh` before the image build; image under 600 MB |
| Pending laws (L20 public marketing; L42 AI disparate-impact audits; L62 AI notices) | Rules shift | Shown as "pending" notes on the relevant screens; rules file versioned |

---

## 11. Decisions for Joe

1. **Step 7 framing.** Provisional: the contract draft lives in an *attorney workspace* used by the seller's
   attorney, and the brokerage side stops at the accepted-offer memorandum, because WS2 found companies and brokers
   may not draft contracts (L21, L22). Alternative: keep it as worded in SC7 with a heavy "draft for attorney
   review" legend; legally weaker in front of an attorney audience.
2. **Who pays for the build** (D19): Max plan or more API credit. Provisional: the build runs as headless jobs only
   if Joe adds credit; otherwise on Max. The demo's own calls stay on the key, inside the $15 reserve.
3. **Live or replay at the meeting.** Provisional: replay by default (recorded the day before, labelled), with a
   live switch if the room has good internet.
4. **Contract structure** (Q-WS7-2): provisional bar-association long-form section structure, own wording.
