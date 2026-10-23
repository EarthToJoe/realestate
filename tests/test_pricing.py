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
    assert 'id="gate-card"' in r.text and 'data-missing="agency"' in r.text
    assert client.post("/pricing/recommend").status_code == 409


def test_comps_table_adjustments_and_range(client):
    """Step 4 (decision 51): the comparables and the advice on one screen; the sales are folded, in plain words."""
    listed(client)
    r = client.get("/pricing")
    assert r.status_code == 200
    assert "Comparative market analysis, not an appraisal" in r.text
    ranks = re.findall(r'<tr data-rank="(\d+)"', r.text)
    assert len(ranks) >= 3
    assert 'id="adjustments"' in r.text and "Suggested range" in r.text
    assert "Dutchess County public sales records" in r.text
    # the adjusted sales' spread is explained beside the narrower range, never left to contradict it
    assert "Why the range is narrower than the adjusted sales" in r.text
    # the old address still lands here
    assert client.get("/pricing/advice").url.path == "/pricing"


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
    r = client.post("/pricing/recommend", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/pricing"  # Post/Redirect/Get
    r = client.get("/pricing")
    assert 'id="recommended"' in r.text and "How the AI worked it out" in r.text and "Why this price" in r.text
    assert 'id="net-sheet"' in r.text and "transfer tax" in r.text
    # the screen leads on the recommendation; the jargon stays in the folds
    head = r.text[r.text.index('id="ai-panel"'):r.text.index("Show the working")]
    for word in ("Reconciled", "arm's-length", "gross"):
        assert word not in head, word
    block = r.text[r.text.index('id="rec-CP-25"'):]
    block = block[:block.index("Read the finding")]
    assert "NY law today" in block and "A licensed real estate broker" in block
    for i in ("F22", "L6", "L18", "WS3-D5"):
        assert f">{i}<" in block
    deal = current_deal(session)
    cp25 = records.latest(session, deal.id, "CP-25")
    assert cp25.kind == "law_marker" and not cp25.blocking
    assert records.latest(session, deal.id, "CP-05").status == "pending"
    # the seller's decision card holds the price form the action bar's button submits
    assert 'id="price-form"' in r.text and 'form="price-form"' in r.text and "Seller: list at" in r.text


def test_cp05_seller_chooses_and_copy_waits(client, session):
    listed(client)
    client.post("/pricing/recommend")
    # copy refuses before the seller chooses
    r = client.get("/copy")
    assert 'id="gate-card"' in r.text and 'data-missing="price"' in r.text
    assert client.post("/copy/draft").status_code == 409
    # the AI and the other client can never record the seller's decision (decision 49)
    for p in ("presenter", "buyer"):
        as_persona(client, p)
        assert client.post("/pricing/choose", data={"price": "650000"}).status_code == 403
    assert client.post("/pricing/choose", data={"price": "650000", "as": "ai"}).status_code == 403
    assert client.post("/pricing/choose", data={"price": "650000", "as": "buyer"}).status_code == 403
    as_persona(client, "presenter")
    r = client.post("/pricing/choose", data={"price": "1", "as": "seller"})
    assert r.status_code == 422
    r = client.post("/pricing/choose", data={"price": "lots", "as": "seller"})
    assert r.status_code == 422 and 'id="err-price"' in r.text and "whole number of dollars" in r.text
    # the button names the seller: recorded as the seller's, whoever is viewing
    assert client.post("/pricing/choose", data={"price": "$655,000", "as": "seller"},
                       follow_redirects=False).status_code == 303
    session.expire_all()
    deal = current_deal(session)
    cp05 = records.latest(session, deal.id, "CP-05")
    assert deal.list_price == 655000 and cp05.status == "done" and cp05.decided_by == "seller"
    assert "655,000" in cp05.reason
    assert 'id="gate-card"' not in client.get("/copy").text
    # the net sheet now shows both prices; the card shows the price and Change
    page = client.get("/pricing").text
    assert "the seller's choice" in page and 'id="chosen-price"' in page and 'href="/path/change/price"' in page


def test_recorded_demo_refuses_an_off_script_price(client, app, session):
    """In a recorded demo the price is the recorded one: another figure is refused in plain words before anything
    is saved, with a way to put it back (fresh-eyes audit 4)."""
    listed(client)
    client.post("/pricing/recommend")
    rec = recommended_price()
    app.state.provider.mode = "replay"
    try:
        r = client.post("/pricing/choose", data={"price": str(rec + 15000), "as": "seller"})
        assert r.status_code == 409 and "Not in the recorded demo" in r.text and 'id="put-back"' in r.text
        session.expire_all()
        assert records.latest(session, current_deal(session).id, "CP-05").status == "pending"
        assert client.post("/pricing/choose", data={"price": f"{rec:,}", "as": "seller"},
                           follow_redirects=False).status_code == 303
    finally:
        app.state.provider.mode = "fake"


def test_choosing_from_the_action_bar_lets_the_ai_write_the_listing(client, session):
    """From the action bar (`ui`), the AI does its own work after the seller's decision (decision 47)."""
    listed(client)
    client.post("/pricing/recommend")
    r = client.post("/pricing/choose", data={"price": str(recommended_price()), "as": "seller", "ui": "1"})
    assert r.status_code == 200 and r.url.path == "/pricing"
    assert "The seller chose to list at" in r.text and "the AI wrote the listing" in r.text
    session.expire_all()
    from app.modules.listing_copy import service as copy_service

    arts = copy_service.artifacts(session, current_deal(session))
    assert len(arts) == 6 and all(a.status == "ready" for a in arts)


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
    r = client.get("/pricing")
    assert f"${rec:,}" in r.text and "outside that range" not in r.text
