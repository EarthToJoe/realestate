# Build job: demo usability fix (Joe could not get past step 1 on his phone)

Date 2026-10-23. Tag BUILD-FIX. Runs after slice 3, before slice 4. Small and focused: fix how the demo behaves
for a presenter clicking through it on a phone, then stop.

## What Joe hit

Joe, on his phone: "The demo doesn't seem to be working I think. Can't click the numbered form hyperlinks." The
links work, but after **Start demo** resets the deal, every step except Intake answers with a silent 303 back to
`/intake` (no deal yet), and later steps bounce again until earlier client decisions are made, some of which need
the persona switched to Seller, which nothing on screen tells him. To a presenter it looks broken. The chat session
walked the shared deal through steps 1 to 6 with `scripts/live-flow.sh` as a stopgap.

## Do

1. **No silent redirects from a step link, ever.** A step whose prerequisite is missing renders its own page with a
   card: what is missing, on which step, who must do it (AI / seller / buyer), with a button to go there. Keep the
   service-layer gates and their tests exactly as they are; only the screens change.
2. **Fast-forward for the Presenter.** On that card and in the step list, "Fast-forward the demo to here" plays the
   earlier steps with the demo's scripted choices (the same ones `scripts/live-flow.sh` makes, from replays, $0),
   recording every decision as made by the right persona, and opens the step.
3. **Client decisions never dead-end the Presenter.** Where the seller or buyer must decide, the card shows "Decide
   as the seller" (or buyer): one tap switches the persona and returns to the same card; the decision is still
   recorded as the client's. Keep the 403 for the Presenter acting directly, and its test.
4. **Start demo asks first** ("This resets the deal to the beginning") and lands on step 1 with one line telling the
   presenter what to press next.
5. **Phone.** At 390 px wide the step list is reachable from every screen without scrolling past the whole page
   (for example a compact step bar at the top), every button is at least 44 px tall, and nothing scrolls sideways.
6. **Tests:** from a fresh reset, every step link returns 200 with its gate card or its screen (no 303), the
   fast-forward reaches each built step, and the "decide as" switch works. Extend `scripts/live-flow.sh` with a check
   that no step link redirects after a reset. Redeploy with `scripts/hosting.sh`, run the live flow, and **leave
   the live deal walked through every built step** so Joe's links show filled screens. Update `docs/DEMO-SCRIPT.md`
   for the new buttons.

## Rules

As in slice 1 (`docs/build/jobs/2026-10-23-slice-1.md`, "Rules"). Read the existing code and follow its patterns.

## Finish

Final answer, under 200 words: what changed on screen, the tests, the live check, and the last commit.
