"""Step 4 of the path, The price (decision 51): the comparable sales and the AI's advice on one screen, leading on
the recommendation; the seller's choice of list price (CP-05) is the action bar's one button."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.db import get_session
from app.demo import path, recorded
from app.model.provider import ReplayMiss, SpendCapReached
from app.modules.pricing import service
from app.records import service as records
from app.records.service import GateError
from app.web import actor, current_deal, gate_page, redirect, render

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
    cp05 = records.latest(s, deal.id, "CP-05")
    chosen = deal.list_price if cp05 and cp05.status == "done" else None
    return {"gate": gate, "pa": pa, "advice": advice, "label": service.LABEL,
            "cp25": records.latest(s, deal.id, "CP-25"), "cp05": cp05, "chosen": chosen,
            "net_rec": service.net_sheet(rec_price, tax) if rec_price else None,
            "net_chosen": service.net_sheet(chosen, tax) if chosen else None}


@router.get("/pricing")
def pricing(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    return render(request, s, "pricing/price.html", errors={}, **_ctx(s, deal))


@router.post("/pricing/recommend")
def recommend(request: Request, s=Depends(get_session)):
    """The AI act (the action bar's button when the AI has not priced on its own). Post/Redirect/Get."""
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    provider = request.app.state.provider
    try:
        service.advise(s, deal, provider)
    except (ReplayMiss, SpendCapReached) as e:
        s.rollback()
        return redirect("/pricing", path.plain_failure(e, provider.mode == "replay"))
    return redirect("/pricing", "The AI priced the house.")


@router.post("/pricing/choose")
async def choose(request: Request, s=Depends(get_session)):
    """CP-05, recorded as the client the button names (decision 49). In a recorded demo the price is the recorded
    one (fresh-eyes audit 4). From the action bar (`ui`), the AI then does its own work (decision 47)."""
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    form = await request.form()
    raw = str(form.get("price", "")).replace(",", "").replace("$", "").strip()
    if not raw.isdigit():
        return render(request, s, "pricing/price.html", status_code=422, price_input=form.get("price", ""),
                      errors={"price": "Enter the list price as a whole number of dollars, for example 640000."},
                      **_ctx(s, deal))
    pa = service.current(s, deal)
    rec = (pa.advice or {}).get("recommended_price") if pa else None
    if rec:
        recorded.check(request, {"price": raw}, {"price": rec}, back="/pricing")
    price = int(raw)
    try:
        service.choose_price(s, deal, actor(request, form), price)
    except ValueError as e:
        return render(request, s, "pricing/price.html", status_code=422, price_input=raw, errors={"price": str(e)},
                      **_ctx(s, deal))
    done = f"The seller chose to list at ${price:,}"
    if form.get("ui"):
        return redirect("/pricing", path.after_action(s, request.app.state.provider, done))
    return redirect("/pricing", done + ".")
