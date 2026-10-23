# Demo walkthrough script

Generated from `app/demo/steps.yaml` by `scripts/gen-demo-script.py`; do not edit by hand (a test fails if
this file and the screens drift apart). Open https://realestate.hughesnode.com (house login), press
**Start demo**, and follow the screens in order. The same words are in the app: **Notes** in the bar at the
top of a phone, **Presenter notes** under the step list on a laptop. The audience sees only the product
until you open them.

**Length.** 10 steps, 20 screens, target 14.5 minutes with the introduction (SC11: 12 to 15). The
words below take about 8.3 minutes to say at 150 words a minute; the rest is tapping and letting
the audience look. The timed run is in `docs/build/e2e-demo-run.md`.

Built: all ten steps.

**Colours on every screen:** blue = the AI did it; amber = the seller's or buyer's own decision (the next
step waits for it); red = **NY law today** requires a licensed broker or a lawyer for this act (recorded,
does not stop the flow); grey = a person or third party outside the software. **View as** (top right)
changes who is acting: Presenter, Seller or Buyer. Only the client whose decision it is can make it. Each
screen leads with its result; tables, drafts and records sit in folds ("Show the working").

**The presenter's controls (phone or laptop):**

- **Start demo** (home) asks first ("This resets the deal to the beginning"), then opens step 1 with the
  guided demo on: the notes open on every screen (close them with ×; they stay closed on that device until
  you open them again), with **Next** to the following screen in walk order.
- **Spotlight** (in the notes) points at the parts of the screen this script names, one at a time, with a
  short caption the audience may read.
- **Do this screen for me** (in the notes) does this screen's taps the way this script does, with the
  recorded AI answers (no cost); each client decision is still recorded as the client's.
- **Decide as the seller** (or buyer) on an amber card switches the persona in one tap and comes back to the
  card; **Back to the Presenter** afterwards. The Presenter can never make a client's decision.
- **Any step link works at any time.** A step that needs an earlier one shows a card: what is missing, on
  which step, who must do it, a button to go there and **Fast-forward the demo to here** (also the ⏩ beside
  each step in the list), which plays the earlier steps with this script's choices at no cost.
- **On a phone** the bar at the top says where you are ("Step 7 of 10: Offers"), with arrows to the
  previous and next screen in walk order, **Notes**, and ☰ for the full list.

**Step numbers.** The screens number the steps in the order the demo walks them, 1 to 10 (Q47). The
success criteria number three of them differently; the mapping, once:

| On screen and in this script | Success criteria |
|---|---|
| 1. Intake | SC1 |
| 2. Pricing | SC2 |
| 3. Listing copy | SC3 |
| 4. Marketing plan | SC4 |
| 5. Communications | SC5 |
| 6. Buyer side | SC8 (renumbered) |
| 7. Offers | SC6 (renumbered) |
| 8. Contract | SC7 (renumbered) |
| 9. Deal timeline | SC9 |
| 10. Marketing the business | SC10 |

## Introduction (0.5 min, on the home page)

- **Say:** This is a demonstration of one Hudson Valley house sale, from the listing to the signed contract, with an AI as the agent on both sides. The seller and the buyer make their own decisions. Wherever New York law today needs a licensed broker or a lawyer, a red note says so; it is recorded and does not stop the sale. Everything is simulated: nothing is sent.
- **Point at:** The four colours on the home page.

## 1. Intake (1.5 min)

### 1.1 Address and facts (`/intake`, screen 1 of 20)

- **Do:** Tap "Use demo house", then "Start intake".
- **Say:** The seller starts with an address and the few facts the public record leaves out: parking, condition, roof, taxes and four questions the state requires. The house is a real address in Holmes, so every screen carries the DEMONSTRATION mark; the seller is fictional and no owner name is stored. When the seller submits, the AI sends the three notices New York requires at first contact.
- **Point at:** The DEMONSTRATION strip at the top; the state's four questions at the end of the form.
- **Markers and decisions:** none; the AI sends three notices when the seller submits (CP-24, blue)
- **Spotlight:** Every screen carries this mark: a real address, fictional people, nothing sent.; The seller's own facts: what the public record leaves out.

### 1.2 Property profile (`/intake/profile`, screen 2 of 20)

- **Do:** Tap "Let the AI fill the gaps".
- **Say:** Every fact shows where it came from: grey from the public record, amber from the seller, blue inferred by the AI, each with its reason. The AI fills gaps about the house, never the seller's own disclosure answers. The badge at the top always says whether the AI is live or a recorded run.
- **Point at:** The three source counts; one blue "AI inferred" fact and its reason.
- **Markers and decisions:** none
- **Spotlight:** Where every fact came from: the public record, the seller, or the AI.; The AI's work: what it inferred, and what the seller should confirm.; Live AI or a recorded run: always labelled, never passed off.

### 1.3 Disclosure checklist (`/intake/disclosures`, screen 3 of 20)

- **Do:** Nothing to tap. The seller's own form can wait for the contract (step 8).
- **Say:** From the facts, the AI works out which disclosures this house needs: no lead-paint form, because it was built in 1995, and it is not in an agricultural district. The Property Condition Disclosure is the seller's own: the software never fills it in. The amber card is a decision only the seller can make, and contract signing waits for it.
- **Point at:** The amber card for the seller's disclosure form.
- **Markers and decisions:** CP-04 seller decision (amber, blocks contract signing)
- **Spotlight:** Which disclosures this house needs, and why.; Only the seller completes this form; the contract waits for it.

### 1.4 Seller onboarding (`/intake/onboarding`, screen 4 of 20)

- **Do:** Tap "Decide as the seller" and acknowledge the agency form. Back as the Presenter, tap "Let the AI accept the listing". Then "Decide as the seller" again and sign the listing agreement.
- **Say:** The AI gives the listing presentation, checks for conflicts and accepts the listing. The red note is the research: in New York today, taking a listing for a fee is a licensed broker's act. It is recorded and counted, and it does not stop the sale. The seller acknowledges the agency form and signs the listing agreement, the seller's own decisions; nothing is marketed until it is signed.
- **Point at:** The red "NY law today" note, then the seller's signed agreement.
- **Markers and decisions:** CP-01 and CP-03 seller decisions (amber); CP-02 NY law today (red, licensed broker)
- **Spotlight:** A red note: an act New York reserves to a licensed broker. Recorded, never a stop.; The seller's own decision: the AI cannot sign for the seller.

## 2. Pricing (1.5 min)

### 2.1 Comparable sales (`/pricing`, screen 5 of 20)

- **Do:** Open "Every adjustment, line by line" only if someone asks how the numbers work.
- **Say:** Eight real sales from the county's public records, all within about four miles. Code, not the model, adjusts each one toward this house: date, size, basement, lot, age, rooms, air conditioning and style, at the rates on the screen. Weak sales are flagged and count for less. The label says what this is: a market analysis, not an appraisal.
- **Point at:** The range at the top and the "not an appraisal" label.
- **Markers and decisions:** none; the range is computed in code
- **Spotlight:** The price range, computed in code from the adjusted sales.; A comparative market analysis, not an appraisal.

### 2.2 The AI's price advice (`/pricing/advice`, screen 6 of 20)

- **Do:** Tap "Let the AI recommend a price", then "Decide as the seller" and "Choose this list price". (Step 3 refuses to start until the seller chooses.)
- **Say:** The AI explains its method, names the weaker sales and recommends a list price, with its reasons and what the seller would keep. The red note: advising a seller on price is a licensed broker's duty in New York today. The price itself is the seller's decision, and the listing copy waits for it.
- **Point at:** The recommended price, the red note, then the seller's choice.
- **Markers and decisions:** CP-25 NY law today (red, licensed broker); CP-05 seller decision (amber, blocks step 3)
- **Spotlight:** The AI's recommended list price, with its reasons.; Price advice is a licensed broker's duty in New York today.; The seller chooses the price.

## 3. Listing copy (1.5 min)

### 3.1 Drafts and the fair-housing check (`/copy`, screen 7 of 20)

- **Do:** Tap "Let the AI write the copy". Open the portal description and tap "Plant a violation (demo)", then "Let the AI apply the fix and re-check", then "Let the AI mark passing copy ready to publish".
- **Say:** The AI writes the MLS remarks, the portal description, three social posts and the flyer. Every piece goes through the fair-housing check: written rules for every federal and New York protected class, then a model review. Plant a violation, "perfect for a young family, steps from the church": caught, with the rule and a fix. Only passing copy can be marked ready, and marking an ad ready is a broker's act today.
- **Point at:** The planted sentence highlighted, the fixed version, then the red note.
- **Markers and decisions:** CP-26 fair-housing pass (blue, per piece); CP-06 NY law today (red, per piece)
- **Spotlight:** The fair-housing check on the portal description.; Marking an ad ready to publish is a broker's act in New York today.

### 3.2 MLS pre-check and package (`/copy/mls`, screen 8 of 20)

- **Do:** Open the flyer (PDF) if you want to show it.
- **Say:** The remarks are checked against OneKey's rules: no contact details, no showing instructions, no commission, never "free". The package lists every field in OneKey's order for the person who keys it in. The flyer carries the DEMONSTRATION mark on every page.
- **Point at:** The ticks of the MLS pre-check.
- **Markers and decisions:** none on this screen
- **Spotlight:** OneKey's rules for the public remarks, checked in code.; Every field, in OneKey's order, ready for the person who keys it in.

## 4. Marketing plan (1 min)

### 4.1 Channel board (`/channels`, screen 9 of 20)

- **Do:** Tap "Decide as the seller", choose "Publish to Internet" and sign. Back as the Presenter, tap "Record the MLS entry (simulated)" and watch the portal cards change.
- **Say:** Each card says who really does the work. OneKey has no way for software to enter a listing, so a licensed MLS member keys it in from the AI's package: the grey "a person does this" note. Zillow, Realtor.com, Redfin and Homes.com are fed from the MLS. The seller signs the exposure choice and the lockbox and photo permissions.
- **Point at:** The grey MLS card, then the portal cards.
- **Markers and decisions:** CP-07 seller decision (amber); CP-08 human required (grey)
- **Spotlight:** No software route into the MLS: a licensed member keys the listing.; The seller's own choices: exposure, lockbox, photographer.

## 5. Communications (1.5 min)

### 5.1 Fact sheet, authority and inbox (`/inbox`, screen 10 of 20)

- **Do:** Tap "Decide as the seller" and approve the fact sheet and the AI's authority (allow self-guided tours). As the Presenter, tap "Let all of them arrive"; answer the seller's two cards as the seller.
- **Say:** Nothing goes out until the seller approves the facts and what the AI may agree. Then eight enquiries arrive and the AI answers each on its own: it discloses the oil heat and the septic, books an owner-hosted showing and a self-guided tour, declines to rate schools and gives no legal advice. Only two questions reach the seller. Each message about the house is a red note: a licensed act today.
- **Point at:** The thread list, then the seller's two cards.
- **Markers and decisions:** CP-27 seller decision (amber); CP-09 and CP-28 NY law today (red); CP-10 human required (grey); CP-24 and CP-29 AI did it (blue)
- **Spotlight:** What the AI may say and agree: the seller approves it first.; Every enquiry answered by the AI, fair-housing checked, signed with the firm's name.; Only the seller's own decisions reach the seller.

## 6. Buyer side (2 min)

### 6.1 Buyer intake (`/buyer`, screen 11 of 20)

- **Do:** Tap "Use the demo buyer (fictional)", then "Become a client of the firm". Then "Decide as the buyer": acknowledge the agency form and sign the buyer agreement.
- **Say:** Now the same sale from the buyer's side. The intake asks about the home and the money, never about family, religion or any protected trait. The AI takes the buyer on as a client, a broker's act today, and sends the notices and a buyer agreement with a stated, negotiable fee. The buyer's private limit goes to the buyer's AI only.
- **Point at:** The buyer's private limit, then the red note.
- **Markers and decisions:** CP-30 NY law today (red); CP-24 AI did it (blue); CP-16 buyer decision (amber)
- **Spotlight:** Only the buyer's AI sees this; the seller's AI never does.; Taking on a client is a broker's act in New York today.; The buyer's own decision, before any tour.

### 6.2 Search and alerts (`/buyer/search`, screen 12 of 20)

- **Do:** Tap "Save the search and let the AI send the alert".
- **Say:** The search uses the home's facts only: there is no school-rating or neighbourhood filter, so it cannot steer. The buyer's AI writes the alert, fair-housing checked and signed with the firm's name, like every message.
- **Point at:** The filters (facts only), then the alert.
- **Markers and decisions:** CP-09 NY law today (red); CP-24 AI did it (blue)
- **Spotlight:** Facts about the home only: nothing that could steer.; The alert, written by the buyer's AI.

### 6.3 Tour and dual-agency consent (`/buyer/tour`, screen 13 of 20)

- **Do:** Tap "Ask the AI to book a tour". Then "Decide as the buyer" and "Decide as the seller" to consent to dual agency.
- **Say:** The code refuses a tour before the buyer agreement is signed. The tour is self-guided, a red note because New York has not decided whether an unaccompanied tour is a licensed showing. The firm now acts for both sides, so both clients consent in writing to dual agency; each keeps its own AI and its own secrets.
- **Point at:** The booked tour, then the two consents.
- **Markers and decisions:** CP-29 AI did it (blue); CP-28 NY law today (red); CP-17 seller and buyer decision (amber)
- **Spotlight:** The tour, booked inside the seller's hours.; Both clients consent: the firm acts for both.

### 6.4 The buyer's offer (`/buyer/offer`, screen 14 of 20)

- **Do:** Tap "Let the buyer's AI advise and draft the offer", then "Decide as the buyer" and approve it. After the seller's counter (step 7), come back here to approve the buyer's reply.
- **Say:** The buyer's AI advises on price and terms from the buyer's own answers and the public sales, and drafts the offer: a broker's act today. Only the buyer can approve it; then it reaches the seller as offer B. When the seller counters, the buyer's AI advises again and sends only the reply the buyer approves.
- **Point at:** The buyer's AI's advice, then the buyer's approval.
- **Markers and decisions:** CP-31 and CP-13 NY law today (red); CP-18 buyer decision (amber)
- **Spotlight:** The buyer's AI advises the buyer.; Only the buyer approves the offer.

## 7. Offers (1.5 min)

### 7.1 Offers, advice and negotiation (`/offers`, screen 15 of 20)

- **Do:** Tap "Let the AI present the offers and advise". "Decide as the seller" and counter offer B at the suggested figures. Tap "Let the AI send the seller's counter". The buyer's reply is approved on step 6's offer screen ("Do this screen for me" plays the whole negotiation).
- **Say:** Two offers: one through an outside buyer's agent, one from the firm's own buyer. Code builds the comparison and what the seller keeps; the seller's AI presents and advises, a licensed act today. The seller decides: accept, counter or reject, and the limits of the counter. The two AIs then negotiate inside those limits; anything outside goes back to the seller. Nothing binds until both sign the contract.
- **Point at:** The AI's recommendation, the seller's decision, then the agreed price.
- **Markers and decisions:** CP-11 and CP-13 NY law today (red); CP-12 seller decision (amber)
- **Spotlight:** Both offers side by side, with what the seller keeps.; The seller's AI presents every offer and advises.; The seller decides, and sets the limits for the AI.; Agreed inside the seller's limits. Not binding until both sign.

## 8. Contract (1.5 min)

### 8.1 Contract draft and signing (`/contract`, screen 16 of 20)

- **Do:** Tap "Let the AI draft the contract and rider". Tap "Open the contract for signing" and watch it refused: the seller's disclosure form is missing. Complete it on the next screen, come back, attach the disclosures, open signing, and sign as the seller and as the buyer.
- **Say:** The AI drafts the contract of sale and rider for both parties, in the bar-association form's order, and code checks it against the deal. The red note says it plainly: in New York today only a lawyer may draft a contract for someone else. Signing waits for the seller's disclosure form. The signing map shows what e-signature cannot do: the deed's notary and the smoke-detector affidavit.
- **Point at:** The red note, the signing map, then the PDF.
- **Markers and decisions:** CP-32 AI did it (blue); CP-14 NY law today (red); CP-15 human required (grey); CP-33 seller and buyer decision (amber)
- **Spotlight:** Only a lawyer may draft a contract for someone else in New York today.; What e-signature can and cannot do.; Every page of the draft carries the demonstration label.

### 8.2 The seller's disclosure form (`/disclosures/pcds`, screen 17 of 20)

- **Do:** Tap "Decide as the seller", then "Seller: submit my prepared answers". Then back to the contract.
- **Say:** The state's current disclosure form: 56 questions. Every answer starts blank, and the seller fills it in from their own knowledge; the software never does. The demo seller's answers are fiction.
- **Point at:** The blank form, then the seller's submitted answers.
- **Markers and decisions:** CP-04 seller decision (amber)
- **Spotlight:** The seller's own answers; the software never fills them in.

## 9. Deal timeline (1 min)

### 9.1 Deal timeline and hurdle map (`/timeline`, screen 18 of 20)

- **Do:** Open "The hurdle map", then "What the AI did".
- **Say:** This page is built only from the records the other screens wrote. Blue is what the AI did, amber what the seller or buyer decided, red where New York law today needs a licensed broker or a lawyer, grey the people and firms outside the software, down to the closing. The hurdle map lists every red note with its rule; the last list is every act a supervising broker would review.
- **Point at:** The four totals, the road to closing, then the hurdle map.
- **Markers and decisions:** every record so far; CP-35 standing; CP-20 to CP-23 and CP-34 planned
- **Spotlight:** The whole sale in four numbers, from the records.; The road to closing: the third parties and their dates.; Every place NY law today needs a licensed broker or a lawyer.; Every act a supervising broker would review.

## 10. Marketing the business (1 min)

### 10.1 The firm's campaign (`/brand`, screen 19 of 20)

- **Do:** Tap "Let the AI write the campaign". On the landing page tap "Try a bolder headline (demo)" and watch it refused; then "Let the AI remove it and re-check".
- **Say:** Last, the AI markets the firm itself: a landing page for sellers, a local ad and a free seller's guide. The same fair-housing check runs, plus a check on claims. Try the headline the idea invites, "the AI that replaces your agent and your lawyer": refused. Advertising law bars that claim while the law still needs them, and no one may be told they do not need a lawyer.
- **Point at:** The refused headline, then the notices the page carries.
- **Markers and decisions:** CP-26 AI did it (blue, per piece)
- **Spotlight:** The landing page, checked like every other piece of copy.; The notices the law requires, added by code, never by the AI.

### 10.2 Who sees the ad (`/brand/targeting`, screen 20 of 20)

- **Do:** Tap "Let the AI set the targeting". Open "What the code will not let the AI do" and tap "Try to target ages 25 to 44 (demo)". Then "Let the AI publish the campaign (simulated)".
- **Say:** Housing ads may not pick people by age, gender, family, ZIP code or a lookalike of past clients, so the AI may only choose a place, by radius. Try age: refused by code. The AI publishes, simulated, and the red note says that in New York today only a licensed broker may place the firm's own ads.
- **Point at:** The targeting (place only), the refused age, then the red note.
- **Markers and decisions:** CP-19 NY law today (red)
- **Spotlight:** Place by radius, everyone 18 and over: nobody picked for who they are.; Only a licensed broker may place the firm's ads in New York today.
