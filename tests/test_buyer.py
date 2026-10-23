"""Slice 3 acceptance, SC8: Step 8 Buyer side. Four screens; CP-30 (taking the buyer on), CP-24 notices, CP-16
blocks tours until the buyer agreement; CP-17 dual-agency consent of both clients before offer B; the buyer's AI
advises and drafts (CP-31) and negotiates (CP-13, buyer side); the buyer approves (CP-18). And the information
wall: no seller-side model call sees the buyer's limits, no buyer-side call the seller's."""

import json
import re

import pytest

from app.modules.buyer import service as buyer
from app.modules.offers import service as offers
from app.records import service as records
from app.web import current_deal
from tests.conftest import as_persona
from tests.flows import (agreed_b, buyer_client, buyer_signed, inbox_approved, offer_b, toured_and_consented)

PROTECTED = ("child", "famil", "married", "religio", "church", "national", "origin", "race", "disab", "age",
             "pregnan", "gender", "sex", "orientation", "military", "veteran", "income source")


def test_four_buyer_screens_exist(client):
    buyer_signed(client)
    for path in ("/buyer", "/buyer/search", "/buyer/tour", "/buyer/offer"):
        assert client.get(path).status_code == 200, path


def test_intake_asks_no_protected_class_question(client):
    inbox_approved(client)
    r = client.get("/buyer?demo=1")
    form = r.text.split('id="buyer-form"')[1].split("</form>")[0]
    names = set(re.findall(r'name="([a-z_]+)"', form))
    assert names <= set(buyer.INTAKE_FIELDS), names - set(buyer.INTAKE_FIELDS)
    labels = re.sub(r"<[^>]+>", " ", form.split('class="help"')[0]).lower()
    for word in PROTECTED:
        assert not re.search(rf"\b{word}", labels), word


def test_ai_takes_the_buyer_on_with_notices_and_cp16(client, session):
    buyer_client(client)
    deal = current_deal(session)
    assert records.latest(session, deal.id, "CP-30").status == "done"
    sent = [c for c in records.records(session, deal.id, "CP-24") if "buyer" in c.reason]
    assert len(sent) == 3
    assert records.latest(session, deal.id, "CP-16").status == "pending"
    r = client.get("/buyer")
    assert 'id="rec-CP-30"' in r.text and 'id="buyer-agreement"' in r.text and "negotiable" in r.text
    as_persona(client, "seller")
    assert client.post("/buyer/sign", data={"decision": "sign"}).status_code == 403


def test_cp16_blocks_tours(client, session):
    buyer_client(client)
    r = client.post("/buyer/tour", data={"kind": "self-guided"})
    assert r.status_code == 409 and "CP-16" in r.text
    assert "tour" not in buyer.state(current_deal(session))


def test_tour_opens_dual_agency_and_is_self_guided(client, session):
    buyer_signed(client)
    assert client.post("/buyer/tour", data={"kind": "self-guided"}, follow_redirects=False).status_code == 303
    deal = current_deal(session)
    assert records.latest(session, deal.id, "CP-17").status == "pending"
    assert any("Buyer 1" in (c.reason or "") for c in records.records(session, deal.id, "CP-28"))
    r = client.get("/buyer/tour")
    assert 'id="booked"' in r.text and 'id="rec-CP-17"' in r.text and 'id="rec-CP-28"' in r.text


def test_search_has_no_steering_filter_and_the_alert_is_checked(client, session):
    buyer_signed(client)
    deal = current_deal(session)
    with pytest.raises(ValueError):
        buyer.search(deal, {"school_rating": 9})
    r = client.get("/buyer/search")
    assert 'data-listing="FIRM"' in r.text and "fictional" in r.text
    form = r.text.split('id="search-form"')[1].split("</form>")[0]
    assert set(re.findall(r'name="([a-z_]+)"', form)) <= set(buyer.SEARCH_FILTERS)
    assert client.post("/buyer/alert", follow_redirects=False).status_code == 303
    r = client.get("/buyer/search")
    assert 'data-topic="alert"' in r.text and "sent (simulated)" in r.text and "identity-block" in r.text


def test_offer_waits_for_both_consents(client, session):
    buyer_signed(client)
    client.post("/buyer/tour", data={"kind": "self-guided"})
    as_persona(client, "buyer")
    client.post("/buyer/consent", data={"decision": "consent"})
    as_persona(client, "presenter")
    r = client.post("/buyer/offer/advise")
    assert r.status_code == 409 and "CP-17" in r.text
    assert 'id="offer-blocked"' in client.get("/buyer/offer").text


def test_buyer_ai_drafts_with_cp31_and_only_the_buyer_approves(client, session):
    toured_and_consented(client)
    client.post("/buyer/offer/advise")
    deal = current_deal(session)
    assert records.latest(session, deal.id, "CP-31").status == "done"
    for p in ("seller", "presenter"):
        as_persona(client, p)
        assert client.post("/buyer/offer/approve", data={"decision": "approve"}).status_code == 403
    as_persona(client, "buyer")
    client.post("/buyer/offer/approve", data={"decision": "approve", "price": "604,000"})
    session.expire_all()
    b = next(o for o in offers.offers(deal) if o["label"] == "B")
    assert b["price"] == 604000 and b["side"] == "firm_buyer"
    assert records.latest(session, deal.id, "CP-18").status == "done"


def test_buyer_ai_negotiates_the_reply_with_cp18_each_time(client, session):
    agreed_b(client)
    deal = current_deal(session)
    session.expire_all()
    cp18 = records.records(session, deal.id, "CP-18")
    assert len(cp18) == 3 and all(c.status == "done" and c.decided_by == "buyer" for c in cp18)
    assert len([c for c in records.records(session, deal.id, "CP-31")]) == 3  # the offer and two replies
    st = buyer.state(deal)
    assert st["agreed"]["final_price"] == 620000
    assert 'id="buyer-agreed"' in client.get("/buyer/offer").text


def test_screens_keep_the_wall(client):
    countered_b_path = agreed_b
    countered_b_path(client)
    as_persona(client, "seller")
    r = client.get("/buyer")
    assert 'id="buyer-private-hidden"' in r.text and "665,000" not in r.text
    assert 'id="wall-note"' in client.get("/buyer/offer").text
    as_persona(client, "buyer")
    r = client.get("/offers")
    assert 'id="wall-note"' in r.text and "618,000" not in r.text and 'id="decide-form"' not in r.text


SELLER_SECRETS = ("618000", "lowest_price", "price_floor", "motivation", "Relocating", "Dana", "Okafor")
BUYER_SECRETS = ("665000", "maximum_price", "Needs a home office", "flexible on closing", "Sam Whitfield",
                 "Whitfield", "sam.wa@example.com")


def test_information_wall(client, provider):
    """Decision 24: run the whole demo path; every model request is checked by the side that made it."""
    agreed_b(client)
    seller_tasks = {"pricing.recommend", "copy.draft", "inbox.reply", "offers.advise"}
    buyer_tasks = {"buyer.alert", "buyer.offer_advise", "buyer.counter_advise"}
    seen = {r["task"] for r in provider.requests}
    assert {"offers.advise", "buyer.offer_advise", "buyer.counter_advise"} <= seen
    for r in provider.requests:
        body = json.dumps(r)
        if r["task"] in seller_tasks:
            for secret in BUYER_SECRETS:
                assert secret not in body, (r["task"], secret)
        if r["task"] in buyer_tasks:
            for secret in SELLER_SECRETS:
                assert secret not in body, (r["task"], secret)
    counter_req = [r for r in provider.requests if r["task"] == "buyer.counter_advise"][-1]
    assert "665000" in counter_req["user"]  # the buyer's own AI does see the buyer's limit
