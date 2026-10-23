"""Step 5 Communications (spec section 3, step 5): the AI answers enquiries and books showings on its own.

1. CP-27 (blocking): the seller approves the fact sheet and the AI's authority. No reply leaves before it.
2. Simulated enquiries arrive (`ENQUIRIES`, fictional prospects labelled by role). `handle` routes each in code:
   - facts: one model call (`inbox.reply`) answers from the approved fact sheet only, disclosing known material
     facts (F83);
   - legal: "I can't give legal advice; you may ask your own lawyer" (L23), fixed text;
   - neighbourhood or schools: neutral official links only (L37), fixed text;
   - seller_only ("would the seller take X?", a showing outside the seller's windows): a decision card for the
     seller, and a holding reply. Nothing else reaches the seller;
   - showing: checked against the seller's windows and the buyer's representation (L15), booked within 24 hours
     (CP-29), owner-hosted (CP-10, human required) or self-guided (CP-28 marker);
   - feedback: summarised and logged (F42).
3. Every outgoing message passes the fair-housing pipeline on its exact text and carries the firm's identity
   block (L10); the first substantive contact on a thread carries the agency form and fair-housing notice (CP-24).
   Each sent message that discusses the listing, negotiates or advises gets its own CP-09 marker.

The model sees the approved fact sheet, the authority and the question; never the seller's confidential
instructions (price floor, motivation) or any PII.
"""

from __future__ import annotations

from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit import record_event
from app.brokerage import identity_block
from app.fairhousing import check as fh
from app.model.provider import ModelProvider
from app.models import ClientInstructions, Deal, Message
from app.modules.inbox.schemas import InboxReply
from app.records import service as records
from app.records.service import GateError, NotYourDecision
from app.sanitize import clean_model

PROMPTS = Path(__file__).with_name("prompts")
PROMPT_VERSION = "reply.v1"

FACT_FIELDS = {
    "ArchitecturalStyle": "Style", "YearBuilt": "Year built", "LivingArea": "Living area (sq ft)",
    "BelowGradeFinishedArea": "Finished lower level (sq ft)", "BedroomsTotal": "Bedrooms",
    "BathroomsFull": "Full baths", "LotSizeAcres": "Lot (acres)", "HeatingFuel": "Heating fuel",
    "Cooling": "Cooling", "WaterSource": "Water", "Sewer": "Sewer", "ParkingFeatures": "Parking",
    "RoofYear": "Roof", "ConditionUpdates": "Updates", "WaterfrontFeatures": "Water features",
    "TaxAnnualAmount": "Annual taxes", "FloodZone": "Flood zone", "SchoolDistrict": "School district",
}

DEFAULT_AUTHORITY = {
    "answer_from_fact_sheet": "Answer any question the approved fact sheet answers, and disclose known material facts",
    "showing_windows": {"Sat": [10, 16], "Sun": [12, 17], "Wed": [17, 19]},
    "showing_kinds": "Owner-hosted showings; self-guided tours if the seller allows them below",
    "price": "Say the list price only. Any question about a lower price, terms or offers goes to the seller",
    "send_without_review": "Send replies without the seller seeing them first (the seller sees only decisions)",
}

# Simulated enquiries for the demonstration: fictional prospects, labelled by role, never real people.
ENQUIRIES = [
    {"thread": "A", "party": "Prospect A (simulated, unrepresented)", "topic": "facts",
     "body": "Hi, is the pond part of the property? And how old is the roof? Is there anything wrong with the "
             "house we should know about?"},
    {"thread": "B", "party": "Buyer's agent for Prospect B (simulated other firm)", "topic": "showing",
     "body": "My buyers are under a signed buyer agreement with me. Can they see the house Saturday at 11am?",
     "slot": {"day": "Sat", "hour": 11}, "self_guided": False, "represented": True},
    {"thread": "C", "party": "Prospect C (simulated, unrepresented)", "topic": "seller_only",
     "body": "Would the seller take $600,000 cash with a quick closing?"},
    {"thread": "D", "party": "Prospect D (simulated, unrepresented)", "topic": "neighbourhood",
     "body": "Are the schools any good? And is it a safe area, what kind of people live around there?"},
    {"thread": "E", "party": "Prospect E (simulated, unrepresented)", "topic": "legal",
     "body": "Do I need a lawyer for the contract, or can I just sign what you send me?"},
    {"thread": "F", "party": "Prospect F (simulated; buyer agreement with their own agent)", "topic": "showing",
     "body": "Could I do a self-guided tour on Sunday at 2pm? I'm under the firm's buyer agreement.",
     "slot": {"day": "Sun", "hour": 14}, "self_guided": True, "represented": True},
    {"thread": "G", "party": "Buyer's agent for Prospect G (simulated other firm)", "topic": "showing",
     "body": "Any chance of a showing Tuesday at 8pm? My buyers work late.",
     "slot": {"day": "Tue", "hour": 20}, "self_guided": False, "represented": True},
    {"thread": "B", "party": "Buyer's agent for Prospect B (simulated other firm)", "topic": "feedback",
     "body": "Thanks for Saturday. My buyers liked the lot and the kitchen; they worry about the lack of central "
             "air and road noise from Route 292. They may make an offer."},
]

LEGAL_REPLY = ("I can't give legal advice, and nothing I send is legal advice. You may ask your own lawyer to "
               "review any contract before you sign it; in the Hudson Valley each side usually has one.")
NEIGHBOURHOOD_REPLY = (
    "I can't describe schools, safety or who lives in an area; those judgements are yours to make. Official "
    "sources: the New York State Education Department's school report cards (data.nysed.gov) for the Pawling "
    "Central School District, and the Dutchess County Sheriff's Office for public safety information. The house is "
    "at 146 Route 292, Holmes; you are welcome to visit the area.")
AGENCY_NOTE = ("Attached: the New York agency disclosure form (I act for the seller) and the New York State Housing "
               "and Anti-Discrimination Notice.")


class SendHeld(Exception):
    pass


# ---- CP-27: the fact sheet and the AI's authority ------------------------------------------------------------

def _instructions(s: Session, deal: Deal) -> ClientInstructions | None:
    q = select(ClientInstructions).where(ClientInstructions.deal_id == deal.id, ClientInstructions.side == "seller")
    return s.execute(q.limit(1)).scalar_one_or_none()


def fact_sheet_from_record(deal: Deal) -> dict:
    facts = {f.field: f.value for f in deal.property.facts}
    sheet = {label: facts[field] for field, label in FACT_FIELDS.items() if facts.get(field) not in (None, "")}
    sheet["List price"] = f"${deal.list_price:,}" if deal.list_price else "not set"
    sheet["Address"] = f"{deal.property.street}, {deal.property.city}, NY"
    return sheet


def open_fact_sheet(s: Session, deal: Deal) -> ClientInstructions:
    records.require(s, deal.id, "CP-03", action="answer enquiries (no marketing before the listing agreement, L9)")
    records.require(s, deal.id, "CP-05", action="answer enquiries (the seller has not chosen a list price)")
    ins = _instructions(s, deal)
    if ins is None:
        ins = ClientInstructions(deal_id=deal.id, side="seller")
        s.add(ins)
    if not ins.approved:
        ins.fact_sheet = fact_sheet_from_record(deal)
        ins.authority = {**DEFAULT_AUTHORITY, **{k: v for k, v in (ins.authority or {}).items()
                                                 if k not in DEFAULT_AUTHORITY}}
        s.flush()
        if not records.is_done(s, deal.id, "CP-27"):
            records.open_decision(s, deal.id, "CP-27", attached_to=f"client_instructions:{ins.id}")
    return ins


def approve(s: Session, deal: Deal, persona: str, decision: str, self_guided: bool) -> None:
    ins = open_fact_sheet(s, deal)
    cp = records.latest(s, deal.id, "CP-27")
    reason = ("The seller approved the fact sheet and the AI's authority; self-guided tours "
              + ("allowed" if self_guided else "not allowed")) if decision == "approve" else \
        "The seller declined the fact sheet and authority; no reply may be sent"
    records.decide(s, cp, persona=persona, decision=decision, reason=reason)
    if decision == "approve":
        ins.approved = True
        ins.authority = {**(ins.authority or {}), "self_guided_tours": bool(self_guided)}
    s.flush()


def authority(s: Session, deal: Deal) -> dict:
    ins = _instructions(s, deal)
    return (ins.authority or {}) if ins else {}


# ---- the inbox -------------------------------------------------------------------------------------------------

def messages(s: Session, deal: Deal, side: str = "seller") -> list[Message]:
    q = select(Message).where(Message.deal_id == deal.id, Message.side == side).order_by(Message.id)
    return list(s.execute(q).scalars())


def arrived(s: Session, deal: Deal) -> list[Message]:
    return [m for m in messages(s, deal) if m.direction == "in"]


def next_enquiry(s: Session, deal: Deal) -> Message | None:
    """A simulated enquiry arrives (the next one in `ENQUIRIES`)."""
    n = len(arrived(s, deal))
    if n >= len(ENQUIRIES):
        return None
    e = ENQUIRIES[n]
    m = Message(deal_id=deal.id, thread=e["thread"], direction="in", party=e["party"], topic=e["topic"],
                body=e["body"], status="received", extra={"index": n})
    s.add(m)
    s.flush()
    record_event(s, actor="system", kind="system", entity="message", entity_id=m.id,
                 summary=f"Enquiry arrived on thread {e['thread']} ({e['topic']}, simulated)")
    return m


def _enquiry(m: Message) -> dict:
    return ENQUIRIES[(m.extra or {})["index"]]


def in_window(auth: dict, slot: dict) -> bool:
    w = (auth.get("showing_windows") or {}).get(slot["day"])
    return bool(w and w[0] <= slot["hour"] < w[1])


def _first_contact(s: Session, deal: Deal, thread: str, side: str = "seller") -> bool:
    return not any(m.direction == "out" and m.thread == thread and m.status == "sent"
                   for m in messages(s, deal, side))


def send(s: Session, deal: Deal, provider: ModelProvider, *, thread: str, party: str, body: str, topic: str,
         discusses_listing: bool, extra: dict | None = None, side: str = "seller",
         agency_note: str | None = None) -> Message:
    """Every outgoing message, either side: fair-housing check on the exact text, identity block, CP-24 at first
    contact, CP-09 when it discusses a listing. A failed check holds the message; it is never sent."""
    first = _first_contact(s, deal, thread, side)
    text = body + (f"\n\n{agency_note or AGENCY_NOTE}" if first else "")
    m = Message(deal_id=deal.id, side=side, thread=thread, direction="out", party=party, topic=topic, body=text,
                status="checking", extra={**(extra or {}), "identity_block": identity_block(deal.brokerage_id),
                                          "first_contact": first})
    s.add(m)
    s.flush()
    res = fh.run(s, text=text, provider=provider, entity="message", entity_id=m.id, version=1, deal_id=deal.id,
                 channel="message")
    m.extra = {**m.extra, "fair_housing": "passed" if res.passed else "not passed", "fh_result_id": res.id}
    if not res.passed:
        m.status = "held"
        record_event(s, actor="ai", kind="ai_action", entity="message", entity_id=m.id,
                     summary=f"Reply on thread {thread} held: fair-housing check not passed")
        s.flush()
        return m
    m.status = "sent"
    if first:
        records.record_auto(s, deal.id, "CP-24", reason=f"First contact on thread {thread} ({party}): agency "
                                                        "disclosure form and fair-housing notice sent (simulated)",
                            attached_to=f"message:{m.id}", step=8 if side == "buyer" else None)
    if discusses_listing:
        records.mark_law(s, deal.id, "CP-09", reason=f"The {side}'s AI sent a message on thread {thread} to "
                                                      f"{party} ({topic}) without the {side} reviewing it",
                         attached_to=f"message:{m.id}", step=8 if side == "buyer" else None)
    record_event(s, actor="ai", kind="ai_action", entity="message", entity_id=m.id,
                 summary=f"The {side}'s AI sent a message on thread {thread} ({topic}, sent (simulated))")
    s.flush()
    return m


def model_context(s: Session, deal: Deal, question: str) -> dict:
    ins = _instructions(s, deal)
    auth = {k: v for k, v in (ins.authority or {}).items()}
    return {"question": question, "fact_sheet": ins.fact_sheet or {}, "authority": auth,
            "firm": "the listing brokerage (the AI acts for the seller)"}


def handle(s: Session, deal: Deal, m: Message, provider: ModelProvider) -> list[Message]:
    """The AI deals with one incoming message on its own, within the seller's approved authority."""
    records.require(s, deal.id, "CP-27", action="send any reply (the seller has not approved the fact sheet and "
                                                "the AI's authority)")
    if m.status != "received":
        return []
    e = _enquiry(m)
    auth = authority(s, deal)
    out: list[Message] = []
    kw = dict(thread=m.thread, party=m.party)
    if m.topic == "facts":
        system = (PROMPTS / f"{PROMPT_VERSION}.md").read_text()
        result = provider.generate("inbox.reply", InboxReply, model_context(s, deal, m.body), s=s, module="inbox",
                                   system=system, prompt_version=PROMPT_VERSION, side="seller")
        r: InboxReply = clean_model(result.output)
        out.append(send(s, deal, provider, body=r.reply, topic="facts", discusses_listing=True,
                        extra={"disclosed": r.disclosed, "mode": result.mode, "model": result.model}, **kw))
    elif m.topic == "legal":
        out.append(send(s, deal, provider, body=LEGAL_REPLY, topic="legal", discusses_listing=False, **kw))
    elif m.topic == "neighbourhood":
        out.append(send(s, deal, provider, body=NEIGHBOURHOOD_REPLY, topic="neighbourhood",
                        discusses_listing=False, **kw))
    elif m.topic == "seller_only" or (m.topic == "showing" and not in_window(auth, e["slot"])):
        m.status = "to_seller"
        why = ("asks whether the seller would take a different price or terms" if m.topic == "seller_only" else
               f"asks for a showing {e['slot']['day']} at {e['slot']['hour']}:00, outside the seller's windows")
        m.extra = {**(m.extra or {}), "seller_question": why}
        out.append(send(s, deal, provider, body="Thank you. That is the seller's decision, so I have put it to "
                        "the seller and will come back to you today.", topic="holding", discusses_listing=True, **kw))
    elif m.topic == "showing":
        out.extend(book_showing(s, deal, provider, m, e, auth))
    elif m.topic == "feedback":
        summary = "Liked: the lot, the kitchen. Concerns: no central air, road noise from Route 292. May offer."
        m.extra = {**(m.extra or {}), "feedback_summary": summary}
        records.record_auto(s, deal.id, "CP-29", reason=f"Showing feedback logged on thread {m.thread}: {summary}",
                            attached_to=f"message:{m.id}")
        out.append(send(s, deal, provider, body="Thank you for the feedback; I have logged it for the seller. "
                        "Any written offer will be presented to the seller promptly.", topic="feedback",
                        discusses_listing=True, **kw))
    if m.status == "received":
        m.status = "answered"
    s.flush()
    return out


def book_showing(s: Session, deal: Deal, provider: ModelProvider, m: Message, e: dict, auth: dict) -> list[Message]:
    slot = e["slot"]
    when = f"{slot['day']} at {slot['hour']}:00"
    if not e.get("represented"):  # L15: no tour before the buyer agreement (or a written waiver) is on file
        return [send(s, deal, provider, thread=m.thread, party=m.party, topic="showing", discusses_listing=True,
                     body="Before a showing I need your signed buyer agreement or your agent's confirmation of one.")]
    self_guided = bool(e.get("self_guided")) and bool(auth.get("self_guided_tours"))
    records.record_auto(s, deal.id, "CP-29", reason=f"Showing booked within 24 hours for thread {m.thread}, {when}: "
                        + ("self-guided tour" if self_guided else "owner-hosted") + "; access and feedback "
                        "requests sent (simulated)", attached_to=f"message:{m.id}")
    if self_guided:
        records.mark_law(s, deal.id, "CP-28", reason=f"AI arranged a self-guided tour for thread {m.thread}, {when}",
                         attached_to=f"message:{m.id}")
        body = (f"Booked: a self-guided tour {when}. You will receive a one-time smart-lock code for that hour "
                "only; lockbox keys and PINs are never lent. Please send feedback afterwards.")
    else:
        records.record_human(s, deal.id, "CP-10", reason=f"The seller (owner) opens the door for the showing on "
                                                         f"thread {m.thread}, {when}")
        note = "" if not e.get("self_guided") else " (the seller has not allowed self-guided tours)"
        body = (f"Booked: a showing {when}{note}. The owner will open the door. Please send feedback afterwards.")
    m.extra = {**(m.extra or {}), "showing": {"when": when, "kind": "self-guided" if self_guided else "owner-hosted"}}
    return [send(s, deal, provider, thread=m.thread, party=m.party, body=body, topic="showing",
                 discusses_listing=True)]


SELLER_CHOICES = {
    "seller_only": {"invite_offer": "Invite a written offer; I will consider it",
                    "decline": "Not at that price for now"},
    "showing": {"allow": "Allow that time; I will open the door", "decline": "Decline; offer my usual windows"},
}


def seller_answer(s: Session, deal: Deal, provider: ModelProvider, persona: str, message_id: int,
                  choice: str) -> list[Message]:
    """The seller's own decision on a question only the seller can answer; the AI then replies within it."""
    if persona != "seller":
        raise NotYourDecision("Only the seller answers a question put to the seller.")
    m = s.get(Message, message_id)
    if m is None or m.deal_id != deal.id or m.status != "to_seller":
        raise ValueError("That question is not waiting for the seller.")
    if choice not in SELLER_CHOICES[m.topic]:
        raise ValueError(f"'{choice}' is not one of {list(SELLER_CHOICES[m.topic])}")
    m.status = "answered"
    m.extra = {**(m.extra or {}), "seller_choice": choice}
    record_event(s, actor="seller", kind="client_decision", entity="message", entity_id=m.id,
                 summary=f"The seller answered the question on thread {m.thread}: {choice}")
    kw = dict(thread=m.thread, party=m.party, discusses_listing=True)
    if m.topic == "seller_only":
        body = ("The seller would consider a written offer. Please send it with your proof of funds and preferred "
                "closing date; I will present it to the seller promptly." if choice == "invite_offer" else
                "The seller is not considering that price at present. Any written offer will still be presented.")
        return [send(s, deal, provider, body=body, topic="negotiation", **kw)]
    if choice == "allow":
        e = _enquiry(m)
        return book_showing(s, deal, provider, m, {**e, "self_guided": False}, authority(s, deal))
    return [send(s, deal, provider, body="That time doesn't work for the seller. Showings are available Saturday "
                 "10 to 4, Sunday 12 to 5 and Wednesday 5 to 7.", topic="showing", **kw)]


def seller_cards(s: Session, deal: Deal) -> list[Message]:
    return [m for m in messages(s, deal) if m.direction == "in" and m.status == "to_seller"]
