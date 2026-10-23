#!/usr/bin/env bash
# Walks steps 1 to 8 on a running app the way the demo does (walk order 1-5, 8, 6, 7), and checks each screen.
#   bash scripts/live-flow.sh                      the live site (house login)
#   bash scripts/live-flow.sh http://127.0.0.1:8000  a local run
# Clicks counted for SC1 ("profile with source chips in under 5 minutes of clicking").
set -uo pipefail
BASE=${1:-https://realestate.hughesnode.com}
AUTH=(); [[ $BASE == https://* ]] && AUTH=(-u ":$(cat /srv/realestate/secrets/HOUSE_PASSWORD)")   # house login, blank username; never in the repo
JAR=$(mktemp); OUT=$(mktemp)
c() { curl -s "${AUTH[@]}" -b "$JAR" -c "$JAR" "$@"; }
fail=0
ok() { if grep -q -- "$2" "$OUT"; then echo "ok   $1"; else echo "FAIL $1 (missing: $2)"; fail=1; fi; }
# ---- After a reset, no step link redirects: each answers 200 with its screen or its gate card (BUILD-FIX)
c "$BASE/demo/start" -o "$OUT"; ok "Start demo asks first" "This resets the deal to the beginning"
c -X POST "$BASE/demo/reset" -o /dev/null
c "$BASE/intake?demo=1&started=1" -o "$OUT"; ok "step 1 says what to press next" 'id="next-hint"'
ROUTES=$(grep -o 'route: /[^ ]*' "$(dirname "$0")/../app/demo/steps.yaml" | sed 's/route: //')
for r in $ROUTES; do
  code=$(c "$BASE$r" -o "$OUT" -w '%{http_code}')
  if [ "$code" != 200 ]; then echo "FAIL step link $r -> HTTP $code (expect 200, never a redirect)"; fail=1
  elif [ "$r" != /intake ] && [ "$r" != /step/10 ] && ! grep -q 'id="gate-card"' "$OUT"; then echo "FAIL $r: no gate card"; fail=1
  else echo "ok   step link $r -> 200$([ "$r" != /intake ] && [ "$r" != /step/10 ] && echo ' with its gate card')"; fi
done
c "$BASE/pricing" -o "$OUT"; ok "gate card offers fast-forward" 'id="gate-ff"'
# ---- Fast-forward the whole demo (replays, $0), then start again and walk it by hand below
c -X POST "$BASE/demo/fast-forward/9" -o /dev/null -w "%{http_code}\n" | sed 's/^/fast-forward to step 9 -> HTTP /'
c "$BASE/contract" -o "$OUT"; ok "fast-forward reaches the signed contract" 'id="signed"'
as_() { curl -s "${AUTH[@]}" -b "persona=$1" "${@:2}"; }
as_ seller -X POST "$BASE/demo/fast-forward/2" -o /dev/null -w "%{http_code}\n" | sed 's/^/seller tries fast-forward -> HTTP (expect 403) /'
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
grep -o 'data-mode="[a-z]*"' "$OUT" | head -1
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
grep -o 'data-mode="[a-z]*"' "$OUT" | head -1
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
# ---- Step 8 Buyer side (walked before step 6: offer B comes from the firm's own buyer)
as presenter "$BASE/offers" -o "$OUT"; ok "offers: only A before the buyer acts" 'id="waiting-b"'
as presenter -X POST "$BASE/buyer" -o /dev/null -w "%{http_code}\n" \
  --data-urlencode "name=Sam Whitfield-Arora" --data-urlencode "email=sam.wa@example.com" \
  --data-urlencode "phone=(914) 555-0187" -d beds_min=3 -d acres_min=1 \
  -d towns=Pawling -d towns=Beekman -d towns=Dover --data-urlencode "towns=Union Vale" --data-urlencode "towns=East Fishkill" \
  --data-urlencode "must_haves=A room for a home office; some land; room for a garden" -d preapproved=yes \
  -d preapproval_amount=680000 --data-urlencode "timeline=Flexible; closing in about two months suits" \
  -d max_price=665000 --data-urlencode "private_notes=Needs a home office; flexible on closing date" | sed 's/^/buyer intake -> HTTP /'
as presenter "$BASE/buyer" -o "$OUT"; ok "buyer: CP-30 marker" 'id="rec-CP-30"'; ok "buyer: CP-16 waiting" 'id="rec-CP-16"'
as presenter -X POST "$BASE/buyer/tour" -d kind=self-guided -o /dev/null -w "%{http_code}\n" | sed 's/^/tour before CP-16 -> HTTP (expect 409) /'
as buyer -X POST "$BASE/buyer/sign" -d decision=sign -o /dev/null -w "%{http_code}\n" | sed 's/^/buyer signs CP-16 -> HTTP /'
as presenter -X POST "$BASE/buyer/alert" -o /dev/null
as presenter "$BASE/buyer/search" -o "$OUT"; ok "search: alert sent (simulated)" 'data-topic="alert"'; ok "search: the firm's listing" 'data-listing="FIRM"'
as presenter -X POST "$BASE/buyer/tour" -d kind=self-guided -o /dev/null
for p in buyer seller; do as $p -X POST "$BASE/buyer/consent" -d decision=consent -o /dev/null -w "%{http_code}\n" | sed "s/^/$p consents CP-17 -> HTTP /"; done
as presenter "$BASE/buyer/tour" -o "$OUT"; ok "tour booked" 'id="booked"'; ok "tour: CP-28 marker" 'id="rec-CP-28"'
as presenter -X POST "$BASE/buyer/offer/advise" -o /dev/null
as buyer "$BASE/buyer/offer" -o "$OUT"; ok "buyer's AI drafted the offer (CP-31)" 'id="draft-offer"'
as presenter -X POST "$BASE/buyer/offer/approve" -d decision=approve -o /dev/null -w "%{http_code}\n" | sed 's/^/presenter approves CP-18 -> HTTP (expect 403) /'
as buyer -X POST "$BASE/buyer/offer/approve" -d decision=approve -o /dev/null -w "%{http_code}\n" | sed 's/^/buyer approves CP-18 -> HTTP /'
# ---- Step 6 Offers
as presenter -X POST "$BASE/offers/advise" -o /dev/null
as seller "$BASE/offers" -o "$OUT"; ok "offers: two compared, AI advice, CP-11" 'id="rec-CP-11"'
v() { grep -o "name=\"$1\"[^>]*value=\"[0-9]*\"" "$OUT" | head -1 | grep -o 'value="[0-9]*"' | grep -o '[0-9]*'; }
OFFER=$(grep -o '<option selected>[AB]</option>' "$OUT" | grep -o '[AB]' | head -1); OFFER=${OFFER:-B}
echo "the AI suggests: counter offer $OFFER at \$$(v counter_price), agreeing down to \$$(v lowest_price), closing $(v closing_days) days"
as seller -X POST "$BASE/offers/decide" -d decision=counter -d offer=$OFFER -d counter_price=$(v counter_price) \
  -d lowest_price=$(v lowest_price) -d closing_days=$(v closing_days) -d closing_min=$(v closing_min) \
  -d closing_max=$(v closing_max) -d inspection_max=$(v inspection_max) -d mortgage_max=$(v mortgage_max) \
  -o /dev/null -w "%{http_code}\n" | sed 's/^/seller counters CP-12 -> HTTP /'
as presenter -X POST "$BASE/offers/negotiate" -o /dev/null
as presenter -X POST "$BASE/offers/counter" -d price=500000 -o "$OUT" -w "%{http_code}\n" | sed 's/^/hand counter below the floor -> HTTP (expect 409) /'
ok "counter refused by code" "below the lowest price the seller allowed"
for _ in 1 2 3 4 5; do
  as presenter "$BASE/offers" -o "$OUT"; grep -q 'id="accepted"' "$OUT" && break
  [ "$OFFER" = B ] || { as presenter -X POST "$BASE/offers/negotiate" -o /dev/null; continue; }
  as presenter -X POST "$BASE/buyer/counter/advise" -o /dev/null
  as buyer -X POST "$BASE/buyer/counter/approve" -d decision=approve -o /dev/null -w "%{http_code}\n" | sed 's/^/buyer approves the reply (CP-18) -> HTTP /'
done
as presenter "$BASE/offers" -o "$OUT"; ok "the AIs negotiated to agreement (CP-13)" 'id="accepted"'
grep -o 'id="accepted">Agreed: [^<]*' "$OUT" | sed 's/id="accepted">//' | head -1
as buyer "$BASE/offers" -o "$OUT"; ok "wall: the buyer does not see the seller's decision" 'id="wall-note"'
as seller "$BASE/buyer" -o "$OUT"; ok "wall: the seller does not see the buyer's limit" 'id="buyer-private-hidden"'
# ---- Step 7 Contract
as presenter -X POST "$BASE/contract/draft" -o /dev/null
as presenter "$BASE/contract" -o "$OUT"
ok "contract: code checks passed" 'data-passed="yes"'; ok "contract: CP-14 marker" 'id="rec-CP-14"'
ok "contract: launch route links the plan" 'docs-plan.html#the-contract-route-what-new-york-allows-today'
ok "contract: side-by-side, 28 rows" 'data-n="28"'; ok "contract: label" "DEMONSTRATION. Drafted by software for the parties"
as presenter -X POST "$BASE/contract/open-signing" -o /dev/null -w "%{http_code}\n" | sed 's/^/signing before the PCDS -> HTTP (expect 409) /'
as seller -X POST "$BASE/disclosures/pcds/prepared" -o /dev/null -w "%{http_code}\n" | sed 's/^/seller submits the PCDS (CP-04) -> HTTP /'
as presenter -X POST "$BASE/contract/attach" -o /dev/null
as presenter -X POST "$BASE/contract/open-signing" -o /dev/null -w "%{http_code}\n" | sed 's/^/open signing -> HTTP /'
for p in seller buyer; do as $p -X POST "$BASE/contract/sign" -d decision=sign -o /dev/null -w "%{http_code}\n" | sed "s/^/$p signs CP-33 -> HTTP /"; done
as presenter "$BASE/contract" -o "$OUT"; ok "contract signed by both (simulated)" 'id="signed"'; ok "CP-15 wet ink / notary" 'id="rec-CP-15"'
PDF=$(mktemp); as presenter "$BASE/contract/draft.pdf" -o "$PDF"
head -c 4 "$PDF" | grep -q '%PDF' && echo "ok   contract is a PDF" || { echo "FAIL contract PDF"; fail=1; }
if command -v pdftotext >/dev/null; then
  n=$(pdftotext "$PDF" - | tr '\f' '\n' | grep -c 'DEMONSTRATION. Drafted by software'); p=$(pdftotext "$PDF" - | grep -c $'\f')
  echo "contract PDF: $p pages; the label printed $n times (top and bottom of each page)"
fi
DOCX=$(mktemp); as presenter "$BASE/contract/draft.docx" -o "$DOCX"
if unzip -p "$DOCX" word/header1.xml 2>/dev/null | grep -q 'DEMONSTRATION. Drafted by software'; then echo "ok   DOCX header carries the label"; else echo "FAIL DOCX label"; fail=1; fi
rm -f "$PDF" "$DOCX"
grep -o 'Live model spend so far \$[0-9.]*' "$OUT" | head -1
c "$BASE/timeline" -o "$OUT"
for k in 'data-code="CP-25"' 'data-code="CP-05"' 'data-code="CP-26"' 'data-code="CP-06"' 'data-code="CP-07"' 'data-code="CP-08"' 'data-code="CP-27"' 'data-code="CP-11"' 'data-code="CP-13"' 'data-code="CP-14"' 'data-code="CP-17"' 'data-code="CP-31"' 'data-code="CP-33"'; do ok "timeline $k" "$k"; done
for k in chip-automated chip-client_decision chip-law_marker chip-third_party 'data-code="CP-35"' 'id="hurdle-map"'; do ok "timeline $k" "$k"; done
grep -o 'The sale so far: [^<]*' "$OUT" | head -1
grep -o '[0-9]*</span> places NY law today[^<]*' "$OUT" | sed 's#</span>##' | head -1
c "$BASE/docs-success-criteria.html" -o "$OUT"; ok "review page still served" "Success criteria"
rm -f "$JAR" "$OUT"
[ $fail = 0 ] && echo "LIVE FLOW: OK" || { echo "LIVE FLOW: FAILED"; exit 1; }
