"""Model output is untrusted input for HTML and PDF (spec section 2): strip every tag with nh3."""

from __future__ import annotations

import nh3
from pydantic import BaseModel


def clean(text: str | None) -> str:
    return nh3.clean(text or "", tags=set())


def clean_model(obj: BaseModel) -> BaseModel:
    """Return a copy of a structured output with every string field sanitised (recursively)."""

    def walk(v):
        if isinstance(v, str):
            return clean(v)
        if isinstance(v, list):
            return [walk(x) for x in v]
        if isinstance(v, dict):
            return {k: walk(x) for k, x in v.items()}
        return v

    return type(obj).model_validate(walk(obj.model_dump()))
