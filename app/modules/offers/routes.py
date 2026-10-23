"""Step 6 Offers screens: comparison and net sheets, the AI's advice (CP-11), the seller's decision (CP-12), the
negotiation thread (CP-13), and the refusal of a counter outside the seller's decision."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.db import get_session
from app.modules.offers import service
from app.records import service as records
from app.records.service import GateError, NotYourDecision
from app.web import current_deal, persona, render

router = APIRouter()


def _int(v) -> int | None:
    try:
        return int(str(v).replace(",", "").replace("$", "").strip())
    except (TypeError, ValueError):
        return None


@router.get("/offers")
def offers(request: Request, s=Depends(get_session), refused: str | None = None):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    gate, table = None, []
    try:
        table = service.compare(s, deal)
    except GateError as e:
        gate = e.message
    return render(request, s, "offers/offers.html", gate=gate, offers=table, st=service.state(deal),
                  cp11=records.latest(s, deal.id, "CP-11"), cp12=records.latest(s, deal.id, "CP-12"),
                  cp13=records.records(s, deal.id, "CP-13"), not_binding=service.NOT_BINDING, refused=refused)


@router.post("/offers/advise")
def advise(request: Request, s=Depends(get_session)):
    service.advise(s, current_deal(s), request.app.state.provider)
    return RedirectResponse("/offers#advice", status_code=303)


@router.post("/offers/decide")
async def decide(request: Request, s=Depends(get_session)):
    form = await request.form()
    service.decide(s, current_deal(s), persona(request), decision=str(form.get("decision", "")),
                   offer=str(form.get("offer", "A")), counter_price=_int(form.get("counter_price")),
                   lowest_price=_int(form.get("lowest_price")))
    return RedirectResponse("/offers#rec-CP-12", status_code=303)


@router.post("/offers/negotiate")
def negotiate(request: Request, s=Depends(get_session)):
    """The AI takes the next negotiation step within the seller's decision."""
    service.negotiate(s, current_deal(s))
    return RedirectResponse("/offers#negotiation", status_code=303)


@router.post("/offers/counter")
async def counter(request: Request, s=Depends(get_session)):
    """Demo: try sending a counter at any price; code refuses one outside the seller's decision."""
    if persona(request) != "presenter":
        raise NotYourDecision("Only the Presenter can try a counter by hand; the AI negotiates on its own.")
    form = await request.form()
    deal = current_deal(s)
    try:
        service.send_counter(s, deal, _int(form.get("price")) or 0, terms_changed=form.get("terms_changed") == "yes")
    except service.CounterRefused as e:
        s.rollback()
        return render(request, s, "refused.html", status_code=409, title="Refused: outside the seller's decision",
                      message=e.message, back="/offers#negotiation")
    return RedirectResponse("/offers#negotiation", status_code=303)
