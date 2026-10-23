# Job: rewrite the executive summary, plan, assumptions and questions around the original idea (decision 21)

Date 2026-10-23. Tag RESPEC-B. Budget cap $10. You are one of two jobs running at the same time; the other
revises the architecture spec and traceability. Touch only the files listed under "Write".

## Why

Joe, this morning: "Keep the original idea, that is what I said I would build. I can pare it back on the future if
need be. The idea is the idea. Completely replace the real estate agents." Read `docs/DECISIONS.md` decisions 21
and 22, `docs/BRIEF.md` (all of it: "The idea" and "What I need out of this" set the bar) and
`docs/SUCCESS-CRITERIA.md` (amended this morning).

The overnight `docs/EXECUTIVE-SUMMARY.md` and `docs/PLAN.md` replaced Joe's idea with a different business ("a
licensed Hudson Valley brokerage with you as broker of record ... software does the file work ... each side keeps an
independent lawyer ... seller-first at a flat fee"), and opened with "the research says New York does not allow
that". Joe rejects that framing. The executive summary goes from Joe to his father-in-law, a New York lawyer who
knows the business; the brief wants him to find it "sober and credible, not just hype" and "promising and
impressive".

## The framing to write

- **The idea is the brief's idea**: software that completely replaces the seller's agent and the buyer's agent,
  does everything an agent does (listing, all marketing, all communications on both sides, marketing the business),
  and drafts the contract so the lawyer is out of the loop; dramatically cheaper than 2.5 to 3% a side; New York,
  Hudson Valley first. State it as the plan, not as something the research overturned.
- **The findings are the hurdles the idea must clear, stated exactly as the research states them, not softened**:
  the broker licence for every core act "for another" with criminal and fee-forfeiture consequences (WS2 section 1,
  RPL 440, 442-d, 442-e); contract drafting for another is the practice of law, a broker may only fill non-legal
  blanks (L21, L22; AG 96-F11; DOS LI04); MLS entry by a licensed participant, no input API (WS3); buyers' agents
  and buyer behaviour (WS4, WS5); customer-acquisition cost; his ten years away; the New York office; E&O; the
  failed kill tests, named plainly. For each hurdle: what it requires today, what the minimum human or licensed
  act is, how the software shrinks it, and what would have to change (or be tested) for the idea to go further.
  That is the honest shape of "the idea, and what stands in its way".
- **The launch path for the original idea**, built from the research: the software is the agent; because the law
  says the operator of a fee-earning agent service must be a licensed broker, the firm operating it is licensed,
  with the father-in-law as broker of record via the $185 no-exam attorney route (if his registration is current)
  doing only the acts the law requires of him, each logged. For the contract: what the research says about how the
  "lawyer out of the loop" part can operate (broker fill-in of a form subject to attorney approval; his own law
  practice under the narrow fixed-fee route in the memo; the parties as their own drafters using the software).
  **You may run targeted web research on one load-bearing gap only**: whether New York treats document-assembly
  software used by a party to prepare their own contract as the unauthorised practice of law (for example NY
  cases or opinions on LegalZoom-type products, Upsolve v. James and its appeal, any NY regulatory sandbox
  proposal). Follow `docs/research/method/researcher.md`: cite, label [PRIMARY] / [SECONDARY] / [CLAIMED] /
  [INFERENCE], date facts; stop on materiality. Everything else comes from the existing research.
- **Paring back is Joe's option, not the plan.** Where the research shows a narrower version is easier (for
  example seller side first, or the attorney-brokered model), mention it once, near the end, as a fallback Joe can
  choose later. Do not lead with it.
- **Money**: reuse WS4's cost structure and numbers; restate them for the idea's pricing (well under 2.5 to 3% a
  side). Invent no new numbers: if a scenario needs one the research lacks, say so and mark it [INFERENCE].
- **The free inspection** was the father-in-law's add-on to evaluate honestly; present WS6's findings and
  recommendation as his idea's evaluation (Q43, provisional).
- **What the demo shows**: per the amended success criteria, the AI doing every step of one sale of the Holmes
  house on both sides, with red "NY law today" markers where a licence or lawyer is required.

## Read (selectively)

The current `docs/EXECUTIVE-SUMMARY.md`, `docs/PLAN.md`, `docs/ASSUMPTIONS.md`, `docs/QUESTIONS-FOR-JOE.md`;
`docs/research/memo-father-in-law.md`; `docs/research/fact-check.md`; the six deliverables' opening sections and
verdicts (`docs/research/WS1` to `WS6`), and grep them for specific facts rather than reading them whole.

## Write

1. **`docs/EXECUTIVE-SUMMARY.md`**: rewritten in Joe's voice to his father-in-law, signed "Joe", same length or
   shorter (it is read on a phone), every number linked to its source report, "research to plan with, not legal
   advice". Sections roughly: the idea; why it can work; the hurdles, plainly; how we launch it; competitors; the
   money; your role; the free inspection; what the demo shows; next three steps with dates.
2. **`docs/PLAN.md`**: rewritten to match: phases (the demo build is 2026-10-23 to 10-27, Joe's click-through
   10-28, meeting about 10-30), costs, open questions, and the human-in-the-loop map recast as the hurdle map
   (each act where NY law today requires a licensed person or a lawyer, who that is at launch, and the path to
   shrinking it). Keep the "What already exists" section.
3. **`docs/ASSUMPTIONS.md`**: for each assumption whose kill test failed, add a dated status line: "Kill test
   failed (evidence). Joe, 2026-10-23 (decision 21): the idea is kept; carried as a hurdle." Do not change the
   evidence or soften the result. Re-rank only if decision 21 changes how fatal an assumption is, and say why.
4. **`docs/QUESTIONS-FOR-JOE.md`**: rework every open question that presumes the replaced business (fee model,
   option A/B, "broker only", lead pitch wording, hours as working broker, etc.): reword it for the original idea
   or close it into "Answered" with "closed by decision 21". Rewrite the father-in-law questions as one short
   bundle (bar registration current; where he lives and a possible NY office; willing to be broker of record
   whose required acts the software prepares; ten people who might sell, by 2026-11-06; his view on the contract
   route), and update the "Start here" box. Keep each question one paragraph with a provisional choice.
5. **`docs/research/memo-father-in-law.md`**: leave the findings alone; add at the top a two-line note that the
   memo is research on his roles and still applies under the original idea (decision 21), and fix any sentence
   that presents the replaced business as the plan.

Do not edit the research deliverables, `SUCCESS-CRITERIA.md`, `BRIEF.md`, `DECISIONS.md`, the architecture spec or
`TRACEABILITY.md` (the other job owns the last two).

## Finish

`git add` only the files you changed and commit ("Executive summary, plan, assumptions and questions rewritten
around the original idea (decision 21): ..."); if git reports the index is locked, wait a few seconds and retry.
Do not push. Final answer, under 300 words: the new framing in two sentences, what the contract-route research
found (with its labels), the father-in-law question bundle as you wrote it, and anything you could not settle.
