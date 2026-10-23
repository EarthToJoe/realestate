"""Output schema for the firm's campaign (step 10, structured output)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class LandingPage(BaseModel):
    headline: str = Field(description="Under 70 characters")
    body: list[str] = Field(description="2 or 3 short paragraphs, 120 to 200 words in all, for home sellers")
    call_to_action: str = Field(description="One line inviting the seller to start, under 60 characters")


class LocalAd(BaseModel):
    headline: str = Field(description="Under 40 characters")
    text: str = Field(description="The ad's primary text, under 150 characters")


class LeadMagnet(BaseModel):
    title: str = Field(description="The guide's title, under 70 characters")
    pitch: str = Field(description="One or two sentences on what the seller gets, under 280 characters")
    outline: list[str] = Field(description="4 to 6 short lines: what the guide covers")


class Campaign(BaseModel):
    landing_page: LandingPage
    local_ad: LocalAd
    lead_magnet: LeadMagnet
    targeting_reason: str = Field(description="One or two sentences: why the ad reaches people by place only, "
                                              "within the radius given, and never by who they are")
