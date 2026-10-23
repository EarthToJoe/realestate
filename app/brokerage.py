"""The one brokerage's identity (config/brokerage.yaml), shown on every page and message (L10, decision 25)."""

from __future__ import annotations

from functools import lru_cache

import yaml

from app.config import ROOT


@lru_cache(maxsize=1)
def _load() -> dict:
    return yaml.safe_load((ROOT / "config" / "brokerage.yaml").read_text())


def brokerage(brokerage_id: str = "default") -> dict:
    return _load()[brokerage_id]


def identity_block(brokerage_id: str = "default") -> str:
    b = brokerage(brokerage_id)
    return f"{b['name']} ({b['name_note']}) · {b['office_address']} · {b['phone']} · {b['broker_of_record']}"
