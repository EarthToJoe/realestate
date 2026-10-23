# Job: revise the POC architecture spec and traceability for decision 21 (the original idea)

Date 2026-10-23. Tag RESPEC-A. Budget cap $10. You are one of two jobs running at the same time; the other
rewrites the executive summary, plan, assumptions and questions. Touch only the files listed under "Write".

## Why

Joe, this morning: "Keep the original idea, that is what I said I would build. I can pare it back on the future if
need be. The idea is the idea. Completely replace the real estate agents." Read `docs/DECISIONS.md` decisions 21
and 22, `docs/BRIEF.md` ("The idea", "Demo-ability", workstream 7) and `docs/SUCCESS-CRITERIA.md` (already amended
for decision 21; it is the finish line, do not edit it).

The spec written overnight designed the demo around a working licensed broker and an attorney: broker approval
gates, "the AI never sets the price", "no message leaves without a human", the contract drafted in the seller's
attorney's workspace. Under decision 21:

- **The AI is the agent on both sides and does every agent act**: accepts the listing, advises on price, writes,
  checks and publishes the marketing, answers and sends messages (sending simulated), schedules showings, presents
  offers and advises, negotiates counters with the other side, drafts the contract and rider in the product's own
  contract step (no attorney workspace), coordinates to closing, and markets the business.
- **The seller and the buyer make their own decisions**, as any agent's clients do: sign the listing agreement or
  buyer agreement, choose the list price, accept / counter / reject, approve their offer, give consents, complete
  their own Property Condition Disclosure. These stay blocking.
- **Wherever New York law today requires a licensed person or a lawyer, a red "NY law today" marker** shows on
  the screen: the rule in one plain sentence, who the law says must act, the F- and L-IDs, and a link to the finding
  on the review site. It is recorded and counted on the timeline. **It does not stop the flow.** The findings are
  not softened: write the rule as the research states it.
- **Practical "human required" steps stay** where no software route exists: a licensed MLS participant keys the
  listing into OneKey (no input API, WS3), notary and wet-ink items, third parties (inspector, appraiser, lender,
  title, escrow holder). These are facts about the world, not design choices.
- The fair-housing checker still blocks publishing copy that fails (that is the software complying, not a human
  gate). The DEMONSTRATION mark on the real Holmes address stays (section 0, point 2).

## Read (selectively; do not read whole research deliverables)

`docs/specs/poc-architecture.md` (all), `docs/TRACEABILITY.md`, `docs/OUT-OF-SCOPE.md`,
`docs/research/handoff/WS1.md`, `WS2.md`, `WS3.md`, `WS7.md`. Look up specific F-IDs and L-IDs with grep in
`docs/research/WS1-agent-functions.md` and `docs/research/WS2-legal-licensing.md` when you need the exact rule
text. No web research: this is a design revision from existing findings.

## Write

1. **`docs/specs/poc-architecture.md`**, revised in place, keeping everything decision 21 does not touch (stack,
   "What already exists", PII, fair-housing pipeline, model choice):
   - Status line: revised 2026-10-23 for decision 21. Section 0 rewritten: the design follows the brief's idea;
     the contract point now says the software drafts the contract for the parties, with the marker stating that
     drafting a contract for another is the practice of law in NY (L21, L22) and that Hudson Valley custom is the
     seller's attorney drafts (L25); MLS point stays.
   - Replace the checkpoint model with one record type carrying a `kind`: `client_decision` (blocking),
     `law_marker` (non-blocking, who the law says must act: L licensed broker, A attorney), `human_required`
     (practical, e.g. MLS keying), `third_party` (planned), `automated` (logged AI acts such as notices). Keep the
     CP-numbers where a step survives so traceability stays stable; renumber nothing that need not change.
   - Rewrite the step-by-step map and the checkpoint catalogue to match: for each row, who acts in the product
     (AI / seller / buyer / third party) and the "NY law today" marker, if any, with its F- and L-IDs.
     Communications: the AI negotiates within authority the seller gave and passes the seller only the seller's
     decisions; messages that negotiate or advise carry a marker. Showings: owner-hosted showing or a self-guided
     tour; say what L19 and WS3 say about each and mark accordingly.
   - Timeline colours: AI did it (blue), the seller or buyer decided (amber), NY law today marker (red), third
     party (grey). The human-in-the-loop map becomes the hurdle map, still built only from records.
   - Section 7: recheck the model per step and the cost per live run now that the AI also negotiates and drafts
     the contract; change only if material.
   - Section 9 build order: the build starts today, Friday 2026-10-23, as soon as this spec is committed. Keep
     four vertical slices; re-date them (Fri 10-23 evening to Tue 10-27), with Joe's click-through still on
     Wed 10-28 and polish 10-29. Update every acceptance check to the amended success criteria. Update "Cut first"
     and "Never cut" (never cut: client-decision gates, NY-law-today markers with reasons, the fair-housing checker
     and its fixtures, "human required" markers for MLS keying, the timeline built from records, narration cards,
     PII baseline, traceability).
   - Section 10 risks: replace the Step 7 risk with the honest one (a lawyer watching software draft a contract;
     handled by the marker stating the law plainly, the plan's launch path, and labels on every page of the draft).
   - Section 11: decisions 1 (contract framing) and 2 (who pays) are answered by decisions 21 and 22; say so and
     keep 3 and 4; add any new decision the revision raises, with a provisional choice.
2. **`docs/TRACEABILITY.md`**: every feature row names the WS1 function it replaces (now including functions WS1
   classes "requires a human or licence", which the AI performs with a marker) and the WS2 constraint, with a new
   column "In the demo" (AI / seller / buyer / third party / human required) and "NY law today" (the marker text
   in a few words, or "none"). No orphan features; list any WS1 function the demo does not cover in a short
   "not in the demo" table with the reason.
3. **`docs/OUT-OF-SCOPE.md`**: adjust only what decision 21 changes.
4. If the revision forces an architecture decision not covered by 21 or 22, append it to `docs/DECISIONS.md` as
   23 onward, with the reasoning. Do not edit decisions 1 to 22.

Do not edit research deliverables, `SUCCESS-CRITERIA.md`, `BRIEF.md`, `PLAN.md`, `EXECUTIVE-SUMMARY.md`,
`ASSUMPTIONS.md` or `QUESTIONS-FOR-JOE.md` (the other job owns the last four). If you find the amended success
criteria inconsistent with the research or each other, say so in your final answer instead.

## Finish

`git add` only the files you changed and commit ("Architecture spec and traceability revised for decision 21:
..."); if git reports the index is locked, wait a few seconds and retry (the other job commits too). Do not push.
Final answer, under 250 words: what changed in the design, the new checkpoint counts by kind, the revised build
dates, any inconsistency found, and any new decision for Joe.
