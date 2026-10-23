"""Shared web plumbing: templates, the persona switcher, the common page context."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.brokerage import brokerage
from app.models import Checkpoint, Deal, ModelCall
from app.records import catalogue

APP_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))

PERSONAS = {"presenter": "Presenter", "seller": "Seller", "buyer": "Buyer"}
COOKIE = "persona"


def persona(request: Request) -> str:
    p = request.cookies.get(COOKIE, "presenter")
    return p if p in PERSONAS else "presenter"


@lru_cache(maxsize=1)
def steps() -> list[dict]:
    return yaml.safe_load((APP_DIR / "demo" / "steps.yaml").read_text())["steps"]


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
    if deal:
        for cp in s.execute(select(Checkpoint).where(Checkpoint.deal_id == deal.id)).scalars():
            if cp.kind == "law_marker" and cp.status == "done" and not catalogue.get(cp.code).standing:
                marker_counts[cp.step] = marker_counts.get(cp.step, 0) + 1
            if cp.status in ("done", "simulated") and cp.kind != "third_party":
                done_steps.add(cp.step)
    spend = s.execute(select(func.coalesce(func.sum(ModelCall.cost_usd), 0.0))
                      .where(ModelCall.mode == "live")).scalar_one()
    settings = request.app.state.settings
    base = {
        "request": request, "persona": persona(request), "personas": PERSONAS, "steps": steps(),
        "active_step": step, "screen": screen, "deal": deal, "marker_counts": marker_counts,
        "done_steps": done_steps, "firm": brokerage(), "cp35": catalogue.get("CP-35"),
        "model_mode": request.app.state.provider.mode, "live_spend": float(spend),
        "spend_cap": settings.spend_cap_usd, "review_url": settings.review_url,
        "kind_label": catalogue.KIND_LABEL, "law_actor_label": catalogue.LAW_ACTOR_LABEL,
        "launch_routes": {c: (e.launch_route, e.launch_link) for c, e in catalogue.load().items() if e.launch_route},
    }
    base.update(ctx)
    return templates.TemplateResponse(request, template, base, status_code=status_code)
