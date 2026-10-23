"""docs/DEMO-SCRIPT.md is generated from steps.yaml and must match it; every screen of the path is served, its
visitor's line (`explain`) is on it, and its presenter notes carry the script's words only when presenting."""

import importlib.util

from markupsafe import escape

from app.config import ROOT
from app.web import stops


def _gen():
    spec = importlib.util.spec_from_file_location("gen", ROOT / "scripts" / "gen-demo-script.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_demo_script_matches_steps():
    mod = _gen()
    assert mod.OUT.read_text() == mod.generate(), "run: python3 scripts/gen-demo-script.py"


def test_every_screen_is_served_with_its_line_and_notes_only_when_presenting(client):
    from tests.conftest import demo_intake

    demo_intake(client)
    for sc in stops():
        r = client.get(sc["route"])
        assert r.status_code == 200, sc["route"]
        assert str(escape(sc["explain"].strip())) in r.text, sc["route"]
        assert 'id="presenter-notes"' not in r.text, sc["route"]
    client.cookies.set("presenting", "on")
    for sc in stops():
        r = client.get(sc["route"])
        assert 'id="presenter-notes"' in r.text and str(escape(sc["say"])) in r.text, sc["route"]
