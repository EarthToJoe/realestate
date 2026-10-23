"""Output schema for the inbox reply model call (structured output)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class InboxReply(BaseModel):
    reply: str = Field(description="The reply to the prospect, 2 to 6 sentences, plain words, from the fact sheet "
                                   "only; no sign-off (the firm's identity block is added by the software)")
    disclosed: list[str] = Field(description="The known material facts the reply discloses (e.g. oil heat, private "
                                             "septic, no central air), one short phrase each")
