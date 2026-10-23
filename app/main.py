"""FastAPI app: the POC screens at /, the review pages (static, written by scripts/publish-review.sh) at their
old addresses (/index.html, /docs-*.html, ...). No login of its own: Traefik's house login is in front.

Run: uvicorn --factory app.main:create_app  (make run)"""

from __future__ import annotations

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app import db, humanize, logging_setup, pii
from app.db import get_session
from app.config import Settings
from app.logging_setup import log
from app.model.provider import ModelProvider, make_provider
from app.records.service import GateError, NotYourDecision
from app.web import APP_DIR, COOKIE, PERSONAS, merged_routes, render


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

    # Old screens merged into the path (decision 51) keep their addresses: each redirects to its new screen and
    # anchor, so the review pages, the tests and any saved link still land. Registered before the module routers.
    for old, (new, anchor) in merged_routes().items():
        app.add_api_route(old, (lambda target: (lambda: RedirectResponse(target, status_code=303)))(f"{new}#{anchor}"),
                          methods=["GET"], include_in_schema=False)

    from app.demo.routes import router as demo_router
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

    for r in (demo_router, intake_router, pcds_router, pricing_router, copy_router, channels_router, inbox_router, offers_router,
              buyer_router, contract_router, timeline_router, brand_router, people_router):
        app.include_router(r)

    def _refused(request: Request, status: int, title: str, message: str):
        """Every refusal in plain words, with the way back to the screen it came from (decision 47)."""
        from urllib.parse import urlparse

        from app.web import screen_for

        s = db.new_session()
        try:
            ref = urlparse(request.headers.get("referer") or "")
            back = ref.path if ref.path.startswith("/") and ref.netloc in ("", request.url.netloc) else None
            if request.url.path.startswith("/path/act/") or request.url.path.startswith("/path/change/"):
                from app.demo.walk import BY_KEY

                m = BY_KEY.get(request.url.path.rsplit("/", 1)[-1])
                back = back or (m.route if m else None)
            st, _ = screen_for(back or "")
            return render(request, s, "refused.html", status_code=status, title=title, message=message,
                          back=back or "/", back_title=st["title"] if st else None, code=None)
        finally:
            s.close()

    @app.exception_handler(FairHousingBlocked)
    async def fh_blocked(request: Request, exc: FairHousingBlocked):
        return _refused(request, 409, "Not yet: the fair-housing check has not passed", str(exc))

    @app.exception_handler(GateError)
    async def gate_refused(request: Request, exc: GateError):
        return _refused(request, 409, "Not yet: a decision comes first", humanize.gate_message(exc.message))

    @app.exception_handler(NotYourDecision)
    async def not_yours(request: Request, exc: NotYourDecision):
        return _refused(request, 403, "That is someone else's decision", humanize.gate_message(str(exc)))

    from app.web import NotFound

    @app.exception_handler(NotFound)
    async def not_found(request: Request, exc: NotFound):
        return _refused(request, 404, "Not found", str(exc))

    @app.exception_handler(ValueError)
    async def not_accepted(request: Request, exc: ValueError):
        return _refused(request, 422, "Not accepted", humanize.gate_message(str(exc)))

    from app.demo.recorded import OffScript

    @app.exception_handler(OffScript)
    async def off_script(request: Request, exc: OffScript):
        s = db.new_session()
        try:
            from app.web import screen_for

            st, _ = screen_for(exc.back.split("#")[0].split("?")[0])
            return render(request, s, "refused.html", status_code=409, title="Not in the recorded demo",
                          message=exc.message, put_back=exc.back, put_back_label=exc.label, back=exc.back,
                          back_title=st["title"] if st else None, code=None)
        finally:
            s.close()

    from app.model.provider import ReplayMiss, SpendCapReached

    @app.exception_handler(ReplayMiss)
    @app.exception_handler(SpendCapReached)
    async def ai_unavailable(request: Request, exc: Exception):
        from app.demo.path import plain_failure

        return _refused(request, 503, "The AI did not run", plain_failure(exc, True) + " Nothing was changed.")

    from starlette.exceptions import HTTPException as StarletteHTTPException

    @app.exception_handler(StarletteHTTPException)
    async def http_error(request: Request, exc: StarletteHTTPException):
        """A GET to an action's address (a refresh or Back after a form) lands on its screen, never on
        {"detail": "Method Not Allowed"} (fresh-eyes audit 5)."""
        if exc.status_code == 405 and request.method == "GET":
            from app.web import screen_for

            parts = request.url.path.rstrip("/").split("/")
            for i in range(len(parts), 1, -1):
                st, _ = screen_for("/".join(parts[:i]))
                if st:
                    return RedirectResponse(st["route"], status_code=303)
            return RedirectResponse("/", status_code=303)
        if exc.status_code == 404 and request.method == "GET":
            return _refused(request, 404, "Not found", "There is no page at this address.")
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

    @app.get("/")
    def home(request: Request, s=Depends(get_session)):
        from app.web import intro

        return render(request, s, "home.html", intro_notes=intro())

    @app.get("/healthz")
    def healthz():
        return JSONResponse({"ok": True, "model_mode": app.state.provider.mode})

    @app.post("/persona")
    def set_persona(request: Request, persona: str = Form(...), back: str = Form("/")):
        """"View as" (in the menu): whose eyes the screens use for the access log and the information wall."""
        target = back if back.startswith("/") and not back.startswith("//") else "/"
        resp = RedirectResponse(target, status_code=303)
        if persona in PERSONAS:
            resp.set_cookie(COOKIE, persona, httponly=True, samesite="lax")
        return resp

    # Review pages keep their addresses: mounted last, so app routes win and everything else falls through.
    if settings.review_dir.is_dir():
        app.mount("/", StaticFiles(directory=str(settings.review_dir), html=False), name="review")
    return app

