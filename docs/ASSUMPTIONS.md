# Riskiest assumptions, ranked, with kill criteria

Scores: **Fatal** = how much of the venture dies if the assumption is false (1 minor to 5 the whole idea).
**Uncertain** = how little we know today (1 near-certain to 5 no idea). Rank = Fatal x Uncertain.
"Tested by" names the research workstream (WS) or the real-world test that settles it. Status is updated
as findings land; kill criteria are stated so a bad finding is recognised, not rationalised.

| Rank | # | Assumption | Fatal | Uncertain | Tested by | Kill criterion (what would mean "stop" or "pivot") | Status |
|---|---|---|---|---|---|---|---|
| 1 | A3 | The "lawyer is out of the loop" pitch is lawful: software may generate and present the contract, and the attorney-founder can be the broker on the deal without becoming the parties' lawyer. | 5 | 4 | WS2 | NY unauthorised-practice rules or the attorney-review custom make a lawyer on each side unavoidable, and ethics rules bar the founder from being both broker and lawyer in one deal. Then the pitch becomes "a cheaper, faster lawyer step", not "no lawyer". | open |
| 2 | A5 | Hudson Valley sellers will list with a new, attorney-led, low-fee brokerage instead of a known local agent, because local trust and word of mouth carry. | 5 | 4 | WS5b, WS5c, then the first real listing | Evidence that low-fee listings are steered against or sell slower locally, plus surveys showing low acceptance of non-traditional agents, and no first customer signs within the pilot window. | open |
| 3 | A1 | One licensed human (the attorney-broker) supervising software is enough for every licensed act, at a scale that pays. | 5 | 3 | WS1, WS2 | NY law or Department of State practice requires a licensed person to personally perform core acts (negotiating, showing, presenting offers) in a way that needs an agent per deal anyway. | open |
| 4 | A6 | Buyers will use a software buyer's agent with no human agent for tours, negotiation and hand-holding. | 4 | 4 | WS1b, WS3b (lockbox and showing rules), WS5c | Showings and lockbox access legally or practically require a licensee, or early AI buyer-agent launches show buyers abandon the service at the touring step. | open |
| 5 | A4 | Listings reach Zillow, Realtor.com and Redfin through the MLS, and MLS entry can be automated or done in minutes by the one licensed human. | 4 | 3 | WS3 | No listing-input API exists, MLS rules forbid flat-fee or limited-service listings, or membership costs and rules make a one-broker shop unviable; then portal reach needs manual labour per listing, which caps scale but does not kill. | open |
| 6 | A2 | An unlicensed co-founder (Joe) may own equity in the brokerage and be paid from its revenue, or be paid as the software vendor. | 4 | 3 | WS2a | NY compensation-sharing rules forbid both unlicensed ownership and vendor fees tied to commissions with no workable structure. | open |
| 7 | A7 | The unit economics work: a flat or low fee covers broker time, marketing, customer acquisition and the cost of being wrong (liability, insurance). | 4 | 3 | WS4, WS5c | Customer-acquisition cost in the region exceeds the fee, or supervised broker hours per deal exceed what the fee pays for. | open |
| 8 | A10 | No well-funded flat-fee or AI player already owns the Hudson Valley. | 3 | 3 | WS5a, WS5b | A funded competitor with real local volume and the same attorney-adjacent trust story. | open |
| 9 | A8 | Model output (listing copy, messages, contract drafts) is good enough under human approval, and fair-housing risk is manageable with checks. | 3 | 2 | POC testing | Violation or error rate in the fixture tests too high to trust even with review. | open |
| 10 | A9 | The free pre-listing inspection helps the pitch more than it costs in liability and seller friction. | 2 | 4 | WS6 | Liability cannot be contained with a licensed inspector under contract with the seller, or buyers do not skip their own inspection anyway, so it is a pure cost. Dropping it does not hurt the core. | open |
| 11 | A11 | The existing VPS can host the demo and the session reliably despite being near its disk limit. | 1 | 3 | setup script, disk checks | Free space cannot be recovered or the plan upgraded. | open |

## How the order drives the work

- A3, A1 and A2 (law) are tested first, by workstream 2, because they decide where human steps live in
  the product. Workstreams 1 to 3 finish before the architecture is locked (Joe's sequencing rule).
- A5 and A6 (demand) cannot be fully settled by research; research gives the base rate, the first real
  listing settles it. The plan will say so.
- Findings land in the Status column with a date and a link to the deliverable. A hit on a kill criterion is
  reported plainly in `PROGRESS.md` and to Joe, not softened.
