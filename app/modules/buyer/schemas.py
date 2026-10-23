"""Output schemas for the buyer's AI (structured output). The buyer's AI is a separate context (decision 24)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AlertNote(BaseModel):
    id: str = Field(description="The listing's id")
    why: str = Field(description="One sentence: how the listing meets the buyer's stated needs, facts only")


class BuyerAlert(BaseModel):
    message: str = Field(description="The alert message to the buyer, 2 to 4 sentences, plain words, facts only; "
                                     "no sign-off (the software adds the firm's identity block)")
    notes: list[AlertNote] = Field(description="One note per matching listing")


class BuyerOfferAdvice(BaseModel):
    advice: str = Field(description="4 to 6 sentences to the buyer: what to offer and why (list price, the public "
                                    "sales, days on the market, the house's known facts), the terms, and the "
                                    "risks. The buyer decides.")
    recommended_price: int = Field(description="The recommended offer price, round dollars")
    walk_away_note: str = Field(description="One sentence on how far the buyer could go later, in relation to the "
                                            "buyer's own maximum, without stating any number to anyone else")
    deposit_pct: int = Field(description="Deposit as a percentage of the price, usually 10")
    financing: str = Field(description="Financing in a few words, e.g. 'Conventional mortgage, 20% down; "
                                       "pre-approval attached'")
    mortgage_days: int = Field(description="Mortgage-commitment period in days")
    inspection_days: int = Field(description="Home-inspection period in days")
    closing_days: int = Field(description="Closing, in days from signing")
    contingencies: list[str] = Field(description="Contingencies to include, e.g. mortgage commitment, home "
                                                 "inspection, well and septic tests")
    requests: list[str] = Field(description="Requests of the seller, if any (items to stay); may be empty")
    risks: list[str] = Field(description="1 to 3 risks for the buyer")


class BuyerCounterAdvice(BaseModel):
    advice: str = Field(description="3 to 5 sentences to the buyer on the seller's counter: what it means, what to "
                                    "reply and why. The buyer decides.")
    action: str = Field(description="accept, counter or walk_away")
    price: int = Field(description="The reply price (the counter's price if accepting), round dollars")
    closing_days: int = Field(description="Closing in days from signing for the reply")
    inspection_days: int = Field(description="Inspection period in days for the reply")
    mortgage_days: int = Field(description="Mortgage-commitment period in days for the reply")
    requests: list[str] = Field(description="Requests kept in the reply; may be empty")
