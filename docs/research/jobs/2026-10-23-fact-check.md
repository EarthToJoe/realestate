# Your job: independent fact-check of the six research reports (headless, 2026-10-23; hard budget cap)

You did not write these reports; check them as an outsider. Joe's standard: "comprehensive, accurate, focused on
the right things"; no arbitrary search limits, but no chasing nits. Be economical with reading: use grep and read
the sections you need; do not read `research_notes/` except a report's own gap-fill verification table.
No state-changing git commands.

## Files
Reports: `docs/research/WS1-agent-functions.md`, `WS2-legal-licensing.md`, `WS3-listing-data-access.md`,
`WS4-cost-model.md`, `WS5-competitors.md`, `WS6-free-inspection.md`, and `docs/research/memo-father-in-law.md`.
Handoffs: `docs/research/handoff/WS1.md` to `WS7.md` (section 6, "Contradictions").

## 1. Settle the dual-role question first (it changes advice already sent to a lawyer)
WS2 constraint **L27** (and the memo) say a lawyer may act as the seller's lawyer AND listing broker in the same
deal if the brokerage fee is fixed, paid upfront, non-refundable and non-contingent, with written consent (NYSBA
Op. 1015, Op. 1117 fn. 1). The WS5 handoff says this looks unsafe because NYSBA Op. 1043 bars the dual role "with
or without client consent". Open the opinions themselves on nysba.org (1015, 1043, 1117, and any later opinion
that cites them; also 2020s opinions on lawyer-brokers) and decide: does the fixed-fee route exist, under what
exact conditions, and how do 1015 and 1043 fit together? Quote the operative sentences with links.

## 2. Cross-report consistency
List every fact or number that appears in more than one report or in the memo (licence fee, OneKey/HGAR/MLS
fees and their annual total, E&O premium, average NY commission, share of buyers using agents, OneKey county
coverage, timelines, attorney-drafting custom, company status such as Opendoor/Hauseit/LocQube, etc.). Where
they disagree, find the primary source and decide which is right.

## 3. The handoffs' "Contradictions" sections
Resolve each item listed there.

## 4. Spot-check what the writers could not verify
In each report's notes gap-fill section, the "Verification of load-bearing claims" table marks some claims
"could not verify" or rests them on [SECONDARY]/[CLAIMED] sources. Pick the three most decision-critical of
those per report and check them against primary sources. Do not redo claims already marked confirmed.

## Apply and record
- Apply each correction directly in the affected report or memo, in place, followed by
  `*(Corrected 2026-10-23 by fact-check: what changed and the source.)*`. Change nothing else.
- Write `docs/research/fact-check.md`: one-paragraph summary (how many checks, how many corrections, the
  dual-role verdict in one plain sentence), then a table `Check | Where | Verdict (confirmed / corrected /
  unresolved) | Source`, then "Unresolved" with what would settle each.
Final reply (under 10 lines): the dual-role verdict, number of corrections, and the most important one.
