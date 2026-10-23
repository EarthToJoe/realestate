"""The one-button path (decisions 47 to 51), built on the milestones in app/demo/walk.py.

- `primary(s, deal, stop)`: the one primary action of a screen: the next undone milestone on it, worded for what it
  does ("Let the AI price the house", "Seller: list at $640,000"), else "Continue: <next step>".
- `pump(s, provider, ...)`: after a person acts, the AI does its own work as soon as what it waits for is done,
  up to the next decision a client or a person must make ("You play the seller and the buyer; the AI does
  everything else"). Each AI act is still its own record, shown on its own screen.
- `change_plan` / `apply_change`: "Change" re-opens a decision and undoes only what depends on it, superseding
  records (never deleting them), and records the change on the timeline (decision 48).
- `page_context`: what every page needs: the progress list, Back, the action bar, the "not yet" card.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.audit import record_event
from app.demo import walk
from app.demo.walk import BY_KEY, WALK, Milestone, is_done
from app.models import Deal, Disclosure, Document, FairHousingResult, Message, PropertyFact
from app.records import service as records
from app.web import current_deal, presenting, screen_for, steps, stops

SALE = [m for m in WALK if m.route != "/brand"]
FIRM = [m for m in WALK if m.route == "/brand"]
# Steps a person may leave for later without holding up what comes after (the AI carries on past them).
SKIPPABLE = {"mls", "seller_answers"}


@dataclass
class Action:
    label: str
    kind: str  # ai | seller | buyer | person | form | continue | link
    url: str | None = None  # POST target (None for a link)
    href: str | None = None  # for a link
    form: str | None = None  # the id of the on-page form this button submits
    fields: dict = field(default_factory=dict)  # hidden fields
    name: str | None = None  # a submit button's name/value (a choice on the form)
    value: str | None = None
    key: str | None = None  # the milestone
    label_template: str | None = None  # "Seller: list at {price}": the script fills in the figure as it is typed

    @property
    def working(self) -> bool:
        return self.kind == "ai" or self.key in AI_FOLLOWS


# ---- labels --------------------------------------------------------------------------------------------------------

def _money(v) -> str:
    try:
        return f"${int(v):,}"
    except (TypeError, ValueError):
        return ""


AI_LABEL = {
    "infer": "Let the AI fill the gaps", "accept": "Let the AI accept the listing",
    "advice": "Let the AI price the house", "copy": "Let the AI write the listing",
    "copy_ready": "Let the AI mark the checked copy ready", "enquiries": "Let the enquiries arrive",
    "alert": "Let the buyer's AI search for homes", "tour": "Let the AI book a tour",
    "offer_advice": "Let the buyer's AI draft the offer", "offers_advice": "Let the seller's AI present the offers",
    "agreed": "Let the AIs negotiate", "contract": "Let the AI draft the contract",
    "attach": "Let the AI attach the disclosures", "signing": "Let the AI open the contract for signing",
    "campaign": "Let the AI write the firm's campaign", "targeting": "Let the AI choose who sees the ad",
    "publish": "Let the AI publish the campaign",
}
# What the AI did, for the one-line confirmation.
AI_DID = {
    "infer": "the AI filled the gaps in the public record", "accept": "the AI accepted the listing",
    "advice": "the AI priced the house (step 4)", "copy": "the AI wrote the listing and checked it (step 5)",
    "copy_ready": "marked the checked copy ready to publish",
    "enquiries": "eight enquiries arrived and the AI answered them", "alert": "the buyer's AI sent a search alert",
    "tour": "the AI booked a tour", "offer_advice": "the buyer's AI drafted an offer (step 9)",
    "offers_advice": "the seller's AI presented both offers (step 10)",
    "contract": "the AI drafted the contract (step 11)", "attach": "attached the disclosures",
    "signing": "opened the contract for signing", "campaign": "the AI wrote the firm's campaign",
    "targeting": "chose who sees the ad", "publish": "published it (simulated)",
}
# Client acts that the AI's work follows at once: their buttons also say "The AI is working…" while it runs.
AI_FOLLOWS = {"intake", "agency", "listing", "price", "authority", "buyer_agreement", "dual_agency", "offer",
              "seller_decision", "agreed", "pcds", "buyer"}
DECLINE = {"agency": ("refuse_with_declaration", "Seller: refuse, with a signed declaration"),
           "listing": ("decline", "Seller: decline"), "buyer_agreement": ("decline", "Buyer: decline"),
           "authorise": ("decline", "Seller: decline"), "authority": ("decline", "Seller: decline")}


def _party_next(s: Session, deal: Deal, code: str, order=("buyer", "seller")) -> str:
    cp = records.latest(s, deal.id, code)
    got = (cp.decision or "") if cp else ""
    return next((p for p in order if f"{p}=" not in got), order[0])


def action_for(s: Session, deal: Deal, m: Milestone) -> tuple[Action, list[Action]]:
    """The primary button for milestone `m`, and its quiet secondary choices."""
    act = f"/path/act/{m.key}"
    if m.who == "ai":
        return Action(AI_LABEL[m.key], "ai", url=act, key=m.key), []
    if m.who == "person":
        return Action("A person at the firm keys in the MLS listing (simulated)", "person", url=act, key=m.key), []
    k = m.key
    if k == "intake":
        return Action("Save and continue", "form", form="intake-form", key=k), []
    if k == "buyer":
        return Action("Save the buyer's answers", "form", form="buyer-form", key=k), []
    if k == "agency":
        return (Action("Seller: acknowledge the agency form", "seller", url=act, fields={"as": "seller",
                       "choice": "acknowledge"}, key=k),
                [Action(DECLINE[k][1], "seller", url=act, fields={"as": "seller", "choice": DECLINE[k][0]}, key=k)])
    if k == "listing":
        return (Action("Seller: sign the listing agreement", "seller", url=act,
                       fields={"as": "seller", "choice": "sign"}, key=k),
                [Action(DECLINE[k][1], "seller", url=act, fields={"as": "seller", "choice": "decline"}, key=k)])
    if k == "price":
        from app.modules.pricing import service as pricing

        pa = pricing.current(s, deal)
        rec = (pa.advice or {}).get("recommended_price") if pa else None
        return Action(f"Seller: list at {_money(deal.list_price or rec)}", "seller", form="price-form", key=k,
                      label_template="Seller: list at {price}"), []
    if k == "authorise":
        return (Action("Seller: sign the marketing plan", "seller", form="authorise-form", name="decision",
                       value="sign", key=k),
                [Action(DECLINE[k][1], "seller", form="authorise-form", name="decision", value="decline", key=k)])
    if k == "authority":
        return (Action("Seller: approve what the AI may say", "seller", form="authority-form", name="decision",
                       value="approve", key=k),
                [Action(DECLINE[k][1], "seller", form="authority-form", name="decision", value="decline", key=k)])
    if k == "seller_answers":
        return Action("Seller: send my answers", "seller", form="answers-form", key=k), []
    if k == "buyer_agreement":
        return (Action("Buyer: sign the buyer agreement", "buyer", url=act, fields={"as": "buyer", "choice": "sign"},
                       key=k),
                [Action(DECLINE[k][1], "buyer", url=act, fields={"as": "buyer", "choice": "decline"}, key=k)])
    if k in ("dual_agency", "signed"):
        p = _party_next(s, deal, m.code, ("buyer", "seller") if k == "dual_agency" else ("seller", "buyer"))
        verb = "consent to dual agency" if k == "dual_agency" else "sign the contract"
        yes = "consent" if k == "dual_agency" else "sign"
        return (Action(f"{p.capitalize()}: {verb}", p, url=act, fields={"as": p, "choice": yes}, key=k),
                [Action(f"{p.capitalize()}: decline", p, url=act, fields={"as": p, "choice": "decline"}, key=k)])
    if k == "offer":
        from app.modules.buyer import service as buyer

        adv = buyer.state(deal).get("advice") or {}
        return (Action(f"Buyer: send this offer at {_money(adv.get('recommended_price'))}", "buyer",
                       form="offer-form", name="decision", value="approve", key=k,
                       label_template="Buyer: send this offer at {price}"),
                [Action("Buyer: not now", "buyer", form="offer-form", name="decision", value="decline", key=k)])
    if k == "seller_decision":
        from app.modules.offers import service as offers

        rd = walk.recorded_decision(deal)
        lab = rd["offer_label"]
        return (Action(f"Seller: counter offer {lab} at {_money(rd['counter_price'])}", "seller", form="decide-form",
                       name="decision", value="counter", key=k, label_template="Seller: counter at {counter_price}"),
                [Action(f"Seller: accept offer {lab} as offered", "seller", form="decide-form", name="decision",
                        value="accept", key=k),
                 Action("Seller: reject", "seller", form="decide-form", name="decision", value="reject", key=k)])
    if k == "pcds":
        return Action("Seller: submit my disclosure form", "seller", url=act, fields={"as": "seller",
                      "choice": "complete"}, key=k), []
    if k == "agreed":
        nxt = walk.negotiation_next(s, deal)
        if nxt == "buyer":
            from app.modules.buyer import service as buyer

            ca = buyer.state(deal).get("counter_advice") or {}
            verb = "accept the counter" if ca.get("action") == "accept" else "reply"
            return (Action(f"Buyer: {verb} at {_money(ca.get('price'))}", "buyer", form="reply-form",
                           name="decision", value="approve", key=k, label_template=f"Buyer: {verb} at {{price}}"),
                    [Action("Buyer: not this reply", "buyer", form="reply-form", name="decision", value="decline",
                            key=k)])
        return Action(AI_LABEL["agreed"], "ai", url=act, key=k), []
    raise KeyError(k)


def next_milestone(s: Session, deal: Deal | None, route: str) -> Milestone | None:
    if deal is None:
        return BY_KEY["intake"] if route == "/intake" else None
    return next((m for m in walk.on_screen(route) if not is_done(s, deal, m)), None)


def _next_stop(stop: dict) -> dict | None:
    all_ = stops()
    i = next((j for j, x in enumerate(all_) if x["route"] == stop["route"]), None)
    return all_[i + 1] if i is not None and i + 1 < len(all_) else None


def _prev_stop(stop: dict) -> dict | None:
    all_ = stops()
    i = next((j for j, x in enumerate(all_) if x["route"] == stop["route"]), None)
    return all_[i - 1] if i else None


def continue_action(stop: dict) -> Action | None:
    nxt = _next_stop(stop)
    if stop["key"] == "finale":
        return Action(nxt["title"], "continue", href=nxt["route"])
    if stop["key"] == "firm":
        return Action("Finish: back to the home page", "continue", href="/")
    return Action(f"Continue: {nxt['title']}", "continue", href=nxt["route"]) if nxt else None


def primary(s: Session, deal: Deal | None, stop: dict) -> tuple[Action | None, list[Action]]:
    """The one primary action of a screen, and its quiet secondary choices (decision 47)."""
    if stop["route"] == "/intake":
        return action_for(s, deal, BY_KEY["intake"])
    m = next_milestone(s, deal, stop["route"])
    if m is None:
        return continue_action(stop), []
    return action_for(s, deal, m)


# ---- the AI pump ------------------------------------------------------------------------------------------------

def _deps_done(s: Session, deal: Deal, m: Milestone) -> bool:
    return all(is_done(s, deal, BY_KEY[d]) for d in walk.DEPS.get(m.key, ()) if d in BY_KEY)


class AIStopped(Exception):
    """The AI could not do its next act; `message` says why in plain words. What came before is kept."""

    def __init__(self, message: str, key: str):
        super().__init__(message)
        self.message = message
        self.key = key


def plain_failure(exc: Exception, recorded: bool) -> str:
    from app.model.provider import ReplayMiss, SpendCapReached

    if isinstance(exc, ReplayMiss):
        return ("This recorded demo has the AI's answers only for the figures and choices it was recorded with, "
                "and this situation is new, so the AI did not run. Put the recorded figures back (the Change links "
                "do it), or try anything in the live demo.")
    if isinstance(exc, SpendCapReached):
        return ("The live demo has used its whole AI budget, so the AI did not run. The recorded demo still works "
                "end to end.")
    msg = getattr(exc, "message", None) or str(exc)
    return msg


def pump(s: Session, provider, *, firm: bool = False) -> list[str]:
    """The AI does its own work, in path order, as soon as what it waits for is done; it stops at the first decision
    a client or a person must make. Commits after each act. Returns the keys it played; raises AIStopped (after
    keeping everything played) when an act cannot run."""
    seq = FIRM if firm else SALE
    played: list[str] = []
    for _ in range(60):
        deal = current_deal(s)
        if deal is None:
            return played
        progressed = False
        for m in seq:
            if is_done(s, deal, m):
                continue
            ai_turn = m.who == "ai" or (m.key == "agreed" and walk.negotiation_next(s, deal) in ("seller_ai",
                                                                                              "buyer_ai"))
            if ai_turn and _deps_done(s, deal, m):
                try:
                    if m.key == "agreed":
                        walk._negotiate_ai(s, deal, provider)
                    else:
                        m.play(s, deal, provider)
                    s.commit()
                except Exception as e:  # noqa: BLE001 (every failure is reported in plain words; nothing is lost)
                    s.rollback()
                    raise AIStopped(plain_failure(e, provider.mode == "replay"), m.key) from e
                played.append(m.key)
                progressed = True
                break
            if m.key in SKIPPABLE:
                continue
            return played
        if not progressed:
            return played
    return played


def did_text(keys: list[str], s: Session, deal: Deal | None) -> str:
    parts = []
    for k in keys:
        if k == "agreed":
            from app.modules.offers import service as offers

            acc = offers.state(deal).get("accepted") if deal else None
            parts.append(f"the AIs agreed at {_money(acc['final_price'])}" if acc else
                         "the seller's AI sent the counter and the buyer's AI advised the buyer")
        elif k in AI_DID:
            parts.append(AI_DID[k])
    seen, out = set(), []
    for p in parts:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return ", ".join(out)


def after_action(s: Session, provider, done: str, *, firm: bool = False) -> str:
    """Run the pump after a person's act and write the one-line confirmation: what they did, then what the AI did.
    The person's act is committed first, so nothing the AI cannot do undoes it."""
    s.commit()
    try:
        keys = pump(s, provider, firm=firm)
        ai = did_text(keys, s, current_deal(s))
        return f"{done}. Then {ai}." if ai else f"{done}."
    except AIStopped as e:
        return f"{done}. {e.message}"


# ---- Change (decision 48) -------------------------------------------------------------------------------------

CHANGEABLE = {"agency", "listing", "price", "authorise", "authority", "seller_answers", "buyer_agreement",
              "dual_agency", "offer", "seller_decision", "agreed", "pcds", "signed"}
CHANGE_LABEL = {
    "agency": "the agency form", "listing": "the listing agreement", "price": "the list price",
    "authorise": "the marketing plan", "authority": "what the AI may say", "seller_answers": "the seller's answers",
    "buyer_agreement": "the buyer agreement", "dual_agency": "the dual-agency consents", "offer": "the buyer's offer",
    "seller_decision": "the seller's decision on the offers", "agreed": "the negotiation",
    "pcds": "the seller's disclosure form", "signed": "the signatures", "house": "the house's address and facts",
    "buyer_needs": "the buyer's answers",
}
WHAT_REOPENS = {
    "infer": "the AI's research", "accept": "the AI accepting the listing", "listing": "the listing agreement",
    "advice": "the AI's price advice", "price": "the list price", "copy": "the listing copy",
    "copy_ready": "the copy marked ready", "authorise": "the marketing plan", "mls": "the MLS entry",
    "authority": "what the AI may say", "enquiries": "the enquiries and the AI's replies",
    "seller_answers": "the seller's answers", "buyer_agreement": "the buyer agreement",
    "alert": "the buyer's search alert", "tour": "the tour", "dual_agency": "the dual-agency consents",
    "offer_advice": "the buyer's AI's offer", "offer": "the buyer's offer", "offers_advice": "the seller's AI's advice",
    "seller_decision": "the seller's decision on the offers", "agreed": "the negotiation",
    "contract": "the contract draft", "pcds": "the seller's disclosure form", "attach": "the attached disclosures",
    "signing": "the contract's signing", "signed": "the signatures",
}


def started(s: Session, deal: Deal, m: Milestone) -> bool:
    """Done, or part-done (one of two consents, a negotiation under way)."""
    if is_done(s, deal, m):
        return True
    if m.key in ("dual_agency", "signed"):
        cp = records.latest(s, deal.id, m.code)
        return bool(cp and cp.decision)
    if m.key == "agreed":
        from app.modules.offers import service as offers

        return bool(offers.state(deal).get("thread"))
    return False


def change_plan(s: Session, deal: Deal, key: str) -> list[Milestone]:
    """What changing `key` re-opens besides itself: the dependents already done or started, in path order."""
    roots = {key}
    return [m for m in walk.dependents(roots) if started(s, deal, m)]


def reopens_text(ms: list[Milestone]) -> str:
    """'the listing copy (step 5) and the marketing plan (step 6)'."""
    names = [f"{WHAT_REOPENS.get(m.key, m.what)} (step {m.step})" if m.step else WHAT_REOPENS.get(m.key, m.what)
             for m in ms]
    if not names:
        return ""
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def apply_change(s: Session, provider, deal: Deal, key: str, *, why: str | None = None) -> str:
    """Re-open `key` (a client decision, or the virtual "house" / "buyer_needs") and undo what depends on it, newest
    first; records are superseded, never deleted; the change itself is an event on the timeline. Returns the
    one-line confirmation."""
    deps = change_plan(s, deal, key)
    label = CHANGE_LABEL.get(key, key)
    why = why or f"the client changed {label}"
    for m in reversed(deps):
        UNDO[m.key](s, deal, why)
        s.flush()
    if key in UNDO:
        UNDO[key](s, deal, why)
    s.flush()
    record_event(s, actor="system", kind="change", entity="deal", entity_id=deal.id,
                 summary=f"Change: {label} re-opened" + (f"; also re-opened: {reopens_text(deps)}" if deps else ""))
    s.commit()
    return f"Re-opened {label}." + (f" Also re-opened: {reopens_text(deps)}." if deps else " Nothing else changed.")


# Each undo puts one milestone back to "not done": its records superseded (or a decision re-opened as a new pending
# record), its module state cleared. Nothing in the audit log is removed.

def _undo_infer(s, deal, why):
    s.execute(delete(PropertyFact).where(PropertyFact.property_id == deal.property_id,
                                         PropertyFact.group == "Inferred by the AI"))
    s.flush()
    s.refresh(deal.property)


def _undo_agency(s, deal, why):
    records.reopen(s, deal.id, "CP-01", why=why)
    for d in s.execute(select(Disclosure).where(Disclosure.deal_id == deal.id, Disclosure.kind == "agency")).scalars():
        d.acknowledged_at = None


def _undo_accept(s, deal, why):
    records.supersede(s, deal.id, "CP-02", why=why)
    records.supersede(s, deal.id, "CP-03", why=why, where=lambda cp: cp.status == "pending")
    deal.status = "intake"


def _undo_listing(s, deal, why):
    if records.latest(s, deal.id, "CP-02"):
        records.reopen(s, deal.id, "CP-03", why=why)
    else:
        records.supersede(s, deal.id, "CP-03", why=why)
    for doc in s.execute(select(Document).where(Document.deal_id == deal.id,
                                                Document.kind == "listing_agreement")).scalars():
        doc.signed_by = None
    deal.status = "listing_offered"


def _undo_advice(s, deal, why):
    from app.modules.pricing import service as pricing

    pa = pricing.current(s, deal)
    if pa is not None:
        pa.advice = None
    records.supersede(s, deal.id, "CP-25", why=why)


def _undo_price(s, deal, why):
    if records.latest(s, deal.id, "CP-25"):
        records.reopen(s, deal.id, "CP-05", why=why)
    else:
        records.supersede(s, deal.id, "CP-05", why=why)


def _delete_messages(s, deal, msgs: list[Message], why: str):
    ids = {m.id for m in msgs}
    if not ids:
        return
    for code in ("CP-09", "CP-24", "CP-28", "CP-29"):
        records.supersede(s, deal.id, code, why=why, where=lambda cp: cp.attached_to in {f"message:{i}" for i in ids})
    s.execute(delete(FairHousingResult).where(FairHousingResult.entity == "message",
                                              FairHousingResult.entity_id.in_(ids)))
    s.execute(delete(Message).where(Message.id.in_(ids)))
    s.flush()


def _undo_copy(s, deal, why):
    from app.models import CopyArtifact

    arts = [a for a in s.execute(select(CopyArtifact).where(CopyArtifact.deal_id == deal.id)).scalars()
            if not a.channel.startswith("brand_")]
    ids = {a.id for a in arts}
    records.supersede(s, deal.id, "CP-26", why=why, where=lambda cp: cp.step == 3)
    records.supersede(s, deal.id, "CP-06", why=why)
    if ids:
        s.execute(delete(FairHousingResult).where(FairHousingResult.entity == "copy_artifact",
                                                  FairHousingResult.entity_id.in_(ids)))
        s.execute(delete(CopyArtifact).where(CopyArtifact.id.in_(ids)))
    s.flush()


def _undo_copy_ready(s, deal, why):
    from app.modules.listing_copy import service as copy

    for a in copy.artifacts(s, deal):
        if a.status == "ready":
            a.status, a.ready_at = "passed", None
    records.supersede(s, deal.id, "CP-06", why=why)


def _undo_authorise(s, deal, why):
    if records.latest(s, deal.id, "CP-07"):
        records.reopen(s, deal.id, "CP-07", why=why)


def _undo_mls(s, deal, why):
    records.supersede(s, deal.id, "CP-08", why=why)


def _undo_authority(s, deal, why):
    from app.modules.inbox import service as inbox

    if records.latest(s, deal.id, "CP-27"):
        records.reopen(s, deal.id, "CP-27", why=why)
    ins = inbox._instructions(s, deal)
    if ins is not None:
        ins.approved = False
        ins.authority = {k: v for k, v in (ins.authority or {}).items() if k != "self_guided_tours"}


def _undo_enquiries(s, deal, why):
    from app.modules.inbox import service as inbox

    _delete_messages(s, deal, inbox.messages(s, deal), why)
    records.supersede(s, deal.id, "CP-10", why=why, where=lambda cp: cp.step == 5)


def _undo_seller_answers(s, deal, why):
    from app.modules.inbox import service as inbox

    msgs = inbox.messages(s, deal)
    for card in [m for m in msgs if m.direction == "in" and (m.extra or {}).get("seller_choice")]:
        later = [m for m in msgs if m.thread == card.thread and m.direction == "out" and m.id > card.id
                 and m.topic in ("negotiation", "showing")]
        holding = [m for m in msgs if m.thread == card.thread and m.direction == "out" and m.topic == "holding"]
        later = [m for m in later if not holding or m.id > holding[0].id]
        _delete_messages(s, deal, later, why)
        for code in ("CP-28", "CP-29"):
            records.supersede(s, deal.id, code, why=why, where=lambda cp, c=card: cp.attached_to == f"message:{c.id}")
        records.supersede(s, deal.id, "CP-10", why=why,
                          where=lambda cp, c=card: cp.step == 5 and f"thread {c.thread}," in (cp.reason or ""))
        card.status = "to_seller"
        card.extra = {k: v for k, v in (card.extra or {}).items() if k not in ("seller_choice", "showing")}
    record_event(s, actor="system", kind="change", entity="deal", entity_id=deal.id,
                 summary=f"The seller's answers to the questions put to the seller re-opened: {why}")


def _buyer_state(s, deal, *drop):
    from app.modules.buyer import service as buyer

    st = buyer.state(deal)
    for k in drop:
        st.pop(k, None)
    buyer._save(s, deal, st)


def _offer_state(s, deal, *drop):
    from app.modules.offers import service as offers

    st = offers.state(deal)
    for k in drop:
        st.pop(k, None)
    offers._save(s, deal, st)


def _contract_state(s, deal, *drop):
    from app.modules.contract import service as contract

    st = contract.state(deal)
    for k in drop:
        st.pop(k, None)
    contract._save(s, deal, st)


def _undo_buyer_agreement(s, deal, why):
    if records.latest(s, deal.id, "CP-16"):
        records.reopen(s, deal.id, "CP-16", why=why)
    for doc in s.execute(select(Document).where(Document.deal_id == deal.id,
                                                Document.kind == "buyer_agreement")).scalars():
        doc.signed_by = None


def _buyer_msgs(s, deal, topic):
    from app.modules.inbox import service as inbox

    return [m for m in inbox.messages(s, deal, "buyer") if m.topic == topic]


def _undo_alert(s, deal, why):
    _delete_messages(s, deal, _buyer_msgs(s, deal, "alert"), why)
    _buyer_state(s, deal, "search")


def _undo_tour(s, deal, why):
    _delete_messages(s, deal, _buyer_msgs(s, deal, "showing"), why)
    for code in ("CP-28", "CP-29"):
        records.supersede(s, deal.id, code, why=why, where=lambda cp: cp.attached_to == "buyer:tour")
    records.supersede(s, deal.id, "CP-10", why=why, where=lambda cp: cp.step == 8)
    records.supersede(s, deal.id, "CP-17", why=why)
    _buyer_state(s, deal, "tour")


def _undo_dual_agency(s, deal, why):
    if records.latest(s, deal.id, "CP-17"):
        records.reopen(s, deal.id, "CP-17", why=why)


def _undo_offer_advice(s, deal, why):
    records.supersede(s, deal.id, "CP-31", why=why, where=lambda cp: cp.attached_to == "buyer:offer")
    records.supersede(s, deal.id, "CP-18", why=why,
                      where=lambda cp: cp.attached_to == "buyer:offer" and cp.status == "pending")
    _buyer_state(s, deal, "advice")


def _undo_offer(s, deal, why):
    from app.modules.buyer import service as buyer

    if buyer.state(deal).get("advice"):
        records.reopen(s, deal.id, "CP-18", why=why, attached_to="buyer:offer",
                       where=lambda cp: cp.attached_to == "buyer:offer")
    else:
        records.supersede(s, deal.id, "CP-18", why=why, where=lambda cp: cp.attached_to == "buyer:offer")
    _buyer_state(s, deal, "offer")
    _offer_state(s, deal, "offer_b")


def _undo_offers_advice(s, deal, why):
    records.supersede(s, deal.id, "CP-11", why=why)
    records.supersede(s, deal.id, "CP-12", why=why, where=lambda cp: cp.status == "pending")
    _offer_state(s, deal, "advice")


def _undo_seller_decision(s, deal, why):
    from app.modules.offers import service as offers

    if offers.state(deal).get("advice"):
        records.reopen(s, deal.id, "CP-12", why=why, attached_to="offers")
    else:
        records.supersede(s, deal.id, "CP-12", why=why)
    _offer_state(s, deal, "decision", "thread", "back_to_seller")


def _undo_agreed(s, deal, why):
    records.supersede(s, deal.id, "CP-13", why=why)
    records.supersede(s, deal.id, "CP-31", why=why, where=lambda cp: cp.attached_to == "buyer:counter")
    records.supersede(s, deal.id, "CP-18", why=why, where=lambda cp: cp.attached_to == "buyer:counter")
    _offer_state(s, deal, "thread", "accepted", "ended", "back_to_seller")
    _buyer_state(s, deal, "counters", "replies", "agreed", "counter_advice")


def _undo_contract(s, deal, why):
    records.supersede(s, deal.id, "CP-14", why=why)
    records.supersede(s, deal.id, "CP-32", why=why)
    _contract_state(s, deal, "draft", "findings", "passed", "mode", "model", "recorded_at", "memorandum", "attached",
                    "signed_at")


def _undo_pcds(s, deal, why):
    records.reopen(s, deal.id, "CP-04", why=why)
    for d in s.execute(select(Disclosure).where(Disclosure.deal_id == deal.id, Disclosure.kind == "pcds")).scalars():
        d.answers, d.acknowledged_at, d.delivered_at = None, None, None


def _undo_attach(s, deal, why):
    records.supersede(s, deal.id, "CP-32", why=why, where=lambda cp: cp.attached_to == "contract:disclosures")
    _contract_state(s, deal, "attached")


def _undo_signing(s, deal, why):
    records.supersede(s, deal.id, "CP-33", why=why)


def _undo_signed(s, deal, why):
    from app.modules.contract import service as contract

    if records.latest(s, deal.id, "CP-33"):
        records.reopen(s, deal.id, "CP-33", why=why)
    _contract_state(s, deal, "signed_at")
    st = contract.state(deal)
    for doc in s.execute(select(Document).where(Document.deal_id == deal.id,
                                                Document.kind.in_(("contract_draft", "rider")),
                                                Document.version == st.get("version"))).scalars():
        doc.signed_by = None
    deal.status = "listed"


UNDO = {
    "infer": _undo_infer, "agency": _undo_agency, "accept": _undo_accept, "listing": _undo_listing,
    "advice": _undo_advice, "price": _undo_price, "copy": _undo_copy, "copy_ready": _undo_copy_ready,
    "authorise": _undo_authorise, "mls": _undo_mls, "authority": _undo_authority, "enquiries": _undo_enquiries,
    "seller_answers": _undo_seller_answers, "buyer_agreement": _undo_buyer_agreement, "alert": _undo_alert,
    "tour": _undo_tour, "dual_agency": _undo_dual_agency, "offer_advice": _undo_offer_advice, "offer": _undo_offer,
    "offers_advice": _undo_offers_advice, "seller_decision": _undo_seller_decision, "agreed": _undo_agreed,
    "contract": _undo_contract, "pcds": _undo_pcds, "attach": _undo_attach, "signing": _undo_signing,
    "signed": _undo_signed,
}


# ---- where a record sits on the path (the finale groups the timeline by step) ------------------------------------

SC_TO_STEP = {1: 1, 2: 4, 3: 5, 4: 6, 5: 7, 8: 8, 6: 10, 7: 11, 9: "finale", 10: "firm"}
CODE_STEP = {"CP-01": 3, "CP-02": 3, "CP-03": 3, "CP-04": 11, "CP-17": 8}


def step_of_record(cp) -> int | str:
    if cp.code in CODE_STEP:
        return CODE_STEP[cp.code]
    att = cp.attached_to or ""
    if cp.code in ("CP-31", "CP-18"):
        return 10 if att == "buyer:counter" else 9
    if cp.code == "CP-13" and att == "offers:buyer":
        return 10
    if cp.code == "CP-24" and cp.step == 1:
        return 1
    if cp.code == "CP-26" and cp.step == 10:
        return "firm"
    return SC_TO_STEP.get(cp.step, cp.step)


# ---- the page context ------------------------------------------------------------------------------------------

def statuses(s: Session, deal: Deal | None) -> dict[str, str]:
    """Per step: "done" (every milestone on it done), "started" (some), "todo" (none). Honest, from the walk."""
    done = walk.done_map(s, deal) if deal else {}
    out = {}
    for st in steps():
        ms = walk.on_screen(st["route"])
        if st["route"] == "/intake":
            out[st["route"]] = "done" if deal else "todo"
            continue
        n = sum(1 for m in ms if done.get(m.key))
        out[st["route"]] = "done" if ms and n == len(ms) else ("started" if n else "todo")
    return out


def resume_route(s: Session, deal: Deal | None) -> str:
    """Where to pick up: the first step with something left to do, else the finale."""
    if deal is None:
        return "/intake"
    st = statuses(s, deal)
    return next((x["route"] for x in steps() if st[x["route"]] != "done"), "/timeline")


def page_context(s: Session, deal: Deal | None, stop: dict | None, request, gate_msg: str | None) -> dict:
    ctx = {"statuses": statuses(s, deal), "bar": None, "secondary": [], "walk_gate": None, "prev_stop": None,
           "next_stop": None, "playable": [], "resume": resume_route(s, deal)}
    if stop is None:
        return ctx
    ctx["prev_stop"], ctx["next_stop"] = _prev_stop(stop), _next_stop(stop)
    gate = walk.gate_for(s, deal, stop["route"], gate_msg)
    ctx["walk_gate"] = gate
    if gate is not None:
        ctx["bar"] = Action(f"Go to step {gate.step['n']}: {gate.step['title']}" if gate.step.get("n")
                            else f"Go to {gate.step['title']}", "link", href=gate.missing.link)
    else:
        try:
            ctx["bar"], ctx["secondary"] = primary(s, deal, stop)
        except Exception:  # noqa: BLE001 (a state the bar has no button for: Continue keeps the path walkable)
            ctx["bar"], ctx["secondary"] = continue_action(stop), []
    if presenting(request):
        ctx["playable"] = walk.playable(s, deal, stop["route"])
    return ctx
