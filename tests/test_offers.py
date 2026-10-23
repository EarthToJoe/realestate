"""Slice 3 acceptance, SC6: Step 6 Offers. Two offers compared with net sheets; the AI presents and advises
(CP-11); the seller decides (CP-12, only the seller); the AI negotiates the counter (CP-13 per counter); a counter
outside the seller's decision is refused by code."""

import json

import pytest

from app.modules.offers import service as offers
from app.records import service as records
from app.web import current_deal
from tests.conftest import as_persona
from tests.test_inbox import approved


def advised(client):
    approved(client)
    assert client.post("/offers/advise", follow_redirects=False).status_code == 303


def countered(client):
    advised(client)
    as_persona(client, "seller")
    r = client.post("/offers/decide", data={"decision": "counter", "offer": "A", "counter_price": "640,000",
                                            "lowest_price": "635000"}, follow_redirects=False)
    assert r.status_code == 303
    as_persona(client, "presenter")


def test_offers_wait_for_cp27(client):
    from tests.test_inbox import ready
    ready(client)
    r = client.get("/offers")
    assert 'id="gate"' in r.text and "CP-27" in r.text


def test_two_offers_compared_and_advised_with_cp11(client, session, provider):
    advised(client)
    r = client.get("/offers")
    assert r.text.count("data-offer=") == 2 and 'id="net-A"' in r.text and 'id="net-B"' in r.text
    assert "Not binding until a formal contract" in r.text and 'id="recommendation"' in r.text
    deal = current_deal(session)
    assert records.latest(session, deal.id, "CP-11").status == "done" and 'id="rec-CP-11"' in r.text
    assert records.latest(session, deal.id, "CP-12").status == "pending"
    req = next(x for x in provider.requests if x["task"] == "offers.advise")
    for leak in ("price_floor", "motivation", "Dana", "Okafor"):
        assert leak not in json.dumps(req)


def test_only_the_seller_decides_cp12(client, session):
    advised(client)
    as_persona(client, "buyer")
    r = client.post("/offers/decide", data={"decision": "accept", "offer": "A"}, follow_redirects=False)
    assert r.status_code == 403
    assert records.latest(session, current_deal(session).id, "CP-12").status == "pending"


def test_ai_negotiates_within_the_decision_to_agreement(client, session):
    countered(client)
    for _ in range(3):
        client.post("/offers/negotiate")
    session.expire_all()
    deal = current_deal(session)
    st = offers.state(deal)
    assert st["accepted"]["final_price"] == 636000
    sent = [t["price"] for t in st["thread"] if t["from"] == "seller's AI"]
    assert sent == [640000, 636000] and all(635000 <= p <= 640000 for p in sent)
    assert len(records.records(session, deal.id, "CP-13")) == 2
    assert 'id="accepted"' in client.get("/offers").text


def test_counter_outside_the_decision_is_refused_by_code(client, session):
    countered(client)
    r = client.post("/offers/counter", data={"price": "625000"})
    assert r.status_code == 409 and "below the lowest price the seller allowed" in r.text
    r = client.post("/offers/counter", data={"price": "645000"})
    assert r.status_code == 409 and "own counter" in r.text
    r = client.post("/offers/counter", data={"price": "638000", "terms_changed": "yes"})
    assert r.status_code == 409
    session.expire_all()
    assert records.records(session, current_deal(session).id, "CP-13") == []
    deal = current_deal(session)
    with pytest.raises(offers.CounterRefused):
        offers.check_counter(deal, 600000)


def test_no_counter_without_a_counter_decision(client, session):
    advised(client)
    deal = current_deal(session)
    with pytest.raises(offers.CounterRefused):
        offers.check_counter(deal, 640000)
