"""Step 6 Offers (spec section 3, step 6): the AI presents every offer and advises; the seller decides; the AI
negotiates the counter within that decision.

1. `OFFERS`: two simulated written offers. A from an outside buyer's agent (simulated other firm); B from the
   firm's own buyer (the buyer side, step 8, drafts it; until step 8 is built it arrives as a fixture).
2. `compare`: code builds the comparison and a net sheet per offer (`pricing.net_sheet`).
3. `advise`: one model call (`offers.advise`) presents each offer and advises with reasoning. CP-11 marker.
4. `decide`: CP-12, the seller's own decision: accept, counter or reject, and for a counter the price, the lowest
   price the AI may agree without coming back, and the terms.
5. `negotiate`: the AI sends counters (CP-13 marker each). `check_counter` refuses in code any counter outside the
   seller's decision (below the seller's lowest price or with different terms); it goes back to the seller.

Offer papers carry "not binding until a formal contract is signed by both" (L24). The model sees the offers'
terms and the market facts, never the seller's confidential instructions or PII.
"""

from __future__ import annotations

import copy
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session, object_session

from app.audit import record_event
from app.model.provider import ModelProvider
from app.models import Deal, OfferState
from app.modules.offers.schemas import OfferAdvice
from app.modules.pricing import service as pricing
from app.records import service as records
from app.sanitize import clean_model

PROMPTS = Path(__file__).with_name("prompts")
PROMPT_VERSION = "advise.v1"
NOT_BINDING = "Not binding until a formal contract of sale is signed by both parties (L24)."

OFFERS = [
    {"label": "A", "party": "Buyer's agent for Prospect B (simulated other firm)", "price": 630000,
     "financing": "Conventional mortgage, 20% down; pre-approval letter attached", "deposit_pct": 10,
     "contingencies": ["mortgage commitment (45 days)", "home inspection (10 days)", "well and septic tests"],
     "closing_days": 60, "buyer_agent_compensation": 0, "requests": "Seller to leave the riding mower"},
    {"label": "B", "party": "The firm's own buyer (Buyer 1, step 8; simulated)", "price": 620000,
     "financing": "Conventional mortgage, 25% down; pre-approval letter attached", "deposit_pct": 10,
     "contingencies": ["mortgage commitment (30 days)", "home inspection (7 days)"],
     "closing_days": 45, "buyer_agent_compensation": 0, "requests": "None"},
]
# The buyer side's simulated answers to the seller's counter, in order (demonstration).
BUYER_REPLIES = {"A": [632000, 636000]}


class CounterRefused(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def _row(deal: Deal) -> OfferState:
    s = object_session(deal)
    row = s.execute(select(OfferState).where(OfferState.deal_id == deal.id)).scalar_one_or_none()
    if row is None:
        row = OfferState(deal_id=deal.id, state={})
        s.add(row)
        s.flush()
    return row


def _state(deal: Deal) -> dict:
    return copy.deepcopy(_row(deal).state or {})


def state(deal: Deal) -> dict:
    return _state(deal)


def _save(s: Session, deal: Deal, st: dict) -> None:
    _row(deal).state = st
    s.flush()


def compare(s: Session, deal: Deal) -> list[dict]:
    records.require(s, deal.id, "CP-27", action="receive offers (the seller has not approved the AI's authority)")
    out = []
    for o in OFFERS:
        ns = pricing.net_sheet(o["price"])
        out.append({**o, "net_before_mortgage": ns["net_before_mortgage"], "net_sheet": ns,
                    "vs_list": o["price"] - (deal.list_price or 0), "deposit": o["price"] * o["deposit_pct"] // 100})
    return out


def model_context(deal: Deal, offers: list[dict]) -> dict:
    return {"list_price": deal.list_price, "offers": [{k: o[k] for k in (
        "label", "price", "financing", "deposit_pct", "contingencies", "closing_days", "requests",
        "net_before_mortgage", "vs_list")} for o in offers],
        "market": {"pricing_range": "$610,000 to $650,000 (step 2)", "days_on_market": 9,
                   "showing_feedback": "liked the lot and kitchen; concerns: no central air, road noise"}}


def advise(s: Session, deal: Deal, provider: ModelProvider) -> dict:
    offers = compare(s, deal)
    system = (PROMPTS / f"{PROMPT_VERSION}.md").read_text()
    result = provider.generate("offers.advise", OfferAdvice, model_context(deal, offers), s=s, module="offers",
                               system=system, prompt_version=PROMPT_VERSION, side="seller")
    adv: OfferAdvice = clean_model(result.output)
    st = _state(deal)
    st["advice"] = {**adv.model_dump(), "mode": result.mode, "model": result.model}
    _save(s, deal, st)
    records.mark_law(s, deal.id, "CP-11", reason=f"AI presented {len(offers)} offers and advised the seller "
                                                  f"({result.mode}, {result.model})", attached_to="offers")
    if not records.is_done(s, deal.id, "CP-12"):
        records.open_decision(s, deal.id, "CP-12", attached_to="offers")
    record_event(s, actor="ai", kind="ai_action", entity="deal", entity_id=deal.id,
                 summary=f"Offers: AI presented and advised on {len(offers)} offers ({result.mode})")
    return st["advice"]


def decide(s: Session, deal: Deal, persona: str, *, decision: str, offer: str, counter_price: int | None = None,
           lowest_price: int | None = None) -> None:
    """CP-12: the seller's own decision. A counter needs a price and the lowest price the AI may agree."""
    cp = records.latest(s, deal.id, "CP-12")
    if cp is None:
        raise records.GateError("CP-11", "The AI has not presented the offers yet.")
    if offer not in {o["label"] for o in OFFERS}:
        raise ValueError("Choose offer A or B.")
    if decision == "counter":
        if not counter_price or not lowest_price or lowest_price > counter_price:
            raise ValueError("A counter needs a price and the lowest price the AI may agree (not above the counter).")
    if decision == "counter":
        reason = (f"The seller countered offer {offer} at ${counter_price:,}; the AI may agree down to "
                  f"${lowest_price:,}, same terms otherwise")
    else:
        reason = f"The seller chose to {decision} offer {offer}"
    records.decide(s, cp, persona=persona, decision=decision, reason=reason)
    st = _state(deal)
    st["decision"] = {"decision": decision, "offer": offer, "counter_price": counter_price,
                      "lowest_price": lowest_price}
    if decision == "accept":
        o = next(x for x in OFFERS if x["label"] == offer)
        st["accepted"] = {**o, "final_price": o["price"]}
    _save(s, deal, st)


def check_counter(deal: Deal, price: int, terms_changed: bool = False) -> None:
    """Code, not the model: a counter outside the seller's decision is refused and goes back to the seller."""
    d = _state(deal).get("decision") or {}
    if d.get("decision") != "counter":
        raise CounterRefused("The seller has not decided to counter, so the AI may not send one (CP-12).")
    if price < d["lowest_price"]:
        raise CounterRefused(f"Refused: ${price:,} is below the lowest price the seller allowed "
                             f"(${d['lowest_price']:,}). It goes back to the seller as a new decision (CP-12).")
    if price > d["counter_price"]:
        raise CounterRefused(f"Refused: ${price:,} is above the seller's own counter (${d['counter_price']:,}).")
    if terms_changed:
        raise CounterRefused("Refused: the seller's decision keeps the offer's other terms; changing them needs "
                             "the seller (CP-12).")


def send_counter(s: Session, deal: Deal, price: int, terms_changed: bool = False) -> dict:
    check_counter(deal, price, terms_changed)
    st = _state(deal)
    d = st["decision"]
    thread = st.setdefault("thread", [])
    thread.append({"from": "seller's AI", "price": price, "note": f"Counter on offer {d['offer']}: ${price:,}, other "
                   f"terms as offered. {NOT_BINDING}"})
    records.mark_law(s, deal.id, "CP-13", reason=f"Seller's AI countered offer {d['offer']} at ${price:,}, inside "
                                                  "the seller's decision", attached_to="offers")
    replies = BUYER_REPLIES.get(d["offer"], [])
    n = len([t for t in thread if t["from"] == "buyer's side"])
    if n < len(replies):
        reply = replies[n]
        if reply >= price:
            st["accepted"] = {**next(x for x in OFFERS if x["label"] == d["offer"]), "final_price": price}
            thread.append({"from": "buyer's side", "price": price, "note": f"Accepted at ${price:,}. {NOT_BINDING}"})
        else:
            thread.append({"from": "buyer's side", "price": reply, "note": f"Counter: ${reply:,}. {NOT_BINDING}"})
    _save(s, deal, st)
    return st


def negotiate(s: Session, deal: Deal) -> dict:
    """The AI's negotiation plan within the seller's decision: open at the seller's counter, then meet the
    buyer's reply halfway, never below the seller's lowest price."""
    st = _state(deal)
    d = st.get("decision") or {}
    thread = st.get("thread") or []
    if st.get("accepted"):
        return st
    if not thread:
        return send_counter(s, deal, d.get("counter_price") or 0)
    last = thread[-1]
    if last["from"] != "buyer's side":
        return st
    mine = [t["price"] for t in thread if t["from"] == "seller's AI"][-1]
    target = max(d["lowest_price"], (mine + last["price"]) // 2 // 1000 * 1000)
    if target <= last["price"]:  # the buyer's figure is inside the seller's decision: agree it
        target = last["price"]
    return send_counter(s, deal, target)
