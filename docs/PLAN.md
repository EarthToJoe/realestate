# Project plan: a seller-first, attorney-brokered, software-run brokerage in the Hudson Valley

*Written 2026-10-23 from the six research reports, the memo on the father-in-law's roles, the fact-check, the
architecture spec and the demo-house data. Every cost comes from [WS4](research/WS4-cost-model.md) unless marked.
"FIL" = Joe's father-in-law, the attorney who would be broker of record. Risks and kill criteria (A-numbers,
K-numbers) are in [ASSUMPTIONS.md](ASSUMPTIONS.md); questions (Q-numbers) are in
[QUESTIONS-FOR-JOE.md](QUESTIONS-FOR-JOE.md).*

## What we are building, after the research

Not "software that replaces both agents and the lawyer": New York does not allow it and buyers do not want it
(A3, A6 hit; K4 hit by that wording). The plan is for a **licensed brokerage** in which the FIL is broker of record
and personally makes each licensed decision on screen; the software does the file work around those decisions
(intake, pricing analysis, listing copy with fair-housing checks, the MLS package, scheduling, message drafts, offer
comparison, deadlines, records); independent attorneys draft the contract, as Hudson Valley custom already has
them do. It is **seller-first**, at a **flat fee** (illustrative $4,500), pays buyer agents a market rate by
default, and offers buyers an optional rebate service with a licensed person at tours. Its edge over the
competition is a trusted, accountable local attorney-broker at the lowest price, not technology alone.

## What already exists (and what we adopt)

- **Competitors** (about 70 reviewed, [WS5](research/WS5-competitors.md)): the nearest models are LocQube (Bronx;
  $899 AI-written listing or 1.99% with an agent; New York and Connecticut, Westchester named), Waymark (Texas; AI
  plus one reviewing broker, $699 to $1,199) and Homa (AI buyer brokerage, one broker per state, 1%). We borrow
  their shape (software plus a licensed human at each licensed act) and none of their code; none operates in the
  eight counties or is attorney-led in New York.
- **Infrastructure we adopt rather than build**: OneKey MLS and its free listing tool (Ocusell List), forms and
  transaction tools (TransactionDesk, included in the subscription; its e-signature extras unconfirmed),
  ShowingTime, and free portal syndication
  ([WS3](research/WS3-listing-data-access.md)). The POC's building blocks are open-source libraries listed in
  [the architecture spec §1](specs/poc-architecture.md#1-what-already-exists).

## Phases at a glance

| Phase | Dates | Goal | Cash cost (lean / realistic) | Gate |
|---|---|---|---|---|
| 0 Validate | 2026-10-26 to about 2026-12-31 | Prove there are sellers, and that he can lawfully run a NY firm | about $0 / $0 (time only) | G0: ten-calls result, bar status, office, DOS and MLS answers (A12, A13, A14, K9) |
| 1 Demo | build 2026-10-25 to 10-28; meeting about 2026-10-30 | Show the FIL a working first slice and a sober plan | build on Max or extra credit (Q26); about $0.16 per live demo run | G1: he wants to proceed and commits to Phase 0 |
| 2 Set up the firm | about 2027-01-04 to 2027-03-31 (8 to 12 weeks) | Entity, licence, office, REALTOR and MLS membership, insurance, forms | one-time about $2,500 / up to $20,300 | G2: licensed, on OneKey, insured, forms approved (K9, A13, A17) |
| 3 Pilot listings | about 2027-04 to 2027-12 | First 10 listings; measure hours, sources, sale speed, costs | year-one fixed $8,236 / $62,575; per closed side $351 / $1,902 | G3: K2, K5, K6, K7, A1, A7 measured |
| 4 Scale or stop | 2028 | Grow to break-even volume, or stop cleanly | year-two fixed about $6,500 / $56,000 | Break-even 2 / 25 closings at $4,500 |

Phases 0 and 1 overlap in time; Phase 0 is numbered first because its gate matters most. Phase 2 starts only if
G0 passes.

## Phase 0: validate (2026-10-26 to about 2026-12-31)

**Goal.** Settle the three risks that research cannot: whether his network still produces listings (A12, A5,
A16), whether he can lawfully run a New York firm from where he lives (A13, A14), and whether the MLS and DOS see
no blocker (K9).

| # | Step | Who | Time | Cost |
|---|---|---|---|---|
| 0.1 | Name ten sellers he could call; call them; record who would list, when, and why (Q13) | FIL | 30 to 60 days after the meeting; a few hours of calls | $0 |
| 0.2 | Check his attorney registration (court attorney search, or OCA 212-428-2800); cure it if lapsed (A14, Q11) | FIL | Under an hour; cure time varies | Registration fee if active ($375) |
| 0.3 | Say where he lives and where the NY office would be; decide broker only or broker plus seller's lawyer (Q11, Q15, Q16) | FIL, with Joe | One conversation | $0 |
| 0.4 | Phone DOS Licensing Services, (518) 474-4429: retired status and the attorney route; out-of-state broker of record; shared or co-working office; Joe's passive ownership (Q29) | Joe drafts, FIL calls or signs | 1 to 2 hours plus wait | $0 |
| 0.5 | Phone OneKey / HGAR (914-681-0833): Ulster coverage, unlicensed-assistant access, whether a broker's software may feed Ocusell's aggregator; phone HVCRR (845-338-5299) for northern MLS fees and rules (Q32) | Joe | 1 to 2 hours | $0 |
| 0.6 | Written question to his malpractice carrier on the business-enterprise exclusion (Q27) | FIL | 1 hour | $0 |
| 0.7 | If he wants the dual role: written advice from his own ethics counsel or the NYSBA ethics hotline (518-463-3200) | FIL; outside lawyer | 1 to 3 weeks | Not costed (counsel fee if used) |
| 0.8 | Confirm today's county closing customs (Q28) | FIL | 15 minutes | $0 |

**Gate G0 (by about 2026-12-31).** Go to Phase 2 only if all hold:
- at least three of the ten named sellers say they would list with the firm in the next 12 months (A12; threshold
  ours, provisional). If fewer: **stop building past the demo and re-plan around a local partner broker** (WS5);
- his registration is current or curable, and DOS raises no bar to the attorney route (A14);
- a New York office he can supervise is workable and DOS raises no objection (A13);
- he agrees to take the licence and join HGAR (K9 dodged only if he does);
- the role is decided; any dual-role plan has written ethics advice (K3);
- he can give about 10 to 15 hours a week (A1, Q17).

## Phase 1: the demo (build 2026-10-25 to 10-28; meeting about 2026-10-30)

**Goal.** A working first slice of the product that shows one Hudson Valley sale, 146 Rt 292, Holmes, with every
AI action visible and every licensed or legal step a visible checkpoint, plus this plan and the executive summary.

| Date | Step | Who |
|---|---|---|
| Sun 10-25 | Skeleton, checkpoint records, intake, first timeline (architecture §9 day 1) | Software (headless build jobs), Joe reviews |
| Mon 10-26 | Pricing, listing copy with the fair-housing checker and 40+ test phrases, marketing channel board | Software, Joe |
| Tue 10-27 | Inbox, offers, accepted-offer memo and attorney workspace (Q24), buyer screens | Software, Joe |
| Wed 10-28 | Business marketing, guided demo mode, generated walkthrough script, end-to-end test; **Joe clicks through on hughesnode** | Software, Joe |
| Thu 10-29 | Polish from Joe's notes; record the replay run (Q25) | Software, Joe |
| about Fri 10-30 | Meeting: about 14-minute walkthrough, then this plan and the summary | Joe, FIL |

**Cost.** The build's own billing is Joe's decision (Q26: Max plan or added API credit). The demo's AI calls cost
about $0.16 per live run and stop at $12, inside the $15 reserve ([architecture §7](specs/poc-architecture.md#7-model-use-and-cost)).

**Gate G1 (at the meeting).** He wants to go on and commits to the Phase 0 steps. The demo itself must pass two
checks before it is shown: the fair-housing checker catches every planted phrase in its test set (A8), and every
licensed act stops at his checkpoint, with no "autonomous" language anywhere (K4).

## Phase 2: set up the firm (about 2027-01-04 to 2027-03-31)

**Goal.** A licensed, insured New York brokerage on OneKey MLS, with forms and procedures that keep the software
on the right side of the law. WS4 puts this at 8 to 12 weeks and 80 to 125 hours of his time, mostly legal set-up.

| # | Step | Who | Time | Cost (lean / realistic or high) |
|---|---|---|---|---|
| 2.1 | Form the LLC; publish for six weeks; file an assumed name if branded | Joe and FIL | 10 h; 6+ weeks | $200 + $395 to $685 publication + $0 to $25 |
| 2.2 | DOS name pre-clearance; broker application by the attorney route (one licence covers a one-broker LLC) | FIL | 3 h; DOS processing time unpublished | $185 per two years |
| 2.3 | New York office with a sidewalk-readable sign (or licensed home office) | FIL | Days to weeks | $0 / $5,500 to $13,200 a year |
| 2.4 | Join HGAR (3 to 5 business days, 3.5 h orientation); subscribe to OneKey (orientation within 90 days); set Keystone syndication switches | FIL | 8 to 10 h | $606/yr + $100 + $650 + $190/month (MLS channel $3,821 in year one with the licence) |
| 2.5 | E&O (and general liability, cyber) for the brokerage | FIL | 5 h; 2 to 5 business days | median $708/yr (up to $1,500) |
| 2.6 | Operating and escrow bank accounts (escrow unused if the firm never holds deposits, Q39) | Joe and FIL | 3 h | $0 |
| 2.7 | Standard operating procedures posted on the website, fair-housing notice, agency-disclosure flow, "not legal services" notice | FIL | 10 to 15 h | $0 |
| 2.8 | Forms and the AI drafting boundary: listing agreement, buyer agreement, fill-in offer with the attorney-approval legend, no document fee | FIL, or outside lawyer | 40 to 80 h | $0 (his time) / about $6,000 realistic, up to $15,000 outside counsel |
| 2.9 | Business texting registration; MLS Grid vendor registration and OneKey website review | Joe | 5 h | about $20 to $61 |
| 2.10 | Turn the POC into a production system: real e-signature (OneKey's TransactionDesk or a vendor), real email and SMS with consent, backups, monitoring, security hardening, identity checks (all out of the POC's scope) | Joe; software | Months, alongside 2.1 to 2.9 | Joe's time, uncosted (a hired developer is $145,830 a year locally) |
| 2.11 | Send the DOS written inquiry (Q29) if not done in Phase 0 | FIL | 1 h | $0 |

**Cost.** One-time cash about **$2,500** (lean) to about **$20,300** (with $15,000 of outside counsel, a second
licence, a branch, a lockbox fleet and a hosted site). These one-time items fall inside the year-one fixed totals of
**$8,236 lean** and **$62,575 realistic**. [→ WS4](research/WS4-cost-model.md#getting-in-the-door-about-2500-cash-or-20000-with-outside-legal-review)

**Gate G2 (about 2027-03-31).** Licence issued; OneKey active (K9 dodged in fact); E&O bound and the carrier's
written answer on his law cover received (A17); office meets DOS rules (A13); forms reviewed by a lawyer; the
software's licensed acts all gated by his recorded approval (K4). If DOS or the MLS refuses, stop or find a local
broker of record.

## Phase 3: pilot listings (about 2027-04 to 2027-12)

**Goal.** Take the first 10 listings (and any buyers that come with them) and measure the numbers that decide the
venture. WS4: "Those four numbers, gathered on the first 10 to 20 deals, will settle A7, K1, K2 and K5 faster than
any further research can."

| # | Step | Who | Time | Cost |
|---|---|---|---|---|
| 3.1 | Win listings from referrals only; record each client's source at intake | FIL; software | Ongoing | $0 paid acquisition (Q34) |
| 3.2 | Run each listing through the product; he approves every licensed act; log his minutes at every checkpoint | FIL; software | About 20 broker hours a side at launch, target 10.5 to 12.75 | per closed seller side $351 lean / $1,902 realistic |
| 3.3 | Key each listing into OneKey; portals follow in 24 to 48 hours | FIL or hourly assistant | 20 to 45 broker minutes; 15 to 60 clerical | included above |
| 3.4 | Offer buyer agents a market rate by default; compare days to contract with matched OneKey comparables | FIL; software | Per listing | included |
| 3.5 | Inspection pilot (Design 2): seller is the inspector's client; cap $1,500 a listing | FIL; licensed inspector; seller's attorney | Per listing | up to about $10,000 for ten (outside the lean case) |
| 3.6 | Optional buyer service: licensed person at every tour (FIL, a sponsored licensee, or a showing agent at about $50 a tour) | FIL or licensee | 7 to 10.5 broker hours per buyer, or about $350 | per buyer |

**Duration and cash.** The first fee arrives 5 to 8 months after set-up starts (35 to 55 days to an accepted offer,
45 to 60 more to close). Founder cash needed before then: **under $10,000 lean; about $31,000 to $40,000 realistic**
(K7). [→ WS4](research/WS4-cost-model.md#kill-criteria-where-the-numbers-land)

**Gate G3 (after the first 10 listings close or expire, or about 2027-12-31).** The thresholds below are ours,
provisional, to be agreed with the FIL before the first listing:
- **K2, K5:** most clients came by referral or past relationship; none was bought with per-lead advertising.
- **A1, A7:** his steady-state hours trend to about 15 a side or fewer (at 25 or more a side the realistic case
  needs about 68 closings to break even with his time valued at $66.65 an hour, beyond one broker).
- **K6, A15:** listings reach contract within about 25% of matched comparables' days and sell at a similar rate.
- **A7, K7:** each closing's contribution is positive at the fee, and founder cash stays inside the ranges above.
- **A8:** no fair-housing complaint; the checker's hits and misses on real copy are logged and reviewed.
- **A9:** the inspection pilot shows fewer renegotiations or fall-throughs, or it switches to the inspection credit
  (Design 3).

## Phase 4: scale or stop (2028)

**Scale** if G3 passes: hire a part-time coordinator at about 15 closings ($24,000 a year); sponsor a licensed
salesperson for tours as buyer volume grows; join HVCRR for Columbia and Greene (placeholder $2,500 a year); aim for
the realistic case's break-even of **25 closings at $4,500** (40 with his time valued at $66.65 an hour); keep paid
marketing to a capped brand budget. Do not drift into the full build-out (free inspections, bought leads, premium
media on every listing), which **never breaks even at a flat fee** and reverts to Redfin's 2% price.
[→ WS4](research/WS4-cost-model.md#the-verdict-in-three-numbers-fee-cost-of-a-customer-broker-hours)

**Stop** if listings had to be bought (K2 hit), his hours stay far above 15 a side (A1), or the firm's listings sell
markedly worse than comparables (K6). Stopping costs little in the lean case: its fixed costs are about $6,500 a
year, mostly the MLS and insurance, and they end when cancelled. One option on stopping, our inference, not researched: Joe's software company
licenses the product for a fixed fee to an existing local brokerage, which is lawful for a non-licensee (WS2 §8).

## Open questions

All are in [QUESTIONS-FOR-JOE.md](QUESTIONS-FOR-JOE.md) with a provisional answer, so none blocks work.
- **Phase 0 (FIL, decide first):** Q11, Q13 to Q18, Q27 to Q30.
- **Phase 1 (Joe, before the build):** Q19, Q24, Q25, Q26, Q41, Q42.
- **Phase 2 (both):** Q14, Q20 to Q23, Q31 to Q33, Q35, Q39, Q40.
- **Phase 3 (both):** Q34, Q36, Q37, Q38.
- **Unresolved after the fact-check:** whether OneKey covers Ulster for a new member (phone call, step 0.5); whether
  the fixed-fee dual role survives a grievance committee (written ethics advice, step 0.7).

## Human-in-the-loop map

Every step where a licensed person, a lawyer or another human must act. It combines WS1's 21 "human or licence
required" functions (F-IDs), WS2's legal checkpoints (L-IDs) and the architecture's checkpoint catalogue (CP-IDs,
which the demo's timeline is built from). Who: **FIL** = the broker of record (or a licensee he sponsors);
**Attorney** = a party's own lawyer; **Seller / Buyer** = the party; **Third party** = inspector, lender, title,
notary, vendor. Times are WS4's broker-hour estimates (launch / steady state) [INFERENCE in WS4], WS3's MLS minutes,
and WS1's task durations; "within" means the time is counted in the row named.

| # | Step | Who acts | Why (F-ID; L-ID) | Roughly how long | Demo checkpoint |
|---|---|---|---|---|---|
| **Firm (one-time and ongoing)** | | | | | |
| 1 | Hold the broker licence; renew every two years | FIL | F73; L3, L4 | 3 h to apply; renewal minutes | Licence in every footer |
| 2 | Keep a New York office with a sign | FIL | F74; L4 | Set-up days; ongoing | Office address on every page |
| 3 | Supervise everything done under the licence: approval queue, audit log, sampling | FIL | F75; L5, L6, L18 | Within each approval below; plus a regular review (our estimate: about an hour a week) | Supervision log (step 9) |
| 4 | Write, notarise and post the standard operating procedures; apply them identically | FIL | F77; L11 | 10 to 15 h at launch | Not in demo |
| 5 | Approve the firm's own advertising and campaigns | FIL | F1, F76; L10, L38, L40 | Minutes per campaign | CP-19 |
| 6 | Be the trusted, named person clients choose; counsel them | FIL | F4, F84 (practical) | Ongoing | Founder shown by name |
| 7 | Disclose any interest of his own in a deal | FIL | F82; L13 | Per occurrence | Not in demo |
| 8 | Business and insurance decisions | FIL and Joe | F88 (practical) | 5 h at launch | Not in demo |
| 9 | Respond to DOS, complaints; keep evidence three years | FIL | F89; L17, L61 | As needed | Evidence export (planned) |
| **Seller side** | | | | | |
| 10 | Seller acknowledges the agency disclosure before the listing agreement | Seller (software delivers) | F9; L12 | Minutes | CP-01 |
| 11 | Choose and record whom the firm represents; conflicts check | FIL | F11; L13 | Within row 12 | CP-17 (on in-house sales) |
| 12 | Accept the listing; pricing consultation | FIL | F12; L1, L5 | 3 h / 1.5 h (with row 14) | CP-02 |
| 13 | Listing agreement signed, with the exclusive-listing explanation | Seller and FIL | F13; L9, L14, L34 | 1 h / 0.5 h | CP-03 |
| 14 | Advise on price; the seller chooses the list price (the AI never sets it) | FIL and seller | F21, F22; L1 | Within row 12 | CP-05 |
| 15 | Seller completes the property condition disclosure; the software never pre-fills it | Seller (seller's attorney advises) | F15, F59; L43 | Seller's own time | CP-04 |
| 16 | Approve listing copy, flyer and posts after the fair-housing check | FIL | F26, F76; L10, L36 | Minutes per batch (within 2 h / 1 h for media, MLS and ads) | CP-06 |
| 17 | Seller signs the marketing-exposure choice | Seller | F32; L9; OneKey rules | Minutes | CP-07 |
| 18 | Key the listing into OneKey MLS and approve it (no listing API exists) | Hourly assistant or FIL keys; FIL approves | F28; L16 | 15 to 60 clerical min; 20 to 45 broker min; later changes 10 to 25 min | CP-08 |
| 19 | Photographer on site; sign; lockbox with the owner's written authorisation | Third party; owner | F27, F31, F38; WS3-R3, R8 | Vendor time | Channel board "vendor booking" |
| 20 | Approve, edit or send every outgoing message | FIL | F2, F33, F75; L5, L10, L18 | Minutes per message | CP-09 |
| 21 | Showings and open houses: the owner or a licensee opens the door | FIL or owner | F39, F40; L19; OneKey 405.8 | 30 to 60 min a showing; 2 to 3 h an open house; 6 h / 3 h a listing | CP-10 |
| 22 | Present every offer and advise on it | FIL | F45, F47; L1 | Within 4 h / 2.5 h for offers | CP-11 |
| 23 | Accept, counter or reject (the AI never decides) | Seller | F47; L24 | Seller's time | CP-12 |
| 24 | Negotiate; send the approved counter; negotiate buyer-agent pay and concessions | FIL | F48, F49; L1, L18 | Within 4 h / 2.5 h | CP-13 |
| 25 | In-house or competing buyers: disclosure and dual-agency consent | FIL, seller and buyer | F51, F11; L13 | Within the offer hours | CP-17 |
| **Inspection pilot (Design 2, optional)** | | | | | |
| 26 | Seller opts in after a plain explanation that a report must be disclosed | Seller | WS6-I1; L43 | Minutes | Inspection screen (planned) |
| 27 | Inspector's licence checked against the State register; booking blocked if not current | Software, then FIL | WS6-I2 | Minutes | Planned |
| 28 | Seller, brokerage and inspector sign who-pays and who-knows-whom disclosure | Seller, FIL, inspector | WS6-I3; RESPA | Minutes | Planned |
| 29 | Seller's own attorney reviews the report against the disclosure form | Attorney | WS6-I7; L43 | Attorney's time | Planned |
| 30 | If the seller shares the report: broker treats findings as known material facts | FIL | WS6-I10; L13 | Under an hour | Planned |
| **Contract to close** | | | | | |
| 31 | Seller's attorney drafts and reviews the contract of sale; buyer's attorney reviews | Attorneys | F52, F53, F54; L21, L22, L25 | Attorney time (fees $995 to $2,500 a side) | CP-14 |
| 32 | Deposit held in the seller's attorney's escrow | Attorney | F55; L25 | Days | CP-20 (planned) |
| 33 | Buyer's licensed inspection; licensee negotiates repairs or credits; attorneys write them in | Third party, FIL, attorneys | F56, F57, F58 | 2 to 4 h inspection; negotiation within 3 h / 1.5 h | CP-21 (planned) |
| 34 | Lead-paint pamphlet, records and 10-day window (pre-1978 homes only; the demo house is 1995) | Seller; FIL ensures compliance | L44 | Minutes | Disclosure checklist |
| 35 | Keep the deal together: problems, extensions, renegotiation | FIL | F64; L1 | Within 3 h / 1.5 h | Timeline |
| 36 | Mortgage commitment, appraisal, title | Third parties | F60, F61, F62 | Weeks | CP-22 (planned) |
| 37 | Closing: deed acknowledged by a notary (may be a remote NY e-notary), powers of attorney on paper, smoke-detector affidavit | Attorneys, title, notary | F67; L35, L45 | Closing day | CP-15, CP-23 |
| 38 | Fee paid only to the licensed brokerage; three-year records | FIL | F68, F69; L7, L17 | 1 h / 0.5 h | CP-23 (planned) |
| **Buyer side (optional service)** | | | | | |
| 39 | Buyer agency disclosure and a written buyer agreement before any tour | Buyer and FIL | F9, F17; L12, L15 | 1.5 h / 0.75 h | CP-16 |
| 40 | Tours, about seven homes: a licensee opens every door | FIL, sponsored licensee or showing agent | F39; L19; OneKey 405.8 | 10.5 h / 7 h, or about $350 via a showing agent | CP-10 |
| 41 | Buyer approves the offer the software drafted | Buyer | F44; L24 | Buyer's time | CP-18 |
| 42 | Negotiate for the buyer | FIL | F48; L1 | 3 h / 2 h | CP-13 (buyer side) |
| 43 | Walkthrough and closing (buyer may walk through alone with access) | Buyer; FIL | F66 | 1.5 h / 1 h | Timeline |

**Per-deal total.** About 20 broker hours a side at launch, 10.5 (seller) to 12.75 (buyer) at steady state, plus 2
to 9 hours of unlicensed help. The only measured benchmark (Redfin) implies about 70, so the pilot measures this
first. [→ WS4](research/WS4-cost-model.md#humans-in-every-deal-1020-broker-hours-a-side-if-the-software-works-far-more-if-it-does-not)

## What the demo shows versus what is real

| The demo shows | What is real today | What it takes to make it real |
|---|---|---|
| A real house, 146 Rt 292, Holmes, from county and state records, with 8 official comparable sales and a $610,000 to $650,000 range for broker review | Real property facts; the house is **not for sale**, every page says DEMONSTRATION, and all people are fictional | An owner's signed listing agreement (L9) |
| AI drafting copy, replies, counters and a contract draft, on screen | Real model calls (live) or a labelled recording (replay, the meeting default) | Already real; about $0.16 per live run |
| Fair-housing checker catching planted phrases, with the rule and a fix | Real rules file and 40+ test phrases | Ongoing review on real copy; NY judges effects (L58) |
| 24 checkpoints that block the next step until a person decides; a timeline built from them | Real records and gates in the software | His actual approvals and minutes |
| "Licensed human required: key into OneKey", with a finished, rule-checked package | Simulated; no MLS has a listing API | His licence, HGAR, OneKey; 20 to 45 broker minutes a listing |
| Zillow, Realtor.com, Redfin, Homes.com "fed from the MLS" | Simulated status | Automatic once on OneKey; free |
| Messages "sent" from an outbox | Simulated; nothing leaves | Email/SMS provider with consent rules (L50 to L52) |
| Signatures | Simulated | OneKey's TransactionDesk or an e-sign vendor |
| Contract draft in the seller's attorney's workspace | A draft for attorney review, not legal advice | A real attorney choosing to use it (untested) |
| Buyer search over listings | Fictional listings | OneKey IDX data under its licence and AI addendum (no AI training on MLS data) |
| Not shown at all | Payments, deposits, identity checks, production security and backups | Phase 2 step 2.10 |
