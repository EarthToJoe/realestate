# Demo walkthrough script

Generated from `app/demo/steps.yaml` by `scripts/gen-demo-script.py`; do not edit by hand (a test fails if
this file and the screens drift apart). Open https://realestate.hughesnode.com (house login), press
**Start demo**, and follow the screens in order. The narration card at the top of each screen says the same.

Built so far: step 1 (Intake), step 9 (Deal timeline). Target length when all ten
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

## 2. Pricing (1.5 min) (slice 2)

Not built yet. Coming in slice 2: comparable sales, the method in plain words, the AI's recommended price and the seller's choice. Until the seller signs the listing agreement, this step refuses to start.

Records: CP-25 NY law today; CP-05 seller decision.

## 3. Listing copy (2 min) (slice 2)

Not built yet. Coming in slice 2 with the fair-housing checker.

Records: CP-26 automated; CP-06 NY law today.

## 4. Marketing plan (1 min) (slice 2)

Not built yet. Coming in slice 2.

Records: CP-07 seller decision; CP-08 human required.

## 5. Communications (1.5 min) (slice 3)

Not built yet. Coming in slice 3.

Records: CP-27, CP-09, CP-10, CP-28, CP-29.

## 6. Offers (1.5 min) (slice 3)

Not built yet. Coming in slice 3.

Records: CP-11, CP-12, CP-13.

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
