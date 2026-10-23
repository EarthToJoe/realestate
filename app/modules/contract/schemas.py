"""Output schema for the contract drafting model call (structured output)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Clause(BaseModel):
    number: str = Field(description="The clause number: '1', '2', ... in the body; 'R1', 'R2', ... in the rider")
    heading: str = Field(description="The clause heading, a few words")
    text: str = Field(description="The clause text in plain English, complete and specific to this deal; use the "
                                  "party tokens [SELLER_1] and [BUYER_1], never real names")


class SideBySideRow(BaseModel):
    standard_number: int = Field(description="The standard form's paragraph number, 1 to 28")
    draft_ref: str = Field(description="Where the draft covers it: a clause number such as '6' or 'R2', several "
                                       "separated by commas, or 'none'")
    note: str = Field(description="One line: how the draft differs from the standard form's paragraph, or "
                                  "'Same substance' if it does not")


class ContractDraft(BaseModel):
    title: str = Field(description="The contract's title")
    sections: list[Clause] = Field(description="The contract body, in the standard form's order")
    rider: list[Clause] = Field(description="The rider: the deal-specific terms (contingencies and their "
                                            "deadlines, personal property, disclosures delivered, closing items)")
    side_by_side: list[SideBySideRow] = Field(description="One row for each of the 28 standard paragraphs")
    notes_to_parties: list[str] = Field(description="2 to 4 short notes to both parties about the draft (what to "
                                                    "check, what happens next). Never say a lawyer is unnecessary")
