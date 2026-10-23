# Success criteria: what "POC done" means

**Status: DRAFT, waiting for Joe's sign-off.** Nothing gets built until this is signed off (Joe's rule:
success criteria first). Reply `SIGN-OFF` or edit the lines you want changed. Every item is checkable:
a person can sit at the demo and tick it.

## 1. The demo (what the father-in-law sees)

One Hudson Valley sale, start to finish, in a web browser on a laptop (readable on a phone too), as a
**guided demo** with a visible step list down the side. Each step is its own screen you click into and
narrate. Nothing happens invisibly: when the AI does something, the screen shows it thinking, the draft it
produced, and the button a human must press.

| # | Step | Done when (checkable) |
|---|------|------------------------|
| 1 | **Intake** | Seller enters an address and a handful of facts (or picks the demo house). The system shows a full property profile; every field is tagged with where it came from (seller, public record, inferred). Finished in under 5 minutes of clicking. |
| 2 | **Pricing** | A comparative market analysis from at least 3 comparable sales, with the method shown in plain words and a suggested range. Ends at a **broker review** checkpoint; the AI never sets the price. |
| 3 | **Listing copy** | AI writes MLS remarks, a portal description, three social posts and a one-page flyer. The **fair-housing checker** runs on screen and catches planted violations (for example "perfect for a young family, steps from the church") with the rule it broke and a fixed version. Corrected copy passes. A **broker approval** gate sits before anything is marked "ready to publish". |
| 4 | **Marketing plan** | A channel board. Each channel shows its status honestly: "MLS entry: **licensed human required**, here is why", "Zillow / Realtor.com / Redfin: fed from the MLS", "Social: drafted and scheduled", "Photos, sign, lockbox: vendor booking". Every "human required" marker links to the research finding behind it. |
| 5 | **Communications** | A shared inbox. Simulated buyer enquiries arrive; the AI drafts replies; a showing gets scheduled; feedback is logged. **No message leaves without approve/edit/send by a human.** The agency disclosure and fair-housing notice appear at first substantive contact, and every outgoing message carries the broker's name as NY advertising rules require. |
| 6 | **Offers** | Two or more offers in a comparison table; AI drafts a counter with its reasoning; **the seller decides**. The AI never accepts or rejects. |
| 7 | **Contract** | AI produces a NY-style draft contract of sale pre-filled from intake and the accepted offer, with a rider, a side-by-side against the standard form structure, and the Property Condition Disclosure attached. A mandatory **attorney review** checkpoint follows. Items that still need a notary or wet ink are marked, per the legal research. |
| 8 | **Buyer side** | A buyer persona on the same system: buyer intake and representation disclosure, search alerts, a tour request, and an AI-drafted offer with the buyer's approval gate. At least these four screens. |
| 9 | **Deal timeline** | One dashboard of the whole sale from listing to closing. Each step is colour-coded **AI / human / licensed or attorney**. This is the human-in-the-loop map, generated from the system's own checkpoints, not drawn by hand. |
| 10 | **Marketing the business** | The AI drafts the brokerage's own campaign (landing-page copy, one local ad, one seller lead magnet), fair-housing-checked like everything else. |
| 11 | **Demo mode** | A "Start demo" button loads the fictional house and walks the ten steps in order with a narration card on each. The walkthrough script in `docs/DEMO-SCRIPT.md` matches the screens one for one. A full run takes 12 to 15 minutes. |

## 2. Under the hood (what makes it the first slice of the product, not a toy)

- **Modular.** Each step is a module behind a stable interface. Swapping the model provider, or replacing a
  stubbed MLS or portal connector with a real one, changes no screen.
- **Checkpoints are real objects.** Every human or licensed step is a record with who must act, why (the
  legal or practical reason), and what they decided. The deal timeline and the human-in-the-loop map are
  built from these records.
- **Traceability.** Every feature row in `docs/TRACEABILITY.md` names the agent function it replaces
  (workstream 1) and the legal constraint it respects (workstream 2). No orphan features.
- **Fair-housing checker.** A written rule set (protected classes under federal and NY law, steering
  patterns, risky phrases) plus a model review pass, tested against a fixture set of at least 30 allowed and
  disallowed phrases. Results are visible in the demo.
- **PII.** Fictional demo data only. Personal data lives in one database with fields marked as PII, an access
  log of who viewed what, export and delete for any person, PII kept out of application logs, and only the
  fields a step needs sent to the model.
- **Spend.** Every model call is logged (module, tokens, cost, time) and rolled up into `docs/SPEND-LOG.md`.
- **Runs in two places.** On the VPS behind a login at a private URL, and locally with one command.
- **Tests.** A fast test suite passes, including an end-to-end run of the demo in headless mode.

## 3. The written deliverables (what makes it credible)

- Six research deliverables in `docs/research/`, each with sources and confidence labels.
- `docs/PLAN.md`: phases, costs, open questions, human-in-the-loop map.
- `docs/EXECUTIVE-SUMMARY.md`: the one document to hand to the father-in-law.
- `docs/ASSUMPTIONS.md` updated with what the research found against each kill criterion.
- Living documents current: decisions, questions, out-of-scope, traceability, progress, spend.

## 4. Explicitly not required for "done"

Real MLS or portal integration, real e-signatures, payments, real public-record feeds, real email or SMS
delivery, identity verification, more than one brokerage, a mobile app. See `docs/OUT-OF-SCOPE.md`.

## Sign-off

- [ ] Joe: `SIGN-OFF` (date) or edits requested
