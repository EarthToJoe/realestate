"""The one path (decisions 47 to 51): one primary button per screen from Start to the finale; nothing lost going
back; Change re-opens a decision and only what depends on it; the client's buttons record the client's decision and
the AI never records one; the visitor's layer shows the product only; the presenter's tools only when presenting."""

import re

import pytest

from app import db
from app.demo import path, walk
from app.models import Checkpoint, Deal, Event
from app.records import service as records
from app.web import current_deal, steps, stops
from tests.conftest import demo_intake

ROUTES = [st["route"] for st in stops()]


def as_persona(client, persona):
    client.cookies.set("persona", persona)


def _reset(client):
    client.cookies.clear()
    assert client.post("/demo/reset", follow_redirects=False).status_code == 303


def _deal():
    s = db.new_session()
    return s, current_deal(s)


def primary(client, route):
    """The action bar's one primary button on `route`: (method, url, fields) to press it."""
    t = client.get(route).text
    assert t.count('id="ab-primary"') == 1, (route, t.count('id="ab-primary"'))
    for m in re.finditer(r'<form method="post" action="([^"]+)" class="ab-form">(.*?)</form>', t, re.S):
        if 'id="ab-primary"' in m.group(2):
            return "post", m.group(1), dict(re.findall(r'name="([^"]+)" value="([^"]*)"', m.group(2)))
    b = re.search(r'<button[^>]*id="ab-primary"[^>]*>', t)
    if b and 'form="' in b.group(0):
        fid = re.search(r'form="([^"]+)"', b.group(0)).group(1)
        start = t.index(f'id="{fid}"')
        head = t.rfind("<form", 0, start)
        action = re.search(r'action="([^"]+)"', t[head:start + 40]).group(1)
        body = t[head:t.index("</form>", start)]
        fields = {}
        for tag in re.findall(r"<input[^>]*>", body):
            name = re.search(r'name="([^"]+)"', tag)
            val = re.search(r'value="([^"]*)"', tag)
            if not name:
                continue
            if 'type="radio"' in tag or 'type="checkbox"' in tag:
                if "checked" in tag:
                    if 'type="checkbox"' in tag:
                        fields.setdefault(name.group(1), [])
                        fields[name.group(1)].append(val.group(1) if val else "on")
                    else:
                        fields[name.group(1)] = val.group(1) if val else "on"
            else:
                fields.setdefault(name.group(1), val.group(1) if val else "")
        for sel in re.finditer(r'<select[^>]*name="([^"]+)"[^>]*>(.*?)</select>', body, re.S):
            opt = re.search(r'<option[^>]*selected[^>]*>([^<]*)<', sel.group(2)) or re.search(
                r'<option[^>]*>([^<]*)<', sel.group(2))
            vopt = re.search(r'<option[^>]*value="([^"]*)"[^>]*selected', sel.group(2))
            fields[sel.group(1)] = vopt.group(1) if vopt else (opt.group(1) if opt else "")
        nv = re.search(r'name="([^"]+)" value="([^"]+)"', b.group(0))
        if nv:
            fields[nv.group(1)] = nv.group(2)
        return "post", action, fields
    a = re.search(r'<a class="button[^"]*" href="([^"]+)" id="ab-primary"', t)
    assert a, route
    return "get", a.group(1), {}


def press(client, route):
    method, url, fields = primary(client, route)
    r = client.post(url, data=fields) if method == "post" else client.get(url)
    assert r.status_code == 200, (route, url, r.status_code, r.text[-1500:])
    return r


def walk_to(client, route_stop: str, limit=60):
    """Press only the primary button, from step 1, until the screen at `route_stop` is reached. Returns presses."""
    route, n = "/intake", 0
    while route != route_stop and n < limit:
        r = press(client, route)
        n += 1
        assert 'id="gate-card"' not in r.text, (route, r.url.path)
        route = r.url.path
    return n


# ---- the one-button walk ----------------------------------------------------------------------------------------

def test_the_one_button_walk_reaches_the_finale_in_30_presses_or_fewer(client):
    client.cookies.clear()
    r = client.get("/demo/start")  # a first visit goes straight in, no reset question
    assert r.url.path == "/intake" and 'id="reset-confirm"' not in r.text
    presses = 1 + walk_to(client, "/timeline")
    assert presses <= 30, presses
    s, deal = _deal()
    try:
        assert records.is_done(s, deal.id, "CP-33")  # signed by both
        assert s.query(Deal).count() == 1
    finally:
        s.close()
    t = client.get("/timeline").text
    assert "The whole sale, start to finish" in t


def test_every_stop_answers_200_after_a_reset_and_old_screens_redirect(client):
    _reset(client)
    for route in ROUTES:
        r = client.get(route, follow_redirects=False)
        assert r.status_code == 200, (route, r.status_code)
        if route != "/intake":
            assert 'id="gate-card"' in r.text and 'data-missing="intake"' in r.text, route
            assert 'href="/intake#intake-form"' in r.text, route
    for old, new in (("/intake/disclosures", "/intake/profile#checklist"), ("/pricing/advice", "/pricing#advice"),
                     ("/copy/mls", "/copy#mls"), ("/buyer/search", "/buyer#search"), ("/buyer/tour", "/buyer#tour"),
                     ("/disclosures/pcds", "/contract#pcds"), ("/brand/targeting", "/brand#targeting")):
        r = client.get(old, follow_redirects=False)
        assert r.status_code == 303 and r.headers["location"] == new, old
    assert client.get("/step/4", follow_redirects=False).headers["location"] == "/pricing"


def test_start_asks_only_when_a_sale_is_in_progress(client):
    _reset(client)
    assert client.get("/demo/start", follow_redirects=False).headers["location"] == "/intake"
    demo_intake(client)
    r = client.get("/demo/start?back=/pricing")
    assert 'id="reset-confirm"' in r.text and 'href="/pricing"' in r.text
    assert 'href="//evil.example"' not in client.get("/demo/start?back=//evil.example").text


# ---- nothing is lost ------------------------------------------------------------------------------------------

def test_step_1_reopens_filled_in_and_saving_again_keeps_the_same_deal(client):
    _reset(client)
    demo_intake(client)
    t = client.get("/intake").text
    assert 'value="146 Route 292"' in t and 'value="Holmes"' in t and "The seller's details, as saved" in t
    for _ in range(2):
        press(client, "/intake")  # Save and continue, again: nothing duplicated
    s, deal = _deal()
    try:
        assert s.query(Deal).count() == 1
        assert len(records.records(s, deal.id, "CP-24")) == 3
    finally:
        s.close()


def test_back_shows_what_was_decided_and_pressing_again_duplicates_nothing(client):
    _reset(client)
    walk_to(client, "/copy")
    t = client.get("/pricing").text  # Back to the price: the chosen price, as saved, with Change
    assert 'data-decided="CP-05"' in t and 'data-change="price"' in t
    press(client, "/pricing")  # the primary is now Continue
    s, deal = _deal()
    try:
        assert len(records.records(s, deal.id, "CP-05")) == 1
        assert s.query(Deal).count() == 1
    finally:
        s.close()


def test_a_get_to_an_action_lands_on_its_screen(client):
    _reset(client)
    for url, screen in (("/copy/ready-all", "/copy"), ("/intake/sign", "/intake/onboarding"),
                        ("/offers/decide", "/offers"), ("/path/act/price", "/")):
        r = client.get(url, follow_redirects=False)
        assert r.status_code in (303, 307), url
        assert r.headers["location"].split("#")[0] in (screen, "/"), (url, r.headers["location"])


# ---- Change -------------------------------------------------------------------------------------------------

def test_changing_the_price_names_what_reopens_and_supersedes_records(client):
    _reset(client)
    walk_to(client, "/channels")  # the listing copy exists
    t = client.get("/path/change/price").text
    assert "Change the list price?" in t and "the listing copy (step 5)" in t
    assert "the marketing plan" not in t  # not signed yet: nothing to re-open there
    r = client.post("/path/change/price")
    assert r.status_code == 200 and r.url.path == "/pricing" and 'id="flash"' in r.text
    s, deal = _deal()
    try:
        assert records.latest(s, deal.id, "CP-05").status == "pending"
        hist = records.records(s, deal.id, "CP-05", history=True)
        assert [c.status for c in hist] == ["superseded", "pending"]
        assert not walk.BY_KEY["copy"].done(s, deal)
        assert records.records(s, deal.id, "CP-06") == []  # the "ready" markers superseded with the copy
        assert any(c.status == "superseded" for c in records.records(s, deal.id, "CP-06", history=True))
        assert s.query(Event).filter(Event.kind == "change").count() >= 2
        assert walk.BY_KEY["listing"].done(s, deal)  # everything before stays
    finally:
        s.close()
    # the seller decides again; the AI writes the listing again
    press(client, "/pricing")
    s, deal = _deal()
    try:
        assert walk.BY_KEY["copy"].done(s, deal) and records.is_done(s, deal.id, "CP-05")
    finally:
        s.close()


def test_changing_the_sellers_name_mid_sale_keeps_the_deal_and_the_offers(client):
    _reset(client)
    client.cookies.set("presenting", "on")
    assert client.post("/demo/skip", data={"route": "/contract"}).status_code == 200
    s, deal = _deal()
    deal_id = deal.id
    s.close()
    form = {"street": "146 Route 292", "city": "Holmes", "zip": "12531", "seller_name": "Robin Q. Seller",
            "seller_email": "robin@example.com", "seller_phone": "(845) 555-0199"}
    from app.modules.intake.service import demo_input

    form.update(demo_input().facts)
    r = client.post("/intake", data=form)
    assert r.status_code == 200 and 'id="change-confirm"' not in r.text  # contact details: nothing to redo
    s, deal = _deal()
    try:
        from app.modules.offers import service as offers

        assert deal.id == deal_id and s.query(Deal).count() == 1
        assert offers.state(deal).get("accepted")
    finally:
        s.close()
    assert "Robin Q. Seller" in client.get("/contract").text


def test_changing_the_house_asks_first_and_names_what_is_redone(client):
    _reset(client)
    walk_to(client, "/pricing")
    from app.modules.intake.service import demo_input

    d = demo_input()
    form = {"street": d.street, "city": d.city, "zip": d.zip, "seller_name": d.seller_name,
            "seller_email": d.seller_email, "seller_phone": d.seller_phone, **d.facts, "roof_year": "2020"}
    r = client.post("/intake", data=form)
    import re as _re
    assert 'id="change-confirm"' in r.text, _re.findall(r"<h1[^>]*>([^<]*)|id=.flash.>([^<]*)", r.text)[:3]
    assert "price advice (step 4)" in r.text, _re.findall(r"re-opens ([^<]*)", r.text)[:2]
    s, deal = _deal()
    try:
        assert next(f.value for f in deal.property.facts if f.field == "RoofYear") == "2012"  # nothing yet
    finally:
        s.close()


# ---- decision 49: the client's button records the client's decision; the AI never decides ---------------------

def test_a_decision_is_recorded_as_the_client_the_button_names(client):
    _reset(client)
    demo_intake(client)
    as_persona(client, "presenter")
    for wrong in ("buyer", "presenter", "ai"):
        r = client.post("/path/act/agency", data={"as": wrong, "choice": "acknowledge"})
        assert r.status_code == 403, wrong
    r = client.post("/path/act/agency", data={"as": "seller", "choice": "acknowledge"})
    assert r.status_code == 200
    s, deal = _deal()
    try:
        cp = records.latest(s, deal.id, "CP-01")
        assert cp.status == "done" and cp.decided_by == "seller" and not cp.played
    finally:
        s.close()


def test_the_ai_never_records_a_client_decision(client, monkeypatch):
    """Walk the whole sale; every AI act (the pump and the AI's own buttons) runs with records.decide forbidden."""
    _reset(client)
    real = records.decide
    state = {"ai": False}

    def guarded(*a, **kw):
        assert not state["ai"], "the AI recorded a client decision"
        return real(*a, **kw)

    monkeypatch.setattr(records, "decide", guarded)
    real_pump = path.pump

    def ai_pump(*a, **kw):
        state["ai"] = True
        try:
            return real_pump(*a, **kw)
        finally:
            state["ai"] = False

    monkeypatch.setattr(path, "pump", ai_pump)
    walk_to(client, "/timeline")
    # and the AI's own buttons refuse to decide anything for a client, whatever they are sent
    for m in walk.WALK:
        if m.who == "ai":
            state["ai"] = True
            client.post(f"/path/act/{m.key}", data={"as": "seller", "choice": "sign"})
            state["ai"] = False


# ---- decision 50: the visitor's layer, and the presenter's ---------------------------------------------------

CODES = re.compile(r"\bCP-\d+|\b[FL]\d{1,3}\b|\bWS3-|FH-RULES")


def visible(html: str) -> str:
    """The text a visitor sees: no folds' insides, no menu, no tags or scripts."""
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)
    t = re.sub(r'<details class="menu".*?</details>\s*</header>', "</header>", t, flags=re.S)
    while True:
        t2 = re.sub(r"(<details[^>]*>\s*<summary[^>]*>.*?</summary>)(?:(?!<details).)*?</details>", r"\1", t,
                    flags=re.S)
        if t2 == t:
            break
        t = t2
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)


def test_the_visitors_layer_has_no_presenter_tools_and_no_codes(client):
    _reset(client)
    walk_to(client, "/timeline")
    for route in ROUTES:
        html = client.get(route).text
        text = visible(html)
        for bad in ("Do this screen for me", "screen 1 of", "View as", "⏩"):
            assert bad not in text, (route, bad)
        assert 'id="presenter-notes"' not in html and 'id="gate-ff"' not in html, route
        found = CODES.findall(text)
        assert not found, (route, found[:5])


def test_presenting_turns_on_the_notes_do_this_screen_and_skip_ahead(client):
    _reset(client)
    r = client.post("/demo/presenting", data={"on": "on", "back": "/pricing"}, follow_redirects=False)
    assert r.status_code == 303 and "presenting=on" in r.headers["set-cookie"]
    client.cookies.set("presenting", "on")
    t = client.get("/pricing").text
    assert 'id="presenter-notes"' in t and 'id="gate-ff"' in t and 'id="skip-ahead"' in t
    r = client.post("/demo/skip", data={"route": "/pricing"})
    assert r.status_code == 200 and 'id="gate-card"' not in r.text
    s, deal = _deal()
    try:
        cp = records.latest(s, deal.id, "CP-03")
        assert cp.status == "done" and cp.decided_by == "seller" and cp.played  # "(played by the demo)"
    finally:
        s.close()
    assert "(played by the demo)" in client.get("/intake/onboarding").text
    r = client.post("/demo/play", data={"route": "/pricing"})
    assert r.status_code == 200 and 'id="notes-play"' not in r.text  # nothing left to play here


def test_the_presenters_tools_are_refused_when_not_presenting(client):
    _reset(client)
    assert client.post("/demo/skip", data={"route": "/pricing"}).status_code == 403
    assert client.post("/demo/play", data={"route": "/intake"}).status_code == 403


@pytest.mark.parametrize("route", ["/contract/print", "/contract/draft.pdf", "/contract/draft.docx"])
def test_the_contract_documents_with_no_sale_show_the_not_yet_card(client, route):
    _reset(client)
    r = client.get(route)
    assert r.status_code == 200 and 'id="gate-card"' in r.text


# ---- an off-script figure in a recorded demo -------------------------------------------------------------------

def test_an_off_script_price_is_refused_plainly_in_a_recorded_demo(client, app):
    _reset(client)
    walk_to(client, "/pricing")
    app.state.provider.mode = "replay"  # recorded: the fake answers stand in for the recordings
    try:
        r = client.post("/pricing/choose", data={"as": "seller", "price": "999000"})
        assert r.status_code == 409 and 'id="put-back"' in r.text and "nothing was saved" in r.text
        s, deal = _deal()
        try:
            assert records.latest(s, deal.id, "CP-05").status == "pending"
        finally:
            s.close()
        t = client.get("/pricing").text
        assert "This recorded demo uses the figures it was recorded with" in t
    finally:
        app.state.provider.mode = "fake"


def test_the_progress_list_is_honest(client):
    _reset(client)
    demo_intake(client)
    t = client.get("/intake/onboarding").text
    assert 'data-step="1" data-status="done"' in t and 'data-step="2" data-status="done"' in t
    assert 'data-step="3" data-status="todo"' in t and 'aria-current="step"' in t
    assert "waiting for a decision" not in t
    assert len(steps()) == 11
