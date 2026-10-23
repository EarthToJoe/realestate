"""Shared web plumbing: templates, the persona switcher, the common page context."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import humanize
from app.brokerage import brokerage
from app.models import Checkpoint, Deal, ModelCall
from app.records import catalogue

APP_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))
# Display helpers (UI audit 2026-10-23): Eastern times, Yes/No, money, decisions in words, one plain sentence per
# law marker. Records keep their stored values; only the screen changes.
templates.env.filters.update(et=humanize.et, yesno=humanize.yesno, slot=humanize.slot,
                             money=lambda v: f"${int(v):,}" if v not in (None, "") else "")
templates.env.globals.update(decision_label=humanize.decision_label, whose=humanize.whose,
                             authority_label=humanize.AUTHORITY_LABELS, authority_value=humanize.authority_value,
                             plain_of=lambda code: catalogue.get(code).plain)

class NotFound(LookupError):
    """A record the request names is not in this deal (shown as a plain 404 page)."""


PERSONAS = {"presenter": "Presenter", "seller": "Seller", "buyer": "Buyer"}
COOKIE = "persona"
GUIDE_COOKIE = "guide"  # "on" while the guided demo runs (Start demo turns it on; "End the guided demo" off)


def persona(request: Request) -> str:
    p = request.cookies.get(COOKIE, "presenter")
    return p if p in PERSONAS else "presenter"


@lru_cache(maxsize=1)
def steps() -> list[dict]:
    """The steps in the order the demo walks them (the order of steps.yaml). `n` is the step's number in the success
    criteria, used by records, routes and tests; `shown` is the number on screen, its place in the walk (Q47), so a
    presenter never says "now step 8, then step 6". Each screen also gets its place in the whole walk (`k`)."""
    out = yaml.safe_load((APP_DIR / "demo" / "steps.yaml").read_text())["steps"]
    k = 0
    for i, st in enumerate(out, 1):
        st["shown"] = i
        for sc in st["screens"]:
            k += 1
            sc["k"] = k
    return out


@lru_cache(maxsize=1)
def intro() -> dict:
    """The introduction's presenter notes (before step 1)."""
    return yaml.safe_load((APP_DIR / "demo" / "steps.yaml").read_text())["intro"]


def screens() -> list[tuple[dict, dict]]:
    """Every (step, screen) in walk order."""
    return [(st, sc) for st in steps() for sc in st["screens"]]


def shown(n: int) -> int:
    """The on-screen number of the step whose success-criteria number is n."""
    return next((st["shown"] for st in steps() if st["n"] == n), n)


def screen_for(route: str) -> tuple[dict | None, dict | None]:
    for st in steps():
        for sc in st["screens"]:
            if sc["route"] == route:
                return st, sc
    return None, None


def current_deal(s: Session) -> Deal | None:
    return s.execute(select(Deal).order_by(Deal.id.desc()).limit(1)).scalar_one_or_none()


def render(request: Request, s: Session, template: str, status_code: int = 200, **ctx):
    deal = ctx.get("deal") or current_deal(s)
    step, screen = screen_for(request.url.path)
    marker_counts: dict[int, int] = {}
    done_steps: set[int] = set()
    waiting_steps: set[int] = set()
    if deal:
        for cp in s.execute(select(Checkpoint).where(Checkpoint.deal_id == deal.id)).scalars():
            if cp.kind == "law_marker" and cp.status == "done" and not catalogue.get(cp.code).standing:
                marker_counts[cp.step] = marker_counts.get(cp.step, 0) + 1
            if cp.status in ("done", "simulated") and cp.kind != "third_party":
                done_steps.add(cp.step)
            if cp.kind == "client_decision" and cp.status == "pending":
                waiting_steps.add(cp.step)
    spend = s.execute(select(func.coalesce(func.sum(ModelCall.cost_usd), 0.0))
                      .where(ModelCall.mode == "live")).scalar_one()
    settings = request.app.state.settings
    base = {
        "request": request, "persona": persona(request), "personas": PERSONAS, "steps": steps(),
        "active_step": step, "screen": screen, "deal": deal, "marker_counts": marker_counts,
        "done_steps": done_steps, "waiting_steps": waiting_steps,
        "firm": brokerage(), "cp35": catalogue.get("CP-35"),
        "model_mode": request.app.state.provider.mode, "live_spend": float(spend),
        "spend_cap": settings.spend_cap_usd, "review_url": settings.review_url,
        "kind_label": catalogue.KIND_LABEL, "law_actor_label": catalogue.LAW_ACTOR_LABEL,
        "launch_routes": {c: (e.launch_route, e.launch_link) for c, e in catalogue.load().items() if e.launch_route},
    }
    # Where this screen sits in the walk, for the step bar, the presenter's box and the guided demo (SC11).
    flat = screens()
    i = next((j for j, (_, sc) in enumerate(flat) if screen and sc["route"] == screen["route"]), -1)
    base.update(walk_screens=flat, here=i, prev_screen=flat[i - 1] if i > 0 else None,
                next_screen=flat[i + 1] if 0 <= i < len(flat) - 1 else (flat[0] if i < 0 else None),
                guide=request.cookies.get(GUIDE_COOKIE) == "on")
    if "walk_gate" not in ctx or "ff_steps" not in ctx:
        from app.demo import walk

        base["walk_gate"] = walk.gate_for(s, deal, request.url.path, ctx.get("gate"))
        base["ff_steps"] = walk.fast_forward_steps(s, deal) if base["persona"] == "presenter" else set()
        base["playable"] = (walk.playable(s, deal, screen["route"])
                            if screen and base["persona"] == "presenter" else [])
    base.update(ctx)
    return templates.TemplateResponse(request, template, base, status_code=status_code)


templates.env.globals.update(shown=shown)


def gate_page(request: Request, s: Session):
    """A step screen with nothing to show yet (no deal, or no buyer): its own page with the gate card, never a
    redirect (a presenter clicking a step link must always land where they clicked)."""
    return render(request, s, "gate.html")
