# Build job: redesign the demo's screens from the UI audit

Date 2026-10-23. Tag BUILD-UX. Runs after the demo usability fix and before slice 4. Joe, on his phone: "The website
needs an audit. It looks weird, and it is not user friendly." The audit is `docs/build/ui-audit-2026-10-23.md`:
read it first and fix everything in it. The software works; this job makes it look and read like a product a
non-technical audience understands at a glance, on a phone and on a laptop.

## Read first

`docs/build/ui-audit-2026-10-23.md` (the brief); `CLAUDE.md` (demo-ability rules; the public-repo rule); the brief's
"Demo-ability" section in `docs/BRIEF.md`; `docs/SUCCESS-CRITERIA.md`; `docs/specs/poc-architecture.md` sections 3
and 8; `docs/DEMO-SCRIPT.md`; the templates, `app/static/app.css` and the screen routes; what the usability fix job
just built (gate cards, fast-forward, "decide as", the phone step bar).

## Do

1. **Before:** run `uv run --no-project --with playwright python3 scripts/screens.py docs/build/screens/before`
   (after `bash scripts/disk-check.sh`) to capture every screen at 390 px and 1280 px.
2. **Redesign** to the audit's "What good looks like", screen by screen: the outcome first in plain English, one
   primary action, the working folded; presenter notes hidden by default behind a "Presenter notes" button (slice 4's
   guided mode builds on it; keep `docs/DEMO-SCRIPT.md` in step); legible "NY law today" callouts and client-decision
   cards with codes folded; human rendering of people (fictional names on screen; masking stays for model calls and
   logs), labels, Yes/No, consents, Eastern times; phone-first layout with no sideways scrolling, stacked tables,
   44 px tap targets, 16 px text; the long screens tamed (inbox thread list, contract summary plus PDF plus folded
   side-by-side, one-screen timeline summary with the log folded); a calm, consistent look (type scale, one accent
   plus the three meaning colours used only for meaning, spacing, line length); plain chrome (View as segmented
   control, "Recorded run", "Start over" with a confirm, no slice labels, research link in the footer). Keep Bulma
   and the no-build rule (decision 7); vendor any font locally or use the system stack.
3. **Nothing behavioural changes:** every marker, decision, gate, record, refusal and test stays. If a test asserts
   on markup the redesign changes, update the selector, not the behaviour.
4. **After:** redeploy with `scripts/hosting.sh`, run `scripts/live-flow.sh` on the live site, re-run
   `scripts/screens.py docs/build/screens/after`; every page must fit its viewport (the script prints TOO WIDE
   otherwise). Look at the after screenshots yourself and fix what still looks wrong. Commit only the after set
   (small PNGs; delete `before/` once compared). Leave the live deal walked through every built step.
5. Add a short "Fixed" section to the audit file listing what changed per finding, with any finding not fixed and
   why.

## Rules

As in slice 1 (`docs/build/jobs/2026-10-23-slice-1.md`, "Rules"), plus: **the repo is public**; the house login is
read from `/srv/realestate/secrets/HOUSE_PASSWORD` and never written into a file, a commit or a log.

## Finish

Final answer, under 250 words: what changed, before and after page widths and heights for the worst screens, the
tests and live walk, anything not fixed, and the last commit.
