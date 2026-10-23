# WS2 handoff: legal and licensing hurdles in New York (2026-10-23)

Deliverable: `docs/research/WS2-legal-licensing.md`. Notes with gap fill: `research_notes/WS2 NY legal hurdles/` (three files, each ending in "Gap fill (2026-10-23, VPS session)"). Research to plan with, to be confirmed by NY counsel; not legal advice.

## 1. Assumption status lines

- A3 | hit | UPL rules stop the software at fill-in offers, Hudson Valley custom has the seller's attorney draft the contract in all nine counties, and the founder cannot be counsel on commission deals, so the pitch must become "a cheaper, faster lawyer step", not "no lawyer". | [WS2 §2, §3, §7](../WS2-legal-licensing.md#2-the-software-may-fill-in-an-offer-only-lawyers-may-draft-or-explain-the-contract)
- A1 | still open | The law permits one licensed broker supervising software (no agent-per-deal rule), but every listing acceptance, ad, offer, counteroffer and showing needs his recorded decision, so whether it scales is a WS1/WS4 hours question. | [WS2 §1](../WS2-legal-licensing.md#1-a-licensed-broker-is-required-for-every-core-agent-act-and-software-cannot-hold-the-licence)
- A2 | dodged | Joe may own equity and take ownership distributions and sell the software for a fixed fee; any per-deal or commission-linked pay to him or his company is unlawful (RPL §442, DOS rule). DOS has not confirmed passive unlicensed ownership (low risk, one email). | [WS2 §8](../WS2-legal-licensing.md#8-joe-can-own-and-build-but-cannot-be-paid-per-deal)
- A4 | partly hit | MLS participation needs a state broker licence plus REALTOR membership, so the attorney exemption alone is not enough; the attorney route to a licence costs $185 with no exam, so this is a step, not a blocker (WS3 owns the rest). | [WS2 §1](../WS2-legal-licensing.md#1-a-licensed-broker-is-required-for-every-core-agent-act-and-software-cannot-hold-the-licence)
- A6 | partly hit | Whether an unaccompanied buyer tour is a licensed "showing" is unresolved in NY; treat showings as licensee- or owner-controlled; a passed-but-unsigned bill (A10679-B) would oblige listing agents to make homes available for showings. | [WS2 §1, §12](../WS2-legal-licensing.md#12-what-may-change-in-the-next-twelve-months)
- A8 | still open | Fair-housing rules are clear and checkable, but NY enforcement is dense (6 revocations, 21 suspensions 2020–2023; 2025–26 voucher "ghosting" and steering settlements), NY codified a disparate-effect test in Dec. 2025 that reaches automated rules, and the model's words are the evidence; POC fixture tests decide. | [WS2 §4](../WS2-legal-licensing.md#4-fair-housing-is-where-new-york-actually-punishes-brokers)
- A7 | still open (legal input) | The fixed-fee path that lets the founder be seller's counsel requires a fee paid whether or not the house sells; A10679-B would add minimum listing duties. Both bear on unit economics (WS4). | [WS2 §7](../WS2-legal-licensing.md#7-what-the-father-in-law-may-and-may-not-do)

## 2. Kill criteria

- K3 (percentage commission while acting as counsel) | dodged if the founder is broker-only in brokerage deals, or uses the fixed, non-refundable, non-contingent fee path with written consent (NYSBA Ops. 1015, 1117 fn. 1); hit if he plans to be counsel on commission deals (Ops. 1043, 1117, 1237: non-consentable).
- K4 (product pitched or built as autonomous) | confirmed as a binding constraint: licensed acts must be the licensee's own decisions (RPL §440, DOS guidance, Flagship "availing" decision); the design dodges it with recorded broker approval on every licensed act. Never pitch "autonomous agent".
- K9 (MLS membership) | dodged on the legal side if the founder takes the DOS broker licence (attorney route, $185, no exam) and joins a REALTOR board; A10679-B, if signed, would make public marketing mandatory, which favours MLS listing. WS3 owns MLS terms.
- A3's kill criterion | hit as written ("a lawyer on each side unavoidable" in practice in the Hudson Valley, and ethics bar the dual role on commission deals): the pitch becomes "cheaper, faster lawyer step".
- A1's kill criterion | not hit: no NY law requires a licensee to personally perform core acts in a way that needs an agent per deal; but each licensed decision must be his.
- A2's kill criterion | not hit: lawful structures exist (equity plus fixed software fee).
- K1, K2, K5, K6, K7, K8 | not WS2's to test; nothing found bears on them.

## 3. Questions for Joe (and his father-in-law)

1. **Will your father-in-law take the DOS broker licence and be broker of record of an LLC you co-own?** It is a paper form (DOS-0036-f-a), $185, no course or exam, plus REALTOR board membership for MLS. *Provisional: yes.* Unblocks: entity setup, MLS access (WS3), every licensed checkpoint in the POC.
2. **Broker-only, or also the seller's lawyer on some deals?** Broker-only is simplest. Being the seller's lawyer too is allowed only if the brokerage fee is fixed, non-refundable and paid whether or not the house sells, with the seller's written consent, and his legal fee billed by his law practice. He can never be the buyer's lawyer where his firm represents the seller. *Provisional: broker-only in the POC; the fixed-fee "seller legal plus listing" package shown as a future option.* Unblocks: pricing screen, contract hand-off screen.
3. **Is Joe content to be paid only through ownership distributions, salary, and a fixed software licence fee, never per deal?** *Provisional: yes.* Unblocks: business-model section of the plan.
4. **Contract step: hand off to independent lawyers?** In all nine Hudson Valley counties the seller's attorney drafts the contract. The product would stop at a fill-in offer and hand off, with a directory of local real-estate attorneys who publish flat fees (no referral payments either way). *Provisional: yes.* Unblocks: the "contract drafting" screen's scope in the POC (it becomes "offer package and attorney hand-off").
5. **Sales only, or rentals too?** Rentals bring the heaviest 2025–26 enforcement (voucher "ghosting", tenant-screening and housing-court-history cases), NYC's FARE Act and lease flood notices. *Provisional: sales only.* Unblocks: scope of the buyer flow and the screening rules.
6. **Automated texting or calling?** Marketing texts and AI-voice calls need prior written consent and NY quiet hours. *Provisional: no cold outreach; only replies and transactional messages to people who opted in.*
7. **Does the old Hudson Valley entity still exist, and does he have a malpractice carrier who will cover a lawyer who also brokers?** *Provisional: new LLC; ask his carrier.* Unblocks: entity name pre-clearance, insurance line in WS4.

## 4. Traceability items (every L-ID, one-line product consequence)

- L1 Licence for listing, marketing for a fee, offers, negotiation → software never accepts a listing, presents an offer or negotiates by itself; licensee checkpoint on each.
- L2 Unlicensed brokerage penalties → only the licensed brokerage bills consumers; no unlicensed mode of the product.
- L3 Attorney exemption personal; licence via attorney route → licence obtained before launch; licence number in product footer.
- L4 Entity licence, approved name, NY office and sign → brand string = DOS-approved name; office address on every page.
- L5 Broker must really control the business → recorded broker approval on every listing, ad, offer, counteroffer; supervision log screen.
- L6 Unlicensed help is clerical only → AI outputs that are licensed acts are drafts until approved.
- L7 No commission share or per-deal pay to unlicensed people or companies → no revenue-share code paths; software licence flat.
- L8 Rebates to parties allowed → optional fee-credit display; flag for lender disclosure.
- L9 Owner authority and agreed fee before marketing → listing cannot publish until signed agreement stored.
- L10 Advertising rules → identity block enforced on every ad/page/first e-mail; broker approves ads; no third-party listing photos.
- L11 Uniform published SOP → SOP encoded once, applied identically, published notarised on site; overrides logged.
- L12 Agency disclosure form (DOS-1736-f, Rev. 09/21) → auto-sent at the three statutory triggers; e-signed; refusal-declaration workflow.
- L13 Disclose whom you act for; dual-compensation consent → agency-relationship screen; consent captured.
- L14 Exclusive-listing terms → listing-agreement template with six-point explanation, offer-routing option, no auto-renewal.
- L15 Buyer agreement before tours → tour scheduling blocked until signed.
- L16 MLS needs licence plus REALTOR membership → MLS step shown as broker action, gated on licence and membership.
- L17 Three-year records → retention store; deletion honoured after retention period.
- L18 Software's acts are the broker's → never "autonomous agent"; each licensed output signed off on screen.
- L19 Showings treated as licensed → showing step requires licensee or owner presence/authorisation.
- L20 Pending public-marketing and showing duties; $5,000 fine cap → default public marketing; opt-out form; buyer-agent inbox; showing availability.
- L21 Only lawyers practise law or are paid for real-estate instruments → company never sells contract drafting; no "lawyer" claims for the software.
- L22 Narrow broker contract privilege → offer module fills facts only, prints legend and attorney-approval clause, never priced separately.
- L23 No legal advice; never discourage a lawyer → chat refuses party-specific legal questions and routes to a lawyer; "you don't need a lawyer" blocked.
- L24 Statute of frauds; offers can bind → parties e-sign themselves; offers labelled not binding until formal contract.
- L25 Seller's attorney drafts (Hudson Valley custom) → product stops at accepted offer; attorney stage is a visible hand-off with tracking.
- L26 No dual lawyer-broker role on commission deals → system cannot assign the founder as counsel on any commission deal.
- L27 Fixed-fee exception → optional seller package with upfront non-refundable fee, consent form, separate legal billing.
- L28 No legal fees or services through Joe's company → brokerage never invoices legal work.
- L29 "Not legal services" written notice → onboarding notice to every buyer and seller, stored.
- L30 Rule 4.3 → if founder is seller's counsel, buyer-facing messages carry no advice.
- L31 No referral fees between lawyers and brokerage → attorney directory with no paid placement or referral fees.
- L32 Title-role limits and affiliated-business disclosures → no bundled or free title/closing services.
- L33 RESPA kickback ban → no lender/title/inspector/mover referral fees; vendor payments flat.
- L34 E-signatures valid → e-sign module with E-SIGN consumer consent screen and audit trail.
- L35 Deeds/mortgages acknowledged; POA on paper → closing documents out of scope; attorney/title/notary checkpoint.
- L36 No discriminatory copy (15 NY classes) → protected-class and proxy screen on all copy; broker approval; results stored.
- L37 No steering or school/demographic talk → chat refusal list; identical answers to all users.
- L38 No discriminatory ad targeting → housing ad category only; no age/gender/family/ZIP/lookalike targeting; audiences logged.
- L39 DOS-2156 at first substantive contact → auto-sent; stored three years; declaration workflow.
- L40 Fair-housing notice on homepage and at open houses → homepage link; open-house kit.
- L41 Solicitation limits, no blockbusting → outreach checks DOS cease-and-desist list and opt-outs; no neighbourhood-change claims.
- L42 Pending AI-agent disparate-impact audits → chat, ad and SOP logs kept audit-ready.
- L43 PCDS before buyer signs (form eff. 2025-07-01) → version-pinned form; seller completes; system never pre-fills; checkpoint before contract.
- L44 Lead paint pre-1978 → triggered by year built; licensee checkpoint; 10-day inspection window tracked.
- L45 Smoke-detector affidavit → closing checklist.
- L46 Agricultural-district notice → parcel check; notice before contract.
- L47 Heating bills on request → request tracking with 15-day clock.
- L48 Stigmatised facts not material → chat never volunteers; relays only seller's written answer.
- L49 County well tests → county-specific task list.
- L50 Consent for autodialed/AI-voice/marketing texts (AI voices count as "artificial") → no cold texting or AI cold calls; consent capture; one "stop" stops every channel.
- L51 NY telemarketing rules → quiet hours hard-coded; opening script gives brokerage name and do-not-call option first, then recording, purpose, goods within 30 seconds.
- L52 CAN-SPAM → unsubscribe and address in every marketing e-mail.
- L53 Call-recording consent (NY one-party; PA, MA, CA and others all-party; CT civil rule; AI-vendor risk) → recording-and-AI announcement opens every call; vendor contract bars reuse/training on call content.
- L54 No deceptive AI claims, fake reviews, impersonation → marketing copy rules; no generated testimonials.
- L55 NY AI disclosure laws → uniform published fee; label synthetic presenters; assistant stays customer-service-only.
- L56 SHIELD safeguards and 30-day breach notice → data minimisation, encryption, no SSN in chat, breach runbook, export/delete.
- L57 Wire-fraud control → product never sends or changes wiring instructions; standing warning banner.
- L58 NY disparate-effect test (Exec. Law §296(5-a), Dec. 2025) → every automated rule that sorts people (lead scoring, reply priority, listings shown, ad audiences, SOP prerequisites) has a written justification and a logged periodic disparate-effect test.
- L59 Source-of-income neutrality, including response speed → identical response-time targets logged per lead; a voucher mention changes nothing.
- L60 RPL §242 seller notices (no electric service, utility surcharge, green-jobs charge, uncapped gas well) → four intake questions; statutory sentences generated verbatim before any offer is accepted.
- L61 Complaint windows (FHA 2 years tolled; DHR 3 years) → chat, SOP, ad-audience and test logs kept at least 3 years, secured as personal data.
- L62 Pending AI/privacy bills awaiting the Governor (A3411-B, A9349-B, S6954-B, S9269; S1169-B Senate only) → persistent "AI answers may be inaccurate; a licensed broker reviews" line now; uniform fee; label synthetic media; minimal accessibility/health data kept apart.

## 5. Open gaps that still matter, and what would close them

- DOS position on an unlicensed passive member of the brokerage LLC → email realestate@dos.ny.gov or call DOS Division of Licensing Services (518) 474-4429 with the proposed structure.
- Whether an unaccompanied buyer tour (lockbox/app access) is a licensed showing → same DOS contact, or the founder's own reading with NYSAR's member legal hotline.
- Governor action on A10679-B (public marketing; $5,000 fine cap) and S8870 (four-year broker experience) → check nysenate.gov bill pages before year end 2026.
- Current (2026) county custom → the founder calls two closing attorneys per county (sheets date from 2017–2020).
- Bar/realtor-approved broker offer form in the Hudson Valley → ask HGAR and Hudson Valley Catskill Region REALTORS whether a joint-committee form exists.
- Licence to embed the NYSBA residential contract form in software → ask NYSBA (reprint@nysba.org per search result; unconfirmed for forms).
- Malpractice insurance for a lawyer who also brokers → the founder's carrier.
- No New York authority on AI-generated legal documents or AI brokerage agents → none exists to find; monitor A9028 and DOS.
- Governor action on A3411-B (AI inaccuracy notice), A9349-B (surveillance-pricing ban), S6954-B (AI-media provenance), S9269 (NYHIPA) → nysenate.gov bill pages before 2026-12-31.
- DOS position on e-delivery and e-signature of the agency form (DOS-1736-f) and the PCDS → same DOS contact as above; meanwhile store signed PDF, delivery message, timestamp and IP.
- Primary text of Rockland County Code ch. 389 (well tests) and Westchester County ch. 700 (county fair-housing classes) → county clerk or county attorney (county websites blocked automated reads).
- What changed in Executive Law §296 on 2026-06-05 and RPL §442-h in 2025 → no diff available online; a NY practitioner or the 2025–26 chapter laws.
- Whether HUD finalises deletion of its disparate-impact rule (comment period closed about 2026-10-09) → Federal Register; does not change NY's §296(5-a).

## 6. Contradictions with other workstreams' notes

- WS4 (`costs_and_revenue_benchmarks.md`) assumes $370 per two-year term ($185 LLC + $185 for the attorney as member). RPL §441-b(2): the LLC licence itself entitles one member to act as broker, so the cost is $185 unless a second member also acts as broker.
- WS3 (`mls_access.md`, KQ5) and WS5 (`hudson_valley_market_and_locals.md`, `why_attempts_failed_and_niche_evidence.md`) could not confirm the DOS attorney waiver; WS2 confirmed it from the DOS application form (DOS-0036-f-a, Rev. 09/23): attorneys are exempt from education, experience and exam.
- WS5's K3 and recommendation 4 (fixed, non-contingent fee if the attorney is both counsel and broker) are consistent with WS2 and now stronger: NYSBA Op. 1117 (2017) fn. 1 reaffirms the Op. 1015 path. WS2 adds: only as the seller's counsel, never the buyer's; legal fee billed by his law practice, not the co-owned LLC.
- WS3 (`mls_access.md`): OneKey's fair-housing word list (March 2025) is stricter than the 1995 HUD memo (it flags "Mother-in-law apt.", "Family", "Exclusive", "Executive", "Private", "Quality neighborhood"); WS2 adopts the stricter list for the copy checker. On MLS AI rules the two workstreams agree (no OneKey AI rule found; OneKey EULA AI/data terms unread in both).
- Internal, fair-housing notes (flagged in that file's gap fill): HUD's 2024 advertising guidance is withdrawn (effective 2025-09-17), not merely missing; DHR filing window is 3 years, not 1; the PCDS changed again on 2025-07-01 (Ch. 353 of 2024); the GBL §399-z disclosure order puts the caller's name first; the TCPA revoke-all rule is delayed to 2027-01-31; the AG New Rochelle settlement is dated 2024-02-04; the NY Privacy Act's Assembly companion is A8158, not A4947; DOS-2156 (11-25) and the posted DOS notice give different DHR phone numbers (reproduce each verbatim).
- Internal (WS2's own licensing and contracts notes, flagged in the gap fill, original text untouched): Op. "1177" is Op. 1117; Op. 1015 is reaffirmed, not doubtful; Columbia and Greene are seller's-attorney-drafted counties, not broker-drafted; the founder cannot be a client's lawyer and title agent in one deal (Op. 1283, 2025); the "first-time definition of buyer's agent" in A8910 is wrong (current RPL §443(1)(c) already has it).
