"""Shared demo-path helpers for the slice 3 tests: each takes the deal one step further along the walk
(steps 1 to 5, then the buyer side up to offer B, then offers, then the contract)."""

from app.modules.buyer import service as buyer
from tests.conftest import as_persona, listed, priced


def inbox_approved(client, self_guided=True):
    listed(client)
    priced(client)
    assert client.get("/inbox").status_code == 200
    as_persona(client, "seller")
    data = {"decision": "approve", **({"self_guided": "yes"} if self_guided else {})}
    assert client.post("/inbox/approve", data=data, follow_redirects=False).status_code == 303
    as_persona(client, "presenter")


def buyer_client(client):
    inbox_approved(client)
    d = buyer.demo_input()
    r = client.post("/buyer", data=d, follow_redirects=False)
    assert r.status_code == 303, r.text


def buyer_signed(client):
    buyer_client(client)
    as_persona(client, "buyer")
    assert client.post("/buyer/sign", data={"decision": "sign"}, follow_redirects=False).status_code == 303
    as_persona(client, "presenter")


def toured_and_consented(client):
    buyer_signed(client)
    assert client.post("/buyer/tour", data={"kind": "self-guided"}, follow_redirects=False).status_code == 303
    for p in ("buyer", "seller"):
        as_persona(client, p)
        assert client.post("/buyer/consent", data={"decision": "consent"}, follow_redirects=False).status_code == 303
    as_persona(client, "presenter")


def offer_b(client):
    toured_and_consented(client)
    assert client.post("/buyer/offer/advise", follow_redirects=False).status_code == 303
    as_persona(client, "buyer")
    assert client.post("/buyer/offer/approve", data={"decision": "approve"}, follow_redirects=False).status_code == 303
    as_persona(client, "presenter")


def offers_advised(client):
    offer_b(client)
    assert client.post("/offers/advise", follow_redirects=False).status_code == 303


def countered_b(client, counter=625000, lowest=618000):
    """With the fake provider: list $625,000; offer B $605,000; the seller counters $625,000 and lets the AI agree
    down to $618,000; the buyer's AI replies $615,000 (outside), the seller's AI counters $620,000, the buyer
    accepts."""
    offers_advised(client)
    as_persona(client, "seller")
    r = client.post("/offers/decide", data={"decision": "counter", "offer": "B", "counter_price": str(counter),
                                            "lowest_price": str(lowest), "closing_days": "45", "closing_min": "30",
                                            "closing_max": "60", "inspection_max": "10", "mortgage_max": "45"},
                    follow_redirects=False)
    assert r.status_code == 303
    as_persona(client, "presenter")
    assert client.post("/offers/negotiate", follow_redirects=False).status_code == 303


def buyer_replies(client):
    assert client.post("/buyer/counter/advise", follow_redirects=False).status_code == 303
    as_persona(client, "buyer")
    assert client.post("/buyer/counter/approve", data={"decision": "approve"},
                       follow_redirects=False).status_code == 303
    as_persona(client, "presenter")


def agreed_b(client):
    """The demo path: counter on B, the buyer's AI counters, the seller's AI counters inside the decision, the
    buyer accepts."""
    countered_b(client)
    for _ in range(4):
        st = client.get("/offers").text
        if 'id="accepted"' in st:
            return
        buyer_replies(client)
    assert 'id="accepted"' in client.get("/offers").text
