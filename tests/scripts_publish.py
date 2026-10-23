"""Test helper: the page names scripts/publish_review.py writes (so marker links are checked, not assumed)."""

from __future__ import annotations

import importlib.util
import sys
import types

from app.config import ROOT


def review_slugs() -> set[str]:
    sys.modules.setdefault("markdown", types.ModuleType("markdown"))  # only its slug() is used here
    spec = importlib.util.spec_from_file_location("publish_review", ROOT / "scripts" / "publish_review.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    paths = [p for _, items in mod.SECTIONS for p, _, _ in items]
    return {mod.slug(p) for p in paths if (ROOT / p).exists()} | {"index.html"}
