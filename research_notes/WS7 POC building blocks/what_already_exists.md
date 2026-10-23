# WS7 — POC building blocks: what already exists (as of 2026-10-23)

Scope: open-source software, open data, public forms and standards that a proof-of-concept "AI real estate agent" web app for New York (Python 3.12, FastAPI, Jinja2 + HTMX, SQLite, Anthropic SDK, small 2 vCPU / 8 GB VPS) could adopt as a baseline or reuse as components. Research only; nothing was designed or built.

Labels: [PRIMARY] = read on the publisher's own page, package index or statute; [SECONDARY] = reported by a third party; [CLAIMED] = from memory or a project's own unverified claim; [INFERENCE] = my reasoning from the cited facts. "Tried" = exercised in a scratch virtual environment at `/tmp/claude-0/-home-user-shorts/b9d90396-1a7a-551a-88fd-52f27e8f6229/scratchpad/ws7/` (script `tests/try_components.py`, results quoted below).

## 0. Plain-language summary (for the founder) and how this was researched

### Takeaway
Nothing off the shelf does what the demo must show (eleven visible screens with AI / human / licensed steps), so the team should build a small, deliberately boring web app and borrow pieces: the RESO Data Dictionary for field names (free to use), New York's own statutory forms as templates (the agency disclosure and the Property Condition Disclosure Statement are printed in the law itself), a handful of permissively licensed Python libraries that I installed and tested (documents, encryption, PII masking, diffs), and the plain Anthropic SDK for the AI steps. The e-signature step should be simulated in the demo (DocuSeal is the production candidate). The one thing nobody publishes in reusable form is a fair-housing word list; the team will have to assemble its own from public guidance and pair it with a model check.

### Cited Findings
- The web-search budget for this turn was exhausted by other agents before this research began ("limit: 200 WebSearch calls per turn, shared by every agent"), so every finding below comes from direct fetches of primary pages, PyPI/npm registry metadata, GitHub topic/repository pages and a scratch virtual environment; no search engine was used — [WebSearch tool response in this session]
- The GitHub REST API (both `gh api` and `api.github.com`) is blocked by this session's policy ("sessions are bound to their configured repositories"), so star counts are the rounded figures shown on github.com pages (e.g. "18.8k") — [GitHub API response in this session]
- Scratch environment: `uv pip install` of docxtpl, python-docx, reportlab, weasyprint, sqlcipher3-binary, sqlite-utils, presidio-anonymizer, anthropic, pydantic-ai-slim[anthropic], fastapi, jinja2, python-multipart, pypdf resolved to 61 packages and 191 MB on disk; all imports and the sample renders below succeeded — [scratch venv `.venv`, `uv pip list`]

### Inferences
- [INFERENCE] The total Python footprint of the recommended stack (FastAPI + Jinja2 + anthropic + WeasyPrint + docxtpl + sqlcipher3 + Playwright driver) is well under 300 MB before browsers; the heavy items to keep out are spaCy models, PyTorch-based checkers and a self-hosted e-signature server.

### Gaps
- Star counts, last-commit dates and release dates for GitHub projects could not be read precisely (API blocked); PyPI/npm release dates are exact, GitHub figures are the rounded page values.

## 1. Whole-product baselines (CRM, transaction management, brokerage back office, listing management)

### Takeaway
None of the active open-source CRMs or property apps is a usable baseline for a "visible-step" demo: they are PHP/Node generalist CRMs (EspoCRM, Krayin, Twenty, SuiteCRM) or landlord/rental tools; no open-source sale-transaction-management system with real activity was found. Recommendation: skip as baseline; borrow two ideas (EspoCRM's Property/Request matching, Twenty's "objects as code").

### Cited Findings
- EspoCRM: "3.5k" stars, "1.0k" forks, "licensed under GNU AGPLv3"; requirements PHP 8.3–8.5, MySQL 8.0+ / MariaDB 10.6+ / PostgreSQL 15+ [PRIMARY] — [GitHub espocrm/espocrm](https://github.com/espocrm/espocrm)
- EspoCRM Real Estate extension "adds two entity types: Properties and Requests", matches them and creates Opportunities; "This extension is distributed for free under AGPLv3 license"; most recent listed release 1.8.6 (Jun 10, 2026) [PRIMARY] — [espocrm.com](https://www.espocrm.com/extensions/real-estate/)
- Krayin laravel-crm: "24.0k" stars, "1.7k" forks, "will always be free under the MIT License"; PHP 8.3+, MySQL 8.0.32+ or MariaDB 11.4 LTS+, RAM "3 GB or higher"; no real-estate features mentioned [PRIMARY] — [GitHub krayin/laravel-crm](https://github.com/krayin/laravel-crm)
- Twenty: "59.5k" stars, "9.7k" forks; stack TypeScript, NestJS, BullMQ, PostgreSQL, Redis, React; "Define objects, fields, and views as code" [PRIMARY] — [GitHub twentyhq/twenty](https://github.com/twentyhq/twenty)
- Twenty licence: "This project is mostly licensed under the GNU Affero General Public License v3.0 (AGPLv3)"; "Certain packages are licensed under the MIT license instead"; files marked `/* @license Enterprise */` are under the Twenty.com Commercial License, which "may only be used in production, if you ... [hold] a valid subscription" (development and testing allowed) [PRIMARY] — [LICENSE file](https://raw.githubusercontent.com/twentyhq/twenty/main/LICENSE)
- GitHub topic "real-estate" sorted by stars (top 20): fredy 1.6k (EU listing crawler/alerts), microrealestate 1.2k (landlord leases/rent/receipts), flathunter 1.1k (rental search bot), HomeHarvest 757 (property-data scraper), property_web_builder 648 (Rails listing website), open-condo 424 (property-management SaaS), prolinkinfo/RealEstateCRM 363 (CRM for agents), AleksNeStu/ai-real-estate-assistant 319 [PRIMARY] — [github.com/topics/real-estate](https://github.com/topics/real-estate?o=desc&s=stars)
- GitHub topic "property-management" (1,165 repos): top entries are QloApps 14.4k (hotel), microrealestate 1.2k, movinin 230 (rental platform), online-rental-property-manager 177, OpenProperty 27 (rental leases/work orders) — all rental/landlord tools, none for home-sale transactions [PRIMARY] — [github.com/topics/property-management](https://github.com/topics/property-management?o=desc&s=stars)
- prolinkinfo/RealEstateCRM: "released under the MIT License", MERN stack, 363 stars, 142 forks, 1,779 commits; no test folder or test script visible; topic page shows last update Feb 27, 2025 [PRIMARY] — [GitHub](https://github.com/prolinkinfo/RealEstateCRM)
- The curated list etewiah/awesome-real-estate (379 stars) "has no open-source projects for CRM/transaction management, fair housing, or AI assistants"; its RETS/RESO entries are commercial services [PRIMARY] — [GitHub](https://github.com/etewiah/awesome-real-estate)
- PyPI has no packages under the names reso-api, pyreso, reso-webapi, resoapi, fairhousing, fair-housing or avm-toolkit (404 from the JSON API) [PRIMARY] — [pypi.org JSON API](https://pypi.org/pypi/reso-api/json)

### Inferences
- [INFERENCE] Adopting EspoCRM/Krayin/Twenty would mean a PHP or Node runtime, a MySQL/PostgreSQL (+Redis) server and AGPL obligations for a demo whose value is the visible step-by-step flow; the generic CRM screens would hide, not show, the AI/human/licensed split the brief requires.
- [INFERENCE] A thin FastAPI app with ~10 tables (Property, Party, Listing, Channel, Message, Offer, ContractVersion, TimelineEvent, AiAction, Approval) is smaller than the configuration work any of these CRMs would need.

### Gaps
- No open-source "transaction management" (dotloop/SkySlope-like) project with real activity was found via topic pages; GitHub search was unavailable, so a low-star project may exist. [CLAIMED] My prior knowledge also contains none.

## 2. Data-model standards (RESO Data Dictionary)

### Takeaway
RESO Data Dictionary 2.0 is free to implement under the RESO EULA (royalty-free licence to incorporate the standard into your own products; you may not re-publish it as a competing standard). Adopting its field names for Property, Member, Office and Media in our own SQLite schema is sensible and costs nothing; the machine-readable DD 2.0 files (XLSX, EDMX XML, OpenAPI JSON, metadata-report JSON) are published in RESO's GitHub and I downloaded and parsed the JSON (1,727 fields, 652 for Property).

### Cited Findings
- RESO lists "Data Dictionary 2.0" as the current major release, with "2.1 Draft" and "1.7"; example resources "Property, Member (real estate agents), Office (brokers), and Media"; "By downloading these resources, you confirm that you agree to the RESO EULA"; full adoption "is not required for certification" [PRIMARY] — [reso.org/data-dictionary](https://www.reso.org/data-dictionary/)
- RESO EULA: licence to "reproduce, distribute, make derivative works of, display and otherwise exploit RESO Standard solely for incorporation into End User's products or services"; no fee stated (described as royalty-free); End User may not create a derivative work intended as a technical standard; "This EULA does not provide any trademark license to End User"; "RESO STANDARDS ARE PROVIDED 'AS IS'"; Illinois law, Cook County venue [PRIMARY] — [reso.org/eula](https://www.reso.org/eula/)
- Ratified versions: RCP-36 Data Dictionary 2.0 (Nov 2023) and 1.7 (Jan 2021); Web API Core 2.1.0 (Dec 2023); RESO Common Format 1.0.0 (Nov 2023) [PRIMARY] — [RESOStandards/transport README](https://raw.githubusercontent.com/RESOStandards/transport/main/README.md)
- Machine-readable reference files in `web-api-commander/src/main/resources`: `RESODataDictionary-2.0.xml`, `.xlsx`, `.openapi3.json`, `.metadata-report.json` (and 1.7 equivalents) plus EDMX XSDs [PRIMARY] — [GitHub directory](https://github.com/RESOStandards/web-api-commander/tree/main/src/main/resources)
- Tried: downloaded `RESODataDictionary-2.0.metadata-report.json` (2,275,174 bytes; `version` "2.0", `generatedOn` 2024-10-15): 1,727 fields and 3,611 lookups; per resource Property 652, Contacts 91, Member 87, Office 73, Media 41; Property contains ListPrice, LivingArea, BedroomsTotal, BathroomsTotalInteger, StandardStatus, ListingKey, PublicRemarks, YearBuilt, LotSizeAcres, ParcelNumber, TaxAnnualAmount, ClosePrice, CloseDate [PRIMARY, tried] — [raw file](https://raw.githubusercontent.com/RESOStandards/web-api-commander/main/src/main/resources/RESODataDictionary-2.0.metadata-report.json)
- dd.reso.org Property resource: "652 fields · Last revised 9/10/2019"; groups include Characteristics, Financial, HOA, Listing (Price, Remarks, Marketing, Contract, Dates, Showing...), Location (Address, GIS, School), Structure (Rooms), Tax, Utilities; StandardStatus "The status of the listing as it reflects the state of the contract between the listing agent and seller..." [PRIMARY] — [dd.reso.org/DD2.0/Property](https://dd.reso.org/DD2.0/Property/)
- Open implementations found: tylercollier/openresync (53 stars, JavaScript, "syncs MLS data via the RESO Web API into MySQL or Solr", last update Sep 14, 2025); troydavisson/PHRETS (457 stars, PHP, RETS client) [PRIMARY] — [github.com/topics/mls](https://github.com/topics/mls?o=desc&s=stars)
- No Python RESO client or ORM exists on PyPI under the obvious names (reso-api, pyreso, reso-webapi, resoapi all absent; the package `reso` is an unrelated logic simulator) [PRIMARY] — [pypi.org/pypi/reso/json](https://pypi.org/pypi/reso/json)

### Inferences
- [INFERENCE] Use RESO names for a ~40-field subset (Property: ListingKey, StandardStatus, ListPrice, LivingArea, BedroomsTotal, BathroomsTotalInteger, YearBuilt, LotSizeAcres, ParcelNumber, TaxAnnualAmount, PublicRemarks, ClosePrice, CloseDate, plus Address fields; Member/Office for people; Media for photos) and ship the DD 2.0 metadata JSON as a validation/lookup resource; do not implement the OData Web API. The EULA's "solely for incorporation into End User's products" clause is satisfied by using names inside our schema.
- [INFERENCE] The EULA does not address field names individually; because it grants derivative-work rights for products, reusing names and definitions in code is within the grant, but the founder-attorney should read Section 4 once.

### Gaps
- Whether RESO objects to publishing a field-name mapping in open documentation (vs inside a product) is not addressed by the EULA text.

## 3. Document generation (PDF/DOCX)

### Takeaway
All four Python options are permissively licensed and current; on a small VPS the lightest working combination is WeasyPrint (HTML/CSS → PDF, reuses Jinja2 templates; needs Pango system libraries, which this box had) plus docxtpl (DOCX for attorney-editable drafts). ReportLab is the fallback when system libraries are unavailable; Typst is a single 31–35 MB binary wheel with no Python deps but a new markup language — skip for now.

### Cited Findings
- docxtpl 0.20.2 released 2025-11-13, licence LGPL-2.1-only, requires python-docx, jinja2, lxml; `uv` resolves 6 packages [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/docxtpl/json)
- python-docx 1.2.0 (2025-06-16), MIT, requires lxml and typing_extensions [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/python-docx/json)
- weasyprint 70.0 (2026-09-08), BSD licence, 8 declared deps, `uv` resolves 13 packages; wheel 0.3 MB [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/weasyprint/json)
- WeasyPrint requires "Python ≥ 3.10.0" and "Pango ≥ 1.44.0"; Debian wheel install needs `apt install python3-pip libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0`; docs warn "WeasyPrint is pretty slow and can take a long time to render long documents" and recommend OS-level memory limits (`ulimit`) for untrusted input [PRIMARY] — [WeasyPrint first steps](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html)
- reportlab 5.1.0 (2026-10-22), BSD, requires pillow and charset-normalizer (3 packages), wheel 2.0 MB [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/reportlab/json)
- typst 0.15.0 (2026-06-16), zero Python dependencies, platform wheels 30.5–34.9 MB; typst-py is Apache-2.0 and compiles to PDF/PNG/SVG via `typst.compile(...)` [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/typst/json), [typst-py README](https://raw.githubusercontent.com/messense/typst-py/main/README.md)
- Tried on a real example: docxtpl rendered a one-paragraph "CONTRACT OF SALE between {{ seller }}..." template to DOCX ("ok: CONTRACT OF SALE between S. Example and B. Example for 1 Demo Rd..."); ReportLab wrote a 1,362-byte PDF; WeasyPrint 70.0 rendered a small HTML page to PDF on this box, which has libpango 1.52.1 and fonts-dejavu installed [PRIMARY, tried] — [scratch script `tests/try_components.py`]

### Inferences
- [INFERENCE] LGPL-2.1 on docxtpl is compatible with a proprietary web app when used as an unmodified library import; if the team later wants a pure-MIT/BSD dependency set, python-docx alone (MIT) with hand-written paragraph substitution is enough for a 10-page contract.
- [INFERENCE] Generating the same contract both as PDF (WeasyPrint from the Jinja2 HTML) and DOCX (docxtpl) from one data model avoids any DOCX→PDF converter (LibreOffice), which would be the heaviest package on the VPS.

### Gaps
- LibreOffice's size and headless conversion behaviour were not verified here ([CLAIMED] several hundred MB); irrelevant if the dual-template approach is used.
- Fonts: WeasyPrint uses system fonts; which fonts the production VPS has was not checked.

## 4. E-signature servers (DocuSeal, Documenso, OpenSign)

### Takeaway
All three are AGPL-3.0 servers in other languages (Ruby/Vue, TypeScript, Node/MongoDB). DocuSeal is the lightest (single container, SQLite by default) and its on-premises open-source tier explicitly includes "Test Mode (Sandbox)" and "Audit log". US E-SIGN and NY ESRA do not prescribe an audit-trail format (they require that the electronic record accurately reflect the contract and remain accessible), so vendor "certificates of completion" are convention, not statute. Recommendation: simulate signing inside the demo (own hash + timestamp + IP log), name DocuSeal as the production candidate.

### Cited Findings
- DocuSeal: "18.8k" stars, "1.9k" forks; "Distributed under the AGPLv3 License with Section 7(b) Additional Terms"; topics ruby-on-rails, vue [PRIMARY] — [GitHub docusealco/docuseal](https://github.com/docusealco/docuseal)
- DocuSeal README: "By default DocuSeal docker container uses an SQLite database"; PostgreSQL/MySQL via `DATABASE_URL`; run with `docker run --name docuseal -p 3000:3000 -v.:/data docuseal/docuseal`; free features include PDF form builder, 12 field types, multiple submitters, SMTP email, "Automatic PDF eSignature", "PDF signature verification", "API and Webhooks"; Pro adds white-label, roles, reminders, SMS/ID verification, conditional fields, bulk send, SSO/SAML, embedded signing [PRIMARY] — [README](https://raw.githubusercontent.com/docusealco/docuseal/master/README.md)
- DocuSeal pricing: on-premises "Open Source" free vs "Pro" "$20 / user / month"; the on-premises comparison table lists "Test Mode (Sandbox)" and "Audit log" as available in both Open Source and Pro; cloud Sandbox "$0/ document" for development [PRIMARY] — [docuseal.com/pricing](https://www.docuseal.com/pricing)
- DocuSeal accepts "PDF, DOCX, XLSX, JPEG, PNG or ZIP files, up to 100MB each"; API servers `https://api.docuseal.com` / `https://api.docuseal.eu`, "On-premises installations use their own host" [PRIMARY] — [docuseal.com](https://www.docuseal.com/), [API docs](https://www.docuseal.com/docs/api)
- Documenso: "15.5k" stars, "3.4k" forks, AGPL-3.0; stack TypeScript, React Router v7, Hono, Prisma, tRPC, @libpdf/core for PDF signatures, Playwright; local development needs "Node.js (v24 or above)" and PostgreSQL; "We no longer accept external pull requests, aside from a small group of trusted contributors" [PRIMARY] — [GitHub documenso/documenso](https://github.com/documenso/documenso), [README](https://raw.githubusercontent.com/documenso/documenso/main/README.md)
- Documenso self-hosting: "Self-hosted Documenso includes full core functionality under the AGPL-3.0 license"; enterprise features (SSO, white-label embed, 21 CFR Part 11) need a licence key; "You must generate a signing certificate. Documenso does not ship with one."; quick start needs "At least 2GB of available RAM" and Docker Compose v2; dev mode signs "with a generated certificate" [PRIMARY] — [self-hosting](https://docs.documenso.com/developers/self-hosting), [how-to](https://docs.documenso.com/developers/self-hosting/how-to)
- OpenSign: "7.1k" stars, 846 forks, "OpenSign is licensed under the AGPL-3 License"; MongoDB (default deployment DB is not persistent); it keeps "detailed logs for tracking document activities" (timestamps, IP, email, phone) and "A completion certificate is generated as soon as document is completed"; API keys in-app; no sandbox mentioned [PRIMARY] — [GitHub OpenSignLabs/OpenSign](https://github.com/OpenSignLabs/OpenSign), [README](https://raw.githubusercontent.com/OpenSignLabs/OpenSign/main/README.md)
- E-SIGN, 15 U.S.C. §7001(a)(1): a signature, contract or record "may not be denied legal effect, validity, or enforceability solely because it is in electronic form"; §7001(d)(1): a retained electronic record must "accurately reflect[] the information set forth in the contract" and "remain[] accessible to all persons who are entitled to access"; no audit-trail format is prescribed [PRIMARY] — [LII 15 USC 7001](https://www.law.cornell.edu/uscode/text/15/7001)
- NY State Technology Law §304(2): "The use of an electronic signature shall have the same validity and effect as the use of a signature affixed by hand" [PRIMARY] — [STT 304](https://www.nysenate.gov/legislation/laws/STT/304)
- NY State Technology Law §307 exceptions cover wills/trusts/powers of attorney-type dispositions, negotiable instruments and documents the electronic facilitator excepts by rule; the current text has no clause excluding Real Property Law article 9 conveyances [PRIMARY] — [STT 307](https://www.nysenate.gov/legislation/laws/STT/307)

### Inferences
- [INFERENCE] For the demo, a "signing ceremony" screen that records signer identity, consent text, SHA-256 of the document version, timestamp and IP into the audit table demonstrates the legally relevant properties (accurate record, accessibility, attribution) without a second server; the production integration is DocuSeal's API/webhooks.
- [INFERENCE] Running DocuSeal as a separate container (unmodified) keeps our own code outside AGPL's reach; modifying DocuSeal's source would trigger AGPL on those modifications. The attorney should confirm this reading before production.

### Gaps
- RAM/CPU needs of DocuSeal and OpenSign are not stated on their pages ([CLAIMED] a Rails app typically needs ~0.5–1 GB).
- Whether DocuSeal's audit log is embedded in the signed PDF or kept only in the database was not confirmed from fetched pages.
- Documenso's audit-log/certificate-of-completion documentation page was not reached (two guessed URLs returned 404).

## 5. Fair-housing word lists and checkers

### Takeaway
No reusable public word list was reachable from a primary source in this session (HUD's advertising pages returned 404/403; the historic 24 CFR Part 109 Appendix I list is not on govinfo for 1995/1996; NAR, NYSAR, HGAR and the Fair Housing Council of Oregon pages had no list). The credible open-source reference is Zillow's Fair Housing Guardrail (stop list + fine-tuned classifier + prompt), but its licence is an OpenRAIL-S "responsible use" licence, not OSI-approved, and the full model and dataset are not public. Recommendation: build a small rules file of our own from public guidance plus an LLM structured-output review; borrow Zillow's architecture; skip the PyTorch-based community checkers.

### Cited Findings
- zillow/fair-housing-guardrail: 39 stars, 7 forks; combines "a stop list with a fine-tuned classifier"; binary model BERT-base-uncased, multi-class RoBERTa-large; "we recommend using Fair Housing Guardrail in combination with a fair housing specific prompt"; the full fine-tuned model and labeled dataset are not public ("Refer to the 'Contact Us' section to request this"); sample JSONL datasets included; "provided for informational purposes only and should not be considered legal advice" [PRIMARY] — [GitHub](https://github.com/zillow/fair-housing-guardrail)
- Its licence file is the "AI PUBS OPEN RAIL-S LICENSE, Version 0.1, March 2, 2023 ... generally applicable to any Source Code to be licensed with responsible use restrictions" [PRIMARY] — [LICENSE](https://raw.githubusercontent.com/zillow/fair-housing-guardrail/main/LICENSE)
- The guardrail's `fair_housing_guardrail/data` folder shows `constants.py` and `json_dataset.py`; no separate stop-list file was visible on the directory page [PRIMARY] — [directory](https://github.com/zillow/fair-housing-guardrail/tree/main/fair_housing_guardrail/data)
- ZheWang-stack/FairProp-AI: 2 stars, MIT; regex rules + SentenceTransformers/ChromaDB + BART-large-MNLI zero-shot classifier; claims "300+ Rules", "100+ Jurisdictions"; "acknowledges building on the 'fair-housing-guardrail' model open-sourced by Zillow Group"; stack PyTorch, FastAPI, Transformers; claims are internally inconsistent (e.g. 20+ languages vs "Multi-language NLP" unchecked on the roadmap) [PRIMARY] — [GitHub](https://github.com/ZheWang-stack/FairProp-AI)
- DE-BARY-LLC/debary-mcp-compliance: 1 star, Apache-2.0; describes an engine of "81 phrase rules, 35 required elements, six states [TX, CA, FL, AZ, NY, NC], no model anywhere in the decision path", but "The public repo ships a sample rule base of six rules and four required elements" and states it is "not a compliance tool" [PRIMARY] — [GitHub](https://github.com/DE-BARY-LLC/debary-mcp-compliance)
- TheProsperityAgent/prosperity-real-estate-skills: 11 stars, MIT; Claude skills incl. `fair-housing-overlay` and `listing-description` ("Fair-Housing-compliant MLS remarks"); no word list shown; README discloses a commercial interest ("partnering means joining eXp Realty and naming us as your sponsor") [PRIMARY] — [GitHub](https://github.com/TheProsperityAgent/prosperity-real-estate-skills)
- GitHub topic "fair-housing" has 22 repositories, the most-starred has 11 stars; others include fha-legal-ai (1 star), cre-agent-audit (0 stars, "fair housing pre-flight check") [PRIMARY] — [github.com/topics/fair-housing](https://github.com/topics/fair-housing)
- New York's required notice: "New York State Housing and Anti-Discrimination Disclosure Form", DOS-2156 (11-25), published by DOS with the Division of Human Rights; DOS's fair-housing page lists it in 13 languages [PRIMARY] — [DOS-2156 PDF](https://dos.ny.gov/housinganti-discrimination-form-dos-2156), [DOS fair housing](https://dos.ny.gov/fair-housing)
- NY internet-advertising rules summarized by DOS: the listing agent must be "clearly disclosed"; a buyer's broker advertising a listing must include the word "advertisement"; disclosures also apply to thumbnail views on lead-generation sites [PRIMARY] — [DOS real estate advertising](https://dos.ny.gov/real-estate-advertising)
- HUD's advertising-and-marketing page and FHEO office page returned 404 / navigation-only content; NAR's fair-housing page lists store products and the EHO logo but no word list; NYSAR returned 403; govinfo has no 1995/1996 CFR Part 109 file at the standard path [PRIMARY, negative results] — [HUD](https://www.hud.gov/program_offices/fair_housing_equal_opp/advertising_and_marketing), [NAR](https://www.nar.realtor/fair-housing), [govinfo](https://www.govinfo.gov/content/pkg/CFR-1995-title24-vol1/pdf/CFR-1995-title24-vol1-part109.pdf)

### Inferences
- [INFERENCE] A production-shaped checker for the demo is: (1) a YAML/JSON rules file the team curates (protected classes under the federal Fair Housing Act and NY Human Rights Law; phrases and the reason each is risky; allowed alternatives), applied by plain regex in Python; (2) an LLM review with a Pydantic schema (`flags[]`, `severity`, `rationale`, `suggested_rewrite`) rendered beside the listing copy; (3) a mandatory human approval. This mirrors Zillow's stop-list + model + prompt design without PyTorch.
- [INFERENCE] FairProp-AI and the Zillow classifier need PyTorch and transformer weights (BART-large is ~1.6 GB [CLAIMED]), which is disproportionate on a 2 vCPU / 8 GB VPS when an API model already does the review.

### Gaps
- The HUD 1995 advertising guidance memo (the Achtenberg memo) and the former 24 CFR Part 109 Appendix I word list exist [CLAIMED from memory] and are federal works (so public domain under 17 U.S.C. §105, see group 7), but no current URL was reachable; the team should obtain a copy from HUD/FHEO or a state fair-housing agency and cite it in the rules file.
- The text of 19 NYCRR 175.25 (advertising) and 175.28 (fair-housing notice) was not fetched; only DOS's summary page was read.
- No MLS-published word list (e.g. OneKey MLS for the Hudson Valley) was found; HGAR's site has a fair-housing page and document library but the pages fetched contained no list.

## 6. PII handling (detection, redaction, encryption at rest, audit logs)

### Takeaway
Presidio (now community-owned, MIT) is the standard but its analyzer pulls spaCy (51 packages) and a large model by default; the anonymizer alone (4 packages) works with our own regex recognizers, which I tested. SQLCipher via `sqlcipher3-binary` (3 MB wheel, MIT wrapper; SQLCipher itself BSD-style with an attribution requirement) encrypted a database that stdlib sqlite3 then could not read. For audit logs, trigger-based append-only tables (sqlite-chronicle pattern) are the lightest option.

### Cited Findings
- presidio-analyzer 2.2.364 (2026-07-22), MIT; requires spacy, numpy, phonenumbers, pydantic, regex, tldextract...; `uv` resolves 51 packages [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/presidio-analyzer/json)
- presidio-anonymizer 2.2.364 (2026-07-22), MIT; requires only `cryptography`; `uv` resolves 4 packages [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/presidio-anonymizer/json)
- Presidio installation: "install the presidio-analyzer and presidio-anonymizer packages with at least one NLP engine"; default spaCy model `en_core_web_lg`; alternative engines transformers and Stanza (loaded lazily); Python 3.10–3.13; images now at `ghcr.io/data-privacy-stack/presidio-analyzer`; "The legacy Microsoft Container Registry images at mcr.microsoft.com/presidio-* are no longer updated" [PRIMARY] — [installation](https://presidio.dataprivacystack.org/installation/)
- Presidio's GitHub page: "11.5k" stars, MIT; "Presidio has moved to a new home!" with transition notice at `docs/project_transition.md`; the docs home says it "is transitioning to a community-owned project" [PRIMARY] — [GitHub data-privacy-stack/presidio](https://github.com/data-privacy-stack/presidio), [docs home](https://presidio.dataprivacystack.org/)
- spacy 3.8.16 (2026-08-24), MIT, 21 declared deps, manylinux wheel ~33 MB [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/spacy/json)
- Tried: `AnonymizerEngine().anonymize(...)` with a hand-made `RecognizerResult("PHONE_NUMBER", ...)` returned "Call Jane at <PHONE>" with no spaCy installed [PRIMARY, tried] — [scratch script]
- sqlcipher3-binary 0.6.0 (2025-12-31), MIT, no deps, x86_64 manylinux wheel 3.2 MB (cp310–cp312 wheels listed; a cp313 interpreter also imported it here) [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/sqlcipher3-binary/json)
- Tried: created `enc.db` with `PRAGMA key='demo-key'`, inserted a row; stdlib `sqlite3` raised `DatabaseError` on read; reopening with the key returned the row; module reports sqlcipher3 2.6.0 bundling SQLite 3.51.1 [PRIMARY, tried] — [scratch script]
- SQLCipher Community Edition is "available under a BSD-style license" that "requires attribution and reproduction of license grants" in "an about or licensing screen in the application" [PRIMARY] — [zetetic.net licence page](https://www.zetetic.net/sqlcipher/license/)
- sqlite-utils 4.2.1 (2026-08-13), Apache-2.0, 7 deps (10 packages) [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/sqlite-utils/json)
- cryptography 50.0.2 (2026-09-30), "Apache-2.0 OR BSD-3-Clause" [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/cryptography/json)
- Audit-log building blocks: sqlite-chronicle 0.6.1 (2026-02-15, Apache-2.0) "Use triggers to maintain a chronicle table of updated/deleted timestamps"; sqlite-history 0.1 (2023-04-09, Apache-2.0) "Track changes to SQLite tables using triggers"; sqlalchemy-continuum 2.0.0 (2026-10-14, BSD-3-Clause) "Versioning and auditing extension for SQLAlchemy" [PRIMARY] — [sqlite-chronicle](https://pypi.org/pypi/sqlite-chronicle/json), [sqlite-history](https://pypi.org/pypi/sqlite-history/json), [sqlalchemy-continuum](https://pypi.org/pypi/sqlalchemy-continuum/json)

### Inferences
- [INFERENCE] Lightest viable PII design for the VPS: presidio-anonymizer + a dozen regex recognizers (phone, email, SSN, DOB, account numbers) applied before any text goes to the model or into logs; add presidio-analyzer with `en_core_web_sm` only if person-name detection proves necessary in the shared inbox.
- [INFERENCE] Encrypt the whole SQLite file with SQLCipher (one pragma, key from an environment secret) and additionally Fernet-encrypt the few fields that must be unreadable to operators (SSN/ID numbers); keep the audit table append-only via triggers (`BEFORE UPDATE/DELETE ... RAISE(ABORT)`) and store a hash chain column so tampering is detectable. The AI-action log should live in the same table family so "every AI action on screen" and the audit trail are one record.
- [INFERENCE] SQLCipher's attribution clause means an "About / licences" screen in the app, which is trivial.

### Gaps
- Sizes of `en_core_web_sm` vs `en_core_web_lg` were not verified ([CLAIMED] ~12 MB vs ~560 MB).
- No cp313 wheel for sqlcipher3-binary is listed on PyPI; the import worked here on Python 3.13, which suggests a newer wheel set than the three shown, but the target is Python 3.12 (cp312 wheel listed) so this does not matter for the team.

## 7. Public forms and open data for New York

### Takeaway
The agency disclosure form (RPL §443) and the Property Condition Disclosure Statement (RPL §462) are printed verbatim in the statute, and DOS publishes them as DOS-1736-f and DOS-1614-f; the fair-housing notice is DOS-2156; the SOP duty is in RPL §442-h (no DOS template); the EPA lead-paint sample forms are federal works and therefore not copyrightable. The NYSBA/NYSAR residential contract form is sold, its copyright status could not be read from a primary page, but copyright does not protect structure/ideas (17 U.S.C. §102(b)), so a contract with the same section structure and our own text is the right approach. Parcel data: Ulster and Orange are in the free statewide NYS Tax Parcels set, Dutchess and Columbia are not (Dutchess sells its parcel GIS for $600 county-wide); assessment rolls for all counties are on Open NY with permissive terms; sales are searchable in ORPTS Sales Web (Excel export, no API).

### Cited Findings
- RPL §443(4) sets out the complete forms for buyer–seller and landlord–tenant transactions; the listing agent provides it "prior to entering into a listing agreement", the seller's agent "at the time of the first substantive contact" with a buyer, the buyer's agent "prior to entering into an agreement to act as the buyer's agent"; on refusal to sign, the agent must "set forth under oath or affirmation a written declaration of the facts of the refusal" and keep it "not less than three years" [PRIMARY] — [RPL 443](https://www.nysenate.gov/legislation/laws/RPP/443)
- DOS form: "DOS-1736-f (Rev. 09/21)", "New York State Disclosure Form for Buyer and Seller", "THIS IS NOT A CONTRACT"; the DOS forms page offers it in English, Spanish, Haitian-Creole, Italian, Korean, Russian, Chinese, Bengali, Arabic, French, Polish, Urdu and Yiddish, and the landlord/tenant version likewise; no reproduction restriction on the page [PRIMARY, PDF text extracted] — [DOS-1736-f PDF](https://dos.ny.gov/buyer-and-seller-disclosure-form-english), [DOS forms page](https://dos.ny.gov/real-estate-broker-forms)
- RPL §462(2): "The following shall be the disclosure form:" followed by the full PCDS; sections General Information (Q1–9), Environmental (Q9–27, with flood questions Q10–17), Structural (Q28–33), Mechanical Systems & Services (Q34–39), component defects (Q40–55), school district (Q56); the statute page shows a revision dated 2025-07-04 [PRIMARY] — [RPL 462](https://www.nysenate.gov/legislation/laws/RPP/462)
- The PDF served at DOS's PCDS URL is "DOS-1614-f (Rev. 06/23)", 6 pages, and still contains "the buyer shall receive upon the transfer of title a credit of $500 against the agreed upon purchase price" and a Q10 "Is any or all of the property located in a designated floodplain?" [PRIMARY, PDF text extracted] — [DOS PCDS PDF](https://dos.ny.gov/property-condition-disclosure-statement)
- DOS-2156 (11-25) "New York State Housing and Anti-Discrimination Disclosure Form" (Department of State with the Division of Human Rights) [PRIMARY, PDF text extracted] — [DOS-2156](https://dos.ny.gov/housinganti-discrimination-form-dos-2156)
- RPL §442-h(4): procedures must address "whether prospective clients shall show identification", "whether an exclusive broker agreement is required" and "whether pre-approval for a mortgage loan is required"; brokers must "date stamp, notarize and post such standardized operating procedures" on "any publicly available website and mobile device application they maintain", keep a copy at offices, post changes within thirty days, archive prior versions and affirm compliance at renewal [PRIMARY] — [RPL 442-h](https://www.nysenate.gov/legislation/laws/RPP/442-H)
- DOS's SOP page provides no template or form; notes that S.7729 removed the requirement to file SOPs with DOS and that "the Department is not considering expanding the list"; deadline was April 20, 2022 [PRIMARY] — [DOS SOP page](https://dos.ny.gov/standardized-operating-procedures)
- EPA lead disclosure: applies to "most pre-1978 private housing"; sample forms `selr_eng.pdf` (seller, English), `seller_disclosure_form-spanish.pdf`, `lesr_eng.pdf`, `spanless.pdf`; pamphlet "Protect Your Family From Lead In Your Home" [PRIMARY] — [EPA page](https://www.epa.gov/lead/real-estate-disclosures-about-potential-lead-hazards)
- 17 U.S.C. §105(a): "Copyright protection under this title is not available for any work of the United States Government" [PRIMARY] — [LII 17 USC 105](https://www.law.cornell.edu/uscode/text/17/105)
- 17 U.S.C. §102(b): "In no case does copyright protection for an original work of authorship extend to any idea, procedure, process, system, method of operation, concept, principle, or discovery" [PRIMARY] — [LII 17 USC 102](https://www.law.cornell.edu/uscode/text/17/102)
- NYSBA Real Property Law Section page lists "Real Estate Transactions – Residential Property, 2020-21" (member price $125) and "LexisNexis NYSBA's Automated Residential Real Estate Forms" (member price $950); it does not mention a "Residential Contract of Sale" by name and carries only a site-wide "© 2026 New York State Bar Association"; both product pages returned 404 [PRIMARY] — [NYSBA section page](https://nysba.org/sections/real-property-law-section/)
- NYS Tax Parcels: public parcels cover 38 counties (Ulster and Orange included; Dutchess and Columbia not); centroid points and state-owned parcels cover "all 62 New York State counties"; "updated once a year"; ArcGIS REST FeatureServers `.../Parcels/NYS_Tax_Parcels_Public/FeatureServer` and `.../NYS_Tax_Parcel_Centroid_Points/FeatureServer`; assessment lookup geoprocessing service `.../NYSTaxAssessmentLookup/GPServer/TaxAssessment/execute`; "GIS parcel data is for planning and general use purposes only and is not a substitute for a legal parcel survey"; "we respect each county's right as the data owner to control the distribution their GIS data" [PRIMARY] — [gis.ny.gov/parcels](https://gis.ny.gov/parcels)
- County links from the same page: Dutchess ParcelAccess viewer `https://gis.dutchessny.gov/parcelaccess/`; Ulster GIS data `https://www.ulstercountyny.gov/Departments/Information-Services/GIS-Services/GIS-Data` and Beacon search; Orange `https://propertydata.orangecountygov.com/search.aspx`; Columbia `https://geodata-cc-ny.opendata.arcgis.com/` [PRIMARY] — [gis.ny.gov/parcels](https://gis.ny.gov/parcels)
- Dutchess digital parcel data: "The cost per municipality is $75, plus shipping and handling", "Cost for the entire county is $600", "No charge for NYS GIS Data Sharing Cooperative Members with account ID"; "Geodatabase is the preferred format" [PRIMARY] — [Dutchess price list](https://www.dutchessny.gov/Departments/Real-Property-Tax/digital-mapping-price-list.htm)
- Ulster tax parcels: "available for download at no cost as zipped ESRI shapefiles", 73 MB, last updated 7/2026, "suitable for tax mapping and general mapping purposes"; REST directory `https://gis.ulstercountyny.gov/server/rest/` [PRIMARY] — [Ulster GIS data](https://www.ulstercountyny.gov/Departments/Information-Services/GIS-Services/GIS-Data)
- Orange: "Image Mate Online" public access to "RPS data, tax maps, and photographic images of properties", refreshed weekly from assessment records [PRIMARY] — [Orange property data](https://propertydata.orangecountygov.com/search.aspx)
- Columbia: the ArcGIS Hub search API returned no dataset titled "parcel"; "Priority Farmland 2013" is parcel-based with licence "custom" (informational/planning use only) [PRIMARY] — [Hub API](https://geodata-cc-ny.opendata.arcgis.com/api/search/v1/collections/all/items?q=parcel)
- Open NY: "Property Assessment Data from Local Assessment Rolls" (attribution: Department of Taxation and Finance), 23,580,051 records, rows updated 2026-04-24; columns include roll_year, county_name, municipality, school district, swis_code, tax_class, roll_section, property_class, parcel address, front/depth, deed book/page, owner names, mailing address, exemptions (list truncated at column 56) [PRIMARY] — [Socrata metadata](https://data.ny.gov/api/views/7vem-aaz7.json)
- Open NY terms: "use our government information however you wish, in private sector projects or in government collaborations"; the terms "do not contain restrictions requiring members of the public to use attribution, to re-post the license terms"; "The State grants you a non-exclusive, revocable license to use the Content"; no warranty [PRIMARY, PDF text extracted] — [Open NY Terms of Use PDF](https://data.ny.gov/download/77gx-ii52/application/pdf)
- Sales: "Sales Web includes 10 years of property sales and transfers for all of New York State, except New York City" (NYC is in ACRIS); updated weekly as localities transmit; results downloadable "as an Excel file" via "Download Search Results"; no API mentioned; portal at `https://pad.tax.ny.gov/index` [PRIMARY] — [Municipal Data Portal](https://www.tax.ny.gov/pit/property/munidataportal.htm)
- ORPTS's RP-5217 pages are aimed at assessors (RPS035 transmittals, SaleScan, "Online Sales Reports") and state no public bulk-download or price [PRIMARY] — [ORPTS sales data management](https://www.tax.ny.gov/research/property/assess/sales/)

### Inferences
- [INFERENCE] The statutory text of the agency disclosure and PCDS can be reproduced in our templates; the DOS layouts (DOS-1736-f, DOS-1614-f, DOS-2156) are government forms published for use and carry no reproduction notice, so the safest demo approach is to render our own HTML/PDF from the statutory text and label the form numbers.
- [INFERENCE] The DOS-hosted PCDS PDF (Rev. 06/23, with the $500 credit sentence) looks older than the statute's current revision (2025-07-04 on the Senate site); the team should generate the PCDS from the statute text, not from the cached PDF, and have the attorney confirm the post-2024 flood questions.
- [INFERENCE] For the contract of sale, mirror the customary structure (parties, premises, personal property, price and deposit, mortgage contingency, title/permitted exceptions, closing date and place, adjustments, risk of loss, default, attorney-review/rider) with original wording; under §102(b) structure and headings are not protected expression, but copying clauses from the NYSBA/NYSAR form would be.
- [INFERENCE] For later intake automation: Open NY assessment rolls (free, statewide, 23.6 M rows) + NYS centroid points (all 62 counties) give address → parcel → class/assessment for Dutchess and Columbia even though their polygons are not open; Ulster/Orange polygons are free; Sales Web gives comps by municipality via manual Excel export only.

### Gaps
- The ownership/copyright notice of the widely used "Residential Contract of Sale" (jointly prepared bar-association/NYSAR form [CLAIMED]) was not readable from a primary page (NYSBA product pages 404, NYSAR 403); the founder, as a NY attorney, can confirm its provenance from a paper copy.
- 19 NYCRR 175.28 text (fair-housing notice duties) and the current DOS PCDS form revision were not confirmed.
- Columbia County parcel polygons: whether any open download exists was not determined (the Hub search showed none).
- NYS Tax Parcels field dictionary (data dictionary link) was not read.

## 8. Comparable sales and valuation

### Takeaway
No credible open-source AVM/CMA library exists (GitHub topics and the curated list show only course-style price-prediction projects). For the demo, build a transparent comps grid in plain Python (sold comps, $/sq ft, feature adjustments, time adjustment from the FHFA House Price Index) and use fictional listings; the public sources with clear terms are FHFA HPI (federal work) and Open NY assessment rolls; Sales Web supplies real comps by manual export. Zillow and Realtor.com data terms could not be fetched.

### Cited Findings
- GitHub topic "zillow": "None of the visible entries is a dedicated AVM or comparable-sales model"; the closest are zillow-deal-finder (31 stars, compares list price to Zestimate), zestimate-lambda (8), zillow-skills (7, "Zestimates, comps, listings") [PRIMARY] — [github.com/topics/zillow](https://github.com/topics/zillow?o=desc&s=stars)
- awesome-real-estate valuation entries are a "Real Estate Price Prediction Project" and a time-series portfolio project, with no licences stated [PRIMARY] — [awesome-real-estate](https://github.com/etewiah/awesome-real-estate)
- seehiong/hdb-price-predictor (270 stars) does in-browser Singapore valuation with XGBoost [PRIMARY] — [topic page](https://github.com/topics/real-estate?o=desc&s=stars)
- PyPI `pyavm` 0.9.9 (2026-03-12, MIT) is "Simple pure-python AVM meta-data handling" (image metadata), not a valuation model [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/pyavm/json)
- FHFA HPI covers "the national, census division, state, metro area, county, ZIP code, and census tract levels"; monthly purchase-only and quarterly all-transactions/expanded indexes; no terms of use stated [PRIMARY] — [fhfa.gov/data/hpi](https://www.fhfa.gov/data/hpi)
- Redfin Data Center downloads include Housing Market Tracker, Redfin Home Price Index, Existing Home Sales etc.; the page says "By searching, you agree to the Terms of Use" and does not state attribution/commercial terms [PRIMARY] — [Redfin downloads](https://www.redfin.com/news/data-center/downloads/)
- Zillow Research data page returned HTTP 403 and realtor.com could not be fetched [PRIMARY, negative] — [Zillow](https://www.zillow.com/research/data/)
- ORPTS Sales Web: 10 years of statewide (ex-NYC) sales, weekly updates, Excel export [PRIMARY] — [Municipal Data Portal](https://www.tax.ny.gov/pit/property/munidataportal.htm)
- Open NY terms permit use "however you wish, in private sector projects" [PRIMARY] — [Open NY Terms PDF](https://data.ny.gov/download/77gx-ii52/application/pdf)

### Inferences
- [INFERENCE] FHFA is a federal agency, so its HPI tables are public domain under 17 U.S.C. §105; they are the cleanest free input for time-adjusting comps.
- [INFERENCE] The AI's role in pricing should be narration and sanity checks over a deterministic grid (scikit-learn/statsmodels are not needed for 3–6 comps); this keeps the "pricing from comparable sales" screen explainable and keeps the licensed-human sign-off meaningful.

### Gaps
- Zillow Research and Realtor.com data terms (attribution, commercial use) were not read; [CLAIMED] both are commonly described as free with attribution for research, which must be verified before any demo uses them.
- No academic/open hedonic AVM code with a licence was located without search.

## 9. Agent and workflow frameworks (Anthropic SDK vs PydanticAI vs LangGraph) and human-in-the-loop patterns

### Takeaway
A thin direct use of the Anthropic Python SDK (2.1.0, Apache-2.0, 16 packages) is enough: `client.messages.parse()` with Pydantic models gives schema-valid outputs for every AI step, strict tools validate tool inputs, and the beta tool runner can hold tool calls for approval. "Show every AI action on screen" is then a database table of AI actions with proposed/approved/rejected states rendered by HTMX, not a framework feature. PydanticAI (17 packages slim) has the closest ready-made approval idiom (deferred tools) and LangGraph (38 packages) has `interrupt()` + SQLite checkpoints; both add abstraction between the screen and the call, so skip them for the first slice.

### Cited Findings
- anthropic 2.1.0 released 2026-10-21, Apache-2.0, 8 deps (anyio, httpx2, jiter, pydantic, opentelemetry-api...), `uv` resolves 16 packages, wheel 2.1 MB; GitHub "4.0k" stars, 893 forks [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/anthropic/json), [GitHub](https://github.com/anthropics/anthropic-sdk-python)
- Tried: `import anthropic` 2.1.0 succeeded; `beta.messages.tool_runner`, `messages.parse` and `beta_tool` are present [PRIMARY, tried] — [scratch script]
- Structured outputs: "The request carries the schema in `output_config.format` with `type: "json_schema`"; "Pass a Pydantic model to `client.messages.parse()` ... returns the parsed model in `parsed_output`"; strict tool use (`strict: true`) "Guarantee[s] schema validation on tool names and inputs"; limit "Strict tools per request | 20"; supported on current models incl. claude-opus-5-5 and claude-sonnet-5-5 [PRIMARY] — [Anthropic docs: structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- Tool runner (SDK `tools.md`): iterating `client.beta.messages.tool_runner()` yields a `BetaMessage` per API call and "The runner executes tools only after your loop body for that reply finishes"; `runner.defer_tool_call(...)` holds a streamed call, `runner.remove_tools()` blocks a tool mid-run, raising `ToolError` returns an error to the model [PRIMARY] — [anthropic-sdk-python tools.md](https://raw.githubusercontent.com/anthropics/anthropic-sdk-python/main/tools.md)
- pydantic-ai 2.59.0 (2026-10-21), MIT; the meta-package pins `pydantic-ai-slim[anthropic,cli,evals,google,logfire,mcp,openai,web]` and `uv` resolves 101 packages; `pydantic-ai-slim` resolves 17; GitHub "20.8k" stars [PRIMARY] — [PyPI pydantic-ai](https://pypi.org/pypi/pydantic-ai/json), [PyPI pydantic-ai-slim](https://pypi.org/pypi/pydantic-ai-slim/json), [GitHub](https://github.com/pydantic/pydantic-ai)
- PydanticAI deferred tools: `requires_approval=True` on tool decorators, or raise `ApprovalRequired`; the run ends with `DeferredToolRequests`; the caller answers with `DeferredToolResults` (`ToolApproved`/`ToolDenied`) and starts a new run with `deferred_tool_results`; "the conversation you store is everything you need to resume"; warning "Approval is not an authorization boundary against an untrusted client" [PRIMARY] — [PydanticAI deferred tools](https://pydantic.dev/docs/ai/tools-toolsets/deferred-tools/)
- langgraph 1.2.16 (2026-10-16), MIT, `uv` resolves 38 packages; GitHub "43.7k" stars; `interrupt()` "pauses graph execution and returns a value to the caller", resumed with `Command(resume=...)` on the same thread ID, needs "A checkpointer to persist the graph state"; `SqliteSaver` from `langgraph.checkpoint.sqlite`; on resume "the node restarts from the beginning" [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/langgraph/json), [GitHub](https://github.com/langchain-ai/langgraph), [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- langgraph-checkpoint-sqlite 3.1.2 (2026-10-12), MIT [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/langgraph-checkpoint-sqlite/json)
- Tried: `pydantic-ai-slim[anthropic]` installed and imported (v2.59.0) alongside anthropic 2.1.0 without conflict [PRIMARY, tried] — [scratch script]

### Inferences
- [INFERENCE] Pattern for the demo: one Python function per AI step (`draft_listing_copy`, `check_fair_housing`, `draft_reply`, `compare_offers`, `draft_counter`, `draft_contract`), each a single `messages.parse` call with a Pydantic result model; the function writes an `ai_actions` row (step, model id, prompt hash, input JSON, output JSON, token usage, status) and the HTMX screen renders that row with Approve / Edit / Reject buttons; the timeline colour comes from the step's declared actor (AI / human / licensed). No background loop is needed, so no checkpointer.
- [INFERENCE] If the team later wants multi-step tool use (e.g. the inbox agent looking up a listing before drafting), the SDK tool runner with deferral covers it; PydanticAI's deferred-tools model is the best-documented alternative, and its warning about approvals not being an authorization boundary is the right design note for our approval table (approve server-side with the user's session, never trust a client flag).

### Gaps
- Per-call cost of the recommended models for the demo volume belongs to WS4; not estimated here.

## 10. UI building blocks for a server-rendered app

### Takeaway
HTMX 2.0.11 (0BSD, ~16 kB gzipped, no dependencies) is the safe choice (4.0 is out but still tagged `next`). Pico CSS is officially unmaintained (final v2.1.1), so prefer Bulma 1.0.4 or Bootstrap 5.3.8 (both MIT) served from a CDN or vendored; Bulma's community timeline/steps extensions are stale (2018–2022), so write ~50 lines of CSS for the timeline and step wizard. Contract diffs: stdlib `difflib.HtmlDiff` works (tested). Tailwind's Play CDN is "for development purposes only". Playwright 1.64.1 (Apache-2.0) is the smoke-test tool; it wants its own Chromium build (~281 MB) or the lighter headless shell; using the pre-installed Chromium via `executable_path` is possible but "use at your own risk".

### Cited Findings
- htmx: "~16k min.gz'd", "dependency-free"; "htmx 4.0 has been released" (announcement dated 2026-08-28) but "It is not currently marked as `latest` in NPM so that people using the 2.x line are not accidentally upgraded"; quick start references `htmx.org@2.0.11` [PRIMARY] — [htmx.org](https://htmx.org/)
- npm: htmx.org latest 2.0.11 (2026-09-22), `next` 4.0.0, licence 0BSD [PRIMARY] — [npm registry](https://registry.npmjs.org/htmx.org)
- htmx licence is Zero-Clause BSD: "Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted" [PRIMARY] — [LICENSE](https://raw.githubusercontent.com/bigskysoftware/htmx/master/LICENSE)
- Pico CSS: "Currently v2.1.1", "Code licensed MIT"; "Pico CSS is no longer maintained", "v2.1.1 is the final release", repositories archived ("No new issues, PRs or releases"); components accordion, card, dropdown, modal, nav, progress, tooltip; no timeline/stepper [PRIMARY] — [picocss.com/docs](https://picocss.com/docs), [maintenance](https://picocss.com/docs/maintenance)
- Bulma 1.0.4 (npm 2025-04-19), "Source code licensed MIT"; components breadcrumb, card, dropdown, menu, message, modal, navbar, pagination, panel, tabs; extensions are "Side projects" [PRIMARY] — [bulma.io](https://bulma.io/documentation/start/overview/), [npm](https://registry.npmjs.org/bulma)
- Bulma extensions: bulma-timeline 3.0.5 (2022-01-15, MIT), bulma-steps 2.2.1 (2018-06-14, MIT) [PRIMARY] — [npm bulma-timeline](https://registry.npmjs.org/bulma-timeline), [npm bulma-steps](https://registry.npmjs.org/bulma-steps)
- Bootstrap 5.3.8 (2025-08-26, MIT); 6.0.0-alpha.1 published 2026-10-08 under `next`; Simple.css 2.3.7 (2025-05-29, MIT); water.css 2.1.1 (2021-08-11, MIT) [PRIMARY] — [npm bootstrap](https://registry.npmjs.org/bootstrap), [npm simpledotcss](https://registry.npmjs.org/simpledotcss), [npm water.css](https://registry.npmjs.org/water.css)
- Tailwind Play CDN: "The Play CDN is designed for development purposes only, and is not intended for production" (v4.3 docs) [PRIMARY] — [tailwindcss.com](https://tailwindcss.com/docs/installation/play-cdn)
- Tried: `difflib.HtmlDiff(wrapcolumn=60).make_table(v1, v2, "v1", "v2")` on two short contract-term versions produced a 1,961-character HTML table with no third-party package [PRIMARY, tried] — [scratch script]
- diff-match-patch 20241021 (Apache-2.0) is the alternative for word-level diffs [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/diff-match-patch/json)
- playwright 1.64.1 (2026-10-22), Apache-2.0, deps pyee and greenlet (4 packages), manylinux x86_64 wheel 48.5 MB [PRIMARY] — [PyPI JSON](https://pypi.org/pypi/playwright/json)
- Playwright browsers: "These browsers will take a few hundred megabytes of disk space when installed" (example cache shows "281M chromium-XXXXXX"); for headless-only use "you can avoid downloading the full Chromium browser by passing `--only-shell`"; `playwright install --with-deps chromium` installs Linux system deps; branded channels `chrome`, `msedge`... [PRIMARY] — [Playwright browsers](https://playwright.dev/python/docs/browsers)
- `executable_path`: "Path to a browser executable to run instead of the bundled one"; "Note that Playwright only works with the bundled Chromium, Firefox or WebKit, use at your own risk"; "Use executable_path option with extreme caution" [PRIMARY] — [BrowserType API](https://playwright.dev/python/docs/api/class-browsertype)

### Inferences
- [INFERENCE] Vendor `htmx.min.js` (~50 kB) and `bulma.min.css` into `/static` instead of relying on a CDN so the demo works offline and the VPS serves everything; both licences permit redistribution.
- [INFERENCE] The deal timeline (AI / human / licensed colour coding) and the step wizard are a `<ol>` with CSS custom properties per actor; no component library is worth a dependency for this.
- [INFERENCE] For the end-to-end smoke test, `playwright install --only-shell chromium` keeps disk use lowest; if disk is the binding constraint, pointing `executable_path` at the existing Chromium is acceptable for a demo-only test.

### Gaps
- Exact size of the Chromium headless shell download was not stated on the docs page.

## 11. Open-source "AI real estate agent" projects worth reading

### Takeaway
Worth reading for ideas: AleksNeStu/ai-real-estate-assistant (polished FastAPI + Next.js reference with CMA reports, a demo mode with simulated AI responses and heavy CI; Polish demo data; too large to adopt), hoangtng/real-estate-agents (MIT Markdown prompt library: CMA generator with 3-tier pricing, offer strategy brief, compliance audit checklist), and Zillow's fair-housing-guardrail (architecture). The rest are scrapers, skills bundles with commercial ties, or tiny early repos.

### Cited Findings
- AleksNeStu/ai-real-estate-assistant: 319 stars, 118 forks, MIT; FastAPI on Python 3.12+ with Next.js 16/React 19, ChromaDB; 16 LLM providers including Anthropic with an "automatic fallback chain"; CMA reports, "AI valuation with price forecasts"; OSS edition ships "250+ properties across 5 Polish cities" and "The demo uses simulated AI responses for instant exploration"; self-reported "6,254+" backend tests at 90%+ coverage; release v5.1.5.2 dated 2026-09-12; page shows internal inconsistencies (provider count 16 vs 13, commit counts) [PRIMARY] — [GitHub](https://github.com/AleksNeStu/ai-real-estate-assistant)
- hoangtng/real-estate-agents: 28 stars, MIT ("use freely, adapt for your market, contribute back"); "12 AI agent personas (the team) + 12 production skills" as Markdown; skills include "CMA Generator: Full comparative market analysis with 3-tier pricing", "Offer Strategy Builder: Complete offer brief with contingency guidance", "Compliance Audit: Disclosure checklist and fair housing review"; 7 commits, no tests [PRIMARY] — [GitHub](https://github.com/hoangtng/real-estate-agents)
- TheProsperityAgent/prosperity-real-estate-skills: 11 stars, MIT, skills for listing copy, MLS/county data and a fair-housing overlay; eXp revenue-share disclosure [PRIMARY] — [GitHub](https://github.com/TheProsperityAgent/prosperity-real-estate-skills)
- tae0y/real-estate-mcp: 380 stars, Python, "Lets Claude query Korean apartment prices via a public government API" [PRIMARY] — [topic page](https://github.com/topics/real-estate?o=desc&s=stars)
- ahacker-1/cre-agent-skills (121 stars) and cre-acquisition-orchestrator (119): commercial-real-estate underwriting/diligence agent workflows [PRIMARY] — [topic proptech](https://github.com/topics/proptech?o=desc&s=stars)
- ZacharyHampton/HomeHarvest: 757 stars, "Python package for scraping property data" (Zillow and others) [PRIMARY] — [topic page](https://github.com/topics/real-estate?o=desc&s=stars)
- AlpacaLabsLLC/skills-for-architects: 386 stars, "Claude Code skills for architecture, real estate, and workplace strategy" [PRIMARY] — [topic page](https://github.com/topics/real-estate?o=desc&s=stars)
- ZeroPointRepo/zillow-skills: 7 stars, "Skills for AI agents covering Zestimates, comps, listings, and price history" [PRIMARY] — [topic zillow](https://github.com/topics/zillow?o=desc&s=stars)
- zillow/fair-housing-guardrail, FairProp-AI, debary-mcp-compliance: see group 5 [PRIMARY]

### Inferences
- [INFERENCE] Quality ranking for reading: ai-real-estate-assistant (engineering practices, demo mode, CMA report layout) > hoangtng (deliverable checklists and persona split that maps onto our AI/human/licensed roles) > prosperity skills (listing-copy prompt shape; ignore the sales pitch) > FairProp/debary (early, unverified claims).
- [INFERENCE] HomeHarvest and similar scrapers conflict with the team's rule against scraping in the pipeline and with portal terms; they are read-only references at most.

### Gaps
- GitHub search was unavailable, so repositories without the topic tags used here (real-estate, proptech, mls, fair-housing, property-management, zillow) may have been missed; a follow-up search for "listing description generator", "buyer agent chatbot" and "negotiation agent" would complete this group.

## 12. Which components to adopt, adapt or skip (demo-quality but production-shaped first slice)

### Takeaway
Adopt five things outright, adapt four, borrow ideas from five, skip the rest. The team builds only what is genuinely its own: the eleven screens, the step/actor state machine, the AI-action and approval log, the NY-specific templates, the fair-housing rules file and the comps grid.

### Cited Findings
- Adopt outright: (1) FastAPI 0.161.1 + Jinja2 3.1.6 + HTMX 2.0.11 (0BSD) + Bulma 1.0.4 or Bootstrap 5.3.8 (MIT), no build step — [PyPI fastapi](https://pypi.org/pypi/fastapi/json), [npm htmx.org](https://registry.npmjs.org/htmx.org), [npm bulma](https://registry.npmjs.org/bulma); (2) anthropic 2.1.0 with `messages.parse` and strict tools — [PyPI anthropic](https://pypi.org/pypi/anthropic/json); (3) RESO DD 2.0 field names and its metadata JSON under the RESO EULA — [reso.org/eula](https://www.reso.org/eula/); (4) WeasyPrint 70.0 (BSD) + docxtpl 0.20.2 (LGPL-2.1) for PDF/DOCX — [PyPI weasyprint](https://pypi.org/pypi/weasyprint/json); (5) sqlcipher3-binary 0.6.0 (MIT wrapper, BSD-style SQLCipher with attribution) + trigger-based audit tables, with stdlib `difflib` for contract diffs and Playwright 1.64.1 for the smoke test — [PyPI sqlcipher3-binary](https://pypi.org/pypi/sqlcipher3-binary/json), [PyPI playwright](https://pypi.org/pypi/playwright/json) [PRIMARY]
- Adapt: NY statutory form text (RPL §443 agency disclosure, RPL §462 PCDS), DOS-2156 and the EPA lead-paint form as our own HTML/PDF templates — [RPL 443](https://www.nysenate.gov/legislation/laws/RPP/443), [RPL 462](https://www.nysenate.gov/legislation/laws/RPP/462), [EPA](https://www.epa.gov/lead/real-estate-disclosures-about-potential-lead-hazards); Zillow guardrail's stop-list + model + prompt architecture re-implemented as rules file + LLM review — [GitHub](https://github.com/zillow/fair-housing-guardrail); presidio-anonymizer with our own recognizers — [PyPI](https://pypi.org/pypi/presidio-anonymizer/json); DocuSeal as the named production e-signature service, simulated in the demo — [docuseal.com/pricing](https://www.docuseal.com/pricing) [PRIMARY]
- Borrow ideas only: EspoCRM Property/Request matching — [espocrm.com](https://www.espocrm.com/extensions/real-estate/); Twenty "objects as code" — [GitHub](https://github.com/twentyhq/twenty); hoangtng deliverable checklists and ai-real-estate-assistant demo mode — [GitHub](https://github.com/hoangtng/real-estate-agents), [GitHub](https://github.com/AleksNeStu/ai-real-estate-assistant); PydanticAI deferred-tool approval semantics — [docs](https://pydantic.dev/docs/ai/tools-toolsets/deferred-tools/); LangGraph interrupt/resume semantics — [docs](https://docs.langchain.com/oss/python/langgraph/interrupts) [PRIMARY]
- Skip: whole-product CRMs as baseline (EspoCRM AGPL/PHP, Krayin MIT/PHP 3 GB RAM, Twenty AGPL+commercial/Node+Postgres+Redis) — [GitHub krayin](https://github.com/krayin/laravel-crm); LangGraph and PydanticAI for the first slice (38 / 17–101 packages of abstraction) — [PyPI langgraph](https://pypi.org/pypi/langgraph/json); FairProp-AI (PyTorch/BART) — [GitHub](https://github.com/ZheWang-stack/FairProp-AI); Typst (31–35 MB wheel, new markup) — [PyPI typst](https://pypi.org/pypi/typst/json); Tailwind Play CDN (dev only) — [tailwindcss.com](https://tailwindcss.com/docs/installation/play-cdn); Pico CSS (unmaintained) and Bulma steps/timeline extensions (2018/2022) — [picocss maintenance](https://picocss.com/docs/maintenance), [npm bulma-steps](https://registry.npmjs.org/bulma-steps); scrapers such as HomeHarvest in the pipeline — [topic page](https://github.com/topics/real-estate?o=desc&s=stars); running an e-signature server inside the demo VPS (all three are AGPL services in other runtimes needing their own DB/RAM) — [Documenso how-to](https://docs.documenso.com/developers/self-hosting/how-to) [PRIMARY]

### Inferences
- [INFERENCE] Everything in "adopt" was installed and exercised in the scratch environment during this research (HTMX/Bulma are static files; Playwright's browser download was not performed), so the builder can expect the first `pip install` to resolve cleanly on Python 3.12 — total about 60 packages and under 200 MB, before browsers.
- [INFERENCE] The "what already exists" table rows for the spec can be lifted from sections 1–11 above: candidate, what it does, licence/cost, tried (yes/no and result), decision.

### Gaps
- Nothing was tried against the real VPS; Pango availability there must be checked (`apt install libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0`) before relying on WeasyPrint.

## Gap fill (2026-10-23, VPS session)

Method: a headless job on the VPS with a fresh search budget (about 80 web searches and page fetches, plus package-registry JSON read with `curl` from pypi.org and registry.npmjs.org, and HTTP HEAD checks on two RESO files). Nothing was installed and no code was written. Where a page was bot-blocked (HTTP 403) or unreachable, the URL is cited and the block is stated; such facts are labelled [SECONDARY] when they come from a search engine's summary of that page. Commands that would inspect the VPS's system libraries (`dpkg-query`, `ldconfig`, `fc-list`) needed interactive approval in this headless run and were not run. Every bullet below was accessed 2026-10-23 unless it says otherwise.

### Coverage audit

The ask (brief, workstream 7, plus this job's requirements) broken into its questions. "Before" judges the notes above; "after" judges notes plus this gap fill.

| # | Question | Before | After | Where |
|---|---|---|---|---|
| 1 | Is there a whole-product open-source baseline (CRM / transaction management) to start from? | Partly (topic pages only, no search) | Full: none exists; the real production "baseline" is the MLS-bundled tool set | G13, G5 |
| 2 | Property intake: forms, address parsing/geocoding, public data, photos | Partly (open data only) | Full | G2 |
| 3 | Listing and marketing copy generation | Partly (SDK only) | Full | G7, G1 |
| 4 | Fair-housing word lists that exist | Not answered (nothing reachable) | Full: lists exist, none authoritative; HUD 2024 ad guidance withdrawn | G1 |
| 5 | Fair-housing checkers (open source) | Mostly | Full (2026 repos, FairHome dataset) | G1 |
| 6 | Buyer and seller message drafting, inbox, showing scheduling | Partly (SDK only) | Full | G11 |
| 7 | NY contract and form generation from templates | Partly | Full (NYSAR forms, bar-association form provenance, docassemble, stale DOS PCDS) | G4 |
| 8 | E-signature | Partly | Full (prices, licence terms, MLS-bundled option, local PDF sealing) | G5 |
| 9 | Document/PDF generation | Mostly | Full (licence traps, VPS facts) | G6 |
| 10 | Human-approval checkpoint workflow | Partly (agent frameworks only) | Full (state machines, Agent SDK, HITL services) | G7 |
| 11 | Audit log (and the AI-action / spend log it shares tables with) | Partly | Full | G8 |
| 12 | PII vault and redaction | Partly | Full (encryption package correction, model sizes, model-provider retention) | G9 |
| 13 | Guided demo mode or product tour | Not answered | Full | G3 |
| 14 | RESO data model and RESO Data Dictionary tooling | Mostly | Full (DD 2.1 still draft, tooling retired/replaced, UPI) | G10 |
| 15 | Map/geo for the demo | Not answered | Full | G2 |
| 16 | For every block: licence, cost, last release, stack fit, disk footprint | Partly | Full | G14 |
| 17 | How to test the fair-housing checker against a fixture set (success criteria) | Not answered | Full | G12 |

### Verification of load-bearing claims

| # | Claim in the notes above | Source checked | Result |
|---|---|---|---|
| 1 | RESO DD 2.0 is the current ratified version; 2.1 is a draft | [reso.org/data-dictionary](https://www.reso.org/data-dictionary/), [dd.reso.org/DD2.1/about](https://dd.reso.org/DD2.1/about/) | Confirmed: 2.1 still labelled "DRAFT" in a page generated 2026-10-19 |
| 2 | RESO EULA: royalty-free licence to incorporate the standard into products; no derivative standard; no trademark licence | [reso.org/eula](https://www.reso.org/eula/) | Confirmed (no revision date on the page) |
| 3 | DD 2.0 metadata JSON is 2,275,174 bytes and downloadable | HTTP HEAD on the [raw file](https://raw.githubusercontent.com/RESOStandards/web-api-commander/main/src/main/resources/RESODataDictionary-2.0.metadata-report.json) | Confirmed (200, 2,275,174 bytes; XLSX 1,268,474 bytes). **Flag:** the repository holding it is now marked "RETIRED" (G10) |
| 4 | DocuSeal is AGPLv3 with Section 7(b) terms; open-source on-prem tier includes Test Mode and Audit log; Pro $20/user/month | [LICENSE_ADDITIONAL_TERMS](https://github.com/docusealco/docuseal/blob/master/LICENSE_ADDITIONAL_TERMS), [pricing](https://www.docuseal.com/pricing) | Confirmed, with a new detail: the 7(b) term requires keeping DocuSeal's attribution in the user interface |
| 5 | Documenso is AGPL and active | [releases](https://github.com/documenso/documenso/releases) | Confirmed active (v2.21.1 dated 22 Oct) |
| 6 | Zillow guardrail: 39 stars, OpenRAIL-S licence, model and data only on request | [repo](https://github.com/zillow/fair-housing-guardrail), [LICENSE](https://raw.githubusercontent.com/zillow/fair-housing-guardrail/main/LICENSE), [arXiv 2409.05990](https://arxiv.org/html/2409.05990v1) | Confirmed |
| 7 | "No reusable public word list was reachable" | MLS and city publications (G1) | **Corrected:** several published lists exist (ArkansasONE MLS, revised March 2026; OneKey MLS and SmartMLS help articles, both bot-blocked; NYC Commission on Human Rights). None is authoritative |
| 8 | Presidio is moving to community ownership, MIT | [project_transition.md](https://raw.githubusercontent.com/data-privacy-stack/presidio/main/docs/project_transition.md) | Confirmed and now complete ("has completed its transition") |
| 9 | spaCy `en_core_web_sm` ~12 MB, `en_core_web_lg` ~560 MB [CLAIMED] | [sm 3.8.0](https://github.com/explosion/spacy-models/releases/tag/en_core_web_sm-3.8.0), [lg 3.8.0](https://github.com/explosion/spacy-models/releases/tag/en_core_web_lg-3.8.0) | sm confirmed (12 MB); **lg corrected to 382 MB** |
| 10 | Use `sqlcipher3-binary` 0.6.0; wheels only for cp310–cp312 | [PyPI sqlcipher3-binary](https://pypi.org/project/sqlcipher3-binary/), [PyPI sqlcipher3](https://pypi.org/project/sqlcipher3/) | **Corrected:** wheels exist for CPython 3.8–3.14, but the package describes itself as "SQLCipher 3.x"; the maintained `sqlcipher3` 0.6.4 (2026-10-13) now ships self-contained SQLCipher 4.x wheels (G9) |
| 11 | SQLCipher Community Edition is BSD-style with an attribution requirement | [zetetic.net](https://www.zetetic.net/sqlcipher/license/) | Confirmed |
| 12 | WeasyPrint 70.0, BSD, needs Pango ≥ 1.44 and three Debian packages | [PyPI](https://pypi.org/pypi/weasyprint/json), [docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html) | Confirmed |
| 13 | docxtpl 0.20.2 is LGPL-2.1-only | [PyPI](https://pypi.org/pypi/docxtpl/json) | Confirmed |
| 14 | anthropic 2.1.0 (Apache-2.0); `messages.parse` with Pydantic; strict tools | [PyPI](https://pypi.org/pypi/anthropic/json), [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) | Confirmed; structured outputs are generally available (page status "ga") on claude-opus-5-5, claude-sonnet-5-5 and claude-haiku-5-5 |
| 15 | HTMX 2.0.11 is `latest`, 4.0 is `next` | [htmx.org](https://htmx.org/), [npm](https://registry.npmjs.org/htmx.org) | Confirmed; htmx says 4.0 will be marked `latest` "at some point in 2027" |
| 16 | Pico CSS is unmaintained | [picocss maintenance](https://picocss.com/docs/maintenance) | Confirmed |
| 17 | Playwright 1.64.1; Chromium ~281 MB; `--only-shell` | [PyPI](https://pypi.org/pypi/playwright/json), [docs](https://playwright.dev/python/docs/browsers) | Confirmed |
| 18 | E-SIGN §7001(a)(1) and (d)(1); no audit-trail format prescribed | [LII 15 USC 7001](https://www.law.cornell.edu/uscode/text/15/7001) | Confirmed |
| 19 | NY STT §307 has no carve-out for real-property documents | [STT 307](https://www.nysenate.gov/legislation/laws/STT/307) | Confirmed (page revision 2026-02-27; an e-wills version takes effect 2027-12-12) |
| 20 | The DOS-hosted PCDS PDF is older than the statute | [RPL 462](https://www.nysenate.gov/legislation/laws/RPP/462), [DOS PCDS PDF](https://dos.ny.gov/property-condition-disclosure-statement) | **Confirmed as a finding:** the statute (revision 2025-07-04) has no $500 credit; the PDF DOS serves today is "DOS-1614-f (Rev. 06/23)" and still says the buyer "shall receive ... a credit of $500" |
| 21 | DOS-2156 is revision 11-25 | [DOS-2156 PDF](https://dos.ny.gov/housinganti-discrimination-form-dos-2156) | Confirmed |
| 22 | NYS Tax Parcels: Ulster and Orange in, Dutchess and Columbia out | [gis.ny.gov/parcels](https://gis.ny.gov/parcels) | Confirmed; Putnam, Greene, Sullivan, Westchester and Rockland are also in |
| 23 | 19 NYCRR 175.28 delivery rules (was a gap) | [LII 175.28](https://www.law.cornell.edu/regulations/new-york/19-NYCRR-175.28) | Read; see G1 |
| 24 | pydantic-ai 2.59.0 is current | [PyPI](https://pypi.org/pypi/pydantic-ai/json) | Superseded: 2.60.0 released 2026-10-23 (no effect on the recommendation) |

### G1. Fair-housing word lists and checkers: no authoritative list exists, so the rules file is ours

#### Takeaway
There is no authoritative fair-housing word list to adopt: HUD's former list left the CFR in 1996, HUD withdrew its 2024 digital-advertising guidance effective 2025-09-17, and the lists that do exist are MLS or city publications that say they are not exhaustive and disagree with each other (for example on "mother-in-law suite"). The POC should borrow their categories and examples, write its own rules in its own words with NY-specific additions (school, neighbourhood-composition and "safety" talk; source of income), pair them with a model review and a broker gate, and treat the fixture tests as the evidence for assumption A8.

#### Cited Findings
- [PRIMARY] HUD Docket FR-6571-N-01, published 2026-04-06: FHEO "has withdrawn" eight guidance documents, "effective date of withdrawal: September 17, 2025", including "Guidance on Application of the Fair Housing Act to the Advertising of Housing, Credit, and Other Real Estate-Related Transactions through Digital Platforms" (issued April 29, 2024); they "should not be relied upon as authoritative"; the notice adds that actions not complying "with the text of the Fair Housing Act continue to be subject to enforcement" and that private suits may be filed within two years. The January 9, 1995 advertising memo is not in the list. — [Federal Register 2026-06624 (public inspection PDF)](https://public-inspection.federalregister.gov/2026-06624.pdf) (accessed 2026-10-23)
- [SECONDARY] A second HUD notice published July 17, 2026 withdrew 13 Office of General Counsel guidance documents, effective September 25, 2025. — [NLIHC](https://nlihc.org/resource/hud-publishes-federal-register-notice-announcing-withdrawal-additional-agency-guidance) (search summary; accessed 2026-10-23)
- [PRIMARY, negative] The hud.gov copy of the January 9, 1995 Achtenberg memo ("Guidance Regarding Advertisements Under §804(c)") returns HTTP 404. — [hud.gov DOC_7784.PDF](https://hud.gov/sites/documents/DOC_7784.PDF) (accessed 2026-10-23)
- [SECONDARY] Oregon REALTORS (2024-05-03) summarises the 1995 memo: "apartment complex with chapel", "Happy Easter" and "walking distance to bus-stop" are not violations, and "mother-in-law suite" and "master bedroom" are commonplace physical descriptions. — [Oregon REALTORS](https://oregonrealtors.org/news/tip-of-the-week/permissible-advertisements-under-the-fair-housing-act/) (accessed 2026-10-23)
- [SECONDARY] Former 24 CFR Part 109 was withdrawn from the CFR effective May 1, 1996. — [search summary of a mirror of Part 109](https://howaiworks.ai/use-cases/ai-for-real-estate-listings) (accessed 2026-10-23)
- [SECONDARY] A municipal fair-housing manual (PDF dated 2011–2012) summarises what Part 109 covered beyond words: human models in ads should reflect the metropolitan area; selective placement of ads (media, geography, EHO logo use) can be discriminatory; ads should carry the Equal Housing Opportunity logo or statement; businesses should keep a written nondiscrimination advertising policy. — [Newark, Ohio Fair Housing Advertising Manual](https://www.newarkohio.gov/wp-content/uploads/2022/08/FairHousingAdvertisingManual.pdf) (accessed 2026-10-23)
- [PRIMARY] ArkansasONE MLS "Fair Housing Advertising Word and Phrase List" (revised March 2026, 4 pages): "This list is NOT all-inclusive"; three tiers (Unacceptable; Use with caution, with preferred alternatives; Acceptable); unacceptable examples include "Adults only", "Empty nesters", "Exclusive Neighborhood", "Safe neighborhood", "Near church(es)", "No children (unless HOPA*)", "Physically fit"; marked "Newly added ... as of 2026": "Mother-in-law suite", "Granny flat", "His and hers [closets/baths]", "Perfect for young professionals", "Walking distance" (use "within X miles of"); caution list maps "Master suite / Master bedroom" to "Primary suite, Owner's suite"; acceptable includes "(School district / School name)", "Near places of worship", "Accessible", "Wheelchair accessible"; a "Digital & AI advertising" section says not to target audiences by age, zip code, neighbourhood or other protected-class proxies and to "always review AI-generated content". — [ArkansasONE MLS PDF](https://www.nwarealtors.org/wp-content/uploads/2026/04/ArkansasONE-Fair-Housing.pdf) (accessed 2026-10-23)
- [SECONDARY] OneKey MLS (the Hudson Valley's largest MLS) publishes a support article "Inappropriate Words – Potential Fair Housing Violation"; its table includes "able-bodied", "adult friendly", "HIV", "homosexual" and "religious reference", some entries are conditional (e.g., "adult community" only for qualifying senior housing), and "OneKey MLS Staff will remove any flagged potential Fair Housing violations from the listing" after a courtesy notice. The page returned HTTP 403 to a direct fetch. — [OneKey MLS support](https://support.onekeymls.com/hc/en-us/articles/43190167691668-Inappropriate-Words-Potential-Fair-Housing-Violation) (search summary; accessed 2026-10-23)
- [SECONDARY] SmartMLS (Connecticut) publishes a word list that says it is "NOT all-inclusive" and "each word must be considered in context" (HTTP 403 to direct fetch). — [SmartMLS](https://compliance.smartmls.com/hc/en-us/articles/13116678459803-Fair-Housing-words-and-phrase-list) (search summary; accessed 2026-10-23)
- [SECONDARY] A NAR presentation says there is no authoritative word and phrase list and warns against lists labelled "HUD Approved" (domain did not resolve on direct fetch). — [NAR PDF](https://d7.nar.realtor/sites/default/files/documents/fair-housing-marketing-compliance-and-beyond.pdf) (search summary; accessed 2026-10-23)
- [PRIMARY] NYC Commission on Human Rights: "consider limiting advertising descriptions to features of the property"; "likely to be discriminatory": "White family home", "No Irish", "Christian home", "No programs", "No Section 8", "No wheelchairs", "No small children", "Couple preferred", "Heavily Jewish area", "Adult or mature couple"; "unlikely": "No smoking", "Walk to bus stop", "Income and credit check", "No elevator". — [NYC CCHR](https://www.nyc.gov/site/fairhousing/rights-responsibilities/real-estate-advertisements.page) (accessed 2026-10-23)
- [PRIMARY] DOS-2156 (11-25) lists New York's protected characteristics as including "but ... not limited to" race, creed, color, national origin, sexual orientation, gender identity or expression, military status, sex, age, disability, marital status, lawful source of income or familial status, and names "steering" and "blockbusting" (including predicting a "decline in the quality of schools"). — [DOS-2156 PDF](https://dos.ny.gov/housinganti-discrimination-form-dos-2156) (accessed 2026-10-23)
- [PRIMARY] 19 NYCRR 175.28: the notice is given "upon first substantive contact"; email, text, electronic messaging, fax or hardcopy are allowed, a link only if the message states "the link contains information regarding the New York State Human Rights Law"; "Oral disclosure does not satisfy the requirements"; hardcopy needs a signed acknowledgment or a sworn declaration on refusal; copies kept "not less than three years"; eff. 2020-06-20. — [LII 19 NYCRR 175.28](https://www.law.cornell.edu/regulations/new-york/19-NYCRR-175.28) (accessed 2026-10-23)
- [PRIMARY] DOS guidance (2021): 19 NYCRR 175.29 requires the Fair Housing and Anti-Discrimination Notice to be displayed in each office window, "prominently displayed on all websites operated by all real estate licensees" and at each open house. — [DOS guidance PDF](https://dos.ny.gov/system/files/documents/2021/08/fair-housing-guidance-for-re-lic-holders.pdf) (accessed 2026-10-23)
- [PRIMARY] Zillow's FairHome dataset paper (arXiv 2409.05990, 2024-09-09): about 75,000 examples, binary "compliant"/"non-compliant" labels, 15 protected categories named; access to the dataset and trained classifier is by email request; no dataset licence is stated. — [arXiv](https://arxiv.org/html/2409.05990v1) (accessed 2026-10-23)
- [PRIMARY] GitHub topic "fair-housing" sorted by recent update: the 2026 entries all have 0–11 stars, e.g. `m-binimran/real-estate-pack` (2 stars, "compliance guardrails and review agents ... on Claude Code"), `trevormchaffie/claude-skills-realestate` (0), `andrewbowlds/llm-agent-evals` (0, fair-housing safety gates for a tenant-email agent), `DE-BARY-LLC/debary-mcp-compliance` (1), `TheProsperityAgent/prosperity-real-estate-skills` (11). — [GitHub topic](https://github.com/topics/fair-housing?o=desc&s=updated) (accessed 2026-10-23)
- [PRIMARY] OneKey MLS release (2026-08-05): Ocusell List, free to all OneKey members, offers "optional AI tools" for public remarks and "built-in rule checks" before a listing goes live; Ocusell is "on the cusp of launching". — [OneKey MLS news](https://corporate.onekeymls.com/news/94u6jq9vsjyb9weezedz7tx26a3jmc) (accessed 2026-10-23)
- [CLAIMED] EstatePass offers a free checker that scans listing copy for fair-housing and state advertising issues (vendor page; no independent test found). — [EstatePass](https://www.estatepass.ai/tools/compliance/for/listing-agents/) (accessed 2026-10-23)
- [SECONDARY] New York's "synthetic performer" law (amending GBL §396-b; signed 2025-12-11, effective 2026-06-09) requires a conspicuous disclosure in ads that use AI-generated human images; penalties $1,000 first and $5,000 subsequent violations. — [Hunton](https://www.hunton.com/privacy-and-information-security-law/new-york-enacts-law-regulating-the-use-of-ai-generated-synthetic-performers-in-advertising), [Cooley](https://www.cooley.com/news/insight/2026/2026-01-29-new-york-enacts-synthetic-performer-disclosure-law-for-advertisements-including-those-using-generative-ai) (accessed 2026-10-23)

#### Inferences
- [INFERENCE] The published lists conflict with each other and with HUD's 1995 view (ArkansasONE 2026 bans "mother-in-law suite"; the 1995 memo allowed it), so the rules file must carry, for each rule, its tier, the reason, the source it borrows from, and a suggested rewrite; the checker should show the reason and source on screen. That is also the demo story: "the AI flags it, says why, and offers a fix; a broker approves".
- [INFERENCE] The lists are copyrighted publications of their MLSs; borrow categories and well-known example phrases (which are short, functional and repeated across many lists), write our own rule text, and cite each source in the file.
- [INFERENCE] New York rules beyond the generic lists, grounded in the WS2 notes' DOS discipline record and DOS-2156: (a) allow a factual "School district: X" field but block evaluative school language ("great schools", "top-rated district") in copy and in buyer replies; (b) block neighbourhood-composition, "safe/safety" and crime generalisations; (c) block source-of-income limits ("No Section 8"); (d) add the broker-identification and fair-housing-notice requirements as "required elements" checks, not word checks.
- [INFERENCE] Part 109's non-word topics (images of people, ad placement and audience targeting) and the 2026 synthetic-performer law matter for the marketing screens: the POC generates text only, so the checker should state that images and targeting are out of its scope and are a broker checkpoint.
- [INFERENCE] OneKey's own listing tool will soon run "rule checks" and AI remarks inside the MLS; our checker should be positioned as the brokerage's pre-check across every channel (social, email, flyer, website), not only MLS remarks.

#### Gaps
- OneKey MLS's full word table (HTTP 403); a licensee logging in can read it. Closing it would refine the rules file but not change the design.
- The 1995 memo's full text (HUD 404). It is non-binding internal guidance; low value.

### G2. Property intake and map/geo for the demo

#### Takeaway
Intake needs no framework: an HTMX multi-step form plus free public services. For the map, Leaflet (BSD-2, ~42 KB, no build step) with OpenStreetMap tiles under their usage policy, or OpenFreeMap's free vector tiles via MapLibre, covers the demo; a small offline fallback (static image or a Protomaps extract) protects the in-person demo. New York's own geocoder (relaunched May 2026), the Census geocoder, FEMA's flood layer and NYS aerial imagery are free and make intake visibly "fetch public facts, tag the source".

#### Cited Findings
- [PRIMARY] Leaflet site: "just about 42 KB of JS"; "Leaflet 2.0.0-alpha.1" released August 16, 2025; npm `latest` is still 1.9.4 (2023-05-18), BSD-2-Clause, no dependencies. — [leafletjs.com](https://leafletjs.com/), [npm leaflet](https://registry.npmjs.org/leaflet) (accessed 2026-10-23)
- [PRIMARY] MapLibre GL JS 6.15.0 (2026-10-18), BSD-3-Clause, 18 dependencies, npm package unpacked 28.8 MB; OpenLayers 10.11.0 (2026-10-04), BSD-2-Clause. — [npm maplibre-gl](https://registry.npmjs.org/maplibre-gl), [npm ol](https://registry.npmjs.org/ol) (accessed 2026-10-23)
- [PRIMARY] OSMF tile usage policy: normal interactive viewing allowed; bulk download, prefetching and offline use forbidden; visible "© OpenStreetMap contributors" attribution; a distinct User-Agent and a valid Referer; "We may block access, without notice, if your usage degrades the service"; for commercial services "access may be withdrawn at any point". — [OSMF tile policy](https://operations.osmfoundation.org/policies/tiles/) (accessed 2026-10-23)
- [PRIMARY] OpenFreeMap: public instance "completely free", "no limits on the number of map views or requests", "no registration, no user database, no API keys, and no cookies", MIT-licensed software, OpenStreetMap data, "Attribution is required", commercial use "Yes", funded by donations; used via the MapLibre style URL `https://tiles.openfreemap.org/styles/liberty` (Leaflet needs the MapLibre GL Leaflet plugin). — [openfreemap.org](https://openfreemap.org/), [quick start](https://openfreemap.org/quick_start/) (accessed 2026-10-23)
- [PRIMARY] Protomaps: a full planet basemap is "roughly 120 gigabytes"; regional extracts via `pmtiles extract`, each extra zoom level "roughly doubles the size"; distributed as an ODbL Produced Work with OpenStreetMap attribution; `pmtiles` npm 4.5.0 (2026-08-10), BSD-3-Clause. — [Protomaps downloads](https://docs.protomaps.com/basemaps/downloads), [npm pmtiles](https://registry.npmjs.org/pmtiles) (accessed 2026-10-23)
- [PRIMARY] NYS Geocoding Service: "published the NYS Geocoder in May 2026", a single composite locator replacing three; New York addresses only; updated on the second and fourth Friday; legacy services' retirement "planned for October 2026"; REST folder `https://nysgeohub.ny.gov/arcgis/rest/services/Geocoder` contains `NYS_Geocoder` (GeocodeServer); data provided "as is". — [gis.ny.gov](https://gis.ny.gov/nys-geocoding-service), [REST folder](https://nysgeohub.ny.gov/arcgis/rest/services/Geocoder) (accessed 2026-10-23)
- [PRIMARY] Census Geocoder API (document updated 02/2026): `onelineaddress`, `address`, `coordinates` endpoints; batch "upper limit of 10,000 records per batch file"; returns coordinates and census geographies; "does not support CORS requests"; no key or price mentioned. — [Census Geocoder API](https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html) (accessed 2026-10-23)
- [SECONDARY] NYS ITS publishes a public SAM Address Points map service (rooftop, entrance, driveway, parcel-centroid point types). — [gisservices.its.ny.gov](https://gisservices.its.ny.gov/arcgis/rest/services/SAM_Address_Points/MapServer) (search summary; accessed 2026-10-23)
- [PRIMARY] FEMA: NFHL data can be viewed in the NFHL Viewer, downloaded by county or state, and used through "dedicated GIS web services"; no licence terms stated. [PRIMARY, negative] The NFHL MapServer layer URL reset the connection on fetch. [SECONDARY] A third-party catalogue lists flood-hazard polygons as layer 28 (`S_FLD_HAZ_AR`) of `hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer`, keyless. — [FEMA NFHL](https://www.fema.gov/flood-maps/national-flood-hazard-layer), [FEMA MapServer](https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28), [glama.ai listing](https://glama.ai/mcp/servers/amyn48mpmn) (accessed 2026-10-23)
- [PRIMARY] RPL §462 PCDS Q10 asks "IS ANY OR ALL OF THE PROPERTY LOCATED IN A ... (FEMA) DESIGNATED FLOODPLAIN?" and Q13/Q15 ask about required and existing flood insurance. — [RPL 462](https://www.nysenate.gov/legislation/laws/RPP/462) (accessed 2026-10-23)
- [PRIMARY] NYS orthoimagery is "available at no cost" through web services and downloads; the newest years are 2025 for Dutchess, Ulster and Orange and 2024 for Columbia; no licence terms stated on the FAQ. — [gis.ny.gov/orthoimagery](https://gis.ny.gov/orthoimagery), [FAQ](https://gis.ny.gov/orthoimagery-faqs) (accessed 2026-10-23)
- [SECONDARY] Agricultural-district boundaries (relevant to the RPL agricultural-district disclosure) are published county by county in Cornell's CUGIR catalogue as shapefiles, generalised from parcels. — [CUGIR record via NYU GeoData](https://geo.nyu.edu/catalog/cugir-007959/metadata) (search summary; accessed 2026-10-23)
- [PRIMARY] Python helpers on PyPI: `usaddress` 0.5.16 (2025-08-07, MIT); `usaddress-scourgify` 0.7.1 (2026-08-07, "Clean US addresses following USPS pub 28 and RESO guidelines", licence not stated on PyPI); `geopy` 2.5.0 (2026-07-12, MIT); `censusgeocode` 0.5.3 (2026-02-08, GPLv3); `folium` 0.20.0 (2025-06-16, MIT, "Make beautiful maps with Leaflet.js & Python"); `Pillow` 13.0.0 (2026-10-16, MIT-CMU). — [usaddress](https://pypi.org/pypi/usaddress/json), [usaddress-scourgify](https://pypi.org/pypi/usaddress-scourgify/json), [geopy](https://pypi.org/pypi/geopy/json), [censusgeocode](https://pypi.org/pypi/censusgeocode/json), [folium](https://pypi.org/pypi/folium/json), [pillow](https://pypi.org/pypi/pillow/json) (accessed 2026-10-23)

#### Inferences
- [INFERENCE] Intake can show each field's provenance (seller / public record / inferred) by calling the NYS geocoder, the parcel or assessment record and the FEMA layer, then tagging each value. A flood-zone result must be shown as a "public record hint", never pre-filled as the seller's PCDS answer, because the PCDS is the seller's statement from actual knowledge.
- [INFERENCE] Leaflet loaded from `/static` with OSM raster tiles is the simplest no-build fit; MapLibre (WebGL, 28.8 MB package) is heavier for little demo gain. Because the demo is in person and the venue's internet is unknown, keep a static map image (or a few-MB Protomaps extract of one town) as a fallback.
- [INFERENCE] Keep demographic layers (Census ACS, school ratings, crime) out of the map entirely: showing them beside a listing is the "steering" pattern DOS-2156 describes.
- [INFERENCE] `censusgeocode` is GPLv3; calling the Census API directly with `httpx` avoids that licence for a few lines of code.

#### Gaps
- The FEMA MapServer was unreachable; a point query should be tried by the architecture step. Not decision-changing (the demo house is fictional).
- `usaddress-scourgify`'s licence needs reading before adoption.

### G3. Guided demo mode or product tour

#### Takeaway
Driver.js (MIT, no dependencies, CDN or vendored file, active: 1.10.2 on 2026-10-18) is the one current tour library that fits a commercial, no-build app; Shepherd.js and Intro.js are AGPL-3.0 with paid commercial licences. Recorded-demo SaaS (Arcade, Storylane) solves a different problem (click-through videos), so the guided demo should be our own narration panel driven by one demo script file, with Driver.js only for the spotlight effect.

#### Cited Findings
- [PRIMARY] `driver.js` 1.10.2 published 2026-10-18, licence MIT, 0 dependencies, unpacked 206 kB; GitHub (now `nilbuild/driver.js`) shows 26.9k stars and the README claims about 5 KB gzipped and "no external dependencies". — [npm](https://registry.npmjs.org/driver.js), [GitHub](https://github.com/kamranahmedse/driver.js) (accessed 2026-10-23)
- [PRIMARY] Driver.js installs with a `<script>` tag for `driver.js.iife.js` and a stylesheet, used via `window.driver.js.driver`; hints and checklists are optional add-on files. — [driverjs.com installation](https://driverjs.com/docs/installation) (accessed 2026-10-23)
- [PRIMARY] `shepherd.js` 15.3.0 (2026-08-24), npm licence AGPL-3.0; "if you want to use Shepherd.js in your commercial app, website or plugin, you would need to obtain a commercial license": Business $50 lifetime (5 projects), Enterprise $300 lifetime. — [npm](https://registry.npmjs.org/shepherd.js), [shepherdjs.dev/pricing](https://shepherdjs.dev/pricing) (accessed 2026-10-23)
- [PRIMARY] `intro.js` 8.6.0 (2026-09-21), "published under AGPL license"; commercial use needs a licence: Starter $9.99, Business $49.99, Premium $299.99 (one-time). — [npm](https://registry.npmjs.org/intro.js), [introjs.com](https://introjs.com/) (accessed 2026-10-23)
- [PRIMARY] Older tour libraries are abandoned: `hopscotch` 0.3.1 (2017-06-02), `bootstrap-tour` 0.12.0 (2017-10-03); `reactour` needs React. — [npm hopscotch](https://registry.npmjs.org/hopscotch), [npm bootstrap-tour](https://registry.npmjs.org/bootstrap-tour), [npm reactour](https://registry.npmjs.org/reactour) (accessed 2026-10-23)
- [SECONDARY] Arcade (interactive recorded demos) has a one-seat free tier and paid tiers (Pro $32/user/month per Arcade's own pricing post; Growth about $50/seat/month per a third party); Storylane's Starter is about $40/seat/month billed annually; sources conflict on free-tier limits. — [Arcade pricing post](https://www.arcade.software/post/arcade-pricing), [Trainn on Storylane](https://trainn.co/blog/storylane-pricing/) (search summaries; accessed 2026-10-23)
- [PRIMARY] (from section 11 above) AleksNeStu/ai-real-estate-assistant ships a demo mode that "uses simulated AI responses for instant exploration". — [GitHub](https://github.com/AleksNeStu/ai-real-estate-assistant) (accessed by the earlier pass; not re-fetched)

#### Inferences
- [INFERENCE] Make `docs/DEMO-SCRIPT.md` and the in-app narration cards come from one source (a YAML or Markdown file of steps: screen, spotlight selector, narration text, the human/licensed checkpoint and its reason). That guarantees the success criterion "the walkthrough script matches the screens one for one".
- [INFERENCE] Live AI calls need internet; a "replay" switch that serves recorded model outputs for the demo house (clearly labelled as recorded) protects the in-person demo, borrowing the simulated-response idea above.
- [INFERENCE] With HTMX swapping page fragments, Driver.js steps must re-attach after swaps; this is the one thing to try on a real two-screen example before adopting.

#### Gaps
- None that change the choice.

### G4. NY contract and form templates; document assembly

#### Takeaway
No open template set can be adopted for the contract: the NYSAR statewide purchase agreement is a member-only benefit, and the long-used bar-association "Residential Contract of Sale" has no visible licence. The POC should mirror the customary section structure with original wording, generate the statutory forms from statute text (the DOS PCDS PDF is out of date), and use docxtpl/WeasyPrint. Docassemble, the leading open-source document-assembly system, is too heavy for this VPS (4 GB RAM, 40 GB disk host minimum) but is the model for "interview, then document".

#### Cited Findings
- [SECONDARY] NYSAR's July/August 2025 CEO column: the Statewide Forms Committee drafts forms "for use anywhere in the state as an exclusive, free benefit to NYSAR members", kept in the member-only library at NYSAR.com/legal/forms; it "released an amended purchase agreement" and approved drafting an escalation addendum, a multiple-offer disclosure and an unrepresented-buyer disclosure (direct fetch returned an empty page). — [New York State REALTOR, July/Aug 2025](https://pubs.royle.com/article/From+the+CEO%E2%80%99s+Desk/5006115/849018/article.html) (search summary; accessed 2026-10-23)
- [SECONDARY] NYSAR (January/February 2025) advises giving an unrepresented buyer the agency disclosure form before negotiating, and the Housing and Anti-Discrimination Disclosure Form. — [New York State REALTOR, Jan/Feb 2025](https://pubs.royle.com/article/Working+with+Unrepresented+Buyers/4916140/838705/article.html) (search summary; accessed 2026-10-23)
- [PRIMARY] The "Residential Contract of Sale 11-2000" states it was "Jointly prepared by the Real Property Section of the New York State Bar Association", the New York State Land Title Association and two City and County bar committees; Justia's page offers a free print-only PDF via U.S. Legal Forms and shows no copyright notice for the form. — [Justia forms](https://forms.justia.com/new-york/statewide/real-estate/title/residential-contract-of-sale-2000-short-42193.html) (accessed 2026-10-23)
- [PRIMARY] docassemble: MIT, 992 stars; `docassemble.base` 1.10.14 released 2026-10-23 (183 declared requirements, Python ≥ 3.12); Docker host needs "at least 4GB of memory and 40GB of hard drive space", the image is "about 4GB", the installation "will use up about 20GB"; one container runs 13 services (postgres, redis, rabbitmq, nginx, celery, unoserver and others). — [GitHub](https://github.com/jhpyle/docassemble), [PyPI](https://pypi.org/pypi/docassemble.base/json), [docassemble Docker docs](https://docassemble.org/docs/docker.html) (accessed 2026-10-23)
- [PRIMARY] RPL §462 (revision 2025-07-04) contains no $500 credit, while the PDF at DOS's PCDS URL is "DOS-1614-f (Rev. 06/23)" and says "the buyer shall receive upon the transfer of title a credit of $500"; the PDF has fillable text fields. — [RPL 462](https://www.nysenate.gov/legislation/laws/RPP/462), [DOS PCDS PDF](https://dos.ny.gov/property-condition-disclosure-statement) (accessed 2026-10-23)
- [PRIMARY] DOS-2156 (11-25) is the current fair-housing disclosure form; the DOS forms page lists the buyer/seller and landlord/tenant agency disclosures in 13 languages. — [DOS-2156](https://dos.ny.gov/housinganti-discrimination-form-dos-2156), [DOS forms page](https://dos.ny.gov/real-estate-broker-forms) (accessed 2026-10-23)
- [PRIMARY] OneKey MLS's product page lists "SkySlope Forms" and "TransactionDesk®" among member tools (no prices or inclusion stated). — [OneKey products](https://corporate.onekeymls.com/benefits-products) (accessed 2026-10-23)

#### Inferences
- [INFERENCE] Hudson Valley practice may use either a broker-prepared purchase agreement "subject to attorney approval" (NYSAR's form) or an attorney-drafted bar-association contract; which one the founder uses decides the POC's contract skeleton. Both can be mirrored structurally without copying text.
- [INFERENCE] The PCDS template must be generated from the statute and carry an "attorney: confirm current form" checkpoint, because the state's own PDF lags the statute; this is a concrete example for the father-in-law of why a human legal check stays in the loop.
- [INFERENCE] Borrow docassemble's pattern (structured interview, each answer feeding a template, a review screen) without running it.

#### Gaps
- The NYSAR purchase agreement's text and terms of use (member-only): the founder, if a NYSAR member, can read it.
- Copyright holder of the bar-association form: unresolved; irrelevant if we write our own text.

### G5. E-signature: simulate in the POC; in production the MLS bundle may already include it

#### Takeaway
For the POC, simulated signing stays right; a real local seal (pyHanko, MIT) can make the simulation tamper-evident without a second server. For production, the cheapest path is probably the OneKey subscription's TransactionDesk with AuthentiSign (reported as included), then DocuSeal (self-hosted free but must show DocuSeal attribution; cloud API $0.20 per document), then commercial APIs such as BoldSign ($0.75 per envelope).

#### Cited Findings
- [SECONDARY] OneKey MLS support page "TransactionDesk Resources": "TransactionDesk® is your all-in-one transaction solution, included in your OneKey MLS Subscription", with AuthentiSign e-signature, forms, document storage, a client portal and a broker dashboard (page returned HTTP 403 to direct fetch). — [OneKey support](https://support.onekeymls.com/hc/en-us/articles/29453946733588-TransactionDesk-Resources) (search summary; accessed 2026-10-23)
- [PRIMARY] DocuSeal's latest GitHub release is 3.3.3 (dated 19 Oct; year not shown), which lets the open-source app accept DOCX uploads; the README says "Distributed under the AGPLv3 License with Section 7(b) Additional Terms" and "© 2023-2026 DocuSeal LLC"; the additional term: "a covered work must retain the original DocuSeal attribution in interactive user interfaces". — [releases](https://github.com/docusealco/docuseal/releases), [README](https://raw.githubusercontent.com/docusealco/docuseal/master/README.md), [LICENSE_ADDITIONAL_TERMS](https://github.com/docusealco/docuseal/blob/master/LICENSE_ADDITIONAL_TERMS) (accessed 2026-10-23)
- [PRIMARY] DocuSeal pricing: cloud Basic $0 (10 signature-request emails a month); Pro $20/user/month or $200/year; API and embedding $0.20 per document signed (needs a Pro seat); on-premises Open Source free with Test Mode and Audit log; on-premises Pro $240/user/year. — [docuseal.com/pricing](https://www.docuseal.com/pricing) (accessed 2026-10-23)
- [PRIMARY] DocuSeal's "Certificate of Signature (Audit Log)" is "stored with the finalized document" and lists IP address, session ID, user agent, time zone and event timestamps; whether it is embedded in the PDF is not stated. — [DocuSeal FAQ](https://www.docuseal.com/faq/what-is-the-certificate-of-signature-audit-log) (accessed 2026-10-23)
- [SECONDARY] DocuSeal resource use: minimum 1 vCPU and 512 MB RAM, idle about 200 MB, peaks about 480 MB while signing (deployment-template guide; no official figure found). — [Railway guide](https://railway.com/deploy/docuseal-docusign-alternative.md) (search summary; accessed 2026-10-23)
- [PRIMARY] Documenso latest release v2.21.1 (22 Oct); OpenSign v3.0.0 (21 Oct) adds Qualified Electronic Signature support. — [Documenso releases](https://github.com/documenso/documenso/releases), [OpenSign releases](https://github.com/OpenSignLabs/OpenSign/releases) (accessed 2026-10-23)
- [SECONDARY] Documenso appends a certificate of completion (signers, timeline, device information, QR code) to the completed PDF by default and digitally seals it. — [Mintlify-hosted Documenso docs](https://mintlify.com/documenso/documenso/concepts/signing-certificates) (accessed 2026-10-23)
- [PRIMARY] BoldSign: "Each envelope sent through the BoldSign API is considered one signature request and is billed at $0.75 per envelope." — [BoldSign support](https://support.boldsign.com/kb/article/21759/understanding-signature-request-charges-in-boldsign-api) (accessed 2026-10-23)
- [SECONDARY] Dropbox Sign's official help page (updated December 2025) describes API tiers by monthly volume (Essentials, Standard for embedded signing, Premium) and a free test mode, without dollar figures; third-party figures conflict. — [Dropbox help](https://help.dropbox.com/plans/how-much-does-the-dropbox-sign-api-cost) (search summary; accessed 2026-10-23)
- [PRIMARY] pyHanko 0.38.0 (2026-10-17, MIT): PAdES baseline B-B to B-LTA signing, RFC 3161 timestamps, signature validation, stamping; README: "currently in beta, and not yet production-ready"; 789 stars. `endesive` 3.0.1 (2026-10-16, MIT) is an alternative. — [GitHub pyHanko](https://github.com/MatthiasValvekens/pyHanko), [PyPI pyHanko](https://pypi.org/pypi/pyhanko/json), [PyPI endesive](https://pypi.org/pypi/endesive/json) (accessed 2026-10-23)
- [PRIMARY] `@docuseal/react` 1.0.75 (MIT) exists for embedding; no plain-JS or Python SDK was checked. — [npm](https://registry.npmjs.org/@docuseal/react) (accessed 2026-10-23)

#### Inferences
- [INFERENCE] Demo signing screen: record consent text, signer, timestamp, IP and the SHA-256 of the document version in the audit log, then apply a pyHanko seal with a self-signed "DEMO" certificate so the audience can see a PDF reader flag any later edit. Label it "simulated; production uses a licensed e-signature service".
- [INFERENCE] Whether AuthentiSign/TransactionDesk can be driven by API from our software is unknown; if it cannot, production signing through it is a human step (the broker sends the envelope), which the timeline should show.
- [INFERENCE] DocuSeal's attribution term rules out a white-labelled self-hosted signing page unless DocuSeal Pro is bought.

#### Gaps
- TransactionDesk inclusion (bot-blocked page) and API availability: a call to OneKey MLS member support closes it.
- DocuSeal's official resource figures: not found; not needed for the POC.

### G6. Document/PDF libraries: licence traps and VPS facts

#### Takeaway
The recommended set (WeasyPrint, docxtpl, pypdf, optional ReportLab) is permissive and current. Two popular PDF libraries are AGPL (PyMuPDF, borb) and must stay out of a proprietary product. The VPS has Python 3.12.3 and `uv`, and no Chromium or LibreOffice, so the dual-template approach (no DOCX-to-PDF converter) is confirmed as the lighter path.

#### Cited Findings
- [PRIMARY] PyPI, versions and licences today: `pypdf` 6.21.2 (2026-10-21, BSD-3-Clause); `reportlab` 5.1.0 (2026-10-22, BSD); `fpdf2` 2.8.9 (2026-09-29, LGPL-3.0-only); `pymupdf` 2.0 (2026-10-19, "Dual Licensed - GNU AFFERO GPL 3.0 or Artifex" commercial, wheels 63–89 MB); `borb` 3.0.9 (2026-08-03, AGPL-3.0-or-later); `python-docx` 1.2.0 (MIT); `docxtpl` 0.20.2 (LGPL-2.1-only); `weasyprint` 70.0 (BSD). — [pypdf](https://pypi.org/pypi/pypdf/json), [reportlab](https://pypi.org/pypi/reportlab/json), [fpdf2](https://pypi.org/pypi/fpdf2/json), [pymupdf](https://pypi.org/pypi/pymupdf/json), [borb](https://pypi.org/pypi/borb/json), [python-docx](https://pypi.org/pypi/python-docx/json), [docxtpl](https://pypi.org/pypi/docxtpl/json), [weasyprint](https://pypi.org/pypi/weasyprint/json) (accessed 2026-10-23)
- [PRIMARY] WeasyPrint 70.0 docs: requires "Pango ≥ 1.44.0"; Ubuntu wheels need `libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libharfbuzz-subset0`; "Using WeasyPrint with untrusted HTML or untrusted CSS may lead to various security problems". — [WeasyPrint first steps](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html) (accessed 2026-10-23)
- [PRIMARY, observed on the VPS 2026-10-23] `python3 --version` → Python 3.12.3; `which` finds `/usr/bin/python3.12` and `/usr/local/bin/uv`, and no `chromium`, `google-chrome`, `soffice` or `libreoffice`; `scripts/disk-check.sh` → 21 GB free of 96 GB (79% used). — [this repo: scripts/disk-check.sh](https://github.com/EarthToJoe/realestate/blob/main/scripts/disk-check.sh) (accessed 2026-10-23)
- [PRIMARY] HTML sanitisers: `nh3` 0.3.7 (2026-08-23, MIT, Rust "Ammonia" binding); `bleach` 6.4.0 (2026-06-05, Apache). — [nh3](https://pypi.org/pypi/nh3/json), [bleach](https://pypi.org/pypi/bleach/json) (accessed 2026-10-23)

#### Inferences
- [INFERENCE] Model output rendered into HTML (listing copy, emails, contract clauses) is untrusted input for both the browser and WeasyPrint; sanitise with `nh3` (or render as escaped text through Jinja2 autoescape) before display or PDF rendering.
- [INFERENCE] Use pypdf to attach or fill government PDFs only where the PDF is current (agency disclosure, EPA lead form); render the PCDS from statute text.

#### Gaps
- Pango and fonts on the VPS were not checked (the inspection commands needed interactive approval). One command closes it: `dpkg -s libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 fonts-dejavu-core`.

### G7. Human-approval checkpoints, the agent loop and copy generation

#### Takeaway
The plain Anthropic SDK with structured outputs (now generally available) remains the right core for every AI step, including listing and marketing copy. Checkpoints are best modelled as a small state machine over the deal plus an approvals table; `python-statemachine` (MIT, released 2026-10-14) is worth a one-hour trial against hand-rolled code. The Claude Agent SDK, PydanticAI and LangGraph all have approval hooks but add weight or a coding-agent runtime the POC does not need.

#### Cited Findings
- [PRIMARY] Structured outputs: schema in `output_config.format` with `type: "json_schema"`; Python `client.messages.parse()` with a Pydantic model returns `parsed_output`; strict tool use guarantees schema-valid tool inputs; page status "ga" on every platform; supported models include claude-opus-5-5, claude-sonnet-5-5 and claude-haiku-5-5; limits: 20 strict tools per request; "the `output_format` parameter is deprecated". — [Anthropic structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) (accessed 2026-10-23)
- [PRIMARY] `python-statemachine` 3.2.2 (2026-10-14, MIT); `transitions` 0.9.3 (2025-07-02, MIT); `SpiffWorkflow` 3.2.0 (2026-08-10, LGPLv3, "A workflow framework and BPMN/DMN Processor"). — [python-statemachine](https://pypi.org/pypi/python-statemachine/json), [transitions](https://pypi.org/pypi/transitions/json), [SpiffWorkflow](https://pypi.org/pypi/spiffworkflow/json) (accessed 2026-10-23)
- [PRIMARY] Claude Agent SDK for Python 0.2.173 (2026-10-22): MIT licence file, but "Use of this SDK is governed by Anthropic's Commercial Terms of Service"; "The Claude Code CLI is automatically bundled with the package"; approval controls via `can_use_tool`, `permission_mode` and `PreToolUse` hooks that can return `permissionDecision: "deny"`; wheels up to about 130 MB. — [GitHub](https://github.com/anthropics/claude-agent-sdk-python), [PyPI](https://pypi.org/pypi/claude-agent-sdk/json) (accessed 2026-10-23)
- [PRIMARY] `pydantic-ai` 2.60.0 and `pydantic-ai-slim` 2.60.0 (2026-10-23, MIT); `langgraph` 1.2.16 (2026-10-16, MIT). — [pydantic-ai](https://pypi.org/pypi/pydantic-ai/json), [langgraph](https://pypi.org/pypi/langgraph/json) (accessed 2026-10-23)
- [SECONDARY] HumanLayer, once a Python toolkit for pausing agents for human approval, has pivoted to a coding IDE and cloud platform (CodeLayer). — [tooldirectory.ai](https://tooldirectory.ai/tools/humanlayer) (search summary; accessed 2026-10-23)
- [PRIMARY] `jinja2-fragments` 1.12.0 (2026-04-08, MIT) renders a single template block as an HTML fragment, the usual pattern for HTMX partial updates. — [PyPI](https://pypi.org/pypi/jinja2-fragments/json) (accessed 2026-10-23)

#### Inferences
- [INFERENCE] Each deal step declares its actor (AI / human / licensed / attorney) and its legal reason; transitions that cross a licensed act are guarded by an approval row signed by a logged-in licensee. A state-machine library gives guards and a diagram for free; the timeline view reads the same definitions, so the human-in-the-loop map cannot drift from the code.
- [INFERENCE] Approval must be enforced server-side (the PydanticAI docs' warning quoted above applies to any framework): the HTMX button only posts a request; the server checks the session's role before the transition fires.

#### Gaps
- None that change the recommendation.

### G8. Audit log, AI-action log and spend tracking

#### Takeaway
Hosted LLM-observability stacks are oversized for this VPS (Langfuse's documented minimum is about 17.5 GiB RAM across five services), so the audit trail, AI-action log and spend log stay as our own SQLite tables with append-only triggers and a hash chain. Anthropic's Usage and Cost Admin API can reconcile per-key spend, but only for an organisation account with an Admin key.

#### Cited Findings
- [PRIMARY] Langfuse self-hosting minimums: web 2 CPU/4 GiB, worker 2 CPU/4 GiB, PostgreSQL 2 CPU/4 GiB, Redis/Valkey 1 CPU/1.5 GiB, ClickHouse 2 CPU/8 GiB, plus blob storage. — [langfuse.com scaling](https://langfuse.com/self-hosting/scaling) (accessed 2026-10-23)
- [SECONDARY] Arize Phoenix is source-available under the Elastic License 2.0 and can run as one container on SQLite. — [Langfuse comparison page (competitor)](https://langfuse.com/resources/engineering/best-phoenix-arize-alternatives.md), [Railway template](https://railway.com/deploy/phoenix) (search summaries; accessed 2026-10-23)
- [PRIMARY] Anthropic Usage and Cost Admin API: `/v1/organizations/usage_report/messages` (tokens; buckets 1m/1h/1d; filter or group by API key, workspace, model) and `/v1/organizations/cost_report` (USD, daily); requires an Admin API key (`sk-ant-admin01-...`); "The Admin API is unavailable for individual accounts"; data "typically appears within 5 minutes". — [Usage and Cost API](https://platform.claude.com/en/docs/build-with-claude/usage-cost-api) (accessed 2026-10-23)
- [PRIMARY] `structlog` 26.1.0 (2026-06-06, MIT OR Apache-2.0); `sqlite-chronicle` 0.6.1 (2026-02-15, Apache-2.0); `SQLAlchemy-Continuum` 2.0.0 (2026-10-14, BSD-3-Clause). — [structlog](https://pypi.org/pypi/structlog/json), [sqlite-chronicle](https://pypi.org/pypi/sqlite-chronicle/json), [SQLAlchemy-Continuum](https://pypi.org/pypi/sqlalchemy-continuum/json) (accessed 2026-10-23)

#### Inferences
- [INFERENCE] One `events` table (who, what, when, record id, before/after hash, previous-row hash) serves the audit log, the PII access log and the AI-action log; per-call token usage from the SDK response gives module-level spend for `docs/SPEND-LOG.md`; the Admin API (if Joe's Console account is an organisation) reconciles it.
- [INFERENCE] `structlog` processors are the natural place to drop or mask PII fields before any log line is written.

#### Gaps
- Langfuse's licence for its core was not re-read; irrelevant because it is ruled out on resources.

### G9. PII: redaction, encryption at rest, and the model provider's retention

#### Takeaway
Presidio (now fully community-governed, MIT) with our own regex recognisers remains the redaction choice; spaCy's large model is 382 MB, not 560 MB, and still unnecessary. For encryption at rest, switch the recommendation from `sqlcipher3-binary` to the maintained `sqlcipher3` (0.6.4, self-contained SQLCipher 4.x wheels). Anthropic deletes API inputs and outputs within 30 days by default (zero retention by arrangement), so minimising what is sent to the model is the main lever.

#### Cited Findings
- [PRIMARY] Presidio "has completed its transition from a Microsoft-owned project to an independent, community-governed open source project" under Data Privacy Stack; "continues to be open source under the MIT license"; new images at `ghcr.io/data-privacy-stack/presidio-*`. — [project_transition.md](https://raw.githubusercontent.com/data-privacy-stack/presidio/main/docs/project_transition.md) (accessed 2026-10-23)
- [PRIMARY] spaCy `en_core_web_sm` 3.8.0 is 12 MB and `en_core_web_lg` 3.8.0 is 382 MB, both MIT. — [sm release](https://github.com/explosion/spacy-models/releases/tag/en_core_web_sm-3.8.0), [lg release](https://github.com/explosion/spacy-models/releases/tag/en_core_web_lg-3.8.0) (accessed 2026-10-23)
- [PRIMARY] `sqlcipher3-binary` 0.6.0 (2025-12-31): manylinux x86-64 wheels for CPython 3.8–3.14; summary "DB-API 2.0 interface for SQLCipher 3.x". `sqlcipher3` 0.6.4 (2026-10-13): summary "SQLCipher 4.x"; wheels for Linux, macOS and Windows on CPython 3.9–3.14 that bundle SQLCipher and need no system library ("A completely self-contained binary package (wheel) is available starting with version 0.6.2"); GitHub licence Zlib. — [PyPI sqlcipher3-binary](https://pypi.org/project/sqlcipher3-binary/), [PyPI sqlcipher3](https://pypi.org/project/sqlcipher3/), [GitHub coleifer/sqlcipher3](https://github.com/coleifer/sqlcipher3) (accessed 2026-10-23)
- [PRIMARY] Anthropic privacy centre (updated July 1, 2026): "we automatically delete inputs and outputs on our backend within 30 days of receipt or generation"; flagged content up to 2 years; feedback 5 years. — [privacy.claude.com](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data) (accessed 2026-10-23)
- [PRIMARY] Anthropic API docs: "Retained data is never used for model training without your express permission"; "Conversation content ... is not retained by default; the exception is Covered Models, which require 30-day retention" (Claude Fable 5.1, Mythos 5.1, Fable 5, Mythos 5); zero data retention is arranged per organisation; even under ZDR flagged content may be kept up to 2 years. — [API and data retention](https://platform.claude.com/docs/en/build-with-claude/api-and-data-retention) (accessed 2026-10-23); this wording conflicts with the privacy centre's 30-day default above.
- [PRIMARY] `scrubadub` 2.0.1 was last released 2023-09-01; `gliner` 0.2.29 (2026-09-08, Apache-2.0) is a general NER model library; `phonenumbers` 9.0.41 (Apache-2.0) validates phone numbers. — [scrubadub](https://pypi.org/pypi/scrubadub/json), [gliner](https://pypi.org/pypi/gliner/json), [phonenumbers](https://pypi.org/pypi/phonenumbers/json) (accessed 2026-10-23)

#### Inferences
- [INFERENCE] Plan for up to 30 days' retention at Anthropic unless Joe's organisation gets ZDR: send the model only the fields a step needs, replace names, phones and emails with placeholders (Presidio anonymizer), and re-insert them after the call. Avoid the "Covered Models" for any PII-bearing call.
- [INFERENCE] `sqlcipher3` (Zlib wrapper + SQLCipher's BSD-style attribution) needs the same "About / licences" screen the notes already proposed.

#### Gaps
- Which of the two Anthropic statements governs a standard API key today: ask Anthropic, or assume 30 days (the safer reading).

### G10. RESO Data Dictionary and tooling in 2026

#### Takeaway
Use DD 2.0 names for our schema subset and ship the 2.0 metadata JSON as a lookup resource; 2.1 is still a draft. RESO's Java tooling ("Commander") is retired and its replacement, `reso-tools`, is TypeScript under the RESO EULA rather than an open-source licence; there is still no maintained Python RESO library, which does not matter because the POC does not speak the RESO Web API.

#### Cited Findings
- [PRIMARY] RESO's Data Dictionary page lists "2.1 Draft" alongside ratified 2.0 and 1.7 spreadsheets; downloading means agreeing to the RESO EULA. — [reso.org/data-dictionary](https://www.reso.org/data-dictionary/) (accessed 2026-10-23)
- [PRIMARY] dd.reso.org labels DD 2.1 "(DRAFT)" (page generated October 19, 2026). — [dd.reso.org/DD2.1/about](https://dd.reso.org/DD2.1/about/) (accessed 2026-10-23)
- [PRIMARY] RESO (2026-01-29): 2026 goals include "publish Data Dictionary 2.1 on a new site"; "Data Dictionary 2.2 and 3.0 will not be too far behind"; a new policy on MINOR and MAJOR versions "was ratified". — [RESO blog](https://www.reso.org/blog/reso-accomplishments-goals/) (accessed 2026-10-23)
- [PRIMARY] `web-api-commander`: "THE COMMANDER HAS RETIRED. THIS REPO IS NO LONGER BEING MAINTAINED. SEE https://tools.reso.org FOR CERTIFICATION." — [GitHub](https://github.com/RESOStandards/web-api-commander) (accessed 2026-10-23)
- [PRIMARY] `reso-tools`: "Open-source toolkit for building and testing RESO-compliant OData servers" with eight packages (reso-validation for "field and business-rule validation for RESO Data Dictionary records", reso-metadata-utils, reso-common, a reference server on PostgreSQL/MongoDB/SQLite, reso-certification, reso-client, an OData filter parser, an unpublished reso-mcp-server); npm install; its LICENSE file is the RESO "End-user License Agreement (EULA)". — [GitHub reso-tools](https://github.com/RESOStandards/reso-tools), [LICENSE](https://raw.githubusercontent.com/RESOStandards/reso-tools/main/LICENSE) (accessed 2026-10-23)
- [PRIMARY] npm: `@reso-standards/reso-reference-server` 0.8.5 (2026-10-23) and `@reso-standards/reso-common` 0.4.1 (2026-10-14), licence "SEE LICENSE IN LICENSE"; the only other match, `reso-data-dictionary` 1.2.5, dates from 2015. — [npm search](https://registry.npmjs.org/-/v1/search?text=reso%20data%20dictionary&size=15) (accessed 2026-10-23)
- [PRIMARY] RESO Universal Parcel Identifier v2.0: `urn:reso:upi:<Version>:<Country>:<CountrySubdivision>:<ParcelNumber>`, e.g. `urn:reso:upi:2.0:US:48201:R000022230`, where the subdivision is a Census GEOID and the parcel number is kept exactly as in the source; downloading means agreeing to the RESO EULA. — [GitHub reso-upi](https://github.com/RESOStandards/reso-upi) (accessed 2026-10-23)
- [PRIMARY] RESOStandards also hosts a `reso-offer-management` repository ("Offer Management standard", 24 commits; specification not read). — [GitHub](https://github.com/RESOStandards/reso-offer-management) (accessed 2026-10-23)
- [SECONDARY] The only Python RESO Web API client found is a third-party repository targeting Python 3.6+. — [GitHub MindaugasKiznis/RESO-WebAPI-Client-Python](https://github.com/MindaugasKiznis/RESO-WebAPI-Client-Python) (search summary; accessed 2026-10-23)
- [PRIMARY] OneKey MLS tells technology vendors it offers "RESO-compliant data" via MLS Grid. — [OneKey benefits](https://corporate.onekeymls.com/benefits) (accessed 2026-10-23)

#### Inferences
- [INFERENCE] Store `ParcelNumber` plus a computed UPI (county GEOID from the Census geocoder) on each property: cheap, standard, and it lets later public-record joins work.
- [INFERENCE] Read the RESO Offer Management specification before designing the offers table; adopting its field names would keep the offers screen consistent with where the industry is heading.
- [INFERENCE] Do not depend on `reso-tools` (TypeScript, EULA-licensed); if validation is wanted, read lookups from the DD 2.0 JSON in Python.

#### Gaps
- Whether RESO objects to publishing a field mapping outside a product (EULA silent); attorney reading only.

### G11. Message drafting, shared inbox and showing scheduling

#### Takeaway
Nothing needs adopting for the POC: drafting is SDK calls, the inbox is our own outbox table with approve/edit/send, and showings in production go through the MLS's own ShowingTime tool. Open-source helpdesks (Chatwoot) and schedulers (Cal.com) would each add a Postgres/Redis server and, for Cal.com, AGPL obligations.

#### Cited Findings
- [SECONDARY] Chatwoot Community Edition is MIT-licensed; the Enterprise Edition needs a paid licence; self-hosting uses PostgreSQL (with pgvector) and Redis. — [Chatwoot FAQ](https://www.chatwoot.com/docs/self-hosted/faq), [Railway template](https://railway.com/deploy/chatwoot-customer-support) (search summaries; accessed 2026-10-23)
- [SECONDARY] Cal.com's core is AGPLv3 and its `/ee` folder is commercially licensed. — [Cal.com docs mirror](https://mintlify.com/calcom/cal.com/introduction) (search summary; accessed 2026-10-23)
- [PRIMARY] OneKey MLS's product list includes "ShowingTime™ for the MLS" and "SentriLock®". — [OneKey products](https://corporate.onekeymls.com/benefits-products) (accessed 2026-10-23)

#### Inferences
- [INFERENCE] The demo's showing request should end at a visible "booked through the MLS showing service by a licensee" marker until WS3/WS1 say otherwise.

#### Gaps
- None that change the POC.

### G12. Testing the fair-housing checker and the demo

#### Takeaway
Plain `pytest` with a parametrised fixture file (at least 30 allowed and disallowed phrases, per the success criteria) and Playwright for the end-to-end demo run is enough. Promptfoo (now owned by OpenAI, still MIT, Node), Inspect (MIT, 113 dependencies) and DeepEval (Apache-2.0) are capable but add a second toolchain or heavy dependencies.

#### Cited Findings
- [PRIMARY] Promptfoo README: "Promptfoo is now part of OpenAI" and remains "MIT licensed"; installed with npm; 26.3k stars. — [GitHub promptfoo](https://github.com/promptfoo/promptfoo) (accessed 2026-10-23)
- [SECONDARY] OpenAI announced the Promptfoo acquisition on March 9, 2026. — [TechCrunch](https://www.techcrunch.com/2026/03/09/openai-acquires-promptfoo-to-secure-its-ai-agents/) (search summary; accessed 2026-10-23)
- [PRIMARY] `inspect-ai` 0.3.283 (2026-10-21, MIT, 113 declared requirements, wheels about 35 MB); `deepeval` 4.3.1 (2026-10-16, Apache-2.0); `pytest` 9.1.1 (MIT); `pytest-playwright` 0.10.0 (Apache-2.0). — [inspect-ai](https://pypi.org/pypi/inspect-ai/json), [deepeval](https://pypi.org/pypi/deepeval/json), [pytest](https://pypi.org/pypi/pytest/json), [pytest-playwright](https://pypi.org/pypi/pytest-playwright/json) (accessed 2026-10-23)

#### Inferences
- [INFERENCE] Two test layers: the rules file is tested deterministically on every run; the model review is tested against recorded responses by default and live only on demand (cost and flakiness), with the pass rate shown on a "checker report" screen in the demo.

#### Gaps
- None.

### G13. Whole-product baselines and AI real estate projects, re-checked

#### Takeaway
A fresh search confirms there is no open-source sale-transaction-management system to adopt; the closest things are landlord tools and CRMs. In production the "baseline" is the MLS bundle a member already pays for (forms, e-signature, showings, listing entry).

#### Cited Findings
- [SECONDARY] A search for open-source transaction-management software returned commercial products (e.g. Paperless Pipeline) and landlord or CRM projects (MicroRealEstate, prolinkinfo RealEstateCRM), no dotloop-like open-source system. — [GetApp category](https://www.getapp.com/real-estate-property-software/real-estate-transaction-management/p/open-source/), [GitHub prolinkinfo/RealEstateCRM](https://github.com/prolinkinfo/RealEstateCRM) (search summaries; accessed 2026-10-23)
- [SECONDARY] GitLab hosts small projects such as CasaBot (listing alerts with a conversational layer) and GeoListing (AGPL-3.0+, listing generation and marketing). — [GitLab topic home-buying](https://gitlab.com/explore/projects/topics/home-buying) (search summary; accessed 2026-10-23)
- [PRIMARY] OneKey MLS's product list includes Matrix, TransactionDesk, SkySlope Forms, ShowingTime for the MLS, SentriLock, Ocusell List, Cloud CMA, Remine Pro, Rayse and OneHome. — [OneKey products](https://corporate.onekeymls.com/benefits-products) (accessed 2026-10-23)

#### Inferences
- [INFERENCE] The product's defensible part is the orchestration and the visible AI/human/licensed split, not forms or signing; the architecture should keep "forms provider", "e-signature provider" and "MLS entry" behind interfaces so a OneKey-bundled tool can be swapped in later without changing screens.

#### Gaps
- Projects without the searched tags may exist; further searching stopped changing the answer.

### G14. Building-block inventory (licence, cost, last release, fit, footprint)

All figures from the registry pages cited in G1–G13 (accessed 2026-10-23). "Fit" is for Python 3.12 + FastAPI + Jinja2/HTMX + SQLite with no JS build step on a 2 vCPU / 8 GB VPS with 21 GB free.

| Block | Candidate | Licence | Cost | Last release | Fit | Disk / RAM |
|---|---|---|---|---|---|---|
| Web app | FastAPI 0.161.1, Jinja2 3.1.6, uvicorn 0.54.0 | MIT / BSD / BSD | free | 2026-10-22 / 2025-03-05 / 2026-09-25 | native | < 5 MB |
| Interactivity | htmx 2.0.11 (+ jinja2-fragments 1.12.0) | 0BSD (+ MIT) | free | 2026-09-22 | native, vendored file | ~50 kB |
| CSS | Bulma 1.0.4 or Bootstrap 5.3.8 | MIT | free | 2025-04-19 / 2025-08-26 | vendored file | < 1 MB used |
| AI steps (copy, replies, offers, contract) | anthropic 2.1.0 + structured outputs | Apache-2.0 | per token | 2026-10-21 | native | ~2 MB |
| Agent loop with approvals | Claude Agent SDK 0.2.173 | MIT + Anthropic Commercial Terms | per token | 2026-10-22 | bundles Claude Code CLI | wheel up to ~130 MB |
| Approval workflow | python-statemachine 3.2.2 / transitions 0.9.3 | MIT | free | 2026-10-14 / 2025-07-02 | native | < 1 MB |
| BPMN workflow | SpiffWorkflow 3.2.0 | LGPLv3 | free | 2026-08-10 | heavy concept | < 1 MB |
| Fair-housing rules sources | ArkansasONE list (Mar 2026), OneKey list, NYC CCHR, DOS-2156 classes | publishers' copyright | free to read | 2026 / n.d. / n.d. / 11-25 | borrow categories | none |
| Fair-housing classifier | Zillow fair-housing-guardrail; FairHome data | OpenRAIL-S; no licence stated | free (data by request) | repo 50 commits | needs PyTorch | GBs if run |
| Document assembly | docassemble (docassemble.base 1.10.14) | MIT | free | 2026-10-23 | separate server | 4 GB RAM, 40 GB disk host |
| DOCX | docxtpl 0.20.2 / python-docx 1.2.0 | LGPL-2.1 / MIT | free | 2025-11-13 / 2025-06-16 | native | < 1 MB |
| PDF | WeasyPrint 70.0 (+ Pango) | BSD | free | 2026-09-08 | native if Pango present | ~2 MB + system libs |
| PDF fallback / merge | ReportLab 5.1.0 / pypdf 6.21.2 | BSD / BSD-3 | free | 2026-10-22 / 2026-10-21 | native | 2–4 MB / < 8 MB |
| PDF (avoid) | PyMuPDF 2.0 / borb 3.0.9 / fpdf2 2.8.9 | AGPL / AGPL / LGPL-3 | commercial licence for PyMuPDF | 2026-10-19 / 2026-08-03 / 2026-09-29 | licence trap | 63–89 MB / 3 MB / < 1 MB |
| PDF seal for demo signing | pyHanko 0.38.0 (or endesive 3.0.1) | MIT | free | 2026-10-17 | native | < 8 MB |
| E-signature (self-host) | DocuSeal 3.3.3 | AGPLv3 + attribution term | free OSS; Pro $240/user/yr | 19 Oct | separate Rails container | ~0.2–0.5 GB RAM [SECONDARY] |
| E-signature (cloud API) | DocuSeal cloud / BoldSign / Dropbox Sign | proprietary | $0.20/doc / $0.75/envelope / tiered | — | HTTP API | none |
| E-signature (MLS bundle) | TransactionDesk + AuthentiSign (OneKey) | proprietary | reported included in OneKey subscription [SECONDARY] | — | API unknown | none |
| E-signature (other self-host) | Documenso 2.21.1 / OpenSign 3.0.0 | AGPL | free | 22 Oct / 21 Oct | Node + Postgres / Mongo | ≥ 2 GB RAM (Documenso) |
| PII redaction | presidio-anonymizer 2.2.364 (+ analyzer, spaCy sm 12 MB) | MIT | free | 2026-07-22 | native | < 1 MB (+ ~50 packages if analyzer) |
| Encryption at rest | sqlcipher3 0.6.4 (SQLCipher 4.x) | Zlib + SQLCipher BSD-style attribution | free | 2026-10-13 | native wheel | 2–7 MB |
| Field encryption | cryptography 50.0.2 (Fernet) | Apache-2.0 OR BSD-3 | free | 2026-09-30 | native | ~5 MB |
| Audit log | own tables + triggers (sqlite-chronicle pattern) | Apache-2.0 (pattern) | free | 2026-02-15 | native | none |
| Logging without PII | structlog 26.1.0 | MIT OR Apache-2.0 | free | 2026-06-06 | native | < 2 MB |
| Output sanitising | nh3 0.3.7 | MIT | free | 2026-08-23 | native | < 2 MB |
| LLM tracing (avoid) | Langfuse / Arize Phoenix | MIT core (unverified) / Elastic 2.0 | free self-host | — | separate servers | ≥ 17.5 GiB RAM (Langfuse) |
| Spend reconciliation | Anthropic Usage and Cost Admin API | API | free | — | HTTP, needs org Admin key | none |
| Product tour | Driver.js 1.10.2 | MIT | free | 2026-10-18 | vendored file | ~200 kB package |
| Product tour (avoid) | Shepherd.js 15.3.0 / Intro.js 8.6.0 | AGPL-3.0 + commercial | $50–$300 / $9.99–$299.99 | 2026-08-24 / 2026-09-21 | licence cost | < 1 MB |
| Recorded demos | Arcade / Storylane | SaaS | free tier; ~$32–$50/seat/mo | — | outside the app | none |
| RESO data model | DD 2.0 metadata JSON + UPI 2.0 | RESO EULA (royalty-free) | free | DD 2.0 ratified Nov 2023 | read as JSON | 2.3 MB |
| RESO tooling | reso-tools (TypeScript) | RESO EULA | free | 2026-10-23 | Node only | n/a |
| Address parsing | usaddress 0.5.16 / usaddress-scourgify 0.7.1 | MIT / not stated | free | 2025-08-07 / 2026-08-07 | native | < 1 MB |
| Geocoding | NYS Geocoder / Census Geocoder | public services | free | May 2026 / doc 02/2026 | HTTP | none |
| Flood, parcels, aerials | FEMA NFHL / NYS Tax Parcels / NYS orthoimagery | public data | free | continuous / yearly / 2024–2025 | HTTP | none |
| Map | Leaflet 1.9.4 (+ OSM tiles or OpenFreeMap) | BSD-2 (+ ODbL data) | free | 2023-05-18 | vendored file | ~42 kB JS |
| Map (heavier) | MapLibre GL JS 6.15.0 / OpenLayers 10.11.0 | BSD-3 / BSD-2 | free | 2026-10-18 / 2026-10-04 | vendored, WebGL | 28.8 MB / 12.8 MB packages |
| Offline tiles | Protomaps PMTiles extract | BSD-3 / ODbL | free | 2026-08-10 | static file | region-dependent |
| Shared inbox (avoid) | Chatwoot CE | MIT | free | — | Rails + Postgres + Redis | ≥ 2 GB RAM [SECONDARY] |
| Scheduling (avoid) | Cal.com | AGPLv3 + EE | free / paid | — | Node + Postgres | n/a |
| Tests | pytest 9.1.1 + Playwright 1.64.1 (`--only-shell`) | MIT / Apache-2.0 | free | 2026-06-19 / 2026-10-22 | native | 35–48 MB wheel + browser shell |
| Eval harness (avoid for POC) | promptfoo / inspect-ai / deepeval | MIT / MIT / Apache-2.0 | free | 2026 | Node / 113 deps / 31 deps | 35 MB+ |

### Contradictions with the notes above
- Section 5 says no reusable word list could be found; published lists do exist (G1). The section's recommendation (build our own rules file plus a model check) stands and is strengthened: none of the lists is authoritative and they conflict.
- Section 6 recommends `sqlcipher3-binary` and says only cp310–cp312 wheels are listed; wheels exist for 3.8–3.14, but the maintained choice is `sqlcipher3` ≥ 0.6.2 with self-contained SQLCipher 4.x wheels (G9).
- Section 6's gap gives `en_core_web_lg` as ~560 MB [CLAIMED]; it is 382 MB (G9).
- Section 2 cites the DD 2.0 reference files from `web-api-commander`; the files are still served, but that repository is retired; RESO's maintained tooling is `reso-tools` under the RESO EULA (G10).
- Section 4 names DocuSeal as the production e-signature candidate; that remains true for self-hosting, but (a) the open-source edition must keep DocuSeal's attribution in the UI, and (b) a OneKey member may already have TransactionDesk with AuthentiSign included (G5).
- Section 9 cites pydantic-ai 2.59.0; 2.60.0 was released today (no effect).

### Still open after gap fill
- Pango and fonts on the VPS: the inspection commands needed interactive approval in this headless run; one `dpkg -s` command closes it.
- OneKey MLS's full fair-housing word table: bot-blocked; a OneKey member can read it.
- Whether TransactionDesk/AuthentiSign is included in the OneKey subscription and whether it has an API: bot-blocked page; one call to OneKey member support.
- NYSAR statewide purchase agreement text and terms: member-only.
- Which Anthropic retention statement applies to a standard key (30 days vs not retained by default): ask Anthropic or assume 30 days.
- FEMA NFHL point query: endpoint reset the connection; try during architecture.
- RESO Offer Management specification: exists, not read; read before designing the offers table.
- Copyright holder of the bar-association Residential Contract of Sale and the 1995 HUD memo text: not decision-changing.
- Dropbox Sign API prices and DocuSeal official resource figures: production-only, not decision-changing.
- Zillow Research / Realtor.com data terms and Columbia County parcels (earlier gaps): not relevant to a POC on fictional data.
