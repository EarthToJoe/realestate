"""Step 7 of the path, Enquiries and showings: the seller approves the fact sheet and the AI's authority (CP-27),
the AI answers every enquiry on its own, and only the seller's own questions reach the seller (one form).
Decisions 47 to 51."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.db import get_session
from app.demo import path
from app.modules.inbox import service
from app.records import service as records
from app.records.service import GateError
from app.web import actor, current_deal, gate_page, redirect, render

router = APIRouter()

TOPIC = {"facts": "A question about the house", "showing": "A showing", "seller_only": "A question for the seller",
         "neighbourhood": "Schools and the area", "legal": "A legal question", "feedback": "Showing feedback",
         "holding": "Passed to the seller", "negotiation": "The seller's answer"}


def _self_guided_before(s, deal) -> bool:
    """A re-opened approval shows the seller's earlier choice (decision 48); else the AI's advice (allow)."""
    old = [cp for cp in records.records(s, deal.id, "CP-27", history=True)
           if cp.status == "superseded" and "self-guided" in (cp.reason or "")]
    return not old or "not allowed" not in old[-1].reason


@router.get("/inbox")
def inbox(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    gate, ins = None, None
    try:
        ins = service.open_fact_sheet(s, deal)
    except GateError as e:
        gate = e.message
    msgs = [] if gate else service.messages(s, deal)
    by_code = {c: records.records(s, deal.id, c) for c in ("CP-09", "CP-10", "CP-24", "CP-28", "CP-29")}
    for code in ("CP-09", "CP-10", "CP-28", "CP-29"):  # the buyer's side (step 8) writes these too
        by_code[code] = [c for c in by_code[code] if c.step == 5]
    by_code["CP-24"] = [c for c in by_code["CP-24"] if (c.attached_to or "").startswith("message:") and c.step != 8]
    answered = [m for m in msgs if m.direction == "in" and (m.extra or {}).get("seller_choice")]
    return render(request, s, "inbox/inbox.html", gate=gate, ins=ins, msgs=msgs,
                  cp27=records.latest(s, deal.id, "CP-27"), recs=by_code,
                  cards=[] if gate else service.seller_cards(s, deal), answered=answered,
                  choices=service.SELLER_CHOICES, topics=TOPIC, self_guided=_self_guided_before(s, deal),
                  remaining=len(service.ENQUIRIES) - len([m for m in msgs if m.direction == "in"]))


@router.post("/inbox/approve")
async def approve(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    form = await request.form()
    decision = str(form.get("decision", "approve"))
    service.approve(s, deal, actor(request, form), decision, self_guided=form.get("self_guided") == "yes")
    done = ("The seller approved what the AI may say" if decision == "approve"
            else "The seller declined: no reply may be sent")
    return redirect("/inbox", path.after_action(s, request.app.state.provider, done))


def _require_authority(s, deal):
    records.require(s, deal.id, "CP-27", action="send any reply (the seller has not approved the fact sheet and "
                                                "the AI's authority)")


@router.post("/inbox/next")
def next_enquiry(request: Request, s=Depends(get_session)):
    """A simulated enquiry arrives and the AI deals with it on its own."""
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    _require_authority(s, deal)
    m = service.next_enquiry(s, deal)
    if m:
        service.handle(s, deal, m, request.app.state.provider)
    return redirect("/inbox", "An enquiry arrived and the AI dealt with it." if m else "No more enquiries.")


@router.post("/inbox/all")
def all_enquiries(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    _require_authority(s, deal)
    while (m := service.next_enquiry(s, deal)) is not None:
        service.handle(s, deal, m, request.app.state.provider)
    return redirect("/inbox", path.after_action(s, request.app.state.provider,
                                                "The enquiries arrived and the AI answered them"))


@router.post("/inbox/answers")
async def answers(request: Request, s=Depends(get_session)):
    """The seller's answers to every question put to the seller, in one form (the bar's "Seller: send my
    answers"). Each is the seller's own decision; the AI then replies within it."""
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    form = await request.form()
    who = actor(request, form)
    provider = request.app.state.provider
    cards = service.seller_cards(s, deal)
    for m in cards:
        service.seller_answer(s, deal, provider, who, m.id, str(form.get(f"card-{m.id}") or ""))
    done = "The seller answered" if cards else "Nothing was waiting for the seller"
    return redirect("/inbox", path.after_action(s, provider, done))


@router.post("/inbox/answer/{message_id}")
async def answer(message_id: int, request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    form = await request.form()
    service.seller_answer(s, deal, request.app.state.provider, actor(request, form), message_id,
                          str(form.get("decision", "")))
    return redirect("/inbox#cards", path.after_action(s, request.app.state.provider, "The seller answered"))


@router.get("/inbox/approve")
@router.get("/inbox/next")
@router.get("/inbox/all")
@router.get("/inbox/answers")
@router.get("/inbox/answer/{message_id}")
def back_to_inbox():
    """A refresh or Back onto an action's address lands on the screen (PRG; fresh-eyes audit 5)."""
    return RedirectResponse("/inbox", status_code=303)
