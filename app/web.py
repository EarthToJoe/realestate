"""Shared web plumbing: templates, the persona, the path (app/demo/steps.yaml), the common page context and the
one-line confirmation after an action (decisions 47 to 51)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from urllib.parse import quote, unquote

import yaml
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import humanize
from app.brokerage import brokerage
from app.models import Deal, ModelCall
from app.records import catalogue

APP_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))
# Display helpers (UI audit 2026-10-23): Eastern times, Yes/No, money, decisions in words, one plain sentence per
# law marker. Records keep their stored values; only the screen changes.
templates.env.filters.update(et=humanize.et, yesno=humanize.yesno, slot=humanize.slot, plain=humanize.plain,
                             money=lambda v: f"${int(v):,}" if v not in (None, "") else "")
templates.env.globals.update(decision_label=humanize.decision_label, whose=humanize.whose,
                             authority_label=humanize.AUTHORITY_LABELS, authority_value=humanize.authority_value,
                             plain_of=lambda code: catalogue.get(code).plain)


class NotFound(LookupError):
    """A record the request names is not in this deal (shown as a plain 404 page)."""


# The persona is kept for the access log and "People and their data" (decision 49); it no longer gates a client's
# decision button, which records the decision as the client the button names. "View as" lives in the menu.
PERSONAS = {"presenter": "The firm (sees both sides)", "seller": "The seller", "buyer": "The buyer"}
COOKIE = "persona"
PRESENTING_COOKIE = "presenting"  # "on": the presenter's tools (decision 50); remembered on the device
FLASH_COOKIE = "flash"  # the one-line confirmation after an action, shown once (decision 47)
YEAR = 60 * 60 * 24 * 365


def persona(request: Request) -> str:
    p = request.cookies.get(COOKIE, "presenter")
    return p if p in PERSONAS else "presenter"


def presenting(request: Request) -> bool:
    return request.cookies.get(PRESENTING_COOKIE) == "on"


def actor(request: Request, form=None) -> str:
    """Whose decision a button records: the client its label names (`as`), else the persona (decision 49). The
    record service still refuses a decision for the wrong client, and the AI never records one."""
    named = str((form or {}).get("as") or "") if form is not None else ""
    return named or persona(request)


@lru_cache(maxsize=1)
def _path() -> dict:
    return yaml.safe_load((APP_DIR / "demo" / "steps.yaml").read_text())


def steps() -> list[dict]:
    """The eleven steps of the sale, in order (decision 51). `n` is the step's place on the path; `shown` is the
    same number (kept for the templates and the demo script)."""
    out = _path()["steps"]
    for st in out:
        st["shown"] = st["n"]
        st.setdefault("short", st["title"])
    return out


def finale() -> dict:
    return {**_path()["finale"], "n": None, "short": "The whole sale"}


def after() -> dict:
    return {**_path()["after"], "n": None}


def stops() -> list[dict]:
    """Every screen of the path in order: the eleven steps, the finale, then "one more thing"."""
    return steps() + [finale(), after()]


def intro() -> dict:
    """The introduction's presenter notes (before step 1)."""
    return _path()["intro"]


def merged_routes() -> dict[str, tuple[str, str]]:
    """Old screens and where they now live (route, anchor), so saved links and the review pages still land."""
    return {m["route"]: (st["route"], m["anchor"]) for st in stops() for m in st.get("merged", [])}


def screen_for(route: str) -> tuple[dict | None, dict | None]:
    """The stop a route belongs to, as (step, screen): both the same dict now that a step is one screen."""
    route = merged_routes().get(route, (route, None))[0]
    st = next((x for x in stops() if x["route"] == route), None)
    return st, st


def shown(n: int) -> int:
    return n


def current_deal(s: Session) -> Deal | None:
    return s.execute(select(Deal).order_by(Deal.id.desc()).limit(1)).scalar_one_or_none()


def redirect(url: str, flash: str | None = None) -> RedirectResponse:
    """Post/Redirect/Get after every action (fresh-eyes audit 5), with the one-line confirmation for the next page."""
    resp = RedirectResponse(url, status_code=303)
    if flash:
        resp.set_cookie(FLASH_COOKIE, quote(flash[:600]), httponly=True, samesite="lax")
    return resp


def render(request: Request, s: Session, template: str, status_code: int = 200, **ctx):
    from app.demo import path

    deal = ctx.get("deal") or current_deal(s)
    stop, _ = screen_for(request.url.path)
    spend = s.execute(select(func.coalesce(func.sum(ModelCall.cost_usd), 0.0))
                      .where(ModelCall.mode == "live")).scalar_one()
    settings = request.app.state.settings
    is_presenting = presenting(request)
    flash = unquote(request.cookies.get(FLASH_COOKIE, "")) or None
    base = {
        "request": request, "persona": persona(request), "personas": PERSONAS, "steps": steps(),
        "stops": stops(), "finale": finale(), "after": after(), "active_step": stop, "screen": stop, "deal": deal,
        "firm": brokerage(), "cp35": catalogue.get("CP-35"), "presenting": is_presenting, "flash": flash,
        "model_mode": request.app.state.provider.mode, "live_spend": float(spend),
        "spend_cap": settings.spend_cap_usd, "review_url": settings.review_url,
        "kind_label": catalogue.KIND_LABEL, "law_actor_label": catalogue.LAW_ACTOR_LABEL,
        "launch_routes": {c: (e.launch_route, e.launch_link) for c, e in catalogue.load().items() if e.launch_route},
        "recorded": request.app.state.provider.mode == "replay",
    }
    base.update(path.page_context(s, deal, stop, request, ctx.get("gate")))
    base.update(ctx)
    resp = templates.TemplateResponse(request, template, base, status_code=status_code)
    # The page always shows what is saved now: the browser's Back and a refresh fetch it again (decision 48).
    resp.headers["Cache-Control"] = "no-store"
    if flash:
        resp.delete_cookie(FLASH_COOKIE)
    return resp


templates.env.globals.update(shown=shown)


def gate_page(request: Request, s: Session):
    """A step screen with nothing to show yet: its own page with the "not yet" card, never a redirect (a step link
    always lands where it was clicked)."""
    return render(request, s, "gate.html")
