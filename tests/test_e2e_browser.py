"""The one-button walk in headless Chromium (SC "Tests"; BUILD-PATH acceptance 1): scripts/e2e-demo.py --quick, the
phone walk on recorded replays with no key, pressing only each screen's primary button from Start to the finale.
Skipped where Playwright's Chromium is not installed."""

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
def test_the_one_button_walk_runs_end_to_end_on_replays_in_a_browser():
    spec = importlib.util.spec_from_file_location("e2e", ROOT / "scripts" / "e2e-demo.py")
    e2e = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(e2e)
    res = e2e.run(widths=(e2e.PHONE,), shots=False, full=False)
    assert not res.problems, res.problems
    w = res.walks["phone"]
    assert w["screens"][-1] == "/timeline" and w["clicks"] <= 30, w
