from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app import db
from app.config import Settings
from app.main import create_app
from app.model.provider import FakeProvider


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
