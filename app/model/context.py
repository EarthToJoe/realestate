"""`AgentContext(side)`: builds the model context for the seller's AI or the buyer's AI (decision 24).

It reads only the side-scoped rows of its own side, so the buyer's confidential limits can never reach a
seller-side call, nor the seller's floor a buyer-side call. People appear only as tokens ([SELLER_1]);
property facts carry no PII and no owner name.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ClientInstructions, Deal, PropertyFact

SIDES = ("seller", "buyer")


class AgentContext:
    def __init__(self, s: Session, deal: Deal, side: str):
        if side not in SIDES:
            raise ValueError(f"side must be one of {SIDES}")
        self.s = s
        self.deal = deal
        self.side = side

    def property_facts(self, fields: list[str] | None = None) -> list[dict]:
        q = select(PropertyFact).where(PropertyFact.property_id == self.deal.property_id)
        facts = self.s.execute(q.order_by(PropertyFact.id)).scalars()
        return [{"field": f.field, "label": f.label, "value": f.value, "source": f.source}
                for f in facts if fields is None or f.field in fields]

    def own_instructions(self) -> dict:
        q = select(ClientInstructions).where(ClientInstructions.deal_id == self.deal.id,
                                             ClientInstructions.side == self.side)
        row = self.s.execute(q).scalar_one_or_none()
        if row is None:
            return {}
        return {"fact_sheet": row.fact_sheet or {}, "authority": row.authority or {},
                "confidential": row.confidential or {}}

    def parties(self) -> dict:
        out = {"client": "[SELLER_1]" if self.side == "seller" else "[BUYER_1]"}
        if self.deal.seller and self.side == "buyer":
            out["other_party"] = "[SELLER_1]"
        if self.deal.buyer and self.side == "seller":
            out["other_party"] = "[BUYER_1]"
        return out

    def build(self, *, facts: list[str] | None = None, instructions: bool = True, extra: dict | None = None) -> dict:
        ctx = {"acting_for": self.side, "parties": self.parties(),
               "property": {"address": f"{self.deal.property.street}, {self.deal.property.city}, NY",
                            "facts": self.property_facts(facts)}}
        if instructions:
            ctx["instructions"] = self.own_instructions()
        if extra:
            ctx.update(extra)
        return ctx
