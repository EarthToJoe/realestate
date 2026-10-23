"""The full Property Condition Disclosure Statement (CP-04, L43): the 7/1/25 form, 56 questions, version-pinned;
only the seller completes it; nothing is pre-filled; "if yes" parts and explanations are checked."""

import re

from app.disclosures import pcds
from app.records import service as records
from app.web import current_deal
from tests.conftest import as_persona, demo_intake


def test_form_is_the_full_2025_form():
    f = pcds.form()
    assert f["version"] == "2025-07-01" and "A9330" in f["source"]
    ns = [q["n"] for q in pcds.questions()]
    assert ns == list(range(1, 57))
    q36 = next(q for q in pcds.questions() if q["n"] == 36)
    assert "septic system operation and maintenance" in q36["note"]  # the 2025 amendment
    q27 = next(q for q in pcds.questions() if q["n"] == 27)
    assert q27["type"] == "ynu"  # the statute gives question 27 no NA box


def test_every_field_starts_blank(client):
    from tests.flows import agreed_b
    agreed_b(client)
    r = client.get("/disclosures/pcds")  # now part of the contract step (decision 51)
    assert r.url.path == "/contract" and r.text.count('class="pcds-q"') == 56
    form = r.text.split('id="pcds-form"')[1].split("</form>")[0]
    assert " checked" not in form
    found = re.findall(r'<input class="input" name="(q[0-9_a-z]+)" value="([^"]*)"', form)
    assert found
    for name, value in found:
        assert value == "", f"{name} must start blank"


def test_prepared_answers_validate():
    assert pcds.validate(pcds.prepared_answers()) == []


def test_only_the_seller_submits_and_explanations_are_required(client, session):
    demo_intake(client)
    answers = pcds.prepared_answers()
    as_persona(client, "presenter")
    assert client.post("/disclosures/pcds", data=answers).status_code == 403
    assert client.post("/disclosures/pcds/prepared").status_code == 403
    as_persona(client, "seller")
    r = client.post("/disclosures/pcds", data={**answers, "q35_explain": ""})
    assert r.status_code == 422 and "Question 35" in r.text and 'id="pcds-error"' in r.text
    r = client.post("/disclosures/pcds", data={**answers, "q21_leaking": ""})
    assert r.status_code == 422 and "Question 21" in r.text
    # "if municipal" is not asked of a well
    assert pcds.validate({**answers, "q34_metered": ""}) == []
    assert client.post("/disclosures/pcds", data=answers, follow_redirects=False).status_code == 303
    session.expire_all()
    deal = current_deal(session)
    assert records.is_done(session, deal.id, "CP-04")
    saved = pcds.answers_of(session, deal)
    assert saved["_form_version"] == "2025-07-01" and saved["q36_type"] == "Septic"
    r = client.get("/disclosures/pcds/print")
    assert 'id="pcds-body"' in r.text


def test_prepared_answers_are_labelled_fiction(client, session):
    demo_intake(client)
    as_persona(client, "seller")
    assert client.post("/disclosures/pcds/prepared", follow_redirects=False).status_code == 303
    r = client.get("/disclosures/pcds/print")
    assert "DEMONSTRATION" in r.text and "not statements about the real house" in r.text
    assert "Pawling Central School District" in r.text
