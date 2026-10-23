"""With a DB_KEY secret the database file is encrypted (T2), and the app still works on it."""

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.model.provider import FakeProvider
from tests.conftest import demo_intake


def test_app_on_encrypted_database(tmp_path):
    secrets = tmp_path / "secrets"
    secrets.mkdir()
    (secrets / "DB_KEY").write_text("test-db-key-123")
    s = Settings(data_dir=tmp_path / "data", secrets_dir=secrets, review_dir=tmp_path / "none", model_mode="fake")
    assert s.db_url.startswith("sqlite+pysqlcipher")
    c = TestClient(create_app(s, FakeProvider()))
    demo_intake(c)
    assert c.get("/timeline").status_code == 200
    raw = (tmp_path / "data" / "realestate.db").read_bytes()
    assert not raw.startswith(b"SQLite format 3") and b"146 Route 292" not in raw
