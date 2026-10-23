"""Step 10 screens: the firm's campaign with its checks; the ad's targeting and publishing."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, Response

from app.db import get_session
from app.fairhousing import check as fh
from app.model.provider import ReplayMiss, SpendCapReached
from app.modules.brand import service
from app.modules.listing_copy.service import highlight
from app.records import service as records
from app.web import current_deal, gate_page, render

router = APIRouter()


def _panel(s, art) -> dict:
    res = fh.latest_result(s, "copy_artifact", art.id)
    current = res is not None and res.version == art.version and res.text_hash == fh.text_hash(art.text)
    claims = service.claims_of(art)
    marks = (res.findings if current and res else []) + [
        {**c, "cls": c["what"], "rule_id": c["rule_id"]} for c in claims]
    return {"art": art, "res": res if current else None, "claims": claims, "parts": service.parse(art),
            "marked": service.founder_html(highlight(art.text, marks)) if marks else None}


def _page(request, s, deal, status_code=200, **extra):
    arts = service.artifacts(s, deal)
    st = service.state(deal)
    landing = next((a for a in arts if a.channel == "brand_landing"), None)
    return render(request, s, "brand/campaign.html", status_code=status_code, panels=[_panel(s, a) for a in arts],
                  st=st, notices=service.notices_present(service.rendered_landing(landing)) if landing else [],
                  founder=service.founder, planted=service.PLANTED, rules_version=fh.load_rules().version,
                  cp19=records.latest(s, deal.id, "CP-19"), **extra)


@router.get("/brand")
def campaign(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    return _page(request, s, deal)


@router.post("/brand/draft")
def draft(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/brand", status_code=303)
    try:
        service.draft(s, deal, request.app.state.provider)
    except (ReplayMiss, SpendCapReached) as e:
        return _page(request, s, deal, ai_error=str(e))
    return RedirectResponse("/brand", status_code=303)


@router.post("/brand/piece/{artifact_id}/{action}")
def piece_action(artifact_id: int, action: str, request: Request, s=Depends(get_session)):
    if action not in ("plant", "fix", "check"):
        return Response(status_code=404)
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/brand", status_code=303)
    art = service.get(s, deal, artifact_id)
    try:
        {"plant": service.plant, "fix": service.apply_fix, "check": service.check}[action](
            s, deal, art, request.app.state.provider)
    except (ValueError, ReplayMiss, SpendCapReached) as e:
        return _page(request, s, deal, status_code=422, error=str(e))
    return RedirectResponse(f"/brand#piece-{art.channel}", status_code=303)


def _targeting_page(request, s, deal, status_code=200, **extra):
    st = service.state(deal)
    arts = service.artifacts(s, deal)
    return render(request, s, "brand/targeting.html", status_code=status_code, st=st, arts=arts,
                  allowed=service.allowed_targeting(), blocked=service.BLOCKED,
                  ad=service.parse(next(a for a in arts if a.channel == "brand_ad")) if arts else None,
                  cp19=records.latest(s, deal.id, "CP-19"), **extra)


@router.get("/brand/targeting")
def targeting(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    return _targeting_page(request, s, deal)


@router.post("/brand/targeting/set")
def set_targeting(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/brand/targeting", status_code=303)
    service.set_targeting(s, deal)
    return RedirectResponse("/brand/targeting", status_code=303)


@router.post("/brand/targeting/try")
def try_targeting(request: Request, criterion: str = Form(...), s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/brand/targeting", status_code=303)
    try:
        service.try_targeting(s, deal, criterion)
    except service.CampaignRefused as e:
        s.commit()  # keep the logged refusal
        return _targeting_page(request, s, deal, status_code=409, refusal=str(e))
    return RedirectResponse("/brand/targeting", status_code=303)


@router.post("/brand/publish")
def publish(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/brand/targeting", status_code=303)
    try:
        service.publish(s, deal)
    except (service.CampaignRefused, fh.FairHousingBlocked) as e:
        return _targeting_page(request, s, deal, status_code=409, refusal=str(e))
    return RedirectResponse("/brand/targeting#published", status_code=303)
