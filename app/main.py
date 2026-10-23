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
from app.web import APP_DIR, COOKIE, GUIDE_COOKIE, PERSONAS, render


def _register_people() -> None:
    """After a restart, teach the log masker the people already in the database."""
    from app.models import Person

    s = db.new_session()
    try:
        for p in s.query(Person).filter(Person.erased_at.is_(None)).all():
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
    from app.disclosures.routes import router as pcds_router
    from app.modules.buyer.routes import router as buyer_router
    from app.modules.contract.routes import router as contract_router
    from app.modules.brand.routes import router as brand_router
    from app.modules.people.routes import router as people_router
    from app.fairhousing.check import FairHousingBlocked

    for r in (intake_router, pcds_router, pricing_router, copy_router, channels_router, inbox_router, offers_router,
              buyer_router, contract_router, timeline_router, brand_router, people_router):
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

    from app.web import NotFound

    @app.exception_handler(NotFound)
    async def not_found(request: Request, exc: NotFound):
        s = db.new_session()
        try:
            return render(request, s, "refused.html", status_code=404, title="Not found", message=str(exc), code=None)
        finally:
            s.close()

    @app.exception_handler(ValueError)
    async def not_accepted(request: Request, exc: ValueError):
        s = db.new_session()
        try:
            return render(request, s, "refused.html", status_code=422, title="Not accepted", message=str(exc),
                          code=None)
        finally:
            s.close()

    from app.model.provider import ReplayMiss, SpendCapReached

    @app.exception_handler(ReplayMiss)
    @app.exception_handler(SpendCapReached)
    async def ai_unavailable(request: Request, exc: Exception):
        s = db.new_session()
        try:
            return render(request, s, "refused.html", status_code=503, title="The AI's answer is not recorded",
                          message=f"{exc} Nothing was changed.", code=None)
        finally:
            s.close()

    @app.get("/")
    def home(request: Request, s=Depends(get_session)):
        from app.web import intro

        return render(request, s, "home.html", intro_notes=intro())

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

    def _local(path: str | None, default: str = "/") -> str:
        return path if path and path.startswith("/") and not path.startswith("//") else default

    @app.get("/demo/start")
    def demo_start(request: Request, back: str = "/", s=Depends(get_session)):
        """Start demo asks first: the reset removes the current deal."""
        return render(request, s, "demo_start.html", back=_local(back))

    @app.post("/demo/reset")
    def demo_reset():
        """Start demo: rebuild the database from the seed (the spend log is kept), act as the Presenter."""
        db.reset_all()
        log.info("demo_reset")
        resp = RedirectResponse("/intake?demo=1&started=1", status_code=303)
        resp.set_cookie(COOKIE, "presenter", httponly=True, samesite="lax")
        resp.set_cookie(GUIDE_COOKIE, "on", httponly=True, samesite="lax")  # Start demo starts the guided demo
        return resp

    @app.post("/demo/guide")
    def demo_guide(on: str = Form("on"), back: str = Form("/")):
        """Turn the guided demo on (notes open on every screen, screen k of N, Next) or off."""
        resp = RedirectResponse(_local(back), status_code=303)
        if on == "on":
            resp.set_cookie(GUIDE_COOKIE, "on", httponly=True, samesite="lax")
        else:
            resp.delete_cookie(GUIDE_COOKIE)
        return resp

    @app.post("/demo/play")
    def demo_play(request: Request, route: str = Form(...), s=Depends(get_session)):
        """Guided demo, Presenter only: "Do this screen for me" plays this screen's taps the way the script does
        (the same plays as fast-forward, on the recorded replays), each client decision recorded as the client's."""
        from app.demo import walk
        from app.web import persona, screen_for

        if persona(request) != "presenter":
            raise NotYourDecision("Only the Presenter can play a screen of the demo.")
        st, sc = screen_for(route)
        if sc is None:
            raise ValueError("That is not a screen of the demo.")
        played = walk.play_screen(s, request.app.state.provider, route)
        log.info("demo_play", route=route, played=[m.key for m in played])
        return RedirectResponse(route, status_code=303)  # the screen opens on its outcome, at the top

    @app.post("/demo/fast-forward/{n}")
    async def demo_fast_forward(n: int, request: Request, s=Depends(get_session)):
        """Presenter only: play the steps before step n with the demo's scripted choices (replays, $0), each client
        decision recorded as the client's, then open the step (the screen the presenter was on, if it is in it)."""
        from app.demo import walk
        from app.web import persona, screen_for, steps

        if persona(request) != "presenter":
            raise NotYourDecision("Only the Presenter can fast-forward the demo.")
        st = next((x for x in steps() if x["n"] == n), None)
        if st is None or not st["built"]:
            raise ValueError(f"Step {n} is not built yet, so there is nothing to fast-forward to.")
        back = _local(str((await request.form()).get("back") or ""), "")
        back_step, _ = screen_for(back)
        if not (back_step and back_step["n"] == n):
            back = st["screens"][0]["route"]
        played = walk.fast_forward(s, request.app.state.provider, n, back)
        log.info("demo_fast_forward", step=n, played=[m.key for m in played])
        return RedirectResponse(back, status_code=303)

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

