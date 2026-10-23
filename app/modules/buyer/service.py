"""Step 8 Buyer side (spec section 3, step 8): the AI is the buyer's agent; the buyer decides.

Four screens, each a function here:
1. `start` (buyer intake and representation disclosure): the buyer's needs, budget and pre-approval; no
   protected-class questions (F6, F18, F19). The AI takes the buyer on as a client (CP-30 marker), sends the
   agency form, the fair-housing notice and the "not legal services" notice (CP-24), and the buyer agreement with
   an objectively ascertainable, negotiable fee (L15). CP-16: the buyer acknowledges and signs.
2. `search` and `send_alert` (search alerts): fictional listings plus the firm's own listing; filters on the
   home's facts only, no steering filters (L37). The alert is one Haiku call, fair-housing checked and sent with
   the identity block (`inbox.send`, buyer side).
3. `request_tour` (tour request): refused until CP-16 is done (L15). The firm's own listing opens CP-17, the
   dual-agency consent of both clients (L13). The seller's AI books it inside the seller's showing windows:
   self-guided (CP-28 marker) if the seller allows it, else owner-hosted (CP-10). CP-29.
4. `advise_offer` / `approve_offer` / `advise_counter` / `approve_reply` (offer advice, draft and approval):
   the buyer's AI advises on price and terms and drafts the offer (CP-31 marker); the buyer approves it (CP-18),
   which needs CP-17; the offer goes to the seller's side as offer B. After the seller's counter the buyer's AI
   advises the buyer and drafts the reply (CP-31); the buyer approves it (CP-18); the buyer's AI sends exactly that
   reply (CP-13 marker, buyer side) and the seller's AI answers within the seller's decision (step 6).

Information wall (decision 24): every model call here is built by `AgentContext(s, deal, "buyer")` plus the
buyer's own state and public facts. Nothing here reads the seller's instructions or the seller's decision; the
buyer's side sees the seller's counter only as sent.
"""

from __future__ import annotations

import copy
from pathlib import Path

import yaml
from sqlalchemy import select
from sqlalchemy.orm import Session, object_session

from app.audit import record_event
from app.brokerage import brokerage
from app.config import ROOT
from app.connectors.public_records import FixtureRecords
from app.model.context import AgentContext
from app.model.provider import ModelProvider
from app.models import BuyerState, ClientInstructions, Deal, Disclosure, Document, Person, now
from app.modules.buyer.schemas import BuyerAlert, BuyerCounterAdvice, BuyerOfferAdvice
from app.modules.inbox import service as inbox
from app.pii import MASKER
from app.records import service as records
from app.records.service import NotYourDecision
from app.sanitize import clean_model

PROMPTS = Path(__file__).with_name("prompts")
THREAD = "BUYER"
PARTY = "Buyer 1 (the firm's buyer client)"
BUYER_AGENCY_NOTE = ("Attached: the New York agency disclosure form (I act for you as your buyer's agent), the New "
                     "York State Housing and Anti-Discrimination Notice, and the \"these are not legal services\" "
                     "notice.")
# The intake asks only about the home and the money: no protected-class question (F18, F19; L37). A test checks
# the form's fields against this list.
INTAKE_FIELDS = ("name", "email", "phone", "beds_min", "acres_min", "towns", "must_haves", "preapproved",
                 "preapproval_amount", "timeline", "max_price", "private_notes")
SEARCH_FILTERS = ("max_price", "beds_min", "acres_min", "towns")
TOWNS = ("Pawling", "Beekman", "Dover", "Union Vale", "East Fishkill")


# ---- state ------------------------------------------------------------------------------------------------------

def _row(deal: Deal) -> BuyerState:
    s = object_session(deal)
    row = s.execute(select(BuyerState).where(BuyerState.deal_id == deal.id)).scalar_one_or_none()
    if row is None:
        row = BuyerState(deal_id=deal.id, state={})
        s.add(row)
        s.flush()
    return row


def state(deal: Deal) -> dict:
    return copy.deepcopy(_row(deal).state or {})


def _save(s: Session, deal: Deal, st: dict) -> None:
    _row(deal).state = st
    s.flush()


def instructions(s: Session, deal: Deal) -> ClientInstructions | None:
    q = select(ClientInstructions).where(ClientInstructions.deal_id == deal.id, ClientInstructions.side == "buyer")
    return s.execute(q.limit(1)).scalar_one_or_none()


def demo_input() -> dict:
    """What the demo buyer types on the intake form (fictional, seed/personas.yaml)."""
    from app.modules.intake.service import load_personas

    b = load_personas()["buyer"]
    return {"name": b["legal_name"], "email": b["email"], "phone": b["phone"], "beds_min": "3", "acres_min": "1",
            "towns": list(TOWNS), "must_haves": "A room for a home office; some land; room for a garden",
            "preapproved": "yes", "preapproval_amount": b["preapproval_amount"],
            "timeline": "Flexible; closing in about two months suits", "max_price": str(
                b["instructions"]["confidential"]["maximum_price"]),
            "private_notes": b["instructions"]["confidential"]["notes"]}


# ---- 1. intake and representation -------------------------------------------------------------------------------

def start(s: Session, deal: Deal, data: dict) -> Person:
    """The AI takes the buyer on as a client (CP-30), sends the notices (CP-24) and the buyer agreement (CP-16)."""
    if deal.buyer_id:
        return deal.buyer
    for k in ("name", "email", "max_price"):
        if not str(data.get(k) or "").strip():
            raise ValueError("Name, e-mail and the most you would pay are needed.")
    buyer = Person(role="buyer", persona_label="Buyer", token="BUYER_1", legal_name=data["name"].strip(),
                   email=data["email"].strip(), phone=(data.get("phone") or "").strip())
    s.add(buyer)
    s.flush()
    for value, label in ((buyer.legal_name, "[BUYER_1]"), (buyer.email, "[EMAIL]"), (buyer.phone, "[PHONE]")):
        MASKER.register(value, label)
    deal.buyer_id = buyer.id
    towns = data.get("towns") or []
    needs = {"beds_min": int(data.get("beds_min") or 0), "acres_min": float(data.get("acres_min") or 0),
             "towns": list(towns) if isinstance(towns, (list, tuple)) else [t.strip() for t in str(towns).split(",")],
             "must_haves": (data.get("must_haves") or "").strip(),
             "preapproved": (data.get("preapproved") or "no") == "yes",
             "preapproval_amount": int(data.get("preapproval_amount") or 0),
             "timeline": (data.get("timeline") or "").strip()}
    s.add(ClientInstructions(deal_id=deal.id, side="buyer", fact_sheet=needs, authority={},
                             confidential={"maximum_price": int(data["max_price"]),
                                           "notes": (data.get("private_notes") or "").strip()}))
    records.mark_law(s, deal.id, "CP-30", reason="The AI took Buyer 1 on as a client and recorded the agency "
                                                  "relationship: buyer's agent. The firm also lists 146 Route 292, "
                                                  "so an interest in it makes this dual agency (CP-17)",
                     attached_to=f"person:{buyer.id}")
    for kind, title, l_id in (("agency", "NY agency disclosure form (DOS-1736-f), buyer's agent", "L12"),
                              ("fair_housing", "NY Housing and Anti-Discrimination Disclosure (DOS-2156)", "L39"),
                              ("not_legal_services", '"These are not legal services" notice', "L29")):
        d = Disclosure(deal_id=deal.id, person_id=buyer.id, kind=f"buyer_{kind}", title=title, l_id=l_id,
                       trigger="First substantive contact with the buyer", required=True, delivered_at=now())
        s.add(d)
        s.flush()
        records.record_auto(s, deal.id, "CP-24", reason=f"Sent to the buyer: {title} ({l_id})",
                            attached_to=f"disclosure:{d.id}", step=8)
    doc = Document(deal_id=deal.id, kind="buyer_agreement", generated_by="ai", label_version="v1")
    s.add(doc)
    s.flush()
    records.open_decision(s, deal.id, "CP-16", attached_to=f"document:{doc.id}")
    _save(s, deal, {"needs": needs, "started_at": now().isoformat()})
    record_event(s, actor="ai", kind="ai_action", entity="deal", entity_id=deal.id,
                 summary="Buyer side: the AI took Buyer 1 on as a client; notices and buyer agreement sent")
    return buyer


def buyer_agreement() -> dict:
    b = brokerage()
    return {"fee": b["buyer_fee"],
            "terms": ["The firm acts as the buyer's agent: loyalty, confidentiality, full disclosure.",
                      f"Compensation: {b['buyer_fee']}.",
                      "Exclusive for 90 days; either side may end it with written notice; no automatic renewal.",
                      "If the buyer wants a home this firm lists for its seller, the firm acts for both only with "
                      "both clients' informed written consent (dual agency).",
                      "No tour or showing before this agreement is signed (L15)."]}


def sign_agreement(s: Session, deal: Deal, persona: str, decision: str) -> None:
    cp = records.latest(s, deal.id, "CP-16")
    if cp is None:
        raise ValueError("The buyer agreement has not been sent yet.")
    records.decide(s, cp, persona=persona, decision=decision,
                   reason="The buyer acknowledged the agency form and signed the buyer agreement (simulated e-sign, "
                          "L34)" if decision == "sign" else "The buyer declined the buyer agreement")
    if cp.status == "done":
        doc = s.execute(select(Document).where(Document.deal_id == deal.id, Document.kind == "buyer_agreement")
                        ).scalar_one()
        doc.signed_by = {"buyer": now().isoformat()}
        for d in s.execute(select(Disclosure).where(Disclosure.deal_id == deal.id,
                                                    Disclosure.kind == "buyer_agency")).scalars():
            d.acknowledged_at = now()


# ---- 2. search and alerts -------------------------------------------------------------------------------------------

def firm_listing(deal: Deal) -> dict:
    facts = {f.field: f.value for f in deal.property.facts}

    def num(field, cast=float, default=0):
        try:
            return cast(str(facts.get(field) or default).replace(",", ""))
        except ValueError:
            return default
    return {"id": "FIRM", "label": "This firm's listing (the demonstration house)",
            "street": f"{deal.property.street} (DEMONSTRATION: not for sale through this firm)",
            "town": "Pawling", "price": deal.list_price or 0, "beds": num("BedroomsTotal", int),
            "baths": num("BathroomsFull", int), "sqft": num("LivingArea", int), "acres": num("LotSizeAcres"),
            "style": facts.get("ArchitecturalStyle") or "", "year_built": num("YearBuilt", int),
            "heat": facts.get("HeatingFuel") or "", "water_sewer": "Well and septic", "days_on_market": 9,
            "firm_listing": True}


def listings(deal: Deal) -> list[dict]:
    fixture = yaml.safe_load((ROOT / "fixtures" / "buyer_listings.yaml").read_text())["listings"]
    return [{**x, "firm_listing": False} for x in fixture] + [firm_listing(deal)]


def search(deal: Deal, criteria: dict) -> list[dict]:
    """Facts-only filters (SEARCH_FILTERS). There is no school-rating, neighbourhood or people filter (L37)."""
    unknown = set(criteria) - set(SEARCH_FILTERS)
    if unknown:
        raise ValueError(f"Not a search filter: {', '.join(sorted(unknown))}. Search uses the home's facts only.")
    towns = set(criteria.get("towns") or TOWNS)
    return [x for x in listings(deal)
            if x["price"] <= int(criteria.get("max_price") or 10**9) and x["beds"] >= int(criteria.get("beds_min") or 0)
            and x["acres"] >= float(criteria.get("acres_min") or 0) and x["town"] in towns]


def default_criteria(s: Session, deal: Deal) -> dict:
    ins = instructions(s, deal)
    needs = (ins.fact_sheet or {}) if ins else {}
    conf = (ins.confidential or {}) if ins else {}
    return {"max_price": conf.get("maximum_price") or 700000, "beds_min": needs.get("beds_min", 3),
            "acres_min": needs.get("acres_min", 1), "towns": needs.get("towns") or list(TOWNS)}


def send_alert(s: Session, deal: Deal, provider: ModelProvider, criteria: dict):
    """The buyer's AI saves the search and sends the alert (simulated), fair-housing checked."""
    if not deal.buyer_id:
        raise ValueError("Start the buyer intake first.")
    matches = search(deal, criteria)
    ctx = AgentContext(s, deal, "buyer").build(facts=[], instructions=False, extra={
        "buyer_needs": (instructions(s, deal).fact_sheet or {}),
        "listings": [{k: x[k] for k in ("id", "label", "town", "price", "beds", "baths", "sqft", "acres", "style",
                                         "year_built", "heat", "water_sewer", "days_on_market", "firm_listing")}
                     for x in matches]})
    ctx.pop("property", None)  # the alert is about the matches, not the firm's listing in particular
    result = provider.generate("buyer.alert", BuyerAlert, ctx, s=s, module="buyer",
                               system=(PROMPTS / "alert.v1.md").read_text(), prompt_version="alert.v1", side="buyer")
    alert: BuyerAlert = clean_model(result.output)
    lines = [alert.message] + [f"- {next((x['label'] for x in matches if x['id'] == n.id), n.id)}: {n.why}"
                               for n in alert.notes]
    m = inbox.send(s, deal, provider, thread=THREAD, party=PARTY, body="\n".join(lines), topic="alert",
                   discusses_listing=True, side="buyer", agency_note=BUYER_AGENCY_NOTE,
                   extra={"mode": result.mode, "model": result.model})
    st = state(deal)
    st["search"] = {"criteria": criteria, "matches": [x["id"] for x in matches], "message_id": m.id,
                    "status": m.status}
    _save(s, deal, st)
    return m


# ---- 3. tour --------------------------------------------------------------------------------------------------------

def request_tour(s: Session, deal: Deal, provider: ModelProvider, *, self_guided: bool = True) -> dict:
    """The buyer's AI asks for a tour of the firm's listing; the seller's AI books it inside the seller's
    authority (CP-27). Refused before the buyer agreement (CP-16, L15)."""
    records.require(s, deal.id, "CP-16", action="book a tour (no tour before a signed buyer agreement, L15)")
    records.require(s, deal.id, "CP-27", action="book a showing (the seller has not approved the AI's authority)")
    st = state(deal)
    if st.get("tour"):
        return st["tour"]
    if not records.latest(s, deal.id, "CP-17"):
        records.open_decision(s, deal.id, "CP-17", reason="The firm's buyer client wants to see the firm's own "
                                                           "listing: both clients must consent to dual agency",
                              attached_to="buyer:tour")
    seller_auth = inbox.authority(s, deal)  # the seller's AI books it: its windows and its self-guided permission
    day, (start_h, _) = next(iter((seller_auth.get("showing_windows") or {"Sat": [10, 16]}).items()))
    when = f"{day} at {start_h}:00"
    guided = self_guided and bool(seller_auth.get("self_guided_tours"))
    records.record_auto(s, deal.id, "CP-29", reason=f"Tour of the firm's listing booked for Buyer 1, {when}: "
                        + ("self-guided" if guided else "owner-hosted") + "; access and feedback requests sent "
                        "(simulated)", attached_to="buyer:tour", step=8)
    if guided:
        records.mark_law(s, deal.id, "CP-28", reason=f"The AI arranged a self-guided tour for Buyer 1, {when}",
                         attached_to="buyer:tour", step=8)
        body = (f"Your tour is booked: {when}, self-guided. You will get a one-time smart-lock code for that hour "
                "only; lockbox keys and PINs are never lent. Please tell me afterwards what you thought.")
    else:
        records.record_human(s, deal.id, "CP-10", reason=f"The seller (owner) opens the door for Buyer 1's tour, "
                                                         f"{when}", step=8)
        body = f"Your tour is booked: {when}. The owner will open the door. Please tell me afterwards what you thought."
    m = inbox.send(s, deal, provider, thread=THREAD, party=PARTY, body=body, topic="showing", discusses_listing=True,
                   side="buyer", agency_note=BUYER_AGENCY_NOTE)
    st["tour"] = {"when": when, "kind": "self-guided" if guided else "owner-hosted", "message_id": m.id}
    _save(s, deal, st)
    return st["tour"]


def consent_dual_agency(s: Session, deal: Deal, persona: str, decision: str) -> None:
    cp = records.latest(s, deal.id, "CP-17")
    if cp is None:
        raise ValueError("No dual-agency consent is needed yet.")
    records.decide(s, cp, persona=persona, decision=decision,
                   reason=f"The {persona} {'consented to' if decision == 'consent' else 'declined'} dual agency "
                          "in writing (simulated e-sign)")


# ---- 4. the offer, and the reply to the counter --------------------------------------------------------------------

def _public_sales() -> list[dict]:
    return [{k: c[k] for k in ("address", "sale_date", "sale_price", "style", "living_area_sqft", "acres")}
            for c in FixtureRecords().data["comparables"]]


def offer_context(s: Session, deal: Deal) -> dict:
    """The buyer's AI's whitelist: the buyer's own instructions (with the private maximum), the listing's public
    facts and list price, and public sales records. Nothing from the seller's side."""
    lst = firm_listing(deal)
    return AgentContext(s, deal, "buyer").build(
        facts=["ArchitecturalStyle", "YearBuilt", "LivingArea", "BelowGradeFinishedArea", "BedroomsTotal",
               "BathroomsFull", "LotSizeAcres", "Cooling", "HeatingFuel", "WaterSource", "Sewer", "ParkingFeatures",
               "ConditionUpdates", "RoofYear", "FloodZone"],
        extra={"listing": {"list_price": lst["price"], "days_on_market": lst["days_on_market"],
                           "firm_listing": True},
               "public_sales": _public_sales(), "tour": state(deal).get("tour")})


def advise_offer(s: Session, deal: Deal, provider: ModelProvider) -> dict:
    records.require(s, deal.id, "CP-16", action="advise on an offer (no buyer agreement yet)")
    records.require(s, deal.id, "CP-17", action="draft an offer on the firm's own listing (both clients must "
                                                "consent to dual agency first, L13)")
    result = provider.generate("buyer.offer_advise", BuyerOfferAdvice, offer_context(s, deal), s=s, module="buyer",
                               system=(PROMPTS / "offer_advise.v1.md").read_text(), prompt_version="offer_advise.v1",
                               side="buyer")
    adv: BuyerOfferAdvice = clean_model(result.output)
    st = state(deal)
    st["advice"] = {**adv.model_dump(), "mode": result.mode, "model": result.model,
                    "recorded_at": result.recorded_at}
    _save(s, deal, st)
    records.mark_law(s, deal.id, "CP-31", reason=f"The buyer's AI advised Buyer 1 on price and terms and drafted "
                                                  f"the offer (${adv.recommended_price:,}; {result.mode}, "
                                                  f"{result.model})", attached_to="buyer:offer")
    if not _pending_cp18(s, deal):
        records.open_decision(s, deal.id, "CP-18", reason="Approve the offer the buyer's AI drafted",
                              attached_to="buyer:offer")
    return st["advice"]


def _pending_cp18(s: Session, deal: Deal):
    cp = records.latest(s, deal.id, "CP-18")
    return cp if cp and cp.status == "pending" else None


def approve_offer(s: Session, deal: Deal, persona: str, decision: str, price: int | None = None) -> dict | None:
    """CP-18: the buyer's own decision on the drafted offer (the buyer may change the price). Approved, the
    buyer's AI submits it to the seller's side as offer B."""
    from app.modules.offers import service as offers

    if persona != "buyer":
        raise NotYourDecision("CP-18 is the buyer's decision; the " + persona + " cannot make it.")
    st = state(deal)
    adv = st.get("advice")
    cp = _pending_cp18(s, deal)
    if not adv or cp is None:
        raise ValueError("The buyer's AI has not drafted an offer yet.")
    price = int(price or adv["recommended_price"])
    terms = {"price": price, "deposit_pct": adv["deposit_pct"], "financing": adv["financing"],
             "mortgage_days": adv["mortgage_days"], "inspection_days": adv["inspection_days"],
             "closing_days": adv["closing_days"], "contingencies": adv["contingencies"],
             "requests": adv["requests"]}
    records.decide(s, cp, persona=persona, decision=decision,
                   reason=(f"The buyer approved an offer of ${price:,}" + (
                       f" (the AI drafted ${adv['recommended_price']:,})" if price != adv["recommended_price"]
                       else "")) if decision == "approve" else "The buyer declined to make the offer")
    if decision != "approve":
        return None
    offers.receive_offer_b(s, deal, terms, party="The firm's own buyer (Buyer 1)")
    st = state(deal)
    st["offer"] = terms
    _save(s, deal, st)
    return terms


def counter_received(s: Session, deal: Deal, counter: dict) -> None:
    """The seller's AI's counter on offer B arrives at the buyer's side, as sent."""
    st = state(deal)
    st.setdefault("counters", []).append(counter)
    st.pop("counter_advice", None)
    _save(s, deal, st)
    record_event(s, actor="ai", kind="ai_action", entity="deal", entity_id=deal.id,
                 summary=f"Buyer side: the seller's counter arrived (${counter['price']:,})")


def counter_context(s: Session, deal: Deal) -> dict:
    st = state(deal)
    return AgentContext(s, deal, "buyer").build(facts=["ArchitecturalStyle", "LivingArea", "LotSizeAcres"], extra={
        "buyer_offer": st.get("offer"), "seller_counter": (st.get("counters") or [None])[-1],
        "earlier_counters": (st.get("counters") or [])[:-1], "replies_sent": st.get("replies") or []})


def advise_counter(s: Session, deal: Deal, provider: ModelProvider) -> dict:
    st = state(deal)
    if not st.get("counters"):
        raise ValueError("No counter from the seller yet.")
    result = provider.generate("buyer.counter_advise", BuyerCounterAdvice, counter_context(s, deal), s=s,
                               module="buyer", system=(PROMPTS / "counter_advise.v1.md").read_text(),
                               prompt_version="counter_advise.v1", side="buyer")
    adv: BuyerCounterAdvice = clean_model(result.output)
    st = state(deal)
    st["counter_advice"] = {**adv.model_dump(), "mode": result.mode, "model": result.model,
                            "recorded_at": result.recorded_at}
    _save(s, deal, st)
    records.mark_law(s, deal.id, "CP-31", reason=f"The buyer's AI advised Buyer 1 on the seller's counter and "
                                                  f"drafted the reply ({adv.action}, ${adv.price:,})",
                     attached_to="buyer:counter")
    if not _pending_cp18(s, deal):
        records.open_decision(s, deal.id, "CP-18", reason="Approve the reply to the seller's counter",
                              attached_to="buyer:counter")
    return st["counter_advice"]


def approve_reply(s: Session, deal: Deal, persona: str, decision: str, price: int | None = None) -> dict | None:
    """CP-18 again: the buyer approves the reply; the buyer's AI sends exactly that (CP-13, buyer side) and the
    seller's AI answers within the seller's decision."""
    from app.modules.offers import service as offers

    if persona != "buyer":
        raise NotYourDecision("CP-18 is the buyer's decision; the " + persona + " cannot make it.")
    st = state(deal)
    adv, cp = st.get("counter_advice"), _pending_cp18(s, deal)
    if not adv or cp is None:
        raise ValueError("The buyer's AI has not drafted a reply yet.")
    counter = st["counters"][-1]
    reply = {"action": adv["action"], "price": int(price or adv["price"]), "closing_days": adv["closing_days"],
             "inspection_days": adv["inspection_days"], "mortgage_days": adv["mortgage_days"],
             "requests": adv["requests"]}
    if reply["action"] == "accept":
        reply.update({k: counter[k] for k in ("price", "closing_days", "inspection_days", "mortgage_days",
                                              "requests") if k in counter})
    records.decide(s, cp, persona=persona, decision=decision,
                   reason=f"The buyer approved the reply: {reply['action'].replace('_', ' ')} at ${reply['price']:,}"
                   if decision == "approve" else "The buyer declined the drafted reply")
    if decision != "approve":
        return None
    st = state(deal)
    st.setdefault("replies", []).append(reply)
    st.pop("counter_advice", None)
    _save(s, deal, st)
    records.mark_law(s, deal.id, "CP-13", reason=f"The buyer's AI sent Buyer 1's reply to the seller's counter: "
                                                  f"{reply['action'].replace('_', ' ')} at ${reply['price']:,}",
                     attached_to="offers:buyer", step=8)
    offers.receive_reply(s, deal, reply, frm="buyer's AI")
    return reply


def agreed(s: Session, deal: Deal, accepted: dict) -> None:
    st = state(deal)
    st["agreed"] = {k: accepted.get(k) for k in ("final_price", "closing_days", "inspection_days", "mortgage_days",
                                                 "requests")}
    _save(s, deal, st)
