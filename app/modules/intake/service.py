"""Step 1 Intake: the AI's work (spec section 3, step 1).

Flow, each act a visible screen and a record:
1. `start_intake`: the seller's address and a handful of facts. The AI parses the address, pulls public-record
   facts (`PublicRecordConnector`), writes every fact with its source, sends the three first-contact notices
   (CP-24, automated) and opens the seller's decisions CP-01 (agency form) and CP-04 (PCDS).
2. `infer_gaps`: one model call (Haiku) fills gaps it can infer, each tagged *inferred* with its reason.
3. `disclosure_checklist`: which disclosures this house needs (code, from the facts; no model).
4. `accept_listing`: conflicts check, then the AI accepts the listing (CP-02, red "NY law today" marker) and
   generates the listing agreement, which opens CP-03 for the seller to sign. Signing needs CP-01 first (L12).
5. The PCDS (CP-04, L43) is the seller's own form: `app/disclosures/pcds.py`, the full 7/1/25 form.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import usaddress
import yaml
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit import record_event
from app.brokerage import brokerage
from app.connectors.public_records import SELLER_FIELDS, FixtureRecords
from app.model.context import AgentContext
from app.model.provider import ModelProvider, ModelResult
from app.models import Deal, Disclosure, Document, Person, Property, PropertyFact, now
from app.modules.intake.schemas import IntakeInference
from app.pii import MASKER
from app.records import service as records
from app.sanitize import clean_model

PROMPTS = Path(__file__).with_name("prompts")
PROMPT_VERSION = "infer_gaps.v1"

# The four RPL §242 questions (L60), asked on the intake form.
SECTION_242 = {
    "no_electric_service": "Does the property have no electric service?",
    "utility_surcharge": "Is the property subject to a utility surcharge for extending service?",
    "green_jobs_charge": "Is there a green-jobs / energy-efficiency on-bill charge tied to the property?",
    "uncapped_gas_well": "Do you know of an uncapped natural gas well on the property?",
}



@dataclass
class IntakeInput:
    street: str
    city: str
    zip: str
    seller_name: str
    seller_email: str
    seller_phone: str
    facts: dict[str, str]  # keys from SELLER_FIELDS and SECTION_242


def load_personas() -> dict:
    from app.config import ROOT

    return yaml.safe_load((ROOT / "seed" / "personas.yaml").read_text())


def demo_input() -> IntakeInput:
    """What the "Use demo house" button fills in."""
    p = load_personas()["seller"]
    return IntakeInput(street="146 Route 292", city="Holmes", zip="12531", seller_name=p["legal_name"],
                       seller_email=p["email"], seller_phone=p["phone"], facts=dict(p["intake_answers"]))


def parse_address(raw: str) -> dict:
    """usaddress tags the parts; on failure keep the raw text (the profile shows what was parsed)."""
    try:
        tagged, kind = usaddress.tag(raw)
    except usaddress.RepeatedLabelError:
        return {"raw": raw, "parsed": False}
    return {"raw": raw, "parsed": True, "kind": kind, **dict(tagged)}


def start_intake(s: Session, data: IntakeInput, connector: FixtureRecords | None = None) -> Deal:
    connector = connector or FixtureRecords()
    parsed = parse_address(f"{data.street}, {data.city}, NY {data.zip}")
    found = connector.lookup(data.street, data.city, data.zip)
    addr = found.address
    prop = Property(street=addr.get("street") or data.street, city=addr.get("city") or data.city,
                    zip=addr.get("zip") or data.zip, county=addr.get("county"),
                    municipality=addr.get("municipality"), latitude=addr.get("latitude"),
                    longitude=addr.get("longitude"), upi=addr.get("upi"), is_demo_house=found.found)
    s.add(prop)
    s.flush()
    for f in found.facts:
        s.add(PropertyFact(property_id=prop.id, field=f.field, label=f.label, group=f.group, value=f.value,
                           source=f.source, source_ref=f.source_ref, confidence=f.confidence,
                           inferred_reason=f.inferred_reason))
    if found.found:  # code-level inference with a reason (no model needed)
        yb = connector.year_built()
        s.add(PropertyFact(property_id=prop.id, field="LeadPaintDisclosure", label="Lead-paint disclosure",
                           group="Records", value="Not required" if yb >= 1978 else "Required",
                           source="inferred", confidence="high",
                           inferred_reason=f"Built {yb}; the federal lead-paint disclosure applies to homes built "
                                           f"before 1978 (L44)"))
    for key, (field, label, group) in SELLER_FIELDS.items():
        v = (data.facts.get(key) or "").strip()
        if v:
            s.add(PropertyFact(property_id=prop.id, field=field, label=label, group=group, value=v,
                               source="seller", source_ref="Seller, on the intake screen", confidence="medium"))
    seller = Person(role="seller", persona_label="Seller", token="SELLER_1", legal_name=data.seller_name,
                    email=data.seller_email, phone=data.seller_phone)
    s.add(seller)
    s.flush()
    for value, label in ((data.seller_name, "[SELLER_1]"), (data.seller_email, "[EMAIL]"),
                         (data.seller_phone, "[PHONE]")):
        MASKER.register(value, label)
    deal = Deal(property_id=prop.id, seller_id=seller.id, status="intake", current_step=1)
    s.add(deal)
    s.flush()
    record_event(s, actor="ai", kind="ai_action", entity="deal", entity_id=deal.id,
                 summary=(f"Intake: address parsed ({'ok' if parsed['parsed'] else 'unparsed'}); "
                          f"{len(found.facts)} public-record facts; record {'found' if found.found else 'not found'}"))
    _checklist(s, deal, seller, connector, data.facts, found.found)
    # First substantive contact: the AI sends the three notices (CP-24, one record each).
    for d in s.execute(select(Disclosure).where(Disclosure.deal_id == deal.id,
                                                Disclosure.kind.in_(("fair_housing", "agency",
                                                                     "not_legal_services")))).scalars():
        d.delivered_at = now()
        records.record_auto(s, deal.id, "CP-24", reason=f"Sent to the seller: {d.title} ({d.l_id})",
                            attached_to=f"disclosure:{d.id}")
    records.open_decision(s, deal.id, "CP-01", attached_to="disclosure:agency")
    records.open_decision(s, deal.id, "CP-04", attached_to="disclosure:pcds")
    # Standing and planned records, so the timeline shows the whole sale from the start.
    for code in ("CP-35", "CP-20", "CP-21", "CP-22", "CP-23", "CP-34"):
        records.plan(s, deal.id, code)
    return deal


def _checklist(s: Session, deal: Deal, seller: Person, connector: FixtureRecords, facts: dict, found: bool) -> None:
    yb = connector.year_built() if found else None
    ag = connector.in_ag_district() if found else None
    any_242 = [k for k in SECTION_242 if (facts.get(k) or "no").lower().startswith("y")]
    items = [
        ("agency", "NY agency disclosure form (DOS-1736-f)", "L12", "Before the listing agreement", True, None),
        ("fair_housing", "NY Housing and Anti-Discrimination Disclosure (DOS-2156)", "L39",
         "First substantive contact", True, None),
        ("not_legal_services", '"These are not legal services" notice', "L29", "Onboarding", True, None),
        ("pcds", "Property Condition Disclosure Statement (RPL §462, 7/1/25 form)", "L43",
         "Before the buyer signs a contract", True, "The seller completes it; the software never pre-fills it"),
        ("lead_paint", "Lead-based paint disclosure and pamphlet", "L44", "Before a contract",
         yb is None or yb < 1978,
         f"Built {yb}: only homes built before 1978" if yb else "Year built unknown: confirm"),
        ("ag_district", "Agricultural district notice (AML §310)", "L46", "Before a contract",
         ag is None or bool(ag), "No agricultural district on the record" if ag is False else "Check the parcel"),
        ("section_242", "RPL §242 seller notices (four questions)", "L60", "Before accepting an offer",
         bool(any_242), ("The seller answered yes to: " + ", ".join(any_242)) if any_242
         else "The seller answered no to all four questions on the intake screen"),
    ]
    for kind, title, l_id, trigger, required, reason in items:
        s.add(Disclosure(deal_id=deal.id, person_id=seller.id, kind=kind, title=title, l_id=l_id, trigger=trigger,
                         required=required, required_reason=reason))
    s.flush()


def model_context(s: Session, deal: Deal) -> dict:
    """The whitelist for the intake call: property facts and the gap list. No PII: no name, e-mail or phone."""
    ctx = AgentContext(s, deal, "seller").build(instructions=False)
    data = FixtureRecords().data if deal.property.is_demo_house else {"gaps": []}
    ctx["gaps"] = [{"field": g["field"], "detail": g["detail"]} for g in data["gaps"]
                   if g["field"] not in ("photos", "putnam_comparables", "recent_sales")]
    return ctx


def infer_gaps(s: Session, deal: Deal, provider: ModelProvider) -> ModelResult:
    system = (PROMPTS / f"{PROMPT_VERSION}.md").read_text()
    result = provider.generate("intake.infer_gaps", IntakeInference, model_context(s, deal), s=s, module="intake",
                               system=system, prompt_version=PROMPT_VERSION, side="seller")
    out: IntakeInference = clean_model(result.output)
    result.output = out
    existing = {f.field for f in deal.property.facts}
    for inf in out.inferences:
        if inf.field in existing:
            continue
        s.add(PropertyFact(property_id=deal.property_id, field=inf.field, label=inf.label, group="Inferred by the AI",
                           value=inf.value, source="inferred", confidence=inf.confidence,
                           inferred_reason=inf.reason, source_ref=f"AI ({result.mode}, {result.model})"))
    record_event(s, actor="ai", kind="ai_action", entity="deal", entity_id=deal.id,
                 summary=f"Intake: AI inferred {len(out.inferences)} facts ({result.mode})")
    s.flush()
    s.refresh(deal.property)
    return result


def conflicts_check(s: Session, deal: Deal) -> dict:
    """The firm has no other client with an interest in this property (no buyer client yet in slice 1)."""
    others = s.execute(select(Deal).where(Deal.property_id == deal.property_id, Deal.id != deal.id)).scalars().all()
    buyer = deal.buyer_id is not None
    clear = not others and not buyer
    return {"clear": clear,
            "detail": "No other client of the firm has an interest in this property; no buyer client yet."
            if clear else "Another client of the firm has an interest in this property: dual agency consent needed."}


def accept_listing(s: Session, deal: Deal) -> Document:
    """The AI accepts the listing (CP-02 marker) and generates the listing agreement (opens CP-03)."""
    check = conflicts_check(s, deal)
    records.mark_law(s, deal.id, "CP-02",
                     reason=f"AI accepted the listing for {deal.property.street} after a conflicts check: "
                            f"{check['detail']}")
    doc = s.execute(select(Document).where(Document.deal_id == deal.id, Document.kind == "listing_agreement")
                    ).scalar_one_or_none()
    if doc is None:
        doc = Document(deal_id=deal.id, kind="listing_agreement", generated_by="ai", label_version="v1")
        s.add(doc)
        s.flush()
    records.open_decision(s, deal.id, "CP-03", attached_to=f"document:{doc.id}")
    deal.status = "listing_offered"
    return doc


def sign_listing_agreement(s: Session, deal: Deal, persona: str, decision: str = "sign"):
    """Signing needs the agency form acknowledged first (L12: before the listing agreement)."""
    records.require(s, deal.id, "CP-01", action="sign the listing agreement")
    cp = records.latest(s, deal.id, "CP-03")
    if cp is None:
        raise records.GateError("CP-02", "The AI has not accepted the listing yet, so there is no agreement to sign.")
    records.decide(s, cp, persona=persona, decision=decision,
                   reason="Signed (simulated e-sign, L34)" if decision == "sign" else "Declined")
    if cp.status == "done":
        doc = s.execute(select(Document).where(Document.deal_id == deal.id, Document.kind == "listing_agreement")
                        ).scalar_one()
        doc.signed_by = {"seller": now().isoformat()}
        deal.status = "listed"
    return cp


def acknowledge_agency(s: Session, deal: Deal, persona: str, decision: str = "acknowledge"):
    cp = records.latest(s, deal.id, "CP-01")
    records.decide(s, cp, persona=persona, decision=decision)
    d = s.execute(select(Disclosure).where(Disclosure.deal_id == deal.id, Disclosure.kind == "agency")).scalar_one()
    d.acknowledged_at = now()
    return cp


def profile_groups(deal: Deal) -> list[tuple[str, list[PropertyFact]]]:
    order = ["Location", "Structure", "Systems", "Land", "Records", "Inferred by the AI"]
    groups: dict[str, list[PropertyFact]] = {}
    for f in deal.property.facts:
        groups.setdefault(f.group, []).append(f)
    return [(g, groups[g]) for g in order if g in groups] + [(g, v) for g, v in groups.items() if g not in order]


def presentation() -> dict:
    b = brokerage()
    return {"services": b["services"], "fee": b["flat_fee"], "timeline": b["timeline"]}
