# Questions for Joe

Answer any of these when you check in, in one line each. Where I could not wait, I made the provisional choice
shown and kept moving; your answer overrides it. Readable at https://realestate.hughesnode.com/docs-questions-for-joe.html

## Open

> **Start here (updated 2026-10-23 morning).** Every question below has a default that holds until you answer.
> - **Answered this morning:** Q26 (credit first, then Max), Q19 and Q24 (the original idea: the software replaces
>   both agents and drafts the contract). The plan, summary and questions for your father-in-law are being
>   rewritten around the original idea today.
> - **Quick confirms for the demo, defaults hold if you say nothing:** Q25 recorded replay at the meeting with a
>   live switch; Q43 free inspection stays as the research recommends.
> - **After the meeting:** everything else (fee model, counties, marketing, lockboxes, inspection pilot, scope).

**Q11. Two facts about your father-in-law, now that he lives outside New York** (raised by Joe's 2026-10-23
answer to Q4). (a) **Where does he live now?** A New York broker must "have and maintain a definite place of
business within this state" with a sign readable from the sidewalk (RPL 441-a(3)), and must supervise the
firm's work; both are harder from out of state. (b) **Is his New York attorney registration current?** NY
lawyers re-register every two years even when they live elsewhere. DOS grants the broker licence with no
course and no exam only to "an Attorney who is currently admitted to the New York State bar"; if his status
lapsed or he registered as retired, that route may need fixing first.
- *Provisional:* he lives outside NY, his registration is current or can be made current, and the firm rents
  a small licensed office in the Hudson Valley. The research on his roles will cover both questions.

### From the research (added 2026-10-23, Q13 to Q42)

Gathered from the seven research handoffs and the architecture spec, duplicates merged. **(FIL)** marks a question
only your father-in-law can answer; take those to the meeting. Each has the choice I am using until you answer, and
what the answer unblocks. Q13 to Q18 matter most: they are Phase 0 in `docs/PLAN.md`.

**Q13 (FIL). Who are the first ten sellers he could call this month?** Names, not categories: estates, divorces,
relocations, owners selling to someone they know. *Provisional:* treat his network as unproven; he calls them over
30 to 60 days after the meeting; if fewer than three would list with the firm in the next year, re-plan around a
local partner broker before building past the demo. *Unblocks:* A12 (now the top risk), A5, K2, and whether the
build goes past the demo. (WS5)

**Q14 (FIL). Will he take the New York broker licence and be broker of record of an LLC you co-own, and join HGAR
as a REALTOR so the firm can use OneKey MLS?** Licence: paper form DOS-0036-f-a, $185 for two years, no course or
exam for an admitted attorney. HGAR: about $606 a year plus $100, with the NAR Code of Ethics. *Provisional:* yes to
all. *Unblocks:* the entity, MLS access and every portal (K9), every licensed checkpoint in the product. (WS2, WS3,
WS7)

**Q15 (FIL). Broker only, or also the seller's lawyer on some listings?** Broker only is simplest. Being the
seller's lawyer too is allowed only where the brokerage fee is fixed, non-refundable and owed whether or not the
house sells, with the seller's written consent, his legal fee billed by his own law practice, never the buyer's
lawyer, and only after written ethics advice (Ops. 1015, 1117). *Provisional:* broker only; the fixed-fee "legal plus
listing" package shown as a later option. *Unblocks:* the pricing screen, the contract hand-off, his insurance and
registration needs. (WS2, memo, fact-check)

**Q16 (FIL). Will he, or a trusted local licensee, be in the Hudson Valley for listing appointments, and what New
York office will the firm use?** Builds on Q11. The firm needs a New York office with a sign readable from the
sidewalk; a licensed home office is allowed; NYSBA Op. 1015 favours keeping it separate from any law office.
*Provisional:* yes to presence; a small licensed office or licensed home office in the Hudson Valley; ask DOS whether
a shared or co-working office qualifies. *Unblocks:* A13, the brand story, the office line ($0 or $5,500 to $13,200 a
year). (WS5, WS4, memo)

**Q17 (FIL). How many hours a week can he give as broker of record?** *Provisional:* 10 to 15, which caps the
firm at about 35 to 50 closings a year at 15 hours a side, plus 80 to 125 hours before launch (mostly legal set-up).
*Unblocks:* the capacity plan and the hiring trigger (A1). (WS4, memo)

**Q18 (FIL). At launch, will he personally negotiate every offer, and who takes buyers on tours?** Tours: (a) him,
(b) a licensed salesperson he sponsors and the firm pays, or (c) no buyer tours at launch. *Provisional:* he
negotiates every offer; tours (a) at launch, (b) once volume outgrows his hours; on the firm's own listings, sellers
host showings and open houses themselves. *Unblocks:* the offer and tour checkpoints, broker hours in the cost model.
(WS1)

**Q20. Fee model.** *Provisional:* a flat $4,500 seller-side fee with optional add-ons; a $3,500 buyer-side fee with
any surplus seller-offered compensation rebated to the buyer; never a document fee. Local anchors: NY Flat Fee Realty
1%, Hauseit 1% with a $7,500 minimum, 845 Realty Guys $9,995, Redfin 2% with a $6,000 minimum. Confirm after the ten
calls. *Unblocks:* the pricing screen, savings calculator, the plan's revenue line. (WS4, WS5)

**Q21. Default buyer-agent pay on the firm's listings?** *Provisional:* the seller chooses, with the firm
recommending a market rate (about 2% to 2.5%) and showing the steering evidence; never silently 0%. *Unblocks:* the
listing intake screen; exposure to K1 and K6. (WS5)

**Q22. When the firm's seller meets the firm's buyer: dual agency with written consent, or represent the seller
only?** *Provisional:* represent the seller only on the firm's own listings; offer the buyer an outside agent or the
unrepresented path with the agency form; dual agency only with written informed consent and never marketed as "full
representation of both sides". *Unblocks:* the consent screens and the "both sides" wording. (WS1)

**Q23 (FIL). Contract step: hand off to independent lawyers, and which purchase form does he use?** Options for the
form: NYSAR's statewide purchase agreement, the bar association's Residential Contract of Sale, or his own.
*Provisional:* the firm stops at the accepted-offer memo and hands off, with a directory of local attorneys who
publish flat fees (no referral payments either way); the demo mirrors the bar-association long form's section
structure in its own words. *Unblocks:* the contract screens. (WS2, WS7, architecture §11)

**Q25. At the meeting: recorded replay by default, with a live switch?** *Provisional:* yes; replay recorded the day
before and labelled, live only if the room has good internet; map with an offline fallback; the app also runs on a
laptop with one command. Does the room have reliable internet? *Unblocks:* demo-mode design. (architecture §11, WS7)

**Q27 (FIL). Will he ask his malpractice carrier, in writing, whether claims connected with a brokerage he co-owns
are excluded and could affect his legal cover?** *Provisional:* assume no cover from that policy; the brokerage buys
its own E&O ($708 to $1,500 a year) and asks its carrier in writing whether a brokerage-funded inspection pilot is
covered. *Unblocks:* the insurance line, his personal risk decision, the inspection pilot (A17). (WS2, WS4, WS6,
memo)

**Q28 (FIL). Confirm today's closing customs in his counties.** Who drafts, usual deposit, mortgage-commitment
period, whether brokers attend closings. The bar association's county sheets are from 2018 to 2020. *Provisional:*
use those sheets. A 15-minute conversation. *Unblocks:* timeline defaults and the contract step. (WS1)

**Q29 (FIL). Send DOS one written inquiry, signed by him as the licensee?** Questions: may software perform tasks
under a broker's supervision; are unaccompanied or unlicensed showings of homes for sale licensed acts; does an
out-of-state broker of record with a small New York office meet the rules; does a shared or co-working office
qualify; is Joe's passive ownership acceptable; how does DOS view brokerage-paid, seller-engaged pre-listing
inspections. Phone first: DOS Division of Licensing Services, (518) 474-4429. *Provisional:* I draft it; he sends it
after the meeting. *Unblocks:* the largest remaining legal unknowns (A1, A2, A13). (WS1, WS2, WS6, memo)

**Q30 (FIL). Was his old business "Hudson Valley Partners Inc." (Rockland, filed 1995), or what was its exact
name?** *Provisional:* unrelated; avoid "Hudson Valley Real Estate" (two licensed firms use it). *Unblocks:* naming
and any reputational history check. (WS5)

**Q31. Are you content to be paid only through ownership distributions, a salary for clerical work, and a fixed
software licence fee, never per deal, and to treat the software build as your own risk capital?** *Provisional:*
yes to both. *Unblocks:* the business-model section of the plan and how K7 is presented. (WS2, WS4)

**Q32. Launch counties.** *Provisional:* OneKey's five (Dutchess, Orange, Putnam, Rockland, Sullivan, plus Ulster
homes entered there); join the northern MLS (HVCRR, 845-338-5299) when the first Columbia or Greene listing signs.
*Unblocks:* the MLS budget and the demo's county list. (WS3, WS4)

**Q33 (FIL). Who keys listings into the MLS at launch?** Him, or an hourly assistant registered as an
"Administrative User" (not you while you co-own the firm and are paid by results). *Provisional:* him for the first
listings, an hourly assistant later. *Unblocks:* broker hours and checkpoint role labels. (WS3)

**Q34. Paid marketing.** *Provisional:* referral-only for the first 12 months; brand spending at most $1,000 a
month; no per-lead buying; no paid portal extras (Zillow Showcase, Homes.com membership) at launch. *Unblocks:* the
K2 guardrail and the marketing budget. (WS4, WS3)

**Q35. Coordination.** *Provisional:* you and the software coordinate until about 15 closings, then a part-time
coordinator (about $24,000 a year with employer costs); you are paid hourly or by salary for this, never per deal.
*Unblocks:* the realistic-case budget. (WS4)

**Q36 (FIL). Lockboxes: SentriLock ($130 a year plus $110 per box) or him attending showings?** *Provisional:*
subscribe once buyer-side touring starts. *Unblocks:* showing design. (WS3)

**Q37 (FIL). Free inspection: drop the "buyers won't need their own inspection" pitch and run a capped pilot
instead?** *Provisional:* dropped; new line "you'll know what a buyer's inspector will find before they do, and you
decide what to fix". Pilot on the first 10 listings, cap $1,500 a listing (about $10,000 in all), the seller as the
inspector's client, owed whether or not the house sells. The demo shows this design, with an inspection credit and a
list of three licensed inspectors for sellers who decline. *Unblocks:* the inspection screens, the pilot budget. (WS6,
WS4)

**Q38 (FIL). The inspector friend: name, and is he New York-licensed?** Will he work at his normal full price, paid
by the brokerage, with the seller as his client, a signed disclosure that he knows your father-in-law, no repairs on
houses he inspects, and nothing given back to the brokerage? *Provisional:* licence unknown; the software checks the
State register; if he will not accept those terms he is not used; the demo uses a fictional inspector. *Unblocks:*
the pilot provider. (WS6)

**Q39. Will the brokerage ever hold deposits?** *Provisional:* no; the seller's attorney holds them, as is the local
custom, so no broker escrow ledger. *Unblocks:* whether the product needs an escrow ledger. (WS1)

**Q40. Scope limits: sales only (no rentals), and no cold texting or AI calls?** Rentals carry the heaviest
2025-26 enforcement; marketing texts and AI-voice calls need prior written consent. *Provisional:* sales only;
replies and transactional messages only, to people who opted in. *Unblocks:* buyer-flow scope and outreach rules.
(WS2)

**Q41. Your Anthropic Console account: is it an organisation, and do you want to ask Anthropic for zero data
retention?** *Provisional:* no; assume inputs and outputs are kept up to 30 days; send the model only what each step
needs, with names and contact details masked. *Unblocks:* the PII wording and automatic spend reconciliation. (WS7)

**Q42. May we ask Zillow for its FairHome fair-housing dataset (by email, with a use case)?** *Provisional:* not for
the demo; our own 40+ phrase test set is enough; revisit for production. *Unblocks:* breadth of the checker's tests.
(WS7)

**Q43. The free inspection: does "keep the original idea" include it?** It was your father-in-law's add-on, which
you asked to be evaluated honestly. *Provisional:* no; the research's recommendation stands (drop it as pitched, run
a capped pilot on the first ten listings with the seller as the inspector's client), shown in the plan as his
idea with the findings. *Unblocks:* the plan's inspection section and the demo's intake step. (WS6, decision 21)

## Answered (newest first)

- **2026-10-23, Joe, Q19, Q24 and the plan's framing:** "Keep the original idea, that is what I said I would
  build. I can pare it back on the future if need be. The idea is the idea. Completely replace the real estate
  agents." **What changes (decision 21):** the pitch is the brief's idea (software replaces the seller's and
  the buyer's agent and drafts the contract), not the attorney-run flat-fee brokerage. In the demo the AI does
  every agent act; red "NY law today" markers show where a licence or a lawyer is required today, without
  stopping the flow. The findings themselves are unchanged.
- **2026-10-23, Joe, Q26 (who pays for the build):** "Do as much as you can with the api credit before moving to
  use the plan." **What changes (decision 22):** jobs run on the credit until about $2 is left above the $15 demo
  reserve, then on the Max login automatically. The build starts today.

- **2026-10-23, Joe, Q12 follow-up:** sent "146 Rt 292, Holmes, NY 12531". Taken as the demo house in place of
  Alexandria (decision 18); the Virginia/New York mismatch is gone. Assumed the OK to use it is Joe's to give.

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
