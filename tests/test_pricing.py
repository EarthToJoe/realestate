"""Slice 2 acceptance, SC2: Step 2 Pricing (>=3 comps, adjustments in code, method, range, the AI's recommended
price with reasoning, net sheet, CP-25 marker, CP-05 seller chooses and blocks copy until chosen)."""

import json
import re

from app.connectors.public_records import FixtureRecords
from app.modules.pricing import service as pricing
from app.records import service as records
from app.web import current_deal
from tests.conftest import as_persona, demo_intake, listed, priced, recommended_price


def test_pricing_refuses_before_the_listing_agreement(client):
    demo_intake(client)
    r = client.get("/pricing")
    assert 'id="gate"' in r.text and "CP-03" in r.text
    assert client.post("/pricing/recommend").status_code == 409


def test_comps_table_adjustments_and_range(client):
    listed(client)
    r = client.get("/pricing")
    assert r.status_code == 200
    assert "Comparative market analysis, not an appraisal" in r.text
    ranks = re.findall(r'<tr data-rank="(\d+)"', r.text)
    assert len(ranks) >= 3
    assert 'id="adjustments"' in r.text and "Suggested range" in r.text
    assert "Dutchess County public sales records" in r.text


def test_adjustment_arithmetic_is_code():
    subj = dict(address="x", style="Raised ranch", year_built=1995, living_area_sqft=2520, finished_basement_sqft=840,
                bedrooms=3, bathrooms_full=3, bathrooms_half=0, acres=4.18, central_air=False, garage=False)
    comp8 = next(c for c in FixtureRecords().data["comparables"] if c["rank"] == 8)
    a = pricing.adjust(comp8, subj)
    by = {x["factor"]: x["amount"] for x in a["adjustments"]}
    assert by["Living area"] == round(547 * 75, -2)  # 2,520 - 1,973 sq ft at $75
    assert by["Full baths"] == 10000 and by["Central air"] == -8000 and "Style" not in by  # same style
    assert a["adjusted_price"] == 525000 + a["net_adjustment"]
    comps = [pricing.adjust(c, subj) for c in FixtureRecords().data["comparables"]]
    sm = pricing.summarise(comps)
    assert sm["range_low"] <= sm["indicated_value"] <= sm["range_high"]
    assert sm["range_low"] % 5000 == 0 and sm["count"] == 8


def test_range_reconciles_with_demo_house_cross_checks():
    """docs/specs/demo-house.md section 4: A $649,782, B $617,652, C $610,864; suggested $610,000 to $650,000."""
    subj = dict(address="x", style="Raised ranch", year_built=1995, living_area_sqft=2520, finished_basement_sqft=840,
                bedrooms=3, bathrooms_full=3, bathrooms_half=0, acres=4.18, central_air=False, garage=False)
    comps = [pricing.adjust(c, subj) for c in FixtureRecords().data["comparables"]]
    sm = pricing.summarise(comps)
    assert [x["value"] for x in sm["cross_checks"]] == [649782, 617652, 610864]
    assert (sm["range_low"], sm["range_high"]) == (610000, 650000)
    assert sm["indicated_value"] == 625000 and sm["adjusted_indicated"] == 635000
    # basement is inside the style rate: no basement line on a sale of another style
    assert all(a["factor"] != "Finished basement" for c in comps if not c["same_style"] for a in c["adjustments"])


def test_ai_recommends_with_reasoning_and_cp25_marker(client, session):
    listed(client)
    r = client.post("/pricing/recommend", headers={"HX-Request": "true"})
    assert r.status_code == 200
    assert 'id="recommended"' in r.text and "The method in plain words" in r.text and "Why this price" in r.text
    assert 'id="net-sheet"' in r.text and "transfer tax" in r.text
    block = r.text[r.text.index('id="rec-CP-25"'):]
    block = block[:block.index("does not stop the flow")]
    assert "NY law today" in block and "A licensed real estate broker" in block
    for i in ("F22", "L6", "L18", "WS3-D5"):
        assert f">{i}<" in block
    assert 'href="https://realestate.hughesnode.com/docs-research-ws2-legal-licensing.html"' in block
    deal = current_deal(session)
    cp25 = records.latest(session, deal.id, "CP-25")
    assert cp25.kind == "law_marker" and not cp25.blocking
    assert records.latest(session, deal.id, "CP-05").status == "pending"


def test_cp05_seller_chooses_and_copy_waits(client, session):
    listed(client)
    client.post("/pricing/recommend")
    # copy refuses before the seller chooses
    r = client.get("/copy")
    assert 'id="gate"' in r.text and "CP-05" in r.text
    assert client.post("/copy/draft").status_code == 409
    # only the seller decides
    for p in ("presenter", "buyer"):
        as_persona(client, p)
        assert client.post("/pricing/choose", data={"price": "650000"}).status_code == 403
    as_persona(client, "seller")
    assert client.post("/pricing/choose", data={"price": "1"}).status_code == 422
    assert client.post("/pricing/choose", data={"price": "$655,000"}, follow_redirects=False).status_code == 303
    session.expire_all()
    deal = current_deal(session)
    assert deal.list_price == 655000 and records.is_done(session, deal.id, "CP-05")
    assert "655,000" in records.latest(session, deal.id, "CP-05").reason
    assert 'id="gate"' not in client.get("/copy").text
    # the net sheet now shows both prices
    assert "your choice" in client.get("/pricing/advice").text


def test_pricing_model_context_has_no_pii_or_confidential(client, provider):
    priced(client)
    req = next(r for r in provider.requests if r["task"] == "pricing.recommend")
    body = json.dumps(req)
    for leak in ("Dana", "Okafor", "dana.or@example.com", "555-0142", "price_floor", "motivation", "Relocating"):
        assert leak not in body, leak
    ctx = json.loads(req["user"])
    assert len(ctx["comparables"]) >= 3 and "computed" in ctx


def test_recommended_price_from_fake_is_inside_range(client):
    listed(client)
    client.post("/pricing/recommend")
    rec = recommended_price()
    r = client.get("/pricing/advice")
    assert f"${rec:,}" in r.text and "outside the computed range" not in r.text
