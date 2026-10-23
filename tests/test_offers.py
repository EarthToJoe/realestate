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


def test_offers_wait_for_the_buyers_offer(client):
    from tests.conftest import listed, priced
    listed(client)
    priced(client)
    r = client.get("/offers")
    assert r.status_code == 200 and 'id="gate-card"' in r.text and "data-offer=" not in r.text


def test_advice_waits_for_offer_b(client, session):
    inbox_approved(client)
    r = client.post("/offers/advise")  # Post/Redirect/Get: the screen opens with the reason, in plain words
    assert r.status_code == 200 and 'id="flash"' in r.text and "Offer B" in r.text
    assert records.latest(session, current_deal(session).id, "CP-11") is None


def test_two_offers_compared_and_advised_with_cp11(client, session, provider):
    offers_advised(client)
    r = client.get("/offers")
    assert r.text.count("data-offer=") == 2 and 'id="net-A"' in r.text and 'id="net-B"' in r.text
    assert "The firm acts for both sides here" in r.text and 'id="wall"' in r.text
    assert "Not binding until a formal contract" in r.text and 'id="recommendation"' in r.text
    assert "Offer A, from another firm&#39;s buyer" in r.text and "Offer B, from the firm&#39;s own buyer" in r.text
    assert "Prospect B" not in r.text and "Buyer 1" not in r.text
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
    assert client.post("/offers/counter", data={"price": "600000"}).status_code == 403  # a presenter's tool only
    client.cookies.set("presenting", "on")
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


def test_a_decision_is_recorded_as_the_client_the_button_names(client, session):
    """Decision 49: the amber button records the seller's decision whoever is viewing; nobody else can be named."""
    offers_advised(client)
    for who in ("ai", "presenter", "buyer"):
        r = client.post("/offers/decide", data={"as": who, "decision": "reject", "offer": "A"}, follow_redirects=False)
        assert r.status_code == 403, who
    r = client.post("/offers/decide", data={"as": "seller", "decision": "reject", "offer": "A"},
                    follow_redirects=False)
    assert r.status_code == 303
    session.expire_all()
    cp = records.latest(session, current_deal(session).id, "CP-12")
    assert cp.status == "declined" and cp.decided_by == "seller"


def test_a_figure_the_recordings_do_not_cover_is_refused_in_plain_words(client, session):
    """Fresh-eyes audit 4: in a recorded demo an off-script counter never reaches a model and never sticks the deal."""
    offers_advised(client)
    client.app.state.provider.mode = "replay"
    try:
        from app.demo import walk
        rd = walk.recorded_decision(current_deal(session))
        form = {"as": "seller", "decision": "counter", "offer": rd["offer_label"], "counter_price": "640000",
                "lowest_price": str(rd["lowest_price"]), "closing_days": str(rd["closing_days"]),
                "closing_min": "30", "closing_max": "60", "inspection_max": "10", "mortgage_max": "45"}
        r = client.post("/offers/decide", data=form)
        assert r.status_code == 409 and "Not in the recorded demo" in r.text and 'id="put-back"' in r.text
        assert "No recorded answer" not in r.text
        session.expire_all()
        assert records.latest(session, current_deal(session).id, "CP-12").status == "pending"
        r = client.post("/offers/decide", data={**form, "counter_price": str(rd["counter_price"])},
                        follow_redirects=False)
        assert r.status_code == 303
    finally:
        client.app.state.provider.mode = "fake"


def test_the_agreed_screen_says_why_from_the_recorded_advice(client, session):
    agreed_b(client)
    r = client.get("/offers")
    st = offers.state(current_deal(session))
    assert 'id="why-accepted"' in r.text and 'id="accepted"' in r.text
    advice = next(v["advice"] for v in st["advice"]["offers"] if v["label"] == st["accepted"]["label"])
    assert advice.split(".")[0].split("'")[0] in r.text  # the AI's own words, not a reason made up for the screen
    assert 'href="/path/change/agreed"' in r.text and 'href="/path/change/seller_decision"' in r.text


def test_refresh_after_an_action_lands_on_the_screen(client):
    offers_advised(client)
    r = client.get("/offers/decide", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/offers"
