"""PII as a first-class concern (spec section 6; SC "PII"): export and delete for any person, the access log.

- `export(s, person)`: every PII field, the person's disclosures, the documents they are a party to, the messages
  on their side, the client decisions they made and every access-log row about them, as one JSON document. The
  export itself is access-logged and an audit event.
- `erase(s, person)`: the PII fields are erased (the documents never stored names: they are put in at render time,
  so every document now renders "[erased]"); a tombstone keeps the non-personal transaction facts with "retained 3
  years (L17)"; the erase is an audit event. NY's three-year record-keeping rule (L17) and an erase request pull in
  different directions: the screen says so (a hurdle, reported), and the demonstration erases on request.
- Who may: the Presenter (the firm acting on a request) or the person themself (the seller for the seller, the
  buyer for the buyer). The seller never opens the buyer's record, nor the buyer the seller's (the information wall).
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit import log_access, record_event
from app.db import Base
from app.models import AccessLog, Checkpoint, Deal, Disclosure, Document, Message, Person, now
from app.pii import registry
from app.records.service import NotYourDecision
from app.web import NotFound

ERASED = "[erased]"
RETENTION = "Transaction facts retained 3 years (L17): the role, the deal's records and the documents' text, without names."
# Documents each role is a party to (names are put in at render time).
PARTY_DOCS = {"seller": {"listing_agreement", "accepted_offer_memorandum"},
              "buyer": {"buyer_agreement", "accepted_offer_memorandum"}}
FIELD_LABEL = {"legal_name": "Name", "email": "E-mail", "phone": "Phone", "mailing_address": "Mailing address",
               "preapproval_amount": "Pre-approval amount", "lender": "Lender"}


def pii_fields() -> list[tuple[str, str]]:
    return registry(Base)["person"]


def people(s: Session, deal: Deal | None) -> list[Person]:
    if deal is None:
        return []
    ids = [i for i in (deal.seller_id, deal.buyer_id) if i]
    return list(s.execute(select(Person).where(Person.id.in_(ids)).order_by(Person.id)).scalars())


def may_view(persona: str, person: Person) -> bool:
    return persona == "presenter" or persona == person.role


def require_view(persona: str, person: Person) -> None:
    if not may_view(persona, person):
        raise NotYourDecision(f"The {persona} cannot open the {person.role}'s personal data: only the firm (the "
                              f"Presenter) or the {person.role} may.")


def get(s: Session, deal: Deal | None, person_id: int) -> Person:
    p = s.get(Person, person_id)
    if p is None or deal is None or p.id not in (deal.seller_id, deal.buyer_id):
        raise NotFound("No such person in this deal.")
    return p


def values(p: Person) -> list[dict]:
    return [{"field": f, "label": FIELD_LABEL.get(f, f), "category": cat, "value": getattr(p, f)}
            for f, cat in pii_fields()]


def access_rows(s: Session, person_id: int | None = None, limit: int | None = None) -> list[AccessLog]:
    q = select(AccessLog).order_by(AccessLog.id.desc())
    if person_id is not None:
        q = q.where(AccessLog.person_id == person_id)
    if limit:
        q = q.limit(limit)
    return list(s.execute(q).scalars())


def view(s: Session, p: Person, persona: str, route: str) -> list[dict]:
    """The person's PII for the screen; the view is access-logged."""
    require_view(persona, p)
    shown = [v for v in values(p) if v["value"] not in (None, "", ERASED)]
    if shown:
        log_access(s, persona=persona, person_id=p.id, fields=[v["field"] for v in shown],
                   purpose="privacy: the person's own record", route=route)
    return values(p)


def export(s: Session, deal: Deal, p: Person, persona: str, route: str) -> dict:
    require_view(persona, p)
    fields = {v["field"]: v["value"] for v in values(p)}
    discl = s.execute(select(Disclosure).where(Disclosure.deal_id == deal.id, Disclosure.person_id == p.id)
                      .order_by(Disclosure.id)).scalars()
    docs = s.execute(select(Document).where(Document.deal_id == deal.id,
                                            Document.kind.in_(PARTY_DOCS.get(p.role, set())))
                     .order_by(Document.id)).scalars()
    msgs = s.execute(select(Message).where(Message.deal_id == deal.id, Message.side == p.role)
                     .order_by(Message.id)).scalars()
    decisions = s.execute(select(Checkpoint).where(Checkpoint.deal_id == deal.id,
                                                   Checkpoint.kind == "client_decision",
                                                   Checkpoint.decided_by == p.role).order_by(Checkpoint.id)).scalars()
    log_access(s, persona=persona, person_id=p.id, fields=list(fields), purpose="privacy: export on request",
               route=route)
    record_event(s, actor=persona, kind="system", entity="person", entity_id=p.id,
                 summary=f"Exported the {p.role}'s personal data ({p.token}) on request")
    return {
        "exported_at": now().isoformat(), "person": {"id": p.id, "role": p.role, "token": p.token,
                                                     "erased_at": p.erased_at.isoformat() if p.erased_at else None,
                                                     **fields},
        "disclosures": [{"title": d.title, "law": d.l_id, "delivered_at": _iso(d.delivered_at),
                         "acknowledged_at": _iso(d.acknowledged_at)} for d in discl],
        "documents": [{"kind": d.kind, "version": d.version, "created_at": _iso(d.created_at),
                       "signed_by": d.signed_by} for d in docs],
        "messages": [{"thread": m.thread, "direction": m.direction, "topic": m.topic, "status": m.status,
                      "body": m.body, "at": _iso(m.created_at)} for m in msgs],
        "decisions": [{"record": c.code, "title": c.title, "decision": c.decision, "at": _iso(c.decided_at)}
                      for c in decisions],
        "access_log": [{"at": _iso(a.ts), "viewed_by": a.persona, "fields": a.fields, "purpose": a.purpose,
                        "screen": a.route} for a in reversed(access_rows(s, p.id))],
    }


def erase(s: Session, p: Person, persona: str) -> Person:
    require_view(persona, p)
    if p.erased_at:
        return p
    for f, _ in pii_fields():
        setattr(p, f, ERASED if f in ("legal_name", "email", "phone", "mailing_address") else None)
    p.persona_label = f"Erased person ({p.role}); {RETENTION}"
    p.erased_at = now()
    s.flush()
    record_event(s, actor=persona, kind="system", entity="person", entity_id=p.id,
                 summary=f"Erased the {p.role}'s personal data ({p.token}) on request; tombstone kept: {RETENTION}")
    return p


def _iso(v) -> str | None:
    return v.isoformat() if v else None
