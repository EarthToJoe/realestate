# WS7 handoff: POC building blocks (gap fill, 2026-10-23, VPS session)

Source for everything below: `research_notes/WS7 POC building blocks/what_already_exists.md`, sections 0–12 (cloud pass)
and the appended "Gap fill (2026-10-23, VPS session)" sections G1–G14 (this pass). No WS7 deliverable was written,
by design; the architecture spec comes after Joe signs off the success criteria. Section references below ("G5")
point into that notes file: [notes](../../../research_notes/WS7%20POC%20building%20blocks/what_already_exists.md).

## 1. Assumption status lines

- A8 | still open | Every building block for "rules + model review + broker gate" exists and is current, but no authoritative fair-housing word list exists (HUD withdrew its 2024 ad guidance effective 2025-09-17; MLS lists conflict), so our own rules file and the 30+ phrase fixture test in the POC are what will settle A8 | notes G1, G12
- A11 | dodged (for the recommended stack) | The recommended stack is about 200 MB of permissively licensed Python packages plus vendored static files; the VPS already has Python 3.12.3 and `uv` and had 21 GB free today; the heavy candidates (docassemble: 4 GB RAM / 40 GB disk host; Langfuse: ~17.5 GiB RAM; self-hosted e-signature, inbox and scheduler servers) are skipped; Pango for WeasyPrint is unverified | notes G6, G14
- A4 | still open (WS3 owns) | OneKey's free Ocusell List (announced 2026-08-05, "on the cusp of launching") adds AI public-remarks tools and pre-publish rule checks to human MLS entry but no API is mentioned, so MLS entry stays a licensed human step in the POC | notes G1, G13
- A7 | partly supports | If the brokerage joins OneKey, forms, e-signature (TransactionDesk with AuthentiSign, reported as included in the subscription) and showing tools come with membership; otherwise e-signature costs $0.20 (DocuSeal cloud) to $0.75 (BoldSign) per document; no software building block threatens unit economics | notes G5, G13
- A1 | still open (WS2 owns) | The tooling supports a single-licensee design (deal state machine, approval records, server-side role checks), but whether one licensee may approve everything is a legal question WS7 cannot answer | notes G7
- A3 | still open (WS2 owns) | No contract template can be adopted (NYSAR's purchase agreement is member-only; the bar-association form has no visible licence), so the POC writes its own contract text and routes it to attorney review, which fits "a cheaper, faster lawyer step" better than "no lawyer" | notes G4

## 2. Kill criteria

- K4 (built or pitched as autonomous): dodged by design. Every licensed act is a server-enforced approval record; autonomous agent runtimes (Claude Agent SDK, LangGraph loops) are skipped for the POC; the checker and drafts always end at a broker or attorney gate.
- K9 (cannot get or keep MLS membership): still open, but this pass raises the stakes: OneKey's subscription bundles forms, e-signature, showing scheduling and a listing-entry tool with AI remarks, so an off-MLS firm would have to buy or build all of them.
- A8's kill criterion (violation or error rate too high even with review): open until the POC's fixture tests run.
- A11's kill criterion (free space cannot be recovered): not hit; 21 GB free on 2026-10-23.
- K1–K3 and K5–K8: not addressed by WS7.

## 3. Questions for Joe

- **Q-WS7-1. Will the brokerage be a OneKey MLS subscriber and a NYSAR member?** Provisional: yes, in production. The POC
  shows forms, e-signature and showings as "through the MLS tools, by a licensed human" markers and uses its own templates
  and simulated signing. Unblocks: whether production e-signature and forms come from the MLS bundle (TransactionDesk,
  SkySlope Forms, NYSAR forms) or from DocuSeal or BoldSign.
- **Q-WS7-2. Which purchase contract does your father-in-law use for Hudson Valley sales?** Options: NYSAR's statewide
  purchase agreement (signed subject to attorney approval), the bar-association Residential Contract of Sale, or his own
  form. Provisional: mirror the bar-association long form's section structure with our own wording, labelled "draft for
  attorney review". Unblocks: the contract template and the "side-by-side against the standard form structure" screen
  (success criterion 7).
- **Q-WS7-3. Will the demo room have reliable internet?** Provisional: assume not. Build a clearly labelled "replay
  recorded AI outputs" switch and an offline map fallback. Unblocks: demo-mode design.
- **Q-WS7-4. Is your Anthropic Console account an organisation, and do you want to ask Anthropic for zero data
  retention?** Provisional: no zero retention; assume Anthropic keeps API inputs and outputs up to 30 days; send the model
  only what each step needs, with names and contact details masked. Unblocks: the PII wording in the plan and whether spend
  can be reconciled automatically (the Usage and Cost API needs an organisation Admin key).
- **Q-WS7-5. May we ask Zillow for its FairHome fair-housing dataset?** (Access is by email request, with a use case.)
  Provisional: no, not for the POC; our own 30+ phrase fixture set is enough; revisit for production. Unblocks: breadth of
  the checker's test set.

## 4. "What already exists" table (ready to paste into `docs/specs/poc-architecture.md`)

Checked 2026-10-23. Licences and versions come from the publishers' pages or package registries cited in the notes
(G1–G14). "(try first)" marks candidates the architecture step should try on a real example before deciding.

| Candidate | Building block | Licence | Cost | Adopt / adapt / borrow ideas / skip | Why |
|---|---|---|---|---|---|
| FastAPI 0.161.1 + Jinja2 3.1.6 + uvicorn 0.54.0 | Web app and screens | MIT / BSD / BSD | Free | Adopt | Provisional stack (decision 7); current releases; server-rendered screens show each step |
| htmx 2.0.11 (+ jinja2-fragments 1.12.0) | Interactivity, partial updates | 0BSD (+ MIT) | Free | Adopt (vendor the file) | No build step; 4.0 exists but htmx will not mark it `latest` until 2027 |
| Bulma 1.0.4 or Bootstrap 5.3.8 | CSS | MIT | Free | Adopt one | Maintained; Pico CSS is unmaintained; write the timeline and step list ourselves (~50 lines CSS) |
| Anthropic Python SDK 2.1.0 (`messages.parse`, strict tools) | Listing and marketing copy, buyer/seller replies, offer comparison, contract drafting, fair-housing model review | Apache-2.0 | Per token | Adopt | Structured outputs are generally available on Opus 5.5 / Sonnet 5.5 / Haiku 5.5; one schema-checked call per AI step, logged as a visible AI action |
| Claude Agent SDK 0.2.173 | Agent loop with tool approvals | MIT file; use governed by Anthropic Commercial Terms | Per token | Borrow ideas (`can_use_tool`, `PreToolUse` deny hooks) | Bundles the Claude Code CLI (~130 MB wheel) and is built for coding agents; the POC needs single calls, not a loop |
| PydanticAI 2.60.0 / LangGraph 1.2.16 | Human-in-the-loop frameworks | MIT | Free | Borrow ideas (deferred tools; interrupt/resume) | Extra abstraction between the screen and the call; approval must be enforced server-side anyway |
| python-statemachine 3.2.2 (or transitions 0.9.3) | Deal steps, actors and checkpoint guards | MIT | Free | Adopt or hand-roll (try first) | Small and active; guards and diagrams could drive both the workflow and the human-in-the-loop map; try on the deal lifecycle first |
| SpiffWorkflow 3.2.0 | BPMN workflow engine | LGPLv3 | Free | Skip | BPMN is more machinery than ~12 steps need |
| HumanLayer | Human-approval service | n/a | n/a | Skip | Pivoted to a coding IDE |
| ArkansasONE MLS list (Mar 2026), OneKey MLS list, NYC CCHR examples, DOS-2156 protected classes, HUD 1995 memo (as summarised) | Fair-housing rules file | Publishers' copyright | Free to read | Borrow ideas (categories, tiers, example phrases); write our own rules | No authoritative list exists; lists conflict (e.g. "mother-in-law suite"); add NY rules on school, neighbourhood-composition, safety and source-of-income talk |
| Zillow fair-housing-guardrail + FairHome dataset | Fair-housing classifier and test data | OpenRAIL-S; dataset licence not stated | Free; model and data by request | Borrow ideas (stop list + classifier + prompt) | Needs PyTorch-scale models; an API model already does the review |
| FairProp-AI, debary-mcp-compliance, real-estate-pack, prosperity skills | Community fair-housing checkers | MIT / Apache-2.0 | Free | Skip | 0–11 stars, unverified claims, commercial ties in one case |
| docxtpl 0.20.2 (python-docx 1.2.0) | Attorney-editable DOCX contract drafts | LGPL-2.1 (MIT) | Free | Adopt | Jinja-style templates; used as an unmodified library |
| WeasyPrint 70.0 | PDF of contract, disclosures, flyer | BSD | Free | Adopt (try first on the VPS) | Reuses Jinja2 HTML; needs Pango ≥ 1.44, not yet verified on the VPS; sanitise model output first |
| ReportLab 5.1.0 / pypdf 6.21.2 | PDF fallback; merge and fill current government PDFs | BSD / BSD-3 | Free | Adopt pypdf; ReportLab as fallback | Permissive and current |
| PyMuPDF 2.0, borb 3.0.9 | PDF libraries | AGPL (PyMuPDF also commercial) | Commercial licence for PyMuPDF | Skip | AGPL in a proprietary product; PyMuPDF wheels 63–89 MB |
| docassemble (1.10.14) | Guided interviews and document assembly | MIT | Free | Borrow ideas | Host needs 4 GB RAM and 40 GB disk, 13 services in one container; too heavy for this VPS |
| NY statutory forms: RPL §443 agency disclosure, RPL §462 PCDS, DOS-2156, EPA lead-paint form | Disclosure templates | Statute text; federal work | Free | Adapt (render our own from statute text) | DOS still serves a 2023 PCDS PDF with the repealed $500 credit, so generate the PCDS from the current statute and show an attorney checkpoint |
| NYSAR statewide forms (purchase agreement etc.) | Contract form | NYSAR, member-only | Free to NYSAR members | Production: adopt if a member; POC: borrow structure only | Text is not public; see Q-WS7-1/2 |
| Bar-association Residential Contract of Sale (11-2000) | Contract form | No licence visible | n/a | Borrow ideas (section structure only) | Structure is not protected expression; copying clauses would be |
| pyHanko 0.38.0 (or endesive 3.0.1) | Tamper-evident seal on the simulated signing | MIT | Free | Adopt (try first) | Seals a generated PDF with a "DEMO" certificate so a reader flags later edits; README says "beta" |
| DocuSeal 3.3.3 | E-signature (self-host or cloud API) | AGPLv3 + attribution term | OSS free; Pro $240/user/yr; cloud API $0.20/doc | Skip in POC; production candidate | Separate Rails container; open-source edition must keep DocuSeal attribution in the UI |
| TransactionDesk + AuthentiSign (Lone Wolf, via OneKey MLS) | E-signature, forms, transaction file | Proprietary | Reported included in OneKey subscription | Production candidate if a OneKey member; confirm API | Likely the cheapest production path; if no API, signing stays a broker step on the timeline |
| BoldSign / Dropbox Sign / DocuSign APIs | E-signature API | Proprietary | BoldSign $0.75/envelope; others tiered | Skip in POC; compare at launch | Only if the MLS bundle cannot be driven by API |
| Documenso 2.21.1 / OpenSign 3.0.0 | E-signature servers | AGPL | Free self-host | Skip | Node + Postgres or MongoDB, ≥ 2 GB RAM, own signing certificate |
| presidio-anonymizer 2.2.364 (+ analyzer with spaCy `en_core_web_sm`, 12 MB, only if names must be found) | PII masking before model calls and logs | MIT | Free | Adapt (our own regex recognisers) | Community-governed, current; anonymizer alone is 4 packages; skip spaCy `lg` (382 MB) and transformer NER |
| sqlcipher3 0.6.4 (SQLCipher 4.x) | Encryption at rest of the SQLite file | Zlib + SQLCipher BSD-style attribution | Free | Adopt (try first: wheel on Python 3.12) | Self-contained wheels since 0.6.2; replaces the earlier `sqlcipher3-binary` pick (labelled SQLCipher 3.x) |
| cryptography 50.0.2 (Fernet) | Field-level encryption for ID numbers | Apache-2.0 OR BSD-3 | Free | Adopt | Standard, current |
| Own `events` table with append-only triggers and hash chain (sqlite-chronicle pattern) | Audit log, PII access log, AI-action log | Apache-2.0 (pattern) | Free | Adopt pattern, build ours | One record family shows every AI action and every human decision |
| structlog 26.1.0 | Application logs without PII | MIT OR Apache-2.0 | Free | Adopt | Processors drop or mask PII before writing |
| nh3 0.3.7 | Sanitise model output before HTML/PDF | MIT | Free | Adopt | Model output is untrusted input for the browser and WeasyPrint |
| Langfuse / Arize Phoenix | LLM tracing dashboards | MIT core (unverified) / Elastic 2.0 | Free self-host | Skip | Langfuse minimum ~17.5 GiB RAM across five services; our own table is the visible log |
| Anthropic Usage and Cost Admin API | Spend reconciliation for `docs/SPEND-LOG.md` | API | Free | Adopt if an organisation Admin key exists | Per-key and per-model daily cost; per-call usage from the SDK gives per-module spend |
| Driver.js 1.10.2 | Spotlight for the guided demo | MIT | Free | Adopt (try first with HTMX swaps) | Only current MIT tour library; no build step; narration cards and `docs/DEMO-SCRIPT.md` come from one steps file |
| Shepherd.js 15.3.0 / Intro.js 8.6.0 | Product tour | AGPL-3.0 + commercial | $50–$300 / $9.99–$299.99 lifetime | Skip | Commercial licence required; Driver.js does the job free |
| Arcade / Storylane | Recorded click-through demos | SaaS | Free tier; ~$32–$50 per seat a month | Skip (optional leave-behind later) | The live app is the demo |
| RESO Data Dictionary 2.0 metadata JSON (+ UPI 2.0) | Field names and parcel identifier | RESO EULA, royalty-free | Free | Adopt (a ~40-field subset; UPI on each property) | 2.1 is still a draft; names cost nothing and ease later MLS work |
| reso-tools (TypeScript) / web-api-commander (Java) | RESO validation and certification | RESO EULA | Free | Skip | Node-only; Commander is retired; the POC does not speak the RESO Web API |
| RESO Offer Management standard | Offer data model | RESO (terms not read) | Free | Borrow ideas (read before designing offers) | Industry field names for the offers screen |
| usaddress 0.5.16 / usaddress-scourgify 0.7.1 | Address parsing and normalising at intake | MIT / licence not stated | Free | Adopt usaddress; scourgify after a licence check | Scourgify follows USPS Pub 28 and RESO guidelines |
| NYS Geocoder (May 2026) / Census Geocoder | Address to coordinates and county | Public services | Free | Adopt behind an interface (demo uses fictional data) | Call the Census API directly (the `censusgeocode` wrapper is GPLv3) |
| FEMA NFHL, NYS Tax Parcels, Open NY assessment rolls, NYS orthoimagery | Public-record facts and aerial view at intake | Public data | Free | Borrow later; FEMA flood point query (try first) | Show as tagged "public record" facts on the profile only, never as help filling the seller's PCDS (WS2 notes record NYSAR's advice that licensees should not assist with the PCDS) |
| Leaflet 1.9.4 + OSM tiles (or OpenFreeMap) | Map on property and timeline screens | BSD-2; ODbL data | Free (light use, attribution) | Adopt (vendored) with an offline fallback | ~42 KB, no build; OSM policy forbids bulk or offline use, so keep a static image or small Protomaps extract for the meeting |
| MapLibre GL JS 6.15.0 / OpenLayers 10.11.0 | Vector maps | BSD-3 / BSD-2 | Free | Skip | Heavier packages, WebGL; no demo gain |
| Chatwoot CE / Cal.com | Shared inbox / showing scheduler | MIT / AGPLv3 + EE | Free self-host | Skip; borrow inbox layout | Each adds Postgres and Redis; showings run through the MLS's ShowingTime in production |
| pytest 9.1.1 + Playwright 1.64.1 (`--only-shell`) | Fixture tests and headless end-to-end demo run | MIT / Apache-2.0 | Free | Adopt | Headless shell avoids the ~281 MB full Chromium |
| promptfoo / inspect-ai / deepeval | LLM evaluation harness | MIT / MIT / Apache-2.0 | Free | Skip for POC | Second toolchain (Node) or 31–113 dependencies; pytest covers 30+ fixtures |
| EspoCRM / Krayin / Twenty | Whole-product CRM baseline | AGPL / MIT / AGPL + commercial | Free | Skip | PHP or Node + MySQL/Postgres/Redis; generic screens hide the AI/human/licensed split |
| AleksNeStu/ai-real-estate-assistant | Reference AI real estate app | MIT | Free | Borrow ideas (demo mode with simulated AI responses) | Too large to adopt; replay mode protects the live demo |
| Ocusell List (OneKey) | MLS listing entry with AI remarks and rule checks | Proprietary | Free to OneKey members | Production path for the licensed human's MLS entry (WS3) | Not an API; the POC shows it as a licensed-human step |

**Try on a real example before deciding** (architecture step, no installs until then):
1. WeasyPrint 70.0 on the VPS: check Pango (`dpkg -s libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0`), render a 10-page contract.
2. `sqlcipher3` 0.6.4 wheel on Python 3.12: create, encrypt, reopen.
3. `python-statemachine`: model the deal lifecycle with actors and guards; compare with ~80 lines of hand-rolled code.
4. pyHanko: seal a generated contract PDF with a demo certificate and confirm a PDF reader flags an edit.
5. Driver.js: a two-screen tour that survives HTMX fragment swaps.
6. FEMA NFHL point query and the NYS Geocoder for one real Hudson Valley address (only to prove the connector; the demo uses fictional data).
7. Presidio anonymizer with our regex recognisers on a sample buyer message, then re-insertion after a model call.
8. Leaflet with OSM tiles plus the offline fallback, on the meeting laptop.

## 5. Open gaps that still matter, and what would close them

- **Pango and fonts on the VPS** (WeasyPrint): the inspection command needed approval in this headless run. Close: run the
  `dpkg -s` line above in the chat session (read-only, no install).
- **Is TransactionDesk/AuthentiSign included in the OneKey subscription, and does it have an API our software can drive?**
  The OneKey support page blocks automated reads. Close: OneKey MLS member support, through the support site, or the
  father-in-law's member login.
- **OneKey MLS's full fair-housing word table**: bot-blocked. Close: a OneKey member opens the support article (URL in notes
  G1) and pastes the table for the rules file.
- **NYSAR statewide purchase agreement text and terms of use**: member-only. Close: the father-in-law's NYSAR login, or NYSAR's
  legal department.
- **Anthropic retention for a standard API key**: the API docs and the privacy centre word it differently ("not retained by
  default" vs "deleted within 30 days"). Close: Console privacy settings or Anthropic support; until then assume 30 days.
- **RESO Offer Management specification**: exists, not read. Close: read `specification.md` in the RESOStandards repository
  before designing the offers table.
- **FEMA NFHL endpoint**: connection reset during this pass. Close: retry during the architecture step.

## 6. Contradictions and cross-workstream updates

- **WS2 (fair_housing_disclosures_ai_privacy.md, KQ1 Gaps)** says it is unverified whether HUD rescinded its April 29, 2024
  digital-advertising guidance. It is withdrawn: HUD notice FR-6571-N-01 (Federal Register 2026-06624, published 2026-04-06),
  withdrawal effective 2025-09-17. The 1995 advertising memo is not on the withdrawal list. (Notes G1.)
- **WS2 (same file, line 51)** quotes the 1995 memo as treating "mother-in-law suite" as acceptable [CLAIMED]. Oregon REALTORS
  (2024) confirms that reading [SECONDARY], but ArkansasONE MLS's March 2026 list now marks "Mother-in-law suite", "Granny
  flat", "His and hers" and "Walking distance" unacceptable: MLS practice is now stricter than HUD's 1995 view. OneKey's own
  table is unread.
- **WS4 (costs_and_revenue_benchmarks.md)** says OneKey's product list states no inclusion or price for TransactionDesk. A
  search summary of OneKey's support page says TransactionDesk is "included in your OneKey MLS Subscription" [SECONDARY,
  page bot-blocked]; if confirmed, the cost model can drop separate e-signature and forms costs for a OneKey member.
- **WS4** gives BoldSign "from $30/month"; BoldSign's own support article states $0.75 per API envelope and does not mention
  the $30 base or 40-envelope allowance, which come from a third party (Verdocs).
- **WS3 (mls_access.md)** covers Ocusell List; OneKey's 2026-08-05 release adds that List includes "optional AI tools" for
  public remarks and "built-in rule checks". That matters to WS5 as well: the MLS itself will offer AI listing copy to every
  member.
- **WS1 and WS2** already record that the 2024 PCDS amendment removed the $500 credit. New here: on 2026-10-23 DOS still serves
  the PCDS as "DOS-1614-f (Rev. 06/23)" with the $500 credit sentence, so anyone downloading the state's PDF gets a superseded
  form.
- **Within WS7**: the cloud pass recommended `sqlcipher3-binary` and gave spaCy `lg` as ~560 MB; corrected to `sqlcipher3`
  0.6.4 and 382 MB (notes G9).

## Orchestrator check (2026-10-23)
- WeasyPrint system libraries on the VPS host: Pango 1.52.1, pangoft2, HarfBuzz 8.3.0, fontconfig, cairo 1.18
  and DejaVu fonts are installed; `libharfbuzz-subset0` is not (optional). Moot if the POC runs in a Docker
  image on hughesnode (decision 13), which installs its own.
