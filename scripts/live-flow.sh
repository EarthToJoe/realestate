#!/usr/bin/env bash
# Walks Step 1 Intake on a running app the way the demo does, and checks each screen.
#   bash scripts/live-flow.sh                      the live site (house login)
#   bash scripts/live-flow.sh http://127.0.0.1:8000  a local run
# Clicks counted for SC1 ("profile with source chips in under 5 minutes of clicking").
set -uo pipefail
BASE=${1:-https://realestate.hughesnode.com}
AUTH=(); [[ $BASE == https://* ]] && AUTH=(-u ":Fibonacci0!")   # house login, blank username
JAR=$(mktemp); OUT=$(mktemp)
c() { curl -s "${AUTH[@]}" -b "$JAR" -c "$JAR" "$@"; }
fail=0
ok() { if grep -q -- "$2" "$OUT"; then echo "ok   $1"; else echo "FAIL $1 (missing: $2)"; fail=1; fi; }
t0=$(date +%s)
c -X POST "$BASE/demo/reset" -o /dev/null                                   # click 0: Start demo
c "$BASE/intake?demo=1" -o "$OUT"; ok "demo form prefilled (click 1: Use demo house)" 'value="146 Route 292"'
c -X POST "$BASE/intake" -o /dev/null \
  --data-urlencode "street=146 Route 292" --data-urlencode "city=Holmes" --data-urlencode "zip=12531" \
  --data-urlencode "seller_name=Dana Okafor-Reyes" --data-urlencode "seller_email=dana.or@example.com" \
  --data-urlencode "seller_phone=(845) 555-0142" \
  --data-urlencode "parking=Paved driveway for four cars; no garage" \
  --data-urlencode "condition=Kitchen updated 2019; original baths, well kept; new windows 2016" \
  --data-urlencode "roof_year=2012" --data-urlencode "oil_tank=Indoor tank in the basement, replaced 2015" \
  --data-urlencode "annual_tax_bill=11800" --data-urlencode "hoa=no" \
  --data-urlencode "other=Pond at the back edge of the lot; septic pumped 2024" \
  --data-urlencode "no_electric_service=no" --data-urlencode "utility_surcharge=no" \
  --data-urlencode "green_jobs_charge=no" --data-urlencode "uncapped_gas_well=no"   # click 2: Start intake
c -X POST -H "HX-Request: true" "$BASE/intake/infer" -o "$OUT"                 # click 3: Let the AI fill the gaps
ok "profile: public-record chips" 'data-source="public_record"'
ok "profile: seller chips" 'data-source="seller"'
ok "profile: inferred chips" 'data-source="inferred"'
grep -o 'AI: [a-z]*[^<]*' "$OUT" | head -1
echo "seconds to a full profile (3 clicks): $(( $(date +%s) - t0 ))"
c "$BASE/intake/disclosures" -o "$OUT"; ok "checklist: lead paint not needed (built 1995)" "Built 1995: only homes built before 1978"
c "$BASE/intake/onboarding" -o "$OUT"; ok "CP-24 notices recorded" "Sent to the seller"
c -X POST "$BASE/intake/accept" -o /dev/null
c "$BASE/intake/onboarding" -o "$OUT"; ok "CP-02 red marker with link" 'docs-research-ws2-legal-licensing.html'
curl -s "${AUTH[@]}" -b "persona=seller" -X POST "$BASE/intake/sign" -d decision=sign -o "$OUT" -w "%{http_code}\n" | sed 's/^/sign before CP-01 -> HTTP /'
ok "CP-03 refused before CP-01" "CP-01"
curl -s "${AUTH[@]}" -b "persona=presenter" -X POST "$BASE/intake/agency" -d decision=acknowledge -o "$OUT" -w "%{http_code}\n" | sed 's/^/presenter acknowledges -> HTTP /'
curl -s "${AUTH[@]}" -b "persona=seller" -X POST "$BASE/intake/agency" -d decision=acknowledge -o /dev/null -w "%{http_code}\n" | sed 's/^/seller acknowledges -> HTTP /'
curl -s "${AUTH[@]}" -b "persona=seller" -X POST "$BASE/intake/sign" -d decision=sign -o /dev/null -w "%{http_code}\n" | sed 's/^/seller signs -> HTTP /'
as() { local p=$1; shift; curl -s "${AUTH[@]}" -b "persona=$p" "$@"; }
# ---- Step 2 Pricing (slice 2)
c "$BASE/pricing" -o "$OUT"; ok "pricing: comparables table" 'data-rank="8"'; ok "pricing: CMA label" "not an appraisal"
c -X POST -H "HX-Request: true" "$BASE/pricing/recommend" -o "$OUT"
ok "pricing: AI recommended price" 'id="recommended"'; ok "pricing: CP-25 marker" 'id="rec-CP-25"'; ok "pricing: net sheet" 'id="net-sheet"'
grep -o 'AI: [a-z]*[^<]*' "$OUT" | head -1
PRICE=$(grep -o 'id="recommended">\$[0-9,]*' "$OUT" | grep -o '[0-9,]*$' | tr -d ,); echo "recommended: \$$PRICE"
as presenter "$BASE/copy" -o "$OUT"; ok "copy refused before CP-05" 'id="gate"'
as presenter -X POST "$BASE/pricing/choose" -d "price=$PRICE" -o /dev/null -w "%{http_code}\n" | sed 's/^/presenter chooses price -> HTTP /'
as seller -X POST "$BASE/pricing/choose" -d "price=$PRICE" -o /dev/null -w "%{http_code}\n" | sed 's/^/seller chooses price -> HTTP /'
# ---- Step 3 Listing copy
as presenter -X POST "$BASE/copy/draft" -o /dev/null
as presenter "$BASE/copy" -o "$OUT"; ok "copy: six pieces drafted" 'data-channel="flyer"'
PORTAL=$(grep -o 'id="art-[0-9]*" data-channel="portal"' "$OUT" | grep -o '[0-9]\+' | head -1)
as presenter -X POST -H "HX-Request: true" "$BASE/copy/$PORTAL/plant" -o "$OUT"; ok "planted violation caught (FH-FAM-01)" 'data-rule="FH-FAM-01"'
as presenter -X POST "$BASE/copy/$PORTAL/ready" -o /dev/null -w "%{http_code}\n" | sed 's/^/mark blocked copy ready -> HTTP /'
as presenter -X POST -H "HX-Request: true" "$BASE/copy/$PORTAL/fix" -o "$OUT"; ok "fix applied, re-check passes" 'data-passed="yes"'
as presenter -X POST "$BASE/copy/ready-all" -o "$OUT"; ok "CP-06 marker after ready" 'id="rec-CP-06"'
as presenter "$BASE/copy/mls" -o "$OUT"; ok "MLS pre-check and package" 'id="mls-package"'
PDF=$(mktemp); as presenter "$BASE/copy/flyer.pdf" -o "$PDF"
if command -v pdftotext >/dev/null; then n=$(pdftotext "$PDF" - | tr '\f' '\n\f' | grep -c DEMONSTRATION); echo "flyer PDF: DEMONSTRATION appears $n times"; fi
head -c 4 "$PDF" | grep -q '%PDF' && echo "ok   flyer is a PDF" || { echo "FAIL flyer PDF"; fail=1; }; rm -f "$PDF"
# ---- Step 4 Marketing plan
as presenter "$BASE/channels" -o "$OUT"; ok "channels: CP-08 human required, WS3 link" 'docs-research-ws3-listing-data-access.html'
ok "channels: portals wait for the MLS" "waiting for the MLS entry"
as seller -X POST "$BASE/channels/authorise" -d decision=sign --data-urlencode "exposure=Publish to Internet" \
  -d granted=cooperating_brokers -d granted=lockbox -d granted=photographer -o /dev/null -w "%{http_code}\n" | sed 's/^/seller signs CP-07 -> HTTP /'
as presenter -X POST "$BASE/channels/mls-entry" -o /dev/null -w "%{http_code}\n" | sed 's/^/presenter records MLS entry -> HTTP /'
as presenter "$BASE/channels" -o "$OUT"; ok "portals fed from the MLS" "fed from the MLS (simulated)"
# ---- Step 5 Communications
as presenter -X POST "$BASE/inbox/next" -o /dev/null -w "%{http_code}\n" | sed 's/^/reply before CP-27 -> HTTP (expect 409) /'
as presenter "$BASE/inbox" -o "$OUT"; ok "inbox: CP-27 waiting for the seller" 'id="rec-CP-27"'
as seller -X POST "$BASE/inbox/approve" -d decision=approve -d self_guided=yes -o /dev/null -w "%{http_code}\n" | sed 's/^/seller approves CP-27 -> HTTP /'
as presenter -X POST "$BASE/inbox/all" -o /dev/null
as presenter "$BASE/inbox" -o "$OUT"; ok "AI replies sent (simulated)" "sent (simulated)"
for k in 'id="rec-CP-09"' 'id="rec-CP-10"' 'id="rec-CP-28"' 'id="feedback-log"' 'class="identity-block"' 'seller-card'; do ok "inbox $k" "$k"; done
# ---- Step 6 Offers
as presenter -X POST "$BASE/offers/advise" -o /dev/null
as presenter "$BASE/offers" -o "$OUT"; ok "offers: two compared, AI advice, CP-11" 'id="rec-CP-11"'
as seller -X POST "$BASE/offers/decide" -d decision=counter -d offer=A -d counter_price=640000 -d lowest_price=635000 -o /dev/null -w "%{http_code}\n" | sed 's/^/seller counters CP-12 -> HTTP /'
as presenter -X POST "$BASE/offers/counter" -d price=625000 -o /dev/null -w "%{http_code}\n" | sed 's/^/counter below the floor -> HTTP (expect 409) /'
for _ in 1 2 3; do as presenter -X POST "$BASE/offers/negotiate" -o /dev/null; done
as presenter "$BASE/offers" -o "$OUT"; ok "AI negotiated to agreement (CP-13)" 'id="accepted"'
grep -o 'Live model spend so far \$[0-9.]*' "$OUT" | head -1
c "$BASE/timeline" -o "$OUT"
for k in 'data-code="CP-25"' 'data-code="CP-05"' 'data-code="CP-26"' 'data-code="CP-06"' 'data-code="CP-07"' 'data-code="CP-08"'; do ok "timeline $k" "$k"; done
for k in chip-automated chip-client_decision chip-law_marker chip-third_party 'data-code="CP-35"' 'id="hurdle-map"'; do ok "timeline $k" "$k"; done
grep -o '[0-9]* NY law today markers[^<]*' "$OUT" | head -1
grep -o '[0-9]* client decisions made, [0-9]* waiting' "$OUT" | head -1
c "$BASE/docs-success-criteria.html" -o "$OUT"; ok "review page still served" "Success criteria"
rm -f "$JAR" "$OUT"
[ $fail = 0 ] && echo "LIVE FLOW: OK" || { echo "LIVE FLOW: FAILED"; exit 1; }
