"""Output schema for the intake model call (structured output)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Inference(BaseModel):
    field: str = Field(description="Short field name, e.g. HeatingFuelTank, TaxEstimate, Accessibility")
    label: str = Field(description="Plain-words label shown on screen")
    value: str = Field(description="The inferred value, stated as a likelihood, never as a confirmed fact")
    reason: str = Field(description="One sentence: which recorded facts this is inferred from")
    confidence: Literal["low", "medium", "high"]


class IntakeInference(BaseModel):
    inferences: list[Inference] = Field(description="3 to 6 inferences that fill gaps in the record")
    questions_for_seller: list[str] = Field(description="2 to 4 short questions the seller should confirm")
    summary: str = Field(description="Two or three plain sentences: what the record shows, what was inferred, "
                                     "what the seller must confirm")
