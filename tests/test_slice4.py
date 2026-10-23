"""Slice 4: step 10 (SC10), the finished timeline (SC9), the guided demo (SC11) and the PII baseline (export, delete,
no PII in logs, the model-context whitelist). The whole walk is played with the fake provider."""

import json
import sqlite3

import pytest

from app import db
from app.models import Event, Person
from app.modules.brand import service as brand
from app.modules.intake.service import load_personas
from app.records import service as records
from app.web import current_deal, steps

PERSONAS = load_personas()


def as_persona(client, persona):
    client.cookies.clear()
    client.cookies.set("persona", persona)


def walked(client, through="/brand/targeting"):
    """Start demo, then "Do this screen for me" on the last screen: the whole walk as the script plays it."""
    client.cookies.clear()
    assert client.post("/demo/reset", follow_redirects=False).status_code == 303
    as_persona(client, "presenter")
    r = client.post("/demo/play", data={"route": through}, follow_redirects=False)
    assert r.status_code == 303, r.text[-2000:]


def _deal():
    s = db.new_session()
    return s, current_deal(s)


def pii_values() -> list[str]:
    out = []
    for key in ("seller", "buyer"):
        p = PERSONAS.get(key) or {}
        out += [p.get(k) for k in ("legal_name", "email", "phone", "mailing_address") if p.get(k)]
    from app.modules.buyer.service import demo_input

    b = demo_input()
    out += [b["name"], b["email"], b["phone"]]
    return [v for v in out if v]


# ---- step 10 -------------------------------------------------------------------------------------------------

def test_campaign_is_checked_and_published_with_cp19(client):
    walked(client)
    s, deal = _deal()
    try:
        arts = brand.artifacts(s, deal)
        assert [a.channel for a in arts] == ["brand_landing", "brand_ad", "brand_magnet"]
        assert all(a.status == "ready" for a in arts)
        cp26 = [r for r in records.records(s, deal.id, "CP-26") if r.step == 10]
        assert len(cp26) >= 3  # one fair-housing and claims pass per piece, on step 10
        cp19 = records.latest(s, deal.id, "CP-19")
        assert cp19 and cp19.kind == "law_marker" and cp19.status == "done" and cp19.step == 10
        assert brand.state(deal)["published"]
    finally:
        s.close()
    page = client.get("/brand/targeting").text
    assert 'id="rec-CP-19"' in page and 'id="published"' in page and 'data-allowed="place"' in page
    landing = client.get("/brand").text
    assert landing.count('data-notice=') == 4 and "check-fail" not in landing.split('id="notices"')[1][:4000]


def test_the_planted_claim_is_refused_and_publishing_waits(client):
    walked(client, "/brand")  # campaign only (the play plants and fixes once): plant again by hand
    s, deal = _deal()
    try:
        landing = next(a for a in brand.artifacts(s, deal) if a.channel == "brand_landing")
        lid = landing.id
    finally:
        s.close()
    client.post(f"/brand/piece/{lid}/plant")
    page = client.get("/brand").text
    assert 'data-rule="CL-REPLACE"' in page and 'data-rule="CL-LAWYER"' in page and 'data-status="blocked"' in page
    client.post("/brand/targeting/set")
    r = client.post("/brand/publish")
    assert r.status_code == 409 and "claims check refuses" in r.text
    client.post(f"/brand/piece/{lid}/fix")
    assert client.post("/brand/publish", follow_redirects=False).status_code == 303


@pytest.mark.parametrize("text,rule", [
    ("No lawyer needed: we do it all.", "CL-LAWYER"), ("You don't need an attorney.", "CL-LAWYER"),
    ("The AI that replaces your agent.", "CL-REPLACE"), ("Sell without a realtor.", "CL-REPLACE"),
    ("We are fully licensed.", "CL-LICENSED"), ("Rated five-star by sellers.", "CL-REVIEWS"),
    ("Guaranteed sale in 30 days.", "CL-GUARANTEE"), ("Save thousands in commission.", "CL-SAVINGS")])
def test_claims_check_catches(text, rule):
    assert rule in {f["rule_id"] for f in brand.claims_check(text)}


@pytest.mark.parametrize("text", [
    "Having a lawyer review your contract is always your choice, and we encourage it.",
    "A licensed home inspector inspects the house.", "One flat fee: $4,995, paid at closing.",
    "The AI reviews every offer with you."])
def test_claims_check_lets_honest_copy_through(text):
    assert not [f for f in brand.claims_check(text) if f["tier"] == "block"]


def test_targeting_refuses_every_blocked_criterion(client):
    walked(client, "/brand")
    for crit in brand.BLOCKED_IDS:
        r = client.post("/brand/targeting/try", data={"criterion": crit})
        assert r.status_code == 409 and 'id="refusal"' in r.text, crit
    s, deal = _deal()
    try:
        assert len(brand.state(deal)["refused"]) == len(brand.BLOCKED_IDS)
        with pytest.raises(brand.CampaignRefused):
            brand.check_targeting([{"id": "age"}, *brand.allowed_targeting()])
    finally:
        s.close()


def test_campaign_model_context_has_no_deal_or_person(client, provider):
    walked(client, "/brand")
    req = next(r for r in provider.requests if r["task"] == "brand.campaign")
    body = json.loads(req["user"])
    assert set(body) == {"firm", "firm_note", "founder", "area", "services", "flat_fee", "timeline", "ad_area"}


# ---- the finished timeline (SC9) -----------------------------------------------------------------------------

def test_timeline_counts_road_hurdles_and_acts(client):
    walked(client)
    page = client.get("/timeline").text
    for key in ("escrow", "inspection", "repairs", "appraisal", "mortgage", "title", "walkthrough", "closing"):
        assert f'data-road="{key}"' in page, key
    assert "by " in page.split('id="closing"')[1].split("</details>")[0]  # dated from the signing
    s, deal = _deal()
    try:
        from app.modules.timeline import service as tl

        t = tl.build(s, deal)
        markers = {r.code for r in records.records(s, deal.id) if r.kind == "law_marker"}
        in_map = {h.record.code for _, hs in t.hurdles for h in hs}
        assert markers <= in_map  # every marker code, planned and standing included, is on the hurdle map
        assert len(t.acts) == sum(1 for r in records.records(s, deal.id) if r.kind == "law_marker"
                                  and r.status == "done" and r.code != "CP-35")
        assert t.counts["third_party"] == 7 and t.counts["human_required"] >= 2
        assert [row.shown for row in t.rows] == list(range(1, 11))
        # buyer-side records sit on the buyer's step
        assert any(r.step == 8 for r in records.records(s, deal.id, "CP-24"))
    finally:
        s.close()
    assert 'id="agent-acts"' in page and 'data-count="people"' in page


# ---- walk-order numbering (Q47) and the guided demo (SC11) -----------------------------------------------------

def test_steps_are_numbered_in_walk_order_on_screen(client):
    walked(client, "/intake")
    page = client.get("/buyer").text
    assert "Step 6 of 10: Buyer side" in page and "Step 6 of 10 · Buyer side" in page
    assert "Step 7 of 10: Offers" in client.get("/offers").text
    assert "Step 8 of 10: Contract" in client.get("/contract").text
    assert "<title>Offers · Hudson Valley AI Realty</title>" in client.get("/offers").text
    order = [int(x) for x in __import__("re").findall(r'<li class="[^"]*" data-step="(\d+)"', page)]
    assert order == [st["n"] for st in steps()] == [1, 2, 3, 4, 5, 8, 6, 7, 9, 10]


def test_guided_demo_walks_every_screen_with_a_narration_card(client):
    client.cookies.clear()
    r = client.post("/demo/reset", follow_redirects=False)
    assert "guide=on" in r.headers.get("set-cookie", "")
    client.cookies.set("guide", "on")
    client.cookies.set("persona", "presenter")
    route, seen = "/intake", []
    while route:
        page = client.get(route).text
        assert 'id="presenter-notes"' in page and 'data-guided="on"' in page, route
        seen.append(route)
        if 'id="play-screen"' in page:
            assert client.post("/demo/play", data={"route": route}, follow_redirects=False).status_code == 303
        page = client.get(route).text
        assert 'id="gate-card"' not in page, route
        nxt = __import__("re").search(r'id="notes-next"[^>]*|href="([^"]+)" id="notes-next"', page)
        route = nxt.group(1) if nxt and nxt.group(1) else None
    assert seen == [sc["route"] for st in steps() for sc in st["screens"]]


def test_play_screen_is_the_presenters_only(client):
    client.post("/demo/reset")
    as_persona(client, "seller")
    assert client.post("/demo/play", data={"route": "/intake/onboarding"}).status_code == 403


# ---- PII: export, delete, no PII in logs, model-context whitelist ---------------------------------------------

def test_export_has_every_field_and_the_access_log(client):
    walked(client)
    s, deal = _deal()
    sid, bid = deal.seller_id, deal.buyer_id
    s.close()
    client.get(f"/people/{sid}")
    data = json.loads(client.get(f"/people/{sid}/export").text)
    assert data["person"]["legal_name"] == PERSONAS["seller"]["legal_name"]
    assert data["person"]["email"] == PERSONAS["seller"]["email"]
    assert {"disclosures", "documents", "messages", "decisions", "access_log"} <= set(data)
    assert any(a["purpose"].startswith("privacy") for a in data["access_log"])
    assert any(d["record"] == "CP-03" for d in data["decisions"])
    # the information wall holds for the data, too
    as_persona(client, "seller")
    assert client.get(f"/people/{bid}").status_code == 403
    assert client.get(f"/people/{sid}/export").status_code == 200


def test_delete_erases_keeps_a_tombstone_and_logs_it(client, settings):
    walked(client)
    s, deal = _deal()
    bid = deal.buyer_id
    s.close()
    buyer_name = __import__("app.modules.buyer.service", fromlist=["x"]).demo_input()["name"]
    assert client.get(f"/people/{bid}/delete").status_code == 200
    assert client.post(f"/people/{bid}/delete", follow_redirects=False).status_code == 303
    page = client.get(f"/people/{bid}").text
    assert 'data-erased="yes"' in page and "retained 3 years (L17)" in page and buyer_name not in page
    s = db.new_session()
    try:
        p = s.get(Person, bid)
        assert p.legal_name == "[erased]" and p.email == "[erased]" and p.preapproval_amount is None and p.erased_at
        assert any("Erased the buyer's personal data" in e.summary for e in s.query(Event).all())
    finally:
        s.close()
    raw = sqlite3.connect(settings.data_dir / "realestate.db").execute("select legal_name from person").fetchall()
    assert all(buyer_name not in (r[0] or "") for r in raw)
    for route in ("/contract", "/buyer", "/contract/draft.pdf"):
        r = client.get(route)
        assert r.status_code == 200 and buyer_name.encode() not in r.content, route


def test_no_pii_in_logs_or_audit_after_the_whole_walk(client, settings):
    walked(client)
    for p in ("seller", "buyer"):
        as_persona(client, p)
        for route in ("/intake/onboarding", "/buyer", "/contract", "/offers", "/inbox"):
            client.get(route)
    text = settings.log_file.read_text()
    s = db.new_session()
    try:
        audit = " ".join(e.summary for e in s.query(Event).all())
    finally:
        s.close()
    for value in pii_values():
        assert value not in text, value
        assert value not in audit, value


def test_no_model_request_carries_pii(client, provider):
    """The model-context whitelist, over every call of the whole walk: no PII-registry value reaches the model."""
    walked(client)
    assert len(provider.requests) > 20
    body = json.dumps(provider.requests).lower()
    for value in pii_values():
        assert value.lower() not in body, value
    for token in ("680000", "665000"):  # the buyer's pre-approval and private limit stay on the buyer's side
        for req in provider.requests:
            if req["task"] in ("offers.advise", "contract.draft"):
                assert token not in req["user"], (req["task"], token)
