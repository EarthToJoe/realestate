# One MLS login unlocks every portal

*Workstream 3 (listing and data access). Written 2026-10-23 from the two WS3 notes files and their same-day gap
fill. Source labels: [PRIMARY] the rule, statute, court record, fee schedule or company's own page; [SECONDARY]
trade press or a third party reporting it; [CLAIMED] an interested party's statement or a search snippet of a page
that could not be opened; [INFERENCE] this report's own reasoning. Prices and statuses are as of the date shown.*

No software can put a for-sale listing on Zillow, Redfin, Realtor.com or Homes.com by itself: none of them
offers a brokerage an API (a door for software) to create a listing, and all four take Hudson Valley listings
from the multiple listing service (MLS) feed. The real gate is **OneKey MLS**, which covers Dutchess, Orange,
Putnam, Rockland and Sullivan by rule (and much of Ulster in practice). It admits only a **REALTOR (association
member) who holds a New York broker licence**; the father-in-law can get that licence as an admitted attorney on
a paper application and **$185, with no course, experience or exam**. OneKey has **no listing-input API** either:
a person keys each listing into its web screens (Matrix, or since 18 August 2026 the free Ocusell List tool),
an unlicensed assistant may do the typing, and the broker answers for every field. That is a direct hit on the
"MLS entry can be automated" half of assumption **A4**: the software can prepare and check the whole listing,
but a human presses submit, at an estimated **20 to 45 minutes of the broker's time per listing**. It does not
kill the venture, because everything after MLS entry (Zillow, Realtor.com, Redfin, Homes.com, OneKey's own
consumer site) is automatic and free, the first-year cost of the MLS channel is about **$3,821**, and OneKey's
rules forbid refusing a broker for offering less service, which **dodges kill criterion K9** as long as the
attorney joins a REALTOR association. Two further limits shape the product: lockbox keys may not be lent, so a
licensee must open doors (**partly hits A6**), and the AI addendum to OneKey's data licence (August 2026) allows
AI search and AI-written marketing but **forbids training AI on MLS data, or keeping it in an AI's memory,
without OneKey's written approval**, so the buyer-side AI must query listings live and keep nothing.

## The brief's three questions, answered

| The brief asked | Short answer | Where |
|---|---|---|
| Can software list a property on Zillow, Redfin, Realtor.com? | Not directly. All three take listings from the MLS. Zillow's other routes are owner-only (FSBO) or a manual pre-market tool for enrolled brokerages. | [Every portal draws from the MLS](#every-portal-draws-from-the-mls-so-onekey-is-the-gate) |
| ... and the regional MLSs (OneKey, "Hudson Valley MLS")? | Yes, but only through web screens operated by a person under a licensed, REALTOR-member broker. OneKey covers the southern counties; the Hudson Valley Catskill Region MLS covers Ulster, Columbia and Greene. | [Getting in](#getting-in-a-broker-licence-realtor-membership-and-about-3800-in-year-one) |
| Is there an API, or must a human click through? | No write API at any Hudson Valley MLS or portal. A human (or a registered clerical user) clicks through; software prepares everything before that. | [No write API](#no-write-api-a-person-submits-each-listing) |
| What memberships or subscriptions, and what do they cost? | NY broker licence ($185 for two years), HGAR REALTOR membership ($606 a year plus $100), OneKey MLS ($650 once plus $190 a month). Portals free. | [Getting in](#getting-in-a-broker-licence-realtor-membership-and-about-3800-in-year-one), [Cheapest path](#the-cheapest-compliant-path-step-by-step) |
| (Specific requirements) Rules that bite; data for the buyer side; cheapest path; POC verdicts | Clear Cooperation, "MLS Only", no entry-only category, 24-hour showings, lockbox, Zillow's standards, photo rights; IDX and the AI addendum; seven setup steps and six per-listing steps; automate the package, stub the submission. | Sections below |

## Every portal draws from the MLS, so OneKey is the gate

All four big portals display a Hudson Valley listing because the MLS sends it to them. Zillow ended manual
listing entry by agents in 2017 ([Inman, 15 Feb 2017](https://inman.com/2017/02/15/zillow-group-nixes-manual-listing-entry-real-estate-agents-doubles-direct-listing-feeds))
[SECONDARY] and since 2021 takes MLS data as an MLS member through IDX feeds
([Metro MLS, 26 May 2021](https://metromls.com/zillow-idx-feed/)) [PRIMARY, pre-2024]; Zillow appears in OneKey's office directory
([OneKey](https://www.onekeymls.com/realtor/offices/Zillow-Inc/ZILLOW)) [PRIMARY]. Redfin says **"All
broker-listed homes from the Multiple Listing Service (MLS)"** appear on its site and that 70% of new MLS listings
post within five minutes ([Redfin data quality, Sept 2025](https://www.redfin.com/about/data-quality)) [PRIMARY];
its terms credit "New York MLS (OneKey)" data "submitted to the MLS GRID" and the Hudson Valley Catskill Region MLS
([Redfin terms](https://www.redfin.com/about/terms-of-use)) [PRIMARY]. Realtor.com receives OneKey listings under
two broker-level switches in OneKey's Keystone settings, one for active and one for pending and sold listings, and
**"Any 'no' or 'off' setting will overrule an indication of yes"**
([OneKey support](https://support.onekeymls.com/hc/en-us/articles/42913600864404)) [PRIMARY]. Homes.com shows MLS
listings and credits only the listing agent ([Homes.com Membership](https://www.homes.com/solutions/membership))
[PRIMARY]. None of them publishes an API through which a brokerage could create a listing; Zillow's own listings API
is read-only and "at the discretion of our individual MLS partners"
([Zillow Group developers](https://www.zillowgroup.com/developers/api/mls-broker-data/mls-listings/)) [PRIMARY].
"Syndication" (the MLS passing a listing on to these sites) is therefore the only route for a brokered listing, and
flat-fee brokers report it takes about 24 to 48 hours ([Hauseit](https://www.hauseit.com/agent-assisted-fsbo/))
[CLAIMED].

The side doors do not help a OneKey brokerage. Zillow's for-sale-by-owner (FSBO) tool is for owners only: "To
advertise a property as FSBO or FRBO you must be the owner of that property"
([Zillow listing quality, snippet](https://www.zillow.com/corporate/quality/)) [CLAIMED], so posting a brokered
listing there would misrepresent it. **Zillow Preview**, launched 17 March 2026 for pre-market listings, now has
**more than 400 enrolled brokerages** and since 17 September 2026 also shows on Realtor.com
([Zillow release, 17 Sep 2026](https://zillow.mediaroom.com/2026-09-17-Zillow-PreviewSM-listings-are-now-live-on-Realtor-com-R-,-offering-the-same-early-access-on-the-two-most-visited-real-estate-platforms-in-the-country))
[PRIMARY], but access is "unlocked at the brokerage level" by agreement with Zillow
([Zillow release, 25 Mar 2026](https://s25.q4cdn.com/975009107/files/doc_news/Zillow-Preview-gains-rapid-momentum-as-dozens-of-new-brokerages-sign-on-2026.pdf))
[PRIMARY] and agents type each listing into Zillow Workspace
([Zillow, snippet](https://www.zillow.com/pro/zillow-preview-work/)) [CLAIMED]. A Preview listing is public
marketing, which starts OneKey's one-business-day clock, and once in OneKey as "Coming Soon" it may not be
syndicated "to advertising websites" ([OneKey Rules 2026C, 302.3](https://support.onekeymls.com/hc/article_attachments/49417630758548))
[PRIMARY], so Preview has little use here [INFERENCE]. Redfin's only non-MLS inventory is FSBO homes posted on
Fizber.com or FSBO.com ([Redfin](https://www.redfin.com/about/data-quality)) [PRIMARY], and its Compass deal is
exclusive, so Redfin "cannot display the coming soon listings of other brokerages"
([HousingWire, 10 Apr 2026](https://www.housingwire.com/articles/premarketing-listings-compass-zillow-exp/))
[SECONDARY]. ListHub, the syndication service Realtor.com's owner runs, does not let brokers type in listings
([How ListHub Works](https://www.listhub.com/how-listhub-works/)) [PRIMARY, read by the earlier pass], and no OneKey
page mentions it.

One thing differs sharply between portals: who receives the buyer's inquiry. On an ordinary Zillow listing the
"Contact Agent" inquiry goes to an agent who pays Zillow, and Zillow aims to send **"more than 75% of our
connections"** to pay-at-close Preferred partners by the end of 2026
([Zillow Q2 2026 letter](https://www.sec.gov/Archives/edgar/data/0001617640/000161764026000050/exhibit992.htm))
[PRIMARY]; Realtor.com reportedly does the same ([Listed Simply](https://faq.listedsimply.com/en/articles/4932413-how-your-contact-information-appears-on-consumer-real-estate-websites))
[CLAIMED]. Homes.com is the exception: it "presents the listing agent and only the listing agent"
([HousingWire, 30 Jul 2024](https://www.housingwire.com/articles/your-listing-your-lead-the-principle-driving-home-coms-agent-friendly-portal/))
[PRIMARY statement]. A flat-fee firm will therefore see few buyer inquiries from Zillow on its own listings unless it
pays for Showcase, which is unpriced publicly and reported at **$300 to $750 per listing** on a 6 to 12 month
contract ([RE/MAX FAQ](https://resources.remax.com/remax-and-zillowpreview-faq/)) [CLAIMED].

### The channel table

| Channel | Can software create a listing? | Route | Who may do it | Membership or subscription required | Cost (dated) | Data-use and AI rules | Verdict for the POC |
|---|---|---|---|---|---|---|---|
| **OneKey MLS** (Dutchess, Orange, Putnam, Rockland, Sullivan by Rule 201; Ulster in practice) | No. No broker write API; an "Ocusell Aggregator" takes brokerage feeds for Participants, but no third-party push is documented | Web form: Matrix Add/Edit or Ocusell List (free, live 18 Aug 2026) | The Participant broker, its licensed subscribers, or registered unlicensed Administrative Users doing clerical work under supervision; the broker answers for every field (Rules 205, 320, 401) | REALTOR membership (HGAR or LIBOR) plus a NY broker licence; annual EULA | HGAR $606/yr + $100 once; OneKey $650 once + $190/month per office (2026 schedules) | Listing content licensed to OneKey (602.1); MLS data confidential (604, 605.3); feeds under the MLS Grid licence and AI Use Addendum (Aug 2026) | **Stub the submission** with "human required here: no listing-input API; a licensee or registered clerical user keys it; the broker approves". **Automate** the listing package and rule pre-check |
| **Hudson Valley Catskill Region MLS** (HVCRR; former Ulster County MLS; Flexmls since ~May 2024; reports cover Columbia, Dutchess, Greene, Orange, Sullivan, Ulster) | No. Flexmls's public API refuses listing writes (HTTP 405) | Web form | Its Participants and subscribers | HVCRR REALTOR membership; terms unpublished | Unpublished: "call ... 845-338-5299" | Rules and data licence unpublished | **Stub** with "human required here: second MLS membership needed for full Ulster/Columbia/Greene cooperation; fees unknown" |
| **Columbia Greene Northern Dutchess MLS** (cgndmls.com; HVCRR subsidiary; database on SourceRE since Jun 2024; may now be merged into the above) | No evidence of a broker write route | Web form | Members | REALTOR membership (2016 form) | Unpublished; dues billed 1 Apr and 1 Oct (2016 form) | Unpublished | **Skip** in POC (marker only) |
| **Mid-Hudson MLS** (Dutchess) | Gone: conversion into OneKey completed end of January 2024 | n/a | n/a | n/a | n/a | n/a | n/a |
| **Global MLS** (Capital Region; Flexmls) | No (Flexmls API refuses writes) | Web form | Its members | REALTOR membership | Unpublished | Not reviewed | **Skip** (outside launch area; some northern Greene listings double-entered there) |
| **Zillow and Trulia**, standard listings | No. Agent manual entry ended 2017 | Via the MLS only (inferred: Zillow takes OneKey data as a member under OneKey's "IDX" switch) | Automatic for any OneKey listing set to "Publish to Internet" | None beyond MLS | Free. Optional Showcase ~$300–750/listing retail [CLAIMED]. Buyer leads go to paying agents | Terms bar scraping; listings API is read-only and MLS-gated | **No build**: show "appears automatically in 24–48 h"; human marker "claim the agent profile once" |
| **Zillow broker direct feed** (MLS Grid "PDAP" feed) | No new listings: it re-sends the firm's own MLS listings | Data feed | Designated managing broker | MLS participation plus a Zillow feed agreement | "Setting up a direct feed agreement with Zillow is free" [CLAIMED]; MLS Grid plumbing may cost | Feed terms unreadable (403) | **Skip** in POC; set up after launch as insurance against feed disputes |
| **Zillow Preview** (pre-market) | No API; manual entry in Zillow Workspace | Web form | Agents of brokerages enrolled with Zillow (400+ by 17 Sep 2026) with a linked MLS membership | Brokerage agreement with Zillow | Free | Listing agent gets direct inquiries free; also shown on Realtor.com (not NYC) | **Skip**: conflicts with OneKey's Coming Soon no-syndication rule and the one-day clock |
| **Zillow FSBO** | Owner's web form | Web form | The owner only | Zillow account | Free | Not on the MLS; excluded from Zillow's listing standards | **Skip**: a brokered listing may not be posted as FSBO |
| **Realtor.com** | No API | Via the MLS (OneKey Keystone switches); pre-market only via Zillow Preview or Zenlist for enrolled brokerages | Broker sets the switches once | None beyond MLS | Free. Paid leads: Connections Plus ~$200/month shared [CLAIMED] | Terms unreadable; reported bans on scraping and data mining [CLAIMED] | **No build**; one-time human setting |
| **Redfin** | No API | Via the MLS (OneKey through MLS Grid; HVCRMLS) | Automatic | None | Free. If the firm takes Redfin buyer referrals: 33–40% of commission above $100,000 (Aug 2025) | Terms ban automated crawling and data mining | **No build** |
| **Homes.com** | No API | Via the MLS (IDX feeds); opt-in pre-market under seller instruction (Mar 2026) | Automatic; listing agent shown and gets leads free | None | Free display. Membership averages $3,400/yr (Apr 2026); Boost ~$260/listing | Terms bar scraping [CLAIMED] | **No build**; show "your leads come to you here" |
| **ListHub** | No: "brokers and agents cannot manually enter listings" | Feed from the MLS, or a broker licence via MLS Grid | Head broker registers | None | Free | Publishers must send leads to the listing broker | **Skip** (OneKey shows no ListHub use) |
| **OneKeyMLS.com and Cribio** (Broker Public Portal) | Automatic from the MLS | Keystone switch; Cribio opt-out | Broker | None | Free | n/a | **No build** |
| **The firm's own website** | Yes, for its own listings | Own code; MLS Grid allows "Participant Listings Use ... in any manner" | The firm | None for own listings; an IDX licence for other brokers' | Hosting only | Showing a listing publicly starts the Clear Cooperation clock (302.2) | **Automate**, gated: publish only once the MLS entry exists or within one business day |
| **Social and classifieds** (Google Business Profile, Meta, Nextdoor, Craigslist) | Google posts: yes (API). Meta: Housing-category ads from a catalog; Marketplace closed to business Pages since 30 Jan 2023. Nextdoor and Craigslist: no | API / ads / manual | Broker or staff | Accounts | Free (ads paid; Craigslist for-sale real estate free) | Craigslist terms forbid posting software; Meta housing ads restricted targeting | **Automate** drafts and Google posts; **stub** manual posts; **skip** Craigslist automation |

Sources for the rows not cited in the text: Ocusell ([OneKey release, 5 Aug 2026](https://corporate.onekeymls.com/news/94u6jq9vsjyb9weezedz7tx26a3jmc))
[PRIMARY]; Ocusell Aggregator ([OneKey support](https://support.onekeymls.com/hc/en-us/articles/41277098013972))
[PRIMARY]; HVCRR fees ([HVCRR join](https://hvcrr.com/the-association/join-the-board/)) [PRIMARY]; Flexmls
([FBS, 14 May 2024](https://wearefbs.com/blog/welcome-to-four-new-flexmls-customers/)) [CLAIMED] and its API
([Spark docs](https://www.sparkplatform.com/docs/api_services/listings)) [PRIMARY]; CGND
([SourceRE, 6 Jun 2024](https://www.sourceredb.com/news/cgndmls-partnership)) [CLAIMED] and
([2016 application](https://hvcrr.com/wp-content/uploads/2016/01/CGND-MLS-Application-01-26-16.pdf)) [PRIMARY];
Mid-Hudson ([RESO interview, 24 May 2024](https://www.reso.org/blog/three-questions-king/)) [SECONDARY]; Zillow feed
([Zillow, snippet](https://www.zillow.com/agents/listing-feed/)) [CLAIMED]; Realtor.com prices
([Clever, 14 Sep 2026](https://listwithclever.com/real-estate-blog/realtor-com-leads-reviews-costs-pros-cons/))
[CLAIMED]; Redfin referral fees ([Redfin Partner form, Aug 2025](https://partneragents.redfin.com/hc/en-us/article_attachments/38904718960141))
[PRIMARY]; Homes.com prices ([The Real Deal via Yahoo, 29 Apr 2026](https://finance.yahoo.com/markets/stocks/articles/costar-ceo-andy-florance-defends-173757873.html))
[SECONDARY] and ([Inman, 16 Jul 2025](https://inman.com/2025/07/16/homes-com-sent-direct-mailers-to-sellers-across-the-country-asking-them-to-pay-to-boost-their-homes))
[SECONDARY]; OneKeyMLS.com and Cribio ([OneKey, 10 Feb 2026](http://corporate.onekeymls.com/news/onekey-mls-advances-consumer-search-strategy-through-partnership-with-broker-public-portal))
[PRIMARY]; MLS Grid licence ([MLS Grid Data License Agreement](https://www.mlsgrid.com/s/MLS-GRID-Data-License-Agreement.pdf))
[PRIMARY]; Craigslist ([terms](https://www.craigslist.org/about/terms.of.use/en)) [PRIMARY] and
([fees](https://www.craigslist.org/about/help/posting_fees)) [PRIMARY]; Meta
([BAM, Jan 2023](https://nowbam.com/facebooks-new-rules-for-real-estate-listings/)) [SECONDARY]; Google Business
Profile ([Google](https://developers.google.com/my-business/content/posts-data)) [PRIMARY].

## Getting in: a broker licence, REALTOR membership and about $3,800 in year one

OneKey's rule book (version 2026C) sets the entry test plainly. A Participant must be a principal of the firm and
**"is a REALTOR® of any Board and holds a valid state-issued Real Estate Broker's license"**; the same rule bars the
MLS from denying participation "based on the level of service provided by the Participant or potential Participant
as long as the level of service satisfies state law" ([OneKey Rules 2026C, 202.1](https://support.onekeymls.com/hc/article_attachments/49417630758548))
[PRIMARY]. Its join page repeats it: "To join OneKey MLS, you must be an active member of a REALTOR® association and
hold a New York real estate license" ([OneKey join](https://corporate.onekeymls.com/join)) [PRIMARY]. NAR loosened
the national rule in November 2025, repealing the policy that backed membership requirements so that "MLSs will now
decide locally whether to allow non-Realtor licensees to participate" from January 2026
([HousingWire, 17 Nov 2025](https://www.housingwire.com/articles/mls-policy-changes/)) [SECONDARY], but OneKey has
kept the requirement in its 2026 rules. The membership is a flat cost, not a hurdle: HGAR charges **$606 a year
plus a $100 processing fee** for 2026, prorated by month ($185 if joining in October)
([HGAR dues schedule](https://www.hgar.com/membership/dues-schedule)) [PRIMARY]; OneKey charges a Participant
**$650 once and $190 a month per office** ([HGAR fee schedule](https://www.hgar.com/membership/fee-schedule))
[PRIMARY]; a home office counts if DOS has licensed it ([19 NYCRR 175.25(c)(6)](https://dos.ny.gov/text-17525vlmb6619))
[PRIMARY]. OneKey's own page lists a $650 branch fee and $200 agent fee where HGAR lists $450 and $225; neither
matters for a one-broker firm.

The licence question bears directly on the father-in-law's options (Q4). Under RPL §442-f he may act as a broker
without a licence, but OneKey requires a *state-issued* broker licence, so **an unlicensed attorney cannot be a
Participant, and without a Participant there is no MLS entry and therefore no portal reach** for brokered listings.
The fix is cheap: the DOS broker application says "Attorneys who are admitted to the New York State bar are exempt
from the educational, experience and examination requirements," and the fee is **$185 for a two-year licence**
([DOS-0036-f-a, Rev. 09/23](https://dos.ny.gov/real-estate-broker-application)) [PRIMARY]. If he takes the licence
but declines REALTOR membership, OneKey is still closed today. So the three cases resolve simply: unlicensed, no
MLS (K9 hit); licensed but not a REALTOR, no MLS (K9 hit); licensed and an HGAR member, full access (K9 dodged)
[INFERENCE]. A bill that passed both houses in June 2026 would lengthen the salesperson route to a broker licence
from two to four years but does not touch the attorney route ([NY Senate S8870](https://www.nysenate.gov/legislation/bills/2025/S8870))
[PRIMARY]; if signed, it makes hiring a second broker harder and the one-broker design more attractive [INFERENCE].

The Hudson Valley is split between two MLS families, and the names on the ground are confusing. OneKey's rule-
defined service area is "Dutchess, Kings (Brooklyn), Nassau, New York (Manhattan), Orange, Putnam, Queens,
Rockland, Suffolk, Sullivan, and Westchester" — **Ulster, Columbia and Greene are not in it**
([OneKey Rules 2026C, 201](https://support.onekeymls.com/hc/article_attachments/49417630758548)) [PRIMARY]. In
practice OneKey carries heavy Ulster volume (1,480 new single-family listings in the year to September 2026)
([OneKey Q3-2026 Ulster report](https://irp.cdn-website.com/a5e60d20/files/uploaded/2026_Q3_Ulster_County.pdf))
[PRIMARY], and HGAR markets OneKey as covering Ulster ([HGAR](https://www.hgar.com/membership/subscribe-to-onekey-mls))
[PRIMARY]. The former Mid-Hudson MLS in Dutchess no longer exists: OneKey "completed that conversion at the end of
January" 2024 ([RESO interview, 24 May 2024](https://www.reso.org/blog/three-questions-king/)) [SECONDARY]. North of
OneKey, the Columbia-Greene and Ulster County REALTOR boards voted in November 2024 to merge into the **Hudson
Valley Catskill Region REALTORS** ([HVCRR](https://hvcrr.com/the-association/)) [PRIMARY]. Its "Hudson Valley
Catskill Region MLS" is the old Ulster County MLS (legal name Multiple Listing Service of Ulster County, Inc.)
([listing copyright notice](https://www.villagegreenrealty.com/listings.php?sortorder=ASC-timestamp_created))
[SECONDARY], running on Flexmls since about May 2024 ([FBS](https://wearefbs.com/blog/welcome-to-four-new-flexmls-customers/))
[CLAIMED], and its reports have claimed Columbia, Dutchess, Greene, Orange, Sullivan and Ulster coverage since June
2025 ([HVCRMLS report](https://hvcrr.com/wp-content/uploads/2025/08/NYSAR_HVCRMLS_MMI_2025-06.pdf)) [PRIMARY]. HVCRR's
member login still points to the **Columbia Greene Northern Dutchess MLS** at cgndmls.com
([HVCRR member centre](https://hvcrr.com/member-center/mls/)) [PRIMARY], and 2026 listings still credit it
separately ([William Pitt listing](https://www.williampitt.com/search/real-estate-sales/167-county-route-26a-stuyvesant-ny-12173-20262774-42974027/))
[SECONDARY], so whether these are one database or two is unresolved. HVCRR publishes no fees ("call ... 845-338-5299
for correct fees") and no rules ([HVCRR join](https://hvcrr.com/the-association/join-the-board/)) [PRIMARY]. No data
share links OneKey with either; a Greene County home was seen entered separately in Global MLS and the HVCR MLS
([Compass listing](https://www.compass.com/homedetails/146-Finch-Rd-Coxsackie-NY-12042/164PBJ_pid/)) [SECONDARY].

The practical answer is to launch on OneKey alone. A OneKey Participant "shall have the option of inputting
Exclusive Listings of Property located outside of the MLS Service Area"
([OneKey Rules 2026C, 302.1](https://support.onekeymls.com/hc/article_attachments/49417630758548)) [PRIMARY], and
such "Out of Area" listings "will still syndicate to major platforms, including Zillow & Realtor.com"
([OneKey support, updated 18 Aug 2026](https://support.onekeymls.com/hc/en-us/articles/47838690968340)) [PRIMARY].
A Columbia or Greene listing entered only in OneKey would therefore reach the portals but not the HVCR/CGND members'
systems or their IDX websites; full cooperation in the northern counties needs a second membership at an unknown
price [INFERENCE].

## No write API: a person submits each listing

No New York REALTOR MLS has been shown to let a broker's own software write listings. The industry standard for
this, RESO Web API "Add/Edit", exists, and the Real Estate Board of New York's listing service was the first certified
for full-listing Add/Edit, with vendors "send[ing] their brokers' listings directly into the Add/Edit-equipped RLS"
([RESO, 22 Jan 2024](https://reso.org/blog/reso-add-edit-official)) [PRIMARY], but that is a New York City service
that does not cover the Hudson Valley. OneKey runs Cotality's Matrix, for which no listing-write route is published
([Cotality Trestle](https://www.cotality.com/products/trestle)) [CLAIMED]; the Hudson Valley Catskill Region MLS and
Global MLS run Flexmls, whose public API answers every attempt to create, change or delete a listing with "HTTP 405
(Method Not Allowed)" and gives every role "Writes: No" ([Spark API](https://www.sparkplatform.com/docs/api_services/listings))
[PRIMARY].

What OneKey added in 2026 is a better screen, not a door. **Ocusell List** went live to subscribers on 18 August
2026 ([The Close, 24 Aug 2026](https://theclose.com/news-onekey-mls-ocusell-list/)) [SECONDARY] as "a free member
benefit", with a paid "List Plus" tier for brokerages and "optional AI tools for auto-generating public remarks"
([OneKey, 5 Aug 2026](https://corporate.onekeymls.com/news/94u6jq9vsjyb9weezedz7tx26a3jmc)) [PRIMARY]. It fills up to
about 70% of a listing from public records, pushes it into Matrix in about five minutes, and warns that passing its
check "does not mean a listing has passed MLS compliance review"
([The Close](https://theclose.com/news-onekey-mls-ocusell-list/)) [SECONDARY]. OneKey also describes an "Ocusell
Aggregator" through which "Brokerages enter their listing once in Ocusell and then it aggregates out to sites through
a data feed" ([OneKey support](https://support.onekeymls.com/hc/en-us/articles/41277098013972)) [PRIMARY]; whether a
brokerage's own system may feed it is undocumented and is the one question worth asking Ocusell, because a yes would
let the software submit listings later.

Who presses the button matters less than who answers for it. OneKey lets a broker register "Administrative Users",
"unlicensed individuals who are under the direct supervision of an MLS Participant and perform only administrative
and clerical tasks" ([OneKey Rules 2026C, 205](https://support.onekeymls.com/hc/article_attachments/49417630758548))
[PRIMARY], and the Department of State lists among unlicensed assistants' tasks "Write ads for approval of broker",
"Prepare flyers and promotional information for approval by broker" and "Schedule appointments for licensees to show
listed property" ([DOS](https://dos.ny.gov/node/64166)) [PRIMARY]. But "Responsibility for the accuracy of such
information shall always remain solely with the Participant" ([OneKey Rules 2026C, 320](https://support.onekeymls.com/hc/article_attachments/49417630758548))
[PRIMARY]. A robot driving Matrix or Ocusell under a member's login is not permitted by anything found and would
invite the credential-sharing penalties MLSs impose (the CGND MLS site is quoted as imposing a $5,000 fine and
30-day suspension, seen only in a search snippet of [cgndmls.com](https://cgndmls.com/)) [CLAIMED]; the POC must not do it [INFERENCE]. No one publishes a measured time for MLS entry. An
Ocusell partner MLS says its users report "time-to-list can be under 15 minutes"
([Doorify MLS, snippet](https://doorifymls.com/news/ocusell-now-live/6962)) [CLAIMED], and Ocusell's own marketer put
the old manual entry at "an hour or more" ([Doorify podcast, snippet](https://doorify.buzzsprout.com/2186713/episodes/17019105-doorify-mls-partners-with-ocusell-for-smarter-listings))
[CLAIMED]. With the software preparing the listing in OneKey's field order, the estimate here is **15 to 60 minutes
of clerical keying plus 20 to 45 minutes of the broker's review and sign-off per listing**, including later price
and status changes [INFERENCE]; the firm should time its first ten listings.

## Seven rules that bite a flat-fee, AI-led, one-broker firm

### Clear Cooperation still binds, and New York may put it into law

OneKey's Rule 302.2 says that "Within one (1) business day after a property is publicly marketed, the listing broker
must submit the listing to the MLS", and counts "advertising on public-facing websites, brokerage website displays
(including IDX and VOW)" and "applications available to the general public" as public marketing
([OneKey Rules 2026C](https://support.onekeymls.com/hc/article_attachments/49417630758548)) [PRIMARY]. Breaking it is
a **Class 6 fine of $2,500 plus $100 for each day** it stays uncorrected (Rules 1101, 1103, 1104 Note D) [PRIMARY].
NAR kept this policy when it added "Multiple Listing Options for Sellers" on 25 March 2025, which every MLS had to
implement by 30 September 2025 and which still requires filing "within one (1) business day from public marketing"
([NAR](https://www.nar.realtor/about-nar/policies/multiple-listing-options-for-sellers)) [PRIMARY]. New York's
legislature then passed the **Fair and Transparent Real Estate Listings Act (A10679B)** in May and June 2026: listing
agents must share information with buyer agents, "respond to their inquiries", make the property available for
showings, and list it on an MLS or a free public platform unless the seller signs a state disclosure form; the
maximum licence fine rises from $2,000 to $5,000. As of 23 October 2026 it **had not been delivered to or signed by
the Governor**, and it would take effect 180 days after signing ([NY Senate A10679](https://www.nysenate.gov/legislation/bills/2025/A10679))
[PRIMARY]. For a firm that wants maximum exposure this is a tailwind, but it turns "answer every buyer agent" into a
legal duty the software must make visible [INFERENCE]. The design consequence is concrete: the firm's own website is
public marketing, so the POC must not publish a listing there until the MLS entry exists or the one-day clock is
running and visible [INFERENCE].

### Delayed marketing exists in OneKey as "MLS Only", without a time limit

OneKey implemented NAR's options on 21 January 2026 through a "Listing Exposure" field: "Publish to Internet" (feeds
to IDX and third parties), "Private" (visible only within the firm) and "MLS Only" ("only be visible within the MLS
system to other MLS Participants and Subscribers"). MLS Only needs a seller opt-out form attached first, keeps the
listing off the brokerage's own website "unless behind authentication", forbids "any internet-based public
marketing", and is "not considered publicly marketed unless transitioned to Publish to Internet"
([OneKey FAQ, updated 24 Jun 2026](https://support.onekeymls.com/hc/en-us/articles/35871094849812)) [PRIMARY]. A
"Coming Soon" status lasts at most 14 days, allows no showings by anyone, and may not be syndicated to advertising
websites, though the firm's own site, other brokers' IDX sites and social media may show it with a "Coming Soon"
notice ([OneKey Rules 2026C, 302.3](https://support.onekeymls.com/hc/article_attachments/49417630758548)) [PRIMARY].
Office exclusives must still be filed with the MLS by midnight the day after the listing date with a signed "Office
Exclusive Seller Disclosure" (303.2, 316) [PRIMARY]. On 20 October 2026 OneKey publicly rejected Compass's demand to
let it "advertise homes for sale while hiding them from the shared MLS database"
([OneKey](https://corporate.onekeymls.com/news/onekey-mls-rejects-compass-demand-defends-the-open-real-estate-marketplace))
[PRIMARY]; Compass has sued other MLSs, not OneKey ([HousingWire, 20 Oct 2026](https://www.housingwire.com/articles/onekey-compass-public-listings/))
[SECONDARY]. HVCRR's equivalent rules are unpublished.

### OneKey has no "entry-only" category, and showings must be arranged within 24 hours

Upstate MLSs let a broker flag a listing "Limited Service" or "MLS Entry Only"
([NYSAMLS rules, eff. 1 Sep 2026](https://live.bnar.webcomand.com/downloads/mlscurrentrules.pdf)) [PRIMARY], but
OneKey's rules contain no such category. They accept exclusive-agency listings flagged in a field (306.5), leave the
type of agreement "freely negotiable" (301.1), and let a listing agreement send other brokers to negotiate directly
with the seller only if "The MLS database field 'Negotiate Through' must have been set to 'Seller'" (403.2)
([OneKey Rules 2026C](https://support.onekeymls.com/hc/article_attachments/49417630758548)) [PRIMARY]. What a flat-fee
firm cannot escape is access: "Participants are required to provide reasonable access to all Listings" (404.1), and
whoever answers a showing request, "whether licensed or unlicensed, must be capable of immediately attempting to
schedule a showing", meaning "within twenty-four (24) hours" (404.4) [PRIMARY]. That last rule is good news for the
software: an unlicensed scheduler, human or automated, may answer showing requests, provided someone can actually let
the buyer in [INFERENCE]. The firm also may not call its service "free" if it is paid from any source (601.4), and
every listing needs the owner's written authorisation to appoint MLS Participants as cooperating brokers (319.4)
[PRIMARY].

### Lockboxes are optional, but keys cannot be lent; ShowingTime is included

No OneKey member must use the lockbox system (405.3); a lockbox needs the owner's written authorisation (405.4); and
a key holder must "Not loan the access device to any person for any purpose whatsoever" or disclose its PIN
(405.8(b)) ([OneKey Rules 2026C](https://support.onekeymls.com/hc/article_attachments/49417630758548)) [PRIMARY].
Without the lockbox, access must be given "by the listing agent accompanying the showing agent, client, or customer,
or by making a physical key available, or by some other means" (405.8(a)) [PRIMARY]. SentriLock costs **$130 plus
tax a year** (July to June, prorated) ([OneKey SentriLock FAQ, updated 1 Jun 2026](https://support.onekeymls.com/hc/en-us/articles/37719023138964))
[PRIMARY] and **$110 per lockbox leased** ([OneKey store](https://support.onekeymls.com/hc/en-us/articles/37497091743380))
[PRIMARY, earlier pass]. ShowingTime for the MLS "is included as part of your OneKey MLS subscription"
([OneKey support](https://support.onekeymls.com/hc/en-us/articles/27252859408020)) [PRIMARY, snippet]. For the buyer
side this means the software cannot open other brokers' listings: the attorney-broker, a hired licensee, or the
listing agent must, which partly hits assumption A6 ("showings and lockbox access ... practically require a
licensee") [INFERENCE].

### Buyer side: a written agreement before any tour, and no compensation in the MLS

Every OneKey Participant "working with a buyer must enter into a written agreement with the buyer prior to touring a
home", stating the compensation "in a manner that is objectively ascertainable and not open-ended" and barring more
from any source (402.3) ([OneKey Rules 2026C](https://support.onekeymls.com/hc/article_attachments/49417630758548))
[PRIMARY]. No offer of compensation to other brokers may appear in any MLS field, photo or attachment (502,
306.3(d)), a $250 fine with immediate deletion (1103) [PRIMARY]; a firm may still state its offer on its own website
for its own listings ([NAR settlement FAQ Q53, 29 Oct 2024](https://www.nar.realtor/sites/default/files/2024-10/nar-settlement-faq-2024-10-29.pdf))
[PRIMARY].

### Zillow's standards no longer require the MLS, but OneKey's rules do

Zillow's April 2025 Listing Access Standards required MLS entry within one business day of public marketing
([Zillow PDF, 10 Oct 2025](https://grow.zillow.com/hubfs/Zillow-Listing-Access-Standards.pdf)) [PRIMARY, superseded].
On 17 March 2026 Zillow replaced that with a test of being "broadly accessible to the general public", dropped the MLS
requirement, and kept blocking listings gated "behind a registration wall or requiring consumers to work with a
specific brokerage" ([Real Estate News, 19 Mar 2026](https://www.realestatenews.com/2026/03/19/zillows-simplified-listing-standards-make-the-mls-optional))
[SECONDARY]; ([Zillow page, snippet](https://www.zillow.com/c/info/zillow-listing-access-standards/)) [CLAIMED]. The
courts have not settled the fight behind it: Compass dropped its suit on 18 March 2026, and on 16 September 2026 a
Chicago federal judge denied Zillow's injunction against the Chicago MLS and Compass, noting that "Zillow has never
enforced its Standard in Chicagoland" ([N.D. Ill. opinion, ECF 141](https://storage.courtlistener.com/recap/gov.uscourts.ilnd.500474/gov.uscourts.ilnd.500474.141.0.pdf))
[PRIMARY]. None of this changes the firm's position: its listings will be in OneKey within a day anyway, which
satisfies both Zillow and OneKey [INFERENCE].

### Photos and copy: license them, label them, never borrow them

Submitting a listing grants OneKey a licence to "photographs, images ... descriptions, remarks, narratives" and
warrants the broker "is fully authorized to license" them (602.1); the broker also warrants the content "does not
infringe" and that it "has the written consent of any party necessary" (603); and "Participants are prohibited from
using the photographs of another Participant for marketing, listing, or promotional purposes (not including
Comparative Market Analyses), without the prior written consent of the original Listing Participant" (612.2)
([OneKey Rules 2026C](https://support.onekeymls.com/hc/article_attachments/49417630758548)) [PRIMARY]. New York's
advertising rule adds that photographs on a broker's website "shall not be used or reproduced without written
permission from the copyright holder" and that ads need "an honest and accurate description of the property"
([19 NYCRR 175.25(b)(2)(iii), (c)(9)](https://dos.ny.gov/text-17525vlmb6619)) [PRIMARY]. The cost of getting this
wrong is per photo: in VHT v. Zillow the Ninth Circuit upheld statutory damages photo by photo, $1,927,200 on remand
([Loeb & Loeb, June 2023](https://www.loeb.com/en/insights/publications/2023/06/vht-inc-v-zillow-group-inc-et-al))
[SECONDARY]. On AI-altered images, OneKey requires only that images "accurately reflect" the property (307.1)
[PRIMARY]; the Department of State warned on 13 November 2025 that "automated technology tools may produce misleading
or exaggerated representation of properties" ([DOS alert](https://apps.cio.ny.gov/apps/mediacontact/public/view.cfm?backButton=&parm=EBC83D37-EA70-CE93-3E596A7DF20C5D6A))
[PRIMARY]; and a bill requiring "A CLEAR AND CONSPICUOUS DISCLOSURE" on altered listing images sits in committee
([NY Senate S9584](https://www.nysenate.gov/legislation/bills/2025/S9584)) [PRIMARY]. The firm therefore needs a
written licence from every photographer covering MLS, portal, website and ad use, an on-image label for any virtual
staging, and a rule that its software never pulls another broker's photos or remarks into marketing [INFERENCE].
OneKey's automated checker also screens every listing and removes flagged fair-housing words such as "Family",
"Exclusive" and "Executive" ([OneKey support, Aug 2026](https://support.onekeymls.com/hc/en-us/articles/43190167691668))
[PRIMARY, earlier pass], which the POC's copy check should mirror.

## Data for the buyer side: IDX is cheap, AI training is not licensed

Pulling other brokers' listings onto the firm's own site (data OUTPUT) runs through MLS Grid, OneKey's data
distributor, under a licence that permits seven uses: IDX (public display of other brokers' listings, defined in the
licence as a cooperative "permission to display ... real-estate listings on another Member Participant's websites"),
VOW (a "virtual office website" for registered clients with a broker-consumer relationship), agent analytics,
comparative market analysis, CRM, market analytics and the firm's own listings
([MLS Grid Data License Agreement](https://www.mlsgrid.com/s/MLS-GRID-Data-License-Agreement.pdf)) [PRIMARY]. The
licence says "an automated valuation model (AVM) is considered a Comparative Market Analysis" for "a single, specific
client", bars derivative works "(other than reformatting), without the written consent of MLS GRID", bars using the
data "for unsolicited communication" or "to contact property owners except when the property owner has initiated
prior contact", and bars handing work to contractors without MLS Grid's written approval [PRIMARY]. OneKey's own rules
add that MLS information may not be passed "to any unauthorized individual, office, or firm" (605.3), that "Any
website that displays listing data must be under the control of the Participant" (607), and that feed data must be
available "for valuation purposes, including automated valuations" (605.4)
([OneKey Rules 2026C](https://support.onekeymls.com/hc/article_attachments/49417630758548)) [PRIMARY].

The decisive new text is MLS Grid's **AI Use Addendum** (file dated 12 August 2026). It "permits the use of MLS GRID
Data with AI Tools solely for (i) Permitted Search/Response Use and (ii) Permitted Marketing Use"; search use covers
"semantic and natural language searching ... conversational guidance, personalized curation" on IDX or VOW sites, and
marketing use covers "listing descriptions ... listing presentation materials" for the firm's own listings and
business. "All other use of MLS GRID Data with an AI Tool is prohibited unless an MLS provides written approval."
"AI Training" includes "the creation of vector embeddings, retrieval indices, knowledge graphs, or similar
representations that persist beyond a single user session", and "MLS GRID Data may not be cached, stored, archived or
retained by an AI Tool beyond the duration reasonably necessary to fulfill an individual user query"; broker and
vendor are "jointly and severally liable" ([MLS Grid AI Use Addendum](https://www.mlsgrid.com/s/MLS-Grid-AI-Use-Addendum.pdf))
[PRIMARY]. This corrects a claim carried in the earlier notes and in kill criterion K4: the line "express written
permission" before AI training is Metro MLS's rule as quoted by NAR
([NAR, 15 Jul 2026](https://www.nar.realtor/news/aexperience/make-it-a-policy-to-protect-mls-data-from-ai-misuse))
[SECONDARY]; NAR's own position is that AI must follow "MLS rules and data license agreements"
([NAR, 21 Oct 2025](https://www.nar.realtor/news/real-estate-news/technology/listing-app-on-ai-platform-can-help-clients-but-must-comply-with-mls-policy))
[PRIMARY]. The substance of K4 stands, and is now sharper.

| Feed (data OUTPUT) | What it gives | Terms that bind | Cost (2026) | AI and LLM rules | POC |
|---|---|---|---|---|---|
| Matrix IDX widget | A OneKey search embedded on the firm's site (up to five configured searches) | IDX rules | "at no additional cost" ([OneKey, snippet](https://support.onekeymls.com/hc/en-us/articles/31456557969556)) [PRIMARY] | Embedded OneKey code, so no AI layer of the firm's own [INFERENCE] | Not used |
| IDX feed (via an IDX vendor, or the firm as its own MLS Grid vendor) | About 98% of OneKey listings for public display, no login ([OneKey](http://corporate.onekeymls.com/benefits-data-delivery)) [PRIMARY] | MLS Grid licence and IDX Rules; attribution; site under the broker's control (607) | $20/month OneKey share via a vendor ([Showcase IDX](https://showcaseidx.com/mls-coverage/onekey-mls/)) [CLAIMED] plus vendor fee; or $250/month + $20/month per licence as own vendor ([OneKey](https://support.onekeymls.com/hc/en-us/articles/27251536794644)) [PRIMARY] | AI search and chat allowed; live per-session queries only; no persistent embeddings or retention | **Demo on fictional listings**; production stub "human required here: sign MLS Grid licence and AI addendum; OneKey approves the site" |
| VOW feed | All OneKey inventory incl. non-public fields, behind client login | VOW rules; broker-consumer relationship | Same MLS Grid fees | Same as IDX | Stub |
| Broker back-office feed | All data, login-protected | Agent-only use | Same | Same | Not in POC |
| Own-listings feed | The firm's own listings, "no usage restrictions" ([OneKey](http://corporate.onekeymls.com/benefits-data-delivery)) [PRIMARY] | "Participant Listings Use ... in any manner" (MLS Grid licence) | Included | Keep AI work on the firm's own database, not the MLS copy, to stay outside the addendum [INFERENCE] | **Automate** (own database) |
| CMA / AVM | Sold comparables for one client's valuation | AVM counts as a CMA, single client | Same feed | AI comparisons inside IDX/VOW search allowed; elsewhere ask OneKey | Demo on fictional comps |
| Portal data (Zillow, Redfin, Homes.com, Realtor.com) | Read-only APIs at MLS discretion (Zillow) or none | Terms ban scraping ([Redfin terms](https://www.redfin.com/about/terms-of-use)) [PRIMARY] | n/a | n/a | **Never scrape** |

## The cheapest compliant path, step by step

The cheapest lawful way to get a Hudson Valley listing onto every major portal is the conventional one: become a
OneKey Participant and let syndication do the rest. Every alternative either does not exist (a portal API), is closed
to brokers (Zillow FSBO), or costs more per listing (paying another flat-fee broker to list it, $399 at Hauseit
([Hauseit](https://hauseit.com/how-to-list-onekey-mls-free)) [CLAIMED], would make the other firm the listing broker
and is not the venture) [INFERENCE].

| # | Step (one-time setup) | Who | Time | Cost (2026) |
|---|---|---|---|---|
| 1 | File the DOS broker application as an admitted attorney (paper, "indicating ... that you are admitted to the New York State bar"); entity licence too if the firm is an LLC (see WS2) | Attorney-broker | Paper filing; weeks for DOS | $185 for two years ([DOS](https://dos.ny.gov/real-estate-broker-application)) [PRIMARY] |
| 2 | Join HGAR as a REALTOR (Designated REALTOR); new-member orientation | Attorney-broker | "3-5 business days" processing ([HGAR](https://www.hgar.com/membership/join-hgar/broker-owner-appraiser-realtor-membership)) [PRIMARY]; 3.5 h orientation ([HGAR application](https://member-portal-new-01-20.s3.us-east-2.amazonaws.com/Application%20-%20HGAR%20REALTOR.pdf)) [PRIMARY] | $606/yr + $100 once ([HGAR](https://www.hgar.com/membership/dues-schedule)) [PRIMARY] |
| 3 | Subscribe to OneKey as Participant; sign the EULA; OneKey orientation of up to 8 hours within 90 days (204.2) | Attorney-broker | About a day of orientation | $650 + $190/month per office ([HGAR](https://www.hgar.com/membership/fee-schedule)) [PRIMARY] |
| 4 | Set Keystone Listing Distribution: Realtor.com on- and off-market, OneKeyMLS.com and IDX all "on" | Broker | Minutes | Free |
| 5 | Register any clerical keyer as an Administrative User (205); never share the broker's login | Broker | Minutes | Free |
| 6 | Optional: SentriLock subscription and boxes; configure ShowingTime to route requests to the firm's scheduler (404.4) | Broker | An hour | $130/yr + $110 per box; ShowingTime included |
| 7 | Optional after launch: Zillow broker direct feed; claim free agent profiles on Zillow, Realtor.com, Homes.com | Broker | An hour | Free [CLAIMED] |

| # | Step (each listing) | Who | Minutes |
|---|---|---|---|
| A | Seller signs the listing agreement and agency disclosure (WS2), with written authorisations for cooperating brokers (319.4), any lockbox (405.4) and any Coming Soon/MLS Only choice; photographer's written licence on file | Broker accepts the listing (licensed act) | Counted in WS1/WS2 |
| B | Software assembles the listing in OneKey's field order and pre-checks it: Parcel ID and tax square footage, no contact details, showing notes or compensation in public remarks, fair-housing words, front photo, and the Clear Cooperation clock | Software | 0 human |
| C | Key or paste it into Ocusell List (pre-fills from public records) before midnight of the day after the listing date; front photo within 24 hours (302.1, 309.1) | Administrative User or broker | 15–60 (estimate) |
| D | Review and publish; accuracy is the broker's (320) | **Broker (licensed)** | 10–20 |
| E | Matrix updates in about 5 minutes; portals in about 24–48 hours | Automatic | 0 |
| F | Each later change: price changes in writing signed by the seller and entered within 24 hours; status changes within 24 hours (310.3, 311) | Clerical entry, broker sign-off | 10–25 over the listing's life |

Adding it up, the MLS channel costs **$3,821 in the first year** for a January start ($185 + $606 + $100 + $650 +
12 × $190) and **$2,886 a year after**, plus $185 every two years for the licence renewal [INFERENCE from the primary
schedules above]. Optional extras are SentriLock ($130 a year plus $110 per box), an IDX website ($240 a year in
OneKey data share plus the vendor's fee, or $3,240 a year as the firm's own MLS Grid vendor), and a second MLS for
Columbia and Greene at an unpublished price. Per listing, the licensed broker spends about **20 to 45 minutes** on
this channel (steps D and F), and a clerical user 15 to 60 minutes on step C; the portals themselves cost nothing and
take no time [INFERENCE]. Photography, signs and other listing costs are in WS4.

## What the proof of concept automates, stubs and skips

The POC should **automate** everything that ends before the submit button and everything the firm owns: the listing
package in OneKey's field order with RESO field names, the rule pre-check (required fields, remarks rules,
fair-housing words, photo rules, the 24-hour and one-business-day clocks), AI-written remarks and marketing copy for
the firm's own listings, the firm's own website (opened only once the MLS clock allows), draft Google Business Profile
posts, and a buyer-side AI search that runs on fictional listings in the same live-query, no-memory pattern the MLS
Grid addendum requires [INFERENCE]. It should **stub with a visible marker** the MLS submission ("human required
here: no listing-input API; a licensee or registered clerical user keys this into OneKey; the broker approves"), the
second-MLS step for Columbia and Greene, the one-time Keystone and portal-profile setup, lockbox placement, the
showing itself, and the MLS Grid licence for real IDX data. It should **skip** Zillow FSBO, Zillow Preview, any
scraping or robotic login, and Craigslist automation. The demo's strongest moment is the hand-off: the software shows
a finished, rule-checked listing, the broker clicks approve, and a status panel shows where it will appear (OneKey,
then Realtor.com, Zillow, Redfin, Homes.com, OneKeyMLS.com) and which of three switches decides it: the listing's
exposure setting, the office's distribution switches, and its status [INFERENCE]. The per-channel and per-feed lines
are in `docs/research/handoff/WS3.md`.

## Conclusion

The research turns "can software list on Zillow?" into a narrower and more useful question: can one licensed
person approve a software-prepared MLS listing in under an hour? The answer is yes, and that makes the listing
side of the venture an administration problem, not a technology or legal barrier. The portals are a solved,
free distribution layer that the firm does not need to build against; the effort belongs in the listing package and
the broker's approval screen. The binding constraints are elsewhere: the attorney must join the REALTOR system the
pitch implicitly competes with, a human must open every door, and the most valuable future feature, AI trained on
local market data, is precisely what the August 2026 data licence forbids without OneKey's written approval. Two
cheap calls would close the remaining uncertainty: to HVCRR about its northern MLS, and to Ocusell about whether a
broker's own system may feed its Aggregator, which is the only visible path to removing the human keystroke.

## Sources and method

Built from `research_notes/WS3 Listing and data access/mls_access.md` and `.../portals.md`, including the
"Gap fill (2026-10-23, VPS session)" section appended to each, with cross-checks against the WS1, WS2, WS4 and WS5
notes. The gap fill re-opened 42 load-bearing claims at their primary sources (26 MLS-side, 16 portal-side): most
were confirmed; eleven were corrected or updated (Zillow v. MRED outcome; Zillow Preview scale and mechanics;
Realtor.com no longer MLS-only for pre-market listings; Redfin's FSBO sources; Homes.com pricing; ListHub via MLS
Grid; HVCRMLS's platform; the NAR "express written permission" attribution; NAR's 2026 membership-policy repeal;
RESO's wording; the Mid-Hudson closing date). Of the 57 gaps the two notes files listed, 21 are closed, 19 partly
closed and 17 remain open; the audit also closed holes no list named (photo and copy rights, the AI addendum,
A10679B, minutes per listing). The open gaps that matter are HVCRMLS/CGND fees and rules (one call to HVCRR,
845-338-5299), the text of Zillow's current standards and feed terms (zillow.com blocked automated readers; read in a
browser), OneKey's EULA (behind the member login), whether a broker system may feed Ocusell's Aggregator, how
OneKey's data reaches Zillow, Redfin and Homes.com (IDX via MLS Grid is inferred), and the Governor's action on
A10679B. Many OneKey support pages refused normal reads and were read through OneKey's public help-centre data feed;
where only a search snippet was available, the claim is labelled [CLAIMED].
