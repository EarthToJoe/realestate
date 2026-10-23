"""SC4, on path step 6 (decisions 47 to 51): every channel says honestly who does it; CP-07 is the seller's,
recorded as the client the button names; CP-08 "a person does this" links to WS3 and works from any view; portals
are fed from the MLS; the firm's site is held by the Clear Cooperation clock; every POST redirects (PRG)."""

import re

from app.records import service as records
from app.web import current_deal
from tests.conftest import as_persona, demo_intake, drafted

WS3 = "https://realestate.hughesnode.com/docs-research-ws3-listing-data-access.html"
PLAN = {"decision": "sign", "exposure": "Publish to Internet",
        "granted": ["cooperating_brokers", "lockbox", "photographer"]}


def _ready(client):
    drafted(client)
    client.post("/copy/ready-all")


def test_board_waits_for_the_listing_agreement(client):
    demo_intake(client)
    r = client.get("/channels")
    assert r.status_code == 200 and 'id="gate-card"' in r.text


def test_every_channel_is_honest_and_compact(client):
    _ready(client)
    r = client.get("/channels")
    assert r.status_code == 200
    rows = re.findall(r'<li class="ch-row kind-([a-z_]+)" id="card-([a-z_]+)"', r.text)
    assert [i for _, i in rows] == ["mls", "portals", "web", "social", "gbp", "vendors", "open_house"]
    assert {k for k, _ in rows} == {"human_required", "fed", "automated", "vendor", "owner"}
    assert "held by the Clear Cooperation clock" in r.text and "waiting for the MLS entry" in r.text
    # no doubled labels, no "(stub)" outside a fold
    for bad in ("Fed from the MLS: fed from the MLS", "Vendor booking: vendor booking", "owner hosts (step 5)",
                "(stub)"):
        assert bad not in r.text, bad
    block = r.text[r.text.index('id="rec-CP-08"'):]
    assert "no listing-input API" in block and f'href="{WS3}"' in block and "WS3-C1" in block
    assert 'id="authorise-form"' in r.text and 'name="as" value="seller"' in r.text


def test_cp07_recorded_as_the_client_named_then_mls_entry_from_any_view(client, session):
    _ready(client)
    client.get("/channels")
    # the MLS entry waits for the seller's authorisations
    assert client.post("/channels/mls-entry").status_code == 409
    # a buyer or the firm cannot sign for the seller, whatever the view
    for named in ("buyer", "presenter", "ai"):
        r = client.post("/channels/authorise", data={**PLAN, "as": named})
        assert r.status_code == 403, named
    # the button names the seller: recorded as the seller's, from any view (here the firm's)
    r = client.post("/channels/authorise", data={**PLAN, "as": "seller"}, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/channels"
    session.expire_all()
    deal = current_deal(session)
    cp07 = records.latest(session, deal.id, "CP-07")
    assert cp07.status == "done" and cp07.decided_by == "seller"
    # a person's simulated step works from any view, the seller's included
    as_persona(client, "seller")
    r = client.post("/channels/mls-entry", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/channels"
    session.expire_all()
    cp08 = records.latest(session, deal.id, "CP-08")
    assert cp08.kind == "human_required" and cp08.status == "simulated" and not cp08.blocking
    r = client.get("/channels")
    assert "The house is on the market" in r.text
    assert re.search(r'id="card-portals".*?class="ch-status">listed<', r.text, re.S)
    assert re.search(r'id="card-vendors".*?class="ch-status">booked<', r.text, re.S)
    t = client.get("/timeline").text
    for code in ("CP-05", "CP-25", "CP-06", "CP-26", "CP-07", "CP-08"):
        assert f'data-code="{code}"' in t, code


def test_the_flash_says_what_happened_once(client):
    _ready(client)
    client.get("/channels")
    r = client.post("/channels/authorise", data={**PLAN, "as": "seller"})
    assert "The seller signed the marketing plan" in r.text
    assert "The seller signed the marketing plan" not in client.get("/channels").text  # shown once


def test_mls_only_exposure_keeps_portals_dark(client):
    _ready(client)
    client.get("/channels")
    client.post("/channels/authorise", data={"decision": "sign", "exposure": "MLS Only", "granted": ["lockbox"],
                                             "as": "seller"})
    client.post("/channels/mls-entry")
    r = client.get("/channels")
    assert r.text.count("portals do not receive the listing") == 5
    assert "waiting for the seller&#39;s permission" in r.text  # photographer not authorised


def test_a_get_to_an_action_lands_on_the_screen(client):
    _ready(client)
    for url in ("/channels/authorise", "/channels/mls-entry"):
        r = client.get(url, follow_redirects=False)
        assert r.status_code == 303 and r.headers["location"] == "/channels", url
