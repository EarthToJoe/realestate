"""The demo's scripted walk, for the Presenter: what each screen is waiting for, and fast-forward.

The walk is a list of milestones in the demo's walk order (steps 1 to 5, 8, 6, 7: decision 34), each with a check
("is it done in the current deal?") and a play ("do it the way the demo does"). The plays make exactly the choices
`scripts/live-flow.sh` makes, through the same service calls the screens use, so model calls hit the recorded
replays ($0). Client decisions are recorded as the client's (persona "seller" or "buyer"); the record service still
checks that, so nothing here can decide for the wrong person.

- `gate_for(s, deal, path)`: the first thing a screen is waiting for (what, on which step, who), or None. Screens
  show it as the gate card instead of redirecting.
- `fast_forward(s, provider, n)`: plays every milestone before step n in walk order that is not done yet.

The service-layer gates are untouched: this module only ever calls them the way a person clicking would.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Deal, Message
from app.records import catalogue
from app.records import service as records
from app.web import current_deal, steps

WHO_LABEL = {"ai": "The AI", "seller": "The seller", "buyer": "The buyer", "seller_and_buyer": "The seller and the buyer",
             "presenter": "The Presenter (a simulated human step)"}


@dataclass(frozen=True)
class Milestone:
    key: str
    step: int
    what: str  # plain words: what is missing
    who: str  # ai | seller | buyer | seller_and_buyer | presenter
    route: str  # the screen where it is done
    done: Callable[[Session, Deal], bool]
    play: Callable[[Session, Deal, object], None]
    code: str | None = None  # the record it writes, when there is one
    optional: bool = False  # part of the demo walk, but no later screen waits for it
    anchor: str | None = None  # where on the screen (defaults to the record's card)

    @property
    def decision(self) -> bool:
        return bool(self.code) and catalogue.get(self.code).kind == "client_decision"

    @property
    def link(self) -> str:
        a = self.anchor or (f"rec-{self.code}" if self.decision else None)
        return f"{self.route}#{a}" if a else self.route


# ---- checks and plays --------------------------------------------------------------------------------------------

def _done(code: str) -> Callable[[Session, Deal], bool]:
    return lambda s, deal: records.is_done(s, deal.id, code)


def _exists(code: str) -> Callable[[Session, Deal], bool]:
    return lambda s, deal: records.latest(s, deal.id, code) is not None


def _intake(s, deal, provider):
    from app.modules.intake import service as intake

    intake.start_intake(s, intake.demo_input())


def _inferred(s, deal):
    return any(f.group == "Inferred by the AI" for f in deal.property.facts)


def _infer(s, deal, provider):
    from app.modules.intake import service as intake

    intake.infer_gaps(s, deal, provider)


def _agency(s, deal, provider):
    from app.modules.intake import service as intake

    intake.acknowledge_agency(s, deal, "seller", "acknowledge")


def _accept(s, deal, provider):
    from app.modules.intake import service as intake

    intake.accept_listing(s, deal)


def _sign_listing(s, deal, provider):
    from app.modules.intake import service as intake

    intake.sign_listing_agreement(s, deal, "seller", "sign")


def _priced(s, deal):
    from app.modules.pricing import service as pricing

    pa = pricing.current(s, deal)
    return bool(pa and pa.advice)


def _advise_price(s, deal, provider):
    from app.modules.pricing import service as pricing

    pricing.advise(s, deal, provider)


def _choose_price(s, deal, provider):
    from app.modules.pricing import service as pricing

    pricing.choose_price(s, deal, "seller", pricing.current(s, deal).advice["recommended_price"])


def _drafted(s, deal):
    from app.modules.listing_copy import service as copy

    return bool(copy.artifacts(s, deal))


def _draft_copy(s, deal, provider):
    from app.modules.listing_copy import service as copy

    copy.draft(s, deal, provider)


def _copy_ready(s, deal):
    from app.modules.listing_copy import service as copy

    arts = copy.artifacts(s, deal)
    return bool(arts) and all(a.status == "ready" for a in arts)


def _ready_copy(s, deal, provider):
    """As the demo does it: plant the violation in the portal description, let the AI fix it, mark all ready."""
    from app.modules.listing_copy import service as copy

    portal = next((a for a in copy.artifacts(s, deal) if a.channel == "portal"), None)
    if portal is not None and portal.version == 1:
        copy.plant(s, deal, portal, provider)
    if portal is not None and portal.edited_by == "planted (demo)":
        copy.apply_fix(s, deal, portal, provider)
    copy.mark_all_ready(s, deal)


def _authorise(s, deal, provider):
    from app.modules.channels import service as channels

    channels.open_authorisations(s, deal)
    channels.sign_authorisations(s, deal, "seller", "sign", "Publish to Internet",
                                 ["cooperating_brokers", "lockbox", "photographer"])


def _mls_entry(s, deal, provider):
    from app.modules.channels import service as channels

    channels.record_mls_entry(s, deal)


def _approve_authority(s, deal, provider):
    from app.modules.inbox import service as inbox

    inbox.open_fact_sheet(s, deal)
    inbox.approve(s, deal, "seller", "approve", self_guided=True)


def _all_arrived(s, deal):
    from app.modules.inbox import service as inbox

    return len(inbox.arrived(s, deal)) >= len(inbox.ENQUIRIES)


def _enquiries(s, deal, provider):
    from app.modules.inbox import service as inbox

    while (m := inbox.next_enquiry(s, deal)) is not None:
        inbox.handle(s, deal, m, provider)


def _buyer(s, deal, provider):
    from app.modules.buyer import service as buyer

    buyer.start(s, deal, buyer.demo_input())


def _sign_buyer(s, deal, provider):
    from app.modules.buyer import service as buyer

    buyer.sign_agreement(s, deal, "buyer", "sign")


def _alerted(s, deal):
    q = select(Message.id).where(Message.deal_id == deal.id, Message.side == "buyer", Message.topic == "alert")
    return s.execute(q.limit(1)).first() is not None


def _alert(s, deal, provider):
    from app.modules.buyer import service as buyer

    buyer.send_alert(s, deal, provider, buyer.default_criteria(s, deal))


def _tour(s, deal, provider):
    from app.modules.buyer import service as buyer

    buyer.request_tour(s, deal, provider, self_guided=True)


def _consent(s, deal, provider):
    from app.modules.buyer import service as buyer

    cp = records.latest(s, deal.id, "CP-17")
    for p in ("buyer", "seller"):
        if f"{p}=" not in (cp.decision or ""):
            buyer.consent_dual_agency(s, deal, p, "consent")


def _buyer_state(key):
    def check(s, deal):
        from app.modules.buyer import service as buyer

        return bool(buyer.state(deal).get(key))
    return check


def _offer_state(key):
    def check(s, deal):
        from app.modules.offers import service as offers

        return bool(offers.state(deal).get(key))
    return check


def _advise_offer(s, deal, provider):
    from app.modules.buyer import service as buyer

    buyer.advise_offer(s, deal, provider)


def _approve_offer(s, deal, provider):
    from app.modules.buyer import service as buyer

    buyer.approve_offer(s, deal, "buyer", "approve")


def _advise_offers(s, deal, provider):
    from app.modules.offers import service as offers

    offers.advise(s, deal, provider)


def _seller_decides(s, deal, provider):
    """The seller counters at the figures the AI suggested, as the demo does (the form's pre-filled values)."""
    from app.modules.offers import service as offers

    adv = offers.state(deal)["advice"]
    labels = [o["label"] for o in offers.offers(deal)]
    d = offers.DECISION_DEFAULTS
    offers.decide(s, deal, "seller", decision="counter",
                  offer_label=adv.get("suggested_offer") if adv.get("suggested_offer") in labels else "B",
                  counter_price=adv.get("suggested_counter_price"), lowest_price=adv.get("suggested_lowest_price"),
                  closing_days=adv.get("suggested_closing_days") or 45, closing_min=d["closing_min"],
                  closing_max=d["closing_max"], inspection_max=d["inspection_max"], mortgage_max=d["mortgage_max"])


def _negotiate(s, deal, provider):
    """The seller's AI sends the counter; the buyer's AI advises and the buyer approves each reply, until agreed."""
    from app.modules.buyer import service as buyer
    from app.modules.offers import service as offers

    offers.negotiate(s, deal)
    for _ in range(5):
        st = offers.state(deal)
        if st.get("accepted") or st.get("ended") or st.get("back_to_seller"):
            return
        if (st.get("decision") or {}).get("offer") != "B":
            offers.negotiate(s, deal)
            continue
        if not buyer.state(deal).get("counter_advice"):
            buyer.advise_counter(s, deal, provider)
        buyer.approve_reply(s, deal, "buyer", "approve")


def _contract_state(key):
    def check(s, deal):
        from app.modules.contract import service as contract

        return bool(contract.state(deal).get(key))
    return check


def _draft_contract(s, deal, provider):
    from app.modules.contract import service as contract

    contract.draft(s, deal, provider)


def _pcds(s, deal, provider):
    from app.disclosures import pcds

    pcds.submit(s, deal, "seller", pcds.prepared_answers(), prepared=True)


def _attach(s, deal, provider):
    from app.modules.contract import service as contract

    contract.attach_disclosures(s, deal)


def _open_signing(s, deal, provider):
    from app.modules.contract import service as contract

    contract.open_signing(s, deal)


def _sign_contract(s, deal, provider):
    from app.modules.contract import service as contract

    cp = records.latest(s, deal.id, "CP-33")
    for p in ("seller", "buyer"):
        if f"{p}=" not in (cp.decision or ""):
            contract.sign(s, deal, p, "sign")


# ---- the walk, in walk order ---------------------------------------------------------------------------------------

M = Milestone
WALK: list[Milestone] = [
    # Step 1 Intake
    M("intake", 1, "The seller's intake: the address and a few facts", "seller", "/intake",
      lambda s, deal: True, _intake, anchor="intake-form"),
    M("infer", 1, "The AI fills the gaps in the property profile", "ai", "/intake/profile", _inferred, _infer,
      optional=True),
    M("agency", 1, "The seller acknowledges the agency disclosure form", "seller", "/intake/onboarding",
      _done("CP-01"), _agency, code="CP-01"),
    M("accept", 1, "The AI accepts the listing", "ai", "/intake/onboarding", _exists("CP-02"), _accept,
      code="CP-02"),
    M("listing", 1, "The seller signs the listing agreement", "seller", "/intake/onboarding", _done("CP-03"),
      _sign_listing, code="CP-03"),
    # Step 2 Pricing
    M("advice", 2, "The AI recommends a list price", "ai", "/pricing/advice", _priced, _advise_price, code="CP-25"),
    M("price", 2, "The seller chooses the list price", "seller", "/pricing/advice", _done("CP-05"), _choose_price,
      code="CP-05"),
    # Step 3 Listing copy
    M("copy", 3, "The AI writes and checks the listing copy", "ai", "/copy", _drafted, _draft_copy, code="CP-26"),
    M("copy_ready", 3, "The AI marks the passing copy ready to publish", "ai", "/copy", _copy_ready, _ready_copy,
      code="CP-06", optional=True),
    # Step 4 Marketing plan
    M("authorise", 4, "The seller signs the marketing authorisations", "seller", "/channels", _done("CP-07"),
      _authorise, code="CP-07"),
    M("mls", 4, "The MLS entry is recorded (simulated)", "presenter", "/channels", _exists("CP-08"), _mls_entry,
      code="CP-08", optional=True),
    # Step 5 Communications
    M("authority", 5, "The seller approves the fact sheet and the AI's authority", "seller", "/inbox",
      _done("CP-27"), _approve_authority, code="CP-27"),
    M("enquiries", 5, "The simulated enquiries arrive and the AI answers them", "ai", "/inbox", _all_arrived,
      _enquiries, optional=True, anchor="inbox"),
    # Step 8 Buyer side (walked before step 6: offer B comes from the firm's own buyer)
    M("buyer", 8, "The buyer's intake: the AI takes the buyer on as a client", "buyer", "/buyer",
      lambda s, deal: bool(deal.buyer_id), _buyer, code="CP-30"),
    M("buyer_agreement", 8, "The buyer signs the buyer agreement", "buyer", "/buyer", _done("CP-16"), _sign_buyer,
      code="CP-16"),
    M("alert", 8, "The buyer's AI sends the search alert", "ai", "/buyer/search", _alerted, _alert, optional=True,
      anchor="alerts"),
    M("tour", 8, "The buyer's AI asks for a tour", "ai", "/buyer/tour", _exists("CP-17"), _tour, anchor="booked"),
    M("dual_agency", 8, "The buyer and the seller consent to dual agency", "seller_and_buyer", "/buyer/tour",
      _done("CP-17"), _consent, code="CP-17"),
    M("offer_advice", 8, "The buyer's AI advises and drafts the offer", "ai", "/buyer/offer", _buyer_state("advice"),
      _advise_offer, code="CP-31", anchor="advice"),
    M("offer", 8, "The buyer approves and sends the offer", "buyer", "/buyer/offer", _buyer_state("offer"),
      _approve_offer, code="CP-18"),
    # Step 6 Offers
    M("offers_advice", 6, "The seller's AI presents the offers and advises", "ai", "/offers",
      _offer_state("advice"), _advise_offers, code="CP-11", anchor="advice"),
    M("seller_decision", 6, "The seller decides on the offers", "seller", "/offers", _offer_state("decision"),
      _seller_decides, code="CP-12"),
    M("agreed", 6, "The AIs negotiate to an agreed offer", "ai", "/offers", _offer_state("accepted"), _negotiate,
      code="CP-13", anchor="negotiation"),
    # Step 7 Contract
    M("contract", 7, "The AI drafts the contract and rider", "ai", "/contract", _contract_state("draft"),
      _draft_contract, code="CP-14", anchor="draft"),
    M("pcds", 7, "The seller completes the Property Condition Disclosure Statement", "seller", "/disclosures/pcds",
      _done("CP-04"), _pcds, code="CP-04", anchor="pcds-prepared"),
    M("attach", 7, "The AI attaches the disclosures to the contract", "ai", "/contract",
      _contract_state("attached"), _attach, code="CP-32", anchor="disclosures"),
    M("signing", 7, "The contract is opened for signing", "ai", "/contract", _exists("CP-33"), _open_signing,
      anchor="rec-CP-33"),
    M("signed", 7, "The seller and the buyer sign the contract", "seller_and_buyer", "/contract", _done("CP-33"),
      _sign_contract, code="CP-33"),
]
BY_KEY = {m.key: m for m in WALK}

# What each screen needs before it can do its work: the furthest milestone it waits for. The card names the first
# missing milestone on the way there. These mirror the service gates (and the old "no deal yet" redirects).
NEEDS = {
    "/intake/profile": "intake", "/intake/disclosures": "intake", "/intake/onboarding": "intake",
    "/pricing": "listing", "/pricing/advice": "listing",
    "/copy": "price", "/copy/mls": "price",
    "/channels": "listing",
    "/inbox": "price",
    "/buyer": "intake", "/buyer/search": "buyer", "/buyer/tour": "buyer", "/buyer/offer": "buyer",
    "/offers": "authority",
    "/contract": "agreed",
    "/disclosures/pcds": "intake",
    "/timeline": "intake",
}


def walk_order() -> list[int]:
    """Step numbers in the order the demo walks them (the order of app/demo/steps.yaml)."""
    return [st["n"] for st in steps()]


def is_done(s: Session, deal: Deal | None, m: Milestone) -> bool:
    return deal is not None and m.done(s, deal)


def plan(n: int, path: str | None = None) -> list[Milestone]:
    """What fast-forwarding to step n plays: every milestone of the steps walked before it, and, when the screen at
    `path` waits for something inside step n itself (the buyer's search waits for the buyer), that too. WALK is in
    walk order, so this is always a prefix of it."""
    order = walk_order()
    earlier = set(order[:order.index(n)]) if n in order else set()
    upto = max((i for i, m in enumerate(WALK) if m.step in earlier), default=-1)
    need = NEEDS.get(path or "")
    if need:
        upto = max(upto, WALK.index(BY_KEY[need]))
    return WALK[:upto + 1]


def done_map(s: Session, deal: Deal | None) -> dict[str, bool]:
    return {m.key: is_done(s, deal, m) for m in WALK}


def fast_forward_steps(s: Session, deal: Deal | None) -> set[int]:
    """Built steps with something still to play before them: the step list offers fast-forward for these."""
    done = done_map(s, deal)
    return {st["n"] for st in steps() if st["built"]
            and any(not done[m.key] for m in plan(st["n"], st["screens"][0]["route"]))}


@dataclass
class Gate:
    """What a screen is waiting for, shown as the gate card."""
    missing: Milestone
    step: dict  # the missing milestone's step (n, title)
    target: dict  # the step of the screen being visited
    who_label: str
    decide_as: list[str] = field(default_factory=list)  # personas the Presenter can switch to, to decide
    message: str | None = None  # the service gate's own words, when the screen has them

    @property
    def can_fast_forward(self) -> bool:
        return bool(self.target.get("built"))


def _step(n: int) -> dict:
    return next((st for st in steps() if st["n"] == n), {"n": n, "title": f"Step {n}"})


def gate_for(s: Session, deal: Deal | None, path: str, message: str | None = None) -> Gate | None:
    """The first missing milestone on the way to what the screen at `path` needs, or None if it has it."""
    need = NEEDS.get(path)
    if need is None:
        return None
    target = BY_KEY[need]
    if is_done(s, deal, target):
        return None
    chain = WALK[:WALK.index(target) + 1]
    first = next(m for m in chain if not m.optional and not is_done(s, deal, m))
    from app.web import screen_for

    st, _ = screen_for(path)
    return Gate(missing=first, step=_step(first.step), target=st or {}, who_label=WHO_LABEL[first.who],
                decide_as=_deciders(s, deal, first), message=message)


def _deciders(s: Session, deal: Deal | None, m: Milestone) -> list[str]:
    if not m.decision:
        return []
    if m.who != "seller_and_buyer":
        return [m.who]
    cp = records.latest(s, deal.id, m.code) if deal else None
    return [p for p in ("seller", "buyer") if f"{p}=" not in ((cp.decision if cp else None) or "")]


def fast_forward(s: Session, provider, n: int, path: str | None = None) -> list[Milestone]:
    """Play what `plan(n, path)` lists and is not done yet, with the demo's scripted choices. Commits after each
    milestone, so a refusal part-way keeps what was played."""
    played = []
    for m in plan(n, path):
        deal = current_deal(s)
        if is_done(s, deal, m):
            continue
        m.play(s, deal, provider)
        s.commit()
        played.append(m)
    return played
