"""Step 3 Listing copy screens: drafts with the fair-housing panel; MLS pre-check and package; the flyer."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, Response

from app.db import get_session
from app.fairhousing import check as fh
from app.model.provider import ReplayMiss, SpendCapReached
from app.modules.listing_copy import pdf, service
from app.records import service as records
from app.records.service import GateError
from app.web import current_deal, render

router = APIRouter()


def _gate(s, deal) -> str | None:
    try:
        records.require(s, deal.id, "CP-03", action="write listing copy (no marketing before the listing agreement, L9)")
        records.require(s, deal.id, "CP-05", action="write listing copy (the seller chooses the list price first)")
    except GateError as e:
        return e.message
    return None


def _panel(s, art) -> dict:
    res = fh.latest_result(s, "copy_artifact", art.id)
    current = res is not None and res.version == art.version and res.text_hash == fh.text_hash(art.text)
    return {"art": art, "res": res if current else None,
            "marked": service.highlight(art.text, res.findings) if current and res.findings else None,
            "mls_checks": service.remarks_checks(art.text) if art.channel == "mls_remarks" else None,
            "flyer": service.parse_flyer(art.text) if art.channel == "flyer" else None}


def _page(request, s, deal, status_code=200, **extra):
    arts = service.artifacts(s, deal)
    return render(request, s, "copy/drafts.html", status_code=status_code, gate=_gate(s, deal),
                  panels=[_panel(s, a) for a in arts], rules_version=fh.load_rules().version,
                  cp06=records.records(s, deal.id, "CP-06"), cp26=records.records(s, deal.id, "CP-26"),
                  planted=service.PLANTED, **extra)


@router.get("/copy")
def drafts(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    return _page(request, s, deal)


@router.post("/copy/draft")
def draft(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    try:
        service.draft(s, deal, request.app.state.provider)
    except (ReplayMiss, SpendCapReached) as e:
        return _page(request, s, deal, ai_error=str(e))
    return RedirectResponse("/copy", status_code=303)


def _artifact_action(request, s, artifact_id: int, action: str):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    if _gate(s, deal):
        return _page(request, s, deal, status_code=409)
    art = service.get(s, deal, artifact_id)
    error = None
    try:
        if action == "check":
            service.check(s, deal, art, request.app.state.provider)
        elif action == "plant":
            service.plant(s, deal, art, request.app.state.provider)
        elif action == "fix":
            service.apply_fix(s, deal, art, request.app.state.provider)
        elif action == "ready":
            service.mark_ready(s, deal, art)
    except fh.FairHousingBlocked as e:
        error = f"Not marked ready to publish: {e}"
    except (ValueError, ReplayMiss, SpendCapReached) as e:
        error = str(e)
    if request.headers.get("HX-Request"):
        return render(request, s, "copy/_artifact.html", p=_panel(s, art), error=error, planted=service.PLANTED,
                      status_code=200)
    if error:
        return _page(request, s, deal, status_code=409 if action == "ready" else 422, error=error)
    return RedirectResponse(f"/copy#art-{art.id}", status_code=303)


@router.post("/copy/{artifact_id}/{action}")
def artifact_action(artifact_id: int, action: str, request: Request, s=Depends(get_session)):
    if action not in ("check", "plant", "fix", "ready"):
        return Response(status_code=404)
    return _artifact_action(request, s, artifact_id, action)


@router.post("/copy/ready-all")
def ready_all(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    if _gate(s, deal):
        return _page(request, s, deal, status_code=409)
    done, refused = service.mark_all_ready(s, deal)
    return _page(request, s, deal, marked_now=done, refused=refused)


@router.get("/copy/mls")
def mls(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    remarks = next((a for a in service.artifacts(s, deal) if a.channel == "mls_remarks"), None)
    res = fh.latest_result(s, "copy_artifact", remarks.id) if remarks else None
    return render(request, s, "copy/mls.html", gate=_gate(s, deal), remarks=remarks,
                  checks=service.remarks_checks(remarks.text) if remarks else [], fh_res=res,
                  package=service.mls_package(s, deal))


@router.get("/copy/flyer")
def flyer_html(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    art = next((a for a in service.artifacts(s, deal) if a.channel == "flyer"), None) if deal else None
    if art is None:
        return RedirectResponse("/copy", status_code=303)
    return Response(pdf.flyer_html(deal, art), media_type="text/html")


@router.get("/copy/flyer.pdf")
def flyer_pdf(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    art = next((a for a in service.artifacts(s, deal) if a.channel == "flyer"), None) if deal else None
    if art is None:
        return RedirectResponse("/copy", status_code=303)
    return Response(pdf.flyer_pdf(deal, art), media_type="application/pdf",
                    headers={"Content-Disposition": 'inline; filename="flyer-DEMONSTRATION.pdf"'})
