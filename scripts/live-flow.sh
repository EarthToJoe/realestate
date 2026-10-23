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
c "$BASE/timeline" -o "$OUT"
for k in chip-automated chip-client_decision chip-law_marker chip-third_party 'data-code="CP-35"' 'id="hurdle-map"'; do ok "timeline $k" "$k"; done
grep -o '[0-9]* NY law today markers[^<]*' "$OUT" | head -1
grep -o '[0-9]* client decisions made, [0-9]* waiting' "$OUT" | head -1
c "$BASE/docs-success-criteria.html" -o "$OUT"; ok "review page still served" "Success criteria"
rm -f "$JAR" "$OUT"
[ $fail = 0 ] && echo "LIVE FLOW: OK" || { echo "LIVE FLOW: FAILED"; exit 1; }
