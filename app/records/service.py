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

import contextvars

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

# Set while the demo plays a decision for a client (fast-forward, "Do this screen for me"): the record says so, on its
# card and on the timeline ("played by the demo"), so nobody mistakes a scripted consent for a person's (audit F18).
PLAYED: contextvars.ContextVar[bool] = contextvars.ContextVar("played", default=False)
# Statuses that no longer count: a record superseded by a change (decision 48) stays on the timeline as history.
GONE = ("superseded",)


def _new(s: Session, deal_id: int, code: str, *, status: str, reason: str | None = None,
         attached_to: str | None = None, step: int | None = None) -> Checkpoint:
    """`step` overrides the catalogue's step for a per-item record written on another step (a CP-24 notice sent
    to the buyer belongs to step 8, a CP-26 pass on the firm's campaign to step 10), so the timeline puts it there."""
    e = catalogue.get(code)
    cp = Checkpoint(
        deal_id=deal_id, code=code, step=step or e.step, kind=e.kind, title=e.title, actor=e.actor,
        law_actor=e.law_actor, side=e.side, rule_text=e.rule, who_text=e.who, reason=reason,
        f_ids=list(e.f_ids), l_ids=list(e.l_ids), ws3_ids=list(e.ws3_ids), research_link=e.link,
        blocking=e.blocking, status=status, attached_to=attached_to,
    )
    s.add(cp)
    s.flush()
    return cp


def records(s: Session, deal_id: int, code: str | None = None, *, history: bool = False) -> list[Checkpoint]:
    """The deal's records (of one code), oldest first. Superseded records are left out unless `history` is asked
    for: the timeline shows them as changes; everything else reads only what stands."""
    q = select(Checkpoint).where(Checkpoint.deal_id == deal_id)
    if code:
        q = q.where(Checkpoint.code == code)
    if not history:
        q = q.where(Checkpoint.status.not_in(GONE))
    return list(s.execute(q.order_by(Checkpoint.id)).scalars())


def latest(s: Session, deal_id: int, code: str) -> Checkpoint | None:
    rs = records(s, deal_id, code)
    return rs[-1] if rs else None


def supersede(s: Session, deal_id: int, code: str, *, why: str, where=None) -> list[Checkpoint]:
    """A change (decision 48): the records of `code` that stand (optionally only those `where(cp)` picks) are marked
    superseded, never deleted, so the timeline keeps the history. Planned and standing records are left alone."""
    out = []
    for cp in records(s, deal_id, code):
        if cp.status == "planned" or catalogue.get(code).standing or (where and not where(cp)):
            continue
        cp.status = "superseded"
        out.append(cp)
    if out:
        s.flush()
        record_event(s, actor="system", kind="change", entity="checkpoint", entity_id=out[-1].id,
                     summary=f"{code} superseded ({len(out)} record{'s' if len(out) > 1 else ''}): {why}")
    return out


def reopen(s: Session, deal_id: int, code: str, *, why: str, attached_to: str | None = None,
           where=None) -> Checkpoint:
    """A client decision made again: the standing record is superseded and a new pending one opens."""
    old = [cp for cp in records(s, deal_id, code) if not where or where(cp)]
    attached_to = attached_to or (old[-1].attached_to if old else None)
    supersede(s, deal_id, code, why=why, where=where)
    cp = _new(s, deal_id, code, status="pending", reason=f"Re-opened: {why}", attached_to=attached_to)
    record_event(s, actor="system", kind="change", entity="checkpoint", entity_id=cp.id,
                 summary=f"{code} re-opened for the {catalogue.get(code).actor.replace('_', ' ')}: {why}")
    return cp


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
            f"{checkpoint.code} is {e.who.lower()}'s decision; the {persona} cannot make it."
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
    checkpoint.played = bool(checkpoint.played) or PLAYED.get()
    if reason:
        checkpoint.reason = reason
    s.flush()
    record_event(s, actor=persona, kind="client_decision", entity="checkpoint", entity_id=checkpoint.id,
                 summary=f"{checkpoint.code} {decision} by the {persona}"
                         f"{' (played by the demo)' if PLAYED.get() else ''}: {checkpoint.title}")
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
            raise GateError(code, f"Cannot {action}: {code} ({e.title}) is {state}. It is "
                                  f"{e.who.lower()}'s decision. Why: {e.rule}")


def mark_law(s: Session, deal_id: int, code: str, *, reason: str, attached_to: str | None = None,
             step: int | None = None) -> Checkpoint:
    """Record an agent act the AI did where NY law today requires a licensed person or a lawyer. Never blocks."""
    e = catalogue.get(code)
    if e.kind != "law_marker":
        raise ValueError(f"{code} is a {e.kind}, not a law marker")
    if not e.per_item and not e.standing:
        existing = latest(s, deal_id, code)
        if existing and existing.status == "done":
            return existing
    cp = _new(s, deal_id, code, status="planned" if e.planned else "done", reason=reason, attached_to=attached_to,
              step=step)
    record_event(s, actor="ai", kind="ai_action", entity="checkpoint", entity_id=cp.id,
                 summary=f"{code} AI act (NY law today: {e.law_actor}): {reason}")
    return cp


def record_auto(s: Session, deal_id: int, code: str, *, reason: str, attached_to: str | None = None,
                step: int | None = None) -> Checkpoint:
    e = catalogue.get(code)
    if e.kind != "automated":
        raise ValueError(f"{code} is a {e.kind}, not automated")
    cp = _new(s, deal_id, code, status="done", reason=reason, attached_to=attached_to, step=step)
    record_event(s, actor="ai", kind="ai_action", entity="checkpoint", entity_id=cp.id, summary=f"{code} {reason}")
    return cp


def record_human(s: Session, deal_id: int, code: str, *, reason: str, simulated: bool = True,
                 step: int | None = None) -> Checkpoint:
    e = catalogue.get(code)
    if e.kind != "human_required":
        raise ValueError(f"{code} is a {e.kind}, not human required")
    cp = _new(s, deal_id, code, status="simulated" if simulated else "done", reason=reason, step=step)
    record_event(s, actor="presenter", kind="system", entity="checkpoint", entity_id=cp.id,
                 summary=f"{code} human-required step recorded (simulated): {reason}")
    return cp


def plan(s: Session, deal_id: int, code: str, *, reason: str | None = None,
         attached_to: str | None = None) -> Checkpoint:
    """A planned record (third-party steps, planned markers, the standing CP-35 marker). A per-item code is planned
    once per item (`attached_to`, e.g. "closing:mortgage"), any other code once."""
    e = catalogue.get(code)
    for existing in records(s, deal_id, code):
        if not (e.per_item and attached_to) or existing.attached_to == attached_to:
            return existing
    status = "done" if e.standing else "planned"
    reason = reason or ("Standing: shown in the identity block on every page" if e.standing
                        else "Planned: shown on the timeline, not acted in the demo")
    cp = _new(s, deal_id, code, status=status, reason=reason, attached_to=attached_to)
    return cp
