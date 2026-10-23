# Your job: assumptions status, questions, project plan and executive summary (headless, 2026-10-23; hard cap)

All research is in: six deliverables, a memo, an independent fact-check (which corrected some reports in place),
the POC architecture spec and the demo-house data. Turn it into the four documents below. Be economical: read the
deliverables' opening (BLUF) sections, kill-criteria sections and conclusions, plus specific sections you need,
rather than every line; do not read `research_notes/`. Commit your own files at the end (`git add <paths>`, a
meaningful message); do not push; do not edit `docs/PROGRESS.md`, `docs/SPEND-LOG.md`, `docs/DECISIONS.md`.

## Read
`docs/BRIEF.md` (Joe's goals: "a well-researched plan that shows the real hurdles ... so he sees this is sober
and credible, not just hype. I want him to look at it and think this is promising and impressive and want to move
forward"), `docs/SUCCESS-CRITERIA.md`, `docs/ASSUMPTIONS.md`, `docs/DECISIONS.md`, `docs/QUESTIONS-FOR-JOE.md`,
`docs/OUT-OF-SCOPE.md`; `docs/research/WS1-...` to `WS6-...`, `memo-father-in-law.md`, `fact-check.md` (its
corrections win over the reports where they differ); all of `docs/research/handoff/WS1.md` to `WS7.md`;
`docs/specs/poc-architecture.md` sections 0, 3 (checkpoint catalogue), 9 and 11; `docs/specs/demo-house.md`
summary; `docs/SPEND-LOG.md`.

## 1. `docs/ASSUMPTIONS.md`
Keep the table; fill the Status column for A1 to A11 with a dated line (hit / partly hit / dodged / still open,
one plain sentence, link to the deliverable section), reconciling the handoffs where they differ (say how). Add
assumptions the research surfaced (at least: the father-in-law's network still produces listings after about ten
years away; he can keep a New York office and supervise from out of state), scored like the others. Add a
"Kill criteria K1 to K9" section with each one's status and evidence. Re-rank if the scores changed. Put a short
"What the research changed" paragraph at the top: hits stated plainly, not softened.

## 2. `docs/QUESTIONS-FOR-JOE.md`
Add the handoffs' "Questions for Joe" under `## Open`, deduplicated, numbered from Q13, each in plain words with a
provisional choice and what it unblocks. Keep Q11 and everything under `## Answered` exactly as it is. Include the
architecture spec's section 11 items (contract draft in the attorney's workspace; replay by default at the meeting).
Mark which questions are for the father-in-law rather than Joe.

## 3. `docs/PLAN.md`
Phases with dates where they follow from the meeting (about 2026-10-30): Phase 0 validate (the ten seller calls,
his bar status and residence, the DOS and OneKey calls); Phase 1 the demo (build 10-25 to 10-28, meeting); Phase 2
set up the firm (entity, licence, office, Realtor and MLS membership, E&O, forms); Phase 3 pilot listings; Phase 4
scale or stop. For each: goal, steps, who does it (Joe, father-in-law, software, outside lawyer), cost (from WS4,
low and realistic), duration, and the go/no-go gate tied to named kill criteria. Then: open questions (link to
QUESTIONS), and the **human-in-the-loop map**: one table of every step where a licensed person, a lawyer or a human
must act (WS1's 21 "human or licence required" functions plus WS2's checkpoints and the architecture's checkpoint
catalogue), with who acts, why (F-ID, L-ID) and roughly how long it takes. End with what the demo shows versus what
is real.

## 4. `docs/EXECUTIVE-SUMMARY.md` (the one document Joe hands his father-in-law)
Two to three pages, plain, sober, compelling where the evidence is. Lead with the idea as the research reshaped it
(what it is now, versus "no agent, no lawyer"), then why it can work (where the evidence is good), the hurdles named
plainly (licence and his personal acts per deal, the lawyer step, MLS entry by a human, buyers' agents and what
sellers really save, cost of winning customers, his ten years away and the New York office), the competitors (who
is closest, nobody local), the money (year-one cost, break-even), the free-inspection verdict, his role options (from
the memo), what the demo shows, and the next three steps with dates. Every number traceable to a report (link the
report). No hype words; no softening. Write it to him (second person is fine), signed "Joe".
Final reply (under 10 lines): the new top-ranked assumption, kill criteria hit, and the three next steps.
