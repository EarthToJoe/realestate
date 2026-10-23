"""The Property Condition Disclosure Statement (CP-04): the seller's own form, now part of step 11, the contract
(decision 51). GET /disclosures/pcds redirects to /contract#pcds (app/main.py); the form posts here and comes back
there (Post/Redirect/Get)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.db import get_session
from app.demo import path
from app.disclosures import pcds
from app.records import service as records
from app.web import actor, current_deal, redirect, templates

router = APIRouter()
BACK = "/contract#pcds"


def _ctx(s, deal, **kw):
    return dict(form=pcds.form(), questions=pcds.questions, fields=pcds.fields, labels=pcds.CHOICE_LABELS,
                cp04=records.latest(s, deal.id, "CP-04"), saved=pcds.answers_of(s, deal), demo_note=pcds.DEMO_NOTE,
                **kw)


def _errors_by_question(errors: list[str]) -> dict[int, str]:
    """"Question 35: the form asks you to explain this answer." -> {35: ...}, so each shows beside its question."""
    out: dict[int, str] = {}
    for e in errors:
        words = e.split()
        if len(words) > 1 and words[0] == "Question":
            n = "".join(ch for ch in words[1] if ch.isdigit())
            if n:
                out.setdefault(int(n), e)
    return out


@router.post("/disclosures/pcds")
async def pcds_submit(request: Request, s=Depends(get_session)):
    """The seller's own typed answers. Only the seller can submit (the record service checks)."""
    deal = current_deal(s)
    if deal is None:
        return redirect("/intake", "Start with step 1: the seller signs up.")
    form = await request.form()
    answers = {k: ",".join(form.getlist(k)) if len(form.getlist(k)) > 1 else str(form.get(k, ""))
               for k in pcds.all_keys()}
    who = actor(request, form)
    errors = pcds.validate({k: v.strip() for k, v in answers.items()})
    if errors:
        if who != "seller":  # someone else's answers are refused before they are checked
            from app.records.service import NotYourDecision

            raise NotYourDecision("Only the seller completes the Property Condition Disclosure Statement.")
        from app.modules.contract.routes import contract_page

        return contract_page(request, s, status_code=422, answers=answers, pcds_errors=errors,
                             pcds_q_errors=_errors_by_question(errors))
    pcds.submit(s, deal, who, answers)
    return redirect(BACK, path.after_action(s, request.app.state.provider, "The seller submitted the disclosure form"))


@router.post("/disclosures/pcds/prepared")
async def pcds_prepared(request: Request, s=Depends(get_session)):
    """The demo seller submits the answers they prepared (seed/personas.yaml). Only the seller can: the record
    service refuses anyone else, so the software cannot complete the form for them."""
    deal = current_deal(s)
    if deal is None:
        return redirect("/intake", "Start with step 1: the seller signs up.")
    form = await request.form()
    pcds.submit(s, deal, actor(request, form), pcds.prepared_answers(), prepared=True)
    return redirect(BACK, path.after_action(s, request.app.state.provider, "The seller submitted the disclosure form"))


@router.get("/disclosures/pcds/print", response_class=HTMLResponse)
def pcds_print(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None or not records.is_done(s, deal.id, "CP-04"):
        if deal is None:
            return redirect("/contract")
        return redirect(BACK, "The seller has not completed the disclosure form yet.")
    return templates.get_template("disclosures/pcds_print.html").render(
        deal=deal, **_ctx(s, deal), answer_label=pcds.answer_label)
