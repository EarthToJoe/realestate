"""PII baseline for slice 1: encrypted columns, registry, masked logs, model-context whitelist, access log, T6."""

import json
import sqlite3

from app import pii
from app.db import Base
from app.models import AccessLog, Person
from app.modules.intake.service import load_personas
from tests.conftest import demo_intake

SELLER = load_personas()["seller"]


def test_registry_lists_person_pii():
    reg = pii.registry(Base)
    assert {c for c, _ in reg["person"]} >= {"legal_name", "email", "phone", "mailing_address"}
    assert "property" not in reg  # no owner name, ever


def test_pii_encrypted_at_rest(client, settings):
    demo_intake(client)
    raw = sqlite3.connect(settings.data_dir / "realestate.db").execute(
        "select legal_name, email, phone from person").fetchone()
    assert SELLER["legal_name"] not in raw[0] and SELLER["email"] not in raw[1] and "555" not in raw[2]


def test_no_pii_in_logs_or_audit(client, settings, session):
    demo_intake(client)
    client.post("/intake/infer")
    client.post("/intake/accept")
    client.get("/intake/onboarding")
    from app.logging_setup import log

    log.info("probe", note=f"contact {SELLER['email']} or {SELLER['phone']} for {SELLER['legal_name']}",
             legal_name=SELLER["legal_name"])
    text = settings.log_file.read_text()
    assert "probe" in text
    for value in (SELLER["legal_name"], SELLER["email"], SELLER["phone"]):
        assert value not in text
    from app.models import Event

    summaries = " ".join(e.summary for e in session.query(Event).all())
    assert SELLER["legal_name"] not in summaries


def test_model_request_carries_no_pii(client, provider):
    demo_intake(client)
    client.post("/intake/infer")
    assert provider.requests, "the intake step made no model call"
    body = json.dumps(provider.requests)
    for value in (SELLER["legal_name"], SELLER["email"], SELLER["phone"], "Okafor", "dana"):
        assert value.lower() not in body.lower()


def test_access_log_on_pii_render(client, session):
    demo_intake(client)
    client.post("/intake/accept")
    r = client.get("/intake/onboarding")
    assert SELLER["legal_name"] in r.text  # shown to the user on the agreement...
    rows = session.query(AccessLog).all()
    assert rows and rows[-1].fields == ["legal_name"] and rows[-1].route == "/intake/onboarding"


def test_t6_tokenize_roundtrip_keeps_pii_out_of_the_request(client, provider, session):
    """T6: mask a buyer message, call the model, re-insert the real values only in the rendered output."""
    from pydantic import BaseModel

    class Reply(BaseModel):
        reply: str
        tokens_seen: list[str]

    message = ("Hi, this is Sam Whitfield-Arora (sam.wa@example.com, 914-555-0187). "
               "Sam would like to see the house Saturday.")
    masked, mapping = pii.tokenize(message, {"BUYER_1": {"name": "Sam Whitfield-Arora",
                                                         "email": "sam.wa@example.com", "phone": "914-555-0187"}})
    assert "Sam" not in masked and "example.com" not in masked and "555" not in masked
    out = provider.generate("probe.mask_roundtrip", Reply, {"message": masked}, s=session, module="probe",
                            system="Reply briefly.", prompt_version="t6")
    sent = json.dumps(provider.requests[-1])
    assert "Whitfield" not in sent and "sam.wa" not in sent and "0187" not in sent
    assert pii.detokenize(out.output.reply, mapping).startswith("Hello Sam Whitfield-Arora")


def test_masker_patterns():
    m = pii.Masker()
    m.register("Dana Okafor-Reyes", "[SELLER_1]")
    assert m.mask("Dana Okafor-Reyes, dana@x.org, (845) 555-0142") == "[SELLER_1], [EMAIL], [PHONE]"
    assert m.mask("Built 1995; 2,520 sq ft; $591,200") == "Built 1995; 2,520 sq ft; $591,200"


def test_person_values_round_trip(session, client):
    demo_intake(client)
    p = session.query(Person).one()
    assert p.legal_name == SELLER["legal_name"]
