"""Step 7 Contract screens: memorandum, the AI's draft and rider with the CP-14 marker, the code checks, the
side-by-side, the disclosures attached, the signing map, simulated signing (CP-33), and the PDF and DOCX."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, Response

from app.audit import log_access
from app.db import get_session
from app.disclosures import pcds
from app.modules.contract import documents, service
from app.records import service as records
from app.records.service import GateError
from app.web import current_deal, gate_page, persona, render

router = APIRouter()


@router.get("/contract")
def contract(request: Request, s=Depends(get_session)):
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
    return render(request, s, "contract/contract.html", gate=gate, memo=memo, st=st, label=service.LABEL,
                  names=names, fill=service.fill,
                  rows=service.side_by_side(st["draft"]) if st.get("draft") else [],
                  disclosures=service.disclosures(s, deal) if not gate else [], signing_map=service.SIGNING_MAP,
                  standard_source=service.STANDARD_SOURCE, cp14=records.latest(s, deal.id, "CP-14"),
                  cp15=records.latest(s, deal.id, "CP-15"), cp32=records.records(s, deal.id, "CP-32"),
                  cp33=records.latest(s, deal.id, "CP-33"), cp04=records.latest(s, deal.id, "CP-04"),
                  refused=request.query_params.get("refused"))


@router.post("/contract/memorandum")
def memorandum(request: Request, s=Depends(get_session)):
    service.send_memorandum(s, current_deal(s))
    return RedirectResponse("/contract#memorandum", status_code=303)


@router.post("/contract/draft")
def draft(request: Request, s=Depends(get_session)):
    service.draft(s, current_deal(s), request.app.state.provider)
    return RedirectResponse("/contract#draft", status_code=303)


@router.post("/contract/attach")
def attach(request: Request, s=Depends(get_session)):
    service.attach_disclosures(s, current_deal(s))
    return RedirectResponse("/contract#disclosures", status_code=303)


@router.post("/contract/open-signing")
def open_signing(request: Request, s=Depends(get_session)):
    service.open_signing(s, current_deal(s))
    return RedirectResponse("/contract#rec-CP-33", status_code=303)


@router.post("/contract/sign")
async def sign(request: Request, s=Depends(get_session)):
    form = await request.form()
    service.sign(s, current_deal(s), persona(request), str(form.get("decision", "sign")))
    return RedirectResponse("/contract#rec-CP-33", status_code=303)


def _rendered(request: Request, s, purpose: str):
    deal = current_deal(s)
    st = service.state(deal)
    if not st.get("draft"):
        raise ValueError("The contract has not been drafted yet.")
    mapping = service.names(deal)
    for pid in (deal.seller_id, deal.buyer_id):
        if pid:
            log_access(s, persona=persona(request), person_id=pid, fields=["legal_name"], purpose=purpose,
                       route=str(request.url.path))
    answers = pcds.answers_of(s, deal) if records.is_done(s, deal.id, "CP-04") else None
    return deal, st, mapping, answers


@router.get("/contract/print")
def print_view(request: Request, s=Depends(get_session)):
    deal, st, mapping, answers = _rendered(request, s, "Contract print view with the parties' names")
    return Response(documents.contract_html(deal, st, mapping, answers), media_type="text/html")


@router.get("/contract/draft.pdf")
def pdf(request: Request, s=Depends(get_session)):
    deal, st, mapping, answers = _rendered(request, s, "Contract PDF with the parties' names")
    data = documents.contract_pdf(documents.contract_html(deal, st, mapping, answers))
    return Response(data, media_type="application/pdf",
                    headers={"Content-Disposition": f'inline; filename="contract-draft-v{st["version"]}.pdf"'})


@router.get("/contract/draft.docx")
def docx(request: Request, s=Depends(get_session)):
    deal, st, mapping, _ = _rendered(request, s, "Contract DOCX with the parties' names")
    data = documents.contract_docx(deal, st, mapping)
    return Response(data, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    headers={"Content-Disposition": f'attachment; filename="contract-draft-v{st["version"]}.docx"'})
