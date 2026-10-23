# Decision log

Every architecture and scope decision, with the reasoning, so Joe can explain choices and later sessions do
not relitigate them. Newest at the bottom. Provisional decisions are marked and get confirmed or reversed
with a dated line.

## 2026-10-23

1. **Own repository, sibling of `shorts`.** The project lives in `/home/user/realestate` here and
   `/root/projects/realestate` on the VPS, never inside the `shorts` folder. Reason: different product,
   different rules; the `shorts` CLAUDE.md governs that folder and its five chats. Repo name `realestate` is
   plain and renamable (GitHub keeps redirects).
2. **Research before code.** All six research workstreams run first, in parallel, as twelve focused
   research passes (two for WS1, three for WS2, two for WS3, one for WS4, three for WS5, one for WS6), each
   writing sourced notes with [PRIMARY] / [SECONDARY] / [CLAIMED] / [INFERENCE] labels, then one written
   deliverable per workstream. No POC code until Joe signs off the success criteria and WS1 to WS3 have
   landed (Joe's two rules: success criteria first; research 1 to 3 before locking the architecture).
3. **The cloud session cannot reach the VPS.** This container has no SSH client or key and HTTPS-only egress;
   the VPS is only known as the `ssh vps` alias on Joe's Mac. So the VPS session is created by a one-command
   script Joe runs (`scripts/vps-setup.sh`), modelled on `shorts/scripts/add-phone-session.sh`, and GitHub is
   the sync between the two. Until the GitHub repo exists (the Claude GitHub app may not create repos: 403), the work stays in
   this container; a temporary branch in the `shorts` repo was tried and blocked by the session's permission
   rules (pointing git at another repo), which was respected. Key documents go to Joe as files in chat at each
   milestone until the push is possible.
4. **API billing is per session, by service file only.** Joe wants the $200 API credit used first; the
   `shorts` rule forbids the API key anywhere Claude Code reads it. Resolution: the key, if Joe stores it, is
   written to `/srv/realestate/secrets/claude-code.env` (root, 0600) and read only through a systemd drop-in
   for `claude-remote@realestate`. No shell profile, no global Claude settings, no other session sees it.
   Off until Joe stores the key.
5. **Checkpoints are first-class.** Every human or licensed step in the product is a stored record (who must
   act, the legal or practical reason, the decision). The deal timeline and the human-in-the-loop map are
   generated from these records. Reason: the brief demands that every hurdle be visible in the demo; a hand-
   drawn map would drift from the software.
6. **Fictional demo data.** The demo house and people are invented (a real town, an invented address) unless
   Joe supplies a consenting real property. Reason: PII and courtesy; also lets the demo be shown to anyone.
7. **Provisional stack (to confirm after WS1 to WS3):** Python 3.12, FastAPI, Jinja2 templates with HTMX for
   interactivity, SQLite, the official Anthropic SDK, no JavaScript build toolchain. Reasons: the VPS is
   2 vCPU, 8 GB and short on disk, and already runs Python tooling (`uv`) for `shorts`; server-rendered
   screens are the clearest way to show each step and each AI action; Python modules map cleanly onto the
   modular architecture the brief asks for. React or a Node toolchain would cost disk and build complexity
   for little demo gain. Revisit only if the research changes the shape of the product.
8. **Spend tracking in two layers.** The POC logs every model call (module, tokens, cost) to a local file and
   rolls it up into `docs/SPEND-LOG.md`; session-level spend comes from the Anthropic Console per key. The
   research done in this cloud session runs on Joe's Max plan and cannot be charged to the credit from here.
9. **Disk is a hard guard, not a reason to do less.** The setup script refuses to install with under 3 GB
   free and warns under 6 GB; the session checks `df` at start and before any install (`scripts/disk-check.sh`)
   and warns Joe in `PROGRESS.md` and directly. Depth of work is never reduced for disk; Joe frees space or
   upgrades.
10. **The VPS session does the work; the cloud session only bootstraps.** Joe (2026-10-23): all of this
    project's work is to run on the API credit. The cloud session cannot be billed to it, so after the in-
    flight research notes land and are pushed, the writing, planning and building move to the VPS session,
    which runs on the key. `docs/HANDOVER.md` is the baton. The cloud session resumes only if Joe says so.
11. **Lifeboat branch, with permission.** Joe allowed GitHub use; the work is pushed to `realestate-lifeboat`
    in the `shorts` repo (the app cannot create repos). It is a parking spot, not a home: `scripts/repoint-
    origin.sh` moves the VPS clone to `EarthToJoe/realestate` once Joe creates it, and the branch is deleted.
12. **Chat session on claude.ai, heavy work on the API key (2026-10-23, evening).** Joe's two wishes, reach
    the session from the Claude app and bill the credit, collide inside one process: Claude Code disables
    Remote Control while `ANTHROPIC_API_KEY` is set (observed on the VPS: "claude.ai connectors are disabled").
    Resolution: the interactive session runs on the claude.ai login (`scripts/session-billing.sh off`) and
    launches headless jobs with `scripts/api-run.sh`, each billed to the key and cost-logged per workstream
    tag; the POC app bills the key directly. The chat's own orchestration is the only Max usage.
