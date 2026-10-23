"""Step 2 Pricing screens: comparable sales and adjustments; the AI's advice, net sheet and the seller's choice."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.db import get_session
from app.model.provider import ReplayMiss, SpendCapReached
from app.modules.pricing import service
from app.records import service as records
from app.records.service import GateError
from app.web import current_deal, gate_page, persona, render

router = APIRouter()


def _ctx(s, deal) -> dict:
    gate = None
    try:
        records.require(s, deal.id, "CP-03", action="start pricing (no marketing before the listing agreement, L9)")
    except GateError as e:
        gate = e.message
    pa = None if gate else service.analyse(s, deal)
    advice = pa.advice if pa else None
    tax = next((f.value for f in deal.property.facts if f.field == "TaxAnnualAmount"), None)
    tax = int(tax) if tax and str(tax).isdigit() else None
    rec_price = advice["recommended_price"] if advice else None
    return {"gate": gate, "pa": pa, "advice": advice, "label": service.LABEL,
            "cp25": records.latest(s, deal.id, "CP-25"), "cp05": records.latest(s, deal.id, "CP-05"),
            "net_rec": service.net_sheet(rec_price, tax) if rec_price else None,
            "net_chosen": service.net_sheet(deal.list_price, tax) if deal.list_price else None}


@router.get("/pricing")
def comps(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    return render(request, s, "pricing/comps.html", **_ctx(s, deal))


@router.get("/pricing/advice")
def advice(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    return render(request, s, "pricing/advice.html", **_ctx(s, deal))


@router.post("/pricing/recommend")
def recommend(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    error = None
    try:
        service.advise(s, deal, request.app.state.provider)
    except (ReplayMiss, SpendCapReached) as e:
        error = str(e)
    if error is None and not request.headers.get("HX-Request"):
        return RedirectResponse("/pricing/advice", status_code=303)
    tpl = "pricing/_advice_body.html" if request.headers.get("HX-Request") else "pricing/advice.html"
    return render(request, s, tpl, ai_error=error, **_ctx(s, deal))


@router.post("/pricing/choose")
async def choose(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    form = await request.form()
    raw = str(form.get("price", "")).replace(",", "").replace("$", "").strip()
    try:
        service.choose_price(s, deal, persona(request), int(raw or 0))
    except ValueError as e:
        return render(request, s, "pricing/advice.html", status_code=422, error=str(e), **_ctx(s, deal))
    return RedirectResponse("/pricing/advice#rec-CP-05", status_code=303)
