# Whole-site audit, 2026-10-23 (evening)

Joe, after clicking through: "looks like the demo doesnt save any of the information when you go back a step. there
is a lot going on, it needs to be made more user friendly and simple, and self explanatory. right now, some of the
features that make it usable and obvious just dont exist. and the user simplicity needs to improve drastically."
Then: "audit the whole website for issues".

**How it was done.**
1. The chat session walked all 20 demo screens on a copy of the app running on the recorded AI answers ($0, the live
   deal untouched). Every screen was screenshotted at laptop (1280 px) and phone (390 px) size, before and after its
   actions, and again when revisited once the sale was done, and every screenshot was looked at. The phone pass
   stopped at screen 15 of 20, because the server was overloaded by other projects.
2. Scripted checks: going back a step (the step list, the browser's Back, and typing then pressing Next), sending a
   form twice, every internal link, and browser errors.
3. The research site: all 37 pages and every internal link and anchor, plus a random 100 of its 1,640 outside links.
4. A separate reviewer, who had not read the earlier audits, walked the site as three first-time users: your
   father-in-law on a laptop, a seller on a phone, and you presenting. Its report is
   `docs/build/audit-fresh-eyes-2026-10-23.md`, and its findings are folded in below where they add something.

## The verdict

The software works. As something a person uses, it doesn't work yet. It is laid out as a set of screens to show,
not a path to walk. A first-time visitor can't tell what to press. The obvious button (**Next**) throws away what
they typed. Every screen asks them to read three layers at once:
- the product: what the AI did;
- the legal record: red, amber and grey cards;
- the demo's own machinery: presenter notes, "View as", fast-forward icons, recorded-run labels.

The last three rounds fixed how the screens look. This round has to fix how the site works: **one path, one button,
nothing lost**. Below, (F) marks a finding the separate reviewer also made.

## 1. Broken: information lost or wrong

1. **Step 1 forgets what was entered.** Once the intake is sent, going back to "Address and facts" by the step
   list, the tab or the back arrow shows an empty form. It is empty even straight after "Do this screen for me",
   which leaves you on the same screen, as if nothing happened (`laptop-01-intake-b`).
2. **Sending step 1 again starts a second sale.** Every send creates a new house and a new deal, and the screens
   always follow the newest deal. Whatever was done in later steps silently disappears from view.
3. **Next never saves.** A laptop screen offers up to six ways forward:
   - the side panel's "Next";
   - the presenter notes' "Next";
   - the step bar's arrow;
   - the screen tabs;
   - the step list;
   - the screen's own "Next" button.

   None of them sends what is on the screen. Type a name into step 1 and press the side panel's "Next", and you land
   on "This screen needs an earlier step first". Go back, and what you typed is gone (`back-typed-then-next`). This
   is what Joe hit.
4. **Nothing can be changed afterwards.** Once the seller has chosen the price, signed, or countered an offer, the
   card shows the decision and nothing else: no "Change" anywhere in the demo.
5. **"Next" buttons disagree.** Each screen hard-codes its own "Next", and three disagree with the walk order:

   | Screen | The screen's own "Next" | The side panel's "Next" |
   |---|---|---|
   | Communications | "Next: offers" | "Next: Buyer intake" |
   | Contract | "Next: the deal timeline" | "Next: The seller's disclosure form" |
   | Who sees the ad | "See the whole sale on the timeline" | backwards |

6. **The progress list is wrong.**
   - Step 1 says "waiting for a decision" for the whole demo. The decision it waits for is the seller's disclosure
     form, which is only needed at the contract.
   - "Deal timeline" shows a done tick from the first screen.
   - The timeline counts itself as a step of the sale ("9 of 10 steps done").
7. **Broken layout.**
   - On the buyer's offer (laptop), the offer's labels break mid-word: "Pric e", "Dep osit", "Fina ncin g", "Con ditio
     ns".
   - Step 1's seller-facts boxes are too narrow to show their contents ("Paved driveway for", "Kitchen updated 2(").
8. **The presenter notes cover the product.** On a laptop they cover the right third of the intake form, including
   the ZIP and phone boxes. On a phone they cover half the screen, and they open on every screen of the guided
   demo.
9. **The research site:**
   - 9 links on 5 pages point to raw note files (`.md`) and fail with "not found": the father-in-law memo (2),
     WS2 legal (4), WS4 cost model (1), the assumptions (1) and one research note (1). All 37 pages load, and every
     anchor resolves.
   - In a random 100 of the 1,640 outside links: 1 is dead (OneKey's SkySlope page), and 2 are malformed
     data.ny.gov query links. 15 refuse automated checks (nysenate.gov, dos.ny.gov, nycourts.gov) but open for a
     person.

## 2. Confusing: what is this, what do I press, what just happened

10. **"Who am I?"** "View as Presenter / Seller / Buyer" is the most prominent control on every screen, and the
    default is the Presenter. As the Presenter, every decision button is greyed out, which looks broken. The way
    forward is "Decide as the seller", decide, then "Back to the Presenter". Seller onboarding alone takes four
    switches, and the demo's 12 client decisions add about two dozen clicks.
11. **Nine orange ⏩ symbols** beside the steps (fast-forward) are never explained.
12. **"Do this screen for me" shows no result.** It leaves you where you were, without saying what changed.
13. **No ending.** The last screen ("Who sees the ad") has no "that was the whole sale" and nowhere obvious to go.
    The step order also ends on marketing the firm, which is not part of the sale.
14. **Leftover jargon and repetition:**
    - "rules FH-RULES 2026-10-23.1" and "7 fair-housing pass records" (copy).
    - "(L12)", "(L39)", "(L29)" (notices).
    - "draft post ready (stub)" and "Buyer 1".
    - "(simulated)" on nearly every line.
    - "Fed from the MLS: fed from the MLS (simulated)", "Vendor booking: vendor booking (simulated)" and "The owner
      hosts: owner hosts (step 5)" on the channel cards.
    - "Recorded on the deal timeline; it does not stop the flow." under every red card.
    - The home page still says the presenter notes are "bottom right"; they moved.
15. **An unexplained outcome.** "Agreed: offer B at $630,000" sits beside "Offer A: $630,000", with no line on
    screen saying why B. The reason is folded away.
16. **A real-looking fake button.** The landing page drafted in step 10 has a "Tell us about your home to begin"
    button that looks real.

## 3. Crowded

17. **The phone spends a third of its screen on chrome.** Four bars (the demonstration strip, the brand, "View as",
    the step bar) plus two rows of screen tabs: the content starts about 310 px down an 844 px screen.
18. **The laptop's side panel is a control room.** It holds:
    - ten steps with nine ⏩ icons;
    - "Guided demo · screen 6 of 20";
    - "Presenter notes", "Next", "Start over" and "People and their data".

    The top bar adds "Recorded run" with its explanation, and "View as".
19. **A five-line footer on every page:** the firm, the office address, the red broker-of-record note, the model
    spend, and links.
20. **Three layers on every screen** (the product, the legal record, the demo's machinery), with nothing to say
    which one a visitor should read.
21. **20 screens in 10 steps,** each step with two to four tabs: a 20-stop route to remember.
22. **Long screens remain:**
    - Communications: 8 threads, 2 decisions and 3 legal cards, about 6,400 px on a phone.
    - The channel board: 13 cards.
    - The pricing advice: its reasoning opens unfolded.

## 4. Missing: what an ordinary web app has and this does not

- Forms that show what was saved, and a **Change** link beside each answer and decision.
- **One Continue button** that saves and moves on, and a **Back** link that keeps what was entered.
- A warning before leaving a form with unsaved typing.
- A **"working…"** state on AI buttons (a live AI answer takes seconds; nothing shows it is working).
- A **confirmation** after each action ("Saved: the AI sent the seller three notices").
- An **honest progress list**: done, you are here, not started.
- **An ending**, and a way to pick up where you left off. The home page's "Continue the current sale" opens the
  property profile, not where you were.
- A short line saying **what each screen is for**, written for the visitor, separate from the presenter's script.

## 5. Also found by the separate reviewer

The reviewer independently confirmed items 1 to 6, 8, 10, 11 and 14 above, and found these besides (details and
screenshots in its report):

- **An off-script figure crashes the demo.** Countering at $640,000 instead of the suggested $635,000 gives an error
  page in developer language ("No recorded answer for buyer.counter_advise…"). The deal then cannot reach the
  contract without starting over.
- **Refreshing after "mark copy ready" shows a raw error:** `{"detail":"Method Not Allowed"}`.
- **"Re-check" quietly un-readies passing copy,** which then blocks step 4, while step 3 still says all six pieces
  are ready.
- **The demo house's answers vanish if you leave the form before sending it.** The grey placeholders that remain
  look like answers, so "Start intake" then fails.
- **"Start demo" greets a first-time visitor with "Start over? This resets the deal".**
- **A dead end in the Seller view on step 4:** the MLS entry button stays greyed out, with no reason given.
- **Decisions made by fast-forward read "Decided by the seller and the buyer"** with a time, and nothing says the
  demo played them. A lawyer would notice.
- **Two clocks:** the recording times sit next to the deal's times.
- **Contradictions:**
  - "adjusted $590,000 to $700,000" beside the $610,000 to $650,000 headline;
  - "needs attention" beside "6 of 6 checks passed";
  - "0 ready to publish";
  - "AI inferred 9" beside "6 facts".
- **Accessibility:** ten unlabelled buttons on the copy screen, chrome text of 12 to 14 px, and phone radio buttons
  of 20 px.
- **The research site:**
  - the index has no link to the demo;
  - four research-notes pages scroll sideways on a phone;
  - long pages (up to about 127 phone screens) have no table of contents;
  - the plan's link for the *Dacey* case is dead;
  - the header shows a cut-off commit message.
- **Also checked in the chat session:** the contract's print view, PDF and Word copy give a server error when no
  sale has started. The contract PDF took more than 30 seconds on the loaded server.

What works: double-clicks make no duplicates; Back after a decision shows the true state; nothing scrolls sideways
in the demo; there are no browser errors outside the two error pages above; and the AI's own work reads as credible.

## What the fix looks like

Two build jobs:

- **The demo:** `docs/build/jobs/2026-10-23-one-path.md` (decisions 47 to 51). One path, about 12 screens, and one
  button on each. Nothing typed or decided is lost, and anything can be changed. You play the seller and the buyer.
  The presenter's tools are off unless you are presenting.
- **The research site:** `docs/build/jobs/2026-10-23-review-site.md`. Links, phone layout, tables of contents, and an
  index that opens on the demo, the executive summary and the memo.

## Fixed (BUILD-PATH, 2026-10-24; decisions 47 to 51)

The demo was rebuilt as one path of 11 steps, a finale and "one more thing" (decision 51's table), with one action
bar per screen. Results of the acceptance run are in `docs/build/e2e-demo-run.md`; screenshots of every screen at 390
and 1280 px are in `docs/build/screens/one-path/`. Finding by finding (this audit, then the separate reviewer's):

**1. Broken**
1. Step 1 forgets: fixed. The form re-opens with what was saved (`intake.saved_input`); a new sale opens with the demo
   house. Tested (`test_step_1_reopens_filled_in…`, the browser back-step test).
2. Sending step 1 again starts a second sale: fixed. The same house and deal are updated; contact details at once, the
   house only after a confirm naming what is redone. Tested (one deal after re-sends; mid-sale name change).
3. Next never saves: fixed. Every other "Next" is gone; the one button saves and moves on; typing then leaving asks
   "Leave without saving?" (`app/static/app.js`). Tested in the browser.
4. Nothing can be changed: fixed. "Change" on every client decision; superseded records, only dependents re-open,
   the change on the timeline. Tested (`test_changing_the_price_…`).
5. "Next" buttons disagree: fixed by construction: the next screen comes from the walk only.
6. The progress list is wrong: fixed. Done ✓ only when every milestone on the step is done; the timeline is the
   finale, not a step; the disclosure form belongs to step 11. Tested (`test_the_progress_list_is_honest`).
7. Broken layout: the offer's terms are a `table.terms` with a minimum label column, stacked on a phone; intake fields
   are at least 220 px wide.
8. The notes cover the product: fixed. Notes only when presenting, in a column that narrows the content (laptop) or a
   bottom sheet that starts closed (phone). Checked in the browser (the notes' left edge is right of the content).
9. The research site: the other job (BUILD-SITE).

**2. Confusing**
10. "Who am I?": View as is in the menu; every decision button names the client and works (decision 49, Q51).
11. ⏩ icons: gone; skip ahead is on the "not yet" card and in the menu, presenting only.
12. "Do this screen for me" shows no result: it now opens with a one-line confirmation of what it played.
13. No ending: the finale, "The whole sale, start to finish", with "Start over", "Read the plan" and "One more thing".
14. Jargon: record codes, L-codes, "(stub)", "Buyer 1", repeated "(simulated)", doubled channel labels and the home
    page's "bottom right" removed from the visitor's layer; "Recorded on the deal timeline…" said once. Tested (no codes
    in the visible text of any screen; `test_the_visitors_layer_…` and the browser run).
15. Why offer B: one line on screen from the recorded advice.
16. The landing page's button: drawn as an inert picture, labelled as the mock's.

**3. Crowded**
17-20. Phone chrome is one line plus one bar (the content starts under 90 px; measured per screen in the run); the
    laptop's side panel holds only the progress list and "Start over"; the footer is one line; the three layers are
    separated (product by default, presenter opt-in). 21. 20 screens → 11 steps. 22. Communications keeps the two
    seller decisions, the thread list (one open) and the messages marker; the other cards are in a fold. The pricing
    advice opens on the recommendation; the reasoning is folded. The channel board is 7 rows.

**4. Missing**: saved forms and Change, one Continue, "Leave without saving?", "The AI is working…", the one-line
confirmation, honest progress, an ending and "Continue where you left off", and the visitor's line on every screen:
all built.

**5. The separate reviewer's findings**
- An off-script figure: in a recorded demo every free figure is the recorded one, with one line saying so; a
  different one is refused in plain words before anything is saved, with "Put the recorded figure back"
  (`app/demo/recorded.py`). Tested for the price.
- Refresh after "mark copy ready": every POST redirects to its screen; a GET to an action's address lands on its
  screen. Tested.
- "Re-check" un-readies passing copy: fixed in `listing_copy.check`; re-check is a presenter's tool.
- The demo house's answers vanish: the form is always pre-filled; no look-alike placeholders.
- "Start" asks to reset on a first visit: fixed. Tested.
- The Seller-view dead end on the MLS entry: the person's step works from any view.
- Decisions played by the demo: marked "(played by the demo)" on the card and the timeline. Tested.
- Two clocks and two counters: deal times only (recording time in the tooltip); "Step n of 11" only.
- Contradictions: the comparables' fold explains the adjusted spread against the range; the MLS headline names what is
  missing; the copy headline never reads "0 ready" as a failure; the profile says "added 6 facts and worked out 3
  more"; onboarding no longer says "four things".
- Pricing jargon: plain words outside the folds.
- Names: "Offer A, from another firm's buyer"; "Offer B, from the firm's own buyer"; "the buyer".
- The negotiation on step 6: the buyer's reply is on step 10, where the path is.
- Accessibility: every button and link has text (the run counts unlabelled ones); chrome text 16 px; radios, folds,
  footer links and the spotlight's buttons at least 44 px.
- Form errors: next to the field, saying what to enter.
- "Plant a violation" and "Try a bolder headline": in the presenter's tools.
- The contract's print view, PDF and DOCX with no sale: the "not yet" card, never a 500. Tested.
- The slow contract PDF: each version's PDF is cached in memory (never on disk: it carries names) and built ahead
  in the background once a draft exists.

**Not fixed, and why**
- The research-site findings belong to BUILD-SITE.
- The browser run screenshots the walk's 12 screens at both widths, not "one more thing" (`/brand`); the live phone
  check covers `/brand` (it passes).
- While the buyer's answers are open for a change (`/buyer?edit=1`), the form carries its own "Save" button beside
  the action bar's button: two primaries on that one state of one screen.
- Every test passes except where noted in PROGRESS; the full suite is about 14 minutes on this server.
