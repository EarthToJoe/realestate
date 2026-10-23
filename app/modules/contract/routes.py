"""Step 11 of the path, the contract: the memorandum, the AI's draft and rider with the CP-14 marker, the code checks,
the side by side, the seller's disclosure form (merged here, CP-04), the disclosures attached, the signing map,
simulated signing (CP-33), and the PDF and DOCX (decisions 47 to 51)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response

from app.audit import log_access
from app.db import get_session
from app.demo import path
from app.disclosures import pcds
from app.modules.contract import documents, service
from app.records import service as records
from app.records.service import GateError
from app.web import actor, current_deal, gate_page, persona, redirect, render

router = APIRouter()


def pcds_ctx(s, deal) -> dict:
    """What the merged disclosure form needs (the seller's own form, CP-04)."""
    return dict(form=pcds.form(), questions=pcds.questions, fields=pcds.fields, labels=pcds.CHOICE_LABELS,
                cp04=records.latest(s, deal.id, "CP-04"), saved=pcds.answers_of(s, deal), demo_note=pcds.DEMO_NOTE)


@router.get("/contract")
def contract(request: Request, s=Depends(get_session)):
    return contract_page(request, s)


def contract_page(request: Request, s, status_code: int = 200, **over):
    """The contract screen; `over` replaces parts of its context (the disclosure form's answers and errors)."""
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    gate, memo = None, None
    try:
        memo = service.memorandum(deal)
    except GateError as e:
        gate = e.message
    st = service.state(deal)
    # The screen shows the parties' fictional names (UI audit 2026-10-23); masking stays for model calls and logs.
    # Showing them is a read of personal data, so it is access-logged like the PDF and DOCX.
    names = service.names(deal) if memo or st.get("draft") else {}
    for pid in (deal.seller_id, deal.buyer_id) if names else ():
        if pid:
            log_access(s, persona=persona(request), person_id=pid, fields=["legal_name"],
                       purpose="Contract screen with the parties' names", route=str(request.url.path))
    if st.get("draft") and request.app.state.provider.mode != "fake":  # build the PDF in the background now, so opening it never waits on WeasyPrint
        answers = pcds.answers_of(s, deal) if records.is_done(s, deal.id, "CP-04") else None
        documents.warm(documents.contract_html(deal, st, names, answers))
    extra = request.query_params
    ctx = dict(answers={}, pcds_errors=None, pcds_q_errors={}, refused=extra.get("refused"), **pcds_ctx(s, deal))
    ctx.update(over)
    return render(request, s, "contract/contract.html", status_code=status_code, gate=gate, memo=memo, st=st,
                  label=service.LABEL.replace(" (L21, L22)", ""), names=names, fill=service.fill,
                  rows=service.side_by_side(st["draft"]) if st.get("draft") else [],
                  disclosures=service.disclosures(s, deal) if not gate else [], signing_map=service.SIGNING_MAP,
                  standard_source=service.STANDARD_SOURCE, cp14=records.latest(s, deal.id, "CP-14"),
                  cp15=records.latest(s, deal.id, "CP-15"), cp32=records.records(s, deal.id, "CP-32"),
                  cp33=records.latest(s, deal.id, "CP-33"), **ctx)


@router.post("/contract/memorandum")
def memorandum(request: Request, s=Depends(get_session)):
    service.send_memorandum(s, current_deal(s))
    return redirect("/contract#memorandum", "The AI sent the accepted-offer memorandum to both parties.")


@router.post("/contract/draft")
def draft(request: Request, s=Depends(get_session)):
    service.draft(s, current_deal(s), request.app.state.provider)
    return redirect("/contract", path.after_action(s, request.app.state.provider, "The AI drafted the contract"))


@router.post("/contract/attach")
def attach(request: Request, s=Depends(get_session)):
    service.attach_disclosures(s, current_deal(s))
    return redirect("/contract#disclosures", path.after_action(s, request.app.state.provider,
                                                                "The AI attached the disclosures"))


@router.post("/contract/open-signing")
def open_signing(request: Request, s=Depends(get_session)):
    service.open_signing(s, current_deal(s))
    return redirect("/contract#rec-CP-33", "The contract is open for signing.")


@router.post("/contract/sign")
async def sign(request: Request, s=Depends(get_session)):
    form = await request.form()
    who = actor(request, form)
    choice = str(form.get("decision", "sign"))
    service.sign(s, current_deal(s), who, choice)
    return redirect("/contract#rec-CP-33", f"The {who} {'signed the contract' if choice == 'sign' else 'declined to sign'}.")


def _rendered(request: Request, s, purpose: str):
    """The deal, the draft and the names for a document, or None when there is no sale or no draft yet."""
    deal = current_deal(s)
    if deal is None:
        return None
    st = service.state(deal)
    if not st.get("draft"):
        return None
    mapping = service.names(deal)
    for pid in (deal.seller_id, deal.buyer_id):
        if pid:
            log_access(s, persona=persona(request), person_id=pid, fields=["legal_name"], purpose=purpose,
                       route=str(request.url.path))
    answers = pcds.answers_of(s, deal) if records.is_done(s, deal.id, "CP-04") else None
    return deal, st, mapping, answers


def _not_yet(request: Request, s):
    """No sale, or no draft yet: the contract screen's "not yet" card, never a server error."""
    if current_deal(s) is None:  # the contract screen's own "not yet" card says what comes first
        return redirect("/contract")
    return redirect("/contract", "There is no contract draft yet: the AI drafts it once the price is agreed.")


@router.get("/contract/print")
def print_view(request: Request, s=Depends(get_session)):
    got = _rendered(request, s, "Contract print view with the parties' names")
    if got is None:
        return _not_yet(request, s)
    deal, st, mapping, answers = got
    return Response(documents.contract_html(deal, st, mapping, answers), media_type="text/html")


@router.get("/contract/draft.pdf")
def pdf(request: Request, s=Depends(get_session)):
    got = _rendered(request, s, "Contract PDF with the parties' names")
    if got is None:
        return _not_yet(request, s)
    deal, st, mapping, answers = got
    data = documents.contract_pdf(documents.contract_html(deal, st, mapping, answers))
    return Response(data, media_type="application/pdf",
                    headers={"Content-Disposition": f'inline; filename="contract-draft-v{st["version"]}.pdf"'})


@router.get("/contract/draft.docx")
def docx(request: Request, s=Depends(get_session)):
    got = _rendered(request, s, "Contract DOCX with the parties' names")
    if got is None:
        return _not_yet(request, s)
    deal, st, mapping, _ = got
    data = documents.contract_docx(deal, st, mapping)
    return Response(data, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    headers={"Content-Disposition": f'attachment; filename="contract-draft-v{st["version"]}.docx"'})
