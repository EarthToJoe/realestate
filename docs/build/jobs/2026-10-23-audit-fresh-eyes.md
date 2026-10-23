# Job AUDIT-FRESH: a first-time user's audit of the whole website (2026-10-23)

**This job only looks and writes a report. It changes no app code, no templates, no docs other than its own report,
and does not commit.**

## Why

Joe, after clicking through the demo (2026-10-23): "looks like the demo doesnt save any of the information when you
go back a step. there is a lot going on, it needs to be made more user friendly and simple, and self explanatory.
right now, some of the features that make it usable and obvious just dont exist. and the user simplicity needs to
improve drastically." Then: "audit the whole website for issues".

This is the fourth round of UI complaints. Earlier rounds (`docs/build/ui-audit-2026-10-23.md`) fixed codes, layout
and length screen by screen. **Do not read that audit or the build briefs before you finish your own walk**: the
point of this job is eyes that are not anchored on what the builders thought they fixed. Read them afterwards only
to mark which of your findings are repeats.

## Who you are while you walk

Walk the site three times, as three people, each seeing it for the first time with no one beside them:

1. **Joe's father-in-law**: a New York attorney in his sixties, sharp, not technical, reading on a laptop. Joe will
   send him the link. He has to understand within a minute what this is, what to press, and what he is looking at.
2. **A home seller** in the Hudson Valley who was told "this replaces your agent": does it feel like a product they
   could use? Phone.
3. **Joe presenting it** at a meeting on a laptop, clicking through quickly, sometimes going back a step to show
   something again, sometimes jumping ahead.

## What to do

1. Start the app locally on recorded replays (no key, $0, the live deal untouched): `scripts/phone-check.py` has
   `local_server()`; reuse it from your own Playwright script (`.venv/bin/python`, Chromium is installed). Use 390 x
   844 (phone) and 1280 x 800 (laptop). Put your scripts and screenshots under `tmp/audit-fresh/` (gitignored).
2. Walk the whole demo from the home page as each person, **using only what is on screen** (no reading the code to
   decide what to click). Take a screenshot at every screen and after every action, and **look at each screenshot**.
3. Do the things real users do, and record what happens each time:
   - Go back a step (browser Back, the step bar's arrow, the step list) after filling in or deciding something. Is
     what you entered or decided still there? Can you change it? Does going forward again keep it?
   - Re-submit a form, double-click a button, refresh after a submit, open a step out of order, open a later step
     before an earlier one is done, switch "View as" mid-step, press "Start over".
   - Use the guided demo (Presenter notes, Next, "Do this screen for me", Spotlight) and also ignore it entirely.
   - Wait for anything slow: does the screen say it is working?
4. Also audit the **research documents site** on the live server, read-only: `https://realestate.hughesnode.com/index.html`
   and every page it links to (house login: blank username, password in `/srv/realestate/secrets/HOUSE_PASSWORD`;
   never print or write the password). Every internal link must resolve; check anchors; check a sample of external
   links; look at phone and laptop layout (tables, long lines, navigation back to the index). Do not open the demo
   app on the live server (`/`, `/intake` and the other app routes): Joe may be using it.
5. Collect console errors, failed requests (4xx/5xx), missing assets, pages wider than the viewport, text under 16
   px, tap targets under 44 px, and anything that looks broken, inconsistent or confusing.

## The report

Write `docs/build/audit-fresh-eyes-2026-10-23.md`, plain English (Joe reads on his phone), and nothing else:

- **The verdict in five lines**: is it simple and self-explanatory? What is the single biggest problem?
- **Findings, worst first.** Each: what you did, what you expected, what happened, which person it hurts, the
  screenshot file, and a one-line fix. Group: broken (data lost, errors, dead links), confusing (what is this, what
  do I press, what just happened), crowded (too much on screen), missing (features any ordinary web app has that
  this lacks: e.g. saved state, an edit after submit, a clear next button, progress, confirmation that something
  happened, a loading state, an undo, a way back to where you were).
- **The "back a step" behaviour**, screen by screen, in a table: what is kept, what is lost, what can be edited.
- **The research site**: broken links and layout problems, listed.
- **What a simple version would look like**: your proposal, concretely, for how a first-time visitor should move
  through this demo (how many things per screen, what the one action is, what goes away entirely). The product
  stays the brief's original idea (the AI replaces both agents and drafts the contract; red "NY law today" markers
  stay visible and do not block; the seller and buyer make their own decisions; decision 21). Simplify the
  presentation, not the idea.
- Afterwards, a short list of which findings repeat items already marked fixed in `docs/build/ui-audit-2026-10-23.md`.

Rules: never put the house password or any key in a file, a command line you echo, or the report. Do not commit.
