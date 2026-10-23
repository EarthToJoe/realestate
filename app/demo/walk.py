"""The sale's milestones, in path order (decision 51), and the demo's scripted plays.

Each milestone has a check ("is it done in the current deal?"), the screen it belongs to, who does it (the AI, the
seller, the buyer, both, a person at the firm, or a form the client fills in) and a play ("do it the way the demo
does"). The plays make exactly the choices `scripts/live-flow.sh` makes, through the same service calls the screens
use, so model calls hit the recorded replays ($0). Client decisions are recorded as the client's; the record
service still checks that, so nothing here can decide for the wrong person, and the AI's own plays never decide.

- `gate_for(s, deal, path)`: the first thing a screen is waiting for (what, on which step, who), or None.
- `fast_forward(s, provider, route)`: plays every milestone before that screen (skip ahead, presenter only).
- `play_screen(s, provider, route)`: "Do this screen for me" (presenter only).

app/demo/path.py builds the one-button path on top of this: the primary action, the AI pump and "Change".
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Deal, Message
from app.records import catalogue
from app.records import service as records
from app.web import current_deal, screen_for, stops

WHO_LABEL = {"ai": "The AI", "seller": "The seller", "buyer": "The buyer", "seller_and_buyer": "The seller and the buyer",
             "person": "A person at the firm (simulated)", "form": "The client"}


@dataclass(frozen=True)
class Milestone:
    key: str
    what: str  # plain words: what it is
    who: str  # ai | seller | buyer | seller_and_buyer | person | form (a client fills in a form)
    route: str  # the screen where it is done
    done: Callable[[Session, Deal], bool]
    play: Callable[[Session, Deal, object], None]
    code: str | None = None  # the record it writes, when there is one
    anchor: str | None = None  # where on the screen (defaults to the record's card)
    form_who: str | None = None  # for a form: whose form it is (seller | buyer)

    @property
    def decision(self) -> bool:
        return self.who in ("seller", "buyer", "seller_and_buyer", "form")

    @property
    def link(self) -> str:
        a = self.anchor or (f"rec-{self.code}" if self.code and catalogue.get(self.code).kind == "client_decision"
                            else None)
        return f"{self.route}#{a}" if a else self.route

    @property
    def step(self) -> int | None:
        st, _ = screen_for(self.route)
        return st["n"] if st else None


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
    return bool(pa and pa.advice) and records.latest(s, deal.id, "CP-25") is not None


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
    """The AI marks every passing piece ready (blocked pieces it fixes first, on the recorded answers)."""
    from app.modules.listing_copy import service as copy

    for a in copy.artifacts(s, deal):
        if a.status == "blocked":
            copy.apply_fix(s, deal, a, provider)
    copy.mark_all_ready(s, deal)


def _ready_copy_demo(s, deal, provider):
    """As the presenter's script does it: plant the violation in the portal description, let the AI fix it, mark
    all ready."""
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


def _answered(s, deal):
    from app.modules.inbox import service as inbox

    return _all_arrived(s, deal) and not inbox.seller_cards(s, deal)


def _answer(s, deal, provider):
    """The demo seller's answers to the questions put to the seller: the first choice on each card."""
    from app.modules.inbox import service as inbox

    for m in inbox.seller_cards(s, deal):
        inbox.seller_answer(s, deal, provider, "seller", m.id, next(iter(inbox.SELLER_CHOICES[m.topic])))


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


def _toured(s, deal):
    from app.modules.buyer import service as buyer

    return bool(buyer.state(deal).get("tour"))


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


def _decided(s, deal):
    from app.modules.offers import service as offers

    return bool(offers.state(deal).get("decision")) and records.is_done(s, deal.id, "CP-12")


def _advise_offer(s, deal, provider):
    from app.modules.buyer import service as buyer

    buyer.advise_offer(s, deal, provider)


def _approve_offer(s, deal, provider):
    from app.modules.buyer import service as buyer

    buyer.approve_offer(s, deal, "buyer", "approve")


def _advise_offers(s, deal, provider):
    from app.modules.offers import service as offers

    offers.advise(s, deal, provider)


def recorded_decision(deal) -> dict:
    """The seller's decision on the offers as the demo makes it: a counter at the figures the AI suggested (the
    form's pre-filled values). In a recorded demo these are the only figures the recordings cover."""
    from app.modules.offers import service as offers

    adv = offers.state(deal).get("advice") or {}
    labels = [o["label"] for o in offers.offers(deal)]
    d = offers.DECISION_DEFAULTS
    return {"decision": "counter",
            "offer_label": adv.get("suggested_offer") if adv.get("suggested_offer") in labels else "B",
            "counter_price": adv.get("suggested_counter_price"), "lowest_price": adv.get("suggested_lowest_price"),
            "closing_days": adv.get("suggested_closing_days") or 45, "closing_min": d["closing_min"],
            "closing_max": d["closing_max"], "inspection_max": d["inspection_max"], "mortgage_max": d["mortgage_max"],
            "allow_requests": False}


def _seller_decides(s, deal, provider):
    from app.modules.offers import service as offers

    offers.decide(s, deal, "seller", **recorded_decision(deal))


def negotiation_next(s, deal) -> str | None:
    """What the negotiation waits for: "seller_ai" (send or answer), "buyer_ai" (advise the buyer on the counter),
    "buyer" (the buyer approves the reply), "seller" (back to the seller), or None (agreed, ended, not started)."""
    from app.modules.buyer import service as buyer
    from app.modules.offers import service as offers

    st = offers.state(deal)
    d = st.get("decision") or {}
    if st.get("accepted") or st.get("ended") or d.get("decision") != "counter":
        return None
    if st.get("back_to_seller") and not records.is_done(s, deal.id, "CP-12"):
        return "seller"
    thread = st.get("thread") or []
    if not thread or thread[-1]["from"] != "seller's AI":
        return "seller_ai"
    if d.get("offer") != "B":
        return "seller_ai"
    return "buyer" if buyer.state(deal).get("counter_advice") else "buyer_ai"


def _negotiate_ai(s, deal, provider):
    """The AIs' part of the negotiation, up to the next human decision."""
    from app.modules.buyer import service as buyer
    from app.modules.offers import service as offers

    for _ in range(8):
        nxt = negotiation_next(s, deal)
        if nxt == "seller_ai":
            offers.negotiate(s, deal)
        elif nxt == "buyer_ai":
            buyer.advise_counter(s, deal, provider)
        else:
            return


def _negotiate(s, deal, provider):
    """The demo's whole negotiation: the AIs' steps, and the buyer approving each drafted reply, until agreed."""
    from app.modules.buyer import service as buyer

    for _ in range(6):
        _negotiate_ai(s, deal, provider)
        if negotiation_next(s, deal) != "buyer":
            return
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


def _attached(s, deal):
    from app.modules.contract import service as contract

    return bool((contract.state(deal).get("attached") or {}).get("complete"))


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


def _brand_state(key):
    def check(s, deal):
        from app.modules.brand import service as brand

        return bool(brand.state(deal).get(key))
    return check


def _campaign_drafted(s, deal):
    from app.modules.brand import service as brand

    return bool(brand.artifacts(s, deal))


def _campaign(s, deal, provider):
    from app.modules.brand import service as brand

    brand.draft(s, deal, provider)


def _campaign_demo(s, deal, provider):
    """As the presenter's script does it: the AI writes the campaign; the presenter tries the bold headline; the AI
    removes it."""
    from app.modules.brand import service as brand

    brand.draft(s, deal, provider)
    landing = next((a for a in brand.artifacts(s, deal) if a.channel == "brand_landing"), None)
    if landing is not None and landing.version == 1 and landing.status == "passed":
        brand.plant(s, deal, landing, provider)
        brand.apply_fix(s, deal, landing, provider)


def _targeting(s, deal, provider):
    from app.modules.brand import service as brand

    brand.set_targeting(s, deal)


def _publish(s, deal, provider):
    from app.modules.brand import service as brand

    brand.publish(s, deal)


# ---- the walk, in path order ---------------------------------------------------------------------------------------

M = Milestone
WALK: list[Milestone] = [
    # 1 The seller signs up
    M("intake", "The seller's details: the address and a few facts", "form", "/intake",
      lambda s, deal: True, _intake, anchor="intake-form", form_who="seller"),
    # 2 The AI researches the house
    M("infer", "The AI fills the gaps in the public record", "ai", "/intake/profile", _inferred, _infer),
    # 3 The seller hires the firm
    M("agency", "The seller acknowledges the agency disclosure form", "seller", "/intake/onboarding",
      _done("CP-01"), _agency, code="CP-01"),
    M("accept", "The AI accepts the listing", "ai", "/intake/onboarding", _exists("CP-02"), _accept, code="CP-02"),
    M("listing", "The seller signs the listing agreement", "seller", "/intake/onboarding", _done("CP-03"),
      _sign_listing, code="CP-03"),
    # 4 The price
    M("advice", "The AI recommends a list price", "ai", "/pricing", _priced, _advise_price, code="CP-25",
      anchor="advice"),
    M("price", "The seller chooses the list price", "seller", "/pricing", _done("CP-05"), _choose_price,
      code="CP-05"),
    # 5 The listing
    M("copy", "The AI writes the listing and checks it for fair housing", "ai", "/copy", _drafted, _draft_copy,
      code="CP-26"),
    M("copy_ready", "The AI marks the passing copy ready to publish", "ai", "/copy", _copy_ready, _ready_copy,
      code="CP-06"),
    # 6 On the market
    M("authorise", "The seller signs the marketing plan", "seller", "/channels", _done("CP-07"), _authorise,
      code="CP-07"),
    M("mls", "A person at the firm keys the listing into the MLS (simulated)", "person", "/channels",
      _exists("CP-08"), _mls_entry, code="CP-08", anchor="rec-CP-08"),
    # 7 Enquiries and showings
    M("authority", "The seller approves the fact sheet and what the AI may say", "seller", "/inbox",
      _done("CP-27"), _approve_authority, code="CP-27"),
    M("enquiries", "The enquiries arrive and the AI answers them", "ai", "/inbox", _all_arrived, _enquiries,
      anchor="inbox"),
    M("seller_answers", "The seller answers the questions only the seller can answer", "seller", "/inbox",
      _answered, _answer, anchor="cards"),
    # 8 The buyer signs up
    M("buyer", "The buyer's details: the home they want and the money", "form", "/buyer",
      lambda s, deal: bool(deal.buyer_id), _buyer, code="CP-30", anchor="buyer-form", form_who="buyer"),
    M("buyer_agreement", "The buyer signs the buyer agreement", "buyer", "/buyer", _done("CP-16"), _sign_buyer,
      code="CP-16"),
    M("alert", "The buyer's AI searches and sends an alert", "ai", "/buyer", _alerted, _alert, anchor="search"),
    M("tour", "The AI books a tour of the house", "ai", "/buyer", _toured, _tour, anchor="tour"),
    M("dual_agency", "The buyer and the seller consent to dual agency", "seller_and_buyer", "/buyer",
      _done("CP-17"), _consent, code="CP-17"),
    # 9 The buyer's offer
    M("offer_advice", "The buyer's AI advises and drafts the offer", "ai", "/buyer/offer", _buyer_state("advice"),
      _advise_offer, code="CP-31", anchor="advice"),
    M("offer", "The buyer sends the offer", "buyer", "/buyer/offer", _buyer_state("offer"), _approve_offer,
      code="CP-18"),
    # 10 The seller decides
    M("offers_advice", "The seller's AI presents the offers and advises", "ai", "/offers", _offer_state("advice"),
      _advise_offers, code="CP-11", anchor="advice"),
    M("seller_decision", "The seller decides on the offers", "seller", "/offers", _decided, _seller_decides,
      code="CP-12"),
    M("agreed", "The AIs negotiate and the buyer approves each reply, to an agreed price", "negotiation", "/offers",
      _offer_state("accepted"), _negotiate, code="CP-13", anchor="negotiation"),
    # 11 The contract
    M("contract", "The AI drafts the contract and rider", "ai", "/contract", _contract_state("draft"),
      _draft_contract, code="CP-14", anchor="draft"),
    M("pcds", "The seller completes the property condition disclosure form", "seller", "/contract",
      _done("CP-04"), _pcds, code="CP-04", anchor="pcds"),
    M("attach", "The AI attaches the disclosures to the contract", "ai", "/contract", _attached, _attach,
      code="CP-32", anchor="disclosures"),
    M("signing", "The AI opens the contract for signing", "ai", "/contract", _exists("CP-33"), _open_signing,
      anchor="signing"),
    M("signed", "The seller and the buyer sign the contract", "seller_and_buyer", "/contract", _done("CP-33"),
      _sign_contract, code="CP-33"),
    # One more thing: how the firm finds sellers (after the finale; nothing in it needs the deal's progress)
    M("campaign", "The AI writes and checks the firm's campaign", "ai", "/brand", _campaign_drafted, _campaign,
      code="CP-26", anchor="campaign-outcome"),
    M("targeting", "The AI chooses who sees the ad", "ai", "/brand", _brand_state("targeting"), _targeting,
      anchor="targeting"),
    M("publish", "The AI publishes the firm's campaign (simulated)", "ai", "/brand", _brand_state("published"),
      _publish, code="CP-19", anchor="published"),
]
BY_KEY = {m.key: m for m in WALK}
# The presenter's script plays two milestones with a demo device first (the planted violation, the bold headline).
DEMO_PLAYS = {"copy_ready": _ready_copy_demo, "campaign": _campaign_demo}

# What each screen needs before it can do its work: the furthest milestone it waits for. The card names the first
# missing milestone on the way there. These mirror the service gates.
NEEDS = {
    "/intake/profile": "intake", "/intake/onboarding": "intake",
    "/pricing": "listing", "/copy": "price", "/channels": "copy_ready", "/inbox": "price",
    "/buyer": "authority", "/buyer/offer": "dual_agency", "/offers": "offer", "/contract": "agreed",
    "/timeline": "intake", "/brand": "intake", "/people": "intake",
}

# What each milestone directly depends on, for "Change" (decision 48): changing one undoes only these, transitively.
# "house" is the seller's address and facts (step 1); "buyer_needs" the buyer's answers (step 8).
DEPS = {
    "infer": {"house"}, "agency": set(), "accept": {"house"}, "listing": {"agency", "accept"},
    "advice": {"listing", "house"}, "price": {"advice"}, "copy": {"price"}, "copy_ready": {"copy"},
    "authorise": {"listing", "price"}, "mls": {"authorise", "copy_ready"}, "authority": {"price"},
    "enquiries": {"authority"}, "seller_answers": {"enquiries"},
    "buyer_agreement": set(), "alert": {"buyer_agreement", "price", "buyer_needs"},
    "tour": {"buyer_agreement", "authority"}, "dual_agency": {"tour"},
    "offer_advice": {"dual_agency", "price", "buyer_needs"}, "offer": {"offer_advice"},
    "offers_advice": {"offer", "authority"}, "seller_decision": {"offers_advice"}, "agreed": {"seller_decision"},
    "contract": {"agreed"}, "pcds": {"house"}, "attach": {"contract", "pcds"}, "signing": {"attach"},
    "signed": {"signing"},
}


def dependents(keys: set[str]) -> list[Milestone]:
    """Every milestone that depends on any of `keys`, directly or not, in path order."""
    out: set[str] = set()
    frontier = set(keys)
    while frontier:
        nxt = {k for k, deps in DEPS.items() if deps & frontier and k not in out}
        out |= nxt
        frontier = nxt
    return [m for m in WALK if m.key in out]


def is_done(s: Session, deal: Deal | None, m: Milestone) -> bool:
    return deal is not None and m.done(s, deal)


def done_map(s: Session, deal: Deal | None) -> dict[str, bool]:
    return {m.key: is_done(s, deal, m) for m in WALK}


def on_screen(route: str) -> list[Milestone]:
    return [m for m in WALK if m.route == route]


@dataclass
class Gate:
    """What a screen is waiting for, shown as the "not yet" card."""
    missing: Milestone
    step: dict  # the missing milestone's step
    target: dict  # the step of the screen being visited
    who_label: str
    message: str | None = None  # the service gate's own words, when the screen has them
    decide_as: list[str] = field(default_factory=list)


def _stop_of(m: Milestone) -> dict:
    st, _ = screen_for(m.route)
    return st or {"n": None, "title": m.route}


def gate_for(s: Session, deal: Deal | None, path: str, message: str | None = None) -> Gate | None:
    """The first missing milestone on the way to what the screen at `path` needs, or None if it has it."""
    from app.web import merged_routes

    path = merged_routes().get(path, (path, None))[0]
    need = NEEDS.get(path)
    if need is None:
        return None
    target = BY_KEY[need]
    if is_done(s, deal, target):
        return None
    chain = WALK[:WALK.index(target) + 1]
    first = next(m for m in chain if not is_done(s, deal, m))
    st, _ = screen_for(path)
    return Gate(missing=first, step=_stop_of(first), target=st or {}, who_label=WHO_LABEL.get(first.who, "The AI"),
                message=message)


def screen_plan(route: str) -> list[Milestone]:
    """What "Do this screen for me" plays: the walk up to and including the last milestone on this screen."""
    last = max((i for i, m in enumerate(WALK) if m.route == route), default=-1)
    return WALK[:last + 1]


def before_plan(route: str) -> list[Milestone]:
    """What skipping ahead to a screen plays: every milestone before the screen's first one, and what it needs."""
    first = min((i for i, m in enumerate(WALK) if m.route == route), default=len(WALK))
    upto = first - 1
    need = NEEDS.get(route)
    if need:
        upto = max(upto, WALK.index(BY_KEY[need]))
    if route == "/brand":  # nothing before the firm's campaign is needed except a deal
        upto = 0
    return WALK[:upto + 1]


def playable(s: Session, deal: Deal | None, route: str) -> list[Milestone]:
    """The milestones "Do this screen for me" would still play here."""
    return [m for m in screen_plan(route) if not is_done(s, deal, m)]


def _play(s: Session, provider, plan: list[Milestone]) -> list[Milestone]:
    """Plays each milestone not done yet, the way the presenter's script does; every client decision is recorded as
    the client's and marked "played by the demo". Commits after each, so a refusal part-way keeps what was played."""
    played = []
    token = records.PLAYED.set(True)
    try:
        for m in plan:
            deal = current_deal(s)
            if is_done(s, deal, m):
                continue
            DEMO_PLAYS.get(m.key, m.play)(s, deal, provider)
            s.commit()
            played.append(m)
    finally:
        records.PLAYED.reset(token)
    return played


def play_screen(s: Session, provider, route: str) -> list[Milestone]:
    return _play(s, provider, screen_plan(route))


def fast_forward(s: Session, provider, route: str) -> list[Milestone]:
    """Skip ahead: play what comes before the screen at `route`."""
    return _play(s, provider, before_plan(route))


def stop_routes() -> list[str]:
    return [st["route"] for st in stops()]
