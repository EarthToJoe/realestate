"""The end-to-end run of the demo in headless Chromium (SC "Tests"): scripts/e2e-demo.py --quick, the guided demo at
phone width on recorded replays with no key. Skipped where Playwright's Chromium is not installed."""

import importlib.util

import pytest

from app.config import ROOT

playwright = pytest.importorskip("playwright.sync_api")


def _chromium_ok() -> bool:
    try:
        with playwright.sync_playwright() as p:
            p.chromium.launch().close()
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _chromium_ok(), reason="Playwright's Chromium is not installed")
def test_the_guided_demo_runs_end_to_end_on_replays_in_a_browser():
    spec = importlib.util.spec_from_file_location("e2e", ROOT / "scripts" / "e2e-demo.py")
    e2e = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(e2e)
    res = e2e.run(widths=e2e.WIDTHS[:1], shots=False)
    assert not res["problems"], res["problems"]
    assert [t["route"] for t in res["widths"]["phone"]["screens"]] == [w[2]["route"] for w in res["walk"]]
