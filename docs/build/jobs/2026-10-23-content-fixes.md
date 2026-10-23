# Build job: two content fixes found in the chat session's review of slice 4

Date 2026-10-23. Tag BUILD-POLISH. Small and focused; stop when both are done, tested, re-recorded and live.

1. **The firm's fees disagree with the plan.** `config/brokerage.yaml` says "$4,995 flat listing fee" and "$4,995 flat
   buyer-representation fee"; the executive summary, the plan and WS4 use **$4,500 for the seller side and $3,500 for
   the buyer side** (WS4's working fees, paid at closing on the broker-only route). The father-in-law will read both,
   so the demo must match the documents. Set the config to WS4's figures (keep "demonstration figure" and "fees are
   not set by law and are negotiable"), then follow every use: the pricing net sheet, the offers net sheets, the
   intake services card, the buyer agreement, the business campaign (step 10), the fakes and any test that asserts a
   figure. Re-record every replay whose request changes (live calls only for those; say what they cost) so the hosted
   demo still runs at $0, and check the AI's recorded texts no longer say $4,995 anywhere (`grep -r 4,995`).
2. **"[Founder's name]" reads as a bug on the landing page.** Keep Q49's rule (no real person named without consent),
   but render the placeholder as a deliberate, styled fill-in chip ("Founder's name", dotted outline, with a title
   tooltip "Named once the founder agrees; see Q49"), never as bracketed plain text, on screen and in any PDF.

Then: tests pass, redeploy with `scripts/hosting.sh`, `scripts/live-flow.sh` passes, re-shoot only the affected screens
into `docs/build/screens/slice4/` and look at them, leave the live deal reset to the start (as slice 4 left it).
Rules as in `docs/build/jobs/2026-10-23-slice-1.md`; the repo is public (house login from
`/srv/realestate/secrets/HOUSE_PASSWORD` only). Final answer under 150 words with the last commit.
