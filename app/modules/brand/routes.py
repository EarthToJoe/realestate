"""One more thing, after the finale (decision 51): how the firm finds sellers. The firm's campaign with its checks,
and who sees the ad, on one screen (/brand/targeting redirects to /brand#targeting). Every POST redirects back to
the screen (Post/Redirect/Get); the presenter's demo devices (a bolder headline, a refused age range) are refused in
plain words on the screen itself."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import Response

from app.db import get_session
from app.fairhousing import check as fh
from app.model.provider import ReplayMiss, SpendCapReached
from app.modules.brand import service
from app.modules.listing_copy.service import highlight
from app.records import service as records
from app.web import current_deal, gate_page, redirect, render

router = APIRouter()


def _panel(s, art) -> dict:
    res = fh.latest_result(s, "copy_artifact", art.id)
    current = res is not None and res.version == art.version and res.text_hash == fh.text_hash(art.text)
    claims = service.claims_of(art)
    marks = (res.findings if current and res else []) + [
        {**c, "cls": c["what"], "rule_id": c["rule_id"]} for c in claims]
    return {"art": art, "res": res if current else None, "claims": claims, "parts": service.parse(art),
            "marked": service.founder_html(highlight(art.text, marks)) if marks else None}


def _refuse(s, deal, message: str) -> None:
    """Keep the refusal to show it once on the screen (the refused attempt itself is already logged)."""
    st = service.state(deal)
    st["last_refusal"] = message
    service._save(s, deal, st)


@router.get("/brand")
def campaign(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    arts = service.artifacts(s, deal)
    st = service.state(deal)
    landing = next((a for a in arts if a.channel == "brand_landing"), None)
    ad = next((a for a in arts if a.channel == "brand_ad"), None)
    refusal = st.get("last_refusal") if request.query_params.get("refused") else None
    return render(request, s, "brand/campaign.html", panels=[_panel(s, a) for a in arts], st=st,
                  notices=service.notices_present(service.rendered_landing(landing)) if landing else [],
                  founder=service.founder, planted=service.PLANTED, rules_version=fh.load_rules().version,
                  allowed=service.allowed_targeting(), blocked=service.BLOCKED,
                  ad=service.parse(ad) if ad else None, refusal=refusal, cp19=records.latest(s, deal.id, "CP-19"))


@router.post("/brand/draft")
def draft(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return redirect("/brand")
    try:
        service.draft(s, deal, request.app.state.provider)
    except (ReplayMiss, SpendCapReached) as e:
        from app.demo.path import plain_failure

        return redirect("/brand", plain_failure(e, True))
    return redirect("/brand", "The AI wrote the firm's campaign and checked every piece.")


@router.post("/brand/piece/{artifact_id}/{action}")
def piece_action(artifact_id: int, action: str, request: Request, s=Depends(get_session)):
    if action not in ("plant", "fix", "check"):
        return Response(status_code=404)
    deal = current_deal(s)
    if deal is None:
        return redirect("/brand")
    art = service.get(s, deal, artifact_id)
    try:
        {"plant": service.plant, "fix": service.apply_fix, "check": service.check}[action](
            s, deal, art, request.app.state.provider)
    except (ValueError, ReplayMiss, SpendCapReached) as e:
        s.rollback()
        deal = current_deal(s)
        _refuse(s, deal, str(e))
        return redirect(f"/brand?refused=1#piece-{art.channel}")
    flash = {"plant": "The presenter tried a bolder headline: the claims check refused it.",
             "fix": "The AI removed the refused wording and checked the page again.",
             "check": "Checked again."}[action]
    return redirect(f"/brand#piece-{art.channel}", flash)


@router.post("/brand/targeting/set")
def set_targeting(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return redirect("/brand")
    service.set_targeting(s, deal)
    return redirect("/brand#targeting", "The AI chose who sees the ad: by place only.")


@router.post("/brand/targeting/try")
def try_targeting(request: Request, criterion: str = Form(...), s=Depends(get_session)):
    """Presenter's tool: try a targeting the law bars. Always refused, in code, and logged."""
    deal = current_deal(s)
    if deal is None:
        return redirect("/brand")
    try:
        service.try_targeting(s, deal, criterion)
    except service.CampaignRefused as e:
        _refuse(s, deal, str(e))
    return redirect("/brand?refused=1#targeting")


@router.post("/brand/publish")
def publish(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return redirect("/brand")
    try:
        service.publish(s, deal)
    except (service.CampaignRefused, fh.FairHousingBlocked) as e:
        s.rollback()
        deal = current_deal(s)
        _refuse(s, deal, f"Not published: {e}")
        return redirect("/brand?refused=1#targeting")
    return redirect("/brand#published", "The AI published the firm's campaign.")
