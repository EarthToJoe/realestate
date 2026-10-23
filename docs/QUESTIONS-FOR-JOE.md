# Questions for Joe

Answer any of these when you check in, in one line each. Where I could not wait, I made the provisional choice
shown and kept moving; your answer overrides it. Readable at https://realestate.hughesnode.com/docs-questions-for-joe.html

## Open

> **Start here (updated 2026-10-23, afternoon, after decision 21).** Every question below has a default that holds
> until you answer.
> - **For the meeting with your father-in-law:** Q44, one short bundle of five questions only he can answer (bar
>   registration, where he lives and an office, broker of record, ten people by 2026-11-06, the contract route).
> - **Quick confirms for the demo, defaults hold if you say nothing:** Q23 in the demo the software drafts the full
>   contract with no attorney-approval clause, under a red "NY law today" marker that names the lawful launch route
>   (the firm's paper subject to each party's attorney's approval; decision 26); Q25 recorded replay at the meeting with a live switch; Q45 the placeholder firm name; Q43 the
>   free inspection shown as his idea with the research's findings.
> - **After the meeting:** everything else (fees, tours, counties, marketing, lockboxes, scope).
> - **Closed today by decision 21 or merged into Q44:** Q11, Q13 to Q17, Q37 (see Answered).

**Q44 (FIL bundle). Five questions for your father-in-law, for the meeting about 2026-10-30.** Take this one page;
each answer unblocks a Phase 0 step in `docs/PLAN.md`. (1) **Is his New York attorney registration current?** The
no-exam broker licence ($185) needs "an Attorney who is currently admitted"; check the court's attorney search or call
212-428-2800; a lapsed registration must be cured first, and "retired" is untested for this route. (2) **Where does he
live, and where could a New York office be?** The firm needs "a definite place of business within this state" with a
sign readable from the sidewalk (a licensed home office counts); no reciprocity excuses a non-resident. (3) **Will he
be broker of record of the firm that runs the software,** doing only the acts the law requires of a licensee (accept
listings, decide ads, offer advice and negotiating positions, supervise), each one prepared, carried out and logged
by the software, and join HGAR so the firm can use OneKey MLS? (4) **Who are ten people who might sell in the next
year?** Names, not categories, by **2026-11-06**; he calls them by about 2026-12-15. (5) **His view on the contract
route:** the software's full contract as the firm's paper subject to each party's attorney's approval; him as the
seller's lawyer on fixed-fee deals (Ops. 1015, 1117; written ethics advice first); or the parties drafting their own
with the software (untested in New York). *Provisional:* (1) current or curable; (2) outside New York, with a small
licensed Hudson Valley office; (3) yes; (4) the ten-calls test runs as written, and if fewer than three would list, we
rethink how the firm finds customers before building past the demo; (5) the first route on every deal, the second
where he chooses it, the third only after a written ethics opinion. *Unblocks:* A12, A13, A14, A18, K9, Phase 0.
(WS2, WS3, WS5, memo, [plan: the contract route](PLAN.md#the-contract-route-what-new-york-allows-today))

### From the research (added 2026-10-23, Q18 to Q43; reworded for decision 21)

Gathered from the seven research handoffs and the architecture spec, duplicates merged, and reworded on 2026-10-23
for the original idea (decision 21). **(FIL)** marks a question only your father-in-law can answer. Each has the choice
I am using until you answer, and what the answer unblocks.

**Q18 (FIL). Who opens the door at showings and buyer tours?** The AI books every showing and tour, but on the best
New York authority a licensed person (or the owner, at his own home) must open the door, and lockbox keys cannot be
lent. Options for buyer tours: (a) a licensed showing agent per tour ($45 to $400 a showing), (b) him, (c) a licensed
salesperson the firm sponsors. *Provisional:* owners host showings and open houses on the firm's listings; (a) for
buyer tours at launch, (c) once volume grows; DOS asked about unaccompanied tours (Q29). *Unblocks:* the tour step's
marker and the buyer-side cost. (WS1, WS3, WS4)

**Q20. Fee per side.** *Provisional:* a flat $4,500 for the seller side (0.88% of a $510,000 house) and $3,500 for the
buyer side (0.69%), with any surplus seller-offered buyer-agent pay rebated to the buyer; never a document fee. When
the firm acts for both sides the seller saves about two thirds of today's commission; one third when the buyer brings
an agent. These are WS4's working figures; confirm after the ten calls. *Unblocks:* the pricing screen, savings
calculator, the plan's revenue line. (WS4, WS5)

**Q21. When the buyer brings their own human agent: what does the seller offer that agent?** *Provisional:* the seller
chooses, with the AI recommending a market rate (about 2% to 2.5%) and showing the evidence that lower-paying listings
sell slower; never silently 0%. *Unblocks:* the listing intake screen; exposure to K1 and K6. (WS5)

**Q22. The software acts for both sides of the same sale: how is dual agency handled?** Acting for both sides is the
idea, and in New York that is dual agency, which needs both parties' advance informed consent on the state form and
reduces the duties owed to each; designated agents would need two more licensees. *Provisional:* dual agency with
written informed consent on the state form at the start of each side, shown with a "NY law today" marker; the
software never claims undivided loyalty to both. *Unblocks:* the consent screens and the "both sides" wording. (WS1,
WS2)

**Q23 (FIL). The contract: which route at launch, and which standard form does the software's draft follow?** Routes
(see the plan): the software's full contract as the firm's paper subject to each party's attorney's approval (lawful
today, AG 96-F11, DOS LI04); his law practice as the seller's lawyer on fixed-fee deals (Ops. 1015, 1117); the parties
as their own drafters (untested in New York). Forms: NYSAR's statewide purchase agreement, the bar association's
Residential Contract of Sale, or his own. *Provisional:* the demo shows the software drafting the full contract under
a "NY law today" marker; at launch the first route on every deal, the second where he chooses it; the draft mirrors the
bar-association long form's section structure in its own words. *Unblocks:* the contract screen and Phase 2 step 2.8.
(WS2, plan, architecture spec)

**Q25. At the meeting: recorded replay by default, with a live switch?** *Provisional:* yes; replay recorded the day
before and labelled, live only if the room has good internet; map with an offline fallback; the app also runs on a
laptop with one command. Does the room have reliable internet? *Unblocks:* demo-mode design. (architecture §11, WS7)

**Q27 (FIL). Will he ask his malpractice carrier, in writing, whether claims connected with a brokerage he co-owns
are excluded and could affect his legal cover?** *Provisional:* assume no cover from that policy; the brokerage buys
its own E&O ($708 to $1,500 a year) and asks its carrier in writing whether a brokerage-funded inspection pilot is
covered. *Unblocks:* the insurance line, his personal risk decision, the inspection pilot (A17). (WS2, WS4, WS6,
memo)

**Q28 (FIL). Confirm today's closing customs in his counties.** Who drafts, usual deposit, mortgage-commitment
period, whether brokers attend closings, and whether local attorneys will approve a contract the firm's software
drafted (the first contract route, Q23). The bar association's county sheets are from 2018 to 2020. *Provisional:*
use those sheets. A 15-minute conversation. *Unblocks:* timeline defaults and the contract step. (WS1)

**Q29 (FIL). Send DOS one written inquiry, signed by him as the licensee?** Questions: may software carry out a
broker's acts (listing, advertising, presenting offers, negotiating) as the broker's own acts under his supervision,
and what supervision DOS expects; are unaccompanied or unlicensed showings of homes for sale licensed acts; does an
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
listings, an hourly assistant later. *Unblocks:* broker hours and the MLS step's "who keys it" label. (WS3)

**Q34. Paid marketing.** The software markets the business itself (the brief), so its own campaigns cost little;
paid advertising is the question. *Provisional:* referrals plus the AI's own campaigns for the first 12 months; brand
spending at most $1,000 a month; no per-lead buying; no paid portal extras (Zillow Showcase, Homes.com membership) at launch. *Unblocks:* the
K2 guardrail and the marketing budget. (WS4, WS3)

**Q35. Coordination.** *Provisional:* the software coordinates every deal (scheduling, document chasing, deadlines,
status updates), with you watching; a part-time coordinator (about $24,000 a year with employer costs) only if the
pilot's measured hours call for one; you are paid hourly or by salary for any of this, never per deal. *Unblocks:* the
realistic-case budget. (WS4)

**Q36 (FIL). Lockboxes: SentriLock ($130 a year plus $110 per box) or him attending showings?** *Provisional:*
subscribe once buyer-side touring starts. *Unblocks:* showing design. (WS3)

**Q38 (FIL). The inspector friend: name, and is he New York-licensed?** Will he work at his normal full price, paid
by the brokerage, with the seller as his client, a signed disclosure that he knows your father-in-law, no repairs on
houses he inspects, and nothing given back to the brokerage? *Provisional:* licence unknown; the software checks the
State register; if he will not accept those terms he is not used; the demo uses a fictional inspector. *Unblocks:*
the pilot provider. (WS6)

**Q39. Will the brokerage ever hold deposits?** With the lawyer out of the drafting, someone still holds the buyer's
deposit. *Provisional:* not at launch; the seller's attorney holds it, as is the local custom (attorneys still approve
under the first contract route); a broker escrow account under DOS's rules only if a deal has no attorney escrow.
*Unblocks:* whether the product needs an escrow ledger. (WS1, WS2)

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
idea with the findings: the pitch line "you'll know what a buyer's inspector will find before they do, and you decide
what to fix", a cap of $1,500 a listing, owed whether or not the house sells, with an inspection credit and a list of
three licensed inspectors for sellers who decline (absorbs Q37). *Unblocks:* the plan's inspection section and the
demo's intake step. (WS6, WS4, decision 21)

**Q45. The firm's name in the demo.** The build uses the placeholder "Hudson Valley AI Realty (demonstration)" on
every screen and message. A web search (2026-10-23) found no company of that name, but similar real ones exist
(Century 21 Hudson Valley Realty in Poughkeepsie, Keller Williams Realty Hudson Valley Realty Group in New City).
*Provisional:* keep the placeholder, always shown with "(demonstration)"; you or your father-in-law name the real
firm later (his old "Hudson Valley Partners" idea, for example, after a name check with the Department of State).
*Unblocks:* nothing now; the name is one setting in the app's brokerage config.

**Q46. The pricing step's adjustment rates.** The demo adjusts each comparable sale in code at rates we set from the
demo house's own data and state on screen (for example $75 a square foot of living area, $2,500 an acre for the
first 3 acres of difference, +2% a year for time, −8% for a style other than a raised ranch, finished basement
adjusted only between same-style sales; re-examined 2026-10-23, decision 30 note). They are demonstration
rates [INFERENCE], not a broker's or appraiser's. The screen shows the three cross-checks from the demo-house
research beside the adjusted sales and reconciles them: the range is $610,000 to $650,000 (the same as
`docs/specs/demo-house.md` section 4), the reconciled value $625,000, and the AI recommends $640,000.
*Provisional:* keep them, labelled; a broker (perhaps your father-in-law's contacts) can replace them with
local paired-sales rates in `app/modules/pricing/service.py`, one line each. *Unblocks:* nothing for the demo.

**Q47. The demo order and the numbers on screen: the buyer's side before the offers.** The firm's own buyer
makes offer B, and the buyer answers the seller's counter on the buyer's screen, so the demo walks the buyer's side
before the offers and the contract. *New provisional (2026-10-23, the chat session's call; decision 42):* the screens
number the steps in the order the demo walks them: 1 Intake, 2 Pricing, 3 Listing copy, 4 Marketing plan, 5
Communications, **6 Buyer side, 7 Offers, 8 Contract**, 9 Timeline, 10 Marketing the business, so you never say
"now step 8, then step 6". The success criteria keep their own numbers (SC8 is the buyer side); `docs/DEMO-SCRIPT.md`
gives the mapping once. *Unblocks:* nothing; Wednesday's click-through will show whether it reads naturally.

**Q48. The contract drafts with Opus, and the draft leaves blanks.** After a side-by-side, the contract is drafted
by Claude Opus 5.5, the strongest model, because a lawyer will read it closely (decision 36). That costs about
$0.27 a live draft, against $0.18 on Sonnet, and nothing in the recorded demo. Where the deal gives no number (the
seller's cure-cost limit, test deadlines, the loan amount), the draft leaves a blank for the parties rather than
inventing one. *Provisional:* Opus, with blanks. If your father-in-law would rather see a draft with every blank
filled with a usual Hudson Valley figure, that is a prompt change; it needs his figures. *Unblocks:* nothing for the
demo.

**Q49. The founder on the firm's own advertising.** Step 10's landing page names the firm's founder, as the
brief asks; the demo shows a placeholder, "[Founder's name]", because naming a real person in public advertising
needs that person's consent. *Provisional:* keep the placeholder. If your father-in-law (or you) should be named, tell
me the name and the one line to say about him; it is one line in `config/brokerage.yaml`. *Unblocks:* nothing for the
demo.

**Q50. Erasing a person's data versus the three-year records rule.** The demo erases a person's personal data on
request ("People and their data"). New York requires a brokerage to keep its transaction records (agreements,
contracts, disclosures and their signed acknowledgments) for three years (L17). *Provisional for production:* erase
marketing and other data at once, and the signed records when the three years end; the demo erases at once to show it
works, and its confirm screen says so. A lawyer's view on where the line falls would settle it. *Unblocks:* nothing for
the demo.

## Answered (newest first)

- **2026-10-23, closed by decision 21 or merged into Q44 (the father-in-law bundle):**
  - **Q11** (where he lives; is his registration current): merged into Q44 (1) and (2).
  - **Q13** (ten sellers he could call): merged into Q44 (4), now due 2026-11-06; the fallback "re-plan around a local
    partner broker" is replaced by "rethink how the firm finds customers", since a partner broker would replace the idea.
  - **Q14** (licence, broker of record, HGAR): merged into Q44 (3), reworded: he is broker of record of the firm that
    runs the software, doing only the acts the law requires of him.
  - **Q15** (broker only, or also the seller's lawyer): closed by decision 21; the "broker only" plan it presumed is
    gone. Its substance (the fixed-fee seller's-lawyer route) is now one of the contract routes in Q44 (5) and Q23.
  - **Q16** (presence for listing appointments; New York office): closed by decision 21 for the appointments (the
    software runs intake and pricing); the office part is merged into Q44 (2).
  - **Q17** (hours a week as working broker of record): closed by decision 21; his hours now go only to the acts the law
    requires, which the pilot measures (A1), and Q44 (3) asks whether he will take that role.
  - **Q37** (drop the free-inspection pitch, run a capped pilot): merged into Q43.
  - **Reworded, still open:** Q18 (who opens the door), Q20 (fee per side), Q21 (buyer's own agent), Q22 (dual agency
    when the software acts for both sides), Q23 (contract route and form), Q29 (DOS inquiry), Q34, Q35, Q39.

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
