"""Slice 2 acceptance, SC3: listing copy drafted and checked, only passing copy marked ready by the AI, CP-06 per
piece, MLS pre-check, the flyer PDF with the DEMONSTRATION mark on every page."""

import json
import re
import shutil
import subprocess

import pytest

from app.modules.listing_copy import service as copy_service
from app.records import service as records
from app.web import current_deal
from tests.conftest import drafted


def test_ai_writes_six_pieces_and_checks_each(client, session):
    drafted(client)
    deal = current_deal(session)
    arts = copy_service.artifacts(session, deal)
    assert [a.channel for a in arts] == ["mls_remarks", "portal", "social_1", "social_2", "social_3", "flyer"]
    assert all(a.status in ("passed", "blocked") for a in arts)
    r = client.get("/copy")
    assert r.status_code == 200 and r.text.count('class="copy-artifact"') == 6
    # the demo devices are the presenter's tools, not the product (decision 50)
    assert "Plant a violation" not in r.text and "pass record" not in r.text
    client.cookies.set("presenting", "on")
    assert "Plant a violation" in client.get("/copy").text
    client.cookies.delete("presenting")
    # the fake portal copy says "master bedroom": a warn, rewritten by the AI, still a pass
    portal = next(a for a in arts if a.channel == "portal")
    assert portal.status == "passed" and 'data-rule="FH-SEX-02"' in r.text and "rewritten" in r.text
    assert len(records.records(session, deal.id, "CP-26")) == 6
    # every button on the screen has words (fresh-eyes audit 22)
    assert not re.search(r"<button[^>]*>\s*</button>", r.text)


def test_ready_all_marks_only_passing_copy_and_writes_cp06(client, session):
    drafted(client)
    deal = current_deal(session)
    portal = next(a for a in copy_service.artifacts(session, deal) if a.channel == "portal")
    assert client.post(f"/copy/{portal.id}/plant", follow_redirects=False).status_code == 303
    r = client.post("/copy/ready-all", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/copy"  # Post/Redirect/Get
    r = client.get(r.headers["location"])
    assert "not portal description" in r.text  # the confirmation names what was not marked
    session.expire_all()
    arts = copy_service.artifacts(session, deal)
    assert {a.channel for a in arts if a.status == "ready"} == {"mls_remarks", "social_1", "social_2", "social_3", "flyer"}
    cp06 = records.records(session, deal.id, "CP-06")
    assert len(cp06) == 5 and all(c.kind == "law_marker" and c.law_actor == "L" for c in cp06)
    assert r.text.count('id="rec-CP-06"') == 1 and "recorded 5 times" in r.text
    block = r.text[r.text.index('id="rec-CP-06"'):]
    assert "A licensed real estate broker" in block and ">L10<" in block
    # one honest headline: how many are ready and what is left
    assert "5 of them are ready to publish" in r.text and 'id="copy-left"' in r.text


def test_refresh_after_an_action_lands_on_the_screen(client):
    """A refresh or Back after "mark copy ready" never shows Method Not Allowed (fresh-eyes audit 5)."""
    drafted(client)
    client.post("/copy/ready-all")
    r = client.get("/copy/ready-all")
    assert r.status_code == 200 and r.url.path == "/copy" and "Method Not Allowed" not in r.text


def test_recheck_keeps_passing_copy_ready(client, session):
    """Re-checking unchanged copy keeps "ready to publish" (fresh-eyes audit 9)."""
    drafted(client)
    client.post("/copy/ready-all")
    deal = current_deal(session)
    remarks = next(a for a in copy_service.artifacts(session, deal) if a.channel == "mls_remarks")
    r = client.post(f"/copy/{remarks.id}/check")
    assert "stays ready to publish" in r.text
    session.expire_all()
    assert remarks.status == "ready"


def test_mls_precheck_rules():
    bad = ("Call the listing agent at (845) 555-0100 for the lockbox code. Free home warranty; 2.5% commission "
           "to the buyer's agent.")
    checks = {c["check"]: c["status"] for c in copy_service.remarks_checks(bad)}
    assert list(checks.values()).count("fail") == 4
    good = {c["status"] for c in copy_service.remarks_checks("Raised ranch on 4.18 acres; free-standing shed.")}
    assert good == {"ok"}


def test_mls_package_page(client, session):
    drafted(client)
    client.post("/copy/ready-all")
    r = client.get("/copy/mls")  # merged into step 5: the old address lands on its section
    assert r.status_code == 200 and r.url.path == "/copy"
    assert 'id="mls"' in r.text and 'id="mls-checks"' in r.text and 'id="mls-package"' in r.text
    # one headline: the checks pass, and what the package still waits for is named
    assert "needs attention" not in r.text and "The remarks pass all 6 checks" in r.text
    for field in ("ListPrice", "ParcelNumber", "PublicRemarks", "Photos"):
        assert f'data-field="{field}"' in r.text


def test_flyer_pdf_has_the_demonstration_mark_on_every_page(client, tmp_path):
    drafted(client)
    html = client.get("/copy/flyer").text
    assert "DEMONSTRATION: not a listing" in html and "@top-center" in html
    r = client.get("/copy/flyer.pdf")
    assert r.status_code == 200 and r.content[:4] == b"%PDF"
    if not shutil.which("pdftotext"):
        pytest.skip("pdftotext not installed")
    f = tmp_path / "flyer.pdf"
    f.write_bytes(r.content)
    text = subprocess.run(["pdftotext", str(f), "-"], capture_output=True, text=True, check=True).stdout
    pages = [p for p in text.split("\f") if p.strip()]
    assert pages and all("DEMONSTRATION" in p for p in pages)


def test_copy_model_context_has_no_pii_or_confidential(client, provider):
    drafted(client)
    for req in provider.requests:
        if req["task"] in ("copy.draft", "fairhousing.review"):
            body = json.dumps(req)
            for leak in ("Dana", "Okafor", "dana.or@example.com", "555-0142", "price_floor", "Relocating"):
                assert leak not in body, (req["task"], leak)
