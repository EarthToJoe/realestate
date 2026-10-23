# Software that replaces both real estate agents: the plan, and what stands in its way

*October 2026. Every number below comes from one of six research reports, an independent fact-check, or a memo on
your roles; the links go to the source. Research to plan with, not legal advice.*

## The idea

Software that completely replaces the real estate agent on both sides of a sale. For the seller it prices the
house, writes the listing and all the marketing, gets it onto the major sites, answers every enquiry, books
showings, compares offers and negotiates. For the buyer it searches, books tours, and drafts and negotiates the
offer. It drafts the contract, so the lawyer is out of the loop too, and it markets the business itself. A New York
seller pays about **4.6%** in total commission today; we would charge a fixed fee per side of well under 1%
([WS4](research/WS4-cost-model.md#what-the-seller-really-saves-a-third-unless-the-buyer-side-comes-too)). New York
first, starting in the Hudson Valley.

That is what I said I would build, and it is the plan. The research does not change it; it shows exactly what
stands in its way.

## Why it can work

- **Most of an agent's job is software work.** Of 89 things New York agents and their broker do, software can do 22
  alone and 46 mostly; 21 need a person. ([WS1](research/WS1-agent-functions.md#counts-and-the-true-bottleneck-list))
- **The AI is cheap:** $2 to $15 a side. ([WS4](research/WS4-cost-model.md#the-verdict-in-three-numbers-fee-cost-of-a-customer-broker-hours))
- **One MLS membership reaches every portal.** OneKey MLS feeds Zillow, Realtor.com, Redfin and Homes.com free,
  costs about $3,821 in year one, and may not refuse a broker for offering less service. ([WS3](research/WS3-listing-data-access.md))
- **The field is open here.** No online, discount or AI brokerage has an office in the eight counties, and nobody
  here does both sides with software. ([WS5](research/WS5-competitors.md#in-the-eight-counties-low-fee-rivals-are-remote-small-or-human))
- **People already try it alone.** In May 2026 a New York Times technology writer sold his Hudson Valley house for
  just over $600,000 with Google's Gemini, reckoned he kept about $90,000, and said the AI gave advice he had to
  catch. We do that properly, and checked. ([WS5](research/WS5-competitors.md#seller-side-ai-and-buyer-side-ai-both-exist-nobody-does-both-here))
- **Sellers choose people.** 66% picked an agent who was referred or used before; 4% said commission mattered most.
  A known local attorney behind it is trust no funded competitor can buy. ([WS5](research/WS5-competitors.md#can-a-locally-connected-launch-win-a-small-niche-yes-the-briefs-version-no))

## The hurdles, plainly

For each: what New York requires today, the least a person must do, and what would have to change.

1. **A broker's licence for every core act.** Listing, marketing for a fee, presenting offers and negotiating "for
   another" are a broker's acts, whoever or whatever does them. One unlicensed act is a misdemeanour, the firm
   cannot sue for its fee, and a consumer can recover up to four times the fee (RPL 440, 442-d, 442-e). What
   software does is the act of the broker who runs it, and his decisions must be real: in 2025 an appeals court
   upheld revoking a broker's licences for "wholesale failure to supervise". **The least:** a licensed broker who
   decides each listing, ad, offer and negotiating position, which the software prepares and carries out; about
   **20 broker hours a side at launch, 10.5 to 12.75 later** (Redfin's record implies about 70). **To go further:** a
   Department of State (DOS) ruling or a statute letting software act under supervision; we ask DOS in writing.
   ([WS2 §1](research/WS2-legal-licensing.md#1-a-licensed-broker-is-required-for-every-core-agent-act-and-software-cannot-hold-the-licence),
   [WS4](research/WS4-cost-model.md#humans-in-every-deal-1020-broker-hours-a-side-if-the-software-works-far-more-if-it-does-not))
2. **The contract is a lawyer's work.** Drafting a contract for another is practising law, and no company may do it
   or be paid for it (Judiciary Law 478, 484, 495). A broker may only fill in the non-legal blanks of an approved
   form, or make the whole paper subject to each party's attorney's approval, for no separate fee, and may never
   discourage anyone from using a lawyer (AG Op. 96-F11; DOS LI04). Free advice is still advice (*Upsolve v. James*,
   2d Cir. 2025). The seller's attorney drafts in all nine Hudson Valley counties by custom. **The least:** the three
   routes below. **To go further:** written ethics advice, or a New York safe harbour for self-help software like
   North Carolina's; none is proposed. ([WS2 §2](research/WS2-legal-licensing.md#2-the-software-may-fill-in-an-offer-only-lawyers-may-draft-or-explain-the-contract))
3. **A person enters every listing on the MLS.** No MLS or portal here takes listings from software. The software
   prepares and checks the listing; a person keys it in (20 to 45 broker minutes). The MLS also requires REALTOR
   membership (about $706 in year one). ([WS3](research/WS3-listing-data-access.md#no-write-api-a-person-submits-each-listing))
4. **Buyer tours, and buyers' own agents.** On the best New York authority a licensed person opens the door on buyer
   tours, and lockbox keys cannot be lent. 88% of buyers use an agent, and listings that pay buyers' agents less sell worse. So the seller
   saves a third of today's commission when the buyer brings an agent, two thirds when we act for both sides. **The
   least:** a licensed showing agent per buyer tour ($45 to $400); owners show their own homes. **To go further:** a
   DOS answer on unaccompanied tours. ([WS4](research/WS4-cost-model.md#what-the-seller-really-saves-a-third-unless-the-buyer-side-comes-too))
5. **We cannot afford to buy customers.** A client won through search or Zillow ads costs $2,780 to $8,120.
   Purplebricks spent about $15,000 per listing it won and left the US in 2019. The software markets the firm
   almost free; referrals must carry it. ([WS4](research/WS4-cost-model.md#kill-criteria-where-the-numbers-land))
6. **Your ten years away, the office, insurance.** 42.5% of owner households in the eight counties moved in since
   2010. The firm needs a physical New York office with a sign; the no-exam licence needs your bar registration
   current; the firm buys its own E&O insurance (about $708 a year), as your malpractice policy will almost certainly
   not cover brokerage claims. ([memo](research/memo-father-in-law.md#running-a-new-york-brokerage-from-out-of-state))

**The kill tests, named.** Four failed: the lawyer out of the loop, a buyer's agent with no human, the free
inspection as pitched, and "pitched as autonomous". Five partly failed: broker hours, MLS automation, local trust,
unit economics, the buyer-agent fee. I keep the idea and carry each as a hurdle. ([assumptions](ASSUMPTIONS.md))

## How we launch it

- **The software is the agent; the firm running it is licensed.** The law says whoever runs a fee-earning agent
  service must be a licensed broker, so the company is a licensed brokerage with you as broker of record: **$185, no
  course, experience or exam** for an admitted attorney. You do only the acts the law requires of you; the software
  prepares each one, carries it out once you decide, and logs it. I build and own the software, and can own equity
  and license it to the firm for a fixed fee, but cannot be paid per deal. ([WS2 §8](research/WS2-legal-licensing.md#8-joe-can-own-and-build-but-cannot-be-paid-per-deal))
- **The contract: three routes that exist today** ([detail](PLAN.md#the-contract-route-what-new-york-allows-today)):
  - *The firm's paper, subject to attorney approval.* The software drafts the full contract, for no separate fee,
    subject to each party's attorney's approval; the lawyers approve instead of drafting. Albany already works this
    way; here it cuts against custom.
  - *You as the seller's lawyer, using the software.* Allowed only if the brokerage fee is fixed, non-refundable and
    not contingent on closing, with written consent, billed by your own law practice (NYSBA Ops. 1015, 1117).
    Advisory: written ethics advice first.
  - *The parties as their own drafters.* No law makes anyone hire a lawyer, and the Court of Appeals did not treat a
    do-it-yourself legal book as practising law (*Dacey*, 1967). But no New York court has ruled on software that
    tailors a contract to one person, and a firm paid on the deal invites the rule against companies preparing
    real-estate papers. Untested.
  - *Provisional:* the first route always, the second where you choose, the third only after an ethics opinion.

## Competitors

About 70 reviewed. The idea is in motion, but split in half, and each half went back to humans. **LocQube** (Bronx,
$899 AI-written listing or 1.99% with an agent) serves sellers only; **Homa** (AI buyer brokerage, 1%, three states)
raised $5 million this month; **Ridley** sells AI listings in three Sun Belt states. None does both sides, drafts New
York's contract or is attorney-led here. Locally the cheapest full option is Redfin at 2% ($6,000 minimum). The window
is probably a year or two. ([WS5](research/WS5-competitors.md))

## The money

WS4's working fees: **$4,500 for the seller side** (0.88% of a $510,000 house) and **$3,500 for the buyer side**
(0.69%). ([WS4](research/WS4-cost-model.md))

| On a $510,000 house | Seller pays | Saving vs today's $23,562 |
|---|---|---|
| We list; buyer has their own agent | $15,771 | $7,791 (33%) |
| We act for both sides | $8,000 | $15,562 (66%) |
| We list; buyer has no agent | $4,500 | $19,062 (81%) |

| | Lean | Realistic |
|---|---|---|
| One-time cash to open | about $2,500 | up to about $20,300 |
| Year-one fixed cost | $8,236 | $62,575 |
| Cost per closed seller side | $351 | $1,902 |
| Break-even at $4,500 a seller side | 2 closings | 25 closings |
| Founder cash before the first fee | under $10,000 | about $31,000 to $40,000 |

These cases assume 8 to 15 broker hours a side; fewer would cut costs, but only the pilot can measure it. The
software is my own investment. A "free inspection, bought leads" version **never breaks even** at a flat fee.

## Your role

Broker of record, doing the acts the law requires and nothing the software can do for you; optionally the seller's
lawyer on fixed-fee deals; and the trusted name. Being either party's lawyer where the firm's fee depends on closing
is barred, and no consent cures it. ([memo](research/memo-father-in-law.md))

## The free inspection: your idea, evaluated

**Buyers will still hire their own inspector** (England dropped seller packs when fewer than one buyer in six
trusted them), so nobody saves a second one. A full upstate package costs **$550 to $2,250 per listing**, sold or not,
and turns the seller's "unknown" into "known", which they must disclose. Your friend needs a New York licence and must
work for the seller at his normal price; a free favour is what federal anti-kickback law forbids. **Recommendation
(provisional):** a capped pilot on the first ten listings (about $10,000), the seller as the inspector's client: "you'll
know what a buyer's inspector will find before they do". ([WS6](research/WS6-free-inspection.md#three-designs-one-recommendation))

## What the demo shows

One sale of a real Dutchess County house, 146 Rt 292 in Holmes, in 12 to 15 minutes; not for sale, and every screen
says so; the people are fictional. The AI does every agent act on both sides, through to negotiating and drafting the
contract; the seller and buyer make their own decisions. Wherever New York law today requires a licensed person or a
lawyer, a red **"NY law today"** marker names the rule and links the finding. Watch the fair-housing checker
catch a planted phrase, and the timeline coloured AI, client or "NY law today". MLS, portals, messages and signatures
are simulated. ([plan](PLAN.md#what-the-demo-shows-versus-what-is-real))

## Next three steps

1. **By 2026-11-06:** you list ten people who might sell in the next year, and call them by about 2026-12-15. If
   fewer than three would list, we rethink how the firm finds customers before I build past the demo.
2. **By 2026-11-13:** you check your bar registration (attorney search, or 212-428-2800), tell me where you live and
   where an office could be, and give me your view on the contract routes. I draft one written question to DOS and
   one to an ethics adviser for you, and phone the MLS.
3. **By 2026-12-31:** go or no-go. A go means forming the firm from January 2027 (8 to 12 weeks, about $2,500 lean),
   first listings in spring 2027.

Each hurdle in detail: [PLAN.md](PLAN.md).

Joe
