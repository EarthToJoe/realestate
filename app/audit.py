"""Append-only audit log (hash chain) and the PII access log."""

from __future__ import annotations

import hashlib
import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AccessLog, Event, now
from app.pii import MASKER

GENESIS = "0" * 64


def _ts(ts) -> str:
    # SQLite drops tzinfo on read, so hash the naive UTC form on both sides.
    return ts.replace(tzinfo=None).isoformat()


def _digest(prev: str, ts: str, actor: str, kind: str, entity: str, entity_id: str | None, summary: str) -> str:
    payload = json.dumps([prev, ts, actor, kind, entity, entity_id, summary], separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def record_event(s: Session, *, actor: str, kind: str, entity: str, entity_id, summary: str) -> Event:
    """Append one event. The summary is masked, so the audit log never holds PII."""
    last = s.execute(select(Event).order_by(Event.seq.desc()).limit(1)).scalar_one_or_none()
    prev = last.hash if last else GENESIS
    ts = now()
    summary = MASKER.mask(summary)
    eid = None if entity_id is None else str(entity_id)
    ev = Event(ts=ts, actor=actor, kind=kind, entity=entity, entity_id=eid, summary=summary, prev_hash=prev,
               hash=_digest(prev, _ts(ts), actor, kind, entity, eid, summary))
    s.add(ev)
    s.flush()
    return ev


def verify_chain(s: Session) -> bool:
    prev = GENESIS
    for ev in s.execute(select(Event).order_by(Event.seq)).scalars():
        expected = _digest(prev, _ts(ev.ts), ev.actor, ev.kind, ev.entity, ev.entity_id, ev.summary)
        if ev.prev_hash != prev or ev.hash != expected:
            return False
        prev = ev.hash
    return True


def log_access(s: Session, *, persona: str, person_id: int, fields: list[str], purpose: str, route: str) -> None:
    s.add(AccessLog(persona=persona, person_id=person_id, fields=fields, purpose=purpose, route=route))
    s.flush()
