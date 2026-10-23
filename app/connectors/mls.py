"""`MLSConnector.submit(listing)`. WS3 found no listing-input API for OneKey MLS (WS3-C1), so the POC's
`StubMLS` never submits anything: it returns `HumanRequired` naming who must key the listing and why. A real
connector would replace it only if OneKey ever offers an input API; no screen would change."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.records import catalogue


@dataclass
class HumanRequired:
    reason: str
    who: str
    f_ids: tuple[str, ...]
    l_ids: tuple[str, ...]
    ws3_ids: tuple[str, ...]
    link: str
    tool: str


class MLSConnector(Protocol):
    def submit(self, package: list[dict]) -> HumanRequired: ...


class StubMLS:
    name = "OneKey MLS"

    def submit(self, package: list[dict]) -> HumanRequired:
        e = catalogue.get("CP-08")
        return HumanRequired(reason=e.rule, who=e.who, f_ids=e.f_ids, l_ids=e.l_ids, ws3_ids=e.ws3_ids, link=e.link,
                             tool="Ocusell List or Matrix (OneKey's own input tools; Rules 205, 320)")
