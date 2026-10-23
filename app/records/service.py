"""Writes records from the catalogue and enforces client-decision gates on the server.

- `open_decision` creates a pending client decision (blocking).
- `decide` records the client's choice; only the client whose decision it is may make it (the persona check is
  here, server-side, so no crafted request can decide for someone else).
- `require` refuses an action until the named decisions are done, saying why (`GateError`).
- `mark_law` writes a red "NY law today" record for an agent act the AI just did. Markers never gate anything.
- `record_auto`, `record_human`, `plan` write the other kinds.
Every write also appends an audit event.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit import record_event
from app.models import Checkpoint, now
from app.records import catalogue


class GateError(Exception):
    """An action was refused because a client decision is not made yet (or was declined)."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


class NotYourDecision(Exception):
    """A persona tried to make a decision that belongs to someone else."""


# Which personas may decide for which actor value in the catalogue.
DECIDERS = {"seller": {"seller"}, "buyer": {"buyer"}, "seller_and_buyer": {"seller", "buyer"}}


def _new(s: Session, deal_id: int, code: str, *, status: str, reason: str | None = None,
         attached_to: str | None = None) -> Checkpoint:
    e = catalogue.get(code)
    cp = Checkpoint(
        deal_id=deal_id, code=code, step=e.step, kind=e.kind, title=e.title, actor=e.actor,
        law_actor=e.law_actor, side=e.side, rule_text=e.rule, who_text=e.who, reason=reason,
        f_ids=list(e.f_ids), l_ids=list(e.l_ids), ws3_ids=list(e.ws3_ids), research_link=e.link,
        blocking=e.blocking, status=status, attached_to=attached_to,
    )
    s.add(cp)
    s.flush()
    return cp


def records(s: Session, deal_id: int, code: str | None = None) -> list[Checkpoint]:
    q = select(Checkpoint).where(Checkpoint.deal_id == deal_id)
    if code:
        q = q.where(Checkpoint.code == code)
    return list(s.execute(q.order_by(Checkpoint.id)).scalars())


def latest(s: Session, deal_id: int, code: str) -> Checkpoint | None:
    rs = records(s, deal_id, code)
    return rs[-1] if rs else None


def open_decision(s: Session, deal_id: int, code: str, *, reason: str | None = None,
                  attached_to: str | None = None) -> Checkpoint:
    e = catalogue.get(code)
    if e.kind != "client_decision":
        raise ValueError(f"{code} is a {e.kind}, not a client decision")
    existing = latest(s, deal_id, code)
    if existing and existing.status == "pending" and not e.per_item:
        return existing
    cp = _new(s, deal_id, code, status="pending", reason=reason, attached_to=attached_to)
    record_event(s, actor="system", kind="system", entity="checkpoint", entity_id=cp.id,
                 summary=f"{code} waiting for the {e.actor.replace('_', ' ')}: {e.title}")
    return cp


def decide(s: Session, checkpoint: Checkpoint, *, persona: str, decision: str, reason: str | None = None
           ) -> Checkpoint:
    e = catalogue.get(checkpoint.code)
    if checkpoint.kind != "client_decision":
        raise ValueError(f"{checkpoint.code} is not a client decision")
    if persona not in DECIDERS.get(e.actor, set()):
        raise NotYourDecision(
            f"{checkpoint.code} is the {e.who.lower()}'s decision; the {persona} cannot make it."
        )
    if e.choices and decision not in e.choices:
        raise ValueError(f"{checkpoint.code}: '{decision}' is not one of {list(e.choices)}")
    if checkpoint.status not in ("pending",):
        raise ValueError(f"{checkpoint.code} is already {checkpoint.status}")
    declined = decision in ("decline", "reject")
    if e.actor == "seller_and_buyer":
        # Both parties must decide; keep each party's choice until both are in.
        parts = dict(item.split("=") for item in (checkpoint.decision or "").split(",") if "=" in item)
        parts[persona] = decision
        checkpoint.decision = ",".join(f"{k}={v}" for k, v in sorted(parts.items()))
        if declined:
            checkpoint.status = "declined"
        elif {"seller", "buyer"} <= set(parts):
            checkpoint.status = "done"
    else:
        checkpoint.decision = decision
        checkpoint.status = "declined" if declined else "done"
    checkpoint.decided_by = persona
    checkpoint.decided_at = now()
    if reason:
        checkpoint.reason = reason
    s.flush()
    record_event(s, actor=persona, kind="client_decision", entity="checkpoint", entity_id=checkpoint.id,
                 summary=f"{checkpoint.code} {decision} by the {persona}: {checkpoint.title}")
    return checkpoint


def is_done(s: Session, deal_id: int, code: str) -> bool:
    cp = latest(s, deal_id, code)
    return bool(cp and cp.status == "done")


def require(s: Session, deal_id: int, *codes: str, action: str) -> None:
    """Refuse `action` unless every listed client decision is done."""
    for code in codes:
        cp = latest(s, deal_id, code)
        e = catalogue.get(code)
        if cp is None or cp.status != "done":
            state = "declined" if cp and cp.status == "declined" else "not made yet"
            raise GateError(code, f"Cannot {action}: {code} ({e.title}) is {state}. It is the "
                                  f"{e.who.lower()}'s decision. Why: {e.rule}")


def mark_law(s: Session, deal_id: int, code: str, *, reason: str, attached_to: str | None = None) -> Checkpoint:
    """Record an agent act the AI did where NY law today requires a licensed person or a lawyer. Never blocks."""
    e = catalogue.get(code)
    if e.kind != "law_marker":
        raise ValueError(f"{code} is a {e.kind}, not a law marker")
    if not e.per_item and not e.standing:
        existing = latest(s, deal_id, code)
        if existing and existing.status == "done":
            return existing
    cp = _new(s, deal_id, code, status="planned" if e.planned else "done", reason=reason, attached_to=attached_to)
    record_event(s, actor="ai", kind="ai_action", entity="checkpoint", entity_id=cp.id,
                 summary=f"{code} AI act (NY law today: {e.law_actor}): {reason}")
    return cp


def record_auto(s: Session, deal_id: int, code: str, *, reason: str, attached_to: str | None = None) -> Checkpoint:
    e = catalogue.get(code)
    if e.kind != "automated":
        raise ValueError(f"{code} is a {e.kind}, not automated")
    cp = _new(s, deal_id, code, status="done", reason=reason, attached_to=attached_to)
    record_event(s, actor="ai", kind="ai_action", entity="checkpoint", entity_id=cp.id, summary=f"{code} {reason}")
    return cp


def record_human(s: Session, deal_id: int, code: str, *, reason: str, simulated: bool = True) -> Checkpoint:
    e = catalogue.get(code)
    if e.kind != "human_required":
        raise ValueError(f"{code} is a {e.kind}, not human required")
    cp = _new(s, deal_id, code, status="simulated" if simulated else "done", reason=reason)
    record_event(s, actor="presenter", kind="system", entity="checkpoint", entity_id=cp.id,
                 summary=f"{code} human-required step recorded (simulated): {reason}")
    return cp


def plan(s: Session, deal_id: int, code: str) -> Checkpoint:
    """A planned record (third-party steps, planned markers, the standing CP-35 marker)."""
    existing = latest(s, deal_id, code)
    if existing:
        return existing
    e = catalogue.get(code)
    status = "done" if e.standing else "planned"
    reason = ("Standing: shown in the identity block on every page" if e.standing
              else "Planned: shown on the timeline, not acted in the demo")
    cp = _new(s, deal_id, code, status=status, reason=reason)
    return cp
