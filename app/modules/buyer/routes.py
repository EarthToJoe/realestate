"""Steps 8 and 9 of the path (decisions 47 to 51): the buyer signs up (intake and representation, the search, the
tour and both clients' dual-agency consent, merged on /buyer) and the buyer's offer (/buyer/offer). The negotiation
the buyer approves replies in now happens on step 10 (/offers); its buyer-side endpoints stay here.

Information wall on screen (decision 49): the "What each side's AI can see" panel shows both sides next to each
other. The persona is kept for the access log only."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select

from app.audit import log_access, record_event
from app.db import get_session
from app.demo import path, recorded
from app.models import Document, Message
from app.modules.buyer import service
from app.pii import MASKER
from app.records import service as records
from app.web import actor, current_deal, gate_page, persona, redirect, render

router = APIRouter()

CONTACT = ("name", "email", "phone")


def _int(v) -> int | None:
    try:
        return int(str(v).replace(",", "").replace("$", "").strip())
    except (TypeError, ValueError):
        return None


def _money(v) -> str:
    return f"${int(v):,}" if v not in (None, "") else ""


def _messages(s, deal):
    return list(s.execute(select(Message).where(Message.deal_id == deal.id, Message.side == "buyer")
                          .order_by(Message.id)).scalars())


def wall_rows(s, deal) -> list[tuple[str, str, str]]:
    """What each side's AI can see (decision 24, shown side by side for decision 49)."""
    from app.modules.inbox import service as inbox
    from app.modules.offers import service as offers

    ins = service.instructions(s, deal)
    conf = (ins.confidential or {}) if ins else {}
    d = offers.state(deal).get("decision") or {}
    lowest = _money(d.get("lowest_price")) if d.get("decision") == "counter" else "set by the seller on step 10"
    rows = [("The most the buyer would pay", "hidden", _money(conf.get("maximum_price")) or "not given yet"),
            ("The buyer's private notes", "hidden", conf.get("notes") or "none")]
    rows.append(("The lowest price the seller allows", lowest, "hidden"))
    auth = inbox.authority(s, deal)
    rows.append(("What the seller lets the AI agree", "the seller's own instructions" if auth else "not set yet",
                 "hidden"))
    rows.append(("The house's public facts and list price", "seen", "seen"))
    return rows


def saved_input(s, deal) -> dict:
    """The buyer's answers as saved, to re-open the form filled in (decision 48)."""
    ins = service.instructions(s, deal)
    needs = (ins.fact_sheet or {}) if ins else {}
    conf = (ins.confidential or {}) if ins else {}
    b = deal.buyer
    return {"name": (b.legal_name or "") if b else "", "email": (b.email or "") if b else "",
            "phone": (b.phone or "") if b else "", "beds_min": str(needs.get("beds_min", "")),
            "acres_min": str(needs.get("acres_min", "")), "towns": list(needs.get("towns") or []),
            "must_haves": needs.get("must_haves", ""), "preapproved": "yes" if needs.get("preapproved") else "no",
            "preapproval_amount": str(needs.get("preapproval_amount", "") or ""),
            "timeline": needs.get("timeline", ""), "max_price": str(conf.get("maximum_price", "") or ""),
            "private_notes": conf.get("notes", "")}


def _norm(v):
    if isinstance(v, (list, tuple)):
        return sorted(str(x).strip() for x in v)
    s = str(v if v is not None else "").strip().replace(",", "").replace("$", "")
    try:
        f = float(s)
        return str(int(f)) if f == int(f) else str(f)
    except ValueError:
        return s


def needs_of(data: dict) -> dict:
    """The buyer's side of the form that later work uses (everything but the contact details)."""
    return {k: _norm(data.get(k)) for k in service.INTAKE_FIELDS if k not in CONTACT}


def _read(form) -> dict:
    return {k: (form.getlist(k) if k == "towns" else str(form.get(k) or "").strip()) for k in service.INTAKE_FIELDS}


def _errors(data: dict) -> dict:
    """Each missing answer next to its field, saying what to enter (fresh-eyes audit 27)."""
    e = {}
    if not data.get("name"):
        e["name"] = "Enter the buyer's name (a fictional person in this demo)."
    if not data.get("email") or "@" not in data["email"]:
        e["email"] = "Enter an e-mail address, for example sam@example.com."
    if _int(data.get("max_price")) is None:
        e["max_price"] = "Enter the most the buyer would pay, in dollars, for example 665000."
    return e


def _intake_page(request, s, deal, status_code=200, *, form_data=None, errors=None, editing=False):
    agreement = s.execute(select(Document).where(Document.deal_id == deal.id, Document.kind == "buyer_agreement")
                          ).scalar_one_or_none()
    if deal.buyer_id:
        log_access(s, persona=persona(request), person_id=deal.buyer_id, fields=["legal_name", "email", "phone"],
                   purpose="The buyer's answers shown on step 8", route=str(request.url.path))
    show_form = not deal.buyer_id or editing
    crit = service.default_criteria(s, deal) if deal.buyer_id else None
    bstate = service.state(deal)
    return render(request, s, "buyer/intake.html", status_code=status_code,
                  data=form_data or (saved_input(s, deal) if deal.buyer_id else service.demo_input()),
                  errors=errors or {}, show_form=show_form, editing=editing and bool(deal.buyer_id),
                  saved=saved_input(s, deal) if deal.buyer_id else None, towns=service.TOWNS, agreement=agreement,
                  agreement_terms=service.buyer_agreement(), bstate=bstate,
                  matches=service.search(deal, crit) if crit else [], filters=service.SEARCH_FILTERS,
                  msgs=_messages(s, deal), listing=service.firm_listing(deal), wall=wall_rows(s, deal),
                  cp16=records.latest(s, deal.id, "CP-16"), cp17=records.latest(s, deal.id, "CP-17"),
                  cp30=records.latest(s, deal.id, "CP-30"), cp28=records.latest(s, deal.id, "CP-28"),
                  cp10=next((c for c in records.records(s, deal.id, "CP-10") if c.step == 8), None),
                  cp24=[c for c in records.records(s, deal.id, "CP-24") if c.step == 8])


@router.get("/buyer")
def intake(request: Request, edit: int = 0, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    return _intake_page(request, s, deal, editing=bool(edit))


def _update_contact(s, deal, data: dict) -> None:
    b = deal.buyer
    b.legal_name, b.email, b.phone = data["name"], data["email"], data.get("phone") or ""
    for value, label in ((b.legal_name, "[BUYER_1]"), (b.email, "[EMAIL]"), (b.phone, "[PHONE]")):
        MASKER.register(value, label)
    record_event(s, actor="buyer", kind="change", entity="person", entity_id=b.id,
                 summary="The buyer changed their contact details on step 8 (nothing else redone)")
    s.flush()


def _update_needs(s, deal, data: dict) -> None:
    ins = service.instructions(s, deal)
    towns = data.get("towns") or []
    ins.fact_sheet = {"beds_min": int(_int(data.get("beds_min")) or 0),
                      "acres_min": float(str(data.get("acres_min") or 0).replace(",", "") or 0),
                      "towns": list(towns), "must_haves": (data.get("must_haves") or "").strip(),
                      "preapproved": (data.get("preapproved") or "no") == "yes",
                      "preapproval_amount": int(_int(data.get("preapproval_amount")) or 0),
                      "timeline": (data.get("timeline") or "").strip()}
    ins.confidential = {"maximum_price": int(_int(data.get("max_price")) or 0),
                        "notes": (data.get("private_notes") or "").strip()}
    st = service.state(deal)
    st["needs"] = ins.fact_sheet
    service._save(s, deal, st)
    record_event(s, actor="buyer", kind="change", entity="deal", entity_id=deal.id,
                 summary="The buyer changed the home they want or the money on step 8")
    s.flush()


@router.post("/buyer")
async def intake_submit(request: Request, s=Depends(get_session)):
    """Save the buyer's answers. The first time, the AI takes the buyer on as a client; again, contact details are
    updated at once and other answers only after a confirm that names what will be redone (decision 48)."""
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    form = await request.form()
    data = _read(form)
    errors = _errors(data)
    if errors:
        return _intake_page(request, s, deal, status_code=422, form_data=data, errors=errors,
                            editing=bool(deal.buyer_id))
    recorded.check(request, needs_of(data), needs_of(service.demo_input()), back="/buyer?edit=1" if deal.buyer_id
                   else "/buyer", what="answer", label="Put the demo buyer back")
    provider = request.app.state.provider
    if not deal.buyer_id:
        service.start(s, deal, data)
        return redirect("/buyer", path.after_action(s, provider, "Saved. The AI took the buyer on as a client and "
                                                                 "sent the buyer agreement"))
    old = saved_input(s, deal)
    contact = [k for k in CONTACT if _norm(old.get(k)) != _norm(data.get(k))]
    needs = needs_of(old) != needs_of(data)
    if needs and form.get("confirmed") != "yes":
        reopen = path.change_plan(s, deal, "buyer_needs")
        hidden = {}
        for k, v in form.multi_items():
            if k != "confirmed":
                hidden.setdefault(k, []).append(v)
        hidden = {k: (v[0] if len(v) == 1 and k != "towns" else v) for k, v in hidden.items()}
        return render(request, s, "change.html", key="buyer_needs", label="the buyer's answers", reopens=reopen,
                      reopens_text=path.reopens_text(reopen), back="/buyer?edit=1", action="/buyer",
                      hidden={**hidden, "confirmed": "yes"})
    if contact:
        _update_contact(s, deal, data)
    if needs:
        _update_needs(s, deal, data)
        flash = path.apply_change(s, provider, deal, "buyer_needs", why="the buyer changed their answers")
        return redirect("/buyer", path.after_action(s, provider, "Saved. " + flash.rstrip(".")))
    return redirect("/buyer", "Saved." if contact else "Nothing changed.")


@router.post("/buyer/sign")
async def sign(request: Request, s=Depends(get_session)):
    form = await request.form()
    decision = str(form.get("decision") or form.get("choice") or "sign")
    service.sign_agreement(s, current_deal(s), actor(request, form), decision)
    done = "The buyer signed the buyer agreement" if decision == "sign" else "The buyer declined the buyer agreement"
    return redirect("/buyer#rec-CP-16", path.after_action(s, request.app.state.provider, done))


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
    return redirect("/buyer#search", "The buyer's AI saved the search and sent an alert.")


@router.post("/buyer/tour")
async def tour_request(request: Request, s=Depends(get_session)):
    form = await request.form()
    service.request_tour(s, current_deal(s), request.app.state.provider,
                         self_guided=form.get("kind", "self-guided") == "self-guided")
    return redirect("/buyer#tour", "The AI booked a tour.")


@router.post("/buyer/consent")
async def consent(request: Request, s=Depends(get_session)):
    form = await request.form()
    who = actor(request, form)
    decision = str(form.get("decision") or form.get("choice") or "consent")
    service.consent_dual_agency(s, current_deal(s), who, decision)
    done = f"The {who} {'consented to' if decision == 'consent' else 'declined'} dual agency"
    return redirect("/buyer#rec-CP-17", path.after_action(s, request.app.state.provider, done))


# ---- step 9: the buyer's offer ---------------------------------------------------------------------------------

def _offer_cp18(s, deal):
    """The CP-18 for the offer itself (the replies to a counter are their own CP-18s, on step 10)."""
    rs = [c for c in records.records(s, deal.id, "CP-18") if c.attached_to == "buyer:offer"]
    return rs[-1] if rs else None


@router.get("/buyer/offer")
def offer(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None or not deal.buyer_id:
        return gate_page(request, s)
    return render(request, s, "buyer/offer.html", bstate=service.state(deal), cp18=_offer_cp18(s, deal),
                  cp17=records.latest(s, deal.id, "CP-17"),
                  cp31=[c for c in records.records(s, deal.id, "CP-31") if c.attached_to == "buyer:offer"],
                  listing=service.firm_listing(deal), wall=wall_rows(s, deal))


@router.post("/buyer/offer/advise")
def offer_advise(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if not service.state(deal).get("advice"):  # once is enough: the AI may already have done it on its own
        service.advise_offer(s, deal, request.app.state.provider)
    return redirect("/buyer/offer#advice", "The buyer's AI advised and drafted the offer.")


@router.post("/buyer/offer/approve")
async def offer_approve(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    form = await request.form()
    decision = str(form.get("decision") or "approve")
    price = _int(form.get("price"))
    adv = service.state(deal).get("advice") or {}
    if decision == "approve" and price is not None:
        recorded.check(request, {"price": price}, {"price": adv.get("recommended_price")}, back="/buyer/offer")
    terms = service.approve_offer(s, deal, actor(request, form), decision, price=price)
    done = (f"The buyer sent the offer at ${terms['price']:,}" if terms else "The buyer decided not to make the "
            "offer for now")
    return redirect("/buyer/offer", path.after_action(s, request.app.state.provider, done))


@router.post("/buyer/counter/advise")
def counter_advise(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if not service.state(deal).get("counter_advice"):  # the AI may already have advised on this counter
        service.advise_counter(s, deal, request.app.state.provider)
    return redirect("/offers#negotiation", "The buyer's AI advised the buyer on the seller's counter.")


@router.post("/buyer/counter/approve")
async def counter_approve(request: Request, s=Depends(get_session)):
    """The buyer's reply to the seller's counter, from step 10's reply form."""
    deal = current_deal(s)
    form = await request.form()
    decision = str(form.get("decision") or "approve")
    price = _int(form.get("price"))
    ca = service.state(deal).get("counter_advice") or {}
    if decision == "approve" and price is not None:
        recorded.check(request, {"price": price}, {"price": ca.get("price")}, back="/offers#negotiation")
    reply = service.approve_reply(s, deal, actor(request, form), decision, price=price)
    done = "The buyer approved the reply" if reply else "The buyer turned down the drafted reply"
    return redirect("/offers#negotiation", path.after_action(s, request.app.state.provider, done))


@router.get("/buyer/offer/{rest:path}")
@router.get("/buyer/counter/{rest:path}")
def back_to_screen(rest: str, request: Request):
    """A refresh or Back after one of the forms above lands on its screen (fresh-eyes audit 5)."""
    return RedirectResponse("/offers#negotiation" if request.url.path.startswith("/buyer/counter") else "/buyer/offer",
                            status_code=303)
