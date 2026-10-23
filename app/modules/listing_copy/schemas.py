"""Output schema for the listing-copy model call (structured output)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class SocialPost(BaseModel):
    platform: Literal["Facebook", "Instagram", "Nextdoor"]
    text: str = Field(description="The post, under 400 characters, no hashtags about people")


class Flyer(BaseModel):
    headline: str = Field(description="Under 60 characters")
    subhead: str = Field(description="One line: town, acreage, beds and baths")
    bullets: list[str] = Field(description="5 to 7 short fact bullets about the property")
    paragraph: str = Field(description="2 or 3 sentences describing the property")


class ListingCopy(BaseModel):
    mls_remarks: str = Field(description="MLS public remarks, under 1,000 characters: the property only; no "
                                         "contact details, showing instructions, compensation or the word free")
    portal_description: str = Field(description="Portal description, 150 to 250 words, the property only")
    social_posts: list[SocialPost] = Field(description="Exactly three posts: Facebook, Instagram, Nextdoor")
    flyer: Flyer
