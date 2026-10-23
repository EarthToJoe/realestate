"""Step 7 Contract (spec section 3, step 7): the AI drafts the contract of sale and rider for the parties, in the
product's own contract step (decision 21). No attorney screen or persona; no attorney-approval clause (decision 26).

1. `send_memorandum`: the accepted-offer memorandum to both parties (simulated). CP-32 (automated).
2. `draft`: one model call (`contract.draft`) writes the contract and rider in the bar-association long form's
   paragraph order (`STANDARD_FORM`, headings only) and the side-by-side notes. CP-14 marker: NY law today says only
   a lawyer may draft a contract of sale for another; the marker names the lawful launch route.
3. `check_draft`: code, not the model, checks the draft against the deal (price, deposit, closing date, parties),
   against L23 (never say a lawyer is unnecessary) and decision 26 (no attorney-approval clause), and that the
   side-by-side covers all 28 paragraphs. A block finding keeps signing shut.
4. `attach_disclosures`: the PCDS (the seller's own, CP-04), lead paint, agricultural district and RPL §242 items
   (CP-32). Signing is refused until the PCDS is completed (L43).
5. `open_signing` / `sign`: CP-33, the seller's and the buyer's own simulated e-signatures (L34). The signing map
   (`SIGNING_MAP`) marks what e-signature cannot cover: the deed's notary acknowledgment, a power of attorney's two
   witnesses, the smoke-detector affidavit at conveyance (CP-15, human required, planned for closing).

Every page of the draft (screen, PDF, DOCX) carries `LABEL`. The model sees party tokens, never names; names are
inserted only when the PDF or DOCX is rendered, and that access is logged.
"""

from __future__ import annotations

import copy
import re
from datetime import date, timedelta
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session, object_session

from app.audit import record_event
from app.disclosures import pcds
from app.model.context import AgentContext
from app.model.provider import ModelProvider
from app.models import ContractState, Deal, Disclosure, Document, now
from app.modules.contract.schemas import ContractDraft
from app.modules.offers import service as offers
from app.records import service as records
from app.sanitize import clean_model

PROMPTS = Path(__file__).with_name("prompts")
PROMPT_VERSION = "draft.v1"
LABEL = ("DEMONSTRATION. Drafted by software for the parties. NY law today: only a lawyer may draft a contract of "
         "sale for another (L21, L22).")
LABEL_VERSION = "d26-v1"
SIGNING_DATE = date(2026, 10, 23)  # the demonstration's signing date, for the closing date in the draft

# The bar-association Residential Contract of Sale (jointly prepared by the NYSBA Real Property Section and others,
# form 11-2000): its paragraph headings only, read 2026-10-23 from a published copy (Justia forms) [SECONDARY].
# Structure is not protected expression; no clause text is used (spec section 1, "Borrow ideas").
STANDARD_FORM = [
    "Premises", "Personal Property", "Purchase Price", "Existing Mortgage", "Purchase Money Mortgage",
    "Downpayment in Escrow", "Acceptable Funds", "Mortgage Commitment Contingency", "Permitted Exceptions",
    "Governmental Violations and Orders", "Seller's Representations", "Condition of Property", "Insurable Title",
    "Closing, Deed and Title", "Closing Date and Place", "Conditions to Closing", "Deed Transfer and Recording Taxes",
    "Apportionments and Other Adjustments; Water Meter and Installment Assessments", "Allowance for Unpaid Taxes, etc.",
    "Use of Purchase Price to Remove Encumbrances",
    "Title Examination; Seller's Inability to Convey; Limitations of Liability",
    "Affidavit as to Judgments, Bankruptcies, etc.", "Defaults and Remedies", "Purchaser's Lien", "Notices",
    "No Assignment", "Broker", "Miscellaneous"]
STANDARD_SOURCE = ("Bar-association Residential Contract of Sale (form 11-2000), paragraph headings only, from a "
                   "published copy (forms.justia.com), read 2026-10-23 [SECONDARY]")

# What e-signature covers and what it does not (L34, L35, L45). Rows: document, who signs, how, law, when.
SIGNING_MAP = [
    {"doc": "Contract of sale and rider", "who": "Seller and buyer", "how": "e-sign", "law": "L34; L24",
     "when": "Now (step 7)"},
    {"doc": "Property Condition Disclosure Statement", "who": "Seller signs; buyer acknowledges receipt",
     "how": "e-sign", "law": "L43; L34", "when": "Seller: done in CP-04; buyer: with the contract"},
    {"doc": "Accepted-offer memorandum", "who": "No signature (sent to both parties)", "how": "sent",
     "law": "F50", "when": "Before the draft"},
    {"doc": "Deed", "who": "Seller", "how": "wet ink, acknowledged before a notary", "law": "L35 (RPL §291)",
     "when": "Closing (CP-15)"},
    {"doc": "Power of attorney, if a party signs through one", "who": "The party", "how": "wet ink, two witnesses",
     "law": "L35 (GOL §5-1501B)", "when": "Before closing (CP-15)"},
    {"doc": "Smoke and carbon-monoxide detector affidavit", "who": "Seller", "how": "signed at conveyance",
     "law": "L45 (Executive Law §378(5-b))", "when": "Closing (CP-15)"},
]

L23_PATTERNS = [r"(do(es)?n['’]?t|do(es)? not|no) need (a |an |to (hire|retain|use) (a |an )?)?(lawyer|attorney)",
                r"no (need|reason) (for|to (hire|retain|use|consult)) (a |an )?(lawyer|attorney|counsel)",
                r"without (the need for |needing )?(a |an )?(lawyer|attorney)s?\b",
                r"(lawyer|attorney|counsel)s? (is|are) (not )?(unnecessary|not needed|not required)",
                r"replaces? (a |an |your )?(lawyer|attorney)"]
APPROVAL_PATTERN = r"subject to (the )?(review and )?approval (of|by) (each|the|both)?\s*(part(y|ies)['’]?s?\s+)?(attorney|counsel|lawyer)"


# ---- state ------------------------------------------------------------------------------------------------------

def _row(deal: Deal) -> ContractState:
    s = object_session(deal)
    row = s.execute(select(ContractState).where(ContractState.deal_id == deal.id)).scalar_one_or_none()
    if row is None:
        row = ContractState(deal_id=deal.id, state={})
        s.add(row)
        s.flush()
    return row


def state(deal: Deal) -> dict:
    return copy.deepcopy(_row(deal).state or {})


def _save(s: Session, deal: Deal, st: dict) -> None:
    _row(deal).state = st
    s.flush()


def accepted(deal: Deal) -> dict:
    a = offers.state(deal).get("accepted")
    if not a:
        raise records.GateError("CP-12", "There is no agreed offer yet: the contract follows the seller's decision "
                                         "and the negotiation in step 6.")
    return a


def closing_date(a: dict) -> str:
    d = SIGNING_DATE + timedelta(days=int(a["closing_days"]))
    return f"{d:%B} {d.day}, {d.year}"


def money(v: int) -> str:
    return f"${int(v):,}"


# ---- 1. memorandum -------------------------------------------------------------------------------------------------

def memorandum(deal: Deal) -> dict:
    a = accepted(deal)
    return {"property": f"{deal.property.street}, {deal.property.city}, NY {deal.property.zip}",
            "seller": "[SELLER_1]", "buyer": "[BUYER_1]", "price": a["final_price"],
            "deposit": a["final_price"] * a["deposit_pct"] // 100, "deposit_pct": a["deposit_pct"],
            "financing": a["financing"], "mortgage_days": a["mortgage_days"],
            "inspection_days": a["inspection_days"], "contingencies": a["contingencies"],
            "requests": a.get("requests") or [], "closing_days": a["closing_days"], "closing_date": closing_date(a),
            "agreed_by": a["agreed_by"], "dual_agency": a.get("side") == "firm_buyer",
            "note": offers.NOT_BINDING}


def send_memorandum(s: Session, deal: Deal) -> dict:
    m = memorandum(deal)
    st = state(deal)
    if st.get("memorandum"):
        return st["memorandum"]
    doc = Document(deal_id=deal.id, kind="accepted_offer_memorandum", generated_by="ai", label_version=LABEL_VERSION)
    s.add(doc)
    s.flush()
    records.record_auto(s, deal.id, "CP-32", reason=f"Accepted-offer memorandum sent to both parties (simulated): "
                                                     f"{money(m['price'])}, closing {m['closing_date']}",
                        attached_to=f"document:{doc.id}")
    st["memorandum"] = {**m, "sent_at": now().isoformat(), "document_id": doc.id}
    _save(s, deal, st)
    return st["memorandum"]


# ---- 2. the draft -------------------------------------------------------------------------------------------------

def disclosures(s: Session, deal: Deal) -> list[dict]:
    """The disclosures that go with the contract, with their state (L43, L44, L46, L60)."""
    rows = {d.kind: d for d in s.execute(select(Disclosure).where(Disclosure.deal_id == deal.id)).scalars()}
    out = [{"kind": "pcds", "title": f"Property Condition Disclosure Statement ({pcds.form()['version']} form)",
            "l_id": "L43", "required": True,
            "status": "completed by the seller" if records.is_done(s, deal.id, "CP-04") else "waiting for the seller (CP-04)",
            "ready": records.is_done(s, deal.id, "CP-04")}]
    for kind in ("lead_paint", "ag_district", "section_242"):
        d = rows.get(kind)
        if d is None:
            continue
        out.append({"kind": kind, "title": d.title, "l_id": d.l_id, "required": d.required,
                    "status": ("to deliver with the contract" if d.required else f"not required: {d.required_reason}"),
                    "ready": True})
    return out


def model_context(s: Session, deal: Deal) -> dict:
    """The whitelist for the draft: party tokens, the property's facts, the agreed terms, the disclosures' state.
    No names, no e-mail, no phone, and neither side's confidential instructions."""
    a = accepted(deal)
    answers = pcds.answers_of(s, deal) if records.is_done(s, deal.id, "CP-04") else {}
    ctx = AgentContext(s, deal, "seller").build(
        facts=["ArchitecturalStyle", "YearBuilt", "LivingArea", "BedroomsTotal", "BathroomsFull", "LotSizeAcres",
               "HeatingFuel", "WaterSource", "Sewer", "FloodZone", "SchoolDistrict", "TaxAnnualAmount"],
        instructions=False)
    ctx["acting_for"] = "both parties (the product's own contract step)"
    ctx["parties"] = {"seller": "[SELLER_1]", "buyer": "[BUYER_1]"}
    ctx["property"]["municipality"] = deal.property.municipality or "Town of Pawling"
    ctx["property"]["county"] = deal.property.county or "Dutchess"
    ctx["terms"] = {"price": a["final_price"], "deposit_pct": a["deposit_pct"],
                    "deposit": a["final_price"] * a["deposit_pct"] // 100, "financing": a["financing"],
                    "mortgage_commitment_days": a["mortgage_days"], "inspection_days": a["inspection_days"],
                    "contingencies": a["contingencies"], "personal_property_included": a.get("requests") or [],
                    "closing_date": closing_date(a), "closing_days": a["closing_days"],
                    "escrow_holder": "to be named by the parties (a third party; by Hudson Valley custom the "
                                     "seller's attorney's escrow account)",
                    "brokerage": "Hudson Valley AI Realty (demonstration name), acting for both parties with their "
                                 "written dual-agency consent" if a.get("side") == "firm_buyer" else
                                 "Hudson Valley AI Realty (demonstration name) for the seller; the buyer's agent "
                                 "at another firm"}
    ctx["disclosures"] = [{k: d[k] for k in ("title", "l_id", "required", "status")} for d in disclosures(s, deal)]
    ctx["pcds_known_facts"] = pcds.summary(answers) if answers else []
    ctx["standard_form_headings"] = [f"{i}. {h}" for i, h in enumerate(STANDARD_FORM, 1)]
    return ctx


def draft(s: Session, deal: Deal, provider: ModelProvider) -> dict:
    a = accepted(deal)
    send_memorandum(s, deal)
    system = (PROMPTS / f"{PROMPT_VERSION}.md").read_text()
    result = provider.generate("contract.draft", ContractDraft, model_context(s, deal), s=s, module="contract",
                               system=system, prompt_version=PROMPT_VERSION, side=None)
    d: ContractDraft = clean_model(result.output)
    body = d.model_dump()
    findings = check_draft(body, a)
    st = state(deal)
    version = int(st.get("version") or 0) + 1
    st.update({"draft": body, "findings": findings, "version": version, "mode": result.mode, "model": result.model,
               "recorded_at": result.recorded_at, "passed": not any(f["tier"] == "block" for f in findings)})
    _save(s, deal, st)
    for kind in ("contract_draft", "rider"):
        s.add(Document(deal_id=deal.id, kind=kind, version=version, generated_by="ai", label_version=LABEL_VERSION))
    records.mark_law(s, deal.id, "CP-14", reason=f"The AI drafted the contract of sale and rider for both parties "
                                                  f"(version {version}; {len(d.sections)} clauses, rider "
                                                  f"{len(d.rider)}; {result.mode}, {result.model})",
                     attached_to=f"contract:v{version}")
    record_event(s, actor="ai", kind="ai_action", entity="deal", entity_id=deal.id,
                 summary=f"Contract: AI drafted version {version}; code checks "
                         f"{'passed' if st['passed'] else 'found a block'} ({len(findings)} findings)")
    return st


def _all_text(body: dict) -> str:
    return "\n".join(f"{c['heading']}. {c['text']}" for c in body["sections"] + body["rider"]) + "\n" + \
        "\n".join(body.get("notes_to_parties") or [])


def check_draft(body: dict, a: dict) -> list[dict]:
    """Code checks on the draft. Tier block keeps signing shut; warn is shown."""
    text = _all_text(body)
    flat = text.replace(" ", " ")
    out = []

    def find(tier, rule, message):
        out.append({"tier": tier, "rule": rule, "message": message})
    price = money(a["final_price"])
    if price not in flat:
        find("block", "deal-price", f"The agreed price {price} does not appear in the draft.")
    deposit = money(a["final_price"] * a["deposit_pct"] // 100)
    if deposit not in flat:
        find("block", "deal-deposit", f"The deposit {deposit} does not appear in the draft.")
    if closing_date(a) not in flat:
        find("block", "deal-closing", f"The closing date {closing_date(a)} does not appear in the draft.")
    for days, what in ((a["inspection_days"], "inspection"), (a["mortgage_days"], "mortgage commitment")):
        if not re.search(rf"\b{days}\b", flat):
            find("block", f"deal-{what.split()[0]}", f"The {what} period ({days} days) does not appear in the draft.")
    for token in ("[SELLER_1]", "[BUYER_1]"):
        if token not in flat:
            find("block", "parties", f"The party {token} is not named in the draft.")
    for pat in L23_PATTERNS:
        m = re.search(pat, flat, re.I)
        if m:
            find("block", "L23", f"The draft says or implies a lawyer is unnecessary (\"{m.group(0)}\"); the "
                                 "product must never say that (L23).")
    m = re.search(APPROVAL_PATTERN, flat, re.I)
    if m:
        find("warn", "decision-26", f"The draft has an attorney-approval clause (\"{m.group(0)}\"); the demonstration "
                                    "has none (decision 26). Shown, not removed.")
    covered = {r["standard_number"] for r in body.get("side_by_side") or []}
    missing = [i for i in range(1, len(STANDARD_FORM) + 1) if i not in covered]
    if missing:
        find("warn", "side-by-side", "The side-by-side has no note for paragraph(s) "
                                     + ", ".join(map(str, missing)) + "; shown as \"not covered\".")
    if not body["rider"]:
        find("block", "rider", "The draft has no rider.")
    return out


def side_by_side(body: dict) -> list[dict]:
    rows = {r["standard_number"]: r for r in body.get("side_by_side") or []}
    return [{"n": i, "heading": h, "draft_ref": rows.get(i, {}).get("draft_ref", "none"),
             "note": rows.get(i, {}).get("note", "Not covered in the draft (shown by code).")}
            for i, h in enumerate(STANDARD_FORM, 1)]


# ---- 4. disclosures and 5. signing ---------------------------------------------------------------------------------

def attach_disclosures(s: Session, deal: Deal) -> dict:
    st = state(deal)
    if not st.get("draft"):
        raise ValueError("Draft the contract first.")
    items = disclosures(s, deal)
    if st.get("attached") and all(i["ready"] for i in items) and st["attached"]["complete"]:
        return st["attached"]
    complete = all(i["ready"] for i in items)
    st["attached"] = {"items": items, "complete": complete, "at": now().isoformat()}
    _save(s, deal, st)
    if complete:
        records.record_auto(s, deal.id, "CP-32", reason="Disclosures attached to the contract: " + "; ".join(
            f"{i['title']} ({i['status']})" for i in items), attached_to="contract:disclosures")
        for d in s.execute(select(Disclosure).where(Disclosure.deal_id == deal.id,
                                                    Disclosure.kind == "pcds")).scalars():
            d.delivered_at = now()
    return st["attached"]


def open_signing(s: Session, deal: Deal):
    """CP-33 opens only when the draft passed its checks and every disclosure is attached; the PCDS first (L43)."""
    st = state(deal)
    if not st.get("draft"):
        raise ValueError("Draft the contract first.")
    if not st.get("passed"):
        raise ValueError("The draft has a block finding from the code checks; the AI must redraft before anyone "
                         "signs.")
    records.require(s, deal.id, "CP-04", action="open the contract for signing (the seller's Property Condition "
                                                "Disclosure Statement must be delivered before the buyer signs, L43)")
    attached = attach_disclosures(s, deal)
    if not attached["complete"]:
        raise ValueError("Not every disclosure is attached yet.")
    if not records.latest(s, deal.id, "CP-15"):
        records.plan(s, deal.id, "CP-15")
    cp = records.latest(s, deal.id, "CP-33")
    if cp and cp.status in ("pending", "done"):
        return cp
    return records.open_decision(s, deal.id, "CP-33", reason="The contract and rider are ready to sign (simulated "
                                                             "e-sign, L34)", attached_to=f"contract:v{st['version']}")


def sign(s: Session, deal: Deal, persona: str, decision: str):
    cp = records.latest(s, deal.id, "CP-33")
    if cp is None:
        raise ValueError("The contract is not open for signing yet.")
    records.decide(s, cp, persona=persona, decision=decision,
                   reason=f"Signed by the {persona} (simulated e-signature, L34)" if decision == "sign" else
                   f"The {persona} declined to sign")
    if cp.status == "done":
        st = state(deal)
        st["signed_at"] = now().isoformat()
        _save(s, deal, st)
        for doc in s.execute(select(Document).where(Document.deal_id == deal.id,
                                                    Document.kind.in_(("contract_draft", "rider")),
                                                    Document.version == st["version"])).scalars():
            doc.signed_by = {"seller": st["signed_at"], "buyer": st["signed_at"]}
        deal.status = "under_contract"
        deal.current_step = max(deal.current_step, 8)
        record_event(s, actor="system", kind="system", entity="deal", entity_id=deal.id,
                     summary="Contract signed by both parties (simulated e-signatures); binding in a real deal")
    return cp


def names(deal: Deal) -> dict[str, str]:
    """The party tokens and their names, for the rendered PDF and DOCX only."""
    out = {"[SELLER_1]": deal.seller.legal_name if deal.seller else "[SELLER_1]",
           "[BUYER_1]": deal.buyer.legal_name if deal.buyer else "[BUYER_1]"}
    return out


def fill(text: str, mapping: dict[str, str]) -> str:
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text
