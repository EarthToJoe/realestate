"""Data model (spec section 4). Every column is marked info={"source": ...} or info={"pii": <category>}.

Slice 1 defined the tables its screens use; slice 2 added pricing_analysis, copy_artifact and
fair_housing_result; slice 3 adds offer and message. The POC rebuilds from the seed, so adding tables needs no migration.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.pii import EncryptedString, pii_column_info


def now() -> datetime:
    return datetime.now(timezone.utc)


SYS = {"source": "system"}


class Property(Base):
    __tablename__ = "property"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    upi: Mapped[str | None] = mapped_column(String(80), info={"source": "public_record"})
    street: Mapped[str] = mapped_column(String(200), info={"source": "seller"})
    city: Mapped[str] = mapped_column(String(100), info={"source": "seller"})
    state: Mapped[str] = mapped_column(String(2), default="NY", info={"source": "seller"})
    zip: Mapped[str | None] = mapped_column(String(10), info={"source": "seller"})
    county: Mapped[str | None] = mapped_column(String(80), info={"source": "public_record"})
    municipality: Mapped[str | None] = mapped_column(String(120), info={"source": "public_record"})
    latitude: Mapped[float | None] = mapped_column(Float, info={"source": "public_record"})
    longitude: Mapped[float | None] = mapped_column(Float, info={"source": "public_record"})
    is_demo_house: Mapped[bool] = mapped_column(Boolean, default=False, info=SYS)
    # No owner name, ever (D18).
    facts: Mapped[list[PropertyFact]] = relationship(back_populates="property", cascade="all, delete-orphan")


class PropertyFact(Base):
    """One fact with where it came from: seller, public_record or inferred."""

    __tablename__ = "property_fact"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    property_id: Mapped[int] = mapped_column(ForeignKey("property.id"), info=SYS)
    field: Mapped[str] = mapped_column(String(80), info=SYS)  # RESO-style name, e.g. BedroomsTotal
    label: Mapped[str] = mapped_column(String(120), info=SYS)
    group: Mapped[str] = mapped_column(String(40), default="Facts", info=SYS)
    value: Mapped[str | None] = mapped_column(Text, info={"source": "fact"})
    source: Mapped[str] = mapped_column(String(20), info=SYS)  # seller | public_record | inferred | gap
    source_ref: Mapped[str | None] = mapped_column(Text, info=SYS)
    confidence: Mapped[str | None] = mapped_column(String(20), info=SYS)  # high | medium | low
    inferred_reason: Mapped[str | None] = mapped_column(Text, info=SYS)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, info=SYS)
    property: Mapped[Property] = relationship(back_populates="facts")


class Person(Base):
    """Fictional people only. PII columns are Fernet-encrypted. No broker or attorney persons (decision 21)."""

    __tablename__ = "person"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    role: Mapped[str] = mapped_column(String(20), info=SYS)  # seller | buyer | other-agent | third-party
    persona_label: Mapped[str] = mapped_column(String(60), info=SYS)  # e.g. "Seller (demo persona)"
    token: Mapped[str] = mapped_column(String(20), info=SYS)  # SELLER_1, BUYER_1: what the model sees
    legal_name: Mapped[str | None] = mapped_column(EncryptedString(500), info=pii_column_info("name"))
    email: Mapped[str | None] = mapped_column(EncryptedString(500), info=pii_column_info("contact"))
    phone: Mapped[str | None] = mapped_column(EncryptedString(500), info=pii_column_info("contact"))
    mailing_address: Mapped[str | None] = mapped_column(EncryptedString(800), info=pii_column_info("address"))
    preapproval_amount: Mapped[str | None] = mapped_column(EncryptedString(200), info=pii_column_info("financial"))
    lender: Mapped[str | None] = mapped_column(EncryptedString(300), info=pii_column_info("financial"))
    erased_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), info=SYS)


class Deal(Base):
    __tablename__ = "deal"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    property_id: Mapped[int] = mapped_column(ForeignKey("property.id"), info=SYS)
    seller_id: Mapped[int | None] = mapped_column(ForeignKey("person.id"), info=SYS)
    buyer_id: Mapped[int | None] = mapped_column(ForeignKey("person.id"), info=SYS)
    side: Mapped[str] = mapped_column(String(10), default="listing", info=SYS)
    status: Mapped[str] = mapped_column(String(30), default="intake", info=SYS)
    current_step: Mapped[int] = mapped_column(Integer, default=1, info=SYS)
    list_price: Mapped[int | None] = mapped_column(Integer, info=SYS)
    brokerage_id: Mapped[str] = mapped_column(String(40), default="default", info=SYS)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, info=SYS)
    property: Mapped[Property] = relationship()
    seller: Mapped[Person | None] = relationship(foreign_keys=[seller_id])
    buyer: Mapped[Person | None] = relationship(foreign_keys=[buyer_id])


class ClientInstructions(Base):
    """Side-scoped: AgentContext(side) reads only its own side's rows (decision 24)."""

    __tablename__ = "client_instructions"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    deal_id: Mapped[int] = mapped_column(ForeignKey("deal.id"), info=SYS)
    side: Mapped[str] = mapped_column(String(10), info=SYS)  # seller | buyer
    fact_sheet: Mapped[dict | None] = mapped_column(JSON, info={"source": "seller"})
    authority: Mapped[dict | None] = mapped_column(JSON, info={"source": "client"})
    confidential: Mapped[dict | None] = mapped_column(JSON, info={"source": "client", "confidential": True})
    approved: Mapped[bool] = mapped_column(Boolean, default=False, info=SYS)


class Checkpoint(Base):
    """The one record type. The timeline, hurdle map and agent-acts log read only this table and the steps."""

    __tablename__ = "checkpoint"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    deal_id: Mapped[int] = mapped_column(ForeignKey("deal.id"), info=SYS)
    code: Mapped[str] = mapped_column(String(8), info=SYS)
    step: Mapped[int] = mapped_column(Integer, info=SYS)
    kind: Mapped[str] = mapped_column(String(20), info=SYS)
    title: Mapped[str] = mapped_column(String(200), info=SYS)
    actor: Mapped[str] = mapped_column(String(20), info=SYS)
    law_actor: Mapped[str | None] = mapped_column(String(4), info=SYS)
    side: Mapped[str] = mapped_column(String(10), info=SYS)
    rule_text: Mapped[str] = mapped_column(Text, info=SYS)
    who_text: Mapped[str] = mapped_column(Text, info=SYS)
    reason: Mapped[str | None] = mapped_column(Text, info=SYS)  # what happened, in plain words
    f_ids: Mapped[list] = mapped_column(JSON, default=list, info=SYS)
    l_ids: Mapped[list] = mapped_column(JSON, default=list, info=SYS)
    ws3_ids: Mapped[list] = mapped_column(JSON, default=list, info=SYS)
    research_link: Mapped[str | None] = mapped_column(String(300), info=SYS)
    blocking: Mapped[bool] = mapped_column(Boolean, default=False, info=SYS)
    status: Mapped[str] = mapped_column(String(12), info=SYS)  # pending | done | declined | simulated | planned
    decision: Mapped[str | None] = mapped_column(String(40), info=SYS)
    decided_by: Mapped[str | None] = mapped_column(String(20), info=SYS)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), info=SYS)
    attached_to: Mapped[str | None] = mapped_column(String(80), info=SYS)  # e.g. "disclosure:3"
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, info=SYS)


class Disclosure(Base):
    __tablename__ = "disclosure"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    deal_id: Mapped[int] = mapped_column(ForeignKey("deal.id"), info=SYS)
    person_id: Mapped[int | None] = mapped_column(ForeignKey("person.id"), info=SYS)
    kind: Mapped[str] = mapped_column(String(30), info=SYS)  # agency | fair_housing | not_legal_services | pcds ...
    title: Mapped[str] = mapped_column(String(200), info=SYS)
    l_id: Mapped[str] = mapped_column(String(10), info=SYS)
    trigger: Mapped[str] = mapped_column(String(120), info=SYS)
    required: Mapped[bool] = mapped_column(Boolean, default=True, info=SYS)
    required_reason: Mapped[str | None] = mapped_column(Text, info=SYS)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), info=SYS)
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), info=SYS)
    answers: Mapped[dict | None] = mapped_column(JSON, info={"source": "seller"})  # PCDS: the seller's own answers


class Document(Base):
    __tablename__ = "document"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    deal_id: Mapped[int] = mapped_column(ForeignKey("deal.id"), info=SYS)
    kind: Mapped[str] = mapped_column(String(40), info=SYS)
    version: Mapped[int] = mapped_column(Integer, default=1, info=SYS)
    body_html: Mapped[str | None] = mapped_column(Text, info=SYS)  # no PII: names are inserted at render time
    generated_by: Mapped[str] = mapped_column(String(20), default="ai", info=SYS)
    needs_wet_ink: Mapped[bool] = mapped_column(Boolean, default=False, info=SYS)
    needs_notary: Mapped[bool] = mapped_column(Boolean, default=False, info=SYS)
    signed_by: Mapped[dict | None] = mapped_column(JSON, info=SYS)
    label_version: Mapped[str | None] = mapped_column(String(20), info=SYS)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, info=SYS)


class Event(Base):
    """Append-only audit log with a hash chain (SQLite triggers forbid UPDATE and DELETE)."""

    __tablename__ = "events"
    seq: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, info=SYS)
    actor: Mapped[str] = mapped_column(String(20), info=SYS)
    kind: Mapped[str] = mapped_column(String(20), info=SYS)  # ai_action | client_decision | system
    entity: Mapped[str] = mapped_column(String(40), info=SYS)
    entity_id: Mapped[str | None] = mapped_column(String(40), info=SYS)
    summary: Mapped[str] = mapped_column(Text, info=SYS)  # masked: never holds PII
    prev_hash: Mapped[str] = mapped_column(String(64), info=SYS)
    hash: Mapped[str] = mapped_column(String(64), info=SYS)


class AccessLog(Base):
    __tablename__ = "access_log"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, info=SYS)
    persona: Mapped[str] = mapped_column(String(20), info=SYS)
    person_id: Mapped[int] = mapped_column(Integer, info=SYS)
    fields: Mapped[list] = mapped_column(JSON, info=SYS)
    purpose: Mapped[str] = mapped_column(String(200), info=SYS)
    route: Mapped[str] = mapped_column(String(200), info=SYS)


class ModelCall(Base):
    """Spend log. No prompt or response bodies here."""

    __tablename__ = "model_call"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, info=SYS)
    module: Mapped[str] = mapped_column(String(40), info=SYS)
    task: Mapped[str] = mapped_column(String(60), info=SYS)
    side: Mapped[str | None] = mapped_column(String(10), info=SYS)
    model: Mapped[str] = mapped_column(String(60), info=SYS)
    input_tokens: Mapped[int] = mapped_column(Integer, default=0, info=SYS)
    cache_write_tokens: Mapped[int] = mapped_column(Integer, default=0, info=SYS)
    cache_read_tokens: Mapped[int] = mapped_column(Integer, default=0, info=SYS)
    output_tokens: Mapped[int] = mapped_column(Integer, default=0, info=SYS)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0, info=SYS)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0, info=SYS)
    mode: Mapped[str] = mapped_column(String(10), info=SYS)  # live | replay | fake
    prompt_version: Mapped[str] = mapped_column(String(40), info=SYS)
    request_hash: Mapped[str] = mapped_column(String(64), info=SYS)


class PricingAnalysis(Base):
    """Step 2: the comparables with code-computed adjustments, the range and the AI's advice. No PII."""

    __tablename__ = "pricing_analysis"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    deal_id: Mapped[int] = mapped_column(ForeignKey("deal.id"), info=SYS)
    comps: Mapped[list] = mapped_column(JSON, info={"source": "public_record"})  # with adjustments (code)
    summary: Mapped[dict] = mapped_column(JSON, info=SYS)  # range, indicated value, rates used
    advice: Mapped[dict | None] = mapped_column(JSON, info={"source": "ai"})  # the model's structured output
    mode: Mapped[str | None] = mapped_column(String(10), info=SYS)
    model: Mapped[str | None] = mapped_column(String(60), info=SYS)
    recorded_at: Mapped[str | None] = mapped_column(String(40), info=SYS)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, info=SYS)


class CopyArtifact(Base):
    """Step 3 (and step 10): one piece of advertising copy. Each edit is a new version of the text; a version
    can be marked "ready to publish" only with a passing fair-housing result for that exact text (spec 5)."""

    __tablename__ = "copy_artifact"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    deal_id: Mapped[int] = mapped_column(ForeignKey("deal.id"), info=SYS)
    channel: Mapped[str] = mapped_column(String(30), info=SYS)  # mls_remarks | portal | social_1..3 | flyer
    title: Mapped[str] = mapped_column(String(120), info=SYS)
    text: Mapped[str] = mapped_column(Text, info={"source": "ai"})
    extra: Mapped[dict | None] = mapped_column(JSON, info={"source": "ai"})  # flyer headline, bullets; platform
    version: Mapped[int] = mapped_column(Integer, default=1, info=SYS)
    status: Mapped[str] = mapped_column(String(20), default="draft", info=SYS)  # draft | blocked | passed | ready
    edited_by: Mapped[str] = mapped_column(String(30), default="ai", info=SYS)  # ai | planted (demo) | ai_fix
    ready_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), info=SYS)
    mode: Mapped[str | None] = mapped_column(String(10), info=SYS)
    model: Mapped[str | None] = mapped_column(String(60), info=SYS)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, info=SYS)


class FairHousingResult(Base):
    """One run of the fair-housing pipeline on one exact text. Kept for the complaint window (L61)."""

    __tablename__ = "fair_housing_result"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    deal_id: Mapped[int | None] = mapped_column(ForeignKey("deal.id"), info=SYS)
    entity: Mapped[str] = mapped_column(String(30), info=SYS)  # copy_artifact | message | campaign
    entity_id: Mapped[int] = mapped_column(Integer, info=SYS)
    version: Mapped[int] = mapped_column(Integer, info=SYS)
    text_hash: Mapped[str] = mapped_column(String(64), info=SYS)
    findings: Mapped[list] = mapped_column(JSON, default=list, info=SYS)
    fixed_text: Mapped[str | None] = mapped_column(Text, info={"source": "ai"})
    passed: Mapped[bool] = mapped_column(Boolean, info=SYS)  # True = no block finding
    rules_version: Mapped[str] = mapped_column(String(40), info=SYS)
    model_mode: Mapped[str | None] = mapped_column(String(10), info=SYS)
    model: Mapped[str | None] = mapped_column(String(60), info=SYS)
    model_error: Mapped[str | None] = mapped_column(Text, info=SYS)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, info=SYS)


class Message(Base):
    """Step 5 (and later 6 and 8): one simulated message in the shared inbox. An outgoing message carries the firm's
    identity block and is sent only with a passing fair-housing result for its exact text; a held one never left.
    Prospects are labelled roles ("Prospect A (simulated)"), never real names."""

    __tablename__ = "message"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    deal_id: Mapped[int] = mapped_column(ForeignKey("deal.id"), info=SYS)
    side: Mapped[str] = mapped_column(String(10), default="seller", info=SYS)
    thread: Mapped[str] = mapped_column(String(40), info=SYS)
    direction: Mapped[str] = mapped_column(String(4), info=SYS)  # in | out
    party: Mapped[str] = mapped_column(String(80), info=SYS)
    topic: Mapped[str | None] = mapped_column(String(30), info=SYS)
    body: Mapped[str] = mapped_column(Text, info={"source": "ai"})
    status: Mapped[str] = mapped_column(String(20), default="received", info=SYS)  # received|sent|held|to_seller|answered
    extra: Mapped[dict | None] = mapped_column(JSON, info={"source": "ai"})
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, info=SYS)


class OfferState(Base):
    """Step 6: the offers' advice, the seller's decision (CP-12) and the negotiation thread, one row per deal.
    No PII: parties are labelled roles."""

    __tablename__ = "offer_state"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    deal_id: Mapped[int] = mapped_column(ForeignKey("deal.id"), info=SYS)
    state: Mapped[dict | None] = mapped_column(JSON, info={"source": "ai"})


class BuyerState(Base):
    """Step 8: the buyer's side of the deal, one row per deal: the buyer's needs (non-confidential search
    criteria), search results and alerts, the tour, the buyer's AI's advice and drafts, and the replies the buyer
    approved. Side-scoped (decision 24): only the buyer's AI and the buyer's screens read it. The buyer's maximum
    price lives in `client_instructions` (side buyer, confidential), never here."""

    __tablename__ = "buyer_state"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    deal_id: Mapped[int] = mapped_column(ForeignKey("deal.id"), info=SYS)
    state: Mapped[dict | None] = mapped_column(JSON, info={"source": "buyer"})


class ContractState(Base):
    """Step 7: the accepted-offer memorandum, the AI's contract draft and rider (with party tokens, never names),
    the code checks on it, the disclosures attached and the signing state, one row per deal."""

    __tablename__ = "contract_state"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    deal_id: Mapped[int] = mapped_column(ForeignKey("deal.id"), info=SYS)
    state: Mapped[dict | None] = mapped_column(JSON, info={"source": "ai"})


class BrandState(Base):
    """Step 10: the firm's own campaign beyond its three pieces of copy (which are `copy_artifact` rows): the ad
    targeting the AI chose, refused targeting attempts, and the simulated publication, one row per deal. No PII."""

    __tablename__ = "brand_state"
    id: Mapped[int] = mapped_column(primary_key=True, info=SYS)
    deal_id: Mapped[int] = mapped_column(ForeignKey("deal.id"), info=SYS)
    state: Mapped[dict | None] = mapped_column(JSON, info={"source": "ai"})


# Replays are not a table: they are JSON files under replays/ (committed, masked, no PII), so a recorded run
# survives the demo reset and ships with the image. See app/model/provider.py.
