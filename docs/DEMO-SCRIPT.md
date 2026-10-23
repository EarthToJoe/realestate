# Demo walkthrough script

Generated from `app/demo/steps.yaml` by `scripts/gen-demo-script.py`; do not edit by hand (a test fails if
this file and the screens drift apart). Open https://realestate.hughesnode.com (house login), press
**Start demo**, and follow the screens in order. The narration card at the top of each screen says the same.

Built so far: step 1 (Intake), step 2 (Pricing), step 3 (Listing copy), step 4 (Marketing plan), step 5 (Communications), step 6 (Offers), step 9 (Deal timeline). Target length when all ten
steps are built: 13.5 minutes plus a 30-second introduction.

**Colours on every screen:** blue = the AI did it; amber = the seller's or buyer's own decision (the next
step waits for it); red = **NY law today** requires a licensed broker or a lawyer for this act (recorded,
does not stop the flow); grey = a person or third party outside the software. The persona switcher (top
right) changes who is acting: Presenter, Seller or Buyer. Only the client whose decision it is can make it.

## 1. Intake (1.5 min)

### 1.1 Address and facts (`/intake`)

- **Click:** Click "Use demo house", then "Start intake".
- **Say:** The seller types an address and a handful of facts the public record leaves out: parking, condition, roof, taxes, and the four state notice questions. The demo house is a real address in Holmes, so every screen carries the DEMONSTRATION mark; the seller is a fictional person and no owner name is stored.
- **Markers and decisions:** none; the AI sends three notices as soon as the seller submits (CP-24, blue)

### 1.2 Property profile (`/intake/profile`)

- **Click:** Click "Let the AI fill the gaps".
- **Say:** Every fact shows where it came from: green is the public record, amber is what the seller told us, purple is what the AI inferred, with its reason and confidence. The AI fills only facts about the house, never the seller's disclosure answers. The badge says whether this is the AI live or a recorded replay.
- **Markers and decisions:** none

### 1.3 Disclosure checklist (`/intake/disclosures`)

- **Click:** Switch persona to Seller, answer the disclosure questions, click "Submit my answers".
- **Say:** The AI works out which disclosures this house needs from the facts: lead paint is not required because it was built in 1995, and it is not in an agricultural district. The Property Condition Disclosure is the seller's own: the software never pre-fills it. That is an amber "Your decision" card: only the seller can complete it, and contract signing waits for it.
- **Markers and decisions:** CP-04 seller decision (amber, blocks contract signing)

### 1.4 Seller onboarding (`/intake/onboarding`)

- **Click:** As Seller, acknowledge the agency form. As Presenter, click "Let the AI accept the listing". As Seller, sign the listing agreement. (Try signing before acknowledging: the app refuses and says why.)
- **Say:** The AI gives the listing presentation, runs a conflicts check and accepts the listing. The red "NY law today" marker says what the research found: accepting a listing for a fee is a licensed broker's act. It is recorded and counted, and it does not stop the flow. The seller acknowledges the agency form and signs the listing agreement, with the state's exclusive-listing explanation printed on it: those are the seller's own decisions, and nothing is marketed until the agreement is signed.
- **Markers and decisions:** CP-01 and CP-03 seller decisions (amber); CP-02 NY law today (red, licensed broker)

## 2. Pricing (1.5 min)

### 2.1 Comparable sales and adjustments (`/pricing`)

- **Click:** Open "Pricing". Open "Every adjustment, line by line" to show the arithmetic.
- **Say:** Eight real sales from the county's public sales records, all within about four miles. The code, not the model, adjusts each one toward this house: date of sale, size, finished basement, lot, age, rooms, central air and style, at the rates printed on the screen. Sales needing large adjustments or far away are flagged and weigh less. The label says what this is: a comparative market analysis, not an appraisal.
- **Markers and decisions:** none on this screen; the range is computed in code

### 2.2 The AI's advice, net sheet and the seller's price (`/pricing/advice`)

- **Click:** Click "Let the AI recommend a price". Switch persona to Seller and click "Choose this list price". (Try step 3 first: the copy refuses to start until the seller chooses.)
- **Say:** The AI explains the method in plain words, names the weaker sales, and recommends a list price with its reasoning and the net sheet. The red marker is the research: advising a seller on price is the listing agent's fiduciary duty, which New York reserves to a licensed broker. It is recorded and does not stop the flow. The price itself is the seller's decision, and the listing copy waits for it.
- **Markers and decisions:** CP-25 NY law today (red, licensed broker); CP-05 seller decision (amber, blocks step 3)

## 3. Listing copy (2 min)

### 3.1 Drafts and the fair-housing check (`/copy`)

- **Click:** Click "Let the AI write the copy". On the portal description click "Plant a violation (demo)", then "Let the AI apply the fix and re-check", then "Let the AI mark passing copy ready to publish".
- **Say:** The AI writes the MLS remarks, the portal description, three social posts and the flyer, and every piece goes through the fair-housing check: our written rules for every federal and New York protected class and for steering, then a model review for coded language. Plant a violation: "perfect for a young family, steps from the church". It is caught with the rule, the class, the legal basis and a fixed version. The AI applies the fix, the re-check passes, and only then can the AI mark it ready to publish. Marking an ad ready is a broker's act in New York: the red marker.
- **Markers and decisions:** CP-26 fair-housing pass (blue, per piece); CP-06 NY law today (red, per piece)

### 3.2 MLS pre-check and package (`/copy/mls`)

- **Click:** Open "MLS pre-check and package"; open the flyer PDF.
- **Say:** The remarks are checked against OneKey's rules: no contact details or showing instructions, no compensation, never "free". The package lists every field in OneKey order with RESO names. The flyer PDF carries the DEMONSTRATION mark on every page, because the house is a real address and nobody authorised a listing.
- **Markers and decisions:** none on this screen

## 4. Marketing plan (1 min)

### 4.1 Channel board (`/channels`)

- **Click:** As Seller, choose "Publish to Internet" and sign. As Presenter, click "Record the MLS entry (simulated)" and watch the portal and website cards change.
- **Say:** Every card says honestly who does the work. OneKey MLS has no listing-input API, so a licensed MLS participant keys the listing from the AI's package: the grey "human required" marker, linked to the research. Zillow, Realtor.com, Redfin and Homes.com are fed from the MLS, not by us. The firm's own page waits for the MLS entry under the Clear Cooperation rule. The seller signs the exposure choice and the lockbox and photo authorisations: their decision.
- **Markers and decisions:** CP-07 seller decision (amber); CP-08 human required (grey)

## 5. Communications (1.5 min)

### 5.1 Fact sheet, authority and shared inbox (`/inbox`)

- **Click:** As Seller, approve the fact sheet and the AI's authority (allow self-guided tours). Then click "Let all of them arrive" and read the threads; as Seller, answer the two cards under "For the seller to decide".
- **Say:** Nothing leaves until the seller approves the facts and the AI's authority. Then eight simulated enquiries arrive and the AI deals with each on its own: it answers from the approved facts and discloses the oil heat and the septic; it books an owner-hosted showing and a self-guided tour; it refuses to rate schools or the area and points to official sources; it says it can't give legal advice. Only two things reach the seller: a price question and a showing outside the seller's hours. Every message carries the firm's identity block, passed the fair-housing check, and the first one on each thread carries the agency form. Each one that discusses the listing records a red CP-09 marker: in New York today that is a licensed act.
- **Markers and decisions:** CP-27 seller decision (amber); CP-09 and CP-28 NY law today (red); CP-10 human required (grey); CP-24 and CP-29 AI did it (blue)

## 6. Offers (1.5 min)

### 6.1 Offer comparison, advice, decision and negotiation (`/offers`)

- **Click:** Click "Let the AI present the offers and advise". As Seller, counter offer A at the suggested figures. As Presenter, try a counter by hand below the seller's lowest price and watch it refused; then click "Let the AI take the next step" until the offer is agreed.
- **Say:** Two written offers: one from an outside buyer's agent, one from the firm's own buyer. Code builds the comparison and each net sheet; the AI presents every offer and advises, a licensed act in New York today (red CP-11). The seller decides: accept, counter or reject, and how low the AI may go. The AI then negotiates with the buyer's side on its own, each counter a red CP-13 marker. A counter outside the seller's decision is refused by code and goes back to the seller. Nothing is binding until both sign a contract.
- **Markers and decisions:** CP-11, CP-12, CP-13

## 7. Contract (1.5 min) (slice 3)

Not built yet. Coming in slice 3.

Records: CP-32, CP-14, CP-15, CP-33.

## 8. Buyer side (1.5 min) (slice 3)

Not built yet. Coming in slice 3.

Records: CP-30, CP-16, CP-17, CP-31, CP-18.

## 9. Deal timeline (1 min)

### 9.1 Deal timeline and hurdle map (`/timeline`)

- **Click:** Open "Deal timeline" in the step list.
- **Say:** This page is built only from the records the other screens wrote; nothing is drawn by hand. Blue is what the AI did, amber what the seller or buyer decided, red where New York law today requires a licensed broker or a lawyer, grey the people and third parties outside the software. The red marker at the top stands for the whole firm: New York requires a licensed broker of record, and this demonstration has none. The hurdle map below lists every red marker with its rule and a link to the research.
- **Markers and decisions:** every record so far; CP-35 standing; CP-20 to CP-23 and CP-34 planned

## 10. Marketing the business (0.5 min) (slice 4)

Not built yet. Coming in slice 4.

Records: CP-26 automated; CP-19 NY law today.
