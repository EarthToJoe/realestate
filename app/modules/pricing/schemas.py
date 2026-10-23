"""Output schema for the pricing model call (structured output)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class WeakComp(BaseModel):
    rank: int = Field(description="The comparable's rank number")
    why: str = Field(description="One sentence: why it is a weaker guide to this house")


class PricingAdvice(BaseModel):
    method_plain: str = Field(description="The method in plain words for the seller, 3 to 5 sentences: which "
                                          "sales, what was adjusted and why, how the range was formed")
    weak_comps: list[WeakComp] = Field(description="Comparables that are weaker guides, with the reason")
    recommended_price: int = Field(description="The recommended list price in whole dollars, a round figure")
    reasoning: str = Field(description="Why this price, 3 to 6 sentences: where it sits in the range, what "
                                       "the adjustments leave out (pond, condition, state-route frontage), and "
                                       "the trade-off between price and time on market")
    things_that_would_change_it: list[str] = Field(description="2 to 4 facts that would move the price up or "
                                                               "down if confirmed (e.g. an inspection finding)")
