# Project plan: software that replaces the seller's agent and the buyer's agent, New York, Hudson Valley first

*Rewritten 2026-10-23 for decision 21 (Joe: "Keep the original idea ... The idea is the idea. Completely replace the
real estate agents."), from the six research reports, the memo on the father-in-law's roles, the fact-check, the
architecture spec and the demo-house data. Every cost comes from [WS4](research/WS4-cost-model.md) unless marked.
"FIL" = Joe's father-in-law, the attorney who would be broker of record. Risks and kill criteria (A-numbers,
K-numbers) are in [ASSUMPTIONS.md](ASSUMPTIONS.md); questions (Q-numbers) in [QUESTIONS-FOR-JOE.md](QUESTIONS-FOR-JOE.md).
Research to plan with, not legal advice.*

## What we are building

The brief's idea, unchanged: **software that completely replaces the real estate agent on both sides**. It does
everything an agent does: intake, pricing, listing on the major sites, all marketing of the property, every
seller-side and buyer-side communication, showings scheduling, offers, negotiation, the deal timeline, and marketing
of the business itself. It **drafts the contract**, so the lawyer is out of the loop. It charges a fixed fee per side
far below today's 2.41% listing and 2.21% buyer-side New York averages. New York state, Hudson Valley first.

The research findings are not softened and do not reshape the idea; they are the hurdles it has to clear, set out in
the [hurdle map](#hurdle-map) below. The launch path that clears them today:

- **The software is the agent; the firm that runs it is licensed.** New York makes listing, marketing for a fee,
  presenting offers and negotiating "for another" the acts of a licensed broker whoever performs them, and treats
  what software does as the act of the broker who runs it (L1, L2, L18). So the company operating the software is a
  licensed brokerage LLC with the FIL as broker of record ($185, no course, experience or exam, as an admitted
  attorney with current registration, L3). He performs only the acts the law requires of a licensee, each one
  prepared by the software, carried out by it once he decides, and logged. His decisions must be real: DOS revoked a
  broker who lent his licence ("availing", Flagship, 2000) and in 2025 an appeals court upheld revoking a broker's
  licences for "wholesale failure to supervise" (Malul) (L5).
- **The contract** goes by one of three routes that exist today, set out in
  [the contract route](#the-contract-route-what-new-york-allows-today): the firm's paper subject to each party's
  attorney's approval; the FIL as the seller's lawyer on fixed-fee deals; or the parties drafting their own with the
  software (untested in New York).
- **MLS entry** is keyed by a person (no listing-input API exists, WS3); **buyer tours** have a licensed person at the
  door (L19); owners show their own homes.
- **Joe** builds and owns the software, may own equity and license the software to the firm for a fixed fee, and is
  never paid per deal (L7, WS2 §8).

## What already exists (and what we adopt)

- **Competitors** (about 70 reviewed, [WS5](research/WS5-competitors.md)): the nearest are LocQube (Bronx; $899
  AI-written listing or 1.99% with an agent; New York and Connecticut; sellers only), Ridley (AI seller platform,
  $1,499 to $3,999, three Sun Belt states), Homa (AI buyer brokerage, one broker per state, 1%), Waymark (Texas; AI plus
  one reviewing broker, $699 to $1,199) and Beycome (flat-fee brokerage with an AI assistant, 18 states, holds a New
  York licence). Every one put licensed humans back on offers, negotiation and closing; none does both sides; none
  drafts New York's contract. We borrow their shape where the law forces it (a licensee behind licensed acts) and
  none of their code.
- **The do-it-yourself baseline**: a New York Times technology writer sold his Hudson Valley house in May 2026 with
  Google's Gemini and a closing he ran himself, keeping about $90,000 by his estimate, while catching bad AI advice
  ([WS5](research/WS5-competitors.md#seller-side-ai-and-buyer-side-ai-both-exist-nobody-does-both-here)) [SECONDARY].
  That is the product's floor: a general chatbot already does part of the job, unchecked.
- **Document-assembly precedents for the contract**: LegalZoom-type self-help software, settled as lawful by statute
  or court in some states and challenged in others; nothing decided in New York (see the contract route).
- **Infrastructure we adopt rather than build**: OneKey MLS and its free listing tool (Ocusell List), TransactionDesk
  forms (included in the subscription; e-signature extras unconfirmed), ShowingTime, free portal syndication
  ([WS3](research/WS3-listing-data-access.md)). The POC's open-source building blocks are in
  [the architecture spec §1](specs/poc-architecture.md#1-what-already-exists).

## Phases at a glance

| Phase | Dates | Goal | Cash cost (lean / realistic) | Gate |
|---|---|---|---|---|
| 1 Demo | build 2026-10-23 to 10-27; Joe's click-through 10-28; polish 10-29; meeting about 2026-10-30 | Show the FIL the AI doing every step of one sale on both sides, with every legal hurdle marked, plus this plan | build on the API credit, then the Max plan (decision 22); about $0.16 per live demo run | G1: he wants to proceed and takes the Phase 0 steps |
| 0 Validate | 2026-10-31 to about 2026-12-31 | Prove there are sellers, that he can lawfully run a New York firm, and which contract route holds | about $0 (time; an ethics opinion if bought) | G0: ten-calls result, bar status, office, DOS, MLS and ethics answers |
| 2 Set up the firm | about 2027-01-04 to 2027-03-31 (8 to 12 weeks) | Entity, licence, office, REALTOR and MLS membership, insurance, contract paper | one-time about $2,500 / up to $20,300 | G2: licensed, on OneKey, insured, contract route settled |
| 3 Pilot | about 2027-04 to 2027-12 | First 10 listings and the buyers that come with them; measure broker minutes, sources, sale speed, costs | year-one fixed $8,236 / $62,575; per closed seller side $351 / $1,902 | G3: A1, A7, A15, K2, K6 measured |
| 4 Scale or stop | 2028 | Grow to break-even volume, or stop cleanly | year-two fixed about $6,500 / $56,000 | Break-even 2 / 25 seller sides at $4,500 |

Phase 1 comes first in time; Phase 0's gate matters most. Phase 2 starts only if G0 passes.

## Phase 1: the demo (build 2026-10-23 to 10-27; meeting about 2026-10-30)

**Goal.** The first real slice of the product, built to [the success criteria](SUCCESS-CRITERIA.md) as amended for
decision 21: one sale of 146 Rt 292, Holmes (Dutchess), where the AI does every agent act on both sides, including
negotiating and drafting the contract; the seller and buyer make their own decisions; and every act New York law
today reserves to a licensed person or a lawyer carries a red **"NY law today"** marker naming the rule and linking
the finding, without stopping the flow.

| Date | Step | Who |
|---|---|---|
| Fri 10-23 | Architecture spec revised for decision 21; skeleton, records for decisions and "NY law today" markers, intake | Headless build jobs; Joe reviews |
| Sat 10-24 | Pricing, listing copy with the fair-housing checker and its 40+ test phrases, marketing channel board | Build jobs |
| Sun 10-25 | Inbox (AI answers and sends, simulated), offers, AI negotiation of the counter | Build jobs |
| Mon 10-26 | Contract draft by the software with its marker; buyer screens (intake, alerts, tour, AI-drafted offer) | Build jobs |
| Tue 10-27 | Deal timeline and hurdle map from the records, business marketing, guided demo mode, walkthrough script, end-to-end test | Build jobs |
| Wed 10-28 | **Joe clicks through on realestate.hughesnode.com** | Joe |
| Thu 10-29 | Polish from Joe's notes; record the replay run (Q25) | Build jobs, Joe |
| about Fri 10-30 | Meeting: 12 to 15 minute walkthrough, then the executive summary and this plan | Joe, FIL |

The day-by-day order follows the architecture spec's build plan, which is being revised in parallel for decision 21.

**Cost.** Build jobs bill the API credit until about $2 is left above the $15 reserve, then the Max plan (decision
22). The demo's own AI calls cost about $0.16 per live run and stop at $12, inside the reserve
([architecture §7](specs/poc-architecture.md#7-model-use-and-cost)).

**Gate G1 (at the meeting).** He wants to go on and takes the Phase 0 steps. Before it is shown the demo must pass two
checks: the fair-housing checker catches every planted phrase in its test set (A8), and every act the hurdle map lists
carries its "NY law today" marker with a working link to the finding (the brief: "Every step where a human or a license
is still required should be visible in the demo itself").

## Phase 0: validate (2026-10-31 to about 2026-12-31)

**Goal.** Settle what research cannot: whether his network still produces sellers (A12, A5, A16), whether he can
lawfully run a New York firm from where he lives (A13, A14), whether DOS and the MLS see a blocker (K9), and which
contract route holds (A18).

| # | Step | Who | Time | Cost |
|---|---|---|---|---|
| 0.1 | Name ten people who might sell in the next year; call them; record who would list, when, why (Q44) | FIL | List by 2026-11-06; calls by about 2026-12-15 | $0 |
| 0.2 | Check his attorney registration (court attorney search, or OCA 212-428-2800); cure it if lapsed (A14, Q44) | FIL | Under an hour; cure time varies | $375 registration if active |
| 0.3 | Say where he lives and where a New York office could be (A13, Q44) | FIL, with Joe | One conversation | $0 |
| 0.4 | Phone DOS Licensing Services, (518) 474-4429, then one written inquiry he signs: may software carry out a broker's acts under his supervision; unaccompanied showings; out-of-state broker of record; shared or co-working office; retired registration and the attorney route; Joe's passive ownership (Q29) | Joe drafts, FIL signs | 1 to 2 hours plus wait | $0 |
| 0.5 | Written ethics question on the contract routes: the fixed-fee seller's-lawyer route (Ops. 1015, 1117) and whether party-used drafting software sold with a brokerage service is the unauthorised practice of law; NYSBA ethics hotline 518-463-3200 or his own ethics counsel (Q44, A18) | Joe drafts, FIL sends | 1 to 3 weeks | Not costed (counsel fee if used) |
| 0.6 | Phone OneKey / HGAR (914-681-0833): Ulster coverage, unlicensed-assistant access, whether a broker's software may feed Ocusell; phone HVCRR (845-338-5299) for northern MLS fees (Q32) | Joe | 1 to 2 hours | $0 |
| 0.7 | Written question to his malpractice carrier on the business-enterprise exclusion (Q27) | FIL | 1 hour | $0 |
| 0.8 | Confirm today's county closing customs, including whether local attorneys will review a broker-drafted contract (Q28) | FIL | 15 minutes | $0 |

**Gate G0 (by about 2026-12-31).** Go to Phase 2 only if all hold:
- at least three of the ten say they would list in the next 12 months (A12; threshold ours, provisional). If fewer,
  rethink how the firm finds its first customers before building past the demo;
- his registration is current or curable, and DOS raises no bar to the attorney route (A14);
- a New York office he can supervise is workable (A13);
- he takes the licence, joins HGAR and agrees to be broker of record (K9);
- a contract route is chosen with written advice behind it where the research says advice is needed (A18, K3);
- his hours fit the required acts at the pilot's volume (A1).

## Phase 2: set up the firm (about 2027-01-04 to 2027-03-31)

**Goal.** A licensed, insured New York brokerage on OneKey MLS, running the software. WS4 puts this at 8 to 12 weeks and
80 to 125 hours of his time, mostly legal set-up.

| # | Step | Who | Time | Cost (lean / realistic or high) |
|---|---|---|---|---|
| 2.1 | Form the LLC; publish for six weeks; assumed name if branded | Joe and FIL | 10 h; 6+ weeks | $200 + $395 to $685 publication + $0 to $25 |
| 2.2 | DOS name pre-clearance; broker application by the attorney route | FIL | 3 h; DOS processing time unpublished | $185 per two years |
| 2.3 | New York office with a sidewalk-readable sign (or licensed home office) | FIL | Days to weeks | $0 / $5,500 to $13,200 a year |
| 2.4 | Join HGAR (3.5 h orientation); subscribe to OneKey (orientation within 90 days); set syndication switches | FIL | 8 to 10 h | $606/yr + $100 + $650 + $190/month (MLS channel $3,821 in year one with the licence) |
| 2.5 | E&O (and general liability, cyber) for the brokerage | FIL | 5 h; 2 to 5 business days | median $708/yr (up to $1,500) |
| 2.6 | Operating and escrow bank accounts (escrow unused if the firm never holds deposits, Q39) | Joe and FIL | 3 h | $0 |
| 2.7 | Operating procedures posted on the website, fair-housing notice, agency-disclosure flow, "not legal services" notice | FIL | 10 to 15 h | $0 |
| 2.8 | Contract paper for the chosen route: the software's full contract with the legend and the attorney-approval clause (route 1); his engagement and consent forms (route 2); listing and buyer agreements | FIL, or outside lawyer | 40 to 80 h | $0 (his time) / about $6,000 realistic, up to $15,000 outside counsel |
| 2.9 | Business texting registration; MLS Grid vendor registration and OneKey website review | Joe | 5 h | about $20 to $61 |
| 2.10 | Turn the POC into production: real e-signature, real email and SMS with consent, backups, monitoring, security, identity checks | Joe; software | Months, alongside 2.1 to 2.9 | Joe's time, uncosted (a developer is $145,830 a year locally) |

**Cost.** One-time cash about **$2,500** (lean) to about **$20,300** (with $15,000 of outside counsel, a second
licence, a branch, a lockbox fleet and a hosted site), inside year-one fixed totals of **$8,236 lean** and **$62,575
realistic**. [→ WS4](research/WS4-cost-model.md#getting-in-the-door-about-2500-cash-or-20000-with-outside-legal-review)

**Gate G2 (about 2027-03-31).** Licence issued; OneKey active; E&O bound and the carrier's answer on his law cover in
hand (A17); office meets DOS rules (A13); contract paper reviewed by a lawyer; every act in the hurdle map that needs
him reaches him with its record (K4). If DOS or the MLS refuses, stop or find a local broker of record.

## Phase 3: pilot (about 2027-04 to 2027-12)

**Goal.** The first 10 listings and the buyers that come with them, measuring the numbers that decide the venture.
WS4: "Those four numbers, gathered on the first 10 to 20 deals, will settle A7, K1, K2 and K5 faster than any further
research can."

| # | Step | Who | Time | Cost |
|---|---|---|---|---|
| 3.1 | Win listings from referrals and the AI's own low-cost marketing; record each client's source at intake | FIL; software | Ongoing | $0 paid acquisition (Q34) |
| 3.2 | Run each deal through the software; log his minutes on every required act | FIL; software | About 20 broker hours a side at launch, target 10.5 to 12.75 | per closed seller side $351 lean / $1,902 realistic |
| 3.3 | Key each listing into OneKey; portals follow in 24 to 48 hours | FIL or hourly assistant | 20 to 45 broker minutes; 15 to 60 clerical | included |
| 3.4 | Act for buyers too; licensed showing agent at tours | Software; showing agent | 7 to 10.5 broker hours per buyer, or about $350 | buyer side $3,500, about $2,060 contribution |
| 3.5 | Compare days to contract with matched OneKey comparables | Software | Per listing | included |
| 3.6 | Inspection pilot (WS6 Design 2) if Joe and the FIL choose it (Q43) | FIL; licensed inspector; seller | Per listing | up to about $10,000 for ten |

**Duration and cash.** The first fee arrives 5 to 8 months after set-up starts. Founder cash before then: **under
$10,000 lean; about $31,000 to $40,000 realistic** (K7). [→ WS4](research/WS4-cost-model.md#kill-criteria-where-the-numbers-land)

**Gate G3 (after the first 10 listings close or expire, or about 2027-12-31).** Thresholds ours, provisional:
- **K2, K5:** most clients came by referral or the AI's own marketing; none was bought with per-lead advertising.
- **A1, A7:** broker hours trend to about 15 a side or fewer (at 25 or more, the realistic case needs about 68
  closings to break even with his time valued at $66.65 an hour).
- **K6, A15:** listings reach contract within about 25% of matched comparables' days and sell at a similar rate.
- **A8:** no fair-housing complaint; the checker's hits and misses on real copy are logged and reviewed.
- **A18:** the contract route worked: attorneys approved the software's drafts, or the chosen route held up.

## Phase 4: scale or stop (2028)

**Scale** if G3 passes: aim for the realistic break-even of **25 seller sides at $4,500** (40 with his time valued);
sponsor a licensed salesperson for tours as buyer volume grows; join HVCRR for Columbia and Greene (placeholder $2,500 a
year); keep paid marketing to a capped brand budget. Do not drift into free inspections and bought leads, which **never
break even at a flat fee** ([WS4](research/WS4-cost-model.md#the-verdict-in-three-numbers-fee-cost-of-a-customer-broker-hours)).

**Stop** if listings had to be bought (K2), his hours stay far above 15 a side (A1), or the firm's listings sell
markedly worse than comparables (K6). The lean case's fixed costs (about $6,500 a year, mostly MLS and insurance) end
when cancelled.

## The contract route: what New York allows today

*Targeted research, 2026-10-23, on the one load-bearing gap: may software used by a party prepare their own contract?
Labels as in the research method; "observation" = what our searches did and did not find.*

**The rules already established (WS2).** Preparing "instruments affecting real estate" for pay is reserved to lawyers,
and a company may not "render legal services of any kind" or be paid for preparing such instruments, even if an officer
is a lawyer (Judiciary Law §§478, 484, 495) [PRIMARY]. A broker may prepare a simple fill-in contract "subject to approval
by each party's attorney", or fill in the non-legal blanks of a bar-and-realtor-approved form; may add provisions only if
"the entire contract" is "subject to and conditioned upon the review and approval of each party's attorney"; must print
a legend recommending counsel; may charge no separate fee; and may never discourage counsel ([AG Op. 96-F11](https://ag.ny.gov/sites/default/files/opinions/96-F11_pw.pdf);
[DOS LI04](https://dos.ny.gov/legal-memorandum-li04-real-estate-brokers-and-salespersons-and-unauthorized-practice-law))
[PRIMARY]. Where a contract is subject to attorney approval, either attorney may disapprove within the window for any
reason ([Moran v. Erk, 2008](https://www.law.cornell.edu/nyctap/I08_0176.htm)) [PRIMARY]. No statute makes a buyer or
seller hire a lawyer; the seller's attorney drafts in all nine Hudson Valley counties by custom, while in Albany the
realtor drafts on the Capital Region MLS form with written attorney approval ([WS2 §3](research/WS2-legal-licensing.md#3-in-the-hudson-valley-the-sellers-lawyer-drafts-so-no-lawyer-fights-local-custom-too))
[SECONDARY: bar survey of custom, 2017 to 2020].

**New findings: software a party uses to draft their own contract.**
- **New York's test is personal application, not paper.** The Court of Appeals reversed a ruling that Norman Dacey's
  do-it-yourself will-and-trust book was unauthorised practice, adopting a dissent that practice of law requires
  "personal contact or relationship with a particular individual" ([NY County Lawyers' Ass'n v. Dacey, 21 N.Y.2d 694,
  1967](https://static.case.law/ny-2d/21/html/0694-01.html)) [PRIMARY citation; holding as described by
  [Hyland and Maulsby, NY Legal Ethics Reporter, c. 2015](https://www.newyorklegalethics.com/virtually-unclear-will-legal-tech-companies-bridge-justice-gap-or-fall-into-upl-abyss/),
  SECONDARY]. The same article reports a 1973 Fourth Department case finding a "Divorce Yourself Kit" seller was not
  practising law for want of personal contact (*State v. Winder*), and later cases finding unauthorised practice where a
  non-lawyer gave customised help (*Sussman v. Grado*, 2002) or applied "legal principles to someone's personal
  predicament" (*Small Business Bodyguard v. House of Moxie*, S.D.N.Y. 2015) [SECONDARY; the *Winder* citation could not
  be confirmed in a free source].
- **No New York authority on interactive document software.** The New York County Lawyers Association's 2017 task-force
  report on online legal-document providers (LegalZoom's general counsel took part) cites no New York case or opinion on
  such software, says only that "It has generally been ruled that the provision of such services does not violate
  unauthorized practice laws in and of itself", and recommends disclosure, privacy and warranty standards, not a ban
  ([NYCLA report, approved 2017-06-13](https://www.nycla.org/resource/board-report/report-of-nycla-task-force-on-on-line-legal-providersregarding-on-line-legal-documents/))
  [PRIMARY for what NYCLA said; not law]. Our searches found no New York court decision, Attorney General action or
  ethics opinion on LegalZoom-type software [observation, 2026-10-23].
- **Other states split.** North Carolina settled with LegalZoom and then legislated that interactive software generating
  a document from the consumer's answers is not the practice of law if conditions are met; South Carolina's court reached
  a similar result; Texas has a statutory safe harbour for forms and software that say they are no substitute for a
  lawyer; a Missouri federal court found LegalZoom's branching software to be unauthorised practice (*Janson v.
  LegalZoom*, 2011) (all as summarised in the NY Legal Ethics Reporter article and the NYCLA report above) [SECONDARY].
  New York has no safe harbour [observation].
- **Advice is regulated even when free.** The Second Circuit held on 2025-09-09 that New York's unauthorised-practice
  statutes are content-neutral rules subject only to intermediate scrutiny and vacated Upsolve's injunction; the
  district court dismissed the complaint on 2026-03-05; the Supreme Court denied review on 2026-03-30; Upsolve said it
  would appeal the final judgment, and we found no report of that appeal's status
  ([Supreme Court docket 25-948](https://www.supremecourt.gov/docket/docketfiles/html/public/25-948.html);
  [petitioners' supplemental brief](https://www.supremecourt.gov/DocketPDF/25/25-948/400536/20260311110011432_Supplemental%20Brief%20of%20Petitioners_PDF-A.pdf))
  [PRIMARY].
- **A pending bill aims at chatbots acting as lawyers.** S7263-A would make an operator liable for damages if it
  knowingly lets a chatbot impersonate a licensed professional in a way that would violate the Judiciary Law's
  unauthorised-practice article if done by a person; an earlier version barred "substantive" advice outright. It
  passed committee 6-0 and was committed to Rules on 2026-06-05; Assembly companion A6545
  ([S7263-A](https://www.nysenate.gov/legislation/bills/2025/S7263)) [PRIMARY]. Not law.
- **No reform in sight.** A 2020 state-bar working group rejected non-lawyer-owned law businesses for now, saying a
  "sandbox" should be reconsidered if other states' experiments succeed ([Legal IT Insider](https://legaltechnology.com/new-york-gives-red-light-to-alternative-business-structures/))
  [SECONDARY]. Chief Judge Wilson's 2026-09-24 civil-legal-needs hearing floated trained non-lawyers and navigators,
  not software or a sandbox ([New York Law Journal, 2026-09-24](https://www.law.com/newyorklawjournal/2026/09/24/not-every-dispute-requires-a-lawyer-ny-chief-judge-highlights-nonlawyer-aid-at-justice-hearing/))
  [SECONDARY]. No New York sandbox proposal was found [observation].

**What this means for the three routes** [INFERENCE throughout]:
1. **The firm's paper, subject to attorney approval (lawful today).** The software can draft the whole contract as the
   brokerage's paper if every added term is covered by the "entire contract subject to each party's attorney's
   approval" clause, the legend is printed, no fee is charged for it and nobody is discouraged from counsel. The lawyer
   moves from drafter to approver with a veto window. Risks: courts disciplined brokers who inserted "broad, legally
   significant" clauses (*Mulford*, 1986, in 96-F11), so the drafts stay close to the standard form; Hudson Valley
   attorneys may refuse to work from broker paper (custom, Q28). What attorneys would charge for approval only was not
   researched.
2. **The FIL as the seller's lawyer, using the software (lawful on advisory opinions).** On a fixed, non-refundable,
   non-contingent brokerage fee with written consent (Ops. 1015, 1117 fn. 1), his law practice drafts with the software as
   his tool and bills separately; the buyer keeps their own lawyer or none (Rule 4.3). Needs active registration, CLE, a
   New York law office (Judiciary Law §470) and malpractice cover ([memo](research/memo-father-in-law.md)).
3. **The parties as their own drafters (untested).** Dacey and Winder favour general self-help tools, but an AI that
   tailors terms to one buyer looks more like "personal application" than a book, and a brokerage paid on the deal that
   supplies the drafting tool runs into §495's bar on companies preparing real-estate instruments for pay. Settle it with
   a written ethics opinion (step 0.5) before use; watch S7263-A and the Upsolve appeal.

## Hurdle map

Every act where New York law today requires a licensed person or a lawyer (plus the few where a third party must act),
who does it at launch, the least that person must do, and how it shrinks. It combines WS1's 21 "human or licence
required" functions (F-IDs) and WS2's legal constraints (L-IDs); the demo's red "NY law today" markers are generated
from the same list (the architecture spec maps them). Times are WS4's broker-hour estimates (launch / steady state)
[INFERENCE in WS4], WS3's MLS minutes and WS1's task durations. **FIL** = broker of record; **Attorney** = a party's own
lawyer.

| # | Act | Why a person (F; L) | At launch | The least a person does; what the software does | Path to shrink it further |
|---|---|---|---|---|---|
| **Firm** | | | | | |
| 1 | Hold the broker licence; renew every two years | F73; L3, L4 | FIL | Apply once (3 h, $185); software tracks renewal | None needed |
| 2 | New York office with a sign | F74; L4 | FIL | Keep it; licensed home office allowed | DOS answer on shared or co-working offices (Q29) |
| 3 | Supervise everything done under the licence | F75; L5, L6, L18 | FIL | Real review of the software's work; software logs every act and flags exceptions (our estimate: about an hour a week plus the acts below) | DOS guidance on software acting under supervision (Q29); none exists |
| 4 | Written operating procedures, applied identically | F77; L11 | FIL | Approve them (10 to 15 h at launch); software applies them identically | — |
| 5 | Advertising: listings and the firm's own campaigns | F1, F26, F76; L10, L36, L38, L40 | FIL decides; AI drafts and runs the fair-housing check | Minutes per batch | Sampling instead of per-item approval, if DOS accepts it [INFERENCE] |
| 6 | Disclose his own interest in a deal; answer DOS; keep records three years | F82, F89; L13, L17, L61 | FIL | Per occurrence; software prompts and keeps the evidence | — |
| **Seller side** | | | | | |
| 7 | Agency disclosure at first substantive contact | F9; L12 | Software delivers in the firm's name; seller acknowledges | Minutes | — |
| 8 | Accept the listing; advise on price | F12, F21, F22; L1, L5 | FIL decides; seller chooses the price | 3 h / 1.5 h; AI prepares the comparables, range and recommendation | DOS ruling or statute on software acting for the broker |
| 9 | Listing agreement | F13; L9, L14, L34 | Seller and the firm | 1 h / 0.5 h; AI generates it from the template | — |
| 10 | Property condition disclosure | F15, F59; L43 | Seller (their own legal duty) | Seller's time; software never pre-fills answers | — |
| 11 | Key the listing into OneKey MLS | F28; L16 | FIL or hourly assistant keys; FIL answers for every field | 15 to 60 clerical min, 20 to 45 broker min; AI prepares and checks the package | A listing-input API (none exists); OneKey approval for a vendor feed (Q32) |
| 12 | Photographer, sign, lockbox with the owner's written authorisation | F27, F31, F38 | Vendors; owner | Vendor time; AI books | — |
| 13 | Messages that advertise or negotiate | F2, F33, F75; L5, L10, L18 | AI sends in the firm's name within facts the seller approved; FIL supervises | Sampling and exception review | As row 3 |
| 14 | Showings and open houses | F39, F40; L19; OneKey 405.8 | Owner hosts; or a licensee | 30 to 60 min a showing; AI schedules within OneKey's 24-hour rule | DOS answer on unaccompanied showings (Q29) |
| 15 | Present each offer and advise on it | F45, F47; L1 | AI presents and advises in the firm's name once FIL has decided the advice; seller decides | Within 4 h / 2.5 h for offers | As row 8 |
| 16 | Negotiate counters, buyer-agent pay, concessions | F48, F49; L1, L18 | FIL sets the position; AI conducts it | Within 4 h / 2.5 h | As row 8 |
| 17 | Same firm on both sides: dual-agency consent | F51, F11; L13 | Seller and buyer consent on the state form | Within the offer hours; software runs the forms. Designated agents would need two more licensees | — |
| **Contract to close** | | | | | |
| 18 | Contract of sale | F52, F53, F54; L21, L22, L23, L25 | Route 1: software drafts, each party's attorney approves. Route 2: FIL as seller's lawyer. Route 3: the parties (untested) | Attorney approval within the window; attorney fees today $995 to $2,500 a side | Ethics opinion on route 3; a New York safe harbour (none proposed); S7263-A watch |
| 19 | Explain what a clause means for a party | F53; L23 | That party's lawyer | Software shows neutral, generic information only and never says "you don't need a lawyer" | Same as row 18 |
| 20 | Deposit escrow | F55; L25 | Seller's attorney by custom (Q39) | Days; software tracks | Broker escrow under 19 NYCRR 175.1 if no attorney holds it [INFERENCE] |
| 21 | Buyer's inspection; negotiate repairs or credits | F56, F57, F58 | Licensed inspector; FIL sets position, AI negotiates | 2 to 4 h inspection; within 3 h / 1.5 h | — |
| 22 | Lead-paint pamphlet and 10-day window (pre-1978 only; the demo house is 1995) | L44 | Seller; firm ensures it happens | Minutes | — |
| 23 | Keep the deal together: problems, extensions | F64; L1 | FIL decides; AI handles | Within 3 h / 1.5 h | As row 8 |
| 24 | Mortgage commitment, appraisal, title | F60, F61, F62 | Third parties | Weeks; AI tracks | — |
| 25 | Closing: deed acknowledged by a notary (remote New York e-notary allowed), powers of attorney on paper, smoke-detector affidavit | F67; L35, L45 | Attorneys, title company, notary | Closing day | — |
| 26 | Fee paid only to the licensed firm; three-year records | F68, F69; L7, L17 | FIL | 1 h / 0.5 h; software keeps the records | — |
| **Buyer side** | | | | | |
| 27 | Buyer agency disclosure and written buyer agreement before any tour | F9, F17; L12, L15 | Buyer and the firm | 1.5 h / 0.75 h; software generates both | — |
| 28 | Tours, about seven homes | F39; L19; OneKey 405.8 | Licensed showing agent, or FIL | 10.5 h / 7 h, or about $350 via showing agents; AI books and routes | DOS answer on unaccompanied tours (Q29) |
| 29 | Buyer's offer | F44; L22, L24 | AI drafts the fill-in offer; buyer approves and signs | Buyer's time | — |
| 30 | Negotiate for the buyer | F48; L1 | FIL sets the position; AI conducts it | 3 h / 2 h | As row 8 |
| 31 | Walkthrough and closing | F66 | Buyer, with access arranged | 1.5 h / 1 h | — |
| **Inspection pilot (only if chosen, Q43)** | | | | | |
| 32 | Seller opts in after a plain warning that a report must be disclosed; licence check; all-party disclosure; seller's attorney reviews the report | WS6-I1 to I10; L43; RESPA | Seller, FIL, licensed inspector, attorney | Minutes each; software blocks unlicensed inspectors | — |

**Per-deal total.** About 20 broker hours a side at launch, 10.5 (seller) to 12.75 (buyer) at steady state, plus 2 to
9 hours of unlicensed help. The only measured benchmark (Redfin) implies about 70, so the pilot measures this first.
[→ WS4](research/WS4-cost-model.md#humans-in-every-deal-1020-broker-hours-a-side-if-the-software-works-far-more-if-it-does-not)

**On the watch list.** S8870/A9518, passed by both houses and awaiting the Governor on 2026-10-23, would require four
years as a salesperson before a broker licence by the experience route; it does not mention attorneys
([WS2 §12](research/WS2-legal-licensing.md#12-what-may-change-in-the-next-twelve-months)) [PRIMARY]. A9028 (AI
"virtual agent" audits) is in committee.

## What the demo shows versus what is real

| The demo shows | What is real today | What it takes to make it real |
|---|---|---|
| A real house, 146 Rt 292, Holmes, from county and state records, with 8 official comparable sales and a $610,000 to $650,000 range | Real property facts; the house is **not for sale**, every page says DEMONSTRATION, all people are fictional | An owner's signed listing agreement (L9) |
| The AI doing every agent act: pricing advice, copy, replies, offers, negotiation, the contract | Real model calls (live) or a labelled recording (replay, the meeting default) | Already real; about $0.16 per live run |
| Red "NY law today" markers on each act in the hurdle map, with the rule and a link | Real records built from the research | The licensed firm and the chosen contract route |
| Fair-housing checker catching planted phrases, with the rule and a fix | Real rules file and 40+ test phrases | Ongoing review on real copy; New York judges effects (L58) |
| "Licensed human required: key into OneKey", with a finished, rule-checked package | Simulated; no MLS has a listing API | His licence, HGAR, OneKey; 20 to 45 broker minutes a listing |
| Zillow, Realtor.com, Redfin, Homes.com "fed from the MLS" | Simulated status | Automatic once on OneKey; free |
| Messages "sent" from an outbox | Simulated; nothing leaves | Email and SMS provider with consent rules (L50 to L52) |
| Signatures | Simulated | OneKey's TransactionDesk or an e-sign vendor |
| The contract drafted by the software | A draft under its "NY law today" marker, not legal advice | One of the three contract routes |
| Buyer search over listings | Fictional listings | OneKey IDX data under its licence and AI addendum (no AI training on MLS data) |
| Not shown at all | Payments, deposits, identity checks, production security and backups | Phase 2 step 2.10 |

## Open questions

All are in [QUESTIONS-FOR-JOE.md](QUESTIONS-FOR-JOE.md) with a provisional answer, so none blocks work.
- **For the meeting (FIL):** Q44, the one bundle: registration, where he lives and the office, broker of record, ten
  people, the contract route.
- **Demo (Joe, quick confirms):** Q23, Q25, Q43.
- **Phase 0 (FIL):** Q27, Q28, Q29, Q30.
- **Phase 2 (both):** Q18, Q20, Q21, Q22, Q31, Q32, Q33, Q35, Q39, Q40, Q41, Q42.
- **Phase 3 (both):** Q34, Q36, Q38.
- **Unresolved after research:** whether OneKey covers Ulster for a new member (step 0.6); whether the fixed-fee
  seller's-lawyer route survives a grievance committee, and whether party-used drafting software sold with a
  brokerage service is lawful in New York (step 0.5); whether unaccompanied showings are licensed acts (step 0.4).

## Paring back: Joe's option, not the plan

Joe (2026-10-23): "I can pare it back on the future if need be." If he chooses to later, the research shows narrower
versions that are easier to launch: seller side first (the buyer side carries most of the human hours, WS1, WS4); the
attorney-brokered model with independent lawyers drafting (WS2 §3); or, on stopping, Joe's company licensing the software
for a fixed fee to an existing local brokerage, which is lawful for a non-licensee (WS2 §8) [INFERENCE, not researched].
None of these is the plan.
