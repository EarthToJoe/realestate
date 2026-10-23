# Traceability matrix

Every POC feature traces to an agent function from workstream 1 (`docs/research/WS1-agent-functions.md`, F1 to
F89) that it replaces, and to a constraint from workstream 2 (`docs/research/WS2-legal-licensing.md`, L1 to L62).
WS3 IDs (C = channel, D = data feed, R = rule) come from `docs/research/handoff/WS3.md`. Record codes (CP-xx) and
kinds are defined in `docs/specs/poc-architecture.md`, section 3. A row without an F-ID and an L-ID is not built.

Written 2026-10-23 from the architecture spec; **revised 2026-10-23 for decision 21** (the AI is the agent on both
sides and performs every agent act, including the functions WS1 classes "human or licence required", each with a
red "NY law today" marker; the seller and the buyer make their own decisions). Status is updated as the build lands
(planned → built → tested).

**In the demo** = who performs it in the product: **AI**, **seller**, **buyer**, **third party** (planned, named
on the timeline), **human required** (a practical step with no software route). **NY law today** = the marker text
in a few words (full sentence, IDs and link in `app/records/catalogue.yaml`), or "none". Record kinds: CD
client_decision, LM law_marker, HR human_required, TP third_party, AU automated.

| Feature (module / screen) | SC # | WS1 functions replaced (F-IDs) | WS2 constraints respected (L-IDs) | Record | In the demo | NY law today | Status |
|---|---|---|---|---|---|---|---|
| `intake` / Address and facts form, "Use demo house" | 1 | F14 | L48, L60 (four §242 questions asked) | none (data entry) | seller, AI | none | planned |
| `intake` / Property profile with source chips (seller, public record, inferred) via `PublicRecordConnector` stub | 1 | F14 | L18, L54 (inferences labelled, no false claims) | none (AI work shown) | AI | none | planned |
| `intake` / Disclosure checklist (PCDS, lead paint, ag district, §242) | 1 | F15, F59 | L43, L44, L46, L60 | CP-04 CD | AI builds; seller completes the PCDS (never pre-filled) | none | planned |
| `intake` / Onboarding notices (agency form, DOS-2156, not-legal-services) | 1 | F8, F9, F10 | L12, L29, L39 | CP-24 AU; CP-01 CD | AI sends; seller acknowledges | none | planned |
| `intake` / Listing presentation, flat fee, conflicts check, listing acceptance | 1 | F5, F7, F12 | L1, L5, L14 | CP-02 LM | AI | Accepting a listing for a fee: licensed broker | planned |
| `intake` / Listing agreement with six-point exclusive-listing explanation | 1 | F13 | L9, L14, L34 | CP-03 CD | AI generates; seller signs | none (the firm is the contracting party; see CP-35) | planned |
| `pricing` / Comparable sales table, adjustments, range, net sheet ("not an appraisal") | 2 | F21, F25 | L6 (preparatory work), WS3-D5 | none (AI work shown) | AI | none | planned |
| `pricing` / AI's recommended list price with reasoning | 2 | F22, F24 | L6, L18, WS3-D5 | CP-25 LM | AI | Price advice: listing agent's fiduciary duty (licensed broker) | planned |
| `pricing` / Seller's list-price choice | 2 | F22, F24 | L9, WS3-R9 | CP-05 CD | seller | none | planned |
| `copy` / Drafts: MLS remarks, portal description, 3 social posts, flyer (PDF) with DEMONSTRATION mark | 3 | F26, F31 | L9, L10, L54, WS3-R6, WS3-R8 | goes to CP-26, CP-06 | AI | see CP-06 | planned |
| `fairhousing` / Rules pass + model review + fixed version, planted-violation button, block on fail | 3, 5, 10 | F26, F78, F81 | L36, L37, L41, L58, L59, L61 | CP-26 AU | AI (software gate) | none | planned |
| `copy` / MLS rule pre-check (required fields, no compensation, not "free") | 3 | F28, F85 | L16, WS3-R6, WS3-R7 | feeds CP-08 | AI | none | planned |
| `copy` / AI marks passing copy "ready to publish" | 3 | F26, F76 | L10, L18, L36 | CP-06 LM | AI | Only the broker places and approves ads (licensed broker) | planned |
| `channels` / Channel board: OneKey MLS card with prepared listing package (`MLSConnector` stub) | 4 | F28 | L1, L16, WS3-C1 | CP-08 HR | human required (licensed MLS participant or Administrative User) | MLS participation needs a broker licence (shown in the HR marker) | planned |
| `channels` / Portal cards fed from MLS (Zillow, Realtor.com, Redfin, Homes.com, OneKeyMLS.com) | 4 | F29 | L16, WS3-C4, C8 to C10, C12, WS3-D7 (never scraped) | one-time setup notes (claim profile, Keystone switches) | AI (status); human required (one-time setup) | none | planned |
| `channels` / Firm website card with Clear Cooperation clock | 4 | F30 | L20 (pending), WS3-C13, WS3-R1 | none (automatic block until MLS entry recorded) | AI | none | planned |
| `channels` / Social, Google Business Profile, Meta/Nextdoor cards (drafted, scheduled, posting stubbed) | 4 | F30 | L10, L38, WS3-C14, WS3-C15 | covered by CP-06 | AI | see CP-06 | planned |
| `channels` / Vendor cards: photos, sign, lockbox; open house | 4 | F20, F27, F31, F38, F40 | L10 (sign names the firm), L19, WS3-R3, WS3-R8 | CP-10 HR for the open house | AI books; third party installs; seller hosts | none for the owner; a non-owner host would be a licensed showing (L19) | planned |
| `channels` / Marketing-exposure choice and seller authorisations | 4 | F32, F38 | L9, L20 (pending), WS3-R2, WS3-R3 | CP-07 CD | seller | none | planned |
| `inbox` / Seller's fact sheet and the AI's negotiating authority | 5 | F33, F84 | L9, L18 | CP-27 CD | seller | none | planned |
| `inbox` / Shared inbox; AI answers and sends (simulated) from the fact sheet, within authority; seller sees only the seller's decisions | 5 | F2, F33, F34, F83 | L18, L23, L37, L59 (same response target for all) | CP-09 LM (per message that discusses the listing, negotiates or advises) | AI; seller decides only seller decisions | Discussing listings with prospects and negotiating: licensed broker | planned |
| `inbox` / First-contact disclosures attached; firm identity block on every message | 5 | F8, F10 | L10, L12, L39 | CP-24 AU | AI | none | planned |
| `inbox` / Outbox "sent (simulated)" (`MessageTransport` stub), fair-housing check on every message | 5 | F2, F33, F78 | L10, L36, L50 to L52 (no real sends) | CP-26 AU | AI | none | planned |
| `inbox` / Legal and school/neighbourhood questions answered neutrally | 5 | F36, F53 (declined, as an agent does) | L23 (no legal advice; never discourage a lawyer), L37 | none | AI | none (the AI gives no legal advice) | planned |
| `inbox` / Showing scheduler (24 h), access instructions, feedback log | 5 | F37, F42 | L15, WS3-R4, WS3-R5 | CP-29 AU | AI | none (scheduling is permitted to unlicensed staff, WS3-R4) | planned |
| `inbox` / Owner-hosted showing | 5, 8 | F39 | L19 | CP-10 HR | seller (owner opens the door) | none (the owner may show their own home) | planned |
| `inbox` / Self-guided tour (owner's own smart lock) | 5, 8 | F39 | L15, L19, WS3-R4 (OneKey Rule 405.8) | CP-28 LM | AI arranges | Unaccompanied tours unresolved; DOS treated unlicensed showing as unlicensed activity (licensed broker) | planned |
| `offers` / Offer comparison table and net sheets | 6 | F46, F65 | L1, L24 | none (AI work shown) | AI | none | planned |
| `offers` / AI presents every offer and advises with reasoning | 6 | F45, F47, F84 | L1, L18 | CP-11 LM | AI | Presenting offers and advising: licensed broker | planned |
| `offers` / Seller decides: accept, counter or reject | 6 | F47 | L24 | CP-12 CD | seller | none | planned |
| `offers` / AI negotiates the counter with the other side; code checks it against the seller's decision | 6, 8 | F48, F49 | L1, L18, L24 | CP-13 LM (per side) | AI | Negotiating price, terms, concessions: licensed broker | planned |
| `contract` / Accepted-offer memorandum to both parties | 7 | F50 | L24 | CP-32 AU | AI | none | planned |
| `contract` / Contract draft + rider, side-by-side with the standard form structure, page labels | 7 | F52, F54 | L21, L22, L23, L25 | CP-14 LM | AI | Drafting a contract for another is the practice of law (attorney) | planned |
| `contract` / Disclosures attached (PCDS, lead paint, ag district, §242); signing blocked until PCDS delivered | 7 | F59 | L43, L44, L46, L60 | CP-32 AU | AI | none | planned |
| `contract` / Signing map: e-signable vs wet ink and notary (`SignatureProvider` stub) | 7 | F67 | L34, L35, L45 | CP-15 HR | human required (notary; the parties in ink) | none (practical; shown as human required) | planned |
| `contract` / Seller and buyer sign the contract (simulated e-sign) | 7 | F59 | L24, L34, L43 | CP-33 CD | seller, buyer | none | planned |
| `buyer` / Buyer intake + representation disclosure | 8 | F6, F9, F18, F19 | L11, L12, L29, L37, L39 | CP-24 AU; CP-16 CD (part 1) | AI; buyer acknowledges | none | planned |
| `buyer` / AI takes on the buyer as a client and records the agency relationship | 8 | F11, F12 | L1, L5, L13 | CP-30 LM | AI | Taking a client and deciding the agency relationship: licensed broker | planned |
| `buyer` / Search alerts on fictional listings (`IDXConnector` stub) | 8 | F35, F36 | L37, WS3-D1, WS3-D6 | none (no steering filters) | AI | none | planned |
| `buyer` / Tour request blocked until buyer agreement signed | 8 | F17, F37 | L15, WS3-R5 | CP-16 CD; then CP-29, and CP-10 or CP-28 | buyer signs; AI books | see CP-28 for a self-guided tour | planned |
| `buyer` / Dual-agency consent (buyer wants the firm's own listing); information wall between the two AIs | 8 | F11, F51 | L13 | CP-17 CD | seller and buyer consent; AI keeps the wall | Designated agents must be two licensees (in the CP-30 marker) | planned |
| `buyer` / AI advises on offer price and terms and drafts the offer | 8 | F23, F43, F44 | L6, L18, L22, L24 | CP-31 LM | AI | Advising the buyer on price: buyer's agent's fiduciary duty (licensed broker) | planned |
| `buyer` / Buyer approves the offer and the reply to the counter | 8 | F44 | L24 | CP-18 CD | buyer | none | planned |
| `timeline` / Deal dashboard coloured AI / client decided / NY law today / third party, built from records | 9 | F34, F63 | L5, L17 | displays all records | AI (display) | shows every marker | planned |
| `timeline` / Hurdle map: every red marker with rule, who the law says, link; header counts | 9 | F89 (evidence of what the law requires, by step) | L1, L5, L18, L21 | displays every LM, HR, TP | AI (display) | shows every marker | planned |
| `timeline` / Planned: deposit escrow, inspection, mortgage, appraisal, title, walkthrough, closing | 9 | F55, F56, F57, F60, F61, F62, F66, F67, F68 | L25, L33, L35 | CP-20, CP-21, CP-22, CP-23 TP | third party | none (planned third-party steps) | planned |
| `timeline` / Planned: AI negotiates repairs or credits and writes them into the contract; keeps the deal together | 9 | F58, F64 | L1, L21 | CP-34 LM (planned) | AI | Negotiating repairs (licensed broker); amending the contract (attorney) | planned |
| `timeline` / Agent-acts log (every AI agent act with its marker) | 9 | F75, F69 | L5, L6, L17, L61 | display of every LM | AI (display) | shows every marker | planned |
| Platform / Brokerage identity block on every page and message; standing broker-of-record marker | under the hood, 5, 9 | F73, F74, F75 | L2, L3, L4, L5, L10 | CP-35 LM (standing) | AI (the firm) | A licensed broker must run and supervise the firm (licensed broker) | planned |
| `brand` / Brokerage campaign: landing page, local ad, seller lead magnet (founder named) | 10 | F1, F3, F4 | L10, L40, L41, L54, L55 | CP-26 AU | AI | see CP-19 | planned |
| `brand` / Ad targeting panel (allowed criteria only) | 10 | F30 | L38, L58 | covered by CP-19 | AI | none | planned |
| `brand` / AI publishes the campaign (simulated) | 10 | F1, F76 | L10, L18, L38 | CP-19 LM | AI | Only the broker places and approves ads (licensed broker) | planned |
| `demo` / Start demo, step list, narration cards, Driver.js, generated `DEMO-SCRIPT.md`, live/replay badge | 11 | all of the above (presentation layer) | L54 (replay labelled, never passed off as live), L55 | none | Presenter | none | planned |
| Platform / `ModelProvider` interface, model-call spend log, spend cap | under the hood | F2, F26 (enabler) | L18, L56 | none | AI | none | planned |
| Platform / Record service: five kinds, client-decision gates enforced server-side, `catalogue.yaml`, persona roles | under the hood | F75, F84 | L1, L5, L18, L24 | enforces every CD; writes every LM, HR, TP, AU | AI | none | planned |
| Platform / `AgentContext(side)` information wall and its test | under the hood | F51, F84 | L13 | none | AI | none | planned |
| Platform / PII registry, Fernet columns, model-context whitelist, access log, export, delete, log masking | under the hood | F87, F69 | L17, L56, L57 | none | AI | none | planned |
| Platform / Append-only audit log with hash chain | under the hood | F69, F75 | L17, L61 | none | AI | none | planned |

## The 21 "human or licence required" functions

From WS1 "Counts and the true bottleneck list". Under decision 21 the AI performs each one the demo covers, with a
red marker; the rest are listed with the reason.

| F-ID | Function | In the demo |
|---|---|---|
| F4 | Win clients through referrals, reputation and local relationships | Step 10: the campaign names the founder as the trusted person; the narration says relationship work stays with people. No marker: a practical trust function, not a legal rule. |
| F11 | Decide and document the agency relationship | AI, CP-30 marker (step 8); both clients consent at CP-17 (L13). |
| F12 | Accept the listing or client | AI, CP-02 marker (step 1) and CP-30 (buyer, step 8) (L1, L5). |
| F39 | Conduct showings and private tours | Owner-hosted showing, CP-10 human required (owner may show their own home, L19); self-guided tour arranged by the AI, CP-28 marker. The AI cannot be on site. |
| F40 | Host open houses | Owner hosts, CP-10 human required (step 4 card). |
| F47 | Advise the client on each offer and convey every one | AI, CP-11 marker (step 6) (L1). |
| F48 | Negotiate price and terms | AI, CP-13 marker, both sides (steps 6 and 8) (L1); also CP-09 on negotiating messages. |
| F49 | Negotiate buyer-broker pay and seller concessions | AI, CP-13 marker: concessions are a field in the offer and the counter. |
| F51 | In-house deals and competing buyers | Offer B comes from the firm's own buyer; CP-17 consent; separate seller and buyer AIs behind an information wall (decision 24); the CP-30 marker says designated agents must be two licensees. |
| F52 | Draft the contract of sale and negotiate its legal terms | AI drafts in the contract step, CP-14 marker (attorney) (L21, L22, L25). |
| F53 | Give legal advice | Not performed: the AI declines party-specific legal questions, as an agent does (L23); no marker because no reserved act is done. |
| F55 | Hold the down payment in escrow | CP-20, third party, planned (custom: the seller's attorney's escrow, L25). |
| F58 | Negotiate repairs or credits after inspection | AI, CP-34 marker, planned (step 9). |
| F64 | Keep the deal together when something goes wrong | AI, CP-34 marker, planned; not acted (the demo runs the happy path). |
| F73 | Hold the broker licence | CP-35 standing marker in the identity block and on the timeline (L2, L3, L4). |
| F74 | Keep a NY place of business, sign, displayed licence | Office address in the identity block (L4, L10); covered by the CP-35 marker. |
| F75 | Supervise licensees and control unlicensed staff and systems | CP-35 standing marker (L5); the agent-acts log shows what a supervising broker would review. |
| F82 | Disclose the broker's own interests | Not in the demo (see below). |
| F84 | Counsel the client and exercise fiduciary judgement | AI, shown by CP-25, CP-11 and CP-31 (the AI advises, the client decides) and CP-27 (the AI acts within the seller's authority, confidential facts walled). No separate record. |
| F88 | Carry insurance and manage business risk | Not in the demo (see below). |
| F89 | Answer regulators and disputes | Not a screen; the audit log, access log, fair-housing results and hurdle map (L17, L61) are the records a response would use. |

## Not in the demo

WS1 functions no feature row replaces, and why.

| F-ID | Function | Why not in the demo |
|---|---|---|
| F16 | Advise on preparing the home (optional pre-listing inspection) | Needs eyes on the house; the inspection add-on is WS6's subject and Q43 is open. |
| F41 | Live virtual tours | Needs a person on video; would add a screen without a new hurdle (the buyer-agreement gate, L15, is already shown). |
| F70 | Pay out commissions and client rebates | Payments are out of scope (`docs/OUT-OF-SCOPE.md`). |
| F71 | After-sale service | The demo ends at closing. |
| F72 | Ask for reviews and referrals | After the sale; no testimonials may be generated (L54). |
| F77 | Institute, notarize, post and archive SOPs | Standing paperwork; the uniform SOP gate itself (F18) is in buyer intake. |
| F79 | Administer an escrow account | The firm holds no money; the deposit sits with a third party (CP-20). |
| F80 | Check every payment against compensation rules | No payments in the POC. |
| F82 | Disclose the broker's own interests | No self-interest in the demo deal; launch work in `docs/PLAN.md`. |
| F86 | Onboard, train and sponsor licensees | No licensees in the demo (decision 21). |
| F88 | Carry insurance and manage business risk | A business matter with no screen; launch work in `docs/PLAN.md`. |
