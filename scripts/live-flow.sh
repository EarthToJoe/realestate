#!/usr/bin/env bash
# Walks the whole sale on a running app along the one path (decisions 47 to 51), the way the action bar's buttons
# post, checks each screen, then the firm's campaign and the people screens, and leaves the sale reset to the start.
#   bash scripts/live-flow.sh                        the live site (house login)
#   bash scripts/live-flow.sh http://127.0.0.1:8765  a local run
set -uo pipefail
BASE=${1:-https://realestate.hughesnode.com}
AUTH=(); [[ $BASE == https://* ]] && AUTH=(-u ":$(cat /srv/realestate/secrets/HOUSE_PASSWORD)")   # house login, blank username; never in the repo
JAR=$(mktemp); OUT=$(mktemp)
c() { curl -s -m 600 "${AUTH[@]}" -b "$JAR" -c "$JAR" "$@"; }
fail=0
ok() { if grep -q -- "$2" "$OUT"; then echo "ok   $1"; else echo "FAIL $1 (missing: $2)"; fail=1; fi; }
no() { if grep -q -- "$2" "$OUT"; then echo "FAIL $1 (found: $2)"; fail=1; else echo "ok   $1"; fi; }
code() { local want=$1; shift; local got; got=$(c -o "$OUT" -w '%{http_code}' "$@"); if [ "$got" = "$want" ]; then echo "ok   $* -> $got"; else echo "FAIL $* -> $got (want $want)"; fail=1; fi; }
post() { c -o "$OUT" -w '%{http_code}' -X POST "$@"; }
p() { local route=$1; shift; local got; got=$(post "$BASE$route" "$@"); [ "$got" = 303 ] && echo "ok   POST $route -> 303" || { echo "FAIL POST $route -> $got"; fail=1; }; }

# ---- start: a first visit goes straight in; every screen answers 200, later ones with the "not yet" card
c -X POST "$BASE/demo/reset" -o /dev/null
code 303 "$BASE/demo/start"
ROUTES=$(grep -o '^  *route: /[^ ]*' "$(dirname "$0")/../app/demo/steps.yaml" | sed 's/.*route: //' | sort -u)
for r in $ROUTES; do
  got=$(c "$BASE$r" -o "$OUT" -w '%{http_code}')
  if [ "$got" != 200 ] && [ "$got" != 303 ]; then echo "FAIL $r -> $got"; fail=1; continue; fi
  case $r in /intake) ;; /intake/*|/pricing|/copy|/channels|/inbox|/buyer|/buyer/offer|/offers|/contract|/timeline|/brand)
    grep -q 'id="gate-card"' "$OUT" && echo "ok   $r: not-yet card" || { echo "FAIL $r: no not-yet card"; fail=1; } ;; esac
done
code 303 "$BASE/pricing/advice"; code 303 "$BASE/copy/ready-all"
c "$BASE/intake" -o "$OUT"; ok "step 1 pre-filled with the demo house" 'value="146 Route 292"'; no "no View as on screen" 'class="viewas-label"'
t0=$(date +%s)
# ---- 1 The seller signs up
p /intake --data-urlencode "street=146 Route 292" --data-urlencode "city=Holmes" --data-urlencode "zip=12531" \
  --data-urlencode "seller_name=Dana Okafor-Reyes" --data-urlencode "seller_email=dana.or@example.com" \
  --data-urlencode "seller_phone=(845) 555-0142" \
  --data-urlencode "parking=Paved driveway for four cars; no garage" \
  --data-urlencode "condition=Kitchen updated 2019; original baths, well kept; new windows 2016" \
  --data-urlencode "roof_year=2012" --data-urlencode "oil_tank=Indoor tank in the basement, replaced 2015" \
  --data-urlencode "annual_tax_bill=11800" --data-urlencode "hoa=no" \
  --data-urlencode "other=Pond at the back edge of the lot; septic pumped 2024" \
  --data-urlencode "no_electric_service=no" --data-urlencode "utility_surcharge=no" \
  --data-urlencode "green_jobs_charge=no" --data-urlencode "uncapped_gas_well=no"
c "$BASE/intake/profile" -o "$OUT"; ok "2: confirmation line" 'id="flash"'
for k in 'data-source="public_record"' 'data-source="seller"' 'data-source="inferred"' 'id="checklist"'; do ok "2: $k" "$k"; done
echo "seconds to a full profile (1 press): $(( $(date +%s) - t0 ))"
c "$BASE/intake" -o "$OUT"; ok "1 re-opens filled in" 'value="Dana Okafor-Reyes"'
# ---- 3 The seller hires the firm (decision 49: recorded as the client the button names; never the AI)
for who in presenter buyer ai; do code 403 -X POST "$BASE/path/act/agency" -d as=$who -d choice=acknowledge; done
p /path/act/agency -d as=seller -d choice=acknowledge
p /path/act/listing -d as=seller -d choice=sign
c "$BASE/intake/onboarding" -o "$OUT"; ok "3: the AI accepted the listing (red note)" 'id="rec-CP-02"'; ok "3: Change link" 'data-change="listing"'
# ---- 4 The price
c "$BASE/pricing" -o "$OUT"; ok "4: recommendation" 'id="recommended"'; ok "4: CP-25" 'id="rec-CP-25"'; ok "4: not an appraisal" "not an appraisal"
PRICE=$(grep -o 'id="recommended">\$[0-9,]*' "$OUT" | grep -o '[0-9,]*$' | tr -d ,); echo "recommended: \$$PRICE"
p /pricing/choose -d as=seller -d ui=1 -d price="$PRICE"
# ---- 5 The listing (written by the AI as soon as the price was chosen)
c "$BASE/copy" -o "$OUT"; ok "5: six pieces" 'data-channel="flyer"'; ok "5: CP-06" 'id="rec-CP-06"'; ok "5: MLS section" 'id="mls"'
no "5: no rules version on screen" ">rules FH-RULES"
PDF=$(mktemp); c "$BASE/copy/flyer.pdf" -o "$PDF"; head -c 4 "$PDF" | grep -q '%PDF' && echo "ok   flyer is a PDF" || { echo "FAIL flyer PDF"; fail=1; }; rm -f "$PDF"
c "$BASE/path/change/price" -o "$OUT"; ok "Change the price names the listing copy" "the listing copy"
# ---- 6 On the market
p /channels/authorise -d as=seller -d decision=sign --data-urlencode "exposure=Publish to Internet" \
  -d granted=cooperating_brokers -d granted=lockbox -d granted=photographer
p /path/act/mls
c "$BASE/channels" -o "$OUT"; ok "6: CP-08 a person does this" 'id="rec-CP-08"'; ok "6: CP-07 decided" 'data-decided="CP-07"'
# ---- 7 Enquiries and showings
p /inbox/approve -d as=seller -d decision=approve -d self_guided=yes
c "$BASE/inbox" -o "$OUT"; ok "7: threads" 'id="inbox"'; ok "7: CP-09" 'id="rec-CP-09"'; ok "7: the seller's questions" 'id="cards"'
ANS=$(grep -o 'name="card-[0-9]*" value="[a-z_]*"[^>]*checked' "$OUT" | sed 's/name="\(card-[0-9]*\)" value="\([a-z_]*\)".*/-d \1=\2/' | tr '\n' ' ')
p /inbox/answers -d as=seller $ANS
# ---- 8 The buyer signs up
p /buyer --data-urlencode "name=Sam Whitfield-Arora" --data-urlencode "email=sam.wa@example.com" \
  --data-urlencode "phone=(914) 555-0187" -d beds_min=3 -d acres_min=1 \
  -d towns=Pawling -d towns=Beekman -d towns=Dover --data-urlencode "towns=Union Vale" --data-urlencode "towns=East Fishkill" \
  --data-urlencode "must_haves=A room for a home office; some land; room for a garden" -d preapproved=yes \
  -d preapproval_amount=680000 --data-urlencode "timeline=Flexible; closing in about two months suits" \
  -d max_price=665000 --data-urlencode "private_notes=Needs a home office; flexible on closing date"
p /path/act/buyer_agreement -d as=buyer -d choice=sign
p /path/act/dual_agency -d as=buyer -d choice=consent
p /path/act/dual_agency -d as=seller -d choice=consent
c "$BASE/buyer" -o "$OUT"; for k in 'id="wall"' 'id="rec-CP-30"' 'id="search"' 'id="tour"' 'data-decided="CP-17"'; do ok "8: $k" "$k"; done
# ---- 9 The buyer's offer
c "$BASE/buyer/offer" -o "$OUT"; ok "9: the buyer's AI advised" 'id="advice"'
OFFER=$(grep -o 'name="price"[^>]*value="[0-9]*"' "$OUT" | head -1 | grep -o '[0-9]*"$' | tr -d '"')
p /buyer/offer/approve -d as=buyer -d decision=approve -d price="$OFFER"
# ---- 10 The seller decides; the AIs negotiate; the buyer replies
c "$BASE/offers" -o "$OUT"; ok "10: two offers" 'id="offers-table"'; ok "10: CP-11" 'id="rec-CP-11"'; ok "10: the wall" 'id="wall"'
v() { grep -o "name=\"$1\"[^>]*value=\"[0-9]*\"" "$OUT" | head -1 | grep -o 'value="[0-9]*"' | grep -o '[0-9]*'; }
p /offers/decide -d as=seller -d decision=counter -d offer=B -d counter_price="$(v counter_price)" \
  -d lowest_price="$(v lowest_price)" -d closing_days="$(v closing_days)" -d closing_min="$(v closing_min)" \
  -d closing_max="$(v closing_max)" -d inspection_max="$(v inspection_max)" -d mortgage_max="$(v mortgage_max)"
for _ in 1 2 3 4; do
  c "$BASE/offers" -o "$OUT"; grep -q 'id="accepted"' "$OUT" && break
  R=$(grep -A40 'id="reply-form"' "$OUT" | grep -o 'name="price"[^>]*value="[0-9]*"' | head -1 | grep -o '[0-9]*"$' | tr -d '"')
  p /buyer/counter/approve -d as=buyer -d decision=approve -d price="$R"
done
c "$BASE/offers" -o "$OUT"; ok "10: agreed (CP-13)" 'id="accepted"'; grep -o 'Agreed: offer [AB] at \$[0-9,]*' "$OUT" | head -1
# ---- 11 The contract
c "$BASE/contract" -o "$OUT"; ok "11: CP-14" 'id="rec-CP-14"'; ok "11: the disclosure form" 'id="pcds"'
p /path/act/pcds -d as=seller -d choice=complete
p /path/act/signed -d as=seller -d choice=sign
p /path/act/signed -d as=buyer -d choice=sign
c "$BASE/contract" -o "$OUT"; ok "11: signed by both" 'data-decided="CP-33"'; ok "11: CP-15 notary" 'id="rec-CP-15"'
PDF=$(mktemp); c "$BASE/contract/draft.pdf" -o "$PDF"; head -c 4 "$PDF" | grep -q '%PDF' && echo "ok   contract is a PDF" || { echo "FAIL contract PDF"; fail=1; }
DOCX=$(mktemp); c "$BASE/contract/draft.docx" -o "$DOCX"; unzip -p "$DOCX" word/header1.xml 2>/dev/null | grep -q 'DEMONSTRATION' && echo "ok   DOCX label" || { echo "FAIL DOCX"; fail=1; }
rm -f "$PDF" "$DOCX"
# ---- Finale and one more thing
c "$BASE/timeline" -o "$OUT"; for k in 'id="tl-counts"' 'id="closing"' 'id="hurdle-map"' 'id="agent-acts"' 'chip-law_marker'; do ok "finale: $k" "$k"; done
grep -o 'The whole sale, start to finish' "$OUT" | head -1
p /path/act/campaign
c "$BASE/brand" -o "$OUT"; ok "firm: three pieces" 'data-channel="brand_magnet"'; ok "firm: targeting" 'id="targeting"'; ok "firm: published, CP-19" 'id="rec-CP-19"'
# ---- People and their data
c "$BASE/people" -o "$OUT"; SID=$(grep -o 'href="/people/[0-9]*" id="open-seller"' "$OUT" | grep -o '[0-9]\+' | head -1)
c "$BASE/people/$SID/export" -o "$OUT"; ok "export: the seller's fields" '"legal_name"'
c "$BASE/docs-success-criteria.html" -o "$OUT"; ok "review page still served" "Success criteria"
echo "total seconds: $(( $(date +%s) - t0 ))"
# ---- leave the sale reset to the start
c -X POST "$BASE/demo/reset" -o /dev/null
rm -f "$JAR" "$OUT"
[ $fail = 0 ] && echo "LIVE FLOW: OK" || { echo "LIVE FLOW: FAILED"; exit 1; }
