"""Output schema for the fair-housing model review pass (structured output)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ModelFinding(BaseModel):
    phrase: str = Field(description="The exact words from the text that raise the issue, copied verbatim")
    protected_class: str = Field(description="The protected class or conduct, e.g. 'familial status', 'creed', "
                                             "'steering (school quality)'")
    rule_id: str = Field(description="The closest rule ID from the rules list, or 'MODEL' if none fits")
    tier: Literal["block", "warn"]
    explanation: str = Field(description="One plain sentence: why this states a preference, limitation or "
                                         "discrimination, or steers")
    suggestion: str = Field(description="A neutral rewrite of the phrase that keeps the meaning about the house")


class FairHousingReview(BaseModel):
    findings: list[ModelFinding] = Field(description="Every issue found, including any the rules list already "
                                                     "names; empty if the text is clean")
    fixed_text: str = Field(description="The whole text rewritten so that no finding remains, keeping every fact "
                                        "about the property; identical to the input if there are no findings")
