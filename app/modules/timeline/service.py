"""The finale (decision 51): the whole sale, start to finish, built only from checkpoint records, the path's steps,
the change events and, for the dates on the road to closing, the signed contract's agreed terms. No model call.

- `rows`: one per step of the path (1 to 11), with its records, superseded ones included as history (a change);
  `firm`: the records of "one more thing" (the firm's own campaign), after the sale.
- `counts`: the header: AI acts, client decisions, "NY law today" markers (licensed broker, lawyer), steps for a
  person and planned third-party steps. Standing records only: a superseded record no longer counts.
- `road`: the planned records from the signed contract to closing (app/records/road.py), dated once signed.
- `hurdles`: every "NY law today" marker and "a person does this" record, grouped by step and code, with how often.
- `acts`: the agent-acts log: every act the AI did where NY law today requires a licensed person or a lawyer, in
  order, which is what a supervising broker would review (F75).
- `changes`: every change a client made ("Change", decision 48), oldest first, from the audit log.
- `story`: four plain lines saying how far the sale got.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Checkpoint, Deal, Event
from app.records import catalogue
from app.records import service as records
from app.records.road import BY_KEY
from app.web import steps

KIND_ORDER = {"automated": 0, "client_decision": 1, "law_marker": 2, "human_required": 3, "third_party": 4}


@dataclass
class StepRow:
    n: int | str
    shown: int | str
    title: str
    route: str = ""
    records: list[Checkpoint] = field(default_factory=list)  # standing and superseded, in order

    @property
    def standing(self) -> list[Checkpoint]:
        return [r for r in self.records if r.status != "superseded"]

    @property
    def built(self) -> bool:  # kept for older templates and tests
        return True


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
    firm: StepRow
    counts: dict
    hurdles: list[tuple[StepRow, list[Hurdle]]]
    road: list[RoadItem]
    signed_on: date | None
    acts: list[tuple[StepRow, Checkpoint]]
    changes: list[Event]
    story: list[tuple[str, bool]]  # (line, done)
    finished: bool


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


def _story(s: Session, deal: Deal) -> tuple[list[tuple[str, bool]], bool]:
    """What the visitor just saw, in four lines, each honest to how far the sale got."""
    from app.demo import walk

    done = walk.done_map(s, deal)
    from app.modules.offers import service as offers

    price = deal.list_price
    acc = offers.state(deal).get("accepted")
    lines = []
    if done["listing"]:
        lines.append(("The seller signed up and hired the firm: the AI researched the house, sent the notices the "
                      "law requires and took the listing.", True))
    else:
        lines.append(("The seller signed up; hiring the firm (step 3) is not finished yet.", False))
    if done["seller_answers"] and done["mls"]:
        lines.append((f"The AI priced the house{f' (the seller listed it at ${price:,})' if price else ''}, wrote "
                      "and checked the listing, put it on the market and answered every enquiry.", True))
    elif done["price"]:
        lines.append((f"The AI priced the house and the seller listed it at ${price:,}; marketing and the enquiries "
                      "(steps 5 to 7) are not finished yet.", False))
    else:
        lines.append(("Pricing, the listing and the enquiries (steps 4 to 7) have not happened yet.", False))
    if acc:
        lines.append((f"A buyer joined the firm and made an offer; the two AIs negotiated, inside the seller's limits, "
                      f"to ${acc['final_price']:,}.", True))
    elif done["offer"]:
        lines.append(("A buyer joined the firm and made an offer; the seller's decision and the negotiation "
                      "(step 10) are not finished yet.", False))
    else:
        lines.append(("The buyer's side (steps 8 to 10) has not happened yet.", False))
    if done["signed"]:
        lines.append(("The AI drafted the contract of sale, the seller completed the state's disclosure form, and "
                      "the seller and the buyer both signed (simulated).", True))
    elif done["contract"]:
        lines.append(("The AI drafted the contract; the disclosure form and the signatures (step 11) are not "
                      "finished yet.", False))
    else:
        lines.append(("The contract (step 11) has not been drafted yet.", False))
    return lines, all(ok for _, ok in lines)


def build(s: Session, deal: Deal) -> Timeline:
    from app.demo.path import step_of_record

    history = records.records(s, deal.id, history=True)
    standing_all = [r for r in history if r.status != "superseded"]
    standing = [r for r in standing_all if catalogue.get(r.code).standing]
    rows = [StepRow(n=st["n"], shown=st["n"], title=st["title"], route=st["route"]) for st in steps()]
    by_n = {row.n: row for row in rows}
    firm = StepRow(n="firm", shown="+", title="One more thing: how the firm finds sellers", route="/brand")
    for r in history:
        if catalogue.get(r.code).standing or r.kind == "third_party" or (r.status == "planned"
                                                                         and r.kind == "law_marker"):
            continue  # the standing marker and the road to closing have their own sections
        where = step_of_record(r)
        row = firm if where == "firm" else by_n.get(where)
        if row is not None:
            row.records.append(r)
    for row in rows + [firm]:
        row.records.sort(key=lambda r: r.id)
    acted = [r for r in standing_all if r.status != "planned"]
    markers = [r for r in acted if r.kind == "law_marker"]
    counts = {
        "markers": len(markers),
        "markers_L": sum(1 for r in markers if r.law_actor in ("L", "L+A")),
        "markers_A": sum(1 for r in markers if r.law_actor in ("A", "L+A")),
        "decisions_done": sum(1 for r in acted if r.kind == "client_decision" and r.status == "done"),
        "decisions_pending": sum(1 for r in acted if r.kind == "client_decision" and r.status == "pending"),
        "decisions_played": sum(1 for r in acted if r.kind == "client_decision" and r.played),
        "human_required": sum(1 for r in acted if r.kind == "human_required"),
        "third_party": sum(1 for r in standing_all if r.kind == "third_party"),
        "planned_markers": sum(1 for r in standing_all if r.kind == "law_marker" and r.status == "planned"),
        "automated": sum(1 for r in acted if r.kind == "automated"),
        "records": len(standing_all),
        "codes": len({r.code for r in standing_all}),
        "superseded": sum(1 for r in history if r.status == "superseded"),
    }
    hurdles = []
    planned_markers = [r for r in standing_all if r.kind == "law_marker" and r.status == "planned"]
    for row in rows + [firm]:
        hs = [r for r in row.standing if r.kind in ("law_marker", "human_required")]
        if row.n == 11:  # the contract's step carries the standing marker and the planned repairs marker
            hs = standing + planned_markers + hs
        grouped: dict[str, Hurdle] = {}
        for r in hs:
            h = grouped.get(r.code)
            grouped[r.code] = Hurdle(record=r, times=(h.times + 1) if h else 1)
        if grouped:
            hurdles.append((row, list(grouped.values())))
    acts = []
    for r in sorted(markers, key=lambda r: r.id):
        if catalogue.get(r.code).standing:
            continue
        where = step_of_record(r)
        row = firm if where == "firm" else by_n.get(where)
        if row is not None:
            acts.append((row, r))
    planned = [r for r in standing_all if r.status == "planned" and (r.attached_to or "").startswith("closing:")]
    road, signed_on = _road(s, deal, planned)
    changes = list(s.execute(select(Event).where(Event.kind == "change").order_by(Event.seq)).scalars())
    story, finished = _story(s, deal)
    return Timeline(standing=standing, rows=rows, firm=firm, counts=counts, hurdles=hurdles, road=road,
                    signed_on=signed_on, acts=acts, changes=changes, story=story, finished=finished)
