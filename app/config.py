"""Runtime settings, all from the environment, with defaults that work for a local run.

Secrets are read from files at runtime (never baked into the image, the repo or a log):
  REALESTATE_SECRETS_DIR/ANTHROPIC_API_KEY   model key (absent = replay mode)
  REALESTATE_SECRETS_DIR/PII_KEY             Fernet key for PII columns (absent locally = generated in the data dir)
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _path(name: str, default: str | Path) -> Path:
    return Path(os.environ.get(name, str(default)))


@dataclass
class Settings:
    data_dir: Path = field(default_factory=lambda: _path("REALESTATE_DATA_DIR", ROOT / "tmp" / "data"))
    secrets_dir: Path = field(default_factory=lambda: _path("REALESTATE_SECRETS_DIR", "/srv/realestate/secrets"))
    review_dir: Path = field(
        default_factory=lambda: _path("REALESTATE_REVIEW_DIR", "/srv/hughesnode/apps/realestate/public")
    )
    review_url: str = field(default_factory=lambda: os.environ.get("REALESTATE_REVIEW_URL", "/index.html"))
    # live | replay | fake. "auto" = live if a key is readable, otherwise replay.
    model_mode: str = field(default_factory=lambda: os.environ.get("REALESTATE_MODEL_MODE", "auto"))
    spend_cap_usd: float = field(default_factory=lambda: float(os.environ.get("SPEND_CAP_USD", "12")))
    database_url: str | None = field(default_factory=lambda: os.environ.get("REALESTATE_DATABASE_URL"))
    log_file: Path | None = field(
        default_factory=lambda: Path(p) if (p := os.environ.get("REALESTATE_LOG_FILE")) else None
    )

    def __post_init__(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)

    @property
    def db_url(self) -> str:
        return self.database_url or f"sqlite:///{self.data_dir / 'realestate.db'}"

    def secret(self, name: str) -> str | None:
        p = self.secrets_dir / name
        try:
            value = p.read_text().strip()
        except (FileNotFoundError, PermissionError, NotADirectoryError):
            return None
        return value or None

    def resolved_model_mode(self) -> str:
        if self.model_mode != "auto":
            return self.model_mode
        return "live" if self.secret("ANTHROPIC_API_KEY") else "replay"
