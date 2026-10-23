# Licensed humans still negotiate, show and sign

*Workstream 1 deliverable (agent function inventory), 2026-10-23. Built from the two WS1 notes files and their
"Gap fill (2026-10-23, VPS session)" sections. Every function has a stable ID (F1 to F89) for other documents to cite.*

A New York buyer's agent, seller's agent and their broker perform **89 distinct functions**; software can do
**22 of them alone**, **46 mostly** (a person approves, signs or attends one step), and **21 still need a
person**, 19 of those at least partly because the law says so. The 21 are not the paperwork. They are the core
of the job: negotiating price and terms for a client (the statute defines a broker by exactly that act),
conducting showings and open houses (the Department of State has treated an unlicensed person showing listings
as unlicensed brokerage), choosing and explaining whose agent the firm is (a "replace both agents" product is a
dual agent in every in-house sale), drafting the contract and giving legal advice (attorneys' work, done by an
attorney, usually the seller's, in all six Hudson Valley county surveys found), holding deposits, and holding the licence and
supervising everything done under it. So the product that New York law allows is **software that does the file
work for a licensed broker who personally performs a short list of decisive acts on every deal**, not an
autonomous agent. Plainly against the kill criteria: this **partly hits A1** (one licensee is enough in law,
but only as fast as he can personally negotiate, show or delegate showings, and approve), **hits A6 as worded**
(buyer tours cannot be human-free inside a brokerage), **meets the first half of A3's kill criterion** (a lawyer
on each side is the Hudson Valley norm and brokers may only fill in blanks subject to attorney approval), and
**hits K4 if the venture is pitched as autonomous** (it dodges K4 if built as licensee-in-the-loop). None of
this kills the venture: the licensed acts are few, short and schedulable, the attorney-founder can hold a broker
licence for $185 with no course or exam, and a typical financed Hudson Valley sale takes three to four months,
most of it attorney, lender and title work that the software can track but the brokerage does not perform.

## How the inventory was built and what the three classes mean

The inventory comes from the State's own description of the job (the Department of State (DOS) course
syllabi for the 77-hour salesperson and 75-hour broker courses), the licensing statute (Real Property Law
(RPL) Article 12-A), the broker rules (19 NYCRR Part 175, cited below as "175.x"), DOS legal memoranda and
disciplinary decisions, Court of Appeals cases on agents' duties, the New York State Bar Association's county
closing-custom sheets, Hudson Valley market data from OneKey MLS (the multiple listing service, or MLS, that
brokers in Dutchess, Orange, Putnam, Rockland and Sullivan use to share listings), and the National
Association of REALTORS' own 179-item list of what agents do. A "licensee" is a licensed broker, associate broker
or salesperson; the "broker of record" is the licensed broker responsible for a firm.

Each function is classed exactly one way. **Fully automatable** means software can perform the whole act with
no per-case human decision; the broker still answers for it in law, because DOS holds the broker responsible for
"training, supervision and control" over everything non-licensed done in the firm's name
([DOS, Unlicensed Real Estate Assistants](https://dos.ny.gov/node/64166)) [PRIMARY]. **Partially automatable**
means software prepares, drafts, schedules, computes or delivers, but a person (a licensee, a party, or a vendor
on site) must decide, approve, sign or be present for at least one step in each case. **Human or licence
required** means the core of the act must be done by a person, and the "Why" column says whether the reason is
**legal** (with the statute, rule or case) or **practical** (physical presence, trust, judgement), so that WS2's
legal-constraint IDs (L-IDs) can be mapped to these F-IDs. "Side" is seller, buyer, both, or brokerage (duties of
the firm itself).

## Five licensed acts set the product's shape

**Negotiating for a client is the act that defines a broker, and software cannot be the one doing it.** The
statute defines a real estate broker as anyone who "for another and for a fee … offers or attempts to negotiate a
sale" ([RPL §440](https://www.nysenate.gov/legislation/laws/RPP/440)) [PRIMARY], and the agency-disclosure
statute already defines a buyer's agent as one who "presents an offer to purchase to the seller or seller's agent
and negotiates on behalf of the buyer" ([RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443))
[PRIMARY]. The State's broker course says the commission is earned when the licensee "negotiates a 'meeting of
the minds'" and that "preserving 'ready, willing and able' parties from contract to closing is the responsibility
of the licensee" ([DOS 75-hour broker syllabus](https://dos.ny.gov/real-estate-broker-75-hour-curriculum-eff-12212022))
[PRIMARY]. DOS's list of what unlicensed assistants may do contains no negotiation, offer or advice item
([DOS assistants page](https://dos.ny.gov/node/64166)) [PRIMARY], and a 2016 informal DOS position reported by a
practitioner was that moving the connection online "does not mean that a license is not required"
([Olshan, 2016](https://www.olshanlaw.com/Real-Estate-Law-Blog/Real-Estate-Websites-Broker-Regulation)) [SECONDARY].
So F47 (advising on offers), F48 (negotiating), F49 (negotiating buyer-broker pay and concessions), F58
(inspection repairs and credits) and F64 (keeping the deal together) are **Human or licence required**. The
software can run all the mechanics around them (deadlines, rounds, draft counters, logging that every offer was
conveyed), which matters: in one DOS case a broker who never passed a seller's counter-offer to his buyer was
suspended for six months ([DOS appeal decision, Lemecke](https://docs.dos.ny.gov/ooah/decisions/appeals/17%20DOS%20APP%2004%20Lemecke.htm))
[PRIMARY].

**Showings and open houses need a licensee or the owner, so buyer tours cannot be human-free.** In 1993 DOS held
that an unlicensed trainee who checked availability with the owners, discussed it with a prospect and showed him
other listings was "working as an unlicensed salesperson", and suspended the broker who let her
([DOS v. Ardelean, 96 DOS 93](https://docs.dos.ny.gov/ooah/decisions/rebrokers/ardelean.pdf)) [PRIMARY]. That
was a rental, but the definition it applied covers anyone associated with a broker "to … sell or offer for
sale" ([RPL §440(3)](https://www.nysenate.gov/legislation/laws/RPP/440)) [PRIMARY], and DOS's assistant list stops
at "Schedule appointments for licensees to show listed property" ([DOS assistants page](https://dos.ny.gov/node/64166))
[PRIMARY]. No sales-specific ruling was found, so this is the best available reading, not a settled rule. The
owner is the exception: a seller showing their own home is not acting "for another". F39 (accompanied showings)
and F40 (open houses) are therefore **Human or licence required** on legal and practical grounds; scheduling,
access codes and feedback (F37, F42) are fully automatable. **This hits A6 as worded** ("buyers will use a
software buyer's agent with no human agent for tours"): on the buyer side the brokerage must supply a licensed
person for tours, either the broker or a licensed salesperson he sponsors and pays (an unlicensed showing
helper cannot be paid per deal ([DOS assistants page](https://dos.ny.gov/node/64166)) [PRIMARY]). On the
listing side, owner-hosted showings and open houses are lawful and cost the brokerage nothing.

**A product that "replaces both agents" is a dual agent, and that reshapes the promise.** The six fiduciary
duties in New York attach to an "agent", defined as a licensed person "acting in a fiduciary capacity"
([RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443)) [PRIMARY]. DOS treats a brokerage and its agents
as one entity, so an in-house sale is dual agency and needs informed written consent from both sides
([DOS LI12](https://dos.ny.gov/legal-memorandum-li12-be-wary-dual-agency)) [PRIMARY]; the statutory form itself
warns that a dual agent "will not be able to provide the full range of fiduciary duties" ([RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443))
[PRIMARY]. The fix the statute offers, designated sales agents, requires two licensed salespersons or associate
brokers under the broker ([RPL §443(1)](https://www.nysenate.gov/legislation/laws/RPP/443)) [PRIMARY], which a
one-licensee firm does not have. And when two of the firm's buyers want the same house, the Court of Appeals says
an individual agent may not represent both without disclosure and consent, though the firm as a whole need not
stop its different agents from doing so ([Rivkin v Century 21 Teran Realty, 2008](https://www.law.cornell.edu/nyctap/I08_0056.htm))
[PRIMARY]; with one licensee acting for every buyer, the individual-agent rule bites. Choosing and documenting the
relationship (F11) and handling in-house deals (F51) are **Human or licence required**; delivering and logging the
disclosure forms (F9, F10) is partially automatable, and the step must be impossible to skip because failing to
give the form is a violation with no intent needed ([Lemecke](https://docs.dos.ny.gov/ooah/decisions/appeals/17%20DOS%20APP%2004%20Lemecke.htm))
[PRIMARY].

**The contract, the legal advice and the deposit belong to attorneys in the Hudson Valley.** A non-lawyer broker
may fill in the blanks of a simple form "subject to the approval of the respective attorneys for the parties", but
may not devise legal terms, give legal advice, discourage anyone from consulting a lawyer, or charge for preparing
a contract ([DOS LI04](https://dos.ny.gov/node/23931)) [PRIMARY]. The State's own salesperson course teaches the
question as "Who Prepares the Contract? Seller's attorney / Seller's broker / Purchaser's broker (purchase offer
contracts)" and "Upstate Contracts / Downstate Contracts" ([DOS 77-hour syllabus](https://dos.ny.gov/real-estate-salesperson-77-hour-curriculum-eff-12212022))
[PRIMARY]. The bar association's county sheets answer it for this market: in Columbia, Greene, Sullivan, Ulster and
Orange the seller's attorney prepares the contract, in Dutchess "an attorney" does, and in all six the seller's
attorney holds the deposit
([NYSBA practices by county](https://nysba.org/real-property-law-section-practices-by-county/)) [PRIMARY-adjacent,
sheets dated 2018–2019]. Contract drafting (F52), legal advice (F53) and deposit escrow (F55) are **Human or licence
required**. **From WS1's side this meets the first half of A3's kill criterion** ("the attorney-review custom
make[s] a lawyer on each side unavoidable"); WS2 owns the ethics half. The software's honest role is to assemble
the facts and pre-fill a bar-approved form for the attorneys, and to send the accepted-offer memorandum (F50).

**The licence and supervision are personal, and they cap throughput.** Holding the broker licence (F73) and a
New York place of business (F74) are cheap one-time acts for an attorney: secondary sources quoting the DOS
application say admitted attorneys skip the course, exam and experience and pay the $185 fee
([RealEstateU, updated 2026-09-14](https://realestateu.com/real-estate/guides/new-york-real-estate-broker-license))
[SECONDARY], and DOS lists the fee as $185 ([DOS](https://dos.ny.gov/become-real-estate-broker)) [PRIMARY]. The
binding constraint is supervision (F75): the rule requires "regular, frequent and consistent personal guidance,
instruction, oversight and superintendence" ([19 NYCRR 175.21](https://www.law.cornell.edu/regulations/new-york/19-NYCRR-175.21))
[PRIMARY]; "All listings, although perhaps negotiated by a salesperson, are accepted by the representative broker"
([DOS salesperson FAQ](https://dos.ny.gov/real-estate-salesperson-frequently-asked-questions)) [PRIMARY]; only the
broker may place advertising ([175.25](https://www.law.cornell.edu/regulations/new-york/19-NYCRR-175.25)) [PRIMARY];
and in November 2025 an appeals court upheld revoking the licences of a broker whose "wholesale failure to
supervise" let others trade on his licence ([Matter of Malul, 3d Dept, 2025 NY Slip Op 06110](https://www.nycourts.gov/reporter/3dseries/2025/2025_06110.htm))
[PRIMARY; full text blocked on re-check, citation and finding confirmed]. DOS has accepted written policies,
training and regular reminders as adequate supervision ([DOS v. Metalios, 2009](https://docs.dos.ny.gov/ooah/decisions/Real_estate/2009/Metalios_Menalaos.htm))
[PRIMARY], so software that produces approval queues, logs and sampling evidence helps. But no DOS rule, opinion
or decision addresses software doing licensed work; the only DOS statement on AI so far is a November 2025 alert
that AI-generated listing photos "may produce misleading or exaggerated representation of properties"
([DOS news release](https://dos.ny.gov/news/new-york-department-state-issues-new-trend-alert-warning-homebuyers-ai-generated-home-listings))
[PRIMARY]. **This is why A1 is partly hit**: one licensee is legally enough, but every listing accepted, every ad
approved, every negotiation and every tour he does not delegate is his own time, and approving more than he can
review is the Malul pattern.

## The State's 152 hours of training map onto the inventory

New York trains a salesperson in **77 hours** (plus a 3-hour exam) and a broker in a further **75 hours**, for
**152 hours** in total; both syllabi took effect on 21 December 2022, raised fair-housing training (salesperson
6 hours; broker 13 hours) and added broker hours on supervision, onboarding, teams and standard operating
procedures ([DOS 77-hour syllabus](https://dos.ny.gov/real-estate-salesperson-77-hour-curriculum-eff-12212022);
[DOS 75-hour syllabus](https://dos.ny.gov/real-estate-broker-75-hour-curriculum-eff-12212022)) [PRIMARY]. DOS's
March 2026 licence-law booklet prints the same subject tables unchanged
([DOS Real Estate License Law, March 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf))
[PRIMARY]. Licensees renew every two years with 22.5 hours of continuing education, from which admitted attorneys
are exempt ([same booklet, RPL §441(3)](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf);
[DOS broker FAQ](https://dos.ny.gov/real-estate-broker-frequently-asked-questions)) [PRIMARY]. The broker course
states its purpose plainly: "The role of the broker is to operate a brokerage in such a manner that all the
principles taught in the 77-Hour Salesperson's Course are implemented either through real estate services performed
directly by the broker or by the broker's sponsored licensees" ([DOS 75-hour syllabus](https://dos.ny.gov/real-estate-broker-75-hour-curriculum-eff-12212022))
[PRIMARY].

| Salesperson subject (19 NYCRR 176.3) | Hours | What it trains | Functions it maps to |
|---|---|---|---|
| License Law and Regulations | 3 | duties that require a licence, exemptions, advertising guidelines, unlicensed-assistant guidelines, Property Condition Disclosure Act, gas-well disclosure | F12, F13, F15, F26, F30, F73–F75 |
| Law of Agency | 11 | fiduciary duties, duties to the other party, agency types, dual and designated agency, informed consent, listing and buyer-agency forms, "first substantive meeting", broker supervision and records | F5, F6, F9–F11, F13, F17, F47, F51, F83, F84 |
| Legal Issues | 10 | estates, liens and easements, deeds, title closing and costs; the agent's pre-closing inspection with the purchaser | F14, F19, F62, F66, F67 |
| The Contract of Sales and Leases | 3 | contract elements, binders, purchase offers, who prepares the contract, who holds the down payment, attorney review clauses | F44, F50, F52, F53, F55 |
| Real Estate Finance | 5 | mortgages, predatory lending | F19, F60 |
| Land Use Regulations | 3 | zoning, planning | F14, F62 |
| Construction and Environmental Issues | 5 | building systems, environmental hazards | F16, F56, F57 |
| Valuation Process and Pricing Properties | 3 | CMA (comparative market analysis, "never … referred to as appraisals"), approaches to value | F21–F25 |
| Human Rights and Fair Housing | 6 | protected classes, steering, blockbusting, required notices, compliant advertising | F8, F18, F26, F30, F36, F78, F81 |
| Real Estate Mathematics | 1 | calculations | F21, F46, F70 |
| Municipal Agencies | 2 | permits, certificates of occupancy (CO) | F62 |
| Property Insurance | 1 | homeowner's insurance | F67 |
| Licensee Safety | 1 | personal safety in the field | F39, F40, F87 |
| Taxes and Assessments | 3 | property taxes, transfer taxes | F14, F19 |
| Condominiums and Cooperatives | 4 | condo and co-op purchases | F14 (rare in the target market) |
| Commercial and Investment Properties | 10 | commercial practice | none (residential product) |
| Income Tax Issues in Real Estate Transactions | 3 | tax effects | F19 (information only) |
| Mortgage Brokerage | 1 | mortgage brokers, dual-agency disclosure under Banking Law | F19 |
| Property Management | 2 | when a licence is required for management | none (out of scope) |

| Broker chapter (DOS 75-hour syllabus) | Hours | What it trains | Functions it maps to |
|---|---|---|---|
| 1 Agency Law, License Law and Operating a Real Estate Office | 26 | supervision and office managers, onboarding, agent safety (incl. cyber security), teams, standard operating procedures (SOPs), budgets and record keeping, escrow, advertising enforcement, MLS participation, unlicensed assistants, broker price opinions, special disclosures, insurance, "meeting of the minds", orchestrating the closing | F1, F12, F13, F48, F55, F64, F67, F69, F73–F80, F85–F88 |
| 2 Real Estate Finance | 7 | loan products, TRID closing disclosures | F19, F60 |
| 3 Real Property Investment | 4 | investment analysis | none (residential product) |
| 4 General Business Law | 3 | consumer-protection and business law | F1, F26, F89 |
| 5 Construction and Development | 3 | construction | F16 |
| 6 Conveyance of Real Property | 4 | deeds, closing | F62, F67 |
| 7 Real Property Management | 4 | management | none (out of scope) |
| 8 Taxes and Assessments | 3 | exemptions (STAR, seniors, veterans) | F14, F19 |
| 9 Advanced Fair Housing and Fair Lending | 13 | disparate impact, steering, implicit bias, cultural competency, assistance animals, source of income | F8, F18, F36, F78 |
| 10 Achieving Transactional Agreements through Transaction Analysis | 6 | representing the client's best interest in price, timing, contingencies, multiple offers, "Lawyer's unconditional approval" | F22, F23, F46–F49, F64 |
| 11 Local Issues and Concerns | 2 | cease-and-desist and nonsolicitation rules, zoning, wetlands, farmland | F3, F14, F81 |

Two things stand out. First, **12 of the 77 salesperson hours and about 13 of the 75 broker hours teach
commercial, investment, leasing or property-management work** (broker: investment 4, property management 4,
commercial financial analysis 2, commercial leasing 2, residential leasing 1, per the 176.4 table in the
[March 2026 booklet](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf)
[PRIMARY]) that a residential sales product does not need. Second, the subjects that carry
the most hours (agency at 11, office operation and supervision at 26, fair housing at 6 plus 13) map almost
entirely onto the Human and Partially classes: the State spends most of its training time on judgement,
loyalty and supervision, which is exactly what software cannot take over.

## Six fiduciary duties attach to a person, not a program

New York's statutory form lists the duties a seller's or buyer's agent owes the client: "reasonable care,
undivided loyalty, confidentiality, full disclosure, obedience and duty to account"; the broker syllabus lists the
same six in the order often remembered as OLDCAR (obedience, loyalty, disclosure, confidentiality, accounting,
reasonable care) ([RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443); [DOS 75-hour syllabus](https://dos.ny.gov/real-estate-broker-75-hour-curriculum-eff-12212022))
[PRIMARY]. The Court of Appeals calls a broker "a fiduciary with a duty of loyalty and an obligation to act in the
best interests of the principal", and where loyalties are divided the disclosure "must lay bare the truth, without
ambiguity or reservation, in all its stark significance" ([Dubbs v Stribling & Associates, 2001](https://www.law.cornell.edu/nyctap/I01_0072.htm))
[PRIMARY]. The statute preserves the common law of agency on top of the form (§443(6)) and exempts a licensee who
works with a party "in a capacity other than as an agent" by agreement (§443(5)) ([RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443))
[PRIMARY]; whether that non-agent route works as a reduced-duty "facilitator" model is untested in any source found.

| Duty | Where NY states it | What it means in practice | What a software-led service must do | F-IDs |
|---|---|---|---|---|
| Obedience | §443 form; broker syllabus | follow the client's lawful instructions | never override a client choice; refuse unlawful (e.g., discriminatory) instructions and route them to the licensee | F22–F24, F84 |
| Undivided loyalty | §443 form; Dubbs; Rivkin; LI12 | act only in the client's interest; no undisclosed conflicts | detect same-property conflicts across clients; force dual-agency consent; separate seller and buyer workspaces | F11, F51, F82 |
| Disclosure (full) | §443 form; Dubbs; Lemecke | tell the client everything material, including every offer | log and deliver every offer and counteroffer at once; no suppression by design | F45, F47, F65 |
| Confidentiality | §443 form | keep the client's position (e.g., lowest price) private | information walls between sides; access logs; personal-data controls (WS2) | F51, F84, F87 |
| Accounting | §443 form; 175.1–175.2 | account for money and documents | ledgers, receipts, three-year records | F55, F69, F79 |
| Reasonable care (and skill) | §443 form; salesperson syllabus "competence, diligence, documentation" | competent pricing, disclosures, deadlines | checklists, deadline engine, data checks; the licensee still owns the advice | F15, F21–F23, F60 |

The form also sets duties to the **other** party: "exercise reasonable skill and care", "deal honestly, fairly and
in good faith", and disclose known facts materially affecting the property's value (seller's agent) or the buyer's
ability to perform (buyer's agent) ([RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443)) [PRIMARY]
(F33, F83). For a software-led service the consequence is structural: the duties belong to a named licensed person,
so every client must have one, and the software's job is to make that person's duties easy to perform and hard to
breach, with evidence.

## A Hudson Valley sale takes three to four months, and attorneys run the middle

The listing side moves from listing to an accepted offer in **35 to 55 days** in most Hudson Valley counties (Q3
2026 single-family averages: Putnam 35, Rockland 40, Dutchess 51, Orange 52, Ulster 55; Sullivan 87), measured by
OneKey MLS from listing to accepted offer ([OneKey Dutchess Q3-2026](https://corporate.onekeymls.com/s/DutchessCounty-mrmd.pdf);
[Putnam](https://corporate.onekeymls.com/s/PutnamCounty-zrtw.pdf); [Rockland](https://corporate.onekeymls.com/s/RocklandCounty-k7m2.pdf);
[Orange](https://corporate.onekeymls.com/s/OrangeCounty-8rdl.pdf); [Ulster](https://corporate.onekeymls.com/s/UlsterCounty-42g5.pdf);
[Sullivan](https://corporate.onekeymls.com/s/SullivanCounty-p6kb.pdf)) [PRIMARY, data as of 7 October 2026]. It is
seasonal: Dutchess took 66 days in Q1 2026 and 60 in Q2, against 51 in Q3 ([OneKey Dutchess Q3-2026, p.8](https://corporate.onekeymls.com/s/DutchessCounty-mrmd.pdf))
[PRIMARY]. An accepted offer is not binding in this region until the attorneys exchange a signed contract and the
deposit ([Boeckelman, Westchester practitioner](https://boeckelman.realgeeks.com/accepted-offer-seller-version/))
[SECONDARY]. No 2026 days-on-market figure was found for Columbia and Greene, which use a different MLS.

| Step (financed sale, Hudson Valley) | Typical timing | Who acts | Source |
|---|---|---|---|
| Listing agreement, agency and fair-housing notices, PCDS (property condition disclosure statement), photos, MLS entry | before listing | listing licensee (accepts listing, explains forms); seller (completes PCDS); photographer | [175.24](https://www.law.cornell.edu/regulations/new-york/19-NYCRR-175.24); [RPL §462](https://www.nysenate.gov/legislation/laws/RPP/462) [PRIMARY] |
| Listing to accepted offer | 35–55 days in most counties (Q3 2026); longer in winter | listing licensee, buyers' licensees, seller | OneKey quarterly reports above [PRIMARY] |
| Accepted-offer memorandum to both parties and both attorneys | day of acceptance | brokers | [Boeckelman](https://boeckelman.realgeeks.com/accepted-offer-seller-version/) [SECONDARY] |
| Home inspection (plus radon, well, septic) | within about a week of acceptance, before the contract | licensed home inspector; buyer's licensee arranges; listing side gives access | [Rand Realty, 2026](https://jeselle.randrealty.com/?p=79) [SECONDARY]; [RPL §444-d](https://www.nysenate.gov/legislation/laws/RPP/444-D) [PRIMARY] |
| Contract drafted, negotiated and signed; deposit paid into the seller's attorney's escrow | 1–2 weeks after acceptance; deposit custom 10% (Ulster), 5% (Orange), $1,000–$5,000 (Columbia, Greene, Sullivan) | seller's attorney drafts; buyer's attorney reviews | [Rand](https://jeselle.randrealty.com/?p=79) [SECONDARY]; [NYSBA Ulster](https://nysba.org/wp-content/uploads/2020/02/Ulster-2.pdf), [Orange](https://nysba.org/wp-content/uploads/2020/02/Orange.pdf), [Columbia](https://nysba.org/wp-content/uploads/2020/02/Columbia-2.pdf) [PRIMARY-adjacent, 2018] |
| Mortgage application, appraisal, commitment | application after the executed contract; commitment window typically 45 days; underwriting 30–45 days | lender; lender-ordered appraiser (agents may only supply information) | [Boeckelman](https://boeckelman.realgeeks.com/accepted-offer-seller-version/), [Angiuli & Gentile, 2022](https://industrym.com/point-of-sale/) [SECONDARY]; [12 CFR 1026.42](https://www.consumerfinance.gov/rules-policy/regulations/1026/42/) [PRIMARY] |
| Title search, municipal searches, survey (customary only for new construction in most HV counties) | weeks 2–7 | buyer's attorney orders; title company or abstract company; seller's attorney clears objections | [NYSBA Columbia](https://nysba.org/wp-content/uploads/2020/02/Columbia-2.pdf), [Ulster](https://nysba.org/wp-content/uploads/2020/02/Ulster-2.pdf) [PRIMARY-adjacent] |
| Final walkthrough | 24–48 hours before closing | buyer (with licensee or alone with access) | [Rand](https://jeselle.randrealty.com/?p=79) [SECONDARY] |
| Closing | about 45–60 days after acceptance; contracts say "on or about", which moves up to 30 days either way | attorneys; the lender's ("bank") attorney disburses; title company records the deed; brokers are paid at closing | [Rand](https://jeselle.randrealty.com/?p=79), [Angiuli & Gentile](https://industrym.com/point-of-sale/) [SECONDARY]; [NYSBA Greene](https://nysba.org/wp-content/uploads/2020/02/Greene-2.pdf) [PRIMARY-adjacent] |

[INFERENCE] Adding the pieces, a financed Hudson Valley sale takes roughly **three to four months from listing to
closing**. On the buyer side, the national median search is **10 weeks** ([Virginia REALTORS summary of NAR 2025
Profile](https://virginiarealtors.org/2025/12/08/key-takeaways-from-nars-2025-profile-of-home-buyers-and-sellers))
[SECONDARY], so a buyer typically spends **four to five months from starting to look to closing** [INFERENCE]. The
licensee's own work clusters at the two ends: before the accepted offer (pricing, marketing, showings, negotiation)
and in short bursts afterwards (inspection negotiation, walkthrough, problem-solving). The middle six to eight weeks
are attorney, lender and title work that the brokerage tracks (F59–F63) but does not perform.

Upstate New York outside the Hudson Valley works differently, which matters if the venture expands. In the Capital
Region and Rochester the broker fills in the purchase contract on an MLS or bar form subject to attorney approval,
and the broker usually holds a small deposit ($500–$2,000 in Albany; $1,000–$2,000 in Monroe)
([NYSBA Albany](https://nysba.org/wp-content/uploads/2020/02/Albany.pdf); [NYSBA Monroe](https://nysba.org/wp-content/uploads/2020/02/Monroe.pdf))
[PRIMARY-adjacent, 2018]. The Court of Appeals enforces those approval clauses as written: either attorney may
disapprove "for any reason or for no stated reason", commonly within three business days
([Moran v Erk, 2008](https://www.law.cornell.edu/nyctap/I08_0176.htm)) [PRIMARY]. Upstate, F44 (offer drafting)
becomes a fill-in contract and F55 brings in the broker escrow rules (175.1).

## The inventory: 89 functions in nine stages

The table below is the core of this deliverable. Stage keys: **BD** business development and client acquisition;
**Intake** listing intake and agreements, including buyer engagement; **Pricing**; **Marketing**; **Showings**,
including buyer search; **Offers** offers and negotiation; **Close** contract to close; **Post** post-close;
**Comply** ongoing duties and compliance. Short source links: "Booklet 2026" is the
[DOS Real Estate License Law (March 2026)](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf),
which prints Article 12-A and Part 175 [PRIMARY]; "DOS assistants" is the [DOS unlicensed-assistant page](https://dos.ny.gov/node/64166)
[PRIMARY]; "NAR 179" is NAR's [179 Ways list](https://www.nar.realtor/sites/default/files/documents/2023_179_ways_real_estate_pros_8.5x11_pages_final.pdf)
[PRIMARY].

### Stage 1: business development and client acquisition

| ID | Function | Side | Stage | Classification | Why (legal rule or practical reason) | What the software can do | Source |
|---|---|---|---|---|---|---|---|
| F1 | Market the brokerage itself (website, social, e-mail, ads, content) | brokerage | BD | Partially automatable | Legal: all promotion is "advertising" (websites, e-mail, business cards) that only the broker may place, naming the broker; fair-housing link on the homepage; SOPs posted on the site | Draft and schedule; insert required broker data and links; block non-compliant drafts; broker approves templates | [Booklet 2026 (175.25, 175.29)](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf); [RPL §442-h](https://www.nysenate.gov/legislation/laws/RPP/442-H) [PRIMARY] |
| F2 | Answer inquiries 24/7 and triage leads | both | BD | Partially automatable | Legal: answering phones and booking are permitted unlicensed tasks; discussing a person's needs or a home's availability is first substantive contact and was salesperson activity in Ardelean | Instant answers from approved facts; send required notices; book a licensee; hand off price, terms and advice | [DOS assistants](https://dos.ny.gov/node/64166); [Ardelean](https://docs.dos.ny.gov/ooah/decisions/rebrokers/ardelean.pdf) [PRIMARY] |
| F3 | Prospect for listings (expired listings, owners selling alone, mailers) | seller | BD | Partially automatable | Legal: blockbusting ban; cease-and-desist list (one zone left, in Brooklyn, to 1 July 2028; none in the Hudson Valley); outreach is advertising. Practical: door-knocking is in person | Screen lists; generate letters for broker approval | [Booklet 2026 (175.17)](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf) [PRIMARY] |
| F4 | Win clients through referrals, reputation and local relationships | brokerage | BD | Human or licence required | Practical (trust): 91% of buyers would reuse or recommend their agent; most clients find agents by referral or prior use | Contact management, past-client touches, review requests | [NAR release, Nov 2025](https://www.nar.realtor/newsroom/first-time-home-buyer-share-falls-to-historic-low-of-21-median-age-rises-to-40) [PRIMARY]; [Virginia REALTORS](https://virginiarealtors.org/2025/12/08/key-takeaways-from-nars-2025-profile-of-home-buyers-and-sellers) [SECONDARY] |
| F5 | Listing presentation and seller consultation | seller | BD | Partially automatable | Legal: agency form before any listing agreement. Practical: sellers choose on trust | Build the presentation (market data, plan, fee); licensee presents | [RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443) [PRIMARY]; NAR 179 items 23–35 |
| F6 | Buyer consultation and needs analysis | buyer | BD | Partially automatable | Legal: agency form before a buyer-agency agreement; SOPs applied uniformly. Practical: judgement | Guided intake, process education, document checklist | [RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443); [RPL §442-h](https://www.nysenate.gov/legislation/laws/RPP/442-H) [PRIMARY] |
| F7 | Set and negotiate the client's fee | both | BD | Partially automatable | Legal: only a licensed broker can sue for a fee; MLS buyer agreements must state a specific, negotiable amount | Publish and quote a flat fee; deviations are the broker's call | [RPL §442-d](https://www.nysenate.gov/legislation/laws/RPP/442-D); [NAR buyer agreements](https://www.nar.realtor/the-facts/written-buyer-agreements-101) [PRIMARY] |

### Stage 2: listing intake and agreements (and buyer engagement)

| ID | Function | Side | Stage | Classification | Why (legal rule or practical reason) | What the software can do | Source |
|---|---|---|---|---|---|---|---|
| F8 | Deliver the DOS fair-housing notice at first substantive contact | both | Intake | Fully automatable | 175.28 allows e-mail, text or a link; oral delivery does not count; keep three years; a refusal needs the licensee's sworn declaration (exception path) | Auto-send at first contact, log, retain; route refusals to the licensee | [175.28](https://www.law.cornell.edu/regulations/new-york/19-NYCRR-175.28) [PRIMARY] |
| F9 | Give own client the agency disclosure form (seller before listing; buyer before buyer agreement); signed acknowledgment kept three years | both | Intake | Partially automatable | Legal: §443(3); failure is a violation with no intent needed; the form names the licensee; refusal needs a sworn declaration | E-deliver, e-sign, block the next step until done, store; licensee named and available to explain | [RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443); [Lemecke](https://docs.dos.ny.gov/ooah/decisions/appeals/17%20DOS%20APP%2004%20Lemecke.htm) [PRIMARY] |
| F10 | Give the other side's party the agency form at first substantive contact | both | Intake | Partially automatable | Legal: §443(3)(b)–(c); "first substantive contact" is undefined, so the safe reading is the first exchange beyond generic information | Trigger on the first substantive exchange; log | [RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443) [PRIMARY] |
| F11 | Decide and document the agency relationship (single, dual with informed written consent, designated agents, or non-agent) | brokerage | Intake | Human or licence required | Legal: §443(1), (4), (5); a brokerage and its agents are one entity; disclosure must "lay bare the truth" | Detect conflicts; generate consent forms; log | [RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443); [DOS LI12](https://dos.ny.gov/legal-memorandum-li12-be-wary-dual-agency); [Dubbs](https://www.law.cornell.edu/nyctap/I01_0072.htm) [PRIMARY] |
| F12 | Accept the listing or client (engagement decision, conflict check) | brokerage | Intake | Human or licence required | Legal: listing "for another and for a fee" is the core broker act; "All listings … are accepted by the representative broker" | Prepare the acceptance file (facts, conflicts, risk flags) | [RPL §440](https://www.nysenate.gov/legislation/laws/RPP/440); [DOS salesperson FAQ](https://dos.ny.gov/real-estate-salesperson-frequently-asked-questions) [PRIMARY] |
| F13 | Prepare and sign the listing agreement | seller | Intake | Partially automatable | Legal: broker is the contracting party; six-point exclusive-listing explanation initialled and MLS offer-routing option (175.24); fixed end date (175.15); no net listing (175.19); owner authority to offer, advertise and place a sign (175.10, 175.11, 175.25); copy at once (175.12); bold Commission Escrow Act notice | Generate, validate every mandatory clause, e-sign, deliver the copy, store | [Booklet 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf); [RPL §294-b](https://www.nysenate.gov/legislation/laws/RPP/294-B) [PRIMARY] |
| F14 | Gather property facts (owner and deed, taxes, lot, zoning, CO and permits, utilities, septic and well, HOA, inclusions) | seller | Intake | Fully automatable | DOS lets unlicensed staff "Gather information for a comparative market analysis"; mostly public records and seller answers | Public-record pulls, seller questionnaire, uploads, gap list | [DOS assistants](https://dos.ny.gov/node/64166) [PRIMARY]; NAR 179 items 7–15, 47–56 |
| F15 | Tell the seller of disclosure duties and track them (PCDS form in force since 1 July 2025; lead paint for pre-1978 homes; other NY notices) | seller | Intake | Fully automatable | Legal duty is to inform (§466); the agent must ensure lead-paint compliance (40 CFR 745.115); licensees should not fill in the PCDS for the seller | Version-stamped forms, triggers (year built, septic), signatures, delivery proof | [RPL §462](https://www.nysenate.gov/legislation/laws/RPP/462); [40 CFR 745.115](https://www.law.cornell.edu/cfr/text/40/745.115) [PRIMARY]; [HGAR/NYSAR](https://hgar.com/nysar-legal-update-amended-pcds-must-be-used-beginning-july-1-2025) [SECONDARY] |
| F16 | Advise on preparing the home (repairs, staging, curb appeal; optional pre-listing inspection) | seller | Intake | Partially automatable | Practical: needs eyes on the property and judgement | Photo-based suggestions, cost ranges, vendor booking (inspection offer: WS6) | NAR 179 items 17, 73–74 |
| F17 | Sign a written buyer agreement before any tour | buyer | Intake | Partially automatable | Legal/contractual: binding on MLS participants since 17 Aug 2024 (specific, capped, "not set by law and are fully negotiable"); broker is the party; a statute (S9564) is pending | Generate, explain, e-sign; block tour booking until signed | [NAR buyer agreements](https://www.nar.realtor/the-facts/written-buyer-agreements-101); [S9564](https://www.nysenate.gov/legislation/bills/2025/S9564) [PRIMARY] |
| F18 | Apply the firm's SOPs (ID, agreement, pre-approval) identically to every buyer | buyer | Intake | Fully automatable | §442-h(4) requires published SOPs; uniform application is the fair-housing safeguard | Same gate for every buyer, logged | [RPL §442-h](https://www.nysenate.gov/legislation/laws/RPP/442-H) [PRIMARY] |
| F19 | Check financing readiness (pre-approval, loan basics, closing-cost estimates) | buyer | Intake | Fully automatable | Information only; negotiating residential mortgage loans is outside the real estate licence (DFS registration) | Collect and verify the letter; cost calculators; no loan negotiation | [DOS salesperson FAQ](https://dos.ny.gov/real-estate-salesperson-frequently-asked-questions); [RPL §440](https://www.nysenate.gov/legislation/laws/RPP/440) [PRIMARY] |
| F20 | Order and coordinate vendors (photographer, stager, contractors, inspectors) | both | Intake | Fully automatable | DOS lets unlicensed staff "Order items of repair as directed by the broker" | Booking, reminders, access codes, invoices | [DOS assistants](https://dos.ny.gov/node/64166) [PRIMARY] |

### Stage 3: pricing

| ID | Function | Side | Stage | Classification | Why (legal rule or practical reason) | What the software can do | Source |
|---|---|---|---|---|---|---|---|
| F21 | Research comparable sales; prepare the CMA, automated estimate and net sheet | both | Pricing | Fully automatable | Data work DOS lets unlicensed staff do; an estimate made only by an automated model is not a Reg Z "valuation"; a CMA "may never be referred to as" an appraisal | Comps, adjustments, ranges, net proceeds | [DOS assistants](https://dos.ny.gov/node/64166); [12 CFR 1026.42](https://www.consumerfinance.gov/rules-policy/regulations/1026/42/); [DOS 77-h syllabus](https://dos.ny.gov/real-estate-salesperson-77-hour-curriculum-eff-12212022) [PRIMARY] |
| F22 | Advise the seller on list price and strategy | seller | Pricing | Partially automatable | Legal: reasonable care is a fiduciary duty; a licensee's estimate is a covered person's "valuation" under Reg Z | Proposed range with reasons; licensee reviews and owns the advice | [RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443); [12 CFR 1026.42](https://www.consumerfinance.gov/rules-policy/regulations/1026/42/) [PRIMARY] |
| F23 | Advise the buyer on offer price and terms | buyer | Pricing | Partially automatable | Legal: fiduciary reasonable care and loyalty | Comps for the target home; offer scenarios | [RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443) [PRIMARY] |
| F24 | Recommend price changes from market response | seller | Pricing | Partially automatable | Legal: fiduciary advice; the seller authorises any change | Weekly market-response analysis with a draft recommendation | NAR 179 items 90, 104–108 |
| F25 | Support the appraisal (supply comps and facts, ask for corrections, never pressure) | both | Pricing | Fully automatable | Reg Z lets agents supply information and request corrections, and bars influencing value | Comps packet; log of all contact | [12 CFR 1026.42](https://www.consumerfinance.gov/rules-policy/regulations/1026/42/) [PRIMARY] |

### Stage 4: marketing

| ID | Function | Side | Stage | Classification | Why (legal rule or practical reason) | What the software can do | Source |
|---|---|---|---|---|---|---|---|
| F26 | Write the listing description and marketing copy | seller | Marketing | Partially automatable | Legal: ads must be "honest and accurate" (175.25(c)(9)); misleading advertising is a §441-c ground; DOS lets staff "Write ads for approval of broker"; fair-housing wording | Draft; run fair-housing and accuracy checks; broker approves each listing's copy | [Booklet 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf); [DOS assistants](https://dos.ny.gov/node/64166) [PRIMARY] |
| F27 | Produce photos, video, floor plans, measurements; keep images truthful | seller | Marketing | Partially automatable | Practical: someone must be on site. Legal: DOS warned (Nov 2025) that AI-generated images can be misleading advertising; written permission for others' photos | Book the photographer; flag undisclosed image alteration; floor plans from scans | [DOS AI alert](https://dos.ny.gov/news/new-york-department-state-issues-new-trend-alert-warning-homebuyers-ai-generated-home-listings) [PRIMARY]; NAR 179 items 38–39, 81 |
| F28 | Enter the listing on the MLS; keep status and price current | seller | Marketing | Partially automatable | Legal/contractual: entry is by the participating broker's subscribers (whether it can be automated: WS3) | Complete, validated data package; status and price-change prompts | [OneKey products](http://corporate.onekeymls.com/benefits-products) [PRIMARY]; [LIBOR rule tips](https://www.lirealtor.com/brokers-agents/member-resources/customer-service-tips/onekey-mls-rules-compliance) [SECONDARY] |
| F29 | Syndicate to Zillow, Realtor.com, Redfin and IDX sites | seller | Marketing | Fully automatable | Happens through the MLS feed once the listing is entered | Monitor that portals show the right data | [OneKey products](http://corporate.onekeymls.com/benefits-products) [PRIMARY] |
| F30 | Run digital campaigns (listing page, social, e-mail, paid ads) | seller | Marketing | Partially automatable | Legal: the broker places all ads; discrimination findings are presumptive untrustworthiness (175.17(b)), so ad targeting must avoid protected classes | Build and schedule; no protected-class targeting; broker approves | [Booklet 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf) [PRIMARY] |
| F31 | Signs and print (yard sign, flyers, brochures, mailers) | seller | Marketing | Partially automatable | Practical: install and print. Legal: owner consent for a sign (175.11); the sign must name the broker (175.25) | Design and order; a vendor installs | [Booklet 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf) [PRIMARY] |
| F32 | Advise on and record the marketing-exposure choice (full MLS vs office-exclusive or delayed) | seller | Marketing | Partially automatable | Legal: the seller's informed decision; if A10679-B is signed, public marketing becomes the default and opting out needs a signed state form kept three years | Explain options; capture the signed choice | [A10679](https://www.nysenate.gov/legislation/bills/2025/A10679) [PRIMARY] |
| F33 | Answer buyers' and buyer agents' questions about the listing | seller | Marketing | Partially automatable | Legal: discussing availability and listings with prospects is salesperson activity (Ardelean); honesty and known-defect disclosure to the non-client (§443 form) | Answer from an approved fact sheet; escalate price, terms and negotiation | [Ardelean](https://docs.dos.ny.gov/ooah/decisions/rebrokers/ardelean.pdf); [RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443) [PRIMARY] |
| F34 | Report activity and progress to the seller | seller | Marketing | Fully automatable | Information only | Dashboards, weekly summaries | NAR 179 items 106–107 |

### Stage 5: showings (and buyer search)

| ID | Function | Side | Stage | Classification | Why (legal rule or practical reason) | What the software can do | Source |
|---|---|---|---|---|---|---|---|
| F35 | Run the buyer's home search (saved searches, alerts, listing details) | buyer | Showings | Fully automatable | Information delivery, within IDX/VOW display rules (WS3); no steering filters | Search portal and alerts | [OneKey products](http://corporate.onekeymls.com/benefits-products) [PRIMARY] |
| F36 | Give neighbourhood, school and community information | buyer | Showings | Partially automatable | Legal: steering is unlawful discrimination and presumptive untrustworthiness (175.17(b)); NAR's item "explain impact of schools on market value" is a New York risk | Neutral links to official data only; no area recommendations | [Booklet 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf) [PRIMARY]; NAR 179 item 19 |
| F37 | Schedule showings, get seller approval, send access instructions and feedback requests | both | Showings | Fully automatable | DOS permits unlicensed staff to "Schedule appointments for licensees to show listed property"; ShowingTime already does this | Calendar, approvals, instructions, reminders | [DOS assistants](https://dos.ny.gov/node/64166); [ShowingTime](https://www.showingtime.com/) [PRIMARY] |
| F38 | Place and manage the lockbox | seller | Showings | Partially automatable | Practical: physical install. Legal/contractual: owner authorisation; SentriLock gives codes only to registered users | Access logs; temporary vendor codes | [SentriLock](https://www.sentrilock.com/) [PRIMARY] |
| F39 | Conduct showings and private tours | both | Showings | Human or licence required | Legal + practical: DOS treated an unlicensed person showing listings as unlicensed salesperson activity; DOS's assistant list stops at scheduling; physical presence and safety. A seller showing their own home is not acting "for another" | Route planning, property briefs, safety check-ins, post-tour notes | [Ardelean](https://docs.dos.ny.gov/ooah/decisions/rebrokers/ardelean.pdf); [DOS assistants](https://dos.ny.gov/node/64166); [RPL §440](https://www.nysenate.gov/legislation/laws/RPP/440) [PRIMARY] |
| F40 | Host open houses | seller | Showings | Human or licence required | Practical + legal: someone must be there; same licensing reading as showings; fair-housing notice displayed at open houses (175.29(d)); the owner may host their own | Scheduling, digital sign-in, follow-up | [Booklet 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf); [Ardelean](https://docs.dos.ny.gov/ooah/decisions/rebrokers/ardelean.pdf) [PRIMARY] |
| F41 | Live virtual tours | both | Showings | Partially automatable | Legal/contractual: a live virtual tour counts as touring under the buyer-agreement rule. Practical: a person operates the camera | Scheduling, recording, captions | [NAR buyer agreements](https://www.nar.realtor/the-facts/written-buyer-agreements-101) [PRIMARY] |
| F42 | Collect and analyse showing feedback | seller | Showings | Fully automatable | Information | Automatic requests, summaries | [ShowingTime](https://www.showingtime.com/) [PRIMARY] |
| F43 | Evaluate homes with the buyer (spot issues, compare options) | buyer | Showings | Partially automatable | Practical: judgement, often on site; 54% of buyers say their agent pointed out issues they would have missed | Checklists from listing data and photos; comparison sheets | [Virginia REALTORS](https://virginiarealtors.org/2025/12/08/key-takeaways-from-nars-2025-profile-of-home-buyers-and-sellers) [SECONDARY] |

### Stage 6: offers and negotiation

| ID | Function | Side | Stage | Classification | Why (legal rule or practical reason) | What the software can do | Source |
|---|---|---|---|---|---|---|---|
| F44 | Draft the buyer's offer (Hudson Valley: non-binding offer sheet or binder; upstate: fill-in contract subject to attorney approval) | buyer | Offers | Partially automatable | Legal: brokers may only fill in blanks on simple forms subject to attorney approval, add no legal terms, charge no separate fee; upstate approval clauses are enforced as written | Structured offer from the buyer's choices; mandatory attorney-approval wording | [DOS LI04](https://dos.ny.gov/node/23931); [Moran v Erk](https://www.law.cornell.edu/nyctap/I08_0176.htm) [PRIMARY] |
| F45 | Submit and present offers; affirm presentation on request; route per the listing agreement | both | Offers | Partially automatable | Legal: the buyer's agent "presents an offer … and negotiates"; offer routing per 175.24(c) | Transmission, time stamps, delivery proof; licensee presents with advice | [RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443); [175.24](https://www.law.cornell.edu/regulations/new-york/19-NYCRR-175.24) [PRIMARY] |
| F46 | Compare offers; prepare net sheets | seller | Offers | Fully automatable | Arithmetic and comparison | Side-by-side terms, net proceeds, risk flags | NAR 179 items 110, 118 |
| F47 | Advise the client on each offer and counteroffer, and convey every one | both | Offers | Human or licence required | Legal: fiduciary loyalty and full disclosure; a broker who did not convey a counteroffer was suspended (with a §443 violation) | Ensure every offer is logged and delivered at once; draft pros and cons | [Dubbs](https://www.law.cornell.edu/nyctap/I01_0072.htm); [Lemecke](https://docs.dos.ny.gov/ooah/decisions/appeals/17%20DOS%20APP%2004%20Lemecke.htm) [PRIMARY] |
| F48 | Negotiate price and terms for the client (counters, multiple-offer rounds) | both | Offers | Human or licence required | Legal: a broker "offers or attempts to negotiate a sale" for another for a fee (§440(1)); a buyer's agent "negotiates on behalf of the buyer" (§443(1)); commission earned by negotiating a "meeting of the minds" | Run deadlines and rounds; draft counters for a licensee who decides and speaks | [RPL §440](https://www.nysenate.gov/legislation/laws/RPP/440); [RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443); [DOS 75-h syllabus](https://dos.ny.gov/real-estate-broker-75-hour-curriculum-eff-12212022) [PRIMARY] |
| F49 | Negotiate buyer-broker pay and seller concessions between the sides | both | Offers | Human or licence required | Legal: negotiation; pay from more than one party only with the client's full knowledge and consent (175.7) | Model concession effects | [Booklet 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf) [PRIMARY] |
| F50 | Send the accepted-offer memorandum to both parties and both attorneys | both | Offers | Fully automatable | Information assembly; copies of broker-prepared papers go out at once (175.12) and are kept (175.23) | Generate, send, file | [Boeckelman](https://boeckelman.realgeeks.com/accepted-offer-seller-version/) [SECONDARY]; [175.23](https://www.law.cornell.edu/regulations/new-york/19-NYCRR-175.23) [PRIMARY] |
| F51 | Handle in-house deals and competing buyers (dual-agency consent, designated agents, information walls) | brokerage | Offers | Human or licence required | Legal: informed written consent; one agent may not represent competing buyers for one home without disclosure and consent; designated agents must be two licensees under the broker | Detect conflicts; separate workspaces; consent forms | [Rivkin](https://www.law.cornell.edu/nyctap/I08_0056.htm); [DOS LI12](https://dos.ny.gov/legal-memorandum-li12-be-wary-dual-agency); [RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443) [PRIMARY] |

### Stage 7: contract to close

| ID | Function | Side | Stage | Classification | Why (legal rule or practical reason) | What the software can do | Source |
|---|---|---|---|---|---|---|---|
| F52 | Draft the contract of sale and negotiate its legal terms | both | Close | Human or licence required | Legal: practice of law (Judiciary Law §§478, 484, as applied in LI04); in all six Hudson Valley county sheets an attorney drafts (the seller's attorney in five) | Assemble the data package; pre-fill a bar-approved form for the attorneys | [DOS LI04](https://dos.ny.gov/node/23931) [PRIMARY]; [NYSBA county sheets](https://nysba.org/real-property-law-section-practices-by-county/) [PRIMARY-adjacent] |
| F53 | Give legal advice (terms, riders, contingencies, title, deed) | both | Close | Human or licence required | Legal: brokers may not give legal advice | Plain-language summaries labelled "not legal advice"; route questions to the party's attorney | [DOS LI04](https://dos.ny.gov/node/23931) [PRIMARY] |
| F54 | Refer each party to their own attorney; hand off the file | both | Close | Partially automatable | Legal: brokers may not discourage parties from consulting attorneys; the attorney-founder's conflicts are WS2's subject | Attorney directory; secure file transfer | [DOS LI04](https://dos.ny.gov/node/23931) [PRIMARY] |
| F55 | Hold the down payment in escrow | both | Close | Human or licence required | Legal: Hudson Valley custom is the seller's attorney's escrow; a broker holding money needs a separate federally insured account, deposit within three business days, and accounting (175.1–175.2) | Track receipt and status; ledger if the broker ever holds funds | [175.1](https://www.law.cornell.edu/regulations/new-york/19-NYCRR-175.1) [PRIMARY]; [NYSBA Ulster](https://nysba.org/wp-content/uploads/2020/02/Ulster-2.pdf) [PRIMARY-adjacent] |
| F56 | Schedule inspections (home, radon, well, septic) and arrange access | buyer | Close | Partially automatable | Practical: someone must open the home. Legal: paid home inspections need a licensed inspector | Book licensed inspectors; coordinate access | [RPL §444-d](https://www.nysenate.gov/legislation/laws/RPP/444-D) [PRIMARY]; [Rand](https://jeselle.randrealty.com/?p=79) [SECONDARY] |
| F57 | Review the inspection report with the buyer | buyer | Close | Partially automatable | Practical: judgement; no legal advice | Summarise findings, cost ranges, questions for the inspector | NAR 179 item 145 |
| F58 | Negotiate repairs or credits after inspection | both | Close | Human or licence required | Legal: negotiation (§440); the result goes into the attorney-drafted contract | Draft the request list and options | [RPL §440](https://www.nysenate.gov/legislation/laws/RPP/440) [PRIMARY] |
| F59 | Make sure the PCDS reaches the buyer before a binding contract and is attached | both | Close | Fully automatable | §462 timing; §466 duty to inform | Delivery proof; contract-attachment checklist | [RPL §462](https://www.nysenate.gov/legislation/laws/RPP/462) [PRIMARY] |
| F60 | Track mortgage application, commitment date and contingency deadlines | both | Close | Fully automatable | DOS lets unlicensed staff follow up loan commitments; commitment windows are typically 45 days | Deadline engine from the executed-contract date | [DOS assistants](https://dos.ny.gov/node/64166) [PRIMARY]; [Angiuli & Gentile](https://industrym.com/point-of-sale/) [SECONDARY] |
| F61 | Arrange appraisal access; answer a low appraisal with facts | both | Close | Partially automatable | Practical: access. Legal: information only, no pressure | Comps packet; reconsideration-request draft | [12 CFR 1026.42](https://www.consumerfinance.gov/rules-policy/regulations/1026/42/) [PRIMARY] |
| F62 | Follow up title, survey and municipal items (CO, permits, violations, liens) | both | Close | Partially automatable | Legal: clearing title is the seller's attorney's and title company's work | Track, request documents, flag delays | [NYSBA 5 Steps](https://nysba.org/?p=132946) [SECONDARY]; [NYSBA Columbia](https://nysba.org/wp-content/uploads/2020/02/Columbia-2.pdf) [PRIMARY-adjacent] |
| F63 | Coordinate all parties and keep everyone informed | both | Close | Fully automatable | DOS lets unlicensed staff assemble closing documents and get loan status reports | Shared timeline, status messages, document requests | [DOS assistants](https://dos.ny.gov/node/64166) [PRIMARY] |
| F64 | Keep the deal together when something goes wrong (extensions, renegotiation, reassurance) | both | Close | Human or licence required | Legal + practical: keeping parties "ready, willing and able … is the responsibility of the licensee"; renegotiation is negotiation; trust | Early-warning flags; options memo | [DOS 75-h syllabus](https://dos.ny.gov/real-estate-broker-75-hour-curriculum-eff-12212022) [PRIMARY] |
| F65 | Keep the seller informed of backup offers and new facts before closing | seller | Close | Partially automatable | Legal: full-disclosure duty | Log and forward every incoming offer; licensee advises | [RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443) [PRIMARY]; NAR 179 item 126 |
| F66 | Final walkthrough | buyer | Close | Partially automatable | Practical: access and presence (the buyer can do it with access); the salesperson course lists the pre-closing inspection with the purchaser as an agent role | Schedule; checklist; photo record | [Rand](https://jeselle.randrealty.com/?p=79) [SECONDARY]; [DOS 77-h syllabus](https://dos.ny.gov/real-estate-salesperson-77-hour-curriculum-eff-12212022) [PRIMARY] |
| F67 | Coordinate the closing (date, place, figures, commission statement, utilities, insurance) | both | Close | Partially automatable | Practical/legal: Hudson Valley closings are attorney-run; the lender's attorney disburses; the title company records | Checklists, figure checks, reminders | [NYSBA Columbia](https://nysba.org/wp-content/uploads/2020/02/Columbia-2.pdf) [PRIMARY-adjacent] |
| F68 | Collect the commission at closing; use the Commission Escrow Act if unpaid | brokerage | Close | Partially automatable | Legal: only a licensed broker can sue (§442-d); the affidavit must come from a licensed broker; six months to sue, and the seller can get the money released if nobody sues within 60 days (§294-b) | Compute; invoice; prepare the affidavit for the broker | [RPL §294-b](https://www.nysenate.gov/legislation/laws/RPP/294-B); [RPL §442-d](https://www.nysenate.gov/legislation/laws/RPP/442-D) [PRIMARY] |

### Stage 8: post-close

| ID | Function | Side | Stage | Classification | Why (legal rule or practical reason) | What the software can do | Source |
|---|---|---|---|---|---|---|---|
| F69 | Close the file; keep records three years (transaction, agency and fair-housing acknowledgments) | brokerage | Post | Fully automatable | 175.23; §443(3)(d); 175.28(d) | Tamper-evident archive, retention clock, export | [175.23](https://www.law.cornell.edu/regulations/new-york/19-NYCRR-175.23) [PRIMARY] |
| F70 | Pay out commissions and client rebates | brokerage | Post | Fully automatable | Legal gates: splits only to licensees (§442); salespersons paid only by their broker (§442-a); rebates to buyers or sellers allowed, but not for licensed work | Compute and check payees | [Booklet 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf) [PRIMARY] |
| F71 | After-sale service (warranty papers, document requests, repair disputes, moving referrals) | both | Post | Partially automatable | Practical: disputes need judgement | Document portal; dispute triage | NAR 179 items 173–179 |
| F72 | Ask for reviews and referrals; keep in touch | both | Post | Partially automatable | Practical: the relationship is personal. Legal: no after-the-fact referral fees (§442-l) | Automated asks and anniversaries | [Booklet 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf) [PRIMARY] |

### Stage 9: ongoing duties and compliance

| ID | Function | Side | Stage | Classification | Why (legal rule or practical reason) | What the software can do | Source |
|---|---|---|---|---|---|---|---|
| F73 | Hold the broker licence (or an entity licence with a representative broker); renew every two years | brokerage | Comply | Human or licence required | Legal: §440-a, §441; attorneys apply without course, exam or experience for $185 and are exempt from continuing education | Renewal calendar | [DOS broker page](https://dos.ny.gov/become-real-estate-broker) [PRIMARY]; [RealEstateU](https://realestateu.com/real-estate/guides/new-york-real-estate-broker-license) [SECONDARY] |
| F74 | Keep a definite New York place of business, outside sign, displayed licence, pocket card | brokerage | Comply | Human or licence required | Legal: §441-a | Reminders | [Booklet 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf) [PRIMARY] |
| F75 | Supervise licensees and control unlicensed staff and systems | brokerage | Comply | Human or licence required | Legal: "regular, frequent and consistent personal guidance …" (175.21); "training, supervision and control" of non-licensed services; revocation for "wholesale failure to supervise" (Malul 2025); policies and reminders were adequate (Metalios) | Approval queues, audit logs, policy attestations, sampling dashboards | [175.21](https://www.law.cornell.edu/regulations/new-york/19-NYCRR-175.21); [DOS assistants](https://dos.ny.gov/node/64166); [Malul](https://www.nycourts.gov/reporter/3dseries/2025/2025_06110.htm); [Metalios](https://docs.dos.ny.gov/ooah/decisions/Real_estate/2009/Metalios_Menalaos.htm) [PRIMARY] |
| F76 | Approve advertising; supervise websites while live | brokerage | Comply | Partially automatable | Legal: 175.25(b)(1), (d)(3) | Pre-check every ad; one-tap approval queue | [175.25](https://www.law.cornell.edu/regulations/new-york/19-NYCRR-175.25) [PRIMARY] |
| F77 | Institute, notarize, post and archive SOPs; affirm at renewal | brokerage | Comply | Partially automatable | Legal: §442-h(4) | Version control; website posting; 30-day change archive | [RPL §442-h](https://www.nysenate.gov/legislation/laws/RPP/442-H) [PRIMARY] |
| F78 | Run the fair-housing programme (policy, posters, homepage link, open-house display, training, monitoring) | brokerage | Comply | Partially automatable | Legal: 175.28–175.29; 175.17(b); 13 broker-course hours | Monitor copy and messages; training records | [Booklet 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf) [PRIMARY] |
| F79 | Administer an escrow account if the broker ever holds money | brokerage | Comply | Partially automatable | Legal: no commingling; three business days; accounting (175.1–175.2) | Ledger, reconciliation, alerts | [175.1](https://www.law.cornell.edu/regulations/new-york/19-NYCRR-175.1) [PRIMARY] |
| F80 | Check every payment against compensation rules | brokerage | Comply | Fully automatable | §442, §442-a, §442-l, 175.7 | Rule engine | [Booklet 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf) [PRIMARY] |
| F81 | Check solicitation lists and block blockbusting language | brokerage | Comply | Fully automatable | 175.17; §442-h(2)–(3) | List screening; copy filters | [Booklet 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf) [PRIMARY] |
| F82 | Disclose the broker's own interests (buying a listing, selling own property, affiliates) | brokerage | Comply | Human or licence required | Legal: 175.4–175.6; Dubbs ("lay bare the truth") | Related-party flags; disclosure drafts | [Booklet 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf); [Dubbs](https://www.law.cornell.edu/nyctap/I01_0072.htm) [PRIMARY] |
| F83 | Deal honestly with the other side; disclose known material facts | both | Comply | Partially automatable | Legal: duties to the non-client printed in the §443 form | Prompt the licensee with known defects before each message | [RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443) [PRIMARY] |
| F84 | Counsel the client and exercise fiduciary judgement day to day (confidentiality, obedience, "what should I do?") | both | Comply | Human or licence required | Legal + practical: the fiduciary is the licensed agent; trust | Prepare options and facts; enforce confidentiality walls | [RPL §443](https://www.nysenate.gov/legislation/laws/RPP/443); [Dubbs](https://www.law.cornell.edu/nyctap/I01_0072.htm) [PRIMARY] |
| F85 | Comply with MLS and association rules (fines, showing availability, Clear Cooperation) | brokerage | Comply | Partially automatable | Contractual (WS3) | Rule checks before entry | [LIBOR rule tips](https://www.lirealtor.com/brokers-agents/member-resources/customer-service-tips/onekey-mls-rules-compliance) [SECONDARY] |
| F86 | Onboard, train and sponsor licensees (contractor terms, association changes) | brokerage | Comply | Partially automatable | Legal: §442-b notices; broker-course onboarding hours; applies once licensees join | Training modules, records, DOS change filings | [DOS 75-h syllabus](https://dos.ny.gov/real-estate-broker-75-hour-curriculum-eff-12212022) [PRIMARY] |
| F87 | Keep agents and data safe (field safety, cyber security, personal data) | brokerage | Comply | Partially automatable | Broker course "Agent Safety and Supervision", including cyber security; personal-data law is WS2's | Check-ins, access control, encryption, logs | [DOS 75-h syllabus](https://dos.ny.gov/real-estate-broker-75-hour-curriculum-eff-12212022) [PRIMARY] |
| F88 | Carry insurance and manage business risk (errors and omissions, liability) | brokerage | Comply | Human or licence required | Practical: business judgement (broker course lists the cover) | Renewal reminders | [DOS 75-h syllabus](https://dos.ny.gov/real-estate-broker-75-hour-curriculum-eff-12212022) [PRIMARY] |
| F89 | Answer regulators and disputes; keep up with law changes | brokerage | Comply | Human or licence required | Legal: DOS may investigate and subpoena (§442-e(5)–(6)); personal accountability (§441-c) | Evidence packs from logs; law-change tracking | [Booklet 2026](https://dos.ny.gov/system/files/documents/2026/03/real-estate-license-law_03.2026.pdf) [PRIMARY] |

The national list is a useful completeness check. NAR's 179 items are all seller-side; on my reading of the item
texts, about 140 are data, document, scheduling, production or tracking steps, about 17 are advice or negotiation
acts New York reserves to the licensee, about 10 need someone on site, about 8 are done by attorneys or title
companies in the Hudson Valley, three do not apply in New York (a New Jersey records report, termite bonds,
township vacancy registration), and item 19 ("explain impact of schools on market value") is a fair-housing hazard
here ([NAR 179 Ways](https://www.nar.realtor/sites/default/files/documents/2023_179_ways_real_estate_pros_8.5x11_pages_final.pdf))
[PRIMARY list; tally INFERENCE]. Every item maps to one of F1 to F89; the inventory adds what the NAR list leaves out:
the buyer side, the firm's compliance duties and business development.

## Counts and the true bottleneck list

| Stage | Fully automatable | Partially automatable | Human or licence required | Total |
|---|---|---|---|---|
| Business development and client acquisition (F1–F7) | 0 | 6 | 1 | 7 |
| Listing intake and agreements, buyer engagement (F8–F20) | 6 | 5 | 2 | 13 |
| Pricing (F21–F25) | 2 | 3 | 0 | 5 |
| Marketing (F26–F34) | 2 | 7 | 0 | 9 |
| Showings and buyer search (F35–F43) | 3 | 4 | 2 | 9 |
| Offers and negotiation (F44–F51) | 2 | 2 | 4 | 8 |
| Contract to close (F52–F68) | 3 | 9 | 5 | 17 |
| Post-close (F69–F72) | 2 | 2 | 0 | 4 |
| Ongoing duties and compliance (F73–F89) | 2 | 8 | 7 | 17 |
| **All** | **22** | **46** | **21** | **89** |

By side, the 89 split into 22 seller, 12 buyer, 32 both and 23 brokerage functions. Of the 21 **Human or licence
required** functions, 15 rest on a legal rule alone, 4 on law and practicality together (F39, F40, F64, F84) and 2
on practicality alone (F4 trust, F88 business judgement); 3 are attorneys' work in the Hudson Valley (F52, F53,
F55) and the rest are the licensee's.

Not all 21 limit the business equally. Holding the licence and the office (F73, F74), self-interest disclosures
(F82), insurance (F88) and regulator response (F89) are occasional. These six are the true bottleneck, in order:

1. **Negotiating for the client (F48, with F47, F49, F58, F64).** Every deal, both sides, often more than once and
   against a deadline; only a licensee can do it, so it sets the floor on licensed hours per deal and is the main
   reason A1 is only partly met.
2. **Accompanied showings and open houses (F39, F40).** Per showing, in person, across a rural region; on the buyer
   side there is no lawful human-free substitute, which is why A6 is hit as worded. On the listing side the owner can
   show and host.
3. **Supervision and personal accountability (F75, with F12 accepting listings and F76 approving ads).** The broker's
   review capacity is the throughput ceiling of the whole firm; approving at a volume he cannot really review is how
   Malul lost his licences.
4. **Agency relationships and in-house conflicts (F11, F51).** "Replace both agents" makes every in-house sale dual
   agency with reduced duties; designated agents need two more licensees; competing buyers need disclosure and consent.
5. **Attorney work (F52, F53, F55).** A lawyer on each side remains the Hudson Valley norm, so the "lawyer out of the
   loop" pitch does not survive; software can shorten the attorneys' work but not remove it.
6. **Trust and referral (F4, F84).** The demand-side bottleneck: software can run the marketing and the follow-up, but
   the client chooses a person, and that person here is the attorney-founder (compare WS5's K5).

## Conclusion

The useful way to read the 89 functions is not "how much of the agent can software replace" but "what is the
smallest licensed core, and how cheaply can software surround it". The answer from New York's own rules is a core
of about eight recurring acts per deal (accept the client, explain the agency relationship, approve the copy,
advise on price, show or have a sponsored licensee show, advise on and negotiate every offer, negotiate inspection
results, keep the deal together), plus two attorneys the brokerage does not supply. Everything else, which is most of the hours in
the NAR list, is software-shaped and much of it already runs on software for agents today. That makes the venture's
real product a **licensee-in-the-loop brokerage system** whose demo shows each of those acts as a visible human
checkpoint with its legal reason, which is also the most credible story to put in front of a New York lawyer.

Two findings change the plan rather than just describe it. The buyer side is the human-heavy side (tours,
negotiation, competing-buyer conflicts), so a cheap buyer service needs either the broker's own hours or a licensed
showing agent the broker sponsors and pays; and the "replace both agents" pitch should become "one firm, two
clearly separated representations, with informed consent", or the firm should represent only one side of its own
listings. If the venture later moves up the Hudson to the Capital Region, the contract step flips from attorney-drafted
to broker-filled, and the escrow and fill-in rules come into play.

## Sources and method

Notes used: `research_notes/WS1 NY agent functions/licensing_curriculum_and_duties.md` and
`research_notes/WS1 NY agent functions/transaction_tasks_and_timeline.md`, each with its section "Gap fill
(2026-10-23, VPS session)". Other workstreams' notes were read for cross-checks only. In the gap fill, about 75
searches and fetches re-checked **34 load-bearing claims** (26 confirmed, 3 confirmed with refinements, 3 corrected,
2 not fully re-verified) and worked **15 gap themes** (12 closed, 3 narrowed). Corrections that matter: only one
cease-and-desist zone remains (Brooklyn, to 1 July 2028); the Commission Escrow Act gives the broker six months to sue
(the earlier "60 days" was the seller's release window); and NAR's 179-item list is public and was classified. Where
the notes and the gap fill disagree, the newer primary source is used here.

Important gaps still open: no DOS ruling on software or AI doing licensed work (a written inquiry to DOS Division of
Licensing Services would settle it); no sales-specific ruling that showings need a licence (the 1993 decision is a
rental); whether a §443(5) "non-agent" engagement works (untested); Governor action on A10679-B (public marketing) and
S8870 (broker experience), both passed in June 2026; current Hudson Valley closing customs (the bar sheets date from
2018–2020; the attorney-founder can confirm them); Columbia and Greene days-on-market for 2026; and a primary
2025–2026 days-to-close statistic.
