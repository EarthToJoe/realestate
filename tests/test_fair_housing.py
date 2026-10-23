"""The fair-housing pipeline (spec section 5): rules fixture, pipeline fixture (100% recall on disallowed, at
most 10% of allowed flagged), the planted violation, and `test_no_unchecked_send`."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
import yaml

from app import db
from app.fairhousing import check as fh
from app.model.provider import FakeProvider, ReplayProvider, ReplayStore, SHIPPED_REPLAYS
from app.models import CopyArtifact, FairHousingResult
from app.modules.listing_copy import service as copy_service
from app.web import current_deal
from tests.conftest import as_persona, drafted

FIXTURES = yaml.safe_load((Path(__file__).parent / "fixtures" / "fair_housing.yaml").read_text())["phrases"]
NY_CLASSES = yaml.safe_load(fh.RULES_PATH.read_text())["classes"]["new_york"]


def _tier(findings) -> str:
    tiers = {f.tier if hasattr(f, "tier") else f["tier"] for f in findings}
    return "disallowed" if "block" in tiers else "warn" if "warn" in tiers else "allowed"


def test_fixture_set_size_and_coverage():
    assert len(FIXTURES) >= 40
    disallowed = [p for p in FIXTURES if p["expected"] == "disallowed"]
    classes = " ".join(p["class"] for p in disallowed)
    for c in NY_CLASSES:  # every NY class (which include the federal ones) at least once
        key = {"color": "color", "creed": "creed"}.get(c, c)
        assert key in classes, f"no disallowed fixture for {c}"
    assert "steering" in classes and "blockbusting" in classes
    assert any(p["expected"] == "warn" for p in FIXTURES)
    assert sum(p["expected"] == "allowed" for p in FIXTURES) >= 10


def test_rules_fixture():
    """Every disallowed phrase marked rules_must_catch is caught by the rules alone; no allowed phrase is flagged
    by the rules at all; every warn phrase gets a warn, never a block."""
    for p in FIXTURES:
        got = _tier(fh.rules_pass(p["text"]))
        if p["expected"] == "disallowed" and p.get("rules_must_catch", True):
            assert got == "disallowed", p["text"]
        elif p["expected"] == "allowed":
            assert got == "allowed", p["text"]
        elif p["expected"] == "warn":
            assert got == "warn", p["text"]


def _pipeline(provider, s) -> dict:
    caught, missed, flagged_allowed, allowed = 0, [], [], 0
    for i, p in enumerate(FIXTURES):
        res = fh.run(s, text=p["text"], provider=provider, entity="fixture", entity_id=i, version=1, deal_id=None,
                     channel="fixture")
        tier = _tier(res.findings)
        if p["expected"] == "disallowed":
            if tier == "disallowed":
                caught += 1
            else:
                missed.append(p["text"])
        if p["expected"] == "allowed":
            allowed += 1
            if tier != "allowed":
                flagged_allowed.append(p["text"])
    total = caught + len(missed)
    return {"recall": caught / total, "missed": missed, "fp_rate": len(flagged_allowed) / allowed,
            "flagged_allowed": flagged_allowed, "disallowed": total, "allowed": allowed}


def test_pipeline_merge_with_fake_model(app):
    s = db.new_session()
    try:
        out = _pipeline(FakeProvider(), s)
    finally:
        s.close()
    assert out["recall"] == 1.0, out["missed"]
    assert out["fp_rate"] <= 0.10, out["flagged_allowed"]


def test_pipeline_fixture(app, request):
    """Rules + the recorded model review (replays committed in replays/). `--live` records them again (~$0.02)."""
    live = request.config.getoption("--live")
    s = db.new_session()
    try:
        if live:
            from app.config import Settings
            from app.model.provider import AnthropicProvider

            key = Settings().secret("ANTHROPIC_API_KEY")
            if not key:
                pytest.skip("--live needs /srv/realestate/secrets/ANTHROPIC_API_KEY")
            provider = AnthropicProvider(key, ReplayStore(SHIPPED_REPLAYS), spend_cap_usd=12)
        else:
            provider = ReplayProvider(ReplayStore(SHIPPED_REPLAYS, [SHIPPED_REPLAYS]))
            missing = [p["text"] for p in FIXTURES if fh.model_pass(s, p["text"], provider, "fixture")[0] is None]
            if missing:
                pytest.skip(f"{len(missing)} fixture replays not recorded; run pytest --live once")
        out = _pipeline(provider, s)
        if os.environ.get("FH_REPORT"):
            print(out)
    finally:
        s.close()
    assert out["recall"] == 1.0, out["missed"]
    assert out["fp_rate"] <= 0.10, out["flagged_allowed"]


def _portal(session):
    deal = current_deal(session)
    return deal, next(a for a in copy_service.artifacts(session, deal) if a.channel == "portal")


def test_planted_violation_demo(client, session):
    drafted(client)
    deal, art = _portal(session)
    r = client.post(f"/copy/{art.id}/plant", headers={"HX-Request": "true"})
    assert r.status_code == 200
    assert 'data-rule="FH-FAM-01"' in r.text and "familial status" in r.text and "42 U.S.C. §3604(c)" in r.text
    assert 'data-rule="FH-REL-02"' in r.text  # the landmark is a warn
    assert '<mark class="fh-block"' in r.text and "fixed version" in r.text
    session.expire_all()
    assert art.status == "blocked"
    # the AI cannot mark it ready while the block finding stands
    r = client.post(f"/copy/{art.id}/ready", follow_redirects=False)
    assert r.status_code == 409 and "FH-FAM-01" in r.text
    # apply the AI's fix: re-check passes, then it can be marked ready
    r = client.post(f"/copy/{art.id}/fix", headers={"HX-Request": "true"})
    session.expire_all()
    assert art.status == "passed", r.text
    assert "young family" not in art.text.lower() and "church" not in art.text.lower()
    assert client.post(f"/copy/{art.id}/ready", follow_redirects=False).status_code == 303
    session.expire_all()
    assert art.status == "ready"


def test_no_unchecked_send(client, session, provider):
    """No artifact reaches "ready to publish" without a passing fair_housing_result for its exact current text.
    (Slice 3's messages use the same `require_pass` gate before "sent (simulated)".)"""
    drafted(client)
    deal = current_deal(session)
    # 1. an artifact that was never checked
    raw = CopyArtifact(deal_id=deal.id, channel="social_9", title="Unchecked", text="Raised ranch on 4.18 acres.")
    session.add(raw)
    session.commit()
    with pytest.raises(fh.FairHousingBlocked, match="No fair-housing check"):
        copy_service.mark_ready(session, deal, raw)
    # 2. text changed after a passing check (same version number, different text)
    _, art = _portal(session)
    copy_service.check(session, deal, art, provider)
    art.text = art.text + " Perfect bachelor pad."
    with pytest.raises(fh.FairHousingBlocked, match="changed"):
        copy_service.mark_ready(session, deal, art)
    session.rollback()
    # 3. the model review pass did not run: the gate stays shut even with no rule hit
    from app.model.provider import ReplayMiss

    class Down(FakeProvider):
        def _call(self, req, h, schema, s):
            raise ReplayMiss("not recorded")

    soc = next(a for a in copy_service.artifacts(session, deal) if a.channel == "social_1")
    res = copy_service.check(session, deal, soc, Down())
    assert not res.passed and res.model_error
    with pytest.raises(fh.FairHousingBlocked, match="model review"):
        copy_service.mark_ready(session, deal, soc)
    session.commit()
    # 4. through the screens: mark everything; then the invariant holds for every ready artifact
    as_persona(client, "presenter")
    client.post("/copy/ready-all")
    session.expire_all()
    ready = [a for a in copy_service.artifacts(session, deal) if a.status == "ready"]
    assert ready
    for a in ready:
        res = fh.latest_result(session, "copy_artifact", a.id)
        assert res.passed and res.version == a.version and res.text_hash == fh.text_hash(a.text), a.title
    assert soc.status != "ready" and raw.status != "ready"
    n_ready_records = len([r for r in session.query(FairHousingResult).all() if r.passed])
    assert n_ready_records >= len(ready)
