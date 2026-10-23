"""The Property Condition Disclosure Statement screen (CP-04): the seller's own form, reached from the step 1
checklist and from the contract step (signing waits for it, L43)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.db import get_session
from app.disclosures import pcds
from app.records import service as records
from app.web import current_deal, gate_page, persona, render, templates

router = APIRouter()


def _ctx(s, deal, **kw):
    return dict(form=pcds.form(), questions=pcds.questions, fields=pcds.fields, labels=pcds.CHOICE_LABELS,
                cp04=records.latest(s, deal.id, "CP-04"), saved=pcds.answers_of(s, deal), demo_note=pcds.DEMO_NOTE,
                **kw)


@router.get("/disclosures/pcds")
def pcds_form(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    return render(request, s, "disclosures/pcds.html", answers={}, error=None, **_ctx(s, deal))


@router.post("/disclosures/pcds")
async def pcds_submit(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    form = await request.form()
    answers = {k: ",".join(form.getlist(k)) if len(form.getlist(k)) > 1 else str(form.get(k, ""))
               for k in pcds.all_keys()}
    try:
        pcds.submit(s, deal, persona(request), answers)
    except ValueError as e:
        return render(request, s, "disclosures/pcds.html", status_code=422, answers=answers, error=str(e),
                      **_ctx(s, deal))
    return RedirectResponse(request.query_params.get("back") or "/disclosures/pcds", status_code=303)


@router.post("/disclosures/pcds/prepared")
def pcds_prepared(request: Request, s=Depends(get_session)):
    """The demo seller submits the answers they prepared (seed/personas.yaml). Only the seller can: the record
    service refuses any other persona, so the software cannot complete the form for them."""
    deal = current_deal(s)
    pcds.submit(s, deal, persona(request), pcds.prepared_answers(), prepared=True)
    return RedirectResponse(request.query_params.get("back") or "/disclosures/pcds", status_code=303)


@router.get("/disclosures/pcds/print", response_class=HTMLResponse)
def pcds_print(s=Depends(get_session)):
    deal = current_deal(s)
    return templates.get_template("disclosures/pcds_print.html").render(
        deal=deal, **_ctx(s, deal), answer_label=pcds.answer_label)
