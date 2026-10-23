# WS4 handoff: cost model (2026-10-23)

Deliverable: [`docs/research/WS4-cost-model.md`](../WS4-cost-model.md).
Notes: `research_notes/WS4 Cost model/costs_and_revenue_benchmarks.md`. The new material is in the section "Gap fill (2026-10-23, VPS session)".

## 1. Assumption status lines

The links point to sections of the deliverable, named in brackets.

- A7 | partly hit / still open | Fixed costs are small ($8,236 lean, $62,575 realistic) and referral-sourced closings clear them (2 or 25 closings at $4,500). But paid acquisition ($2,780–$8,120 per client) exceeds the contribution, and the full build-out never breaks even at flat fees. | [WS4-cost-model.md → "Kill criteria: where the numbers land"](../WS4-cost-model.md#kill-criteria-where-the-numbers-land)
- A1 | still open | One broker can carry about 40 closings a year in about 600 hours only if steady-state broker time is about 15 hours or less per side; the only measured analogue (Redfin, about 28 sides per lead agent in 2024) implies about 70. | [→ "Humans in every deal"](../WS4-cost-model.md)
- A9 | partly hit | A free comprehensive inspection costs $900–$1,800 per listing, paid whether or not the house sells, and is the main reason the full build-out loses money on every closing. | [→ "Kill criteria" and "Running costs"](../WS4-cost-model.md)
- A4 | dodged (cost side) | OneKey costs $3,636 in year one, ShowingTime is included, and SentriLock is optional ($130/yr + $110 per box). But OneKey's rule covers only 5 of the 8 counties; the Ulster/Columbia/Greene MLS fees are unpublished. | [→ "Getting in the door"](../WS4-cost-model.md)
- A5 | still open | The cost model cannot settle demand; it shows the firm cannot afford to buy listings, so A5 must be met by referrals. | [→ "The verdict in three numbers"](../WS4-cost-model.md)
- A3 | partly hit (cost side) | Customers still pay two closing attorneys ($995–$2,500 each), and the brokerage may not charge for documents, so "AI drafts the contract" produces no fee and no lawyer saving. | [→ "What the seller really saves"](../WS4-cost-model.md)
- A2 | still open (cost side) | The model treats the software as a fixed-fee vendor cost, not per deal, per WS2. Joe's build time is uncosted; at the local developer median ($145,830/yr) it would be the largest single cost. | [→ "Kill criteria" (K7)](../WS4-cost-model.md)
- A6 | still open | Buyer touring is the largest licensed time block: 7–10.5 broker hours per buyer, or about $350 through a licensed showing agent. | [→ "Humans in every deal"](../WS4-cost-model.md)
- A8 | dodged (cost side) | AI costs $2.35–$15 per side (worst case about $72), immaterial to the go/no-go. Quality and fair-housing risk are not cost questions. | [→ "AI costs less per deal than the yard sign"](../WS4-cost-model.md)

## 2. Kill criteria

- **K1** | partly hit (pitch) / dodged (firm margin) |
  - The firm's margin does not need unrepresented buyers.
  - The seller's saving does. With a buyer's agent at 2.21%, the seller saves 33% of the 4.62% NY average ($7,791 at $510,000).
  - The seller saves 66–81% only if the firm also takes the buyer side or the buyer is unrepresented.
- **K2** | hit if paid acquisition is needed |
  - Agent and broker search leads cost $157.59–$162.39 each (LocaliQ, Apr 2025–Mar 2026). At 2–5% conversion that is $3,150–$8,120 per client.
  - Zillow outside major metros costs $139 per connection, or $2,780–$6,950 per client.
  - Contribution before acquisition at $4,500 is only $2,600–$4,150.
- **K3** | shapes the fee design |
  - A fee contingent on closing bars the father-in-law from being counsel on that deal.
  - Only a fixed, prepaid, non-refundable broker fee (Op. 1015) could allow both roles.
  - The model assumes he is never counsel on brokerage deals (Q4 provisional).
- **K4** | not a cost criterion | The model costs every licensed act as a human checkpoint, consistent with "licensee in the loop".
- **K5** | open; must be measured | Intake must record where each customer came from (traceability WS4-C3).
- **K6** | open; cost effect quantified | Slow or unsold listings raise the per-listing costs carried by each closing by 25–33% (the model assumes 20–25% of listings do not sell in the realistic and full cases). This must be measured against OneKey comparables.
- **K7** | dodged (lean) / open (realistic) / hit (full build-out) |
  - Founder cash needed before the first fee (5–8 months in): under $10,000 lean; about $31,000–$40,000 realistic; open-ended at flat fees in the full build-out.
  - The software build, if bought, is the real capital item.
  - Macro risk: mortgage rate 7.03% and a Fed rise on 16 Sep 2026.
- **K8** | not applicable to WS4.
- **K9** | dodged on cost | MLS membership is affordable. Coverage is the issue (5 of 8 counties by OneKey rule).
- **Assumption kill criterion A7** ("CAC exceeds the fee, or broker hours per deal exceed what the fee pays") | hit for paid acquisition; open for broker hours |
  - At $66.65/h, Redfin-like hours (about 70/side) cost about $4,700, more than a $4,500 fee.
  - At 15 h/side they cost about $1,000.

## 3. Questions for Joe (and his father-in-law)

1. **Fee model.**
   - Provisional: a flat **$4,500 seller-side fee** with à-la-carte add-ons, and a **$3,500 buyer-side fee** with any surplus seller-offered compensation rebated to the buyer.
   - No document fee, ever.
   - Unblocks: the POC's fee and savings calculator, and the plan's revenue line.
2. **Free inspection.**
   - Provisional: offered as a seller-paid or at-cost option, with a free pilot on at most 5 listings to measure renegotiation and fall-through.
   - Unblocks: the inspection screen's pricing and the full-build-out budget.
3. **Father-in-law's hours.** How many hours a week can he give as broker of record?
   - Provisional: 10–15 hours/week, which caps the firm at about 35–50 closings a year at 15 hours a side.
   - Unblocks: the capacity plan and the hiring trigger.
4. **Launch counties.**
   - Provisional: the five OneKey counties (Dutchess, Orange, Putnam, Rockland, Sullivan) at launch. Call HVCRR (845-338-5299) for fees before adding Ulster, Columbia and Greene.
   - Unblocks: MLS budget and the demo's county list.
5. **Office.**
   - Provisional: a DOS-licensed home office or a small separate office, not his law office. NYSBA Op. 1015 fn. 5 favours a separate office, name and staff.
   - Unblocks: the office line ($0 vs $5,500–$13,200 a year).
6. **Coordinator.**
   - Provisional: Joe and the software do coordination until about 15 closings, then a part-time hire (about $24,000/yr including employer costs).
   - Unblocks: the realistic-case budget.
7. **Paid marketing.**
   - Provisional: referral-only for the first 12 months, brand budget at most $1,000/month, no per-lead buying.
   - Unblocks: the K2 guardrail in the plan.
8. **His malpractice carrier.** Will he ask his carrier, in writing, whether its business-enterprise exclusion would deny cover for claims connected with a brokerage he owns, and whether such claims could affect his law firm's cover?
   - Provisional: assume no cover. The brokerage buys its own E&O ($708–$1,500/yr).
   - Unblocks: the insurance line and his personal risk decision.
9. **Software investment.** Is Joe's build treated as his own risk capital, not repaid from the brokerage's first-years fees?
   - Provisional: yes.
   - Unblocks: how the plan presents K7.

## 4. Traceability items (cost lines that drive POC features)

- **WS4-C1 Cost-per-deal tracker.**
  - Every deal shows the firm's own costs next to the fee and the resulting contribution.
  - Costs shown: media, inspection pass-through, e-sign envelopes, SMS segments, AI tokens and dollars at current list prices, showing-agent fees.
  - Visible on the deal screen and in demo mode.
- **WS4-C2 Broker and coordinator time log.**
  - Every human checkpoint (licensed act) records broker minutes.
  - Clerical steps record coordinator minutes.
  - A running total per deal is compared with the targets: 10.5 h seller side and 12.75 h buyer side steady state; 20 h at launch.
- **WS4-C3 Customer-source capture at intake.** Options: referral, past client, attorney network, paid ad, portal, other. A dashboard shows the share from paid sources and cost per client (K2/K5 monitor).
- **WS4-C4 Honest savings calculator.**
  - Shows the seller's saving in three cases: buyer with own agent (default, about 33%), firm on both sides, unrepresented buyer.
  - Uses 4.62% (NY 2026 average) with 5–6% as the "traditional" alternative.
  - Always shows that attorney fees and transfer tax remain.
- **WS4-C5 Fee configuration with an ethics flag.**
  - Fee types: flat, percentage with minimum, or à la carte. No document-fee line.
  - Each fee is marked contingent or prepaid-non-refundable. A contingent fee blocks the "attorney is also counsel" option at a checkpoint (K3).
- **WS4-C6 Inspection as an optional, costed add-on.** Shows the firm's cost if offered free.
- **WS4-C7 AI spend per module per deal.** Already in DECISIONS #8. Compare the actual figure with the $2–$15 per side estimate.
- **WS4-C8 Listing outcome log.** Sold, expired or withdrawn, with days to contract, compared with OneKey county figures. This measures the unsold-listing gross-up and K6.

## 5. Key numbers for the plan and the executive summary

All are as of 2026-10-23 and sourced in the deliverable.

**Opening and running the firm:**

- **Licence:** the attorney's broker licence is **$185 per two years**, with no course, no experience and no exam (DOS form DOS-0036-f-a). One licence covers a one-broker LLC.
- **Year-one fixed cost:**
  - **$8,236** lean: home office, unpaid owner-broker, OneKey only, no paid ads.
  - **$62,575** realistic: part-time coordinator, small office, outside legal review, $1,000/month marketing, MLS-fed site.
  - **$140,836** full build-out.
- **Year-two fixed cost:** about $6,500 / $56,000 / $127,000.
- **Upfront one-time cash:** about **$2,500** (lean) to about **$20,300** (with $15,000 of outside counsel).
- **MLS:** $3,636 in year one (HGAR $706 + OneKey $650 + 12 × $190). It covers **5 of 8** target counties by OneKey's rule.
- **Insurance:** E&O median **$708/yr**, required in practice. The lawyer's malpractice policy likely will not cover brokerage claims (*Admiral v. Adges*, S.D.N.Y. 2012; *Lee & Amtzis*, App. Div. 2015).

**Per deal:**

- **Variable cost per closed seller side:** **$351** lean / **$1,902** realistic / **$7,471** full build-out (with free inspection, premium media, Zillow Showcase, paid leads).
- **Break-even at a $4,500 flat fee:** **2** closings (lean), **25** (realistic), **never** (full build-out). With the broker's time valued at $66.65/h, the realistic case needs 40.
- **AI cost:** **$2.35–$4.70 per side** at base budget; about **$15** heavy; about **$72** worst case.
- **Paid customer cost:** **$2,780–$8,120 per client**, against contribution of $2,600–$4,150. Redfin spent about **$1,864 of marketing per transaction** in 2024.

**People:**

- **Broker hours (assumed):** about **20 per side at launch, 10.5–12.75 steady**. Unlicensed help 2–9 hours. Benchmarks: Redfin about **28 sides per lead agent per year** (2024); a typical Realtor **9 sides** (2025).
- **Father-in-law's launch time:** about **80–125 hours**, mostly legal set-up. Calendar about 8–12 weeks.

**The pitch:**

- **Seller saving at $510,000:**
  - **$7,791 (33%)** if the buyer has an agent.
  - **$15,562 (66%)** if the firm takes both sides.
  - **$19,062 (81%)** if the buyer is unrepresented.
- **Market base:** NY average commission **4.62%** (2.41% + 2.21%; Clever, Aug 2026, 434 agents). Q3-2026 medians: Dutchess $547,700, Orange $510,000, Rockland $800,000, Sullivan $371,000.

## 6. Open gaps that still matter, and what would close them

- **HVCRMLS (Ulster, Columbia, Greene) dues and MLS fees.** One phone call to HVCRR, 845-338-5299.
- **Insurance quotes (E&O, BOP, cyber).** Apply through CRES, Hiscox or Insureon once the LLC exists.
- **The father-in-law's malpractice carrier's position.** Written inquiry to his carrier or broker.
- **Real broker and coordinator hours per side.** Log them on the first 10–20 deals (WS4-C2). No study exists.
- **Local cost per customer and lead conversion.** Track source and spend from day one (WS4-C3). A small, capped search-ad test (for example $1,000) would give a local cost-per-lead figure.
- **Outside legal review price and the NYSBA contract-form licence.** Get a quote from a Hudson Valley real estate or ethics lawyer and ask NYSBA (overlaps WS2).
- **OneKey unlicensed-assistant MLS access and SentriLock lease term.** Call HGAR Member Success, 914-681-0833.
- **Lender treatment of buyer rebates.** Not researched; matters for the buyer-side fee model. WS2 or a lender call.

## 7. Contradictions with other workstreams' notes (and with WS4's own earlier notes)

- **OneKey county coverage.** HGAR's subscription page lists Ulster. OneKey Rule 201 (ver. 2026C, read by WS3) does not. WS4's earlier notes said "six of eight". The newer rule text wins: five of eight.
- **Broker licence count.** WS4's earlier notes inferred $370 (entity plus member). RPL §441-b and the DOS form give $185 for a one-broker LLC, consistent with WS2.
- **Comparison commission.** WS4's earlier notes used "customary 5–6%" (Hudson River Realtors, secondary). WS5 and the gap fill use 4.62% (Clever, Aug 2026). The deliverable uses 4.62% and shows 5–6% as the traditional figure.
- **Inspection cost.** WS4's earlier notes: $550–$700 (village) to $1,100–$2,000 (rural). WS6: $900–$1,800 central, up to $2,500. The deliverable uses WS6's range, the more detailed workstream on this point.
- **MLS hearing fines.** WS1 (S7) cites LIBOR's 2023 tip: up to $5,000 first and $15,000 subsequent. WS3 reads OneKey Rules 2026C: a single cap of $15,000. Use WS3.
- **OneKey branch and agent fees.** These conflict on two live 2026 pages: HGAR says $450 per branch and $225 per agent; OneKey says $650 per branch and $200 per agent (noted by both WS3 and WS4).
- **Redfin's listing fee.** WS5 (why-attempts notes) describes 1.5% standard. The gap fill finds a competitor's August 2026 claim of 2.0% billed with a $6,000 NY minimum. Both are secondary or claimed; Redfin's own page shows no figures.
- **Gap closed for WS2.** WS2 listed "malpractice-insurer underwriting of lawyers who also broker" as unresearched. The WS4 gap fill found NY authority (*Admiral v. Adges*; *Lee & Amtzis*) that business-enterprise exclusions are enforced.
