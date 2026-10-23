"""Slice 3 acceptance, SC7: Step 7 Contract. Memorandum (CP-32); the AI's draft and rider in the product's own
step with the CP-14 marker stating the law and naming the launch route; code checks (deal numbers, L23, decision
26); the side-by-side against the long form's 28 paragraphs; the PCDS attached and signing refused until the seller
completes it (L43); the signing map with the wet-ink and notary items (CP-15); simulated signing by both (CP-33);
PDF and DOCX with the label on every page; no attorney screen or persona anywhere."""

import html
import io
import json
import re
import shutil
import subprocess
import zipfile

import pytest

from app.modules.contract import service as contract
from app.records import service as records
from app.web import current_deal
from tests.conftest import as_persona
from tests.flows import agreed_b

PLAN_LINK = "https://realestate.hughesnode.com/docs-plan.html#the-contract-route-what-new-york-allows-today"


def drafted(client):
    agreed_b(client)
    assert client.post("/contract/draft", follow_redirects=False).status_code == 303


def seller_pcds(client):
    as_persona(client, "seller")
    assert client.post("/disclosures/pcds/prepared", follow_redirects=False).status_code == 303
    as_persona(client, "presenter")


def test_contract_waits_for_an_agreed_offer(client):
    from tests.flows import offers_advised
    offers_advised(client)
    r = client.get("/contract")
    assert 'id="gate-card"' in r.text and 'data-missing=' in r.text


def test_memorandum_draft_and_cp14_marker_with_launch_route(client, session, provider):
    drafted(client)
    deal = current_deal(session)
    r = client.get("/contract")
    assert "sent to both parties first (simulated)" in r.text and "$620,000" in r.text
    assert any("memorandum" in (c.reason or "") for c in records.records(session, deal.id, "CP-32"))
    block = r.text[r.text.index('id="rec-CP-14"'):]
    block = html.unescape(block[:block.index('id="pcds"')])
    assert "NY law today: only a lawyer may draft a contract of sale for another" in block
    assert "Judiciary Law" in block and "decision 26" in block
    assert 'id="launch-CP-14"' in block and "the firm's paper, subject to each party's attorney's approval" in block
    assert f'href="{PLAN_LINK}"' in block
    for i in ("F52", "L21", "L22", "L25"):
        assert f">{i}<" in block
    assert records.latest(session, deal.id, "CP-14").status == "done"
    assert 'data-passed="yes"' in r.text and contract.LABEL.replace(" (L21, L22)", "") in r.text
    req = next(x for x in provider.requests if x["task"] == "contract.draft")
    body = json.dumps(req)
    for leak in ("Dana", "Okafor", "Whitfield", "example.com", "555-01", "maximum_price", "665000", "lowest_price",
                 "price_floor", "Relocating"):
        assert leak not in body, leak
    assert "[SELLER_1]" in body and "[BUYER_1]" in body


def test_side_by_side_covers_all_28_paragraphs(client):
    drafted(client)
    r = client.get("/contract")
    assert len(re.findall(r'<tr data-n="\d+">', r.text)) == 28
    assert "Downpayment in Escrow" in r.text and "Mortgage Commitment Contingency" in r.text


def test_code_checks_block_a_draft_that_says_no_lawyer_is_needed(client, session, provider):
    from app.model import fakes

    def bad(ctx):
        out = fakes.default("contract.draft", ctx)
        out["notes_to_parties"] = ["You don't need a lawyer for this contract."]
        out["rider"].append({"number": "R9", "heading": "Approval",
                             "text": "This contract is subject to the approval of each party's attorney."})
        return out
    provider.responders["contract.draft"] = bad
    drafted(client)
    st = contract.state(current_deal(session))
    rules = {f["rule"]: f["tier"] for f in st["findings"]}
    assert rules["L23"] == "block" and rules["decision-26"] == "warn" and not st["passed"]
    seller_pcds(client)
    r = client.post("/contract/open-signing")
    assert r.status_code == 422 and "block finding" in r.text


def test_code_checks_block_wrong_numbers(client, session, provider):
    from app.model import fakes

    def wrong(ctx):
        out = fakes.default("contract.draft", ctx)
        out["sections"][2]["text"] = "The purchase price is $999,000."
        return out
    provider.responders["contract.draft"] = wrong
    drafted(client)
    st = contract.state(current_deal(session))
    assert any(f["rule"] == "deal-price" and f["tier"] == "block" for f in st["findings"])


def test_signing_refused_until_the_seller_completes_the_pcds(client, session):
    drafted(client)
    r = client.get("/contract")
    assert 'id="rec-CP-04"' in r.text and 'id="pcds-open"' in r.text and 'id="pcds-form"' in r.text
    r = client.post("/contract/open-signing")
    assert r.status_code == 409 and "Disclosure Statement" in r.text
    assert "CP-04" not in r.text.split('id="refused"')[1][:600]  # plain words on the audience layer
    assert records.latest(session, current_deal(session).id, "CP-33") is None
    seller_pcds(client)
    assert client.post("/contract/open-signing", follow_redirects=False).status_code == 303
    deal = current_deal(session)
    session.expire_all()
    assert records.latest(session, deal.id, "CP-33").status == "pending"
    assert records.latest(session, deal.id, "CP-15").status == "planned"
    assert any("Property Condition" in (c.reason or "") for c in records.records(session, deal.id, "CP-32"))


def test_both_parties_sign_and_only_they_can(client, session):
    drafted(client)
    seller_pcds(client)
    client.post("/contract/open-signing")
    assert client.post("/contract/sign", data={"decision": "sign"}).status_code == 403  # the presenter
    for p in ("seller", "buyer"):
        as_persona(client, p)
        assert client.post("/contract/sign", data={"decision": "sign"}, follow_redirects=False).status_code == 303
    deal = current_deal(session)
    session.expire_all()
    assert records.latest(session, deal.id, "CP-33").status == "done" and deal.status == "under_contract"
    r = client.get("/contract")
    assert 'id="signed"' in r.text and 'id="rec-CP-15"' in r.text and "wet ink, acknowledged before a notary" in r.text


def test_pdf_has_the_label_on_every_page_and_the_pcds_attached(client, tmp_path):
    drafted(client)
    seller_pcds(client)
    r = client.get("/contract/draft.pdf")
    assert r.status_code == 200 and r.content[:4] == b"%PDF"
    html = client.get("/contract/print").text
    assert "Sam Whitfield-Arora" in html and "Dana Okafor-Reyes" in html and "Property Condition Disclosure" in html
    if not shutil.which("pdftotext"):
        pytest.skip("pdftotext not installed")
    f = tmp_path / "c.pdf"
    f.write_bytes(r.content)
    text = subprocess.run(["pdftotext", str(f), "-"], capture_output=True, text=True, check=True).stdout
    pages = [p for p in text.split("\f") if p.strip()]
    assert len(pages) >= 3
    assert all("DEMONSTRATION. Drafted by software for the parties" in p for p in pages)


def test_docx_has_the_label_in_header_and_footer(client):
    drafted(client)
    r = client.get("/contract/draft.docx")
    assert r.status_code == 200
    z = zipfile.ZipFile(io.BytesIO(r.content))
    headers = [n for n in z.namelist() if re.match(r"word/(header|footer)\d*\.xml", n)]
    assert headers
    for n in headers:
        assert "DEMONSTRATION. Drafted by software for the parties" in z.read(n).decode()
    doc = z.read("word/document.xml").decode()
    assert "Rider" in doc and "Side by side" in doc and "$620,000" in doc


def test_no_attorney_screen_or_persona_anywhere(client):
    from app.web import PERSONAS
    assert set(PERSONAS) == {"presenter", "seller", "buyer"}
    from app.main import create_app
    paths = [getattr(r, "path", "") for r in client.app.routes]
    assert not [p for p in paths if "attorney" in p or "lawyer" in p]
    _ = create_app


def test_documents_without_a_sale_or_a_draft_never_error(client):
    """The print view, PDF and Word copy: the "not yet" card, never a server error (site audit)."""
    for url in ("/contract/print", "/contract/draft.pdf", "/contract/draft.docx", "/disclosures/pcds/print"):
        r = client.get(url)
        assert r.status_code == 200 and 'id="gate-card"' in r.text, url
    from tests.conftest import demo_intake
    demo_intake(client)
    for url in ("/contract/print", "/contract/draft.pdf", "/contract/draft.docx"):
        r = client.get(url)
        assert r.status_code == 200 and 'id="gate-card"' in r.text and 'id="flash"' in r.text, url


def test_each_pdf_version_is_built_once():
    from app.modules.contract import documents

    html_doc = "<html><body><p>DEMONSTRATION cache test</p></body></html>"
    first = documents.contract_pdf(html_doc)
    assert documents.cached(html_doc) and documents.contract_pdf(html_doc) is first
    documents.warm(html_doc)  # already built: nothing to do


def test_the_disclosure_form_lives_on_the_contract_step(client):
    r = client.get("/disclosures/pcds", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"] == "/contract#pcds"
