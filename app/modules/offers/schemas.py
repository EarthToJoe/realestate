"""Output schema for the offer advice model call (structured output)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class OfferView(BaseModel):
    label: str = Field(description="The offer's label, A or B")
    summary: str = Field(description="One or two sentences presenting the offer in plain words")
    risks: list[str] = Field(description="1 to 3 risks: contingencies, financing, dates")
    advice: str = Field(description="One or two sentences: what the AI advises on this offer and why")


class OfferAdvice(BaseModel):
    offers: list[OfferView] = Field(description="Every offer, presented; none left out")
    recommendation: str = Field(description="3 to 5 sentences: which offer to work with and whether to accept, "
                                            "counter or reject, with the reasoning (price, net, contingencies, "
                                            "dates, risk). The seller decides.")
    suggested_counter_price: int = Field(description="If countering, the counter price the AI suggests, round dollars")
    suggested_lowest_price: int = Field(description="If countering, the lowest price the AI suggests the seller let "
                                                    "it agree without coming back, round dollars")
