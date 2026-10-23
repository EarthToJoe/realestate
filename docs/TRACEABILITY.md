# Traceability matrix

Every POC feature traces to an agent function from workstream 1 (`docs/research/WS1-agent-functions.md`, F1 to
F89) and respects a constraint from workstream 2 (`docs/research/WS2-legal-licensing.md`, L1 to L62). WS3 IDs
(C = channel, D = data feed, R = rule) come from `docs/research/handoff/WS3.md`. Checkpoint codes (CP-xx) are
defined in `docs/specs/poc-architecture.md`, section 3. A row without an F-ID and an L-ID is not built.

Written 2026-10-23 from the architecture spec. Status is updated as the build lands (planned → built → tested).
Who acts: **L** licensed broker or sponsored licensee, **A** attorney, **H** seller or buyer, **T** third party,
**AI** automated and logged.

| Feature (module / screen) | Success criterion # | Agent functions (F-IDs) replaced or assisted | Legal constraints respected (L-IDs) | Checkpoint (who acts, why) | Status |
|---|---|---|---|---|---|
| `intake` / Address and facts form, "Use demo house" | 1 | F14 | L48, L60 (four §242 questions asked) | none (data entry) | planned |
| `intake` / Property profile with source chips (seller, public record, inferred) via `PublicRecordConnector` stub | 1 | F14 | L18, L54 (inferences labelled, no false claims) | none (AI work shown) | planned |
| `intake` / Disclosure checklist (PCDS, lead paint, ag district, §242) | 1 | F15, F59 | L43, L44, L46, L60 | CP-04: H, the seller completes the PCDS; the software does not help fill it (NYSAR advice via WS7) | planned |
| `intake` / Seller onboarding notices (agency form, DOS-2156, not-legal-services) | 1 | F8, F9 | L12, L29, L39 | CP-01: H acknowledges agency form (L12); CP-24: AI delivers fair-housing notice, logged (L39) | planned |
| `intake` / Accept listing and listing agreement | 1 | F12, F13, F7 | L1, L5, L9, L14, L34 | CP-02: L accepts after conflicts check (licensed act); CP-03: H and L sign (written authority before marketing) | planned |
| `pricing` / Comparable sales table, adjustments, range, net sheet | 2 | F21, F25 | L1, L6 (CMA is preparatory; labelled not an appraisal); WS3-D5 | none until review | planned |
| `pricing` / Broker review and list-price choice | 2 | F22, F24 | L1, L18 | CP-05: L reviews and advises, H chooses the price; the AI never sets it | planned |
| `copy` / Drafts: MLS remarks, portal description, 3 social posts, flyer (PDF) with DEMONSTRATION mark | 3 | F26, F31 | L9, L10, L54, WS3-R6, WS3-R8 | goes to CP-06 | planned |
| `fairhousing` / Rules pass + model review + fixed version, planted-violation button | 3, 5, 10 | F26, F78, F81 | L36, L37, L41, L58, L59, L61 | blocks the approval gate until clean | planned |
| `copy` / MLS rule pre-check (required fields, no compensation, not "free") | 3 | F28, F85 | L16, WS3-R6, WS3-R7 | feeds CP-08 | planned |
| `copy` / Broker approval before "ready to publish" | 3 | F26, F76 | L10, L18, L36 | CP-06: L approves every advertisement (broker places all advertising) | planned |
| `channels` / Channel board: OneKey MLS card with prepared listing package (`MLSConnector` stub) | 4 | F28 | L1, L16, WS3-C1 | CP-08: L keys the listing into OneKey; no listing-input API exists | planned |
| `channels` / Portal cards fed from MLS (Zillow, Realtor.com, Redfin, Homes.com, OneKeyMLS.com) | 4 | F29 | L16, WS3-C4, C8 to C10, C12, WS3-D7 (never scraped) | one-time setup markers (L: claim profile, Keystone switches) | planned |
| `channels` / Firm website card with Clear Cooperation clock | 4 | F30 | L20 (pending), WS3-C13, WS3-R1 | none (automatic block until MLS entry recorded) | planned |
| `channels` / Social, Google Business Profile, Meta/Nextdoor cards (drafted, scheduled, posting stubbed) | 4 | F30 | L10, L38, WS3-C14, WS3-C15 | covered by CP-06 | planned |
| `channels` / Vendor cards: photos, sign, lockbox; open house | 4 | F20, F27, F31, F38, F40 | L10 (sign names broker), L19, WS3-R3, WS3-R8 | marker: L hosts open houses (F40); seller signs lockbox authorisation | planned |
| `channels` / Marketing-exposure choice | 4 | F32 | L9, L20 (pending), WS3-R2 | CP-07: H signs the exposure form | planned |
| `inbox` / Shared inbox with simulated enquiries; AI reply drafts from approved fact sheet | 5 | F2, F33 | L18, L23, L37, L59 (same response target for all) | escalation marker for price, terms, legal, school questions | planned |
| `inbox` / First-contact disclosures attached; broker identity block on every message | 5 | F8, F10 | L10, L12, L39 | CP-24 (AI, logged) | planned |
| `inbox` / Approve / edit / send gate; Outbox "sent (simulated)" (`MessageTransport` stub) | 5 | F2, F33, F34, F75 | L5, L10, L18, L50 to L52 (no real sends) | CP-09: L approves each outgoing message; software's acts are the broker's | planned |
| `inbox` / Showing scheduler (24 h), access instructions, feedback log | 5 | F37, F42 | L15, L19, WS3-R4, WS3-R5 | CP-10: L or the owner opens the door; showings are licensed | planned |
| `offers` / Offer comparison table and net sheets | 6 | F46, F65 | L1, L22, L24 | goes to CP-11 | planned |
| `offers` / AI counter draft with reasoning | 6 | F48 (assisted), F49 (assisted) | L1, L18, L22 | CP-13: L sends the approved counter; negotiation is licensed | planned |
| `offers` / Present offers and seller decision | 6 | F45, F47 | L1, L24 | CP-11: L presents every offer and advises; CP-12: H decides; the AI never accepts or rejects | planned |
| `contract` / Accepted-offer memorandum to both attorneys | 7 | F50, F54 | L22, L23, L24, L25 | hand-off to CP-14 | planned |
| `contract` / Attorney workspace: draft contract + rider, side-by-side with the standard form structure | 7 | F52 (assisted, for the attorney), F53 | L21, L22, L23, L25, L29 | CP-14: A drafts and reviews; only lawyers may draft instruments | planned |
| `contract` / Disclosures attached (PCDS, lead paint, ag district, §242) | 7 | F59 | L43, L44, L46, L60 | none (automatic attachment; blocks if PCDS missing) | planned |
| `contract` / Signing map: e-signable vs wet ink and notary (`SignatureProvider` stub) | 7 | F67 | L34, L35, L45 | CP-15: A and notary at closing (deed acknowledgment, POA) | planned |
| `buyer` / Buyer intake + representation disclosure | 8 | F6, F9, F18, F19 | L11, L12, L29, L37, L39 | CP-16 (part 1): H acknowledges agency form | planned |
| `buyer` / Search alerts on fictional listings (`IDXConnector` stub) | 8 | F35, F36 | L37, WS3-D1, WS3-D6 | none (no steering filters) | planned |
| `buyer` / Tour request blocked until buyer agreement signed | 8 | F17, F37, F39 | L15, L19, WS3-R5 | CP-16: H and L sign buyer agreement before any tour; CP-10 for the tour | planned |
| `buyer` / Dual-agency consent (buyer wants the firm's own listing) | 8 | F11, F51 | L13 | CP-17: L records the relationship; both parties consent | planned |
| `buyer` / AI-drafted offer with buyer approval gate | 8 | F44, F23 | L22, L24 | CP-18: H approves; then CP-11 on the seller side | planned |
| `timeline` / Deal dashboard coloured AI / human / licensed or attorney, built from checkpoint records | 9 | F34, F63, F60 | L5, L17 | displays all CPs; planned CP-20 to CP-23 | planned |
| `timeline` / Planned steps: deposit escrow, inspection, mortgage, appraisal, title, walkthrough, closing | 9 | F55, F56, F57, F58, F61, F62, F64, F66, F67, F68 | L25, L33, L35 | CP-20: A holds deposit; CP-21: T inspects, L negotiates repairs; CP-22: T; CP-23: A and T close | planned |
| `timeline` / Supervision log (every broker approval) | 9 | F75, F69 | L5, L17, L61 | display of CP-02, 05, 06, 08, 09, 11, 13, 17, 19 | planned |
| `brand` / Brokerage campaign: landing page, local ad, seller lead magnet | 10 | F1, F3, F4 (founder named) | L10, L40, L41, L54, L55 | goes to CP-19 | planned |
| `brand` / Ad targeting panel (allowed criteria only) | 10 | F30 | L38 | covered by CP-19 | planned |
| `brand` / Broker approval of the campaign | 10 | F1, F76 | L10, L18 | CP-19: L approves brokerage advertising | planned |
| `demo` / Start demo, step list, narration cards, Driver.js, generated `DEMO-SCRIPT.md`, live/replay badge | 11 | all of the above (presentation layer) | L54 (replay labelled, never passed off as live), L55 | none | planned |
| Platform / `ModelProvider` interface, model-call spend log, spend cap | under the hood | F2, F26 (enabler) | L18, L56 | none | planned |
| Platform / Checkpoint service (server-enforced gates, persona roles) | under the hood | F75 | L1, L5, L6, L18 | enforces every CP | planned |
| Platform / PII registry, Fernet columns, model-context whitelist, access log, export, delete, log masking | under the hood | F87, F69 | L17, L56, L57 | none | planned |
| Platform / Append-only audit log with hash chain | under the hood | F69, F75 | L17, L61 | none | planned |
| Platform / Brokerage config (name, licence, office address) on every page | under the hood | F73, F74 | L3, L4, L10 | none | planned |

## The 21 "Human or licence required" functions

From WS1 "Counts and the true bottleneck list". Each is shown at a checkpoint in the demo or marked not in the POC.

| F-ID | Function | Where the demo shows it |
|---|---|---|
| F4 | Win clients through referrals, reputation and local relationships | Not a checkpoint: relationship work. Step 10 names the founder as the trusted person in the brokerage campaign, and the narration says so. |
| F11 | Decide and document the agency relationship | CP-17 (step 8): dual-agency consent screen, L records the relationship (L13). |
| F12 | Accept the listing or client | CP-02 (step 1): broker accepts after a conflicts check (L1, L5). |
| F39 | Conduct showings and private tours | CP-10 (steps 5 and 8): "licensee or owner opens the door" (L19). |
| F40 | Host open houses | Step 4 channel board: open-house card marked "licensee hosts" (L19). |
| F47 | Advise the client on each offer and convey every one | CP-11 (step 6): broker presents every offer and advises (L1). |
| F48 | Negotiate price and terms | CP-13 (step 6): AI drafts the counter; broker sends it (L1, L18). |
| F49 | Negotiate buyer-broker pay and seller concessions | CP-13 (step 6): concessions are a field in the offer table; the broker negotiates them. |
| F51 | In-house deals and competing buyers | CP-17 (step 8) and step 6: one of the two offers comes from the firm's own buyer; dual-agency consent is required (L13). |
| F52 | Draft the contract of sale and negotiate its legal terms | CP-14 (step 7): seller's attorney drafts in the attorney workspace (L21, L22, L25). |
| F53 | Give legal advice | CP-14 (step 7), and step 5: legal questions in the inbox are refused and routed to a lawyer (L23). |
| F55 | Hold the down payment in escrow | CP-20 (step 9, planned): seller's attorney's escrow (L25). |
| F58 | Negotiate repairs or credits after inspection | CP-21 (step 9, planned): licensee negotiates after the inspection. |
| F64 | Keep the deal together when something goes wrong | Step 9 timeline: shown as a licensee lane on CP-21 and CP-22 (renegotiation after inspection or appraisal). Not acted: the demo runs the happy path. |
| F73 | Hold the broker licence | Not a checkpoint: standing requirement. Broker licence number in the brokerage config, shown on every page and advertisement (L3, L10). |
| F74 | Keep a NY place of business, sign, displayed licence | Not a checkpoint: standing requirement. Office address in the identity block on every page (L4, L10). |
| F75 | Supervise licensees and control unlicensed staff and systems | Step 9 supervision log built from every broker approval (CP-02, 05, 06, 08, 09, 11, 13, 17, 19) (L5, L6). |
| F82 | Disclose the broker's own interests | Not in the POC: no self-interest in the demo deal; listed as launch work in `docs/PLAN.md`. |
| F84 | Counsel the client and exercise fiduciary judgement | Shown by the pattern at CP-05, CP-11 and CP-13: the AI drafts, the broker advises, the client decides. No separate checkpoint. |
| F88 | Carry insurance and manage business risk | Not in the POC: a business matter with no screen; listed as launch work in `docs/PLAN.md`. |
| F89 | Answer regulators and disputes | Not in the POC as a screen; the audit log, access log and fair-housing results (L17, L61) are the records a response would use. |
