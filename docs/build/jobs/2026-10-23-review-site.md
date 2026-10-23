# Build job: the research documents site, fixed for a first-time reader

Date 2026-10-23. Tag BUILD-SITE. Billing: the Max plan.

Runs at the same time as BUILD-PATH, which owns `app/`, `tests/`, `app/demo/` and `docs/DEMO-SCRIPT.md`. **This
job touches only:**
- `scripts/publish_review.py` and its test (`tests/scripts_publish.py`, if it covers the publisher);
- the Markdown documents whose links it fixes.

Commit with `git add <your paths>` only. If git reports `index.lock`, wait a few seconds and retry; never delete
the lock while the other job may be committing.

## Why

Joe asked to "audit the whole website for issues". The findings are in:
- `docs/build/site-audit-2026-10-23.md`, item 9;
- `docs/build/audit-fresh-eyes-2026-10-23.md`, "The research site".

Joe's father-in-law, a New York attorney, will be sent the index link. He has to find the demo, the executive
summary and the memo without help, on a laptop or a phone.

## Do

1. **Broken links: 9 links, 6 targets, all 404s to raw `.md` files.**
   - The publisher rewrites every link to a published document's `.md` into its `.html` page, including links to
     research notes in `research_notes/` that are published. Today it misses relative paths with `../` and `%20`.
   - A link to a file that is not published (`handoff/WS4.md`, `research/handoff/WS7.md`) is either published,
     if Joe would want to read it, or turned into plain text with no link.
   - The publisher also prints a warning, and fails its test, for any link it leaves pointing at a `.md` file.
2. **Dead and malformed outside links.**
   - *Dacey*, 21 N.Y.2d 694 (in the plan; it is load-bearing): find a working public source (the NY Court of
     Appeals or another reliable case-law site) and replace the link. Search; do not guess the URL.
   - OneKey's SkySlope page: replace it with OneKey's current page, if there is one; otherwise mark the link "(page
     since removed)" and keep the citation's date.
   - The two malformed data.ny.gov query links: URL-encode them so they open.
   - Sample about 150 more outside links, one per website, and fix any that are really dead. A 403 from a state
     site is bot-blocking, not a dead link: leave it.
3. **Phone layout.**
   - Wrap every table in a horizontal scroll box. Four research-notes pages scroll sideways today; the worst is WS5
     Hudson Valley market, 823 px wide.
   - Body text at 16 px, and tap targets of at least 44 px (the "← All documents" link included).
   - Put "← All documents" at the bottom of every page as well as the top.
4. **Long pages.** Add a table of contents from the H2 headings at the top of every page longer than about three
   phone screens, as a fold ("On this page"). Each heading gets an anchor.
5. **The index, for a first-time reader:**
   - First, a short "Start here" block with three links, in order:
     1. "Open the demo" (`/`);
     2. "The executive summary";
     3. "The memo on your role" (the father-in-law memo).
   - Keep "Waiting on you" (it is Joe's), but under that heading, with a one-line note that it is Joe's list.
   - The research notes get readable titles taken from each note's H1, not from file names ("mls access").
   - Move the internal pages (UI audits, the build briefs if listed, the spend log) into a last section titled "How
     this was built", below the research.
   - Replace the header's cut-off commit message with "Updated <date, time ET>". The commit hash may stay in small
     text.
   - Explain the WS codes once at the top of the research section: "WS1 to WS6 are the six research workstreams",
     with each one's name.
6. **Check.**
   - Re-run the link check over all published pages: no internal 404, no missing anchor.
   - Screenshot the index, the executive summary, the plan and the WS5 notes page at 390 and 1280 px, using
     Playwright with long timeouts (the server is heavily loaded; one browser at a time).
   - Look at each screenshot, and fix what looks wrong.
   - Commit, and let the hooks republish.
   - Confirm on the live site, with the house login read from `/srv/realestate/secrets/HOUSE_PASSWORD`, never
     written anywhere.

## Rules

- **The repo is public:** no password, key or token in any file, commit or log.
- **Change no research finding, number or claim:** links and layout only.
- **Where a source is replaced,** the claim it supports must still be what the new source says; if not, leave the
  old link marked "(page since removed)".
- Do not touch `app/`, `tests/` other than the publisher's own test, `app/demo/`, or `docs/DEMO-SCRIPT.md`.

## Finish

Final answer, under 200 words:
- the links fixed, and to what;
- the pages that scrolled sideways, now fixed;
- what the index now shows first;
- the last commit.
