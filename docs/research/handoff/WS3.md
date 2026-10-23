# WS3 handoff to the orchestrator (2026-10-23)

Deliverable: `docs/research/WS3-listing-data-access.md` (D below). Notes with gap fill:
`research_notes/WS3 Listing and data access/mls_access.md` and `.../portals.md`.

## 1. Assumption status lines

- A4 | partly hit | No Hudson Valley MLS or portal offers a listing-input API (a named A4 kill condition), so a person keys every listing; but OneKey may not refuse a flat-fee firm, costs are ~$3,821 in year one, and portals syndicate free, so it caps throughput rather than killing it (est. 20–45 broker minutes per listing) | [D: No write API](../WS3-listing-data-access.md#no-write-api-a-person-submits-each-listing)
- A6 | partly hit | OneKey lockbox keys may not be lent or their PIN shared (Rule 405.8), so a licensee (our broker, a hired licensee, or the listing agent) must open every door, and a written buyer agreement is required before any tour (402.3); scheduling itself may be done by unlicensed staff or software (404.4) | [D: Lockboxes](../WS3-listing-data-access.md#lockboxes-are-optional-but-keys-cannot-be-lent-showingtime-is-included)
- A1 | partly hit | MLS rules let an unlicensed Administrative User key listings, but "Responsibility for the accuracy ... shall always remain solely with the Participant" (Rule 320), so the one broker must review and approve every listing and every price/status change; the time is modest (20–45 min per listing for this channel) | [D: Cheapest path](../WS3-listing-data-access.md#the-cheapest-compliant-path-step-by-step)
- A7 | dodged (for this channel) | MLS, association and licence costs are ~$3,821 first year and ~$2,886 a year after; portals free; paid portal products optional | [D: Getting in](../WS3-listing-data-access.md#getting-in-a-broker-licence-realtor-membership-and-about-3800-in-year-one)
- A2 | still open (WS2 owns it); WS3 adds two constraints | Joe's software company may receive OneKey data only as the broker's licensed MLS Grid vendor (licence V(f)(xi), Rules 605.3/606); DOS says an unlicensed assistant paid "on a completed transaction basis" must be licensed | [D: Data for the buyer side](../WS3-listing-data-access.md#data-for-the-buyer-side-idx-is-cheap-ai-training-is-not-licensed)
- A8 | still open, with a rule-based assist | OneKey screens every listing with an automated checker and removes flagged fair-housing words; MLS Grid's AI addendum allows AI-written listing descriptions for our own listings; DOS (13 Nov 2025) warns AI images can be misleading advertising | [D: Photos and copy](../WS3-listing-data-access.md#photos-and-copy-license-them-label-them-never-borrow-them)
- A10 | still open (WS5 owns it); WS3 context | Compass is pushing OneKey to allow private marketing and OneKey refused (20 Oct 2026); Redfin shows only Compass's Coming Soon listings under an exclusive deal | [D: Delayed marketing](../WS3-listing-data-access.md#delayed-marketing-exists-in-onekey-as-mls-only-without-a-time-limit)

## 2. Kill criteria

- K9 (MLS membership on acceptable terms) | dodged, conditionally | OneKey must not deny participation "based on the level of service" (202.1(d)) and costs are small; but it requires REALTOR membership plus a state-issued broker licence, so K9 is **hit** if the attorney will not get the $185 licence or will not join HGAR (NAR made membership a local choice from 1 Jan 2026; OneKey kept it).
- K4 (pitched or built as autonomous) | substance confirmed, evidence corrected | The "express written permission before AI training" line attributed to NAR is Metro MLS's rule; the binding text for OneKey data is MLS Grid's AI Use Addendum (Aug 2026): AI search and our own marketing copy allowed, everything else needs OneKey's written approval, no persistent embeddings or retention. Licensee-in-the-loop is also built into OneKey (Participant responsible for every field) and DOS's assistant guidance ("for approval of broker"). Please update the K4 evidence line in WS5/ASSUMPTIONS.
- A4 kill criterion | first clause hit (no listing-input API), second and third dodged (flat-fee listings allowed; costs viable). The assumption's own text says this "caps scale but does not kill".
- A6 kill criterion | first clause partly hit (lockbox access needs a licensee or the listing agent); second clause (buyers abandon at touring) untested.
- K2 (listings bought with advertising) | context only | Portals do not supply sellers; Zillow and reportedly Realtor.com send buyer inquiries on our listings to paying agents; Homes.com sends them to the listing agent free. WS3 neither hits nor dodges K2.
- K6 (local steering penalty) | open; WS3 enabler | MLS membership gives the firm OneKey comparables (CMA use) to measure its own days-on-market against the market, which is how K6 would be tested.
- K1, K3, K5, K7, K8 | not bearing on WS3.

## 3. Questions for Joe (or his father-in-law)

- Q-WS3-1. Will your father-in-law join HGAR as a REALTOR (about $606 a year plus $100; NAR Code of Ethics and arbitration) and take the attorney broker licence ($185, paper form, no exam)? Provisional: yes to both. Unblocks: OneKey MLS and every portal (K9).
- Q-WS3-2. Launch on OneKey alone (Dutchess, Orange, Putnam, Rockland, Sullivan, plus Ulster and any Columbia/Greene homes entered "out of area"), and join the northern HVCRR MLS only when the first Columbia or Greene listing signs? Provisional: yes. Unblocks: the cost model and the POC's map of where listings appear.
- Q-WS3-3. Who types listings into the MLS at launch: your father-in-law himself, or an hourly or salaried assistant registered as an "Administrative User"? (Not Joe, while A2 is open; DOS says per-deal pay requires a licence.) Provisional: the broker himself for the first listings, an hourly assistant later. Unblocks: broker-hours in WS4 and the POC checkpoint role labels.
- Q-WS3-4. Pay for portal extras (Zillow Showcase ~$300–750 per listing; Homes.com Membership ~$3,400 a year)? Provisional: no at launch; rely on free syndication, Homes.com's free listing-agent leads and the firm's own site. Unblocks: WS4 marketing budget.
- Q-WS3-5. Lockboxes: subscribe to SentriLock ($130 a year plus $110 per box) or rely on the broker attending showings? Provisional: subscribe once buyer-side touring is in scope. Unblocks: showing design (A6).

## 4. Traceability items (WS3 IDs; map to WS1 F-IDs and WS2 L-IDs when those land)

Channels (listing INPUT):
- WS3-C1 OneKey MLS submission | Stub with marker "human required here: OneKey has no listing-input API; a licensee or registered Administrative User keys this listing into Ocusell List or Matrix, and the broker approves it (OneKey Rules 205, 320)". The POC automates everything before it: the listing package in OneKey field order (RESO names), and a rule pre-check (Parcel ID, tax square footage, no contact details, showing notes or compensation in public remarks, fair-housing words, front photo).
- WS3-C2 Hudson Valley Catskill Region MLS (Ulster/Columbia/Greene) | Stub with marker "human required here: second MLS membership (HVCRR) needed for full cooperation north of OneKey; fees unpublished; meanwhile entered in OneKey as out-of-area".
- WS3-C3 Columbia Greene Northern Dutchess MLS | Skip; shown inside the WS3-C2 card only.
- WS3-C4 Zillow/Trulia | No API call. Simulated status "appears automatically from OneKey in about 24–48 h"; one-time marker "human required here: claim the agent profile". Show that buyer inquiries go to paying agents on Zillow.
- WS3-C5 Zillow broker direct feed | Skip (post-launch insurance; marker only on the setup checklist).
- WS3-C6 Zillow Preview | Skip, with an explainer: conflicts with OneKey's Coming Soon no-syndication rule (302.3) and the one-business-day clock.
- WS3-C7 Zillow FSBO | Skip; the POC blocks any FSBO export for a brokered listing.
- WS3-C8 Realtor.com | Simulated status; one-time marker "human required here: turn on Keystone Realtor.com switches".
- WS3-C9 Redfin | Simulated status only.
- WS3-C10 Homes.com | Simulated status; highlight "your buyer leads come to you here".
- WS3-C11 ListHub | Skip.
- WS3-C12 OneKeyMLS.com and Cribio | Simulated status; tied to the Keystone switch.
- WS3-C13 The firm's own website | Automated publish, gated by a Clear Cooperation clock: no public page until the MLS entry is recorded, or a visible one-business-day countdown starts (OneKey 302.2; A10679B if signed).
- WS3-C14 Google Business Profile | Automated draft post; actual posting via API optional (stub in the demo).
- WS3-C15 Meta, Nextdoor, Craigslist | Automated ad and post copy (with the fair-housing check); posting stubbed "human required here: platform rules forbid automated posting (Craigslist) or business-page Marketplace listings (Meta)".

Data feeds (data OUTPUT):
- WS3-D1 IDX feed (MLS Grid) | Demo uses fictional listings; production stub "human required here: broker signs the MLS Grid licence and AI Use Addendum; OneKey approves the site".
- WS3-D2 VOW feed | Stub (same marker; requires client registration).
- WS3-D3 Broker back-office feed | Not in POC.
- WS3-D4 Own listings | Automated from the firm's own database (keeps AI work outside the MLS Grid addendum).
- WS3-D5 CMA / AVM | Fictional comparables; checkpoint "broker reviews the valuation before it goes to the client" (single-client CMA use).
- WS3-D6 AI buyer search | Automated in the permitted pattern: live per-session queries, no persistent embeddings or vector store of MLS data, no retention by the model provider, IDX attribution shown; any other AI use of MLS data gets the marker "human required here: OneKey written approval".
- WS3-D7 Portal data (Zillow, Redfin, Homes.com, Realtor.com) | Never scraped; no code.

Rules that become visible checkpoints:
- WS3-R1 Clear Cooperation clock (302.2; $2,500 + $100/day) | Automated countdown and publish block.
- WS3-R2 Listing Exposure choice (Publish to Internet / MLS Only / Private) and Coming Soon (14 days, no showings, no syndication) | Human: seller signs the required form; the POC shows where the listing will and will not appear.
- WS3-R3 Seller authorisations: cooperating brokers (319.4), lockbox (405.4), photographer licence (603) | Human signatures; the POC generates the forms.
- WS3-R4 Showing requests answered within 24 hours (404.4) | Automated scheduling; marker "human required here: a licensee or the listing agent opens the door (405.8)".
- WS3-R5 Written buyer agreement before any tour (402.3) | Checkpoint before any tour booking.
- WS3-R6 No compensation in MLS fields (502, 306.3(d)); not "free" (601.4) | Automated checks.
- WS3-R7 Public remarks and fair-housing screen (306.3(b)) | Automated check plus broker approval.
- WS3-R8 Photo rights and AI-altered images (602.1, 603, 612.2; 19 NYCRR 175.25(b)(2)(iii); DOS alert 13 Nov 2025) | Automated flag and on-image label; human: photographer licence on file; never pull other brokers' photos.
- WS3-R9 Price and status changes within 24 hours, price changes signed by the seller (310.3, 311) | Automated task; human signature and broker sign-off.

## 5. Open gaps that still matter, and what closes them

- HVCRR MLS fees, rules (Clear Cooperation, delayed marketing, limited service), lockbox vendor, and whether HVCRMLS and CGND are one database | Phone HVCRR, 845-338-5299, ask for Kim Fiore (MLS Compliance/Communications); 2926 Route 32, Saugerties. Four questions are listed in the mls_access gap fill (theme M1).
- Whether a broker's own software may push listings into OneKey through the Ocusell Aggregator, and the List Plus price | Phone OneKey Success Team, 1-888-663-5392, Support@OneKeyMLS.com (number from a search snippet of OneKey's Welcome Center; confirm), and ask to be connected to Ocusell; Ocusell's site is ocusell.com.
- How OneKey's data reaches Zillow, Redfin and Homes.com; whether a Zillow Preview listing breaches Rule 302.3; whether OneKey has approved AI uses beyond the MLS Grid addendum | Same OneKey call.
- Zillow's current Listing Access Standards and Listing Feed Terms | Open in a browser (zillow.com blocks automated readers): zillow.com/c/info/zillow-listing-access-standards and zillow.com/corp/listing-feed-terms-of-use.
- OneKey EULA text (copyright options for brokers) | Readable after joining OneKey.
- Governor's action on A10679B (private listings) and S8870 (broker supervision) | Check nysenate.gov bill pages; neither had been delivered as of 23 Oct 2026.
- Measured minutes per MLS entry | Time the first ten real listings.
- Orchestrator note: these calls are Joe-list items; please add them with `joe-todo` and notes (this job did not touch the shared list).

## 6. Contradictions with other workstreams' notes

- WS5 (why_attempts_failed..., KQ5 and K4): "NAR policy requires express written permission before MLS data is used for AI training" — the wording is Metro MLS's own rule quoted by NAR; NAR has no Handbook AI rule; for OneKey the MLS Grid AI Use Addendum governs.
- WS4 (costs_and_revenue_benchmarks, §2): "OneKey now states coverage of ... Ulster" and "Columbia and Greene ... run on the Columbia Greene Northern Dutchess MLS" — OneKey's Rule 201 omits Ulster (covered in practice as out-of-area); the "Hudson Valley Catskill Region MLS" is the former Ulster County MLS on Flexmls, and CGND may still be separate.
- WS4 (§2): "Lockbox and ShowingTime prices are not published" and OneKey feed fees "unpublished" — SentriLock is $130 a year plus $110 per box leased; ShowingTime is included; MLS Grid feeds are $250/month plus $20/month per licence, or $20/month OneKey share through an IDX vendor.
- WS5 (hudson_valley_market_and_locals): "Hudson Valley Catskill Region MLS, formerly Columbia Greene Northern Dutchess MLS" — the HVCRMLS name continues the Ulster County MLS series; CGND is a separate name and possibly a separate database.
- WS1 (transaction_tasks_and_timeline, S7): MLS input "~1 hour" (unsourced) — consistent with WS3's 15–60 clerical minutes plus 20–45 broker minutes; WS1 cites LIBOR 2023 fine ceilings now superseded by OneKey Rules 2026C.
- WS2 (licensing_law_entities_compensation, KQ2): MLS licence requirement marked [CLAIMED] — now confirmed [PRIMARY] (OneKey Rule 202.1(c)(1)).
