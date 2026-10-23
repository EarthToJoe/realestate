# Questions for Joe

Answer any of these when you check in, in one line each. Where I could not wait, I made the provisional choice
shown and kept moving; your answer overrides it. Readable at https://realestate.hughesnode.com/docs-questions-for-joe.html

## Open

**Q11. Two facts about your father-in-law, now that he lives outside New York** (raised by Joe's 2026-10-23
answer to Q4). (a) **Where does he live now?** A New York broker must "have and maintain a definite place of
business within this state" with a sign readable from the sidewalk (RPL 441-a(3)), and must supervise the
firm's work; both are harder from out of state. (b) **Is his New York attorney registration current?** NY
lawyers re-register every two years even when they live elsewhere. DOS grants the broker licence with no
course and no exam only to "an Attorney who is currently admitted to the New York State bar"; if his status
lapsed or he registered as retired, that route may need fixing first.
- *Provisional:* he lives outside NY, his registration is current or can be made current, and the firm rents
  a small licensed office in the Hudson Valley. The research on his roles will cover both questions.

## Answered (newest first)

- **2026-10-23, Joe, Q7 (sign-off):** "i sign off". The success criteria are the finish line; the build starts
  as soon as workstreams 1 to 3 land.
- **2026-10-23, Joe, Q12 (Virginia house, New York product):** "thats fine" to the provisional: use 4910 John
  Ticer Dr, Alexandria, VA as given, with every legal step labelled "New York rules (launch market)". Not yet
  answered: whether it is Joe's own house; assumed the OK to use it is his, since he chose it.

- **2026-10-23, Joe, Q4 (father-in-law's status):** (a) broker licence or attorney exemption: "Not sure what
  this means. Perhaps not important at this juncture. He hasn't lived or worked in NY for almost 10 years. He
  passed his bar in NY and worked there a while." (b) practising law: "Not directly." (c) willing to be broker
  of record and approve every checkpoint: "Yes." (d) also act as attorney for either party in brokerage deals:
  "Yes, if possible. I'm happy to inform him of the implications, risks, or contrary tos." Old Hudson Valley
  entity: "No." **What changes:** (a) explained in the chat: he can get a NY broker licence on paper for $185
  with no course or exam, as an admitted NY attorney, so it is easy, but it raises Q11. (d) conflicts with the
  early research (NY bar ethics opinions bar being both broker and lawyer in one deal; the narrow exception is a
  fixed fee with written consent), so a plain memo on what he can and cannot do follows the WS2 deliverable,
  for Joe to share with him. Ten years away also weakens the "he knows everybody up there" premise behind A5;
  the assumptions update will say so.
- **2026-10-23, Joe, Q5 (meeting):** "Week from now let's call it." So about 2026-10-30. Pace: research and
  plan this weekend, build 2026-10-25 to 10-28, Joe's click-through on hughesnode 10-28, polish 10-29.
- **2026-10-23, Joe, Q6 (demo property):** "Use 4910 John Ticer Dr, Alexandria, VA." Follow-up in Q12.
- **2026-10-23, Joe, Q8 (name):** "Not yet." Neutral placeholder in one configuration file.
- **2026-10-23, Joe, Q9 (buyer depth):** seller flow complete plus four buyer screens: "Sounds good for now."
- **2026-10-23, Joe, Q10 (separate API keys):** "No." One key; the POC logs its own spend per module.
- 2026-10-23: Q4 to Q9 were put on Joe's ranked to-do list (https://shorts.hughesnode.com/todo).
- 2026-10-23, Joe: created `EarthToJoe/realestate`; origin repointed (Q1 done).
- 2026-10-23, Joe: VPS session `realestate` is up and billed to the API key (Q2, Q3 done).
- 2026-10-23, Joe: "Use GitHub. You have my permission." and "I want all this setup work to be done using the API credit." (see Q1 and Q3).

### Setup questions (all done; kept for the record)

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
