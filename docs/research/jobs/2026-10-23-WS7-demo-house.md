# Your job: gather the demo house's facts and comparable sales (headless, 2026-10-23)

You are a headless job in /root/projects/realestate. Joe signed off the POC success criteria today
(`docs/SUCCESS-CRITERIA.md`, read it) and chose a real Hudson Valley address as the demo house: **146 Rt 292, Holmes, NY 12531** (Dutchess
County; it replaces an earlier Virginia address; decisions 14 and 17 in `docs/DECISIONS.md`). Your job is
the property data only.
Other jobs are running in parallel in this working tree: **do not run any git command that changes state
(no add, commit, push, stash, checkout)** and write only the two files below.

## Rules (from CLAUDE.md; they matter here)
- Use official public records: Dutchess County's parcel and real property tax services (e.g. Dutchess
  County Parcel Access / GIS), the town assessor's assessment roll (confirm which town Holmes falls in for
  this parcel: likely Pawling or Beekman), New York State ORPTS data (assessment rolls, sales data, RP-5217
  sales where public), data.ny.gov datasets, the County Clerk's public indexes, FEMA flood maps, and other
  government sources. Read
  public pages normally. **Never use or scrape Zillow, Redfin, Realtor.com, Homes.com or any MLS**, and never
  copy listing photos or listing descriptions from anyone.
- **PII:** never record an owner's or buyer's name, for the demo house or for any comparable. Addresses, unit
  numbers, sale dates and prices from official records are fine (they are what a real comparative market
  analysis uses).
- Cite every fact with its source URL and the date you accessed it (2026-10-23). If a fact is not in an
  official record, leave it blank and say so; never guess. Label anything derived [INFERENCE].

## What to find
1. **The demo house:** property class (NY property class code), property type (detached, townhouse, condo; building or complex name if any), year
   built, living area, lot size if any, bedrooms, bathrooms, stories, parking, heating/cooling, notable
   features recorded, current assessed value (land and improvements, by year for the last 3 years), last
   recorded sale date and price, zoning, condo or HOA association if recorded, and the official parcel ID.
2. **Comparable sales:** at least 5, ideally 8, arm's-length sales from the last 12 to 18 months of the most
   similar properties nearby (same building or complex first, then the same neighbourhood), from official
   sales records. For each: address (unit if any), sale date, price, type, year built, living area, beds and
   baths where recorded, and why it is comparable. Note any sale that looks non-arm's-length and exclude it.
3. **Neighbourhood facts usable in listing copy** (property and place, never people, to stay within fair
   housing rules): distances to the nearest Metro-North station (Harlem Line), major roads (I-84, Route 22,
   Taconic), lakes, parks, the Appalachian Trail, shopping, from official or map sources; the public school
   district name only as a fact (no "great schools" claims); flood zone; whether the property is on well and
   septic if recorded (these drive NY disclosures).

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
