"""docs/DEMO-SCRIPT.md is generated from steps.yaml and must match it; every built route has a screen, with its
presenter notes (hidden behind the "Presenter notes" button) carrying the script's words."""

import importlib.util

from markupsafe import escape

from app.config import ROOT
from app.web import steps


def _gen():
    spec = importlib.util.spec_from_file_location("gen", ROOT / "scripts" / "gen-demo-script.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_demo_script_matches_steps():
    mod = _gen()
    assert mod.OUT.read_text() == mod.generate(), "run: python3 scripts/gen-demo-script.py"


def test_every_step_route_is_served(client):
    from tests.conftest import demo_intake

    demo_intake(client)
    for st in steps():
        for sc in st["screens"]:
            r = client.get(sc["route"])
            assert r.status_code == 200, sc["route"]
            assert 'id="presenter-notes"' in r.text and str(escape(sc["say"])) in r.text, sc["route"]
