# End-to-end run of the one path (BUILD-PATH)

Written by `scripts/e2e-demo.py`: headless Chromium on a local app in replay mode with **no API key**
(an AI answer that is not recorded would fail the run), laptop 1280 x 800 and phone 390 x 844.
Screenshots of every screen: `docs/build/screens/one-path/`.

**Problems found: 0.**

## 1. The one-button walk

- laptop: **29 presses** from Start to the finale (target 30 or fewer), 12 screens, 106.0 s on this machine.
- phone: **29 presses** from Start to the finale (target 30 or fewer), 12 screens, 91.4 s on this machine.

## 2. Back, change and unsaved typing (laptop)

- On every screen, Back showed the previous screen as it was left, the button again duplicated nothing,
  and the browser's Back and forward returned the same page (any exception is listed above).
- Mid-sale: the seller's name changed on step 1 after the offers: {'ok': True, 'before': {'deals': 1, 'records': 67, 'messages': 20, 'offers': 2}, 'after': {'deals': 1, 'records': 67, 'messages': 20, 'offers': 2}}; the
  new name on the contract: True.
- Changing the price after the copy exists, the confirm says: "Change the list price?

Changing the list price re-opens the listing copy (step 5), the copy marked ready (step 5), the marketing plan (step 6), the MLS entry (step 6), what the AI may say (step 7), the enquiries and the AI's replies (step "
- Typing then pressing a step: ['Leave without saving? What you typed on this screen is not saved yet.']

## 3. Crowding, measured on every screen (outside folds; the menu closed)

| Screen | Primary buttons (laptop) | Other buttons (laptop) | Chrome above content (phone, px) | Page height (phone, px) |
|---|---|---|---|---|
| `/intake` | 1 | 0 | 80 | 3111 |
| `/intake/profile` | 1 | 0 | 80 | 3280 |
| `/intake/onboarding` | 1 | 1 | 80 | 1445 |
| `/pricing` | 1 | 0 | 80 | 2010 |
| `/copy` | 1 | 0 | 80 | 2174 |
| `/channels` | 1 | 1 | 80 | 3038 |
| `/inbox` | 1 | 1 | 80 | 1382 |
| `/buyer` | 1 | 0 | 80 | 2456 |
| `/buyer/offer` | 1 | 1 | 80 | 4320 |
| `/offers` | 1 | 2 | 80 | 3179 |
| `/contract` | 1 | 0 | 80 | 2713 |
| `/timeline` | 1 | 0 | 80 | 2239 |
