# Demo house: 146 Route 292, Holmes, NY 12531 (Dutchess County)

Gathered 2026-10-23 from public records only (county, state and federal sources, plus OpenStreetMap routing
for driving distances). No portal or MLS was used, no photos or listing text were copied, and **no owner's or
buyer's name is recorded here or in the fixture**. The structured version the app loads is
`fixtures/demo_house.json`; every value there carries a source key from the Sources list at the end of this
page. Labels: [PRIMARY] = read from an official record; [INFERENCE] = worked out by us from official data;
[SECONDARY] = official data served through a third party.

## In plain words

- **What it is:** a detached one-family house in the raised-ranch style, built in 1995, on 4.18 acres in the
  hamlet of Holmes, Town of Pawling, Dutchess County. Not a condo; no homeowners' association is recorded.
- **Size and rooms (assessor's record):** 2,520 sq ft of living area plus an 840 sq ft finished basement,
  3 bedrooms, 3 full bathrooms, 1 kitchen. Oil-fired hot-water heat; no central air recorded. Private well
  and private septic. A 400 sq ft deck or open porch and two sheds. No garage is recorded.
- **Assessment (2026 final roll):** $161,700 (land $37,800). New York's equalisation rate for Pawling turns
  that into a "full market value" of $591,200. That number is the state's formula, not an appraisal.
- **Last sale:** none at market on the current record. The last transfer (9 April 2021) was for $0 and is
  coded as one where a buyer was also a seller, so it is not a market sale.
- **Place:** flood zone X (minimal flood hazard); zoning HA (Hamlet Area); Pawling Central School District.
  Patterson's Metro-North station is about 2.8 miles by road; I-84 (Exit 58) about 2.8 miles; Wonder Lake
  State Park about 0.9 miles away in a straight line.
- **Comparable sales:** 8 market sales from April 2025 to June 2026, 0.8 to 3.8 miles away, $525,000 to
  $769,000, all from Dutchess County's official sales records.
- **What they suggest [INFERENCE]:** roughly **$610,000 to $650,000** for the broker to review (the working
  is in section 4). The demo's pricing step shows this as a suggestion with a broker checkpoint; the AI never
  sets the price.
- **Biggest gaps:** garage or parking, interior condition and recent updates, the age of the roof, septic,
  well and oil tank, whether part of the pond is on the lot, the annual tax bill, and the last market sale
  price. The demo's seller persona fills these on the intake screen, tagged "seller".

## 1. The house: facts from the record

| Field | Value | Label | Source |
|---|---|---|---|
| Address | 146 Route 292, Holmes, NY 12531 | PRIMARY | `dutchess_rps_2026`, `nys_parcel_centroids` |
| Town (assessing unit) | Town of Pawling (SWIS 134089, outside the village) | PRIMARY | `dutchess_rps_2026` |
| Hamlet | Holmes (state place point 0.10 mi from the parcel centre) | PRIMARY | `nys_place_points` |
| Official parcel ID | SWIS 134089, print key **6855-02-833559-0000** (county parcel grid 13408900685500028335590000) | PRIMARY | `dutchess_rps_2026`, `dutchess_parcels_gis` |
| Property class | **210, One Family Year-Round Residence** | PRIMARY | `dutchess_rps_2026`, `nys_open_roll` |
| Property type | Detached single-family house; no building or complex name | INFERENCE (class 210, raised-ranch style, 4.18-acre lot, no condo flag) | `dutchess_rps_2026`, `dutchess_property_card` |
| Building style | Raised ranch (style code 02) | PRIMARY | `dutchess_property_card` |
| Year built | 1995 (no remodel year recorded) | PRIMARY | `dutchess_property_card` |
| Living area | 2,520 sq ft (assessor's square feet of living area) | PRIMARY | `dutchess_property_card`, `nys_parcel_centroids` |
| Basement | Full basement, 840 sq ft finished (recorded separately from living area) | PRIMARY | `dutchess_property_card` |
| Stories | 1 (as recorded for a raised ranch) | PRIMARY | `dutchess_property_card` |
| Bedrooms | 3 | PRIMARY | `dutchess_property_card` |
| Bathrooms | 3 full, 0 half | PRIMARY | `dutchess_property_card` |
| Kitchens | 1 | PRIMARY | `dutchess_property_card` |
| Fireplaces | 0 | PRIMARY | `dutchess_property_card` |
| Heating | Hot water/steam, oil fuel | PRIMARY | `dutchess_property_card` |
| Cooling | No central air recorded | PRIMARY | `dutchess_property_card` |
| Water supply | Private (well) | PRIMARY | `dutchess_property_card` |
| Sewer | Private (septic) | PRIMARY | `dutchess_property_card` |
| Utilities | Electric | PRIMARY | `nys_parcel_centroids` |
| Lot size | 4.18 acres ("4.18 Ac (S)" on the roll); the county's GIS parcel outline measures 4.19 acres | PRIMARY; GIS area is INFERENCE | `dutchess_rps_2026`, `dutchess_parcels_gis` |
| Other improvements | Open porch/deck 400 sq ft (1995); machine shed 300 sq ft (2014); machine shed 100 sq ft (2014) | PRIMARY | `dutchess_property_card` |
| Parking / garage | **Not recorded** (no garage on the improvements list) | gap | `dutchess_property_card` |
| Quality and condition | Grade C (Average); condition Normal; site desirability Typical | PRIMARY | `dutchess_property_card` |
| Zoning | **HA, Hamlet Area** (Town of Pawling). The county zoning map puts 4.18 of the 4.19 GIS acres in HA; a 0.01-acre sliver of R-4 at the edge is a mapping artefact. No zoning overlay district. | PRIMARY (zone); INFERENCE (split) | `dutchess_zoning`, `dutchess_property_card` |
| Agricultural district | None | PRIMARY | `dutchess_rps_2026` |
| Condo or HOA | No condominium recorded; the assessment roll does not track HOAs, and none is recorded | PRIMARY (no condo); gap (HOA) | `dutchess_rps_2026` |
| School district | Pawling Central School District (code 134001) | PRIMARY | `dutchess_rps_2026`, `nys_open_roll` |
| Roll section | 1 (taxable) | PRIMARY | `dutchess_rps_2026` |
| Last recorded transfer | 2021-04-09, **$0**, condition code **C** ("one of the buyers is also a seller"), sale type 3 (land and building), 1 parcel, deed book 22021 page 51453. **Not a market sale.** | PRIMARY (code meaning from the state's RP-5217 instructions) | `dutchess_rps_2026`, `rp5217_instructions` |
| Last market sale | Not on the current record | gap | `dutchess_rps_2026` |
| Flood zone | FEMA zone **X**, "Area of minimal flood hazard"; not a special flood hazard area (FIRM DFIRM_ID 36027C). The whole parcel falls in zone X. | PRIMARY (FEMA data via the county's layer) | `dutchess_flood` |
| Mapped wetlands and water | No state (DEC) wetland mapped on the parcel. The federal National Wetlands Inventory maps stream channels (one perennial, one intermittent) and a freshwater pond touching it. The state's water map shows a pond of about 2.5 acres at the lot's edge, about 13% of which (about a third of an acre) falls inside the mapped parcel lines. | PRIMARY (layers); INFERENCE (share inside the lot) | `dutchess_wetlands`, `nys_hydro` |
| Well report on file | None found in the county's well-report records | PRIMARY | `dutchess_wells` |
| Coordinates (parcel centre) | 41.523196, -73.645089 | PRIMARY | `nys_parcel_centroids` |

## 2. Assessed value by year

The assessed value has not changed since at least the 2021 roll, because Pawling assesses at a fraction of
market value and has not reassessed. The "full market value" moves only because the state's equalisation
rate changes. Improvements = total minus land [INFERENCE: subtraction].

| Roll year | Land AV | Total AV | Improvements (derived) | Equalisation rate | Full market value | Source |
|---|---|---|---|---|---|---|
| 2026 (final, 2026-07-01) | $37,800 | $161,700 | $123,900 | 27.35% | **$591,200** | `dutchess_rps_2026` |
| 2025 | $37,800 | $161,700 | $123,900 | 29.61% | $546,100 | `nys_open_roll`, `nys_equalization` |
| 2024 | $37,800 | $161,700 | $123,900 | 31.36% | $515,600 | `nys_open_roll`, `nys_equalization` |
| 2023 (context) | $37,800 | $161,700 | $123,900 | 32.78% | $493,300 | `nys_open_roll`, `nys_equalization` |

Check: $161,700 ÷ 0.2735 = $591,225, which rounds to the $591,200 on the record. Pawling's 2025 residential
coefficient of dispersion is 12.96, so individual assessments in the town sit on average about 13% away from
the town's typical level (`nys_equity_stats`). The full market value is therefore only a rough guide.

## 3. Comparable sales

**Where they come from.** Dutchess County's ParcelAccess "Residential Sales" search, run for one-family
(class 210) sales dated 2025-04-23 to 2026-10-23 in the Town of Pawling, Village of Pawling, Beekman, East
Fishkill, Union Vale and Dover. It returned 545 sales; the newest is dated 2026-06-23, so the county's sales
data runs about four months behind. Every one of the 545 carried RP-5217 condition code **J** ("None" of the
unusual conditions), so none was flagged as non-arm's-length. Each chosen sale was re-checked on the county's
property record: single-parcel sale, code J, deed book and page present. Distances are straight lines between
parcel centres from the state's parcel points [INFERENCE: computed].

**How they were chosen.** One-family houses of 1,900 to 3,300 sq ft, built 1976 to 2010, on 1 acre or more,
with private wells and septic as far as possible, nearest first. Six are in the Pawling Central School
District like the house; seven share its 12531 ZIP. The 2026 building details are today's assessor record and
may postdate the sale.

| # | Address | Town | Miles | Sale date | Price | Style | Built | Living sq ft | Beds | Baths (full/half) | Acres | $ per sq ft |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 561 Route 292, 12531 | Pawling | 0.94 | 2026-03-12 | $715,000 | Ranch, 1 story | 1988 | 2,456 | 4 | 4/0 | 1.04 | $291.12 |
| 2 | 10 Stonewall Dr, 12531 | Pawling | 0.80 | 2025-07-31 | $769,000 | Colonial, 2 story | 1992 | 3,216 | 3 | 3/1 | 2.30 | $239.12 |
| 3 | 195 S White Rock Rd, 12531 | Pawling | 1.51 | 2025-08-27 | $685,000 | Contemporary, 2 story | 1985 | 3,089 | 3 | 2/1 | 6.55 | $221.75 |
| 4 | 10 Andreas Ct, 12531 | East Fishkill | 1.87 | 2025-12-16 | $635,000 | Colonial, 2 story | 2002 | 2,544 | 4 | 2/1 | 2.00 | $249.61 |
| 5 | 26 W Forest Trl, 12531 | East Fishkill | 2.18 | 2026-04-15 | $664,500 | Colonial, 2 story | 1999 | 2,354 | 4 | 3/1 | 1.44 | $282.29 |
| 6 | 331 Grape Hollow Rd, 12531 | Beekman | 2.77 | 2026-04-24 | $750,000 | Cape Cod, 1.7 story | 1992 | 2,555 | 4 | 2/1 | 3.22 | $293.54 |
| 7 | 226 White Pond Rd, 12582 | East Fishkill | 3.81 | 2026-06-08 | $638,500 | Raised ranch, 1 story | 1976 | 2,849 | 3 | 2/0 | 1.00 | $224.11 |
| 8 | 16 Mountain View Dr, 12531 | Pawling | 2.02 | 2025-09-25 | $525,000 | Raised ranch, 1 story | 1979 | 1,973 | 3 | 2/0 | 2.85 | $266.09 |

All eight are detached one-family houses (class 210 [PRIMARY]; "detached" [INFERENCE] from style and lot
size). Source for every row: `dutchess_sales_search` (sale date, price, condition, building data),
`dutchess_property_card` (deed, assessment, improvements), `nys_parcel_centroids` (location, ZIP).

**Why each is comparable, and how it differs**

1. **561 Route 292:** same road, same town, school district and ZIP; nearly the same living area (2,456 vs
   2,520 sq ft); one story; well and septic; average grade. Differs: smaller lot, 4 bedrooms and 4 full
   baths, central air, electric heat, a fireplace. Deed 22026/50962. Pawling CSD.
2. **10 Stonewall Dr:** the nearest similar sale (0.8 mi); built 1992; 3 bedrooms and 3 full baths like the
   house; oil hot-water heat; well and septic. Differs: larger two-story colonial, central air, fireplace,
   covered porch, generator; site rated "Superior". Deed 22025/52588. Pawling CSD.
3. **195 S White Rock Rd:** same town, school district and ZIP; a big lot (6.55 acres) like the house's;
   oil hot-water heat; well and septic. Differs: larger two-story contemporary, detached one-car garage,
   central air, fireplace. Deed 22025/53043. Pawling CSD.
4. **10 Andreas Ct:** almost the same living area (2,544 sq ft); no central air, like the house; oil
   hot-water heat; well and septic; 2 acres; same ZIP and school district. Differs: two-story colonial,
   newer (2002), 4 bedrooms and 2.5 baths, fireplace. Deed 22025/54585. Pawling CSD.
5. **26 W Forest Trl:** similar size and age band (1999); finished basement (779 sq ft) like the house's;
   same ZIP; well and septic. Differs: two-story colonial, attached one-car garage, central air, fireplace,
   Carmel CSD. Deed 22026/51371.
6. **331 Grape Hollow Rd:** close in size (2,555 sq ft) and age (1992); 3.22 acres; no central air; oil
   hot-water heat; well and septic; same ZIP and school district. Differs: Cape Cod style, crawl space
   rather than a full basement, two fireplaces, 4 bedrooms and 2.5 baths. Deed 22026/51562. Pawling CSD.
7. **226 White Pond Rd:** the same style (raised ranch) at a similar size (2,849 sq ft) with a large finished
   basement (1,006 sq ft); no central air; oil hot-water heat; well and septic. Differs: older (1976), 1 acre,
   2 full baths, enclosed porch and decks, Carmel CSD, ZIP 12582. Deed 22026/52090.
8. **16 Mountain View Dr:** the same style (raised ranch), same town and school district, 3 bedrooms, finished
   basement (764 sq ft), 2.85 acres, oil hot-water heat. Differs: smaller (1,973 sq ft), older (1979), 2 full
   baths, central air, public water, above-ground pool; site rated "Superior". Deed 22025/53407. Pawling CSD.

**Considered and not used**

| Address | Sale | Why not used |
|---|---|---|
| 873 Route 292, Pawling (1.58 mi) | 2025-05-27, $860,000; contemporary, 3,087 sq ft, 1990, 7.14 ac | Higher quality grade ("Good"), attached 1.5-car garage, 910 sq ft deck, pool, propane hot-air heat. A clear upper bracket ($278.59/sq ft), not a like-for-like comparable. |
| 916 Route 216, Beekman (5.50 mi) | 2026-01-20, $626,000; raised ranch, 2,388 sq ft, 1986, 3 beds, 3 full baths | Good style match ($262.14/sq ft) but farther away, ZIP 12570, Arlington CSD. First alternate. |
| 140 Milltown Rd, East Fishkill (3.28 mi) | 2025-06-12, $650,000; contemporary, 3,252 sq ft, 1989, 5.28 ac | Much larger house ($199.88/sq ft). Second alternate. |
| 391 and 379 S White Rock Rd, Pawling (0.59 and 0.66 mi) | 2025-07-30 $510,000 (1951 Cape, 1,834 sq ft); 2026-05-08 $689,500 (2023 split level, 1,822 sq ft) | Nearest sales, but too different in age and size. |
| 146 Route 292 itself | 2021-04-09, $0, condition C | **Excluded: not arm's-length** (a buyer was also a seller). |

No other non-arm's-length sale turned up: the county search returned only code J sales.

## 4. The price range the comparables suggest [INFERENCE]

This is the arithmetic behind the demo's pricing step. It is a suggestion for the broker's review checkpoint,
never a set price. The house: 2,520 sq ft of living area.

**Method A, price per square foot, all 8 sales.** Sorted: $221.75, $224.11, $239.12, $249.61, $266.09,
$282.29, $291.12, $293.54.
- Median = ($249.61 + $266.09) ÷ 2 = **$257.85** per sq ft. $257.85 × 2,520 = **$649,782**.
- Middle half (quartiles, inclusive method): $235.37 to $284.50 per sq ft, so $593,123 to $716,928. This is
  the wider evidence band.

**Method B, the same style only (the two raised ranches, #7 and #8).** ($224.11 + $266.09) ÷ 2 = $245.10 per
sq ft. $245.10 × 2,520 = **$617,652**. Only two sales, so weak on its own.

**Method C, the town's own assessment as a yardstick (the four Pawling sales, same roll, same 27.35%
rate).** Sale price ÷ 2026 full market value: #1 715,000 ÷ 694,700 = 1.0292; #2 769,000 ÷ 744,100 = 1.0335;
#3 685,000 ÷ 653,000 = 1.0490; #8 525,000 ÷ 508,200 = 1.0331. Median 1.0333 × the house's $591,200 =
**$610,864**. A cross-check only: Pawling's assessments scatter by about 13% (section 2), and the method
cannot be used across towns (Beekman's 57.48% rate, for example, gives #6 a ratio of 1.66).

**Suggested range for the broker: $610,000 to $650,000**, from the lowest to the highest of the three
results, rounded to the nearest $10,000. Midpoint about $630,000.

What would move it, for the broker to weigh (none of this is adjusted in the numbers above):
- **Up:** the 4.18-acre lot (larger than all but one comparable); 3 full baths; the 840 sq ft finished
  basement; any pond frontage, if confirmed; updates the seller reports.
- **Down:** no central air recorded; oil heat; no garage recorded; the raised-ranch style; frontage on a state
  route; condition unknown until seen.
- **Time:** Pawling's equalisation rate fell from 29.61% to 27.35% between the 2025 and 2026 rolls, which
  implies about 8% town-wide value growth between valuation dates (29.61 ÷ 27.35 = 1.083). Sales from mid-2025
  may therefore understate today's level by a few percent. Not adjusted here; the broker's call.

## 5. Neighbourhood facts for listing copy

Places and distances only, never people. The school district appears as a name only, with no claims about
quality. Several nearby lakes have private lake communities, so copy must not suggest the house has lake
access unless the seller documents it. "Straight" = straight-line miles from the parcel centre [INFERENCE:
computed from official coordinates]. "Drive" = OpenStreetMap routing on the OSRM server, free-flow, rounded
[INFERENCE].

| Fact | Straight | Drive | Source |
|---|---|---|---|
| Patterson station, Metro-North Harlem Line (filed in the MTA's list under the line's Wassaic branch) | 2.26 mi | 2.8 mi, about 6 min | `mta_stations`, `osrm` |
| Pawling station, Metro-North Harlem Line | 3.68 mi | 7.3 mi, about 14 min | `mta_stations`, `osrm` |
| Southeast station (Brewster), Metro-North Harlem Line | 7.66 mi | 9.8 mi, about 21 min | `mta_stations`, `osrm` |
| I-84 Exit 58, Ludingtonville Road | 2.11 mi | 2.8 mi, about 9 min | `nys_exits`, `osrm` |
| I-84 Exit 61, Route 311 | 3.4 mi | 5.8 mi, about 12 min | `nys_exits`, `osrm` |
| Route 22 (nearest point, in Patterson) | 2.79 mi | 3.7 mi, about 7 min | `nys_streets`, `osrm` |
| Taconic State Parkway at I-84 (Taconic exit 37) | 6.6 mi | 10.2 mi, about 19 min | `nys_exits`, `osrm` |
| The house fronts NY Route 292, a numbered state route | 0.04 mi | n/a | `nys_streets` |
| Wonder Lake State Park (state park, 1,189 acres, open to the public) | 0.90 mi to the park boundary | not computed | `padus` |
| Great Swamp Wildlife Management Area (NYS DEC) | 2.27 mi | not computed | `padus` |
| Appalachian Trail | 3.59 mi to the trail | nearest official A.T. parking: NY Route 55 lot 6.0 mi (about 11 min); Stormville Mountain Rd 5.6 mi (about 15 min) | `nps_at_centerline`, `nps_at_facilities`, `osrm` |
| Denton Lake | 0.40 mi | not computed | `nys_hydro` |
| Lake Dutchess | 1.20 mi | not computed | `nys_hydro` |
| Whaley Lake (about 264 acres) | 1.97 mi | 2.9 mi to the Whaley Lake hamlet point, about 6 min | `nys_hydro`, `nys_place_points`, `osrm` |
| Village of Pawling centre (shops, services) | 3.70 mi | 7.1 mi, about 13 min | `nys_place_points`, `osrm` |
| Nearest full-size grocery stores (state-licensed, 15,000 sq ft or more) | DeCicco & Sons, Brewster 7.24 mi; Stop & Shop, Hopewell Junction 7.68 mi | 8.9 mi and 9.5 mi, about 17 min each | `nys_food_stores`, `osrm` |
| Smaller stores nearby | Dollar Tree, Route 22, Patterson 2.83 mi; Dollar General, Route 22, Pawling 2.97 mi | not computed | `nys_food_stores` |
| Public school district (name only) | Pawling Central School District | n/a | `dutchess_rps_2026` |
| Flood zone | FEMA zone X, minimal flood hazard | n/a | `dutchess_flood` |
| Water and sewer | Private well and private septic | n/a | `dutchess_property_card` |

## 6. Facts that drive New York disclosures and checks

- **Well and septic (private water, private sewer):** the Property Condition Disclosure Statement asks about
  both. No well completion report is on file with the county. [PRIMARY record; the disclosure link is
  INFERENCE]
- **Flood zone X:** outside FEMA's special flood hazard area; the disclosure statement's flood questions still
  need the seller's answers on past flooding and insurance. [PRIMARY zone; INFERENCE on use]
- **Built 1995:** after 1978, so the federal lead-based paint disclosure for pre-1978 housing does not apply.
  [INFERENCE from the year built]
- **Not in an agricultural district:** the agricultural-district notice is not triggered. [PRIMARY: no ag
  district on the record; INFERENCE on the notice]
- **New York City water-supply watershed:** the federal watershed map puts the house in the Muddy Brook
  sub-watershed of the East Branch Croton River (`usgs_wbd`), and NYC DEP says the East Branch watershed
  "includes portions of the Towns of Patterson and Southeast in Putnam County and Pawling in Dutchess County"
  (`nyc_dep_east_branch`). So the lot is very likely inside the NYC watershed, where NYC DEP rules govern
  septic repairs and replacements. [INFERENCE; confirm on DEP's watershed map]
- **Oil heat:** the location of the fuel tank (above or below ground) is not in any record. Ask the seller.

## 7. Gaps (not found in an official record; left blank, never guessed)

1. **Last market sale price.** The county record keeps only the latest transfer (2021, $0, not at market).
   The roll's description field also carries "1963 0108 1328 0654", which look like older deed book and page
   references [INFERENCE]; they were not looked up. The County Clerk's index was not searched because it
   lists party names.
2. **Parking and garage.** None recorded. Raised ranches often have a garage under the house, but that is
   not on the record. Ask the seller.
3. **Central air:** recorded as none. **Bathrooms:** 3 full and 0 half as recorded. Confirm both with the seller.
4. **How the living area was measured:** whether 2,520 sq ft includes the raised ranch's lower level. The
   840 sq ft finished basement is recorded separately. Confirm at measurement.
5. **Interior condition and updates** (kitchen, baths, roof, windows), **well** yield and water quality,
   **septic** age and last pumping, **oil tank** location. None of this is in public records.
6. **HOA:** the roll does not track associations. None is recorded; confirm with the seller.
7. **The pond:** how much is on the lot and any rights to it. GIS overlay only; needs the deed or a survey.
8. **Annual property tax bill:** not retrieved (taxable value $161,700 for county, town and school; rates
   not looked up).
9. **FEMA panel number and effective date:** FEMA's own map server (hazards.fema.gov) refused connections
   from this server. The zone comes from FEMA's DFIRM data (36027C) as served by Dutchess County.
10. **NYC watershed status:** inferred from USGS and DEP sources. Confirm on DEP's map.
11. **Putnam County sales:** the house is about 2 miles from Patterson, Putnam County, but only Dutchess
    records were searched. Putnam sales would sharpen the comparables.
12. **Sales after about June 2026:** not yet in the county's sales data (newest record: 2026-06-23).
13. **Building permits and certificates of occupancy:** the Town of Pawling building department was not checked.
14. **Special district code PF021** on the record: meaning not looked up.
15. **Photos:** none collected, by rule. The county shows assessor photos; the demo must use seller-supplied
    or placeholder images.

## 8. Notes for the build

- `fixtures/demo_house.json` mirrors this page. Every property field is an object with `value`,
  `provenance` (`public_record`, `inferred` or `not_in_record`), `label` and `source`. The intake screen tags
  each field from `provenance`. `not_in_record` fields are the ones the seller persona fills on screen,
  tagged "seller".
- `comparables` holds the 8 sales used; `comparables_considered` holds the alternates and the exclusion.
  `cma_reference` holds the arithmetic above, so a test can check that the pricing module reproduces
  $649,782, $617,652 and $610,864.
- The fixture holds no names, mailing addresses, mortgage or bank codes, or owner exemption details. Keep it
  that way: success criteria section 2 (PII) and CLAUDE.md.

## Sources (all accessed 2026-10-23)

| Key | Source | URL |
|---|---|---|
| `dutchess_rps_2026` | Dutchess County Real Property Tax Service Agency, ParcelAccess: parcel record from the 2026 final assessment roll (filed 2026-07-01) | https://gis.dutchessny.gov/parcelaccess/?parcelgrid=13408900685500028335590000 (data call: `https://gis.dutchessny.gov/parcelaccess/asp/search_extract_parcelgrids.asp`) |
| `dutchess_property_card` | Dutchess County ParcelAccess property card: site, residential building and improvement records | https://gis.dutchessny.gov/parcelaccess/property-card/?parcelgrid=13408900685500028335590000&parcelid=61038 (data calls: `asp/get_property_details.asp`, `asp/get_property_improvements.asp`) |
| `dutchess_sales_search` | Dutchess County ParcelAccess "Residential Sales" search: class 210, sales 2025-04-23 to 2026-10-23, SWIS 134089, 134001, 132200, 132800, 135400, 132600 | https://gis.dutchessny.gov/parcelaccess/ (Search > Sales; data call `asp/search_residential_sales.asp`) |
| `dutchess_parcels_gis` | Dutchess County ParcelAccess_Public map service, parcels layer | https://gis.dutchessny.gov/server/rest/services/ParcelAccess_Public/MapServer/3 |
| `dutchess_flood` | Dutchess County ParcelAccess_Public, layer 36 "DFIRM Flood Hazard Areas" (FEMA DFIRM 36027C) | https://gis.dutchessny.gov/server/rest/services/ParcelAccess_Public/MapServer/36 |
| `dutchess_wetlands` | Dutchess County ParcelAccess_Public, layers 37 (NWI wetlands) and 38 (DEC wetlands) | https://gis.dutchessny.gov/server/rest/services/ParcelAccess_Public/MapServer/37 |
| `dutchess_zoning` | Dutchess County zoning map service, layers 9 (zoning) and 4 (overlays) | https://gis.dutchessny.gov/zoning/?parcelgrid=13408900685500028335590000 ; https://gis.dutchessny.gov/server/rest/services/Zoning/MapServer/9 |
| `dutchess_wells` | Dutchess County ParcelAccess well-report lookup (returned no records) | https://gis.dutchessny.gov/parcelaccess/asp/search_private_wells.asp?parcelgrid=13408900685500028335590000 |
| `nys_open_roll` | NYS Dept. of Taxation and Finance (ORPTS), "Property Assessment Data from Local Assessment Rolls", Open NY dataset 7vem-aaz7 (roll years 2021 to 2025) | https://data.ny.gov/resource/7vem-aaz7.json?county_name=Dutchess&print_key_code=6855-02-833559-0000 |
| `nys_parcel_centroids` | NYS ITS GIS, NYS Tax Parcel Centroid Points (2025 roll; utilities, coordinates) | https://gisservices.its.ny.gov/arcgis/rest/services/NYS_Tax_Parcel_Centroid_Points/FeatureServer/0 |
| `nys_equalization` | ORPTS equalization rates, Open NY dataset e6pv-77bh | https://data.ny.gov/resource/e6pv-77bh.json?swis_code=134000 |
| `nys_equity_stats` | ORPTS assessment equity statistics by municipality, Open NY dataset 4sut-q3dt | https://data.ny.gov/resource/4sut-q3dt.json?swis_code=134000 |
| `rp5217_instructions` | NYS Tax Dept., RP-5217-PDF Real Property Transfer Report Instructions (Rev. 06/13), item 15 conditions of sale | https://www.tax.ny.gov/pdf/current_forms/orpts/rp5217pdfins.pdf |
| `mta_stations` | MTA Rail Stations, Open NY dataset wxmd-5cpm | https://data.ny.gov/resource/wxmd-5cpm.json?railroad=MNR |
| `nys_exits` | NYS ITS GIS, NYS Streets, Exit layer | https://gisservices.its.ny.gov/arcgis/rest/services/NYS_Streets/MapServer/1 |
| `nys_streets` | NYS ITS GIS, NYS Streets, street segments | https://gisservices.its.ny.gov/arcgis/rest/services/NYS_Streets/MapServer/4 |
| `nys_hydro` | NYS ITS GIS, NYS Hydrography, waterbodies | https://gisservices.its.ny.gov/arcgis/rest/services/NYS_Hydrography/MapServer/9 |
| `nys_place_points` | NYS ITS GIS, NYS Place Points | https://gisservices.its.ny.gov/arcgis/rest/services/NYS_Place_Points/MapServer/0 |
| `nys_food_stores` | NYS Dept. of Agriculture and Markets, Retail Food Stores, Open NY dataset 9a8c-vfzj | https://data.ny.gov/resource/9a8c-vfzj.json |
| `padus` | USGS Protected Areas Database (PAD-US) 4.1 Fee layer via an ArcGIS Online hosted view [SECONDARY: the USGS endpoint returned HTTP 403] | https://services.arcgis.com/v01gqwM5QqNysAAi/ArcGIS/rest/services/Fee_Managers_PADUS/FeatureServer/0 |
| `nps_at_centerline` | National Park Service, Appalachian National Scenic Trail official centerline (version June 2023) | https://services1.arcgis.com/fBc8EJBxQRMcHlei/ArcGIS/rest/services/ANST_Centerline/FeatureServer/0 |
| `nps_at_facilities` | National Park Service, A.T. official features and facilities, Parking layer | https://services1.arcgis.com/fBc8EJBxQRMcHlei/ArcGIS/rest/services/ANST_Facilities/FeatureServer/2 |
| `usgs_wbd` | USGS Watershed Boundary Dataset (HUC12 020301010201 Muddy Brook; HUC10 0203010102 East Branch Croton River) | https://hydro.nationalmap.gov/arcgis/rest/services/wbd/MapServer |
| `nyc_dep_east_branch` | NYC Department of Environmental Protection, East Branch Reservoir page | https://www.nyc.gov/site/dep/water/east-branch-reservoir.page |
| `osrm` | OSRM routing on OpenStreetMap data (public demo server); driving distances and free-flow times [INFERENCE] | https://router.project-osrm.org/ |
