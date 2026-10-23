# Questions for Joe

Answer any of these when you check in, in one line each. Where I could not wait, I made the provisional choice
shown and kept moving; your answer overrides it. Newest at the top of each section.

## Open: these three unblock things

**Q1. Create the GitHub repo.** The Claude GitHub app is not allowed to create repositories (it got a 403), so
please make it, exactly as you made `shorts`:
1. Open github.com/new on your phone.
2. Name: `realestate`. Owner: EarthToJoe. **Private.** Leave "Add a README" unticked. Create.
3. Reply "repo made". I push everything there within minutes and delete the temporary copy.
- *Why it matters:* this cloud container is wiped after inactivity. I tried to park the work on a temporary
  branch inside the `shorts` repo, but the session's permission rules block pointing git at another repo (a
  sensible rule, and I did not work around it). So until the repo exists the work lives only in this container.
- *Provisional:* I send you the key documents as files in chat at each milestone, and push everything the
  minute you say "repo made".

**Q2. Start the VPS session.** I cannot reach the VPS from this cloud session (no SSH here; the VPS is only
known as the `ssh vps` alias on your Mac). After Q1, run this once on your Mac:
```bash
ssh -t vps 'git clone https://github.com/EarthToJoe/realestate.git /root/projects/realestate && bash /root/projects/realestate/scripts/vps-setup.sh'
```
It checks disk space first and stops if there is too little, clones next to `shorts`, marks the folder
trusted, adds `realestate` to `rc`, starts `claude-remote@realestate`, and offers to store the API key with
hidden input (see Q3). Success: a session named **realestate** appears in your Claude app.
- *If you are not near the Mac:* you can instead paste this into the existing **shorts** Remote Control chat
  on your phone: "Clone https://github.com/EarthToJoe/realestate.git to /root/projects/realestate and run
  bash /root/projects/realestate/scripts/vps-setup.sh". The key step needs a terminal, so skip it there.
- *If the clone fails for credentials:* the VPS already pulls the private `shorts` repo, so it should work;
  if it does not, tell me the error line.

**Q3. Billing for this project's session.** Your brief says to use the $200 API credit (expires Nov 8) before
Max. The `shorts` rule says never set `ANTHROPIC_API_KEY` where Claude Code reads it. I will honour both: the
key is read **only** by the `realestate` session's own service file, never by a shell profile, never by the
shorts sessions, never pasted into chat. Storing it switches that one session to API billing; removing the
file switches it back. The POC's own model calls use the same key. Confirm with "api billing yes" (or run
step 2 and say yes when asked), or say "keep Max".
- *Provisional:* mechanism ready, **off** until you store the key.
- *Note:* the research running in **this** cloud session bills your Max plan; I cannot point it at the credit
  from here. The VPS session can be.

## Open: shape the plan

**Q4. Your father-in-law's exact status.** Four facts change workstream 2's conclusions:
(a) Does he hold an actual NY real estate **broker** licence (with a licence number), or does he act under
the attorney exemption only? (b) Is he still actively practising law? (c) Is he willing to be the **broker
of record** and the licensed human who approves every checkpoint, at least at launch? (d) Does he expect to
also act as the attorney for either party in deals the brokerage handles? (Early reading: NY ethics
opinions bar being both broker and lawyer in the same deal; WS2 will confirm.) Also: does the old Hudson
Valley entity still exist, and under what name?
- *Provisional:* planning assumes he gets or holds a broker licence, is broker of record, and does **not**
  act as either party's lawyer in brokerage deals.

**Q5. When is the meeting?** Date or rough window. Sets the pace and what gets polished first.
- *Provisional:* research done in the next two days, POC in the following week, polish after.

**Q6. Demo property.** Fictional-but-realistic Hudson Valley house, or a real one he knows (his own, or a
consenting friend's)? A real address he knows makes the demo land harder, but needs the owner's OK.
- *Provisional:* fictional house in a real town, with a one-line switch to a real address later.

**Q7. Sign off the success criteria** in `docs/SUCCESS-CRITERIA.md` (reply `SIGN-OFF` or edits). Building
starts after this and after workstreams 1 to 3 land.

**Q8. Working name.** Any name in mind for the brokerage or product? The brand sits in one configuration
file either way.
- *Provisional:* neutral placeholder in the UI; repo stays `realestate`.

**Q9. Buyer side depth in the first demo.** Full parity with the seller side, or seller flow complete plus
four buyer screens (intake, search, tour request, offer)?
- *Provisional:* seller complete, four buyer screens (that is what the success criteria say).

**Q10. Separate API keys per workstream?** In the Anthropic Console you can create several keys. If you make
one per use (`realestate-session`, `realestate-poc`), the Console's usage page shows spend per key with no
extra work. Optional.
- *Provisional:* one key; the POC logs its own spend per module.

## Answered

(none yet)
