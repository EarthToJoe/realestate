"""Step 5 Communications screens: fact sheet and authority (CP-27), shared inbox, seller's decision cards,
showings and feedback, outbox."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.db import get_session
from app.modules.inbox import service
from app.records import service as records
from app.records.service import GateError
from app.web import current_deal, persona, render

router = APIRouter()


@router.get("/inbox")
def inbox(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    gate, ins = None, None
    try:
        ins = service.open_fact_sheet(s, deal)
    except GateError as e:
        gate = e.message
    msgs = [] if gate else service.messages(s, deal)
    by_code = {c: records.records(s, deal.id, c) for c in ("CP-09", "CP-10", "CP-24", "CP-28", "CP-29")}
    return render(request, s, "inbox/inbox.html", gate=gate, ins=ins, msgs=msgs,
                  cp27=records.latest(s, deal.id, "CP-27"), recs=by_code,
                  cards=[] if gate else service.seller_cards(s, deal), choices=service.SELLER_CHOICES,
                  remaining=len(service.ENQUIRIES) - len([m for m in msgs if m.direction == "in"]))


@router.post("/inbox/approve")
async def approve(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    form = await request.form()
    service.approve(s, deal, persona(request), str(form.get("decision", "approve")),
                    self_guided=form.get("self_guided") == "yes")
    return RedirectResponse("/inbox#rec-CP-27", status_code=303)


@router.post("/inbox/next")
def next_enquiry(request: Request, s=Depends(get_session)):
    """A simulated enquiry arrives and the AI deals with it on its own."""
    deal = current_deal(s)
    records.require(s, deal.id, "CP-27", action="send any reply (the seller has not approved the fact sheet and "
                                                "the AI's authority)")
    m = service.next_enquiry(s, deal)
    if m:
        service.handle(s, deal, m, request.app.state.provider)
    return RedirectResponse(f"/inbox#thread-{m.thread if m else ''}", status_code=303)


@router.post("/inbox/all")
def all_enquiries(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    records.require(s, deal.id, "CP-27", action="send any reply (the seller has not approved the fact sheet and "
                                                "the AI's authority)")
    while (m := service.next_enquiry(s, deal)) is not None:
        service.handle(s, deal, m, request.app.state.provider)
    return RedirectResponse("/inbox#inbox", status_code=303)


@router.post("/inbox/answer/{message_id}")
async def answer(message_id: int, request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    form = await request.form()
    service.seller_answer(s, deal, request.app.state.provider, persona(request), message_id,
                          str(form.get("decision", "")))
    return RedirectResponse("/inbox#cards", status_code=303)
