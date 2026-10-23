"""Step 9 Deal timeline (SC9): built only from checkpoint records, the step table and, for the dates on the road to
closing, the signed contract's agreed terms. No model call.

- `rows`: one per step in walk order, with its records; each record a chip in its colour.
- `counts`: the header: AI acts, client decisions, "NY law today" markers (licensed broker, lawyer), steps for a
  person and planned third-party steps.
- `road`: the planned records from the signed contract to closing (app/records/road.py), dated once signed.
- `hurdles`: every "NY law today" marker and "a person does this" record, grouped by step and code, with how often.
- `acts`: the agent-acts log: every act the AI did where NY law today requires a licensed person or a lawyer, in
  order, which is what a supervising broker would review (F75).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models import Checkpoint, Deal
from app.records import catalogue
from app.records import service as records
from app.records.road import BY_KEY
from app.web import steps

KIND_ORDER = {"automated": 0, "client_decision": 1, "law_marker": 2, "human_required": 3, "third_party": 4}


@dataclass
class StepRow:
    n: int
    shown: int
    title: str
    built: bool
    records: list[Checkpoint] = field(default_factory=list)


@dataclass
class RoadItem:
    record: Checkpoint
    what: str
    who: str
    when: date | None


@dataclass
class Hurdle:
    record: Checkpoint  # the newest record of this code on this step
    times: int


@dataclass
class Timeline:
    standing: list[Checkpoint]
    rows: list[StepRow]
    counts: dict
    hurdles: list[tuple[StepRow, list[Hurdle]]]
    road: list[RoadItem]
    signed_on: date | None
    acts: list[tuple[StepRow, Checkpoint]]


def _signed(s: Session, deal: Deal) -> tuple[date | None, dict | None]:
    cp = records.latest(s, deal.id, "CP-33")
    if not (cp and cp.status == "done" and cp.decided_at):
        return None, None
    from app.modules.offers import service as offers

    return cp.decided_at.date(), offers.state(deal).get("accepted")


def _road(s: Session, deal: Deal, planned: list[Checkpoint]) -> tuple[list[RoadItem], date | None]:
    signed_on, terms = _signed(s, deal)
    out = []
    for r in planned:
        key = (r.attached_to or "").removeprefix("closing:")
        if key not in BY_KEY:
            continue
        _, _, what, who, days, rel = BY_KEY[key]
        when = None
        if signed_on:
            if days is not None:
                when = signed_on + timedelta(days=days)
            elif terms and terms.get(rel[0]) is not None:
                when = signed_on + timedelta(days=int(terms[rel[0]]) + rel[1])
        out.append(RoadItem(record=r, what=what, who=who, when=when))
    order = {k: i for i, k in enumerate(BY_KEY)}
    out.sort(key=lambda x: (x.when or date.max, order[(x.record.attached_to or "").removeprefix("closing:")]))
    return out, signed_on


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
        rows.append(StepRow(n=st["n"], shown=st["shown"], title=st["title"], built=st["built"], records=rs))
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
        "planned_markers": sum(1 for r in all_records if r.kind == "law_marker" and r.status == "planned"),
        "automated": sum(1 for r in acted if r.kind == "automated"),
        "records": len(all_records),
        "codes": len({r.code for r in all_records}),
    }
    hurdles = []
    for row in rows:
        hs = [r for r in row.records if r.kind in ("law_marker", "human_required")]
        if row.n == 9:
            hs = standing + hs
        grouped: dict[str, Hurdle] = {}
        for r in hs:
            h = grouped.get(r.code)
            grouped[r.code] = Hurdle(record=r, times=(h.times + 1) if h else 1)
        if grouped:
            hurdles.append((row, list(grouped.values())))
    by_n = {row.n: row for row in rows}
    acts = [(by_n[r.step], r) for r in sorted(markers, key=lambda r: r.id)
            if not catalogue.get(r.code).standing and r.step in by_n]
    planned = [r for r in all_records if r.status == "planned" and (r.attached_to or "").startswith("closing:")]
    road, signed_on = _road(s, deal, planned)
    return Timeline(standing=standing, rows=rows, counts=counts, hurdles=hurdles, road=road, signed_on=signed_on,
                    acts=acts)
