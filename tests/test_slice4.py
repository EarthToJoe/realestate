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
from app.demo import walk
from app.web import current_deal, steps, stops

PERSONAS = load_personas()


def as_persona(client, persona):
    client.cookies.clear()
    client.cookies.set("persona", persona)


def presenting(client, persona="presenter"):
    """The presenter's tools on ("I'm presenting", decision 50), viewing as `persona`."""
    as_persona(client, persona)
    client.cookies.set("presenting", "on")


def walked(client, through="/brand"):
    """Start over, then "Do this screen for me" on the last screen: the whole walk as the script plays it."""
    client.cookies.clear()
    assert client.post("/demo/reset", follow_redirects=False).status_code == 303
    presenting(client)
    r = client.post("/demo/play", data={"route": through}, follow_redirects=False)
    assert r.status_code == 303, r.text[-2000:]
    assert "flash" in r.headers.get("set-cookie", "")  # "The demo played this screen: ..."


def campaign_only(client):
    """The sale walked, then only the firm's campaign written (the script plants and fixes the headline once):
    the targeting and the publication still to do."""
    walked(client, "/contract")
    s, deal = _deal()
    try:
        walk._play(s, client.app.state.provider, [walk.BY_KEY["campaign"]])
    finally:
        s.close()


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
    page = client.get("/brand/targeting").text  # merged into /brand (decision 51)
    assert 'id="rec-CP-19"' in page and 'id="published"' in page and 'data-allowed="place"' in page
    assert page.count('data-notice=') == 4 and "check-fail" not in page.split('id="notices"')[1].split("</details>")[0]
    # the landing page's call to action is part of the mock and inert: no link, no button of this site
    cta = page.split('class="lp-cta"')[1].split("</p>")[0]
    assert 'class="mock-button"' in cta and "<a " not in cta and "<button" not in cta
    # the presenter's demo devices only when presenting
    client.cookies.delete("presenting")
    page = client.get("/brand").text
    assert 'id="try-age"' not in page and "plant-btn" not in page


def test_the_planted_claim_is_refused_and_publishing_waits(client):
    campaign_only(client)  # the play plants and fixes once: plant again by hand
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
    r = client.post("/brand/publish", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"].startswith("/brand?refused=1")  # Post/Redirect/Get
    r = client.get(r.headers["location"])
    assert 'id="refusal"' in r.text and "claims check refuses" in r.text
    client.post(f"/brand/piece/{lid}/fix")
    r = client.post("/brand/publish", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/brand#published"


@pytest.mark.parametrize("text,rule", [
    ("No lawyer needed: we do it all.", "CL-LAWYER"), ("You don't need an attorney.", "CL-LAWYER"),
    ("The AI that replaces your agent.", "CL-REPLACE"), ("Sell without a realtor.", "CL-REPLACE"),
    ("We are fully licensed.", "CL-LICENSED"), ("Rated five-star by sellers.", "CL-REVIEWS"),
    ("Guaranteed sale in 30 days.", "CL-GUARANTEE"), ("Save thousands in commission.", "CL-SAVINGS")])
def test_claims_check_catches(text, rule):
    assert rule in {f["rule_id"] for f in brand.claims_check(text)}


@pytest.mark.parametrize("text", [
    "Having a lawyer review your contract is always your choice, and we encourage it.",
    "A licensed home inspector inspects the house.", "One flat fee: $4,500, paid at closing.",
    "The AI reviews every offer with you."])
def test_claims_check_lets_honest_copy_through(text):
    assert not [f for f in brand.claims_check(text) if f["tier"] == "block"]


def test_targeting_refuses_every_blocked_criterion(client):
    campaign_only(client)
    assert 'id="try-age"' in client.get("/brand").text  # a presenter's tool
    for crit in brand.BLOCKED_IDS:
        r = client.post("/brand/targeting/try", data={"criterion": crit}, follow_redirects=False)
        assert r.status_code == 303, crit
        assert 'id="refusal"' in client.get(r.headers["location"]).text, crit
    s, deal = _deal()
    try:
        assert len(brand.state(deal)["refused"]) == len(brand.BLOCKED_IDS)
        with pytest.raises(brand.CampaignRefused):
            brand.check_targeting([{"id": "age"}, *brand.allowed_targeting()])
    finally:
        s.close()


def test_campaign_model_context_has_no_deal_or_person(client, provider):
    campaign_only(client)
    req = next(r for r in provider.requests if r["task"] == "brand.campaign")
    body = json.loads(req["user"])
    assert set(body) == {"firm", "firm_note", "founder", "area", "services", "flat_fee", "timeline", "ad_area"}


def test_founder_placeholder_is_a_styled_fill_in_chip(client):
    """Q49: no real person named without consent; the placeholder reads as a deliberate fill-in, never as a bug."""
    walked(client)
    page = client.get("/brand").text
    assert 'class="fill-in"' in page and 'title="Named once the founder agrees; see Q49"' in page
    assert "[Founder" not in page and "[FOUNDER]" not in page


def test_fees_match_the_plan():
    """WS4's working fees, as in the executive summary and the plan: $4,500 seller side, $3,500 buyer side."""
    from app.brokerage import brokerage
    from app.modules.buyer.service import buyer_agreement
    from app.modules.pricing.service import net_sheet

    b = brokerage()
    assert b["flat_fee"].startswith("$4,500 ") and b["buyer_fee"].startswith("$3,500 ")
    assert "demonstration figure" in b["flat_fee"] and "negotiable" in b["buyer_fee"]
    assert net_sheet(600_000)["lines"][0]["amount"] == 4500
    assert any("$3,500" in term for term in buyer_agreement()["terms"])


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
        assert [row.n for row in t.rows] == list(range(1, 12))  # the eleven steps of the path
        assert t.finished and all(ok for _, ok in t.story)
        assert any(r.code == "CP-19" for r in t.firm.records)  # the firm's campaign, after the sale
        # buyer-side records sit on the buyer's step
        assert any(r.step == 8 for r in records.records(s, deal.id, "CP-24"))
    finally:
        s.close()
    assert 'id="agent-acts"' in page and 'data-count="people"' in page
    assert "The whole sale, start to finish" in page and 'id="finale-lines"' in page
    assert page.count("does not stop the flow") == 1  # said once, here
    assert 'id="finale-start-over"' in page and "docs-executive-summary.html" in page
    assert "(played by the demo)" in page  # the walk's decisions were played by the script, and say so
    assert page.count('id="ab-primary"') == 1 and "How the firm finds sellers" in page


def test_timeline_keeps_a_change_as_history(client):
    walked(client, "/contract")
    r = client.post("/path/change/price", follow_redirects=False)
    assert r.status_code == 303
    s, deal = _deal()
    try:
        from app.modules.timeline import service as tl

        t = tl.build(s, deal)
        assert t.counts["superseded"] >= 1 and t.changes
        assert not t.finished
        price_row = next(row for row in t.rows if row.n == 4)
        assert any(r.status == "superseded" for r in price_row.records)
        assert all(r.status != "superseded" for r in price_row.standing)
    finally:
        s.close()
    page = client.get("/timeline").text
    assert 'id="changes"' in page and "chip-superseded" in page


# ---- walk-order numbering (Q47) and the guided demo (SC11) -----------------------------------------------------

def test_steps_are_numbered_along_the_path(client):
    walked(client, "/intake")
    page = client.get("/buyer").text
    assert "Step 8 of 11 · The buyer signs up" in page
    assert "Step 10 of 11 · The seller decides" in client.get("/offers").text
    assert "<title>The seller decides · Hudson Valley AI Realty</title>" in client.get("/offers").text
    order = [int(x) for x in __import__("re").findall(r'<li class="[^"]*" data-step="(\d+)"', page)]
    assert order[:11] == [st["n"] for st in steps()] == list(range(1, 12))


def test_presenting_walks_every_screen_with_its_notes(client):
    client.cookies.clear()
    client.post("/demo/reset", follow_redirects=False)
    presenting(client)
    for st in stops():
        route = st["route"]
        page = client.get(route).text
        assert 'id="presenter-notes"' in page and 'id="presenting-off"' in page, route
        if 'id="play-screen"' in page:
            r = client.post("/demo/play", data={"route": route}, follow_redirects=False)
            assert r.status_code == 303 and r.headers["location"] == route, route
        page = client.get(route).text
        assert 'id="gate-card"' not in page, route
    s, deal = _deal()
    try:
        assert records.is_done(s, deal.id, "CP-33") and brand.state(deal).get("published")
    finally:
        s.close()


def test_the_visitor_sees_no_presenter_tools(client):
    walked(client)
    client.cookies.delete("presenting")
    for st in stops():
        page = client.get(st["route"]).text
        for bit in ('id="presenter-notes"', 'id="play-screen"', 'id="gate-ff"', "Skip ahead"):
            assert bit not in page, (st["route"], bit)


def test_play_screen_is_the_presenters_only(client):
    client.cookies.clear()
    client.post("/demo/reset")
    as_persona(client, "presenter")  # presenting is off
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
    assert 'data-erased="yes"' in page and "retained 3 years:" in page and buyer_name not in page
    assert "(L17)" not in page  # research IDs stay off the visitor's screen
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
