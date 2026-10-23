# Progress (daily summary, newest first)

## 2026-10-23 (day 1, cloud session)

**Done**
- Project created as its own git repo, with Joe's brief saved verbatim (`docs/BRIEF.md`).
- Twelve research passes launched across the six workstreams; each writes sourced notes to `research_notes/`
  and will be turned into one deliverable per workstream in `docs/research/`.
- Living documents written: success criteria (draft for sign-off), riskiest assumptions with kill criteria,
  decision log, questions for Joe, out-of-scope list, traceability skeleton, spend log.
- One-command VPS setup written (`scripts/vps-setup.sh`), with disk guard and per-session API billing option.

**Blocked or waiting on Joe**
- GitHub repo `EarthToJoe/realestate` must be created by Joe (the Claude GitHub app got a 403 creating it).
  Work is kept on a temporary `lifeboat/realestate` branch in the `shorts` repo meanwhile.
- VPS session needs Joe to run one command (see `QUESTIONS-FOR-JOE.md` Q2).
- Success criteria need sign-off before any POC code.

**Disk**: cannot be checked from here; the setup script checks it first thing on the VPS.

**Next**
- Turn research notes into the six deliverables; write the plan and the executive summary; update the
  assumptions table against the kill criteria; then, with sign-off and WS1 to WS3 in hand, lock the
  architecture and build the POC.
