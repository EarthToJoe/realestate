# End-to-end demo run (slice 4)

Written by `scripts/e2e-demo.py`: headless Chromium plays the guided demo from the home page on a local
app in replay mode with **no API key**, so any AI answer that is not recorded would fail the run. On
every screen, in walk order, it opens the screen from the narration card's Next, taps "Do this screen
for me" where the screen has taps, checks for gate cards, unrecorded answers and sideways scrolling, and
screenshots what the audience sees (`docs/build/screens/slice4/`).

**Problems found: 0.**

- phone: 20 screens walked, click path 40.5 s (the machine's time: replays answer at once)
- laptop: 20 screens walked, click path 34.4 s (the machine's time: replays answer at once)

## How long the demo takes with the narration

- Talk: 8.3 min (1175 words of narration plus the introduction, at 150 words a minute)
- Taps: 45 named buttons in the script at about 4 s each: 3.0 min
- Looking: 20 screens at about 10 s each before the words start: 3.3 min
- **Estimated run: 14.6 minutes** (SC11: 12 to 15). Targets in steps.yaml add up to 14.5 minutes.

The pace figures are stated assumptions [INFERENCE]; a rehearsal with a person timing it is the
real test. If a rehearsal runs long, trim in this order: skip the MLS package screen (3.2, about 30 s),
the search screen (6.2, 25 s) and the disclosure form (8.2, 25 s), whose points the next screens repeat.

## Per screen (phone run)

| # | Step | Screen | Words | Taps | Page height (px) |
|---|---|---|---|---|---|
| 1 | 1. Intake | Address and facts | 66 | 2 | 3863 |
| 2 | 1. Intake | Property profile | 54 | 1 | 4282 |
| 3 | 1. Intake | Disclosure checklist | 60 | 0 | 4040 |
| 4 | 1. Intake | Seller onboarding | 68 | 3 | 3297 |
| 5 | 2. Pricing | Comparable sales | 59 | 1 | 2531 |
| 6 | 2. Pricing | The AI's price advice | 54 | 3 | 4549 |
| 7 | 3. Listing copy | Drafts and the fair-housing check | 72 | 4 | 3414 |
| 8 | 3. Listing copy | MLS pre-check and package | 41 | 0 | 2527 |
| 9 | 4. Marketing plan | Channel board | 59 | 3 | 4472 |
| 10 | 5. Communications | Fact sheet, authority and inbox | 71 | 2 | 6374 |
| 11 | 6. Buyer side | Buyer intake | 61 | 3 | 2612 |
| 12 | 6. Buyer side | Search and alerts | 35 | 1 | 4506 |
| 13 | 6. Buyer side | Tour and dual-agency consent | 57 | 3 | 2702 |
| 14 | 6. Buyer side | The buyer's offer | 56 | 2 | 4289 |
| 15 | 7. Offers | Offers, advice and negotiation | 68 | 4 | 3733 |
| 16 | 8. Contract | Contract draft and signing | 66 | 2 | 4247 |
| 17 | 8. Contract | The seller's disclosure form | 31 | 2 | 2360 |
| 18 | 9. Deal timeline | Deal timeline and hurdle map | 71 | 2 | 4265 |
| 19 | 10. Marketing the business | The firm's campaign | 69 | 3 | 4012 |
| 20 | 10. Marketing the business | Who sees the ad | 57 | 4 | 2893 |
