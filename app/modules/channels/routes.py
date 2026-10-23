"""Step 4 Marketing plan screen: the channel board, the seller's authorisations, the MLS "human required" step."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.db import get_session
from app.modules.channels import service
from app.records import service as records
from app.records.service import GateError, NotYourDecision
from app.web import current_deal, gate_page, persona, render

router = APIRouter()


@router.get("/channels")
def board(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    gate = None
    try:
        service.open_authorisations(s, deal)
    except GateError as e:
        gate = e.message
    return render(request, s, "channels/board.html", gate=gate, cards=[] if gate else service.board(s, deal),
                  cp07=records.latest(s, deal.id, "CP-07"), cp08=records.latest(s, deal.id, "CP-08"),
                  exposures=service.EXPOSURES, authorisations=service.AUTHORISATIONS)


@router.post("/channels/authorise")
async def authorise(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    form = await request.form()
    service.sign_authorisations(s, deal, persona(request), str(form.get("decision", "sign")),
                                str(form.get("exposure", "")), list(form.getlist("granted")))
    return RedirectResponse("/channels#rec-CP-07", status_code=303)


@router.post("/channels/mls-entry")
def mls_entry(request: Request, s=Depends(get_session)):
    """A simulated human-required completion: only the Presenter records it (spec section 2)."""
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    if persona(request) != "presenter":
        raise NotYourDecision("Only the Presenter records a simulated human-required step; no client can.")
    service.record_mls_entry(s, deal)
    return RedirectResponse("/channels#card-mls", status_code=303)
