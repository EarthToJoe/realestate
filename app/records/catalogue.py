"""Loads app/records/catalogue.yaml, the one file holding every record's text."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import yaml

PATH = Path(__file__).with_name("catalogue.yaml")

KINDS = ("client_decision", "law_marker", "human_required", "third_party", "automated")
# On-screen names and colours (timeline chips and components).
KIND_LABEL = {
    "client_decision": "Your decision",
    "law_marker": "NY law today",
    "human_required": "Human required",
    "third_party": "Third party",
    "automated": "AI did it",
}
LAW_ACTOR_LABEL = {"L": "licensed broker", "A": "lawyer", "L+A": "licensed broker and lawyer"}


@dataclass(frozen=True)
class Entry:
    code: str
    title: str
    kind: str
    step: int
    actor: str
    side: str
    rule: str
    who: str
    link: str
    f_ids: tuple[str, ...] = ()
    l_ids: tuple[str, ...] = ()
    ws3_ids: tuple[str, ...] = ()
    law_actor: str | None = None
    choices: tuple[str, ...] = ()
    blocks: str | None = None
    per_item: bool = False
    planned: bool = False
    standing: bool = False
    extra: dict = field(default_factory=dict)

    @property
    def blocking(self) -> bool:
        return self.kind == "client_decision"


@lru_cache(maxsize=1)
def load(path: Path = PATH) -> dict[str, Entry]:
    raw = yaml.safe_load(path.read_text())
    links = raw.get("links", {})
    out: dict[str, Entry] = {}
    for code, e in raw["records"].items():
        if e["kind"] not in KINDS:
            raise ValueError(f"{code}: unknown kind {e['kind']}")
        out[code] = Entry(
            code=code,
            title=e["title"],
            kind=e["kind"],
            step=int(e["step"]),
            actor=e["actor"],
            side=e.get("side", "seller"),
            rule=e.get("rule", ""),
            who=e.get("who", ""),
            link=links.get(e.get("link", ""), e.get("link", "")),
            f_ids=tuple(e.get("f_ids") or ()),
            l_ids=tuple(e.get("l_ids") or ()),
            ws3_ids=tuple(e.get("ws3_ids") or ()),
            law_actor=e.get("law_actor"),
            choices=tuple(e.get("choices") or ()),
            blocks=e.get("blocks"),
            per_item=bool(e.get("per_item", False)),
            planned=bool(e.get("planned", False)),
            standing=bool(e.get("standing", False)),
        )
    return out


def get(code: str) -> Entry:
    return load()[code]
