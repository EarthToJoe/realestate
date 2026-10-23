"""Provider, spend log, replay, information wall, audit chain, review pages, brokerage identity."""

import pytest
from pydantic import BaseModel
from sqlalchemy import text

from app import audit, db
from app.model import provider as prov
from app.model.context import AgentContext
from app.models import ClientInstructions, Deal, ModelCall, Property
from tests.conftest import demo_intake


class Out(BaseModel):
    answer: str


class StubLive(prov.AnthropicProvider):
    """A live provider whose API call is replaced, to test recording and the spend cap without the network."""

    def __init__(self, store, cap):
        self.store, self.cap, self.calls = store, cap, 0

    def _call(self, req, h, schema, s):
        spent = prov.live_spend(s)
        if spent >= self.cap:
            raise prov.SpendCapReached("cap")
        self.calls += 1
        out = schema(answer="recorded")
        self.store.put(h, req, out.model_dump())
        return prov.ModelResult(output=out, mode="live", model=req["model"], cost_usd=0.5), {"input": 10, "output": 5}


def test_fake_call_is_logged_with_cost_fields(client, session):
    demo_intake(client)
    client.post("/intake/infer")
    row = session.query(ModelCall).one()
    assert (row.module, row.task, row.mode, row.side) == ("intake", "intake.infer_gaps", "fake", "seller")
    assert row.model == "claude-haiku-5-5" and row.request_hash and row.prompt_version == "infer_gaps.v1"


def test_replay_answers_what_live_recorded_and_cap_refuses(session, tmp_path):
    store = prov.ReplayStore(tmp_path / "rep", read_dirs=[])
    live = StubLive(store, cap=0.6)
    r1 = live.generate("probe.mask_roundtrip", Out, {"q": 1}, s=session, module="probe", system="s",
                       prompt_version="v1")
    assert r1.mode == "live" and live.calls == 1
    replay = prov.ReplayProvider(store)
    r2 = replay.generate("probe.mask_roundtrip", Out, {"q": 1}, s=session, module="probe", system="s",
                         prompt_version="v1")
    assert r2.mode == "replay" and r2.output.answer == "recorded" and r2.cost_usd == 0 and r2.recorded_at
    with pytest.raises(prov.ReplayMiss):
        replay.generate("probe.mask_roundtrip", Out, {"q": 2}, s=session, module="probe", system="s",
                        prompt_version="v1")
    live.generate("probe.mask_roundtrip", Out, {"q": 3}, s=session, module="probe", system="s", prompt_version="v1")
    with pytest.raises(prov.SpendCapReached):  # $1.00 logged >= $0.60 cap
        live.generate("probe.mask_roundtrip", Out, {"q": 4}, s=session, module="probe", system="s",
                      prompt_version="v1")


def test_cost_formula():
    # Haiku: 3k in, 1k out = 0.0003 + 0.0005
    assert prov.cost_usd("claude-haiku-5-5", 3000, 1000) == pytest.approx(0.0008)
    assert prov.cost_usd("claude-sonnet-5-5", 0, 0, cache_read=1_000_000) == pytest.approx(0.10)


def test_information_wall(session):
    p = Property(street="146 Route 292", city="Holmes", zip="12531")
    session.add(p)
    session.flush()
    d = Deal(property_id=p.id)
    session.add(d)
    session.flush()
    session.add_all([
        ClientInstructions(deal_id=d.id, side="seller", authority={"price_floor": 615000},
                           confidential={"motivation": "relocating"}),
        ClientInstructions(deal_id=d.id, side="buyer", confidential={"maximum_price": 665000}),
    ])
    session.flush()
    seller_ctx = str(AgentContext(session, d, "seller").build())
    buyer_ctx = str(AgentContext(session, d, "buyer").build())
    assert "615000" in seller_ctx and "665000" not in seller_ctx
    assert "665000" in buyer_ctx and "615000" not in buyer_ctx and "relocating" not in buyer_ctx


def test_audit_chain_and_append_only(client, session):
    demo_intake(client)
    client.post("/intake/accept")
    assert audit.verify_chain(session)
    with pytest.raises(Exception, match="append-only"):
        with db.engine().begin() as conn:
            conn.execute(text("UPDATE events SET summary='x' WHERE seq=1"))
    with pytest.raises(Exception, match="append-only"):
        with db.engine().begin() as conn:
            conn.execute(text("DELETE FROM events"))


def test_review_pages_keep_their_addresses(client):
    home = client.get("/")
    assert home.status_code == 200 and "Start demo" in home.text and 'href="/index.html"' in home.text
    assert "review home" in client.get("/index.html").text
    assert client.get("/docs-success-criteria.html").status_code == 200
    assert client.get("/healthz").json()["ok"] is True


def test_identity_block_and_demo_mark_on_every_page(client):
    demo_intake(client)
    for path in ("/", "/intake", "/intake/profile", "/intake/disclosures", "/intake/onboarding", "/timeline",
                 "/step/5"):
        t = client.get(path).text
        assert "DEMONSTRATION" in t, path
        assert "Licensed broker of record: required by NY law; none in this demonstration" in t, path
        assert "Hudson Valley AI Realty" in t, path


def test_persona_switch(client):
    r = client.post("/persona", data={"persona": "seller", "back": "/timeline"}, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/timeline"
    assert "persona=seller" in r.headers["set-cookie"]
    r = client.post("/persona", data={"persona": "seller", "back": "//evil.example"}, follow_redirects=False)
    assert r.headers["location"] == "/"


def test_shipped_replay_answers_the_demo_intake(settings):
    """The recorded live run (replays/) answers the demo-house intake with no network and no key."""
    from fastapi.testclient import TestClient

    from app.main import create_app

    store = prov.ReplayStore(settings.data_dir / "replays", read_dirs=[prov.SHIPPED_REPLAYS])
    c = TestClient(create_app(settings, prov.ReplayProvider(store)))
    demo_intake(c)
    r = c.post("/intake/infer", headers={"HX-Request": "true"})
    assert 'data-mode="replay"' in r.text and "Recorded run" in r.text and 'data-source="inferred"' in r.text
