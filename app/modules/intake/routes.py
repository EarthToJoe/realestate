"""Steps 1 to 3 of the path: the seller signs up (the form), the AI researches the house (the profile and the
disclosure checklist, merged), the seller hires the firm (onboarding). Decisions 47 to 51."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select

from app.audit import log_access
from app.db import get_session
from app.demo import path, recorded
from app.disclosures import pcds
from app.models import Disclosure, Document
from app.modules.intake import service
from app.records import service as records
from app.web import actor, current_deal, gate_page, persona, redirect, render

router = APIRouter()

NEXT = "/intake/profile"


def _deal_or_redirect(s):
    deal = current_deal(s)
    return deal, (None if deal else RedirectResponse("/intake", status_code=303))


def _form_page(request, s, data, status_code=200, errors=None, **extra):
    return render(request, s, "intake/form.html", status_code=status_code, data=data, errors=errors or {},
                  seller_fields=service.SELLER_FIELDS, section_242=service.SECTION_242, **extra)


@router.get("/intake")
def intake_form(request: Request, demo: int = 0, s=Depends(get_session)):
    """The form re-opens filled in with what was saved; a new sale opens with the demo house (decision 50)."""
    deal = current_deal(s)
    if deal is not None and not demo:
        data = service.saved_input(s, deal)
        if deal.seller:  # the form shows the seller's details: log the access (spec section 6)
            log_access(s, persona=persona(request), person_id=deal.seller.id, fields=["legal_name", "email", "phone"],
                       purpose="Step 1 re-opened with the seller's saved details", route=str(request.url.path))
    else:
        data = service.demo_input()
        if deal is not None:  # "Put the demo house back": the demo house, with the seller's own saved details
            saved = service.saved_input(s, deal)
            data.seller_name, data.seller_email, data.seller_phone = (saved.seller_name, saved.seller_email,
                                                                      saved.seller_phone)
    return _form_page(request, s, data)


def _read(form) -> service.IntakeInput:
    facts = {k: str(form.get(k, "")).strip() for k in list(service.SELLER_FIELDS) + list(service.SECTION_242)}
    return service.IntakeInput(street=str(form.get("street", "")).strip(), city=str(form.get("city", "")).strip(),
                               zip=str(form.get("zip", "")).strip(), seller_name=str(form.get("seller_name", "")).strip(),
                               seller_email=str(form.get("seller_email", "")).strip(),
                               seller_phone=str(form.get("seller_phone", "")).strip(), facts=facts)


def _errors(data: service.IntakeInput) -> dict:
    """Each missing field, next to the field, saying what to enter (fresh-eyes audit 27)."""
    e = {}
    if not data.street:
        e["street"] = "Enter the street address, for example 146 Route 292."
    if not data.city:
        e["city"] = "Enter the town, for example Holmes."
    if data.zip and not (data.zip.isdigit() and len(data.zip) == 5):
        e["zip"] = "Enter a five-digit ZIP code, or leave it blank."
    if not data.seller_name:
        e["seller_name"] = "Enter the seller's name (a fictional person in this demo)."
    return e


@router.post("/intake")
async def intake_submit(request: Request, s=Depends(get_session)):
    """Save and continue. The first time, the sale starts; again, the same house and the same deal are updated:
    contact details at once, the house only after a confirm that names what will be redone (decision 48)."""
    form = await request.form()
    data = _read(form)
    errors = _errors(data)
    if errors:
        return _form_page(request, s, data, status_code=422, errors=errors)
    demo = service.demo_input()
    recorded.check(request, service.house_of(data), service.house_of(demo), back="/intake?demo=1", what="house",
                   label="Put the demo house back")
    provider = request.app.state.provider
    deal = current_deal(s)
    if deal is None:
        service.start_intake(s, data)
        return redirect(NEXT, path.after_action(s, provider, "Saved. The AI found the house in the public record "
                                                            "and sent the seller three notices"))
    ch = service.changes(service.saved_input(s, deal), data)
    if ch["house"] and form.get("confirmed") != "yes":
        reopen = path.change_plan(s, deal, "house")
        hidden = {k: v for k, v in form.multi_items() if k != "confirmed"}
        return render(request, s, "change.html", key="house", label="the house's address and facts",
                      reopens=reopen, reopens_text=path.reopens_text(reopen), back="/intake", action="/intake",
                      hidden={**hidden, "confirmed": "yes"})
    if ch["contact"]:
        service.update_contact(s, deal, data)
    if ch["house"]:
        service.update_house(s, deal, data)
        flash = path.apply_change(s, provider, deal, "house", why="the seller changed the house's address or facts")
        return redirect(NEXT, path.after_action(s, provider, "Saved. " + flash.rstrip(".")))
    return redirect(NEXT, "Saved." if ch["contact"] else None)


@router.get("/intake/profile")
def profile(request: Request, s=Depends(get_session)):
    """Step 2: the AI's research: every fact with where it came from, and the disclosures this house needs."""
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    inferred = [f for f in deal.property.facts if f.group == "Inferred by the AI"]
    items = s.execute(select(Disclosure).where(Disclosure.deal_id == deal.id).order_by(Disclosure.id)).scalars().all()
    return render(request, s, "intake/profile.html", groups=service.profile_groups(deal), inferred=inferred,
                  items=[d for d in items if not d.kind.startswith("buyer_")], questions=len(pcds.questions()))


@router.post("/intake/infer")
def infer(request: Request, s=Depends(get_session)):
    """The AI act: fill gaps (the action bar's button when the AI has not done it on its own)."""
    deal, gone = _deal_or_redirect(s)
    if gone:
        return gone
    service.infer_gaps(s, deal, request.app.state.provider)
    return redirect("/intake/profile", "The AI filled the gaps it could.")


@router.get("/intake/onboarding")
def onboarding(request: Request, s=Depends(get_session)):
    """Step 3: the seller hires the firm."""
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
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
                  cp03=records.latest(s, deal.id, "CP-03"), cp24=[c for c in records.records(s, deal.id, "CP-24")
                                                                 if c.step == 1],
                  conflicts=service.conflicts_check(s, deal), presentation=service.presentation())


@router.post("/intake/agency")
async def agency(request: Request, s=Depends(get_session)):
    deal, gone = _deal_or_redirect(s)
    if gone:
        return gone
    form = await request.form()
    service.acknowledge_agency(s, deal, actor(request, form), str(form.get("decision", "acknowledge")))
    return redirect("/intake/onboarding", "The seller acknowledged the agency form.")


@router.post("/intake/accept")
def accept(request: Request, s=Depends(get_session)):
    deal, gone = _deal_or_redirect(s)
    if gone:
        return gone
    service.accept_listing(s, deal)
    return redirect("/intake/onboarding#agreement", "The AI accepted the listing.")


@router.post("/intake/sign")
async def sign(request: Request, s=Depends(get_session)):
    deal, gone = _deal_or_redirect(s)
    if gone:
        return gone
    form = await request.form()
    service.sign_listing_agreement(s, deal, actor(request, form), str(form.get("decision", "sign")))
    return redirect("/intake/onboarding#agreement", "The seller signed the listing agreement.")
