"""Step 6 Offers (spec section 3, step 6): the seller's AI presents every offer and advises; the seller decides;
the seller's AI negotiates the counter, price and terms, within that decision.

1. Offers: A from an outside buyer's agent (simulated other firm, `OFFER_A`); B from the firm's own buyer, drafted
   by the buyer's AI and approved by the buyer in step 8 (`receive_offer_b`). B needs both clients' dual-agency
   consent first (CP-17).
2. `compare`: code builds the comparison and a net sheet per offer (`pricing.net_sheet`).
3. `advise`: one model call (`offers.advise`, seller side) presents each offer and advises. CP-11 marker.
4. `decide`: CP-12, the seller's own decision: accept, counter or reject. A counter sets the price, the lowest price
   the AI may agree without coming back, and the terms: closing-date range, the longest inspection and mortgage
   periods, and whether the buyer's requests may stay.
5. `send_counter` / `receive_reply` / `negotiate`: the seller's AI sends counters and answers replies on its own
   (CP-13 marker, seller side, each): a reply inside the decision is agreed; one outside it gets a further counter
   inside it; when nothing inside it is left, it goes back to the seller. `check_counter` refuses in code any counter or agreement outside the seller's decision
   (price, closing date, inspection and mortgage periods, deposit, contingencies, financing, requests, credits);
   anything outside goes back to the seller as a new CP-12.

A counter on offer A gets the outside agent's simulated replies (`A_REPLIES`). A counter on offer B goes to the
buyer's AI, which advises the buyer; the buyer approves the reply (CP-18) and the buyer's AI sends it (step 8).

Offer papers carry "not binding until a formal contract is signed by both" (L24). The seller's AI sees the offers'
terms and the market facts, never the buyer's confidential limits, the seller's own confidential notes or PII.
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
PROMPT_VERSION = "advise.v2"
NOT_BINDING = "Not binding until a formal contract of sale is signed by both parties (L24)."
TERM_KEYS = ("price", "deposit_pct", "financing", "mortgage_days", "inspection_days", "closing_days",
             "contingencies", "requests")

# Offer A is a common kind of weaker paper: a higher price, but 10% down, a long closing and a contingency on the
# sale of the buyer's current home (demonstration fixture).
OFFER_A = {"label": "A", "party": "Buyer's agent for Prospect B (simulated other firm)", "side": "outside",
           "price": 630000, "deposit_pct": 10, "financing": "Conventional mortgage, 10% down; pre-approval attached",
           "mortgage_days": 45, "inspection_days": 10, "closing_days": 75,
           "contingencies": ["mortgage commitment", "home inspection", "well and septic tests",
                             "sale of the buyer's current home within 60 days"],
           "requests": ["the riding mower stays"]}
# The outside agent's simulated answers to a counter on offer A, in order (demonstration).
A_REPLIES = [{"price": 632000, "closing_days": 60, "inspection_days": 10, "mortgage_days": 45},
             {"price": 636000, "closing_days": 60, "inspection_days": 10, "mortgage_days": 45}]
DECISION_DEFAULTS = {"closing_min": 30, "closing_max": 60, "inspection_max": 10, "mortgage_max": 45}


class CounterRefused(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotReady(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


# ---- state ------------------------------------------------------------------------------------------------------

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


def offers(deal: Deal) -> list[dict]:
    st = _state(deal)
    return [OFFER_A] + ([st["offer_b"]] if st.get("offer_b") else [])


def offer(deal: Deal, label: str) -> dict:
    o = next((x for x in offers(deal) if x["label"] == label), None)
    if o is None:
        raise ValueError(f"There is no offer {label}.")
    return o


def terms_text(t: dict) -> str:
    parts = [f"${t['price']:,}"]
    if t.get("closing_days"):
        parts.append(f"closing in {t['closing_days']} days")
    if t.get("inspection_days") is not None:
        parts.append(f"inspection {t['inspection_days']} days")
    if t.get("mortgage_days") is not None:
        parts.append(f"mortgage commitment {t['mortgage_days']} days")
    if t.get("requests"):
        parts.append("requests: " + "; ".join(t["requests"]))
    return ", ".join(parts)


# ---- offers in ----------------------------------------------------------------------------------------------------

def receive_offer_b(s: Session, deal: Deal, terms: dict, party: str) -> dict:
    """The buyer's AI submits offer B, as the buyer approved it (CP-18). Called by the buyer side (step 8)."""
    records.require(s, deal.id, "CP-17", action="present an offer from the firm's own buyer (both clients must "
                                                 "consent to dual agency first, L13)")
    st = _state(deal)
    b = {"label": "B", "party": party, "side": "firm_buyer", **{k: terms[k] for k in TERM_KEYS if k in terms}}
    st["offer_b"] = b
    _save(s, deal, st)
    record_event(s, actor="ai", kind="ai_action", entity="deal", entity_id=deal.id,
                 summary=f"Offers: offer B from the firm's own buyer received ({terms_text(b)})")
    return b


def compare(s: Session, deal: Deal) -> list[dict]:
    records.require(s, deal.id, "CP-27", action="receive offers (the seller has not approved the AI's authority)")
    out = []
    for o in offers(deal):
        ns = pricing.net_sheet(o["price"])
        out.append({**o, "net_before_mortgage": ns["net_before_mortgage"], "net_sheet": ns,
                    "vs_list": o["price"] - (deal.list_price or 0), "deposit": o["price"] * o["deposit_pct"] // 100})
    return out


def model_context(deal: Deal, table: list[dict]) -> dict:
    """Seller side. Offer terms and market facts only: nothing from the buyer's side beyond what offer B says."""
    return {"list_price": deal.list_price, "offers": [{k: o[k] for k in (
        "label", "side", "price", "financing", "deposit_pct", "mortgage_days", "inspection_days", "closing_days",
        "contingencies", "requests", "net_before_mortgage", "vs_list")} for o in table],
        "market": {"pricing_range": "$610,000 to $650,000 (step 2)", "days_on_market": 9,
                   "showing_feedback": "liked the lot and kitchen; concerns: no central air, road noise"}}


def advise(s: Session, deal: Deal, provider: ModelProvider) -> dict:
    table = compare(s, deal)
    if len(table) < 2:
        raise NotReady("Only offer A is in. Offer B, from the firm's own buyer, has not arrived yet: the buyer is "
                       "still working with the buyer's AI (step 6).")
    system = (PROMPTS / f"{PROMPT_VERSION}.md").read_text()
    result = provider.generate("offers.advise", OfferAdvice, model_context(deal, table), s=s, module="offers",
                               system=system, prompt_version=PROMPT_VERSION, side="seller")
    adv: OfferAdvice = clean_model(result.output)
    st = _state(deal)
    st["advice"] = {**adv.model_dump(), "mode": result.mode, "model": result.model,
                    "recorded_at": result.recorded_at}
    _save(s, deal, st)
    records.mark_law(s, deal.id, "CP-11", reason=f"The seller's AI presented {len(table)} offers and advised the "
                                                  f"seller ({result.mode}, {result.model})", attached_to="offers")
    if not records.is_done(s, deal.id, "CP-12"):
        records.open_decision(s, deal.id, "CP-12", attached_to="offers")
    record_event(s, actor="ai", kind="ai_action", entity="deal", entity_id=deal.id,
                 summary=f"Offers: AI presented and advised on {len(table)} offers ({result.mode})")
    return st["advice"]


# ---- the seller's decision ----------------------------------------------------------------------------------------

def decide(s: Session, deal: Deal, persona: str, *, decision: str, offer_label: str,
           counter_price: int | None = None, lowest_price: int | None = None, closing_days: int | None = None,
           closing_min: int | None = None, closing_max: int | None = None, inspection_max: int | None = None,
           mortgage_max: int | None = None, allow_requests: bool = False) -> None:
    """CP-12: the seller's own decision. A counter needs a price, the lowest price the AI may agree, and the
    terms the AI may agree (closing-date range, inspection and mortgage periods, the buyer's requests)."""
    cp = records.latest(s, deal.id, "CP-12")
    if cp is None:
        raise records.GateError("CP-11", "The AI has not presented the offers yet.")
    o = offer(deal, offer_label)
    d = {"decision": decision, "offer": offer_label}
    if decision == "counter":
        d.update({k: v if v is not None else DECISION_DEFAULTS[k] for k, v in (
            ("closing_min", closing_min), ("closing_max", closing_max), ("inspection_max", inspection_max),
            ("mortgage_max", mortgage_max))})
        d.update(counter_price=counter_price, lowest_price=lowest_price,
                 closing_days=closing_days or o["closing_days"], allow_requests=bool(allow_requests))
        if not counter_price or not lowest_price or lowest_price > counter_price:
            raise ValueError("A counter needs a price and the lowest price the AI may agree (not above the counter).")
        if not d["closing_min"] <= d["closing_days"] <= d["closing_max"]:
            raise ValueError("The counter's closing date must sit inside the closing range you allow.")
        reason = (f"The seller countered offer {offer_label}: ${counter_price:,}, closing in {d['closing_days']} "
                  f"days, inspection at most {d['inspection_max']} days, mortgage commitment at most "
                  f"{d['mortgage_max']} days, requests {'allowed' if allow_requests else 'not agreed'}; the AI may "
                  f"agree down to ${lowest_price:,} and a closing {d['closing_min']} to {d['closing_max']} days out")
    else:
        reason = f"The seller chose to {decision} offer {offer_label}"
    records.decide(s, cp, persona=persona, decision=decision, reason=reason)
    st = _state(deal)
    st["decision"] = d
    st["thread"] = []
    st.pop("back_to_seller", None)
    _save(s, deal, st)
    if decision == "accept":
        agree(s, deal, {k: o[k] for k in TERM_KEYS}, by="the seller (accepted as offered)")


def counter_terms(deal: Deal, price: int | None = None) -> dict:
    """The seller's counter on the decided offer: the offer's terms with the seller's price, closing date and
    limits applied."""
    d = _state(deal)["decision"]
    o = offer(deal, d["offer"])
    return {**{k: o[k] for k in TERM_KEYS}, "price": price or d["counter_price"], "closing_days": d["closing_days"],
            "inspection_days": min(o["inspection_days"], d["inspection_max"]),
            "mortgage_days": min(o["mortgage_days"], d["mortgage_max"]),
            "requests": list(o["requests"]) if d["allow_requests"] else []}


def outside_decision(deal: Deal, terms: dict, *, agreeing: bool = False) -> list[str]:
    """Code, not the model: every way `terms` falls outside the seller's decision. Empty = inside it."""
    d = _state(deal).get("decision") or {}
    if d.get("decision") != "counter":
        return ["the seller has not decided to counter (CP-12)"]
    o = offer(deal, d["offer"])
    out = []
    price = int(terms.get("price") or 0)
    if price < d["lowest_price"]:
        out.append(f"${price:,} is below the lowest price the seller allowed (${d['lowest_price']:,})")
    if not agreeing and price > d["counter_price"]:
        out.append(f"${price:,} is above the seller's own counter (${d['counter_price']:,})")
    cd = int(terms.get("closing_days") or o["closing_days"])
    if not d["closing_min"] <= cd <= d["closing_max"]:
        out.append(f"a closing in {cd} days is outside the seller's range ({d['closing_min']} to "
                   f"{d['closing_max']} days)")
    if int(terms.get("inspection_days", o["inspection_days"])) > d["inspection_max"]:
        out.append(f"an inspection period of {terms.get('inspection_days')} days is longer than the seller allows "
                   f"({d['inspection_max']})")
    if int(terms.get("mortgage_days", o["mortgage_days"])) > d["mortgage_max"]:
        out.append(f"a mortgage-commitment period of {terms.get('mortgage_days')} days is longer than the seller "
                   f"allows ({d['mortgage_max']})")
    if int(terms.get("deposit_pct", o["deposit_pct"])) < o["deposit_pct"]:
        out.append("a smaller deposit than offered")
    if terms.get("financing", o["financing"]) != o["financing"]:
        out.append("different financing")
    extra = [c for c in terms.get("contingencies", o["contingencies"]) if c not in o["contingencies"]]
    if extra:
        out.append("new contingencies: " + "; ".join(extra))
    reqs = terms.get("requests", [])
    if reqs and not d["allow_requests"]:
        out.append("the buyer's requests (" + "; ".join(reqs) + ") were not agreed by the seller")
    if [r for r in reqs if r not in o["requests"]]:
        out.append("new requests")
    if int(terms.get("seller_credit") or 0) > 0:
        out.append(f"a seller credit of ${int(terms['seller_credit']):,}, which the seller did not allow")
    return out


def check_counter(deal: Deal, terms: dict) -> None:
    problems = outside_decision(deal, terms)
    if problems:
        raise CounterRefused("Refused by code, not sent: " + "; ".join(problems) + ". It goes back to the seller "
                             "as a new decision (CP-12).")


# ---- negotiation (the seller's AI) ---------------------------------------------------------------------------------

def send_counter(s: Session, deal: Deal, terms: dict) -> dict:
    """The seller's AI sends a counter. Code checks it against the seller's decision first."""
    check_counter(deal, terms)
    st = _state(deal)
    d = st["decision"]
    terms = {**counter_terms(deal), **terms}
    st.setdefault("thread", []).append({"from": "seller's AI", "terms": terms,
                                        "note": f"Counter on offer {d['offer']}: {terms_text(terms)}, other terms "
                                                f"as offered. {NOT_BINDING}"})
    _save(s, deal, st)
    records.mark_law(s, deal.id, "CP-13", reason=f"The seller's AI countered offer {d['offer']}: {terms_text(terms)}, "
                                                  "inside the seller's decision", attached_to="offers:seller")
    if d["offer"] == "A":
        _outside_agent_reply(s, deal)
    else:
        from app.modules.buyer import service as buyer

        buyer.counter_received(s, deal, terms)
    return _state(deal)


def _outside_agent_reply(s: Session, deal: Deal) -> None:
    st = _state(deal)
    n = len([t for t in st["thread"] if t["from"] != "seller's AI"])
    if n < len(A_REPLIES):
        last = st["thread"][-1]["terms"]
        reply = {**last, **A_REPLIES[n]}
        if reply["price"] >= last["price"]:
            reply = {**last, "action": "accept"}
        else:
            reply["action"] = "counter"
        receive_reply(s, deal, reply, frm="buyer's agent (simulated other firm)")


def receive_reply(s: Session, deal: Deal, reply: dict, frm: str = "buyer's AI") -> dict:
    """A reply from the buyer's side. Inside the seller's decision, the seller's AI agrees on its own; outside it,
    the AI counters again within the decision, or sends it back to the seller."""
    st = _state(deal)
    terms = {k: reply[k] for k in TERM_KEYS if k in reply}
    st.setdefault("thread", []).append({"from": frm, "terms": {**st["thread"][-1]["terms"], **terms},
                                        "action": reply.get("action", "counter"),
                                        "note": f"{reply.get('action', 'counter').replace('_', ' ').capitalize()}: "
                                                f"{terms_text({**st['thread'][-1]['terms'], **terms})}. {NOT_BINDING}"})
    _save(s, deal, st)
    action = reply.get("action", "counter")
    if action == "walk_away":
        st = _state(deal)
        st["ended"] = f"The {frm} walked away"
        _save(s, deal, st)
        return st
    full = _state(deal)["thread"][-1]["terms"]
    if action == "accept" or not outside_decision(deal, full, agreeing=True):
        agree(s, deal, full, by=f"the seller's AI, inside the seller's decision ({frm} "
                                f"{'accepted' if action == 'accept' else 'proposed'} it)")
        records.mark_law(s, deal.id, "CP-13", reason=f"The seller's AI agreed {terms_text(full)} with the {frm}, "
                                                      "inside the seller's decision", attached_to="offers:seller")
        return _state(deal)
    return negotiate(s, deal)  # outside the decision: the seller's AI answers on its own, within it


def negotiate(s: Session, deal: Deal) -> dict:
    """The seller's AI takes its next step within the seller's decision: open with the seller's counter; after a
    reply outside the decision, meet it halfway (never below the seller's lowest price) and pull its terms back
    inside the decision; if nothing inside the decision is left to offer, send it back to the seller."""
    st = _state(deal)
    d = st.get("decision") or {}
    if st.get("accepted") or st.get("ended") or d.get("decision") != "counter":
        return st
    thread = st.get("thread") or []
    if not thread:
        return send_counter(s, deal, counter_terms(deal))
    last = thread[-1]
    if last["from"] == "seller's AI":
        return st  # waiting for the buyer's side
    mine = [t["terms"] for t in thread if t["from"] == "seller's AI"][-1]
    theirs = last["terms"]
    if theirs["price"] >= d["lowest_price"]:  # only their terms were outside: keep their price, fix the terms
        price = min(theirs["price"], d["counter_price"])
    else:
        price = max(d["lowest_price"], (mine["price"] + theirs["price"]) // 2 // 1000 * 1000)
    if price >= mine["price"] and theirs["price"] < d["lowest_price"]:
        price = d["lowest_price"] if mine["price"] > d["lowest_price"] else None
    if price is None:
        back_to_seller(s, deal, f"The buyer's side is at {terms_text(theirs)}; the seller's lowest price "
                                f"(${d['lowest_price']:,}) is already on the table.")
        return _state(deal)
    terms = {**mine, "price": price,
             "closing_days": min(max(int(theirs.get("closing_days", mine["closing_days"])), d["closing_min"]),
                                 d["closing_max"]),
             "inspection_days": min(int(theirs.get("inspection_days", mine["inspection_days"])),
                                    d["inspection_max"]),
             "mortgage_days": min(int(theirs.get("mortgage_days", mine["mortgage_days"])), d["mortgage_max"])}
    return send_counter(s, deal, terms)


def back_to_seller(s: Session, deal: Deal, why: str) -> None:
    st = _state(deal)
    st["back_to_seller"] = why
    _save(s, deal, st)
    records.open_decision(s, deal.id, "CP-12", reason=f"Back to the seller: {why}", attached_to="offers")


def agree(s: Session, deal: Deal, terms: dict, *, by: str) -> dict:
    st = _state(deal)
    label = (st.get("decision") or {}).get("offer", "A")
    o = offer(deal, label)
    st["accepted"] = {**{k: o[k] for k in TERM_KEYS}, **terms, "label": label, "party": o["party"],
                      "side": o["side"], "final_price": terms["price"], "agreed_by": by}
    _save(s, deal, st)
    deal.current_step = max(deal.current_step, 7)
    record_event(s, actor="ai", kind="ai_action", entity="deal", entity_id=deal.id,
                 summary=f"Offers: agreed with offer {label}'s buyer: {terms_text(terms)} ({by}). {NOT_BINDING}")
    if o["side"] == "firm_buyer":
        from app.modules.buyer import service as buyer

        buyer.agreed(s, deal, st["accepted"])
    return st["accepted"]
