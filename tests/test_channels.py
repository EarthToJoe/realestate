"""Slice 2 acceptance, SC4: every channel card honest; CP-07 the seller signs; CP-08 "human required" links to WS3;
portals fed from the MLS; the firm's site held by the Clear Cooperation clock."""

import re

from app.records import service as records
from app.web import current_deal
from tests.conftest import as_persona, demo_intake, drafted

WS3 = "https://realestate.hughesnode.com/docs-research-ws3-listing-data-access.html"


def _ready(client):
    drafted(client)
    client.post("/copy/ready-all")


def test_board_refuses_before_the_listing_agreement(client):
    demo_intake(client)
    r = client.get("/channels")
    assert 'id="gate"' in r.text and "CP-03" in r.text


def test_every_card_is_honest_and_linked(client):
    _ready(client)
    r = client.get("/channels")
    assert r.status_code == 200
    cards = re.findall(r'<div class="card-ch kind-([a-z_]+)" id="card-([a-zA-Z0-9_-]+)"', r.text)
    kinds = {k for k, _ in cards}
    assert {"human_required", "fed", "automated", "vendor", "owner"} <= kinds
    assert len([1 for k, _ in cards if k == "fed"]) == 5  # Zillow, Realtor.com, Redfin, Homes.com, OneKeyMLS.com
    assert r.text.count("Read the finding") >= len(cards)
    assert "held by the Clear Cooperation clock" in r.text and "waiting for the MLS entry" in r.text
    block = r.text[r.text.index('id="rec-CP-08"'):]
    assert "no listing-input API" in block and f'href="{WS3}"' in block and "WS3-C1" in block


def test_cp07_seller_only_then_mls_entry_by_presenter(client, session):
    _ready(client)
    client.get("/channels")
    # the MLS entry waits for the seller's authorisations
    assert client.post("/channels/mls-entry").status_code == 409
    for p in ("presenter", "buyer"):
        as_persona(client, p)
        r = client.post("/channels/authorise", data={"decision": "sign", "exposure": "Publish to Internet",
                                                     "granted": ["cooperating_brokers", "lockbox", "photographer"]})
        assert r.status_code == 403
    as_persona(client, "seller")
    r = client.post("/channels/authorise", data={"decision": "sign", "exposure": "Publish to Internet",
                                                 "granted": ["cooperating_brokers", "lockbox", "photographer"]},
                    follow_redirects=False)
    assert r.status_code == 303
    # a simulated human-required completion is the Presenter's, not a client's
    assert client.post("/channels/mls-entry").status_code == 403
    as_persona(client, "presenter")
    assert client.post("/channels/mls-entry", follow_redirects=False).status_code == 303
    session.expire_all()
    deal = current_deal(session)
    cp08 = records.latest(session, deal.id, "CP-08")
    assert cp08.kind == "human_required" and cp08.status == "simulated" and not cp08.blocking
    r = client.get("/channels")
    assert "fed from the MLS (simulated)" in r.text and "published (simulated)" in r.text
    assert "vendor booking (simulated)" in r.text
    t = client.get("/timeline").text
    for code in ("CP-05", "CP-25", "CP-06", "CP-26", "CP-07", "CP-08"):
        assert f'data-code="{code}"' in t, code


def test_mls_only_exposure_keeps_portals_dark(client):
    _ready(client)
    client.get("/channels")
    as_persona(client, "seller")
    client.post("/channels/authorise", data={"decision": "sign", "exposure": "MLS Only", "granted": ["lockbox"]})
    as_persona(client, "presenter")
    client.post("/channels/mls-entry")
    r = client.get("/channels")
    assert r.text.count("portals do not receive the listing") == 5
    assert "waiting for the seller&#39;s authorisation (CP-07)" in r.text  # photographer not authorised


def test_step_links_go_to_the_built_screens(client):
    for n, route in ((2, "/pricing"), (3, "/copy"), (4, "/channels")):
        r = client.get(f"/step/{n}", follow_redirects=False)
        assert r.status_code == 303 and r.headers["location"] == route
