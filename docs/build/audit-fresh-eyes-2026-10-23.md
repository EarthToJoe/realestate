# Fresh-eyes audit of the whole website, 2026-10-23

Joe asked: "audit the whole website for issues". This audit walked the demo three times, each time as someone seeing
it for the first time:

- **His father-in-law**: a NY attorney in his sixties, on a laptop, alone.
- **A Hudson Valley home seller**: on a phone, told "this replaces your agent".
- **Joe presenting**: on a laptop, clicking fast, going back, jumping ahead.

How it was run:
- The demo ran locally on recorded AI answers: no cost, and the live deal was not touched.
- The research documents site was checked on the live server, read only.
- Screenshots are in `tmp/audit-fresh/shots/` on the VPS, in the folders `fil/`, `seller/`, `joe/`, `end/` and
  `research/`. Each finding names its file.
- The earlier UI audit was read only after the walks, to mark repeats.

Caveat: the server was badly overloaded during the walk (load about 36 on 2 CPUs), so every click took 5 to 30
seconds. **Slowness is not counted against the app.** What is counted is that the screen never says it is working.

Not covered (the walks stopped early to stay within budget):
- The seller's phone walk past step 2.
- Going back and changing a decision in steps 3 to 5, one step at a time.
- The father-in-law's own read of steps 7 to 10.

Steps 8 to 10, re-submitting the intake and Start over were checked in a separate pass on a fast-forwarded deal.

---

## The verdict in five lines

1. **No: it is not simple or self-explanatory.** Each screen's content is good, but the presenter's controls, the
   ten-step list, the codes and three or four "Next" buttons are louder than the content.
2. **The single biggest problem: the demo has no memory a person can see, and no way to change anything.**
   - Go back to step 1 after submitting and you get an empty form with "Start intake" offered again.
   - Press it and the whole finished deal is silently wiped, signed contract included.
   - Every decision is final, with no "change" or "undo".
3. The obvious "Next" skips the screen's actual action and lands on a "NOT YET" card.
4. Nothing says the AI is working, and the step list ticks the wrong steps.
5. The father-in-law would get the headline in ten seconds and be lost within a minute.

---

## Findings, worst first

Who it hurts: **F** = father-in-law, **S** = seller, **J** = Joe presenting.

### Broken (data lost, errors, dead ends)

1. **Re-submitting step 1 silently wipes the finished deal.**
   - Did: fast-forwarded the deal to a signed contract, opened step 1 "Address and facts", pressed "Use the demo
     house", then "Start intake". Nothing on screen says the intake was already done.
   - Expected: either "Intake already done" or a warning.
   - Happened: no warning. The contract step went back to "NOT YET: there is no agreed offer", and the timeline
     went from "9 of 10 steps done" to "1 of 10 steps done".
   - Hurts: J, F, S.
   - Shots: `end/04-contract-full.png` (before), `end/06-resubmit-intake.png`,
     `end/07-contract-after-resubmit.png`.
   - Fix: once intake exists, show it read-only with a "Change" link. Any change that undoes later steps must ask
     first and say what it undoes.
2. **Step 1 forgets everything once it is submitted.** This is exactly Joe's complaint.
   - Did: submitted the intake, signed the listing agreement, then clicked "Address and facts".
   - Expected: my answers, marked done.
   - Happened: an empty form, grey placeholder text, a live "Start intake" button, and no sign the intake happened.
   - Hurts: F, S, J.
   - Shots: `fil/22-intake-after-submit.png`, `seller/20-intake-after-submit.png`.
   - Fix: show the submitted answers with "Done ✓" and "Change".
3. **The demo-house answers vanish before you submit.** Grey placeholders that look like answers are left behind.
   - Did: "Start demo" fills the form in. Then I either left the form and came back, or switched "View as" to Seller.
   - Happened: every box is empty, but the grey placeholders ("146 Route 292", "Holmes", "12531") look exactly like
     filled-in answers. Pressing "Start intake" gives "Please fill out this field".
   - Hurts: F, S.
   - Shots: `fil/04-intake-again.png`, `fil/08-submit-empty.png`, `seller/05-intake-as-seller.png`.
   - Fix: keep a draft (on the server, or in the browser), and drop the look-alike placeholders.
4. **Changing a figure from the script crashes the demo and leaves the deal stuck.**
   - Did: on step 7, countered offer B at $640,000 instead of the suggested $635,000, then "Do this screen for me".
   - Happened: a "Refused" error page (HTTP 503) in developer language: "No recorded answer for
     buyer.counter_advise with these inputs (request 116e19b794e0)". After that the contract step says "There is
     no agreed offer yet". The only way on needs the same missing recording, so the deal can only be restarted.
   - Hurts: J. Any audience question like "what if she asks for more?" ends the demo.
   - Shots: `joe/14-counter-sent.png`, `joe/16-offers-played.png`.
   - Fix: in recorded mode, either lock the figures to the recorded ones (and say so on screen), or fall back to
     the nearest recording. Word the error in plain English with a "Put the suggested figures back" button.
5. **Refresh after "mark copy ready" shows a raw error page.**
   - Did: step 3, "Let the AI mark passing copy ready to publish", then refresh or Back.
   - Happened: a white page that says only `{"detail":"Method Not Allowed"}` (HTTP 405).
   - Hurts: J (refreshing is a reflex), F.
   - Shot: `fil/31-reload-ready-all.png`.
   - Fix: after every form submit, return to the screen's own address.
6. **No decision can be changed or undone.**
   - Covers acknowledge, sign, price, approve, counter, and the rest.
   - Back, refresh and returning later all show the stored decision correctly. But there is no "change" anywhere,
     and no confirmation before signing.
   - The only way to change one figure is "Start over", which wipes the deal.
   - Hurts: J, S.
   - Shots: `fil/19-signed.png`, `joe/11-back-after-counter.png`, `joe/13-offers-revisit.png`.
   - Fix: a "Change this" link on each decision card until a later step depends on it.
7. **The step list shows the wrong progress.**
   - "Deal timeline ✓" is ticked right after the intake.
   - "Intake: waiting for a decision" stays on to the end. The waiting item is the seller's disclosure form,
     which is not on the intake screens.
   - "Offers ✓" is ticked while the negotiation is unfinished and the contract step still refuses to open.
   - Hurts: F, S, J.
   - Shots: `fil/11-after-intake-full.png`, `joe/05-ff-landed.png`, `joe/15-offers-as-buyer.png`.
   - Fix: tick a step only when its last action is done. Never tick the timeline. Name what is waiting.
8. **Step 4 is a dead end in the Seller view.**
   - "Record the MLS entry (simulated)" stays greyed out, with no hint who can press it.
   - In the Seller view, the "NOT YET" cards also lose their fast-forward offer.
   - Hurts: F, S.
   - Shot: `fil/36-mls-entered.png`.
   - Fix: say "The firm does this: switch View as to Presenter", or let it work from any view.
9. **"Re-check" quietly un-readies copy and blocks step 4.**
   - Step 4 then says it is waiting for the remarks to be marked ready, while step 3 still says all 6 are ready.
   - Hurts: J.
   - Shots: `fil/30-copy-auto-3.png`, `fil/35-channels-auto-1.png`.
   - Fix: re-checking passing copy must not change its status, or must say that it did.
10. **"Next: offers →" on step 5 opens step 6, Buyer side.**
    - Shot: `fil/37-inbox.png`.
    - Fix: label it "Next: the buyer side →".

### Confusing (what is this, what do I press, what just happened)

11. **Three or four "Next" buttons per screen, and the most obvious one skips the work.**
    - On step 1 alone there is: the step list's "Next: Property profile →", the notes panel's Next, "Do this screen
      for me", and the form's own "Start intake".
    - The big Next moves on without submitting and lands on "NOT YET: this screen needs an earlier step first",
      while the guided counter still goes up ("screen 2 of 20").
    - Hurts: F, S, J.
    - Shots: `fil/03-after-confirm.png`, `fil/06-next-without-submit.png`, `seller/06-arrow-next-before-submit.png`.
    - Fix: one Next per screen. On a screen with a form, the Next *is* the submit; otherwise it is greyed out with
      the reason until the action is done.
12. **On a first visit, "Start demo" opens "Start over? This resets the deal…".**
    - The first thing a newcomer reads is a warning about deleting something they never made.
    - Hurts: F, S.
    - Shots: `fil/02-start.png`, `seller/03-start-confirm.png`.
    - Fix: no confirm when no deal is in progress.
13. **The presenter's notes cover the content, for everyone.**
    - On a laptop, the panel opens over the right half of the page:
      - step 1: it hides the "press Start intake" hint and a column of fields;
      - step 7: it hides offer B and half the seller's decision and the red marker;
      - step 8: it hides the contract's price, buyer and closing.
    - Joe found it reopens on each new step after it was closed. The seller found that × sticks on the phone.
    - On a phone it covers the bottom half of the screen even in the Seller view, with stage directions ("Say: …",
      "Point at: …").
    - Its "Do" text tells you to press buttons that a fast-forward has already pressed.
    - Hurts: F, S, J.
    - Shots: `fil/03-after-confirm.png`, `joe/02-offers-direct.png`, `end/04-contract-full.png`,
      `seller/04-intake-top.png`.
    - Fix: closed by default, never over the content, hidden in the Seller and Buyer views.
14. **"View as" behaves unpredictably.**
    - "Decide as the seller" silently switches the whole site to the Seller view. After that:
      - the ⏩ buttons and the "Do this screen for me" offers disappear;
      - "Back to the Presenter" appears twice on one screen;
      - the presenter notes stay.
    - Choosing Seller on the home page is thrown away by Start demo, whose confirm says "as the Presenter".
    - Hurts: F, S, J.
    - Shots: `fil/18-ai-accepted.png`, `seller/02-viewas-seller.png`, `seller/04-intake-top.png`.
    - Fix: decide in place with a small "deciding as the seller" label. Keep the chosen view until the person
      changes it.
15. **Codes and statute numbers are on the audience's screen.**
    - Internal codes: L12, L39, L29, L43, CP-01, CP-05, CP-17, F9, F11, "(L24)", FH-RULES 2026-10-23.1.
    - Form numbers and statutes: DOS-1736-f, RPL §462, AML §310, 19 NYCRR 175.25.
    - Record references: "Liber 22026 page 50962", "Record CP-01".
    - Step 3's "NOT YET" card reads "Refused for now: … CP-05 (Seller chooses the list price) is not made yet".
    - An attorney respects a cited statute; nobody respects an internal ID.
    - Hurts: F, S.
    - Shots: `fil/15-onboarding.png`, `fil/25-copy-before.png`, `joe/14-counter-sent.png`.
    - Fix: internal IDs only inside the "Why" folds; statutes only there too.
16. **Jargon and headlines that contradict each other.**
    - Pricing jargon: "Reconciled value", "arm's-length", "The code adjusts each one", "gross/net adjustment". The
      headline range $610k–$650k sits beside "adjusted $590,000 to $700,000" (`fil/23-pricing.png`).
    - "The MLS package needs attention" next to "6 of 6 checks passed" (`fil/32-mls.png`).
    - "The AI wrote 6 pieces of copy; 0 ready to publish" reads as a failure (`fil/30-copy-auto-1.png`).
    - "AI inferred 9" next to "Inferred by the AI: 6 facts" (`fil/13-after-fill-gaps.png`).
    - Hurts: F, S.
17. **Two counters and two clocks.**
    - Counters: "Step 1 of 10" next to "Guided demo · screen 1 of 20", and after a jump they disagree ("Step 3 of
      10" with "screen 7 of 20").
    - Clocks: the AI cards show when the recording was made ("Recorded run, Fri 23 Oct, 6:43 am ET"), next to
      today's decision times ("4:08 pm ET").
    - Hurts: F, J.
    - Fix: one progress line. Show deal times only.
18. **Fast-forward consents on the people's behalf without saying so on the card.**
    - The dual-agency consent and the signatures read "Decided by the seller and the buyer" with a real-looking
      time. The note under the fast-forward button says the demo plays them; the card itself does not.
    - Hurts: F (a lawyer will notice).
    - Fix: mark played decisions "(played by the demo)".
19. **Small confusions.**
    - The home page says the Presenter notes are "bottom right"; they are in the left sidebar on a laptop and in
      the top bar on a phone.
    - The orange ⏩ icons are never explained.
    - Offer A comes from "Prospect B" and offer B from "Buyer 1".
    - The step 7 negotiation continues on step 6 ("Waiting for the buyer's side… (step 6)").
    - A red "Plant a violation (demo)" button sits on every piece of copy.
    - "Use the demo house" still shows when the form already holds the demo house.
    - Onboarding says "Four things happen here" when two are visible.

### Crowded (too much on screen)

20. **The chrome outweighs the content.**
    - Every screen has, around the content:
      - the black DEMONSTRATION strip;
      - a header with the "Recorded run" badge and the three-way View as;
      - the ten-step list with ⏩ buttons;
      - the guided counter, Presenter notes, Next, Start over and "People and their data";
      - the sub-step tabs;
      - a three-line footer with its own red NY LAW TODAY note and a model-spend line ("$0.0000 of the $12 cap").
    - On a 1280 × 800 laptop, step 1's first screen shows one row of form fields (`fil/03-after-confirm.png`).
    - On a phone the header takes about a third of the screen (`seller/04-intake-top.png`).
21. **Long screens on the phone.**
    - Heights: intake form 4,359 px (about 5 screens), disclosure checklist 3,924, price advice 4,565.
    - The price screen's one button sits below a long block of reasoning.
    - On the laptop, the offers screen is 2,240 px holding about ten blocks (`joe/08-advised-full.png`).
    - The marketing plan is 13 cards (`fil/34-channels.png`).
22. **Accessibility.**
    - Ten unlabelled empty buttons on the copy screen, and an empty-text link beside the red note on onboarding.
    - Chrome text is 12–14 px throughout: step numbers, "waiting for a decision", source chips, View as, footer.
    - Tap targets under 44 px:
      - phone: the eight state-question radio buttons (20 × 20) and the footer links (16 px tall);
      - laptop: View as pills, ⏩ buttons, sub-tabs and guide buttons (36 px), "Why…" toggles (32 px), Spotlight
        Back/Next (about 22 px).

### Missing (things any ordinary web app has)

23. **A "working" state.**
    - After "Start intake", "Let the AI fill the gaps", "Let the AI recommend a price", "Let the AI write the copy"
      and "Fast-forward", the screen is unchanged at 0.3 to 1 s: no greyed button, no spinner, no message.
    - Fast-forward took about 50 to 95 s on this overloaded box. "Write the copy" took 25 s.
    - The code does have "The AI is …" messages for three of the buttons, but on replays they never showed. The
      contract's "The AI is drafting" message is wired to a plain form, so it can never show.
    - On a live run every AI action takes real seconds, and Joe would click again.
    - Shots: `fil/10-submitting-0.4s.png`, `fil/12-fill-gaps-0.6s.png`, `seller/23-recommend-0.5s.png`.
24. **Saved drafts.** Anything typed is lost on a view switch or a step-list click. It survives only the browser's
    own Back button.
25. **Edit after submit, and undo.** See items 1, 2 and 6.
26. **A "this step is done" moment.** After a step's last action there is a small "Next: pricing →" link among
    other buttons: no ✓ banner, no one-line summary of what was decided.
27. **Clear form errors.** An empty buyer form returns only "Name, e-mail and the most you would pay are needed."
    above the form, with no field highlighted (`fil/40-buyer-auto-1.png`).
28. **A seller-only path.** Nothing tells a seller "this is the one thing for you to do here".

What worked:
- Double-clicking a submit made no duplicates.
- Refreshing after most submits is safe; step 3's "mark ready" is the exception (item 5).
- Back after a decision shows the true current state.
- "Start over" asks first, and Cancel returns you to where you were.
- No console errors anywhere except the two error pages above.
- Nothing scrolls sideways at 390 or 1280 px.
- The AI's own work (pricing reasoning, copy, inbox replies, contract) reads as credible.

---

## Going "back a step", screen by screen

| Screen | What was done first | Kept on going back | Lost | Can it be changed? |
|---|---|---|---|---|
| 1 Address and facts (before submit) | demo house filled in, then left via the step list or View as | nothing | every pre-filled answer (placeholders remain and look filled) | yes, but must be re-typed |
| 1 Address and facts (before submit) | typed answers, then the → arrow, then the browser's Back | typed answers (the browser's own restore only) | – | yes |
| 1 Address and facts (after submit) | intake submitted | nothing is shown | the whole form looks blank; "Start intake" is offered again | **no; re-submitting silently restarts the whole deal** |
| 1 Property profile | AI filled the gaps | all facts and the AI's fill | – | no way to correct a fact |
| 1 Disclosure checklist | – | the checklist | – | – |
| 1 Seller onboarding | acknowledged, AI accepted, signed | all three decisions, with times | – | no undo or change |
| 2 Pricing | AI recommended $640,000; price chosen | recommendation and price | – | no change of price |
| 3 Listing copy | marked ready, re-checked | copy and status | refresh on "mark ready" gives an error page | "Re-check" silently un-readies a piece |
| 4 Marketing plan | plan signed | the signature | – | no; the MLS button is a dead end in the Seller view |
| 5 Communications | replies approved | approvals | – | no |
| 6 Buyer side | buyer intake, offer | offer and advice | – | no |
| 7 Offers | countered at $640,000 | the counter (Back, refresh, step list, leaving and returning) | – | no edit or undo; the off-script figure stalls the deal |
| 8 Contract | signed by both (fast-forward) | signed state | – | no (correct for a signature) |
| 9 Deal timeline | – | view only | – | – |
| 10 Marketing the business | – | not tested beyond the screen | – | – |

---

## The research site (https://realestate.hughesnode.com/index.html)

Checked: the index and all 36 pages it links to; every internal link and anchor; 30 of about 1,640 outside links
(one per website); layout of all 37 pages on phone and laptop.

**Broken internal links: 9 links, 6 different targets, all "page not found" (404).** They point at raw `.md` files
that the site never publishes; most of those pages do exist as `.html`.

- Father-in-law memo: "WS4 handoff" and "WS4" → `handoff/WS4.md` (not published at all).
- WS2 legal report: "WS5 notes" → the WS5 why-attempts-failed notes `.md`.
- WS2 legal report: "WS3's notes" (twice) and "WS3 notes" → `mls_access.md`.
- WS4 cost model: "WS1 notes" → `transaction_tasks_and_timeline.md`.
- Assumptions: "→ WS7 handoff" → `research/handoff/WS7.md` (not published).
- WS2 licensing research notes: "WS3 mls_access.md, KQ5" → `mls_access.md`.

Fix: the publisher rewrites `.md` links to their `.html` names, and publishes or unlinks the handoff files.

**Anchors:** none broken. Only three pages use in-page links at all.

**Outside links (sample of 30):**
- 21 work.
- **1 is really dead:** the plan's "NY County Lawyers' Ass'n v. Dacey, 21 N.Y.2d 694" link on vlex.com (404).
  The plan leans on that case.
- 8 refused the script (403): nysenate.gov, dos.ny.gov, the two NY courts sites, and three others. These are
  probably bot-blocking, not dead pages. Five of them are in the father-in-law memo, so click each once by hand.
- 21 link to raw `.md` or GitHub files, which open as plain text on a phone.

**Layout problems:**
- **Four research-notes pages scroll sideways on a phone.** Their tables are not in a scroll box. The worst is WS5
  Hudson Valley market (823 px wide, with a 1,227 px table). The others are WS6 pre-listing inspection, WS2 fair
  housing and WS2 licensing.
- **No table of contents on any page.** Phone pages run 28,000 to 107,000 px, up to about 127 screens.
- **"← All documents" appears only at the top of each page, and it is a small tap target.** There is no way back at
  the bottom of a 50-screen page.
- **Small text.** On the phone, most of the text is under 16 px on several pages: out-of-scope 91%, traceability 88%,
  assumptions 76%, index 70%. On the laptop the index descriptions are about 14 px.

**Confusing for a visitor:**
- **The index has no link to the demo.** The father-in-law, sent this link, cannot find the product from it.
- The header shows a cut-off commit message ("End of day 1: … spend (credit at its reserve, $60.66 no").
- The "Waiting on you" cards are written to Joe ("Reply SIGN-OFF in the chat…"). "Demo finish line" opens the
  success-criteria page.
- Research-notes cards are titled like file names ("contracts upl ethics esign", "mls access").
- WS, L, F and KQ codes are unexplained, and some documents are named as code text instead of links.
- The internal UI-audit page and the spend log sit beside the research.
- There is no "start here" reading order beyond the executive-summary card.

Screenshots: `tmp/audit-fresh/shots/research/`. Full notes: `tmp/audit-fresh/notes-research.md`.

---

## What a simple version would look like

The idea stays exactly as it is:
- The AI is the agent on both sides and drafts the contract.
- The seller and the buyer make their own decisions.
- Every red "NY law today" note stays visible and never blocks.

Only the presentation changes.

**1. One door in.** The home page has a single big button, "Watch a house sale from listing to signed contract
(5 minutes)", and three lines of explanation. No reset warning on a first visit. "Start over" lives in a small menu.

**2. One screen = one moment of the sale.** About 12 screens instead of 20 sub-screens behind 10 steps. Each screen
has exactly:
- a one-line headline in plain words: "The AI suggests listing at $640,000";
- the AI's work as one card, with "Show the working" folded underneath;
- at most one decision card ("Dana decides: Choose $640,000 / Pick another price"), with a "Change" link after;
- the red "NY law today" line where it applies: one sentence, with "Why" folded;
- **one** button at the bottom right: "Next: the listing copy →". It is greyed out with the reason ("Dana chooses
  a price first") until the screen's action is done.

**3. Progress is a thin bar, not a menu.** "4 of 12 · Pricing", with ticks that only appear when a screen is
really done. The full step list sits behind a "Jump to…" link, and jumping ahead fast-forwards with a visible
progress message ("Playing intake… pricing… copy…").

**4. Memory and change.**
- Every screen shows what was entered or decided when you come back.
- Every decision has "Change", which says what it will redo ("Changing the price redoes the copy and the plan").
- Typed answers are kept as a draft.
- Re-doing the intake asks first.

**5. Who you are is chosen once.**
- A first visitor is simply watching. When a decision appears, the seller's or buyer's buttons work right there,
  labelled "Dana (the seller) decides".
- "View as" moves to a presenter menu.
- Seller and buyer views hide every presenter control.

**6. The presenter layer is separate.**
- Presenter notes open only from a small "Presenter" link, as a side drawer that pushes the content aside instead
  of covering it, and stay closed until opened.
- "Do this screen for me" and Spotlight live in that drawer.

**7. Goes away entirely from the audience's screen:**
- the ⏩ buttons;
- the "screen n of 20" counter;
- internal codes (L-, CP-, F- numbers, FH-RULES);
- the model-spend line;
- recording times;
- "Plant a violation" (it moves into the presenter drawer);
- the repeated footer marker. It becomes a single line on the timeline screen and a link in the footer.

**8. Always shows it is working.** Any button that calls the AI turns into "The AI is working…" and is greyed out
until the answer arrives.

**9. An off-script figure never crashes the demo.** In recorded mode, decision fields show the recorded figure with
a note, "Recorded demo: try other figures in the live demo". In the live demo, any figure works.

**10. The research site links to the demo** at the top of its index, under the line "Open the demo".

---

## Repeats of items the earlier audit marked fixed

From `docs/build/ui-audit-2026-10-23.md`:

- **Internal codes on the audience's screen** ("fixed" #2 and "leftover codes" in the slice 4 polish): L12, L39,
  CP-01, CP-05, F9, "(L24)" and FH-RULES are still on screen. Findings 15 and 4.
- **The presenter notes cover the content** (slice 4 says "nothing floats over the content"): on a laptop the notes
  panel opens over the page on steps 1, 7, 8 and 9. Finding 13.
- **The profile counts disagree** (slice 4 says fixed): "AI inferred 9" next to "Inferred by the AI: 6 facts", with
  no explanation seen. Finding 16.
- **One primary action per screen** (redesign brief): there are still three or four competing Nexts. Finding 11.
- **Quiet, correct step-list marks** ("fixed" #6): the marks are now quiet but wrong. Finding 7.
- **Long phone screens** (marked "only partly" fixed): intake 4,359 px, price advice 4,565 px, disclosures
  3,924 px. Finding 21.
- **Body text 16 px and tap targets 44 px** ("fixed" #4): chrome text is 12–14 px, phone radios are 20 px, and
  footer links are 16 px tall. Finding 22.
- **Times** ("fixed" #3, every time in ET): the times are ET, but recording times now sit beside deal times.
  Finding 17.
- **Start over "still asks first"** ("fixed" #7): it now also asks on a first visit, through "Start demo". Finding 12.
- **The home page's "Presenter notes, bottom right"**: the notes were moved in slice 4, but the home text was not
  updated. Finding 19.
