"""Step 10 of the path, the seller decides: the offers compared with what the seller keeps, the seller's AI's advice
(CP-11), the seller's decision (CP-12) with its price and terms, and the negotiation (CP-13), where the buyer
approves each reply (decisions 47 to 51). The buyer's reply posts to /buyer/counter/approve (the buyer's side)."""

from __future__ import annotations

import re

from fastapi import APIRouter, Depends, Request

from app.db import get_session
from app.demo import path, recorded, walk
from app.modules.offers import service
from app.records import service as records
from app.records.service import GateError, NotYourDecision
from app.web import actor, current_deal, gate_page, presenting, redirect, render

router = APIRouter()


def _int(v) -> int | None:
    try:
        return int(str(v).replace(",", "").replace("$", "").strip())
    except (TypeError, ValueError):
        return None


def first_sentence(text: str | None) -> str:
    """The recorded advice's own first sentence (never a reason the AI did not give)."""
    t = (text or "").strip()
    m = re.match(r"(.+?[.!?])(\s|$)", t)
    return m.group(1) if m else t


def _wall(s, deal, st) -> list[tuple[str, str, str]]:
    from app.modules.buyer import service as buyer

    ins = buyer.instructions(s, deal)
    ceiling = ((ins.confidential or {}).get("maximum_price") if ins else None)
    d = st.get("decision") or {}
    lowest = d.get("lowest_price")
    money = (lambda v: f"${int(v):,}" if v else "")
    return [
        ("The buyer's most they would pay", "hidden", money(ceiling) or "not given"),
        ("The lowest price the seller lets the AI agree", money(lowest) or "set when the seller decides", "hidden"),
        ("Offer A, from another firm's buyer", "seen", "hidden (another firm's client)"),
        ("Offer B and each counter, as sent", "seen", "seen"),
    ]


@router.get("/offers")
def offers(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    gate, table = None, []
    try:
        table = service.compare(s, deal)
    except GateError as e:
        gate = e.message
    st = service.state(deal)
    adv = st.get("advice") or {}
    advised = {v["label"]: v for v in adv.get("offers") or []}
    why = None
    if st.get("accepted"):
        why = first_sentence((advised.get(st["accepted"]["label"]) or {}).get("advice")) or \
            first_sentence(adv.get("recommendation"))
    from app.modules.buyer import service as buyer

    bst = buyer.state(deal)
    return render(request, s, "offers/offers.html", gate=gate, offers=table, st=st, why=why,
                  rec_first=first_sentence(adv.get("recommendation")), advised=advised,
                  cp11=records.latest(s, deal.id, "CP-11"), cp12=records.latest(s, deal.id, "CP-12"),
                  cp13=[c for c in records.records(s, deal.id, "CP-13") if c.attached_to == "offers:seller"],
                  cp18=records.latest(s, deal.id, "CP-18"), bst=bst, nxt=walk.negotiation_next(s, deal),
                  not_binding=service.NOT_BINDING.replace(" (L24)", ""), rd=walk.recorded_decision(deal),
                  defaults=service.DECISION_DEFAULTS, terms_text=service.terms_text, wall_rows=_wall(s, deal, st),
                  not_ready=request.query_params.get("not_ready"))


@router.post("/offers/advise")
def advise(request: Request, s=Depends(get_session)):
    try:
        service.advise(s, current_deal(s), request.app.state.provider)
    except service.NotReady as e:
        return redirect("/offers#advice", e.message)
    return redirect("/offers", path.after_action(s, request.app.state.provider,
                                                 "The seller's AI presented both offers"))


@router.post("/offers/decide")
async def decide(request: Request, s=Depends(get_session)):
    form = await request.form()
    deal = current_deal(s)
    decision = str(form.get("decision", ""))
    label = str(form.get("offer", "A"))
    if decision == "counter":
        rd = walk.recorded_decision(deal)
        given = {k: form.get(k) for k in ("counter_price", "lowest_price", "closing_days", "closing_min",
                                          "closing_max", "inspection_max", "mortgage_max")}
        given.update(offer=label, allow_requests="yes" if form.get("allow_requests") == "yes" else "no")
        figures = {k: rd[k] for k in ("counter_price", "lowest_price", "closing_days", "closing_min", "closing_max",
                                      "inspection_max", "mortgage_max")}
        figures.update(offer=rd["offer_label"], allow_requests="yes" if rd["allow_requests"] else "no")
        recorded.check(request, given, figures, back="/offers#rec-CP-12")
    service.decide(s, deal, actor(request, form), decision=decision, offer_label=label,
                   counter_price=_int(form.get("counter_price")), lowest_price=_int(form.get("lowest_price")),
                   closing_days=_int(form.get("closing_days")), closing_min=_int(form.get("closing_min")),
                   closing_max=_int(form.get("closing_max")), inspection_max=_int(form.get("inspection_max")),
                   mortgage_max=_int(form.get("mortgage_max")), allow_requests=form.get("allow_requests") == "yes")
    done = {"counter": f"The seller countered offer {label} at ${_int(form.get('counter_price')) or 0:,}",
            "accept": f"The seller accepted offer {label} as offered",
            "reject": f"The seller rejected offer {label}"}.get(decision, "The seller decided")
    return redirect("/offers", path.after_action(s, request.app.state.provider, done))


@router.post("/offers/negotiate")
def negotiate(request: Request, s=Depends(get_session)):
    """The seller's AI takes its next step within the seller's decision."""
    service.negotiate(s, current_deal(s))
    return redirect("/offers#negotiation", path.after_action(s, request.app.state.provider,
                                                             "The seller's AI took its next step"))


@router.post("/offers/counter")
async def counter(request: Request, s=Depends(get_session)):
    """Presenter's tool: try sending a counter by hand; code refuses one outside the seller's decision."""
    if not presenting(request):
        raise NotYourDecision("Trying a counter by hand is one of the presenter's tools: turn on \"I'm presenting\" "
                              "in the menu first. The AI negotiates on its own.")
    form = await request.form()
    deal = current_deal(s)
    terms = {**service.counter_terms(deal), "price": _int(form.get("price")) or 0}
    for k in ("closing_days", "inspection_days", "mortgage_days", "seller_credit"):
        if _int(form.get(k)) is not None:
            terms[k] = _int(form.get(k))
    try:
        service.check_counter(deal, terms)
    except service.CounterRefused as e:
        return render(request, s, "refused.html", status_code=409, title="Refused: outside the seller's decision",
                      message=e.message, back="/offers#negotiation", back_title="The seller decides")
    service.send_counter(s, deal, terms)
    return redirect("/offers#negotiation", "The counter was sent by hand, inside the seller's decision.")


@router.post("/offers/consent")
async def consent(request: Request, s=Depends(get_session)):
    """CP-17 from the seller's side (the buyer's consent is on step 8)."""
    from app.modules.buyer import service as buyer

    form = await request.form()
    buyer.consent_dual_agency(s, current_deal(s), actor(request, form), str(form.get("decision", "consent")))
    return redirect("/offers", "Consent recorded.")
