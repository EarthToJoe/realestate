"""Step 6 of the path, On the market: the channel board, the seller's marketing plan (CP-07), and the MLS entry
a person at the firm keys in (CP-08, simulated). Decisions 47 to 51."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.db import get_session
from app.demo import path
from app.modules.channels import service
from app.records import service as records
from app.records.service import GateError
from app.web import actor, current_deal, gate_page, redirect, render

router = APIRouter()


def _previous_choice(s, deal) -> tuple[str, list[str]]:
    """What the seller chose before, so a re-opened plan shows it (decision 48); else the AI's advice."""
    exposure, granted = next(iter(service.EXPOSURES)), [k for k, _, _ in service.AUTHORISATIONS]
    old = [cp for cp in records.records(s, deal.id, "CP-07", history=True)
           if cp.status == "superseded" and (cp.reason or "").startswith("Exposure: ")]
    if old:
        reason = old[-1].reason
        exposure = reason.split(".")[0].replace("Exposure: ", "")
        granted = [k for k, label, _ in service.AUTHORISATIONS if label in reason]
    return exposure, granted


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
    exposure, granted = _previous_choice(s, deal)
    return render(request, s, "channels/board.html", gate=gate, cards=[] if gate else service.board(s, deal),
                  cp07=records.latest(s, deal.id, "CP-07"), cp08=records.latest(s, deal.id, "CP-08"),
                  exposures=service.EXPOSURES, authorisations=service.AUTHORISATIONS, chosen_exposure=exposure,
                  chosen_granted=granted)


@router.post("/channels/authorise")
async def authorise(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    form = await request.form()
    decision = str(form.get("decision", "sign"))
    service.sign_authorisations(s, deal, actor(request, form), decision, str(form.get("exposure", "")),
                                list(form.getlist("granted")))
    done = "The seller signed the marketing plan" if decision == "sign" else "The seller declined the marketing plan"
    return redirect("/channels", path.after_action(s, request.app.state.provider, done))


@router.post("/channels/mls-entry")
def mls_entry(request: Request, s=Depends(get_session)):
    """A simulated person's step (CP-08), from any view: a person at the firm keys the listing into the MLS. It is
    not a client decision, so no persona is needed; the record says it was simulated."""
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    service.record_mls_entry(s, deal)
    return redirect("/channels", path.after_action(s, request.app.state.provider,
                                                   "A person at the firm keyed the listing into the MLS (simulated)"))


@router.get("/channels/authorise")
@router.get("/channels/mls-entry")
def back_to_board():
    """A refresh or Back onto an action's address lands on the screen (PRG; fresh-eyes audit 5)."""
    return RedirectResponse("/channels", status_code=303)
