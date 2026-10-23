# Demo walkthrough script

Generated from `app/demo/steps.yaml` by `scripts/gen-demo-script.py`; do not edit by hand (a test fails if
this file and the screens drift apart). Open https://realestate.hughesnode.com (house login) and press
**Start**.

**Length.** 11 steps of the sale, then the finale and one more thing: target 18 minutes
with the introduction (SC11: 12 to 15). The words below take about 6.7 minutes to say at 150 words
a minute; the rest is pressing and letting the audience look. The timed run is in
`docs/build/e2e-demo-run.md`.

**How the screens work (decisions 47 to 51).** One path, walked in order. Every screen ends in one action
bar: **← Back** on the left, one button on the right. The button does the next thing on the screen, worded
for what it does ("Seller: list at $640,000"); when nothing is left it reads **Continue: <next step>**.
**You play the seller and the buyer: the amber buttons are their decisions. The AI does everything else**,
on its own, as soon as what it waits for is done, so each screen opens with the AI's work already there.
Every decision has a **Change** link once made: it says what it re-opens, then re-opens only that. Going
back never loses anything.

**Colours on every screen:** blue = the AI did it; amber = the seller's or buyer's own decision; red = **NY
law today** requires a licensed broker or a lawyer for this act (recorded, does not stop the flow); grey = a
person or third party outside the software. Each screen leads with its result; tables, drafts and records
sit in folds ("Show the working").

**Presenting.** Open the menu (top right) and press **I'm presenting**: it is remembered on that device.
Then the menu also holds:

- **Presenter notes**: these words, in a drawer beside the screen on a laptop (the screen narrows; nothing is
  covered) or a sheet from the bottom on a phone (starts closed).
- **Do this screen for me**: plays this screen's buttons the way this script does, with the recorded AI
  answers (no cost). Each seller or buyer decision it plays is recorded as theirs and marked "played by
  the demo" on its card and on the timeline.
- **Spotlight**: points at the parts of the screen this script names, one at a time.
- **Skip ahead**: plays every step before the chosen one with this script's choices, then opens it. A
  step that comes later in the sale shows a "Not yet" card with the same Skip ahead button.
- The demo devices (plant a fair-housing violation, a bolder headline, a refused ad target, a counter by
  hand) sit in a "Presenter's tools" fold on their screens, only when presenting.

Without presenting, a visitor sees the product only: no notes, no skip ahead, no codes.

## Introduction (0.5 min, on the home page)

- **Say:** This is one Hudson Valley house sale, from the seller signing up to the signed contract, with an AI as the agent on both sides. You play the seller and the buyer: the amber buttons are their decisions. The AI does everything else. Wherever New York law today needs a licensed broker or a lawyer, a red note says so; it is recorded and does not stop the sale. Everything is simulated: nothing is sent.
- **Point at:** The four colours on the home page, then Start.

## 1. The seller signs up (1 min)

Screen `/intake`. **The visitor reads:** A homeowner tells the firm about the house: the address and a few things only they know. The demo house is filled in; press Save and continue at the bottom.

- **Do:** Press "Save and continue".
- **Say:** The seller starts with an address and the few facts the public record leaves out: parking, condition, roof, taxes and four questions the state requires. The house is a real address in Holmes, so every screen carries the demonstration mark; the seller is fictional and no owner name is stored. When the seller saves, the AI looks the house up in the public record and sends the three notices New York requires at first contact.
- **Point at:** The demonstration line at the top; the state's four questions at the end of the form.
- **Markers and decisions:** none; the AI sends three notices when the seller saves (blue)
- **Spotlight:** Every screen carries this line: a real address, fictional people, nothing sent.; The seller's own facts: what the public record leaves out.

## 2. The AI researches the house (1 min)

Screen `/intake/profile`. **The visitor reads:** The AI has looked the house up in the public record, filled the gaps it could, and worked out which legal disclosures this house needs. Nothing to decide here: read, then continue.

- **Do:** Nothing to press. Open "Every fact, and where it came from" if someone asks.
- **Say:** Every fact shows where it came from: grey from the public record, amber from the seller, blue worked out by the AI, each with its reason. The AI fills gaps about the house, never the seller's own disclosure answers. Below, the disclosures this house needs: no lead-paint form, because it was built in 1995. The seller's own disclosure form waits for the contract, at the end.
- **Point at:** The three source counts; one blue fact and its reason; then the disclosure list.
- **Markers and decisions:** none
- **Spotlight:** Where every fact came from: the public record, the seller, or the AI.; Which disclosures this house needs, and why.

## 3. The seller hires the firm (1.5 min)

Screen `/intake/onboarding`. **The visitor reads:** The AI explains what the firm does and what it costs. The seller acknowledges the state's agency form and signs the listing agreement: both are the seller's decisions, so you press them.

- **Do:** Press "Seller: acknowledge the agency form", then "Seller: sign the listing agreement".
- **Say:** The AI gives the listing presentation and the notices. The seller acknowledges the agency form; the AI then checks for conflicts and accepts the listing. The red note is the research: in New York today, taking a listing for a fee is a licensed broker's act. It is recorded and counted, and it does not stop the sale. The seller signs the listing agreement; nothing is marketed until it is signed.
- **Point at:** The red "NY law today" note, then the signed agreement.
- **Markers and decisions:** seller decisions, agency form and listing agreement (amber); taking the listing, NY law today (red, licensed broker)
- **Spotlight:** A red note: an act New York reserves to a licensed broker. Recorded, never a stop.; The seller's own decision: the AI cannot sign for the seller.

## 4. The price (1.5 min)

Screen `/pricing`. **The visitor reads:** The AI compared eight nearby sales and recommends a list price. The price is the seller's decision: press the amber button to accept it, or change the figure first.

- **Do:** Press "Seller: list at" the recommended price. Open "The eight sales" only if someone asks how.
- **Say:** Eight real sales from the county's public records, all within about four miles. Code, not the model, adjusts each one toward this house; the AI explains the method, names the weaker sales and recommends a list price, with what the seller would keep. The red note: advising a seller on price is a licensed broker's duty in New York today. The price itself is the seller's decision. It says what this is: a market analysis, not an appraisal.
- **Point at:** The recommended price, the red note, then the seller's choice.
- **Markers and decisions:** price advice, NY law today (red, licensed broker); the seller chooses the price (amber)
- **Spotlight:** The AI's recommended list price, with its reasons.; Price advice is a licensed broker's duty in New York today.; The seller chooses the price.

## 5. The listing (1.5 min)

Screen `/copy`. **The visitor reads:** The AI wrote the listing: the MLS remarks, the portal description, three social posts and a flyer. Every piece passed a fair-housing check before it was marked ready. Nothing to decide here.

- **Do:** Nothing to press for the sale. Presenting: open the portal description, press "Plant a violation" in the presenter's tools, then "Let the AI apply the fix".
- **Say:** The AI writes the MLS remarks, the portal description, three social posts and the flyer. Every piece goes through the fair-housing check: written rules for every federal and New York protected class, then a model review. Plant a violation, "perfect for a young family, steps from the church": caught, with the rule and a fix. Only passing copy can be marked ready, and marking an ad ready is a broker's act today. The remarks are also checked against the MLS's own rules.
- **Point at:** The pieces marked ready, the red note, then the MLS checks.
- **Markers and decisions:** fair-housing pass (blue, per piece); marking an ad ready, NY law today (red, per piece)
- **Spotlight:** The fair-housing check on the portal description.; Marking an ad ready to publish is a broker's act in New York today.; The MLS's rules for the public remarks, checked in code.

## 6. On the market (1 min)

Screen `/channels`. **The visitor reads:** Where the house will be advertised, and who really does each job. The seller signs the marketing plan; then a person at the firm keys the listing into the MLS, which no software may do today.

- **Do:** Press "Seller: sign the marketing plan", then "A person at the firm keys in the MLS listing".
- **Say:** Each card says who really does the work. The MLS has no way for software to enter a listing, so a licensed MLS member keys it in from the AI's package: the grey "a person does this" note. Zillow, Realtor.com, Redfin and Homes.com are fed from the MLS. The seller signs the exposure choice and the lockbox and photo permissions.
- **Point at:** The grey MLS card, then the portal cards.
- **Markers and decisions:** the seller's marketing plan (amber); the MLS entry, a person does this (grey)
- **Spotlight:** No software route into the MLS: a licensed member keys the listing.; The seller's own choices: exposure, lockbox, photographer.

## 7. Enquiries and showings (1.5 min)

Screen `/inbox`. **The visitor reads:** People ask about the house. The seller approves what the AI may say; the AI then answers every enquiry and books showings on its own. Only two questions need the seller.

- **Do:** Press "Seller: approve", then answer the seller's two questions.
- **Say:** Nothing goes out until the seller approves the facts and what the AI may agree. Then eight enquiries arrive and the AI answers each on its own: it discloses the oil heat and the septic, books an owner-hosted showing and a self-guided tour, declines to rate schools and gives no legal advice. Only two questions reach the seller. Each message about the house is a red note: a licensed act today.
- **Point at:** The seller's two questions, then one thread.
- **Markers and decisions:** the seller approves the fact sheet (amber); messages and the self-guided tour, NY law today (red); owner-hosted showing (grey)
- **Spotlight:** Only the seller's own decisions reach the seller.; Every enquiry answered by the AI, fair-housing checked, signed with the firm's name.

## 8. The buyer signs up (2 min)

Screen `/buyer`. **The visitor reads:** Now the buyer's side. A buyer joins the firm and signs a buyer agreement; the AI finds homes and books a tour. The firm then acts for both sides, so the buyer and the seller each consent.

- **Do:** Press "Save the buyer's answers", "Buyer: sign the buyer agreement", "Buyer: consent to dual agency" and "Seller: consent to dual agency".
- **Say:** The same sale from the buyer's side. The intake asks about the home and the money, never about family, religion or any protected trait. The AI takes the buyer on as a client, a broker's act today, and sends the notices and a buyer agreement with a stated, negotiable fee. The search uses the home's facts only, so it cannot steer. The firm now acts for both sides, so both clients consent in writing; each keeps its own AI and its own secrets: the panel shows what each side's AI can see.
- **Point at:** What each side's AI can see, then the red note, then the two consents.
- **Markers and decisions:** taking on the buyer, NY law today (red); the buyer agreement (amber); the self-guided tour (red); both consents (amber)
- **Spotlight:** What each side's AI can see: the buyer's limit stays on the buyer's side.; Taking on a client is a broker's act in New York today.; Both clients consent: the firm acts for both.

## 9. The buyer's offer (1.5 min)

Screen `/buyer/offer`. **The visitor reads:** The buyer's AI advises on a price and drafts the offer from the buyer's own answers. Sending it is the buyer's decision.

- **Do:** Press "Buyer: send this offer".
- **Say:** The buyer's AI advises on price and terms from the buyer's own answers and the public sales, and drafts the offer: a broker's act today. It sees the buyer's private limit; the seller's AI never does. Only the buyer can send it; it reaches the seller as offer B.
- **Point at:** The buyer's AI's advice, then the buyer's decision.
- **Markers and decisions:** the buyer's AI advises, NY law today (red); the buyer sends the offer (amber)
- **Spotlight:** The buyer's AI advises the buyer.; Only the buyer approves the offer.

## 10. The seller decides (1.5 min)

Screen `/offers`. **The visitor reads:** Two offers are in. The seller's AI compares them and advises; the seller decides. The two AIs then negotiate inside the seller's limits, and the buyer approves each reply.

- **Do:** Press "Seller: counter offer B", then "Buyer: reply".
- **Say:** Two offers: one from another firm's buyer, one from the firm's own buyer. Code builds the comparison and what the seller keeps; the seller's AI presents and advises, a licensed act today. The seller decides: accept, counter or reject, and the limits of the counter. The two AIs then negotiate inside those limits; the buyer approves each reply. Nothing binds until both sign the contract.
- **Point at:** The AI's recommendation, the seller's decision, then the agreed price.
- **Markers and decisions:** presenting offers and negotiating, NY law today (red); the seller's decision and the buyer's reply (amber)
- **Spotlight:** Both offers side by side, with what the seller keeps.; The seller decides, and sets the limits for the AI.; Agreed inside the seller's limits. Not binding until both sign.

## 11. The contract (1.5 min)

Screen `/contract`. **The visitor reads:** The AI drafted the contract of sale. Before anyone signs, the seller completes the state's disclosure form; then the seller and the buyer each sign.

- **Do:** Press "Seller: submit my disclosure form", "Seller: sign the contract" and "Buyer: sign the contract".
- **Say:** The AI drafts the contract of sale and rider for both parties, in the bar-association form's order, and code checks it against the deal. The red note says it plainly: in New York today only a lawyer may draft a contract for someone else. Signing waits for the seller's disclosure form, which the software never fills in. The signing map shows what e-signature cannot do: the deed's notary and the smoke-detector affidavit.
- **Point at:** The red note, the disclosure form, then the two signatures.
- **Markers and decisions:** drafting the contract, NY law today (red); the disclosure form and both signatures (amber); notary at closing (grey)
- **Spotlight:** Only a lawyer may draft a contract for someone else in New York today.; The seller's own disclosure form: the software never fills it in.; What e-signature can and cannot do.

## The finale: The whole sale, start to finish (1 min)

Screen `/timeline`. **The visitor reads:** Everything the AI did, everything the seller and the buyer decided, and every place New York law today needs a licensed broker or a lawyer, from the records the other screens wrote.

- **Do:** Open "The hurdle map", then "What the AI did".
- **Say:** This page is built only from the records the other screens wrote. Blue is what the AI did, amber what the seller or buyer decided, red where New York law today needs a licensed broker or a lawyer, grey the people and firms outside the software, down to the closing. The hurdle map lists every red note with its rule; the last list is every act a supervising broker would review.
- **Point at:** The four totals, the road to closing, then the hurdle map.
- **Markers and decisions:** every record so far
- **Spotlight:** The whole sale in four numbers, from the records.; The road to closing: the third parties and their dates.; Every place NY law today needs a licensed broker or a lawyer.

## After the finale: One more thing: how the firm finds sellers (1 min)

Screen `/brand`. **The visitor reads:** Not part of the sale: the AI also markets the firm itself, with the same fair-housing check and a check on what the firm may claim. Press the button to let the AI write and publish the campaign.

- **Do:** Press "Let the AI write the campaign", then "Let the AI publish the campaign". Presenting: "Try a bolder headline" and "Try to target ages 25 to 44" are in the presenter's tools.
- **Say:** Last, the AI markets the firm itself: a landing page for sellers, a local ad and a free seller's guide. The same fair-housing check runs, plus a check on claims. Try the headline the idea invites, "the AI that replaces your agent and your lawyer": refused. Housing ads may not pick people by age, gender, family or ZIP code, so the AI may only choose a place. In New York today only a licensed broker may place the firm's own ads.
- **Point at:** The refused headline, the targeting by place only, then the red note.
- **Markers and decisions:** the firm's ads, NY law today (red); fair-housing pass (blue)
- **Spotlight:** The landing page, checked like every other piece of copy.; Place by radius, everyone 18 and over: nobody picked for who they are.

## Step numbers and the success criteria

The records and the success criteria keep their own step numbers; the path's steps map to them:

| On screen | Success criteria |
|---|---|
| 1. The seller signs up | SC1 |
| 2. The AI researches the house | SC1 |
| 3. The seller hires the firm | SC1 |
| 4. The price | SC2 |
| 5. The listing | SC3 |
| 6. On the market | SC4 |
| 7. Enquiries and showings | SC5 |
| 8. The buyer signs up | SC8 |
| 9. The buyer's offer | SC8 |
| 10. The seller decides | SC6 |
| 11. The contract | SC7 |
| The whole sale, start to finish | SC9 |
| One more thing: how the firm finds sellers | SC10 |
