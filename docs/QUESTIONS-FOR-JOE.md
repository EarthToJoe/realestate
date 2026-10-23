# Questions for Joe

Answer any of these when you check in, in one line each. Where I could not wait, I made the provisional choice
shown and kept moving; your answer overrides it. Newest at the top of each section.

## Open: these three unblock things

**Q1. Create the GitHub repo. Done 2026-10-23: origin is `github.com/EarthToJoe/realestate`; the VPS clone pulls and pushes there.** Joe answered 2026-10-23: "Use GitHub.
You have my permission." With that, the work is pushed to a temporary branch `realestate-lifeboat` in the
`shorts` repo, and the VPS can start from it. The Claude GitHub app still cannot *create* a repository (the
403 is the app's permission on GitHub, not yours), so the clean fix is still yours: github.com/new, name
`realestate`, owner EarthToJoe, **private**, no README. Then on the VPS, once:
`bash /root/projects/realestate/scripts/repoint-origin.sh`. The lifeboat branch gets deleted after.

**Q2. Start the VPS session. Done 2026-10-23: Joe ran the command; the session is up on the API key.** I cannot reach the VPS from the cloud (no
SSH here; the VPS is only the `ssh vps` alias on your Mac). One command, run once. It clones from the real
repo if it exists, else from the lifeboat branch; checks disk; sets up the always-on session; and asks for
the API key with hidden input (press Enter to accept the default "yes").

From your Mac (the clone reuses the shorts checkout's own GitHub access, so nothing to type):
```bash
ssh -t vps 'd=/root/projects/realestate; [ -f "$d/scripts/vps-setup.sh" ] || git clone -q -b realestate-lifeboat --single-branch "$(git -C /root/projects/shorts remote get-url origin)" "$d"; bash "$d/scripts/vps-setup.sh"'
```
From your phone, with no Mac: open the Hostinger hPanel browser terminal for the VPS (you are root there)
and paste the same command without the `ssh -t vps '...'` wrapper:
```bash
d=/root/projects/realestate; [ -f "$d/scripts/vps-setup.sh" ] || git clone -q -b realestate-lifeboat --single-branch "$(git -C /root/projects/shorts remote get-url origin)" "$d"; bash "$d/scripts/vps-setup.sh"
```
If it says the folder already exists (left over from the earlier attempt), first run `rmdir /root/projects/realestate`
(it only removes an empty folder) and try again.
Have an API key ready first: console.anthropic.com, API keys, Create key (name it `realestate`).
Success: a session named **realestate** in your Claude app, and `/status` there says it uses the API key.
- 2026-10-23: the first version used plain HTTPS and asked for a GitHub login (which GitHub no longer accepts
  anyway); replaced by the command above, which uses the shorts checkout's own remote URL.

**Q3. Billing: answered.** Joe, 2026-10-23: "I want all this setup work to be done using the API credit."
So: the VPS session runs on the key (step 2 above stores it, for that session only; the shorts rule stays
intact), and it takes over the work. The thirteen research passes already running in the cloud are the only
part billed to Max; stopping them would throw away finished work, so they land, get committed, and the VPS
session writes everything from there. Say "continue here" if you would rather I keep going in the cloud on
Max until the VPS session is up.

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

- 2026-10-23: Q4 to Q9 are on Joe's ranked to-do list (https://shorts.hughesnode.com/todo): Q7 sign-off (item 0e39cd), Q4 father-in-law questions (8ba86e), Q5/Q6/Q8/Q9 one-liners (ffd75b).
- 2026-10-23, Joe: created `EarthToJoe/realestate`; origin repointed (Q1 done).

- 2026-10-23, Joe: VPS session `realestate` is up and billed to the API key (Q2, Q3 done).
- 2026-10-23, Joe: "Use GitHub. You have my permission." and "I want all this setup work to be done using the API credit." (see Q1 and Q3).
