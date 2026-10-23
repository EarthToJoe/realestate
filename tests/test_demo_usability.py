"""The demo for a presenter clicking through it (BUILD-FIX): no step link ever redirects, a step that waits for an
earlier one says what, where and who with a way there, fast-forward plays the earlier steps with the demo's
scripted choices, and "Decide as the seller" switches the persona in one tap while the decision stays the client's."""

import pytest

from app import db
from app.demo import walk
from app.records import service as records
from app.web import current_deal, steps
from tests.conftest import demo_intake

SCREENS = [sc["route"] for st in steps() for sc in st["screens"]]
BUILT = [st for st in steps() if st["built"]]


def as_persona(client, persona):
    """One persona cookie at a time (the server also sets it, on reset and on "Decide as")."""
    client.cookies.clear()
    client.cookies.set("persona", persona)


def _reset(client):
    client.cookies.clear()
    r = client.post("/demo/reset", follow_redirects=False)
    assert r.status_code == 303
    as_persona(client, "presenter")


def _deal():
    s = db.new_session()
    return s, current_deal(s)


def test_every_step_link_answers_200_after_a_reset(client):
    _reset(client)
    for route in SCREENS:
        r = client.get(route, follow_redirects=False)
        assert r.status_code == 200, (route, r.status_code, r.headers.get("location"))
        if route not in ("/intake", "/step/10"):
            assert 'id="gate-card"' in r.text, route
            assert 'data-missing="intake"' in r.text, route
            assert 'id="gate-go"' in r.text and 'href="/intake#intake-form"' in r.text, route
    # the step list and the compact step bar link to the same screens; none of them redirects either
    page = client.get("/pricing").text
    for st in steps():
        assert f'href="{st["screens"][0]["route"]}"' in page


def test_gate_card_says_what_where_who_and_offers_fast_forward(client):
    _reset(client)
    demo_intake(client)
    r = client.get("/copy")
    assert r.status_code == 200
    assert 'data-missing="agency"' in r.text and 'data-step="1"' in r.text
    assert "The seller acknowledges the agency disclosure form" in r.text and "The seller: their own decision" in r.text
    assert 'id="gate"' in r.text and "CP-03" in r.text  # the service gate's own words are kept
    assert 'data-decide-as="seller"' in r.text  # one tap to decide as the seller
    assert 'action="/demo/fast-forward/3"' in r.text and 'id="gate-ff"' in r.text
    # the client sees the card but not the presenter's fast-forward
    as_persona(client, "seller")
    r = client.get("/copy")
    assert 'id="gate-card"' in r.text and 'id="gate-ff"' not in r.text and 'data-decide-as="seller"' not in r.text


def test_step_list_offers_fast_forward_to_the_presenter_only(client):
    _reset(client)
    page = client.get("/intake").text
    for st in BUILT:
        assert (f'data-ff="{st["n"]}"' in page) == (st["n"] != 1), st["n"]
    assert 'data-ff="10"' not in page  # not built yet
    as_persona(client, "seller")
    assert "data-ff=" not in client.get("/intake").text


@pytest.mark.parametrize("st", BUILT, ids=lambda st: f"step{st['n']}")
def test_fast_forward_reaches_each_built_step(client, st):
    _reset(client)
    route = st["screens"][0]["route"]
    r = client.post(f"/demo/fast-forward/{st['n']}", data={"back": route}, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == route
    page = client.get(route)
    assert page.status_code == 200 and 'id="gate-card"' not in page.text, page.text[-3000:]
    s, deal = _deal()
    try:
        done = walk.done_map(s, deal)
        assert all(done[m.key] for m in walk.plan(st["n"], route)), [m.key for m in walk.plan(st["n"], route)
                                                                    if not done[m.key]]
        # nothing of the step itself was played (it is the presenter's to walk), except what its screen waits for
        own = [m for m in walk.WALK if m.step == st["n"] and m not in walk.plan(st["n"], route)]
        assert not any(done[m.key] for m in own if m.key != "intake"), [m.key for m in own if done[m.key]]
    finally:
        s.close()
    assert 'data-ff="%d"' % st["n"] not in page.text  # nothing left to play before it


def test_fast_forward_records_each_decision_as_the_client(client):
    _reset(client)
    assert client.post("/demo/fast-forward/9", follow_redirects=False).status_code == 303
    s, deal = _deal()
    try:
        by = {code: records.latest(s, deal.id, code) for code in
              ("CP-01", "CP-03", "CP-05", "CP-07", "CP-27", "CP-16", "CP-17", "CP-12", "CP-04", "CP-33")}
        for code in ("CP-01", "CP-03", "CP-05", "CP-07", "CP-27", "CP-12", "CP-04"):
            assert by[code].status == "done" and by[code].decided_by == "seller", code
        assert by["CP-16"].decided_by == "buyer"
        for code in ("CP-17", "CP-33"):
            assert by[code].status == "done" and by[code].decision in ("buyer=consent,seller=consent",
                                                                       "buyer=sign,seller=sign"), code
        assert all(cp.decided_by == "buyer" for cp in records.records(s, deal.id, "CP-18") if cp.status == "done")
        assert records.latest(s, deal.id, "CP-08").status == "simulated"  # the presenter's simulated human step
    finally:
        s.close()
    t = client.get("/contract").text
    assert 'id="signed"' in t and 'id="gate-card"' not in t
    assert "data-ff=" not in client.get("/timeline").text  # every built step walked


def test_fast_forward_to_a_screen_inside_the_step(client):
    _reset(client)
    r = client.post("/demo/fast-forward/8", data={"back": "/buyer/search"}, follow_redirects=False)
    assert r.headers["location"] == "/buyer/search"
    page = client.get("/buyer/search").text
    assert 'id="gate-card"' not in page
    s, deal = _deal()
    try:
        assert deal.buyer_id and not records.is_done(s, deal.id, "CP-16")  # the buyer's own signature is not played
    finally:
        s.close()


def test_fast_forward_is_the_presenters_only_and_only_to_built_steps(client):
    _reset(client)
    as_persona(client, "seller")
    assert client.post("/demo/fast-forward/2").status_code == 403
    as_persona(client, "presenter")
    assert client.post("/demo/fast-forward/10").status_code == 422
    s, deal = _deal()
    s.close()
    assert deal is None


def test_decide_as_switches_persona_and_returns_to_the_same_card(client):
    _reset(client)
    demo_intake(client)
    page = client.get("/intake/onboarding").text
    assert 'data-decide-as="seller"' in page and 'value="/intake/onboarding#rec-CP-01"' in page
    # the presenter acting directly is still refused
    assert client.post("/intake/agency", data={"decision": "acknowledge"}).status_code == 403
    client.cookies.clear()  # the cookie the button sets is the only one (no presenter cookie default needed)
    r = client.post("/persona", data={"persona": "seller", "back": "/intake/onboarding#rec-CP-01"},
                    follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/intake/onboarding#rec-CP-01"
    assert client.cookies.get("persona") == "seller"
    page = client.get("/intake/onboarding").text
    assert 'data-decide-as="seller"' not in page
    assert client.post("/intake/agency", data={"decision": "acknowledge"}, follow_redirects=False).status_code == 303
    s, deal = _deal()
    try:
        assert records.latest(s, deal.id, "CP-01").decided_by == "seller"
    finally:
        s.close()
    assert "Back to the Presenter" in client.get("/intake/onboarding").text


def test_decide_as_for_both_parties_offers_the_one_still_to_decide(client):
    _reset(client)
    client.post("/demo/fast-forward/8", data={"back": "/buyer/tour"})
    s, deal = _deal()
    try:
        walk.BY_KEY["buyer_agreement"].play(s, deal, None)
        s.commit()
    finally:
        s.close()
    client.post("/buyer/tour", data={"kind": "self-guided"})
    page = client.get("/buyer/tour").text
    assert 'data-decide-as="seller"' in page and 'data-decide-as="buyer"' in page
    as_persona(client, "buyer")
    client.post("/buyer/consent", data={"decision": "consent"})
    page = client.get("/buyer/tour").text
    assert 'data-decide-as="seller"' in page and 'data-decide-as="buyer"' not in page


def test_start_demo_asks_first_and_says_what_to_press(client):
    page = client.get("/").text
    assert 'href="/demo/start"' in page and 'action="/demo/reset"' not in page
    r = client.get("/demo/start?back=/pricing")
    assert r.status_code == 200 and "This resets the deal to the beginning" in r.text
    assert 'action="/demo/reset"' in r.text and 'href="/pricing"' in r.text
    assert 'href="//evil.example"' not in client.get("/demo/start?back=//evil.example").text
    r = client.post("/demo/reset")  # follows to step 1
    assert r.status_code == 200 and 'id="next-hint"' in r.text and "Start intake" in r.text
    assert 'value="146 Route 292"' in r.text


def test_compact_step_bar_on_every_screen(client):
    _reset(client)
    for route in ("/intake", "/pricing", "/timeline"):
        page = client.get(route).text
        assert 'class="stepbar"' in page and 'href="#step-list"' in page
