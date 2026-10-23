"""Slice 1 acceptance: Step 1 Intake end to end through the screens (SC1, CP-01/02/03/04/24, timeline)."""

import re

from app.records import service as records
from app.web import current_deal
from tests.conftest import as_persona, demo_intake


def test_demo_form_is_prefilled(client):
    r = client.get("/intake?demo=1")
    assert r.status_code == 200
    assert 'value="146 Route 292"' in r.text
    assert "DEMONSTRATION" in r.text


def test_profile_shows_all_three_source_chips(client, session):
    demo_intake(client)
    r = client.get("/intake/profile")
    assert r.status_code == 200
    assert 'data-source="public_record"' in r.text and 'data-source="seller"' in r.text
    r = client.post("/intake/infer", headers={"HX-Request": "true"})
    assert r.status_code == 200
    assert 'data-source="inferred"' in r.text
    assert "AI: fake" in r.text  # the badge always says which mode answered
    # every fact row carries a chip
    rows = re.findall(r'<tr data-field="[^"]+" data-source="([a-z_]+)"', r.text)
    assert len(rows) >= 30 and set(rows) == {"public_record", "seller", "inferred"}


def test_first_contact_notices_recorded(client, session):
    demo_intake(client)
    deal = current_deal(session)
    cp24 = records.records(session, deal.id, "CP-24")
    assert len(cp24) == 3 and all(r.kind == "automated" and r.status == "done" for r in cp24)
    assert {r.l_ids[0] for r in cp24} == {"L39"}  # catalogue IDs are per code; reasons name each notice
    reasons = " ".join(r.reason for r in cp24)
    for lid in ("L39", "L12", "L29"):
        assert lid in reasons


def test_client_decisions_block_until_made(client, session):
    demo_intake(client)
    # CP-03: signing before CP-01 is refused, even by the seller
    as_persona(client, "presenter")
    assert client.post("/intake/accept", follow_redirects=False).status_code == 303
    as_persona(client, "seller")
    r = client.post("/intake/sign", data={"decision": "sign"})
    assert r.status_code == 409 and "CP-01" in r.text
    # pricing (step 2) refuses to start before CP-03
    r = client.get("/step/2")
    assert 'id="gate"' in r.text and "CP-03" in r.text
    # CP-01 is the seller's: the presenter and the buyer are refused server-side
    for p in ("presenter", "buyer"):
        as_persona(client, p)
        assert client.post("/intake/agency", data={"decision": "acknowledge"}).status_code == 403
    as_persona(client, "seller")
    assert client.post("/intake/agency", data={"decision": "acknowledge"}, follow_redirects=False).status_code == 303
    as_persona(client, "presenter")
    assert client.post("/intake/sign", data={"decision": "sign"}).status_code == 403
    as_persona(client, "seller")
    assert client.post("/intake/sign", data={"decision": "sign"}, follow_redirects=False).status_code == 303
    deal = current_deal(session)
    session.expire_all()
    assert records.is_done(session, deal.id, "CP-01") and records.is_done(session, deal.id, "CP-03")
    assert 'id="gate"' not in client.get("/step/2").text
    # CP-04 stays pending (it blocks contract signing in slice 3) until the seller answers
    assert records.latest(session, deal.id, "CP-04").status == "pending"


def test_pcds_only_the_seller_answers_and_nothing_is_prefilled(client, session):
    demo_intake(client)
    r = client.get("/intake/disclosures")
    for name in ("owned_years", "defects", "fuel_tanks"):
        assert re.search(rf'name="{name}" value=""', r.text), f"{name} must start blank"
    answers = {k: "unknown" for k in ("owned_years", "occupied", "flood_insurance", "water_source", "sewage",
                                      "roof_leaks", "basement_water", "fuel_tanks", "defects")}
    as_persona(client, "presenter")
    assert client.post("/intake/pcds", data=answers).status_code == 403
    as_persona(client, "seller")
    assert client.post("/intake/pcds", data={**answers, "defects": ""}).status_code == 422
    assert client.post("/intake/pcds", data=answers, follow_redirects=False).status_code == 303
    session.expire_all()
    assert records.is_done(session, current_deal(session).id, "CP-04")


def test_cp02_marker_shows_rule_who_ids_and_link(client):
    demo_intake(client)
    client.post("/intake/accept")
    r = client.get("/intake/onboarding")
    block = r.text[r.text.index('id="rec-CP-02"'):]
    block = block[:block.index("does not stop the flow")]
    assert "NY law today" in r.text
    assert "licensed broker" in block.lower()
    assert "A licensed real estate broker" in block  # who
    for i in ("F12", "L1", "L5"):
        assert f">{i}<" in block
    assert 'href="https://realestate.hughesnode.com/docs-research-ws2-legal-licensing.html"' in block


def test_marker_never_blocks(client, session):
    demo_intake(client)
    client.post("/intake/accept")
    deal = current_deal(session)
    cp02 = records.latest(session, deal.id, "CP-02")
    assert cp02.kind == "law_marker" and not cp02.blocking and cp02.status == "done"


def test_timeline_shows_records_in_their_colours(client):
    demo_intake(client)
    client.post("/intake/accept")
    r = client.get("/timeline")
    assert r.status_code == 200
    for cls in ("chip-automated", "chip-client_decision", "chip-law_marker", "chip-third_party"):
        assert cls in r.text, cls
    for code in ("CP-01", "CP-02", "CP-03", "CP-04", "CP-24", "CP-35", "CP-20", "CP-34"):
        assert f'data-code="{code}"' in r.text, code
    assert 'id="hurdle-map"' in r.text
    # CP-35 standing marker is in the identity block on every page
    assert "none in this demonstration" in client.get("/intake/profile").text


def test_unknown_address_still_works(client):
    r = client.post("/intake", data={"street": "1 Nowhere Rd", "city": "Beacon", "zip": "12508",
                                     "seller_name": "A Person", "seller_email": "a@example.com",
                                     "seller_phone": "(845) 555-0100", "parking": "street"},
                    follow_redirects=True)
    assert r.status_code == 200 and "No public record was found" in r.text


def test_reset_starts_a_fresh_demo_and_keeps_spend(client, session):
    demo_intake(client)
    client.post("/intake/infer")
    from app.models import ModelCall

    before = session.query(ModelCall).count()
    r = client.post("/demo/reset", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/intake?demo=1"
    session.expire_all()
    assert current_deal(session) is None
    assert session.query(ModelCall).count() == before
