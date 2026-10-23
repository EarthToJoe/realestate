"""FastAPI app: the POC screens at /, the review pages (static, written by scripts/publish-review.sh) at their
old addresses (/index.html, /docs-*.html, ...). No login of its own: Traefik's house login is in front.

Run: uvicorn --factory app.main:create_app  (make run)"""

from __future__ import annotations

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app import db, logging_setup, pii
from app.db import get_session
from app.config import Settings
from app.logging_setup import log
from app.model.provider import ModelProvider, make_provider
from app.records.service import GateError, NotYourDecision
from app.web import APP_DIR, COOKIE, PERSONAS, render


def _register_people() -> None:
    """After a restart, teach the log masker the people already in the database."""
    from app.models import Person

    s = db.new_session()
    try:
        for p in s.query(Person).all():
            for value, label in ((p.legal_name, f"[{p.token}]"), (p.email, "[EMAIL]"), (p.phone, "[PHONE]"),
                                 (p.mailing_address, "[ADDRESS]")):
                pii.MASKER.register(value, label)
    finally:
        s.close()


def create_app(settings: Settings | None = None, provider: ModelProvider | None = None) -> FastAPI:
    settings = settings or Settings()
    logging_setup.configure(settings.log_file)
    pii.configure_key(settings.secret("PII_KEY"), settings.data_dir)
    db.init_engine(settings.db_url)
    db.create_all()
    from app.db import Base

    logging_setup.set_pii_keys({col for cols in pii.registry(Base).values() for col, _ in cols})
    _register_people()

    app = FastAPI(title="realestate POC", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.settings = settings
    app.state.provider = provider or make_provider(settings)
    app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")

    from app.modules.intake.routes import router as intake_router
    from app.modules.timeline.routes import router as timeline_router
    from app.modules.pricing.routes import router as pricing_router
    from app.modules.listing_copy.routes import router as copy_router
    from app.modules.channels.routes import router as channels_router
    from app.modules.inbox.routes import router as inbox_router
    from app.modules.offers.routes import router as offers_router
    from app.fairhousing.check import FairHousingBlocked

    for r in (intake_router, pricing_router, copy_router, channels_router, inbox_router, offers_router,
              timeline_router):
        app.include_router(r)

    @app.exception_handler(FairHousingBlocked)
    async def fh_blocked(request: Request, exc: FairHousingBlocked):
        s = db.new_session()
        try:
            return render(request, s, "refused.html", status_code=409,
                          title="Refused: the fair-housing check has not passed", message=str(exc), code=None)
        finally:
            s.close()

    @app.exception_handler(GateError)
    async def gate_refused(request: Request, exc: GateError):
        s = db.new_session()
        try:
            return render(request, s, "refused.html", status_code=409, title="Refused: a client decision comes first",
                          message=exc.message, code=exc.code)
        finally:
            s.close()

    @app.exception_handler(NotYourDecision)
    async def not_yours(request: Request, exc: NotYourDecision):
        s = db.new_session()
        try:
            return render(request, s, "refused.html", status_code=403, title="Refused: not your decision",
                          message=str(exc), code=None)
        finally:
            s.close()

    @app.get("/")
    def home(request: Request, s=Depends(get_session)):
        return render(request, s, "home.html")

    @app.get("/healthz")
    def healthz():
        return JSONResponse({"ok": True, "model_mode": app.state.provider.mode})

    @app.post("/persona")
    def set_persona(request: Request, persona: str = Form(...), back: str = Form("/")):
        target = back if back.startswith("/") and not back.startswith("//") else "/"
        resp = RedirectResponse(target, status_code=303)
        if persona in PERSONAS:
            resp.set_cookie(COOKIE, persona, httponly=True, samesite="lax")
        return resp

    @app.post("/demo/reset")
    def demo_reset():
        """Start demo: rebuild the database from the seed (the spend log is kept), act as the Presenter."""
        db.reset_all()
        log.info("demo_reset")
        resp = RedirectResponse("/intake?demo=1", status_code=303)
        resp.set_cookie(COOKIE, "presenter", httponly=True, samesite="lax")
        return resp

    @app.get("/step/{n}")
    def step_placeholder(n: int, request: Request, s=Depends(get_session)):
        from app.records import service as records
        from app.web import current_deal, steps

        st = next((x for x in steps() if x["n"] == n), None)
        if st and st["built"]:
            return RedirectResponse(st["screens"][0]["route"], status_code=303)
        deal = current_deal(s)
        gate = None
        if n in (2, 3, 4) and deal:
            try:  # no marketing before the listing agreement is signed (L9)
                records.require(s, deal.id, "CP-03", action=f"start step {n}")
            except GateError as e:
                gate = e.message
        return render(request, s, "placeholder.html", step=st, gate=gate)

    # Review pages keep their addresses: mounted last, so app routes win and everything else falls through.
    if settings.review_dir.is_dir():
        app.mount("/", StaticFiles(directory=str(settings.review_dir), html=False), name="review")
    return app

