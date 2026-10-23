#!/usr/bin/env bash
# T5: Census geocoder + FEMA NFHL point query for 146 Route 292, Holmes, NY 12531.
set -uo pipefail
echo "== Census geocoder"
curl -s -m 30 -G "https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress" \
  --data-urlencode "address=146 Route 292, Holmes, NY 12531" --data-urlencode "benchmark=Public_AR_Current" \
  --data-urlencode "vintage=Current_Current" --data-urlencode "layers=Counties" --data-urlencode "format=json" \
  -o /tmp/t5-census.json -w "HTTP %{http_code}\n"
python3 - <<'PY'
import json
try:
    d = json.load(open("/tmp/t5-census.json"))
    m = d["result"]["addressMatches"]
    print("matches:", len(m))
    for x in m[:2]:
        print(x["matchedAddress"], x["coordinates"], x["geographies"]["Counties"][0]["NAME"])
except Exception as e:
    print("could not parse:", type(e).__name__, open("/tmp/t5-census.json").read()[:300])
PY
echo "== FEMA NFHL flood hazard zones (layer 28) at the parcel centroid 41.523196,-73.645089"
curl -s -m 40 -G "https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query" \
  --data-urlencode "geometry=-73.645089,41.523196" --data-urlencode "geometryType=esriGeometryPoint" \
  --data-urlencode "inSR=4326" --data-urlencode "spatialRel=esriSpatialRelIntersects" \
  --data-urlencode "outFields=FLD_ZONE,ZONE_SUBTY,SFHA_TF,DFIRM_ID" --data-urlencode "returnGeometry=false" \
  --data-urlencode "f=json" -o /tmp/t5-fema.json -w "HTTP %{http_code}\n"
head -c 600 /tmp/t5-fema.json; echo
