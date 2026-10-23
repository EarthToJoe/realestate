"""Step 6 Offers screens: comparison and net sheets, the seller's AI's advice (CP-11), the seller's decision (CP-12)
with its price and terms, the negotiation thread (CP-13), the dual-agency consent (CP-17) and the refusal of a
counter outside the seller's decision."""

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
def offers(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    gate, table = None, []
    try:
        table = service.compare(s, deal)
    except GateError as e:
        gate = e.message
    st = service.state(deal)
    return render(request, s, "offers/offers.html", gate=gate, offers=table, st=st,
                  cp11=records.latest(s, deal.id, "CP-11"), cp12=records.latest(s, deal.id, "CP-12"),
                  cp13=[c for c in records.records(s, deal.id, "CP-13") if c.attached_to == "offers:seller"],
                  cp17=records.latest(s, deal.id, "CP-17"), not_binding=service.NOT_BINDING,
                  defaults=service.DECISION_DEFAULTS, terms_text=service.terms_text,
                  not_ready=request.query_params.get("not_ready"))


@router.post("/offers/advise")
def advise(request: Request, s=Depends(get_session)):
    try:
        service.advise(s, current_deal(s), request.app.state.provider)
    except service.NotReady as e:
        return RedirectResponse(f"/offers?not_ready={e.message}#advice", status_code=303)
    return RedirectResponse("/offers#advice", status_code=303)


@router.post("/offers/decide")
async def decide(request: Request, s=Depends(get_session)):
    form = await request.form()
    service.decide(s, current_deal(s), persona(request), decision=str(form.get("decision", "")),
                   offer_label=str(form.get("offer", "A")), counter_price=_int(form.get("counter_price")),
                   lowest_price=_int(form.get("lowest_price")), closing_days=_int(form.get("closing_days")),
                   closing_min=_int(form.get("closing_min")), closing_max=_int(form.get("closing_max")),
                   inspection_max=_int(form.get("inspection_max")), mortgage_max=_int(form.get("mortgage_max")),
                   allow_requests=form.get("allow_requests") == "yes")
    return RedirectResponse("/offers#rec-CP-12", status_code=303)


@router.post("/offers/negotiate")
def negotiate(request: Request, s=Depends(get_session)):
    """The seller's AI takes its next step within the seller's decision."""
    service.negotiate(s, current_deal(s))
    return RedirectResponse("/offers#negotiation", status_code=303)


@router.post("/offers/counter")
async def counter(request: Request, s=Depends(get_session)):
    """Demo: try sending a counter by hand; code refuses one outside the seller's decision."""
    if persona(request) != "presenter":
        raise NotYourDecision("Only the Presenter can try a counter by hand; the AI negotiates on its own.")
    form = await request.form()
    deal = current_deal(s)
    terms = {**service.counter_terms(deal), "price": _int(form.get("price")) or 0}
    for k in ("closing_days", "inspection_days", "mortgage_days", "seller_credit"):
        if _int(form.get(k)) is not None:
            terms[k] = _int(form.get(k))
    try:
        service.check_counter(deal, terms)
    except service.CounterRefused as e:
        return render(request, s, "refused.html", status_code=409, title="Refused: outside the seller's decision",
                      message=e.message)
    service.send_counter(s, deal, terms)
    return RedirectResponse("/offers#negotiation", status_code=303)


@router.post("/offers/consent")
async def consent(request: Request, s=Depends(get_session)):
    """CP-17 from the seller's screen (the buyer gives theirs on the buyer's tour screen)."""
    from app.modules.buyer import service as buyer

    form = await request.form()
    buyer.consent_dual_agency(s, current_deal(s), persona(request), str(form.get("decision", "consent")))
    return RedirectResponse("/offers#rec-CP-17", status_code=303)
