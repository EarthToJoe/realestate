"""Step 8 Buyer side screens: intake and representation (CP-30, CP-24, CP-16), search alerts, tour request
(CP-16 gate, CP-17, CP-28 / CP-10, CP-29), and offer advice, draft and approval (CP-31, CP-18, CP-13 buyer side).

Information wall on screen: the buyer's private limits show only to the buyer and the Presenter; the seller persona
sees that they are hidden."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select

from app.audit import log_access
from app.db import get_session
from app.models import Document, Message
from app.modules.buyer import service
from app.records import service as records
from app.web import current_deal, persona, render

router = APIRouter()


def _int(v) -> int | None:
    try:
        return int(str(v).replace(",", "").replace("$", "").strip())
    except (TypeError, ValueError):
        return None


def _base(request, s, deal):
    ins = service.instructions(s, deal)
    see_private = persona(request) in ("buyer", "presenter")
    return {"bstate": service.state(deal), "needs": (ins.fact_sheet if ins else None) or {},
            "private": (ins.confidential if ins and see_private else None), "see_private": see_private,
            "has_buyer": bool(deal.buyer_id), "cp16": records.latest(s, deal.id, "CP-16"),
            "cp17": records.latest(s, deal.id, "CP-17"), "cp30": records.latest(s, deal.id, "CP-30")}


def _messages(s, deal):
    return list(s.execute(select(Message).where(Message.deal_id == deal.id, Message.side == "buyer")
                          .order_by(Message.id)).scalars())


@router.get("/buyer")
def intake(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return RedirectResponse("/intake", status_code=303)
    base = _base(request, s, deal)
    if deal.buyer_id and persona(request) in ("buyer", "presenter"):
        log_access(s, persona=persona(request), person_id=deal.buyer_id, fields=["legal_name"],
                   purpose="Buyer agreement shown on the buyer intake screen", route=str(request.url.path))
    agreement = s.execute(select(Document).where(Document.deal_id == deal.id, Document.kind == "buyer_agreement")
                          ).scalar_one_or_none()
    return render(request, s, "buyer/intake.html", demo=service.demo_input() if request.query_params.get("demo")
                  else None, towns=service.TOWNS, agreement=agreement, agreement_terms=service.buyer_agreement(),
                  buyer=deal.buyer if base["see_private"] else None,
                  cp24=[c for c in records.records(s, deal.id, "CP-24") if "buyer" in (c.reason or "")],
                  error=None, **base)


@router.post("/buyer")
async def intake_submit(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    form = await request.form()
    data = {k: (form.getlist(k) if k == "towns" else form.get(k)) for k in service.INTAKE_FIELDS}
    try:
        service.start(s, deal, data)
    except ValueError as e:
        return render(request, s, "buyer/intake.html", status_code=422, demo=data, towns=service.TOWNS,
                      agreement=None, agreement_terms=service.buyer_agreement(), buyer=None, cp24=[],
                      error=str(e), **_base(request, s, deal))
    return RedirectResponse("/buyer#rec-CP-16", status_code=303)


@router.post("/buyer/sign")
async def sign(request: Request, s=Depends(get_session)):
    form = await request.form()
    service.sign_agreement(s, current_deal(s), persona(request), str(form.get("decision", "sign")))
    return RedirectResponse("/buyer#rec-CP-16", status_code=303)


@router.get("/buyer/search")
def search(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None or not deal.buyer_id:
        return RedirectResponse("/buyer", status_code=303)
    base = _base(request, s, deal)
    crit = service.default_criteria(s, deal)
    if not base["see_private"]:
        crit = {**crit, "max_price": None}
    return render(request, s, "buyer/search.html", criteria=crit, matches=service.search(
        deal, {**crit, "max_price": crit["max_price"] or 10**9}), towns=service.TOWNS, msgs=_messages(s, deal),
                  filters=service.SEARCH_FILTERS, **base)


@router.post("/buyer/alert")
async def alert(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    form = await request.form()
    crit = service.default_criteria(s, deal)
    for k in ("max_price", "beds_min"):
        if _int(form.get(k)) is not None:
            crit[k] = _int(form.get(k))
    if form.get("acres_min"):
        crit["acres_min"] = float(form.get("acres_min"))
    if form.getlist("towns"):
        crit["towns"] = form.getlist("towns")
    service.send_alert(s, deal, request.app.state.provider, crit)
    return RedirectResponse("/buyer/search#alerts", status_code=303)


@router.get("/buyer/tour")
def tour(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None or not deal.buyer_id:
        return RedirectResponse("/buyer", status_code=303)
    return render(request, s, "buyer/tour.html", listing=service.firm_listing(deal), msgs=_messages(s, deal),
                  cp28=records.latest(s, deal.id, "CP-28"), cp10=records.latest(s, deal.id, "CP-10"),
                  **_base(request, s, deal))


@router.post("/buyer/tour")
async def tour_request(request: Request, s=Depends(get_session)):
    form = await request.form()
    service.request_tour(s, current_deal(s), request.app.state.provider,
                         self_guided=form.get("kind", "self-guided") == "self-guided")
    return RedirectResponse("/buyer/tour#booked", status_code=303)


@router.post("/buyer/consent")
async def consent(request: Request, s=Depends(get_session)):
    form = await request.form()
    service.consent_dual_agency(s, current_deal(s), persona(request), str(form.get("decision", "consent")))
    return RedirectResponse("/buyer/tour#rec-CP-17", status_code=303)


@router.get("/buyer/offer")
def offer(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None or not deal.buyer_id:
        return RedirectResponse("/buyer", status_code=303)
    cp18s = records.records(s, deal.id, "CP-18")
    return render(request, s, "buyer/offer.html", cp18=cp18s[-1] if cp18s else None, cp18s=cp18s,
                  cp31=records.records(s, deal.id, "CP-31"),
                  cp13=[c for c in records.records(s, deal.id, "CP-13") if c.attached_to == "offers:buyer"],
                  listing=service.firm_listing(deal), **_base(request, s, deal))


@router.post("/buyer/offer/advise")
def offer_advise(request: Request, s=Depends(get_session)):
    service.advise_offer(s, current_deal(s), request.app.state.provider)
    return RedirectResponse("/buyer/offer#advice", status_code=303)


@router.post("/buyer/offer/approve")
async def offer_approve(request: Request, s=Depends(get_session)):
    form = await request.form()
    service.approve_offer(s, current_deal(s), persona(request), str(form.get("decision", "approve")),
                          price=_int(form.get("price")))
    return RedirectResponse("/buyer/offer#rec-CP-18", status_code=303)


@router.post("/buyer/counter/advise")
def counter_advise(request: Request, s=Depends(get_session)):
    service.advise_counter(s, current_deal(s), request.app.state.provider)
    return RedirectResponse("/buyer/offer#counter", status_code=303)


@router.post("/buyer/counter/approve")
async def counter_approve(request: Request, s=Depends(get_session)):
    form = await request.form()
    service.approve_reply(s, current_deal(s), persona(request), str(form.get("decision", "approve")),
                          price=_int(form.get("price")))
    return RedirectResponse("/buyer/offer#counter", status_code=303)
