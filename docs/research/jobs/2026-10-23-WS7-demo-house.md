# Your job: gather the demo house's facts and comparable sales (headless, 2026-10-23)

You are a headless job in /root/projects/realestate. Joe signed off the POC success criteria today
(`docs/SUCCESS-CRITERIA.md`, read it) and chose his real address as the demo house: **4910 John Ticer Dr,
Alexandria, VA** (decisions 14 and 17 in `docs/DECISIONS.md`). The product's legal flow is New York's; the
demo labels state-specific steps "New York rules (launch market)". Your job is the property data only.
Other jobs are running in parallel in this working tree: **do not run any git command that changes state
(no add, commit, push, stash, checkout)** and write only the two files below.

## Rules (from CLAUDE.md; they matter here)
- Use official public records: the City of Alexandria real estate assessment search, the City's open data
  portal (sales and assessment datasets), Virginia or Alexandria GIS, and other government sources. Read
  public pages normally. **Never use or scrape Zillow, Redfin, Realtor.com, Homes.com or any MLS**, and never
  copy listing photos or listing descriptions from anyone.
- **PII:** never record an owner's or buyer's name, for the demo house or for any comparable. Addresses, unit
  numbers, sale dates and prices from official records are fine (they are what a real comparative market
  analysis uses).
- Cite every fact with its source URL and the date you accessed it (2026-10-23). If a fact is not in an
  official record, leave it blank and say so; never guess. Label anything derived [INFERENCE].

## What to find
1. **The demo house:** property type (detached, townhouse, condo; building or complex name if any), year
   built, living area, lot size if any, bedrooms, bathrooms, stories, parking, heating/cooling, notable
   features recorded, current assessed value (land and improvements, by year for the last 3 years), last
   recorded sale date and price, zoning, condo or HOA association if recorded, and the official parcel ID.
2. **Comparable sales:** at least 5, ideally 8, arm's-length sales from the last 12 to 18 months of the most
   similar properties nearby (same building or complex first, then the same neighbourhood), from official
   sales records. For each: address (unit if any), sale date, price, type, year built, living area, beds and
   baths where recorded, and why it is comparable. Note any sale that looks non-arm's-length and exclude it.
3. **Neighbourhood facts usable in listing copy** (property and place, never people, to stay within fair
   housing rules): distances to the nearest Metro station, major roads, parks, trails, shopping, from
   official or map sources; the public school district name only as a fact (no "great schools" claims).

## Write
- `docs/specs/demo-house.md`: plain-language summary for Joe and the build, a facts table with sources, the
  comparables table with sources, a short note on the price range the comparables suggest (show the
  arithmetic, label it [INFERENCE]; the demo's pricing step is a broker-reviewed suggestion, never a set price),
  and a "Gaps" list of anything not found.
- `fixtures/demo_house.json`: the same facts as structured data the app will load: `{"property": {...},
  "sources": {...}, "comparables": [{...}], "neighbourhood": [{...}], "gaps": [...], "retrieved": "2026-10-23"}`,
  with each value's source key so the intake screen can tag every field with where it came from.

## Done when
Both files are written. Final reply (under 10 lines): property type, beds/baths/size, number of comparables,
the suggested range, and the gaps.
