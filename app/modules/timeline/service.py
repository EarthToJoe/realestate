"""Step 9 Deal timeline: built only from checkpoint records and the step table. No model call."""

from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from app.models import Checkpoint, Deal
from app.records import catalogue
from app.records import service as records
from app.web import steps

KIND_ORDER = {"automated": 0, "client_decision": 1, "law_marker": 2, "human_required": 3, "third_party": 4}


@dataclass
class StepRow:
    n: int
    title: str
    built: bool
    records: list[Checkpoint] = field(default_factory=list)


@dataclass
class Timeline:
    standing: list[Checkpoint]
    rows: list[StepRow]
    counts: dict
    hurdles: list[tuple[StepRow, list[Checkpoint]]]


def build(s: Session, deal: Deal) -> Timeline:
    all_records = records.records(s, deal.id)
    standing = [r for r in all_records if catalogue.get(r.code).standing]
    by_step: dict[int, list[Checkpoint]] = {}
    for r in all_records:
        if r in standing:
            continue
        by_step.setdefault(r.step, []).append(r)
    rows = []
    for st in steps():
        rs = sorted(by_step.get(st["n"], []), key=lambda r: (r.status == "planned", r.id))
        rows.append(StepRow(n=st["n"], title=st["title"], built=st["built"], records=rs))
    acted = [r for r in all_records if r.status != "planned"]
    markers = [r for r in acted if r.kind == "law_marker"]
    counts = {
        "markers": len(markers),
        "markers_L": sum(1 for r in markers if r.law_actor in ("L", "L+A")),
        "markers_A": sum(1 for r in markers if r.law_actor in ("A", "L+A")),
        "decisions_done": sum(1 for r in acted if r.kind == "client_decision" and r.status == "done"),
        "decisions_pending": sum(1 for r in acted if r.kind == "client_decision" and r.status == "pending"),
        "human_required": sum(1 for r in acted if r.kind == "human_required"),
        "third_party": sum(1 for r in all_records if r.kind == "third_party"),
        "automated": sum(1 for r in acted if r.kind == "automated"),
        "records": len(all_records),
        "codes": len({r.code for r in all_records}),
    }
    hurdles = []
    for row in rows:
        hs = [r for r in row.records if r.kind in ("law_marker", "human_required")]
        if row.n == 9:
            hs = standing + hs
        if hs:
            hurdles.append((row, hs))
    return Timeline(standing=standing, rows=rows, counts=counts, hurdles=hurdles)
