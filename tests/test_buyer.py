"""Slice 3 acceptance, SC8, on the one path (decisions 47 to 51): step 8 (the buyer signs up: intake, search, tour
and both consents, one screen) and step 9 (the buyer's offer). CP-30 (taking the buyer on), CP-24 notices, CP-16
blocks tours until the buyer agreement; CP-17 dual-agency consent of both clients before offer B; the buyer's AI
advises and drafts (CP-31) and negotiates (CP-13, buyer side); the buyer approves (CP-18). And the information
wall: no seller-side model call sees the buyer's limits, no buyer-side call the seller's; on screen, both sides'
views side by side."""

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


def test_buyer_screens_exist_and_old_addresses_land(client):
    buyer_signed(client)
    for path, lands, anchor in (("/buyer", "/buyer", None), ("/buyer/search", "/buyer", "search"),
                                ("/buyer/tour", "/buyer", "tour"), ("/buyer/offer", "/buyer/offer", None)):
        r = client.get(path)
        assert r.status_code == 200 and r.url.path == lands, path
        if anchor:
            assert f'id="{anchor}"' in r.text


def test_intake_asks_no_protected_class_question(client):
    inbox_approved(client)
    r = client.get("/buyer")
    form = r.text.split('id="buyer-form"')[1].split("</form>")[0]
    names = set(re.findall(r'name="([a-z_]+)"', form))
    assert names <= set(buyer.INTAKE_FIELDS), names - set(buyer.INTAKE_FIELDS)
    labels = re.sub(r"<[^>]+>", " ", form.split('class="help"')[0]).lower()
    for word in PROTECTED:
        assert not re.search(rf"\b{word}", labels), word
    # pre-filled with the demo buyer (decision 50), with a way to clear it, and no "Use the demo buyer" button
    assert f'value="{buyer.demo_input()["email"]}"' in form and 'data-clear-form="buyer-form"' in r.text
    assert "use-demo-buyer" not in r.text


def test_ai_takes_the_buyer_on_with_notices_and_cp16(client, session):
    buyer_client(client)
    deal = current_deal(session)
    assert records.latest(session, deal.id, "CP-30").status == "done"
    sent = [c for c in records.records(session, deal.id, "CP-24") if c.step == 8]
    assert len(sent) == 3
    assert records.latest(session, deal.id, "CP-16").status == "pending"
    r = client.get("/buyer")
    assert 'id="rec-CP-30"' in r.text and 'id="buyer-agreement"' in r.text and "negotiable" in r.text
    assert "Buyer 1" not in r.text
    as_persona(client, "seller")
    assert client.post("/buyer/sign", data={"decision": "sign"}).status_code == 403


def test_cp16_blocks_tours(client, session):
    buyer_client(client)
    r = client.post("/buyer/tour", data={"kind": "self-guided"})
    assert r.status_code == 409 and "buyer agreement" in r.text and "CP-16" not in r.text  # in plain words
    assert "tour" not in buyer.state(current_deal(session))


def test_tour_opens_dual_agency_and_is_self_guided(client, session):
    buyer_signed(client)
    assert client.post("/buyer/tour", data={"kind": "self-guided"}, follow_redirects=False).status_code == 303
    deal = current_deal(session)
    assert records.latest(session, deal.id, "CP-17").status == "pending"
    assert records.records(session, deal.id, "CP-28")  # one marker for self-guided tours (the inbox's or the buyer's)
    r = client.get("/buyer")
    assert 'id="booked"' in r.text and 'id="rec-CP-17"' in r.text and 'id="rec-CP-28"' in r.text


def test_search_has_no_steering_filter_and_the_alert_is_checked(client, session):
    buyer_signed(client)
    deal = current_deal(session)
    with pytest.raises(ValueError):
        buyer.search(deal, {"school_rating": 9})
    r = client.get("/buyer")
    assert 'data-listing="FIRM"' in r.text and "fictional" in r.text and "cannot steer" in r.text
    assert client.post("/buyer/alert", follow_redirects=False).status_code == 303
    r = client.get("/buyer")
    assert 'data-topic="alert"' in r.text and "identity-block" in r.text and "(simulated)" not in r.text


def test_offer_waits_for_both_consents(client, session):
    buyer_signed(client)
    client.post("/buyer/tour", data={"kind": "self-guided"})
    as_persona(client, "buyer")
    client.post("/buyer/consent", data={"decision": "consent"})
    as_persona(client, "presenter")
    r = client.post("/buyer/offer/advise")
    assert r.status_code == 409 and "dual agency" in r.text
    page = client.get("/buyer/offer").text  # step 9 says what it waits for: the seller's consent, on step 8
    assert 'id="gate-card"' in page and 'data-missing="dual_agency"' in page and 'data-step="8"' in page


def test_buyer_ai_drafts_with_cp31_and_only_the_buyer_approves(client, session):
    toured_and_consented(client)
    client.post("/buyer/offer/advise")
    deal = current_deal(session)
    assert records.latest(session, deal.id, "CP-31").status == "done"
    for p in ("seller", "presenter"):
        as_persona(client, p)
        assert client.post("/buyer/offer/approve", data={"decision": "approve"}).status_code == 403
    as_persona(client, "presenter")
    client.post("/buyer/offer/approve", data={"as": "buyer", "decision": "approve", "price": "604,000"})
    session.expire_all()
    b = next(o for o in offers.offers(deal) if o["label"] == "B")
    assert b["price"] == 604000 and b["side"] == "firm_buyer"
    cp = [c for c in records.records(session, deal.id, "CP-18") if c.attached_to == "buyer:offer"][-1]
    assert cp.status == "done" and cp.decided_by == "buyer"
    page = client.get("/buyer/offer").text
    assert 'id="offer-sent"' in page and 'href="/path/change/offer"' in page


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


def _wall(text: str) -> dict:
    wall = text.split('id="wall"')[1].split("</table>")[0]
    rows = re.findall(r'<tr><th scope="row">(.*?)</th>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>', wall, re.S)
    return {w: (a.strip(), b.strip()) for w, a, b in rows}


def test_screens_keep_the_wall_side_by_side(client):
    """Decision 49: no persona switch: steps 8 and 9 show what each side's AI can see, next to each other."""
    agreed_b(client)
    for path in ("/buyer", "/buyer/offer"):
        by = _wall(client.get(path).text)
        assert by["The most the buyer would pay"] == ("hidden", "$665,000"), (path, by)
        assert by["The lowest price the seller allows"] == ("$618,000", "hidden"), (path, by)


def test_a_decision_is_the_client_named_on_the_button(client, session):
    """Decision 49: a button records the decision as the client it names; the record service still refuses the
    wrong client, and the presenter never decides."""
    buyer_client(client)
    assert client.post("/buyer/sign", data={"as": "seller", "decision": "sign"}).status_code == 403
    assert client.post("/buyer/sign", data={"as": "presenter", "decision": "sign"}).status_code == 403
    r = client.post("/buyer/sign", data={"as": "buyer", "decision": "sign"}, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"].startswith("/buyer")  # Post/Redirect/Get
    session.expire_all()
    deal = current_deal(session)
    cp = records.latest(session, deal.id, "CP-16")
    assert cp.status == "done" and cp.decided_by == "buyer" and not cp.played
    # the AI's work followed on its own (the alert, the tour); the consents are the clients' own
    assert buyer.state(deal).get("tour") and records.latest(session, deal.id, "CP-17").status == "pending"
    for p in ("buyer", "seller"):
        r = client.post("/path/act/dual_agency", data={"as": p, "choice": "consent"}, follow_redirects=False)
        assert r.status_code == 303
    session.expire_all()
    deal = current_deal(session)
    cp17 = records.latest(session, deal.id, "CP-17")
    assert cp17.status == "done" and cp17.decision == "buyer=consent,seller=consent"
    assert buyer.state(deal).get("advice")  # the buyer's AI drafted the offer at once (step 9)


def test_the_form_reopens_filled_in_and_a_contact_change_keeps_everything(client, session):
    offer_b(client)
    page = client.get("/buyer?edit=1").text
    form = page.split('id="buyer-form"')[1].split("</form>")[0]
    d = buyer.demo_input()
    assert f'value="{d["email"]}"' in form and 'value="665000"' in form  # what was saved, not blanks
    data = {**d, "name": "Robin Q. Example"}
    assert client.post("/buyer", data=data, follow_redirects=False).status_code == 303
    session.expire_all()
    deal = current_deal(session)
    assert deal.buyer.legal_name == "Robin Q. Example"
    assert records.latest(session, deal.id, "CP-16").status == "done"
    assert any(o["label"] == "B" for o in offers.offers(deal))  # the offer is still there
    # a change to the money asks first, and says what it re-opens
    r = client.post("/buyer", data={**data, "max_price": "700000"})
    assert r.status_code == 200 and 'id="change-confirm"' in r.text and "the buyer&#39;s AI&#39;s offer" in r.text
    session.expire_all()
    assert buyer.instructions(session, current_deal(session)).confidential["maximum_price"] == 665000


def test_missing_answers_are_marked_next_to_the_field(client):
    inbox_approved(client)
    r = client.post("/buyer", data={"name": "", "email": "", "max_price": ""})
    assert r.status_code == 422
    for f in ("name", "email", "max_price"):
        assert f'id="err-{f}"' in r.text and f'aria-describedby="err-{f}"' in r.text


def test_offer_screen_has_the_offer_form_and_a_terms_table(client):
    toured_and_consented(client)
    r = client.get("/buyer/offer")
    assert 'id="offer-form"' in r.text and 'name="as" value="buyer"' in r.text
    assert 'class="table is-narrow is-fullwidth terms"' in r.text
    r = client.get("/buyer/offer/approve")  # a refresh after the form lands on the screen, never a 405
    assert r.status_code == 200 and r.url.path == "/buyer/offer"


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
