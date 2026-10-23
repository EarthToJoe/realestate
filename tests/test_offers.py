"""Slice 3 acceptance, SC6: Step 6 Offers. Two offers (A from an outside agent, B from the firm's own buyer)
compared with net sheets; the seller's AI presents and advises (CP-11); only the seller decides (CP-12), price and
terms; the seller's AI negotiates with the buyer's side (CP-13 per act); a counter or agreement outside the
seller's decision is refused by code."""

import json

import pytest

from app.modules.offers import service as offers
from app.records import service as records
from app.web import current_deal
from tests.conftest import as_persona
from tests.flows import agreed_b, countered_b, inbox_approved, offer_b, offers_advised


def test_offers_wait_for_cp27(client):
    from tests.conftest import listed, priced
    listed(client)
    priced(client)
    r = client.get("/offers")
    assert 'id="gate"' in r.text and "CP-27" in r.text


def test_advice_waits_for_offer_b(client, session):
    inbox_approved(client)
    r = client.get("/offers")
    assert r.text.count("data-offer=") == 1 and 'id="waiting-b"' in r.text
    r = client.post("/offers/advise")
    assert 'id="not-ready"' in r.text and "Offer B" in r.text
    assert records.latest(session, current_deal(session).id, "CP-11") is None


def test_two_offers_compared_and_advised_with_cp11(client, session, provider):
    offers_advised(client)
    r = client.get("/offers")
    assert r.text.count("data-offer=") == 2 and 'id="net-A"' in r.text and 'id="net-B"' in r.text
    assert "dual agency: the firm acts for both" in r.text
    assert "Not binding until a formal contract" in r.text and 'id="recommendation"' in r.text
    deal = current_deal(session)
    assert records.latest(session, deal.id, "CP-11").status == "done" and 'id="rec-CP-11"' in r.text
    assert records.latest(session, deal.id, "CP-12").status == "pending"
    req = next(x for x in provider.requests if x["task"] == "offers.advise")
    for leak in ("665000", "maximum_price", "home office", "price_floor", "motivation", "Dana", "Okafor",
                 "Whitfield"):
        assert leak not in json.dumps(req), leak


def test_only_the_seller_decides_cp12(client, session):
    offers_advised(client)
    for p in ("buyer", "presenter"):
        as_persona(client, p)
        r = client.post("/offers/decide", data={"decision": "accept", "offer": "A"}, follow_redirects=False)
        assert r.status_code == 403
    assert records.latest(session, current_deal(session).id, "CP-12").status == "pending"


def test_counter_carries_terms_and_the_negotiation_reaches_agreement(client, session):
    agreed_b(client)
    session.expire_all()
    deal = current_deal(session)
    st = offers.state(deal)
    assert st["accepted"]["final_price"] == 620000 and st["accepted"]["label"] == "B"
    sent = [t["terms"] for t in st["thread"] if t["from"] == "seller's AI"]
    assert [t["price"] for t in sent] == [625000, 620000]
    assert all(t["closing_days"] == 45 and t["inspection_days"] <= 10 and t["requests"] == [] for t in sent)
    seller_side = [c for c in records.records(session, deal.id, "CP-13") if c.attached_to == "offers:seller"]
    buyer_side = [c for c in records.records(session, deal.id, "CP-13") if c.attached_to == "offers:buyer"]
    assert len(seller_side) == 3 and len(buyer_side) == 2  # two counters and the agreement; two buyer replies
    assert deal.current_step >= 7


@pytest.mark.parametrize("terms,why", [
    ({"price": 610000}, "below the lowest price"),
    ({"price": 630000}, "above the seller's own counter"),
    ({"price": 620000, "closing_days": 90}, "outside the seller's range"),
    ({"price": 620000, "inspection_days": 21}, "longer than the seller allows"),
    ({"price": 620000, "seller_credit": 5000}, "seller credit"),
    ({"price": 620000, "requests": ["the riding mower stays"]}, "not agreed by the seller"),
])
def test_counter_outside_the_decision_is_refused_by_code(client, session, terms, why):
    countered_b(client)
    deal = current_deal(session)
    with pytest.raises(offers.CounterRefused, match=why):
        offers.check_counter(deal, {**offers.counter_terms(deal), **terms})


def test_hand_counter_outside_the_decision_is_refused_on_screen(client, session):
    countered_b(client)
    before = len(records.records(session, current_deal(session).id, "CP-13"))
    r = client.post("/offers/counter", data={"price": "600000"})
    assert r.status_code == 409 and "below the lowest price the seller allowed" in r.text
    r = client.post("/offers/counter", data={"price": "620000", "inspection_days": "21"})
    assert r.status_code == 409
    session.expire_all()
    assert len(records.records(session, current_deal(session).id, "CP-13")) == before


def test_no_counter_without_a_counter_decision(client, session):
    offers_advised(client)
    deal = current_deal(session)
    with pytest.raises(offers.CounterRefused):
        offers.check_counter(deal, {"price": 640000})


def test_outside_agent_path_on_offer_a(client, session):
    offers_advised(client)
    as_persona(client, "seller")
    client.post("/offers/decide", data={"decision": "counter", "offer": "A", "counter_price": "640000",
                                        "lowest_price": "635000", "closing_days": "60", "allow_requests": "yes"})
    as_persona(client, "presenter")
    client.post("/offers/negotiate")
    session.expire_all()
    st = offers.state(current_deal(session))
    assert st["accepted"]["final_price"] == 636000 and st["accepted"]["requests"] == ["the riding mower stays"]


def test_offer_b_needs_dual_agency_consent(client, session):
    from tests.flows import buyer_signed
    buyer_signed(client)
    client.post("/buyer/tour", data={"kind": "self-guided"})
    deal = current_deal(session)
    with pytest.raises(records.GateError):
        offers.receive_offer_b(session, deal, {"price": 600000}, party="x")


def test_back_to_the_seller_when_nothing_inside_the_decision_is_left(client, session):
    offer_b(client)
    client.post("/offers/advise")
    as_persona(client, "seller")
    client.post("/offers/decide", data={"decision": "counter", "offer": "B", "counter_price": "625000",
                                        "lowest_price": "625000", "closing_days": "45"})
    as_persona(client, "presenter")
    client.post("/offers/negotiate")
    deal = current_deal(session)
    session.expire_all()
    offers.receive_reply(session, deal, {"action": "counter", "price": 606000}, frm="buyer's AI")
    session.commit()
    st = offers.state(deal)
    assert "back_to_seller" in st and records.latest(session, deal.id, "CP-12").status == "pending"
