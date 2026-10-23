"""The Property Condition Disclosure Statement (CP-04, L43): the full current form, version-pinned.

The form's text lives in `pcds_2025.yaml` (RPL §462(2), effective 2025-07-01, 56 questions). The seller completes
it; the software never pre-fills an answer (RPL §466; the agent informs, does not fill in). Every field starts blank.
The demonstration seller may submit the answers they prepared in `seed/personas.yaml` (fictional answers, labelled
on the form and in the PDF), which is the seller's own act, enabled only for the seller persona (decision 34).

Answer keys: `q<n>` for a one-part question, `q<n>_<part>` for each part, `q<n>_explain` for its explanation, and
`explanation` for the free area at the end. A question needs an explanation when an answer matches its
`explain_if`.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Deal, Disclosure, now
from app.records import service as records

FORM_PATH = Path(__file__).with_name("pcds_2025.yaml")
CHOICES = {"ynun": ["yes", "no", "unkn", "na"], "ynu": ["yes", "no", "unkn"]}
CHOICE_LABELS = {"yes": "Yes", "no": "No", "unkn": "Unkn", "na": "NA"}
DEMO_NOTE = ("DEMONSTRATION: answers prepared by the fictional demo seller (seed/personas.yaml); they are not "
             "statements about the real house at this address.")


@lru_cache
def form() -> dict:
    return yaml.safe_load(FORM_PATH.read_text())


def questions() -> list[dict]:
    return [q for sec in form()["sections"] for q in sec["questions"]]


def fields(q: dict) -> list[dict]:
    """The answer fields of one question: [{key, type, label, options, explain_if}]."""
    n = q["n"]
    if q.get("type") == "parts":
        out = []
    else:
        out = [{"key": f"q{n}", "type": q["type"], "label": None, "explain_if": q.get("explain_if"),
                "options": CHOICES.get(q["type"])}]
    for p in q.get("parts", []):
        out.append({"key": f"q{n}_{p['key']}", "type": p["type"], "label": p["label"],
                    "explain_if": p.get("explain_if"), "options": p.get("options") or CHOICES.get(p["type"]),
                    "asked_if": p.get("asked_if")})
    return out


def asked(f: dict, answers: dict) -> bool:
    """A part the form asks only "if yes", "if municipal" or "if septic or cesspool"."""
    for key, values in (f.get("asked_if") or {}).items():
        given = [x.strip().lower() for x in (answers.get(key) or "").split(",")]
        if not any(str(v).lower() in given for v in values):
            return False
    return True


def all_keys() -> list[str]:
    keys = []
    for q in questions():
        keys += [f["key"] for f in fields(q)] + [f"q{q['n']}_explain"]
    return keys + ["explanation"]


def needs_explanation(q: dict, answers: dict) -> bool:
    return any(f["explain_if"] and asked(f, answers) and (answers.get(f["key"]) or "").lower() == f["explain_if"]
               for f in fields(q))


def validate(answers: dict) -> list[str]:
    """Every field needs the seller's own answer; "UNKN" is allowed. A matching `explain_if` needs words."""
    errors = []
    for q in questions():
        n = q["n"]
        for f in fields(q):
            v = (answers.get(f["key"]) or "").strip()
            if not asked(f, answers):
                continue
            if not v:
                errors.append(f"Question {n}{' (' + f['label'] + ')' if f['label'] else ''} needs your answer.")
            elif f["type"] == "multi":
                if any(x.strip() not in f["options"] for x in v.split(",")):
                    errors.append(f"Question {n}: circle from {', '.join(f['options'])}.")
            elif f["options"] and v.lower() not in f["options"]:
                errors.append(f"Question {n}: choose one of {', '.join(CHOICE_LABELS[o] for o in f['options'])}.")
        if needs_explanation(q, answers) and not (answers.get(f"q{n}_explain") or "").strip():
            errors.append(f"Question {n}: the form asks you to explain this answer.")
    return errors


def disclosure(s: Session, deal: Deal) -> Disclosure:
    return s.execute(select(Disclosure).where(Disclosure.deal_id == deal.id, Disclosure.kind == "pcds")).scalar_one()


def prepared_answers() -> dict:
    """The fictional demo seller's own prepared answers (seed/personas.yaml)."""
    from app.modules.intake.service import load_personas

    return {k: str(v) for k, v in load_personas()["seller"]["pcds_answers"].items()}


def submit(s: Session, deal: Deal, persona: str, answers: dict, *, prepared: bool = False):
    """CP-04: the seller's own decision. Records the seller's answers and the form version; delivery to the buyer
    happens with the contract (CP-32)."""
    cp = records.latest(s, deal.id, "CP-04")
    if cp is None:
        raise ValueError("The PCDS is not open for this deal.")
    clean = {k: str(answers.get(k, "")).strip() for k in all_keys()}
    errors = validate(clean)
    if errors:
        raise ValueError(" ".join(errors[:6]) + (f" ({len(errors) - 6} more.)" if len(errors) > 6 else ""))
    records.decide(s, cp, persona=persona, decision="complete",
                   reason=f"Completed and signed by the seller on the {form()['version']} form "
                          f"({len(questions())} questions)" + ("; the demo seller's prepared answers" if prepared
                                                               else ""))
    d = disclosure(s, deal)
    d.answers = {**{k: v for k, v in clean.items() if v}, "_form_version": form()["version"],
                 "_prepared_demo": prepared, "_signed_at": now().isoformat()}
    d.title = f"Property Condition Disclosure Statement (RPL §462, {form()['version']} form)"
    d.acknowledged_at = now()
    s.flush()
    return cp


def answers_of(s: Session, deal: Deal) -> dict:
    return dict(disclosure(s, deal).answers or {})


def answer_label(v: str) -> str:
    return CHOICE_LABELS.get((v or "").lower(), v or "")


def summary(answers: dict) -> list[str]:
    """Known material facts the seller disclosed (yes answers and their explanations), for the contract step."""
    out = []
    for q in questions():
        for f in fields(q):
            if (answers.get(f["key"]) or "").lower() == "yes":
                out.append(f"Q{q['n']} {f['label'] or q['text']} Yes"
                           + (f": {answers.get(f'q{q['n']}_explain')}" if answers.get(f"q{q['n']}_explain") else ""))
    return out
