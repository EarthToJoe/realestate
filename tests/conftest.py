from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app import db
from app.config import Settings
from app.main import create_app
from app.model.provider import FakeProvider


def pytest_addoption(parser):
    parser.addoption("--live", action="store_true", default=False,
                     help="re-record the fair-housing fixture replays with live model calls (~$0.02)")


@pytest.fixture()
def settings(tmp_path):
    review = tmp_path / "public"
    review.mkdir()
    (review / "index.html").write_text("<h1>Real estate: review home</h1>")
    (review / "docs-success-criteria.html").write_text("<h1>Success criteria</h1>")
    return Settings(data_dir=tmp_path / "data", secrets_dir=tmp_path / "no-secrets", review_dir=review,
                    model_mode="fake", log_file=tmp_path / "app.log")


@pytest.fixture()
def provider():
    return FakeProvider()


@pytest.fixture()
def app(settings, provider):
    return create_app(settings, provider)


@pytest.fixture()
def client(app):
    return TestClient(app)


def as_persona(client: TestClient, persona: str) -> None:
    client.cookies.set("persona", persona)


@pytest.fixture()
def session(app):
    s = db.new_session()
    yield s
    s.close()


def demo_intake(client: TestClient) -> None:
    """Submit the intake form exactly as the "Use demo house" button fills it."""
    from app.modules.intake.service import demo_input

    d = demo_input()
    form = {"street": d.street, "city": d.city, "zip": d.zip, "seller_name": d.seller_name,
            "seller_email": d.seller_email, "seller_phone": d.seller_phone, **d.facts}
    r = client.post("/intake", data=form, follow_redirects=False)
    assert r.status_code == 303, r.text


def listed(client: TestClient) -> None:
    """Step 1 done: intake, agency form acknowledged, listing accepted, listing agreement signed."""
    demo_intake(client)
    as_persona(client, "seller")
    client.post("/intake/agency", data={"decision": "acknowledge"})
    as_persona(client, "presenter")
    client.post("/intake/accept")
    as_persona(client, "seller")
    assert client.post("/intake/sign", data={"decision": "sign"}, follow_redirects=False).status_code == 303
    as_persona(client, "presenter")


def recommended_price() -> int:
    from app.modules.pricing import service as pricing
    from app.web import current_deal

    s = db.new_session()
    try:
        return pricing.current(s, current_deal(s)).advice["recommended_price"]
    finally:
        s.close()


def priced(client: TestClient, price: int | None = None) -> int:
    """Step 2 done: the AI advised, the seller chose (the recommended price unless one is given)."""
    listed(client)
    assert client.post("/pricing/recommend", follow_redirects=False).status_code == 303
    chosen = price or recommended_price()
    as_persona(client, "seller")
    r = client.post("/pricing/choose", data={"price": str(chosen)}, follow_redirects=False)
    assert r.status_code == 303, r.text
    as_persona(client, "presenter")
    return chosen


def drafted(client: TestClient) -> None:
    """Step 3 started: the AI wrote and checked all six pieces."""
    priced(client)
    assert client.post("/copy/draft", follow_redirects=False).status_code == 303
