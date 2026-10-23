"""Slice 3 acceptance, SC5: Step 5 Communications. CP-27 before any reply; the AI answers and sends on its own;
only seller decisions reach the seller; disclosures at first contact; the identity block on every outgoing message;
showings owner-hosted (CP-10) and self-guided (CP-28); feedback logged; CP-09 on each message that discusses the
listing; legal and neighbourhood questions answered safely; the model never sees confidential instructions."""

import json

from app.brokerage import identity_block
from app.models import ClientInstructions
from app.modules.inbox import service as inbox
from app.records import service as records
from app.web import current_deal
from tests.conftest import as_persona, listed, priced


def ready(client):
    listed(client)
    priced(client)
    assert client.get("/inbox").status_code == 200


def approved(client, self_guided=True):
    ready(client)
    as_persona(client, "seller")
    data = {"decision": "approve", **({"self_guided": "yes"} if self_guided else {})}
    assert client.post("/inbox/approve", data=data, follow_redirects=False).status_code == 303
    as_persona(client, "presenter")


def test_inbox_refuses_before_price_chosen(client):
    listed(client)
    r = client.get("/inbox")
    assert 'id="gate"' in r.text and "CP-05" in r.text


def test_no_reply_before_cp27(client, session):
    ready(client)
    r = client.post("/inbox/next", follow_redirects=False)
    assert r.status_code == 409 and "CP-27" in r.text
    assert inbox.messages(session, current_deal(session)) == []


def test_only_the_seller_approves_cp27(client, session):
    ready(client)
    as_persona(client, "buyer")
    r = client.post("/inbox/approve", data={"decision": "approve"}, follow_redirects=False)
    assert r.status_code == 403
    assert not records.is_done(session, current_deal(session).id, "CP-27")


def test_ai_answers_all_on_its_own(client, session):
    approved(client)
    assert client.post("/inbox/all", follow_redirects=False).status_code == 303
    deal = current_deal(session)
    msgs = inbox.messages(session, deal)
    out = [m for m in msgs if m.direction == "out"]
    assert len([m for m in msgs if m.direction == "in"]) == len(inbox.ENQUIRIES)
    assert out and all(m.status == "sent" for m in out)
    assert all(m.extra["identity_block"] == identity_block() and m.extra["fair_housing"] == "passed" for m in out)
    # agency form and fair-housing notice at first contact on each thread, once
    threads = {m.thread for m in out}
    firsts = [m for m in out if m.extra["first_contact"]]
    assert {m.thread for m in firsts} == threads and len(firsts) == len(threads)
    assert all(inbox.AGENCY_NOTE in m.body for m in firsts)
    assert len(records.records(session, deal.id, "CP-24")) >= len(threads)
    # CP-09 once per sent message that discusses the listing; not for the legal or neighbourhood replies
    cp09 = records.records(session, deal.id, "CP-09")
    assert len(cp09) == len([m for m in out if m.topic not in ("legal", "neighbourhood")])
    by_topic = {m.topic: m for m in out}
    assert "can't give legal advice" in by_topic["legal"].body and "own lawyer" in by_topic["legal"].body
    assert "data.nysed.gov" in by_topic["neighbourhood"].body
    assert "oil heat" in by_topic["facts"].extra["disclosed"]
    r = client.get("/inbox")
    assert "sent (simulated)" in r.text and identity_block() in r.text and 'id="feedback-log"' in r.text


def test_showings_owner_hosted_and_self_guided(client, session):
    approved(client)
    client.post("/inbox/all")
    deal = current_deal(session)
    assert records.latest(session, deal.id, "CP-10").status == "simulated"
    assert records.latest(session, deal.id, "CP-28").status == "done"
    assert len(records.records(session, deal.id, "CP-29")) >= 3  # two bookings and the feedback
    r = client.get("/inbox")
    assert 'id="rec-CP-28"' in r.text and 'id="rec-CP-10"' in r.text


def test_self_guided_needs_the_sellers_permission(client, session):
    approved(client, self_guided=False)
    client.post("/inbox/all")
    deal = current_deal(session)
    assert records.latest(session, deal.id, "CP-28") is None
    assert len(records.records(session, deal.id, "CP-10")) == 2


def test_only_seller_questions_reach_the_seller(client, session):
    approved(client)
    client.post("/inbox/all")
    deal = current_deal(session)
    cards = inbox.seller_cards(session, deal)
    assert sorted(m.thread for m in cards) == ["C", "G"]  # the price question; the showing outside the windows
    m = next(c for c in cards if c.thread == "C")
    as_persona(client, "buyer")
    assert client.post(f"/inbox/answer/{m.id}", data={"decision": "invite_offer"}).status_code == 403
    as_persona(client, "seller")
    assert client.post(f"/inbox/answer/{m.id}", data={"decision": "invite_offer"}).status_code == 200
    session.expire_all()
    assert [c.thread for c in inbox.seller_cards(session, deal)] == ["G"]
    replies = [x for x in inbox.messages(session, deal) if x.thread == "C" and x.direction == "out"]
    assert replies[-1].topic == "negotiation" and "written offer" in replies[-1].body


def test_reply_model_sees_no_confidential_instructions(client, session, provider):
    approved(client)
    deal = current_deal(session)
    ins = session.query(ClientInstructions).filter_by(deal_id=deal.id, side="seller").one()
    ins.confidential = {"price_floor": 611000, "motivation": "relocating"}
    session.commit()
    client.post("/inbox/next")
    sent = [r for r in provider.requests if r["task"] == "inbox.reply"]
    assert sent
    blob = json.dumps(sent[-1])
    for leak in ("611000", "relocating", "price_floor", "Dana", "Okafor", "555-0142"):
        assert leak not in blob, leak


def test_failed_fair_housing_check_holds_the_message(client, session, provider, monkeypatch):
    approved(client)
    monkeypatch.setattr(inbox, "LEGAL_REPLY", "Perfect for a young family, steps from the church.")
    for _ in range(5):
        client.post("/inbox/next")
    deal = current_deal(session)
    legal = [m for m in inbox.messages(session, deal) if m.direction == "out" and m.topic == "legal"]
    assert legal and legal[0].status == "held"
    assert not any(r.attached_to == f"message:{legal[0].id}" for r in records.records(session, deal.id, "CP-24"))
