# realestate: AI real estate agent (New York, Hudson Valley first)

- **New session? Read `docs/HANDOVER.md` first**, then `docs/PROGRESS.md` and `docs/QUESTIONS-FOR-JOE.md`.

- **Source of truth:** `docs/BRIEF.md` (Joe's brief, verbatim). Decisions: `docs/DECISIONS.md`. Questions and
  Joe's answers: `docs/QUESTIONS-FOR-JOE.md`. What "done" means: `docs/SUCCESS-CRITERIA.md`. Assumptions and
  kill criteria: `docs/ASSUMPTIONS.md`. Out of scope: `docs/OUT-OF-SCOPE.md`. Traceability: `docs/TRACEABILITY.md`.
- **This is its own project.** Never edit `/root/projects/shorts` or any other project from this session. This
  session is the Remote Control chat "realestate", running in `/root/projects/realestate` on the VPS.
- **Joe reads on his phone:** plain language, fewest numbered steps, exact copy-paste commands. Never ask Joe
  to paste a secret into chat; use `scripts/secret-set.sh NAME` (hidden input, root-only file under
  `/srv/realestate/secrets/`).
- **Disk guard (Joe: the VPS is near its limit; never let the session get stuck).** Run `scripts/disk-check.sh`
  at the start of every session and before any install, build, download or large write. Under 6 GB free:
  warn Joe in `docs/PROGRESS.md` and in your next reply. Under 3 GB: stop anything disk-heavy and tell Joe
  what to free or upgrade. Never reduce the depth or quality of work because of disk; that is Joe's call.
- **Billing (two layers, Joe 2026-10-23: all work on the $200 API credit, expires 2026-11-08).** This chat
  session runs on the claude.ai login because Remote Control (what makes it appear in Joe's app) is disabled
  whenever an API key is in its environment. So the chat session only orchestrates and reviews: **every
  substantial piece of work (writing a deliverable, the plan, the summary, building or testing the POC) is
  launched as a headless job with `bash scripts/api-run.sh --tag WS<n> "<full task prompt>"`**, which bills
  the credit and logs cost per tag to `/srv/realestate/spend.jsonl` (`scripts/spend-summary.sh` makes the
  table for `docs/SPEND-LOG.md`). Several jobs can run at once with `&`. The POC app reads the same key from
  `/srv/realestate/secrets/ANTHROPIC_API_KEY`. Never put `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`,
  `ANTHROPIC_BASE_URL` or `apiKeyHelper` in a shell profile, `~/.claude/settings.json`, `/root/.claude.json`
  or anywhere another session reads. Do not conserve tokens (Joe: thoroughness over cost); do use `/clear`
  between unrelated tasks in this chat.
- **Working practices (from the brief):** success criteria before building; riskiest assumptions first with
  kill criteria reported plainly; every feature traces to a WS1 function and a WS2 constraint; every decision
  logged with reasoning; daily summary in `docs/PROGRESS.md`; questions in `docs/QUESTIONS-FOR-JOE.md` with a
  provisional choice so nothing blocks; explicit out-of-scope; fair-housing checks in every copy pipeline;
  PII handled as a first-class concern (minimise, mark, log access, allow export and delete, keep out of logs).
- **Demo-ability is a design requirement:** each stage is its own visible screen; the AI's work is shown, not
  hidden; every human or licensed step is a visible checkpoint with its reason; a guided demo mode and
  `docs/DEMO-SCRIPT.md` stay in step with the screens.
- **Research rules:** cite sources; label claims [PRIMARY] / [SECONDARY] / [CLAIMED] / [INFERENCE]; date
  facts; never soften a finding. Read public pages normally; never scrape MLSs or portals against their terms;
  never store other people's listing photos or copy.
- **Git:** commit at every milestone with a meaningful message; `git add <paths>`, never `git commit -a`
  blindly; push to `origin main` (GitHub is the sync). Secrets never enter the repo (`.gitignore` covers
  `secrets/`, `*.env`, `*.key`).
- **Spend log:** every milestone, update `docs/SPEND-LOG.md` (the app's own call log plus Console totals).
