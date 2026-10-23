"""Step 1 Intake screens: address and facts, property profile, disclosure checklist, seller onboarding."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select

from app.audit import log_access
from app.db import get_session
from app.disclosures import pcds
from app.model.provider import ReplayMiss, SpendCapReached
from app.models import Disclosure, Document
from app.modules.intake import service
from app.records import service as records
from app.web import current_deal, persona, render

router = APIRouter()


def _deal_or_redirect(s):
    deal = current_deal(s)
    return deal, (None if deal else RedirectResponse("/intake", status_code=303))


@router.get("/intake")
def intake_form(request: Request, demo: int = 0, s=Depends(get_session)):
    data = service.demo_input() if demo else None
    return render(request, s, "intake/form.html", data=data, seller_fields=service.SELLER_FIELDS,
                  section_242=service.SECTION_242)


@router.post("/intake")
async def intake_submit(request: Request, s=Depends(get_session)):
    form = await request.form()
    facts = {k: str(form.get(k, "")) for k in list(service.SELLER_FIELDS) + list(service.SECTION_242)}
    data = service.IntakeInput(street=str(form.get("street", "")).strip(), city=str(form.get("city", "")).strip(),
                               zip=str(form.get("zip", "")).strip(), seller_name=str(form.get("seller_name", "")),
                               seller_email=str(form.get("seller_email", "")),
                               seller_phone=str(form.get("seller_phone", "")), facts=facts)
    if not data.street or not data.city:
        return render(request, s, "intake/form.html", status_code=422, data=data, error="Street and town are needed.",
                      seller_fields=service.SELLER_FIELDS, section_242=service.SECTION_242)
    service.start_intake(s, data)
    return RedirectResponse("/intake/profile", status_code=303)


@router.get("/intake/profile")
def profile(request: Request, s=Depends(get_session)):
    deal, redirect = _deal_or_redirect(s)
    if redirect:
        return redirect
    inferred = [f for f in deal.property.facts if f.group == "Inferred by the AI"]
    return render(request, s, "intake/profile.html", groups=service.profile_groups(deal), inferred=inferred)


@router.post("/intake/infer")
def infer(request: Request, s=Depends(get_session)):
    """The AI act: fill gaps. Returns the profile fragment (htmx) or redirects."""
    deal, redirect = _deal_or_redirect(s)
    if redirect:
        return redirect
    result, error = None, None
    try:
        result = service.infer_gaps(s, deal, request.app.state.provider)
    except (ReplayMiss, SpendCapReached) as e:
        error = str(e)
    tpl = "intake/_profile_body.html" if request.headers.get("HX-Request") else "intake/profile.html"
    inferred = [f for f in deal.property.facts if f.group == "Inferred by the AI"]
    return render(request, s, tpl, groups=service.profile_groups(deal), inferred=inferred, result=result,
                  ai_error=error)


@router.get("/intake/disclosures")
def disclosures(request: Request, s=Depends(get_session)):
    deal, redirect = _deal_or_redirect(s)
    if redirect:
        return redirect
    items = s.execute(select(Disclosure).where(Disclosure.deal_id == deal.id).order_by(Disclosure.id)).scalars().all()
    return render(request, s, "intake/disclosures.html", items=items, cp04=records.latest(s, deal.id, "CP-04"),
                  questions=len(pcds.questions()))


@router.get("/intake/onboarding")
def onboarding(request: Request, s=Depends(get_session)):
    deal, redirect = _deal_or_redirect(s)
    if redirect:
        return redirect
    notices = s.execute(select(Disclosure).where(
        Disclosure.deal_id == deal.id, Disclosure.kind.in_(("agency", "fair_housing", "not_legal_services")))
    ).scalars().all()
    agreement = s.execute(select(Document).where(Document.deal_id == deal.id,
                                                 Document.kind == "listing_agreement")).scalar_one_or_none()
    seller = deal.seller
    if agreement and seller:  # the agreement shows the seller's name: log the access (spec section 6)
        log_access(s, persona=persona(request), person_id=seller.id, fields=["legal_name"],
                   purpose="Listing agreement shown on the onboarding screen", route=str(request.url.path))
    return render(request, s, "intake/onboarding.html", notices=notices, agreement=agreement, seller=seller,
                  cp01=records.latest(s, deal.id, "CP-01"), cp02=records.latest(s, deal.id, "CP-02"),
                  cp03=records.latest(s, deal.id, "CP-03"), cp24=records.records(s, deal.id, "CP-24"),
                  conflicts=service.conflicts_check(s, deal), presentation=service.presentation())


@router.post("/intake/agency")
async def agency(request: Request, s=Depends(get_session)):
    deal, redirect = _deal_or_redirect(s)
    if redirect:
        return redirect
    form = await request.form()
    service.acknowledge_agency(s, deal, persona(request), str(form.get("decision", "acknowledge")))
    return RedirectResponse("/intake/onboarding", status_code=303)


@router.post("/intake/accept")
def accept(request: Request, s=Depends(get_session)):
    deal, redirect = _deal_or_redirect(s)
    if redirect:
        return redirect
    service.accept_listing(s, deal)
    return RedirectResponse("/intake/onboarding#agreement", status_code=303)


@router.post("/intake/sign")
async def sign(request: Request, s=Depends(get_session)):
    deal, redirect = _deal_or_redirect(s)
    if redirect:
        return redirect
    form = await request.form()
    service.sign_listing_agreement(s, deal, persona(request), str(form.get("decision", "sign")))
    return RedirectResponse("/intake/onboarding#agreement", status_code=303)
