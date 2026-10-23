"""Step 3 Listing copy (spec section 3, step 3; section 5).

The package is `listing_copy` (the spec calls the module `copy`; that name would shadow Python's `copy`).

1. `draft`: one model call (`copy.draft`) writes the MLS remarks, the portal description, three social posts and
   the flyer from the property profile and the seller's chosen price. Refused until CP-05 (the seller chose the
   price) and CP-03 (the listing agreement: no marketing without it, L9).
2. `check`: the fair-housing pipeline on one artifact's exact text (rules pass + model review pass). A pass writes
   CP-26 (automated, per artifact).
3. `plant` (demo button) adds a planted violation as a new version; `apply_fix` makes the AI's fixed version the
   next version; both re-run the check.
4. `mark_ready`: the AI marks a passing artifact "ready to publish" and writes the CP-06 marker (per artifact).
   Refused, in this service layer, unless the newest fair-housing result passed on exactly this version and text
   (`fairhousing.require_pass`) and, for the MLS remarks, the MLS pre-check has no failure.
5. `mls_precheck` and `mls_package`: OneKey's remarks rules and the package the licensed participant keys (step 4).
"""

from __future__ import annotations

import re
from pathlib import Path

from markupsafe import Markup, escape
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit import record_event
from app.brokerage import brokerage
from app.fairhousing import check as fh
from app.model.context import AgentContext
from app.model.provider import ModelProvider, ModelResult
from app.models import CopyArtifact, Deal, FairHousingResult, now
from app.modules.listing_copy.schemas import ListingCopy
from app.records import service as records
from app.sanitize import clean_model

PROMPTS = Path(__file__).with_name("prompts")
PROMPT_VERSION = "draft.v1"
PLANTED = "Perfect for a young family, steps from the church."
DEMO_MARK = "DEMONSTRATION: not a listing, not for sale through this firm, no owner authority."

CHANNELS = [
    ("mls_remarks", "MLS public remarks"),
    ("portal", "Portal description"),
    ("social_1", "Social post 1"),
    ("social_2", "Social post 2"),
    ("social_3", "Social post 3"),
    ("flyer", "One-page flyer"),
]
MLS_REMARKS_LIMIT = 1000  # [INFERENCE] OneKey's public-remarks limit is not confirmed; 1,000 is assumed

COPY_FACTS = ["PropertySubType", "ArchitecturalStyle", "YearBuilt", "LivingArea", "Basement",
              "BelowGradeFinishedArea", "Stories", "BedroomsTotal", "BathroomsFull", "BathroomsHalf", "Heating",
              "HeatingFuel", "Cooling", "WaterSource", "Sewer", "LotSizeAcres", "OtherStructures",
              "WaterfrontFeatures", "SchoolDistrict", "Zoning", "FloodZone", "ParkingFeatures", "ConditionUpdates",
              "RoofYear", "OilTank", "SellerNotes", "TaxAnnualAmount", "AssociationYN"]


def artifacts(s: Session, deal: Deal) -> list[CopyArtifact]:
    rows = s.execute(select(CopyArtifact).where(CopyArtifact.deal_id == deal.id)).scalars().all()
    order = {c: i for i, (c, _) in enumerate(CHANNELS)}
    return sorted(rows, key=lambda a: order.get(a.channel, 99))


def get(s: Session, deal: Deal, artifact_id: int) -> CopyArtifact:
    art = s.get(CopyArtifact, artifact_id)
    if art is None or art.deal_id != deal.id:
        raise LookupError("No such copy artifact for this deal.")
    return art


def model_context(s: Session, deal: Deal) -> dict:
    """Whitelist: property facts, neighbourhood facts marked fit for copy, the chosen price, the firm's name.
    No PII, no seller instructions (motivation and floor stay out of the copy)."""
    from app.connectors.public_records import FixtureRecords

    ctx = AgentContext(s, deal, "seller").build(facts=COPY_FACTS, instructions=False)
    nb = FixtureRecords().data["neighbourhood"] if deal.property.is_demo_house else []
    ctx["setting"] = [{"fact": n["fact"], "drive_min": n.get("drive_min"), "distance_mi": n.get("distance_mi_straight")}
                      for n in nb if n.get("copy_ok")]
    ctx["list_price"] = deal.list_price
    ctx["firm"] = brokerage()["name"]
    return ctx


def flyer_text(f: dict) -> str:
    return "\n".join([f["headline"], f["subhead"], *[f"- {b}" for b in f["bullets"]], f["paragraph"]])


def parse_flyer(text: str) -> dict:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    bullets = [ln[2:] for ln in lines if ln.startswith("- ")]
    rest = [ln for ln in lines if not ln.startswith("- ")]
    return {"headline": rest[0] if rest else "", "subhead": rest[1] if len(rest) > 1 else "",
            "bullets": bullets, "paragraph": " ".join(rest[2:])}


def draft(s: Session, deal: Deal, provider: ModelProvider) -> ModelResult | None:
    records.require(s, deal.id, "CP-03", action="write listing copy (no marketing before the listing agreement, L9)")
    records.require(s, deal.id, "CP-05", action="write listing copy (the seller chooses the list price first)")
    if artifacts(s, deal):
        return None
    system = (PROMPTS / f"{PROMPT_VERSION}.md").read_text()
    result = provider.generate("copy.draft", ListingCopy, model_context(s, deal), s=s, module="listing_copy",
                               system=system, prompt_version=PROMPT_VERSION, side="seller")
    out: ListingCopy = clean_model(result.output)
    result.output = out
    texts = {"mls_remarks": (out.mls_remarks, None), "portal": (out.portal_description, None)}
    for i, p in enumerate(out.social_posts[:3], 1):
        texts[f"social_{i}"] = (p.text, {"platform": p.platform})
    texts["flyer"] = (flyer_text(out.flyer.model_dump()), None)
    for channel, title in CHANNELS:
        if channel not in texts:
            continue
        text, extra = texts[channel]
        s.add(CopyArtifact(deal_id=deal.id, channel=channel, title=title, text=text, extra=extra,
                           mode=result.mode, model=result.model))
    s.flush()
    record_event(s, actor="ai", kind="ai_action", entity="deal", entity_id=deal.id,
                 summary=f"Listing copy: AI wrote {len(texts)} pieces ({result.mode}, {result.model})")
    for art in artifacts(s, deal):
        check(s, deal, art, provider)
    return result


def check(s: Session, deal: Deal, art: CopyArtifact, provider: ModelProvider) -> FairHousingResult:
    res = fh.run(s, text=art.text, provider=provider, entity="copy_artifact", entity_id=art.id,
                 version=art.version, deal_id=deal.id, channel=art.channel)
    art.status = "passed" if res.passed else "blocked"
    if res.passed:
        warns = len(res.findings)
        records.record_auto(s, deal.id, "CP-26",
                            reason=f"Fair-housing check passed: {art.title} v{art.version} ({res.rules_version}; "
                                   f"model review {res.model_mode}; {warns} warn finding(s) handled)",
                            attached_to=f"copy_artifact:{art.id}:v{art.version}")
    s.flush()
    return res


def _new_version(s: Session, art: CopyArtifact, text: str, edited_by: str) -> None:
    art.text = text
    art.version += 1
    art.edited_by = edited_by
    art.status = "draft"
    art.ready_at = None
    s.flush()


def plant(s: Session, deal: Deal, art: CopyArtifact, provider: ModelProvider) -> FairHousingResult:
    """Demo button: insert the planted violation and show the checker catching it."""
    sep = "\n" if art.channel == "flyer" else " "
    _new_version(s, art, f"{art.text.rstrip()}{sep}{PLANTED}", "planted (demo)")
    record_event(s, actor="presenter", kind="system", entity="copy_artifact", entity_id=art.id,
                 summary=f"Demo: planted a violation in {art.title} (v{art.version})")
    return check(s, deal, art, provider)


def apply_fix(s: Session, deal: Deal, art: CopyArtifact, provider: ModelProvider) -> FairHousingResult:
    res = fh.latest_result(s, "copy_artifact", art.id)
    if res is None or not res.fixed_text or res.version != art.version:
        raise ValueError("There is no fixed version for the current text; run the check first.")
    _new_version(s, art, res.fixed_text, "ai_fix")
    record_event(s, actor="ai", kind="ai_action", entity="copy_artifact", entity_id=art.id,
                 summary=f"AI applied the fair-housing fix to {art.title} (v{art.version})")
    return check(s, deal, art, provider)


def mark_ready(s: Session, deal: Deal, art: CopyArtifact) -> CopyArtifact:
    """The AI marks the artifact "ready to publish" (CP-06). Refused unless the newest fair-housing result is a pass
    on exactly this text; for the MLS remarks, also unless the MLS remarks pre-check has no failure."""
    if art.status == "ready":
        return art
    fh.require_pass(s, "copy_artifact", art.id, art.version, art.text)
    if art.channel == "mls_remarks":
        failed = [c for c in remarks_checks(art.text) if c["status"] == "fail"]
        if failed:
            raise fh.FairHousingBlocked("The MLS pre-check failed: " + "; ".join(c["check"] for c in failed))
    art.status = "ready"
    art.ready_at = now()
    records.mark_law(s, deal.id, "CP-06", reason=f"AI marked {art.title} v{art.version} ready to publish after a "
                                                  "passing fair-housing check",
                     attached_to=f"copy_artifact:{art.id}:v{art.version}")
    s.flush()
    return art


def mark_all_ready(s: Session, deal: Deal) -> tuple[list[CopyArtifact], list[tuple[CopyArtifact, str]]]:
    done, refused = [], []
    for art in artifacts(s, deal):
        try:
            done.append(mark_ready(s, deal, art))
        except fh.FairHousingBlocked as e:
            refused.append((art, str(e)))
    return done, refused


# ---- MLS pre-check (WS3-C1, WS3-R6, WS3-R7) -----------------------------------------------------------------

CONTACT = re.compile(r"(\(?\b\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b|[\w.+-]+@[\w-]+\.\w+|https?://|\bwww\.)", re.I)
COMPENSATION = re.compile(r"\b(commission|compensation|co-?broke|cooperating (fee|broker)|bonus|"
                          r"buyer'?s? (agent|broker) (fee|pays?))\b", re.I)
FREE = re.compile(r"\bfree\b(?![- ]?standing)", re.I)
SHOWING = re.compile(r"\b(lockbox|showing instructions|appointment only|call (the )?(listing )?(agent|office|"
                     r"owner)|text (the )?(agent|owner)|key (is )?(in|under))\b", re.I)


def remarks_checks(text: str) -> list[dict]:
    def row(name, rule, bad, detail_ok, detail_bad):
        return {"check": name, "rule": rule, "status": "fail" if bad else "ok", "detail": detail_bad if bad else detail_ok}

    contact, comp, free, show = CONTACT.search(text), COMPENSATION.search(text), FREE.search(text), SHOWING.search(text)
    return [
        row("No contact details in public remarks", "OneKey Rule 306.3(b) (WS3-C1, R7)", contact,
            "none found", f"found \"{contact.group(0)}\"" if contact else ""),
        row("No compensation in MLS fields", "OneKey Rules 502, 306.3(d) (WS3-R6)", comp,
            "none found", f"found \"{comp.group(0)}\"" if comp else ""),
        row("Not advertised as \"free\"", "OneKey Rule 601.4 (WS3-R6)", free,
            "the word does not appear", f"found \"{free.group(0)}\"" if free else ""),
        row("No showing instructions in public remarks", "OneKey Rule 306.3(b) (WS3-C1)", show,
            "none found", f"found \"{show.group(0)}\"" if show else ""),
        row(f"Length within {MLS_REMARKS_LIMIT:,} characters", "OneKey input limit [INFERENCE: limit assumed]",
            len(text) > MLS_REMARKS_LIMIT, f"{len(text):,} characters", f"{len(text):,} characters"),
    ]


# OneKey input order [INFERENCE: grouped as OneKey's listing-input screens are, with RESO Data Dictionary names].
PACKAGE_FIELDS = [
    ("ListPrice", "List price"), ("PropertyType", "Property type"), ("PropertySubType", "Property sub-type"),
    ("UnparsedAddress", "Address"), ("ParcelNumber", "Parcel ID (tax map)"), ("CountyOrParish", "County"),
    ("Municipality", "Municipality"), ("SchoolDistrict", "School district"), ("BedroomsTotal", "Bedrooms"),
    ("BathroomsFull", "Full baths"), ("BathroomsHalf", "Half baths"), ("LivingArea", "Living area (tax sq ft)"),
    ("BelowGradeFinishedArea", "Finished below grade"), ("LotSizeAcres", "Lot (acres)"), ("YearBuilt", "Year built"),
    ("ArchitecturalStyle", "Style"), ("Heating", "Heating"), ("HeatingFuel", "Heating fuel"), ("Cooling", "Cooling"),
    ("WaterSource", "Water"), ("Sewer", "Sewer"), ("ParkingFeatures", "Parking"), ("TaxAnnualAmount", "Annual taxes"),
    ("AssociationYN", "HOA"), ("FloodZone", "Flood zone"), ("PublicRemarks", "Public remarks"),
    ("ListingAgreement", "Listing agreement on file"), ("ListingExposure", "Listing exposure choice"),
    ("Photos", "Front photo"),
]
REQUIRED = {"ListPrice", "PropertyType", "UnparsedAddress", "ParcelNumber", "BedroomsTotal", "BathroomsFull",
            "LivingArea", "LotSizeAcres", "YearBuilt", "TaxAnnualAmount", "PublicRemarks", "ListingAgreement",
            "ListingExposure", "Photos"}


def mls_package(s: Session, deal: Deal) -> list[dict]:
    facts = {f.field: f.value for f in deal.property.facts}
    p = deal.property
    remarks = next((a for a in artifacts(s, deal) if a.channel == "mls_remarks"), None)
    cp07 = records.latest(s, deal.id, "CP-07")
    values = {
        "ListPrice": f"${deal.list_price:,}" if deal.list_price else None,
        "PropertyType": "Residential", "UnparsedAddress": f"{p.street}, {p.city}, NY {p.zip}",
        "CountyOrParish": p.county, "Municipality": p.municipality,
        "PublicRemarks": (remarks.text if remarks and remarks.status == "ready" else None),
        "ListingAgreement": "Signed (CP-03)" if records.is_done(s, deal.id, "CP-03") else None,
        "ListingExposure": (cp07.reason if cp07 and cp07.status == "done" else None),
        "Photos": None,  # no photos yet: the licensed photographer is a vendor booking; never portal photos (WS3-R8)
    }
    rows = []
    for field, label in PACKAGE_FIELDS:
        v = values[field] if field in values else facts.get(field)
        note = None
        if field == "PublicRemarks" and remarks and remarks.status != "ready":
            note = "waiting: the remarks are not yet marked ready to publish"
        if field == "Photos":
            note = "the photographer is booked in step 4; the MLS needs a front photo before it goes live"
        rows.append({"field": field, "label": label, "value": v, "required": field in REQUIRED,
                     "ok": v is not None and v != "", "note": note})
    return rows


def highlight(text: str, findings: list[dict]) -> Markup:
    """The original text with every located finding wrapped in a <mark> (escaped; model output is untrusted)."""
    spans = sorted((f for f in findings if f.get("start", -1) >= 0), key=lambda f: f["start"])
    out, cursor = [], 0
    for f in spans:
        if f["start"] < cursor:
            continue
        out.append(escape(text[cursor:f["start"]]))
        out.append(Markup('<mark class="fh-{t}" title="{r}: {c}">').format(t=f["tier"], r=f["rule_id"], c=f["cls"]))
        out.append(escape(text[f["start"]:f["end"]]))
        out.append(Markup("</mark>"))
        cursor = f["end"]
    out.append(escape(text[cursor:]))
    return Markup("").join(out)
