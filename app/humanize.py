"""What the screens show people instead of raw data (UI audit 2026-10-23): Eastern times, Yes/No, labels for keys,
decisions in words. Display only; the records keep their stored values."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

EASTERN = ZoneInfo("America/New_York")
DAYS = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday",
        "Sat": "Saturday", "Sun": "Sunday"}


def _as_datetime(v) -> datetime | None:
    if isinstance(v, datetime):
        return v
    if isinstance(v, str) and v:
        s = v.strip()
        if s.endswith(" UTC"):
            s = s[:-4]
        try:
            return datetime.fromisoformat(s)
        except ValueError:
            return None
    return None


def et(v, fmt: str = "full") -> str:
    """A stored time (UTC, aware or naive as SQLite returns it, or an ISO string) in New York time."""
    d = _as_datetime(v)
    if d is None:
        return str(v or "")
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    d = d.astimezone(EASTERN)
    clock = d.strftime("%I:%M %p").lstrip("0").lower()
    if fmt == "time":
        return f"{clock} ET"
    if fmt == "date":
        return d.strftime("%a %d %b %Y").replace(" 0", " ")
    return f"{d.strftime('%a %d %b').replace(' 0', ' ')}, {clock} ET"


def hour(h: int) -> str:
    h = int(h)
    return "noon" if h == 12 else ("midnight" if h in (0, 24) else (f"{h} am" if h < 12 else f"{h - 12} pm"))


def yesno(v) -> str:
    if isinstance(v, bool):
        return "Yes" if v else "No"
    if isinstance(v, str) and v.lower() in ("true", "false", "yes", "no"):
        return "Yes" if v.lower() in ("true", "yes") else "No"
    return "" if v is None else str(v)


AUTHORITY_LABELS = {
    "answer_from_fact_sheet": "Questions",
    "showing_windows": "Showing hours",
    "showing_kinds": "Kinds of showing",
    "price": "Price",
    "send_without_review": "Replies",
    "self_guided_tours": "Self-guided tours allowed",
}


def authority_value(key: str, v) -> str:
    if isinstance(v, dict):
        return "; ".join(f"{DAYS.get(d, d)} {hour(h[0])} to {hour(h[1])}" for d, h in v.items())
    return yesno(v)


DECISION_WORDS = {
    "acknowledge": "acknowledged", "refuse_with_declaration": "refused, with a signed declaration",
    "sign": "signed", "decline": "declined", "consent": "consented", "approve": "approved", "choose": "chosen",
    "complete": "completed", "counter": "countered", "accept": "accepted", "reject": "rejected", "allow": "allowed",
}
ROLE = {"seller": "the seller", "buyer": "the buyer", "presenter": "the presenter", "ai": "the AI",
        "seller_and_buyer": "the seller and the buyer"}


def whose(actor: str) -> str:
    return {"seller": "The seller's decision", "buyer": "The buyer's decision",
            "seller_and_buyer": "The seller's and the buyer's decision"}.get(actor, "A client's decision")


def decision_label(cp) -> str:
    """'done: buyer=consent,seller=consent' becomes 'Both consented'; 'pending' becomes 'Waiting for the seller'."""
    raw = (cp.decision or "").strip()
    if cp.status == "pending":
        if cp.actor == "seller_and_buyer" and "=" in raw:
            got = dict(p.split("=", 1) for p in raw.split(",") if "=" in p)
            done = [f"{ROLE[k].capitalize()} {DECISION_WORDS.get(v, v)}" for k, v in got.items() if k in ROLE]
            left = [ROLE[k] for k in ("seller", "buyer") if k not in got]
            return "; ".join(done + [f"waiting for {' and '.join(left)}"]) if left else "; ".join(done)
        return f"Waiting for {ROLE.get(cp.actor, 'a client')}"
    if cp.status != "done":
        return cp.status.capitalize()
    if "=" in raw:
        got = dict(p.split("=", 1) for p in raw.split(",") if "=" in p)
        vals = set(got.values())
        if len(got) == 2 and len(vals) == 1:
            return f"Both {DECISION_WORDS.get(vals.pop(), 'decided')}"
        return "; ".join(f"{ROLE.get(k, k).capitalize()} {DECISION_WORDS.get(v, v)}" for k, v in got.items())
    if raw:
        return DECISION_WORDS.get(raw, raw.replace("_", " ")).capitalize()
    return "Done"


def slot(v: str) -> str:
    """'Sun at 14:00' (a showing slot as the services write it) becomes 'Sunday at 2 pm'."""
    m = re.fullmatch(r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun) at (\d{1,2}):00", (v or "").strip())
    return f"{DAYS[m.group(1)]} at {hour(int(m.group(2)))}" if m else (v or "")


# ---- the audience layer: no record codes, research IDs or repeated "(simulated)" (decision 50) ---------------------

_CODE_PAREN = re.compile(r"\s*\((?:(?:L|F)\d+[a-z]?|WS\d-[A-Z]\d+|CP-\d+)(?:[,;] ?(?:(?:L|F)\d+[a-z]?|WS\d-[A-Z]\d+|CP-\d+))*\)")
_CODE_NAMED = re.compile(r"\bCP-\d+ \(([^)]*)\)")
_CODE_BARE = re.compile(r"\s*\b(?:CP-\d+|WS\d-[A-Z]\d+)\b")


def plain(text) -> str:
    """Display only: drops research IDs and record codes in brackets, "(stub)" and "(simulated)" (said once per
    screen instead), and names the firm's buyer as the buyer. Records keep their stored words."""
    if text is None:
        return ""
    t = str(text)
    t = _CODE_NAMED.sub(lambda m: m.group(1)[:1].lower() + m.group(1)[1:], t)
    t = _CODE_PAREN.sub("", t)
    t = re.sub(r"\s*\((?:simulated|stub)\)", "", t)
    t = re.sub(r"\bBuyer 1's\b", "the buyer's", t)
    t = re.sub(r"\bBuyer 1\b", "the buyer", t)
    return t


def gate_message(text: str) -> str:
    """A service refusal in plain words: the record codes and the rule's citation go; what is missing stays."""
    t = plain(text or "")
    t = t.split(" Why: ")[0]
    t = _CODE_BARE.sub("", t)
    return t.strip()
