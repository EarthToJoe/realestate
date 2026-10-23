# Joe's brief (verbatim, 2026-10-23)

This is the source of truth for the project. Later decisions are in `DECISIONS.md`; questions and Joe's
answers are in `QUESTIONS-FOR-JOE.md`. Nothing here is edited; if Joe changes his mind, the change goes in
those files with a date.

---

# New project: AI Real Estate Agent — proof of concept + research plan

## Background
My father-in-law is a lawyer in New York. In NY, being a lawyer automatically makes you eligible to act as a real estate agent, and he has been registered as one. Earlier in his life he started a real estate business in the Hudson Valley (something like "Hudson Valley Partners" or "Hudson Valley Real Estate") that fizzled out, so he knows the business from the inside. He is ambitious and very well connected in that region. I am not well connected, so having him behind this adds a lot of value, and I want to invest heavily in making this as strong as possible.

## The idea
Software that completely replaces the real estate agent — not just the seller's agent, but the buyer's agent too. Agents typically take 2.5–3% of the sale price on each side; this undercuts that. The software should also cut out the other middlemen: it drafts the contract, so the lawyer is out of the loop as well. A licensed broker may still be legally required, and that should be treated as an open question to answer, not an assumption. The pitch is a dramatically cheaper home-selling and home-buying experience. Starting market: New York state.

The software must do everything a real estate agent does: listing on the major websites, complete marketing of the property, all buyer-side and seller-side communications, and marketing of the business itself to attract customers.

Add-on idea from my father-in-law: offer a free, comprehensive upfront home inspection (he has a friend upstate who could do it) before listing. The seller gets the chance to fix everything first, the buyer may not feel the need to pay for their own inspection, and the seller doesn't pay for a second one. My reservation: not every seller will want to make all the fixes. Evaluate this honestly, including liability.

First customer: he says this will be no problem because he knows everybody up there. Don't build the plan around a specific county; keep it New York state with a Hudson Valley starting point.

## What I need out of this
Two things, equally important:
1. A proof of concept that shows him I can actually build this.
2. A well-researched plan that shows the real hurdles — where an AI agent can't act alone and a human or license is required — so he sees this is sober and credible, not just hype. I want him to look at it and think this is promising and impressive and want to move forward.

I am almost certain this idea has been conceived before and is probably in motion somewhere. Competitor research is a personal priority for me — be rigorous and don't soften it.

## Demo-ability is a core design requirement
I will be showing this software off in person. Every feature must be explainable and walk-through-able: easy to see, easy to understand, and visibly impressive to a non-technical audience. Prioritize a clear visual interface over clever backend work. Each stage of the process (intake, listing generation, marketing, communications, contract drafting, human-approval checkpoints) should be its own visible step that I can click through and narrate. Nothing should happen invisibly — if the AI does something, show it doing it. Build a guided demo mode or walkthrough script I can follow when presenting.

## Infrastructure
- Set this project up as its own Claude Code session running on my Hostinger VPS so it runs continuously and I can reach it from any device, not tied to my phone or laptop. Reuse the existing VPS address and access credentials that other Claude Code sessions already use.
- Heads up: the VPS is close to its disk limit. Do not constrain the quality or depth of your work because of this. Check free space at the start, monitor it as you go, and warn me well before it becomes a problem so I can upgrade the plan or free up space from other projects. Never let the session get stuck by running out of disk.
- Use my $200 Anthropic API credit (expires Nov 8) before my Max subscription usage. Do not conserve tokens. Thoroughness over cost — I am willing to spend whatever it takes to make this plan sound and the proof of concept impressive.
- Initialize a git repository on day one. Commit with meaningful messages at every milestone so nothing is lost if the VPS hiccups.
- Track API spend per workstream in a running log so I can see where the credit went.

## Working practices
- **Success criteria first.** Before building anything, write down what "POC done" looks like — specific, checkable outcomes — and get my sign-off. Build to that finish line.
- **Riskiest assumptions first.** List the assumptions this venture depends on (e.g. "a licensed broker isn't required for every step," "MLS listing can be automated," "sellers will accept a flat fee over a known local agent"). Rank them by how fatal and how uncertain each is, and test the top ones first. Define kill criteria: which findings would mean this isn't worth pursuing. Report those plainly if you hit them.
- **Requirements traceability.** Every feature in the POC must trace back to a specific agent function from workstream 1 and respect a specific legal constraint from workstream 2. Maintain a traceability matrix. This is what makes the demo narrative airtight.
- **Decision log.** Keep a running log of every architecture and scope decision with the reasoning behind it, so I can explain choices to my father-in-law and future sessions don't relitigate them.
- **Async reporting.** This runs unattended. Write a daily progress summary to a fixed file, and maintain a running "questions for Joe" file that I answer when I check in. Never block indefinitely on a question — note it, make a reasonable provisional choice, flag it, and keep moving.
- **Explicit out-of-scope list.** Write down what the POC will not do. Don't gold-plate.
- **Fair housing and PII guardrails.** AI-generated listing and marketing copy can violate fair housing law (protected-class language, steering, discriminatory targeting). Build explicit checks into the copy-generation pipeline. The system will also handle buyer and seller personal data — treat PII handling, storage, and access as a first-class design concern, not an afterthought.

## Sequencing
Run research workstreams 1–3 before locking in the software architecture. The legal, licensing, and listing-access findings determine where human-approval steps must live in the product, and I don't want to build on wrong assumptions. Workstreams 4–6 can run in parallel with early build work.

## Workstreams (produce a written deliverable for each)
1. Agent function inventory: start by figuring out everything a NY buyer's and seller's agent actually does. Pull from the NY licensing course curricula (what classes they take, what they're trained on), broker duties, fiduciary expectations, and typical transaction timelines. Mark each function as fully automatable, partially automatable, or requires a human/licensed person.
2. Legal and licensing hurdles in NY: broker requirement, who may legally draft and present contracts, attorney-review customs in NY transactions, fair housing compliance, disclosure obligations, e-signature validity, and what a lawyer-licensee like my father-in-law is and isn't permitted to do.
3. Listing and data access: can software list a property on Zillow, Redfin, Realtor.com, and the regional MLSs (e.g. OneKey MLS, Hudson Valley MLS)? Is there an API, or does a human have to click through manually? What memberships or subscriptions are required and what do they cost?
4. Cost model: what it costs to get our foot in the door (upfront), what the ongoing subscription and service costs are, and what human interaction is required at launch versus ongoing.
5. Competitor research: a rigorous list of companies already doing AI-driven or flat-fee agent replacement on the buyer side, seller side, or both. What they charge, where they operate, how far along they are, and where they fall short. Include discount brokerages and any startups in stealth or early stage. Important framing: competitors existing is not disqualifying. Even if this concept is already in motion nationally, assess whether a locally connected launch in the Hudson Valley can win as a niche play — relationship-driven markets, trust in a known local lawyer, and word of mouth may matter more than product parity there. Identify which competitors actually operate in the Hudson Valley today and how entrenched they are.
6. Free upfront inspection offering: evaluate the pros, cons, liability exposure, and whether buyers would actually skip their own inspection. Note my seller-reluctance concern.
7. Proof of concept: this is the first real slice of the product, not a throwaway demo. Build it on a modular architecture that the full product can grow from. Start with the parts that will survive regardless of what the research finds: property intake, listing and marketing copy generation, buyer and seller communication drafting, and NY-compliant draft contract generation. Stub the Zillow, MLS, and portal integrations with explicit "human required here" markers until workstream 3 confirms what's possible, then wire up whatever can be automated. Every step where a human or a license is still required should be visible in the demo itself so it illustrates the hurdles. Apply the demo-ability requirement and the working practices above throughout.

## Output
- A single executive summary I can hand to my father-in-law.
- A project plan with phases, costs, open questions, and the human-in-the-loop map.
- A presentation walkthrough script for the proof of concept.
- The success criteria, riskiest-assumptions ranking with kill criteria, traceability matrix, decision log, and out-of-scope list as living documents in the repo.
- Ask me clarifying questions before starting anything that depends on my decisions.
