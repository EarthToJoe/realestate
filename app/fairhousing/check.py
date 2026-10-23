"""The fair-housing pipeline (spec section 5), run on every piece of copy and every outgoing message.

1. Rules pass: deterministic, instant; every hit with rule ID, class, span, tier and legal basis.
2. Model review pass (Haiku): the rules summary is the cached system prompt; the model looks for what patterns
   miss (implied preference, coded language, steering by implication) and returns findings in the same shape plus
   a corrected version that keeps the meaning.
3. Merge: one findings list; the AI's fixed version; warn findings carry the AI's choice and its reason.
4. Gate: `require_pass` refuses "ready to publish" or "sent" unless a passing result exists for that exact text.
   This is the software complying with the law, not a human approval; it is enforced here, in the service layer.

Results are stored (`fair_housing_result`) for the discrimination-complaint window (L61).
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field
from functools import lru_cache
from pathlib import Path

import yaml
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit import record_event
from app.fairhousing.schemas import FairHousingReview
from app.logging_setup import log
from app.model.provider import ModelProvider, ReplayMiss, SpendCapReached
from app.models import FairHousingResult
from app.sanitize import clean, clean_model

HERE = Path(__file__).resolve().parent
RULES_PATH = HERE / "rules.yaml"
PROMPT_VERSION = "fh_review.v1"


class FairHousingBlocked(Exception):
    """Publishing or sending was refused: no passing fair-housing result for this exact text."""


@dataclass(frozen=True)
class Rule:
    id: str
    cls: str
    tier: str
    basis: str
    explanation: str
    suggestion: str
    fix: str | None
    patterns: tuple[re.Pattern, ...]


@dataclass
class RuleSet:
    version: str
    rules: list[Rule]
    by_id: dict[str, Rule] = field(default_factory=dict)


@dataclass
class Finding:
    rule_id: str
    cls: str
    tier: str
    phrase: str
    start: int
    end: int
    basis: str
    explanation: str
    suggestion: str
    source: str  # rules | model | rules+model
    ai_choice: str | None = None  # warn findings: rewritten | kept
    ai_reason: str | None = None


@lru_cache(maxsize=1)
def load_rules(path: Path = RULES_PATH) -> RuleSet:
    raw = yaml.safe_load(path.read_text())
    rules = [Rule(id=r["id"], cls=r["class"], tier=r["tier"], basis=r["basis"], explanation=r["explanation"],
                  suggestion=r["suggestion"], fix=r.get("fix"),
                  patterns=tuple(re.compile(p, re.IGNORECASE) for p in r["patterns"]))
             for r in raw["rules"]]
    rs = RuleSet(version=raw["version"], rules=rules)
    rs.by_id = {r.id: r for r in rules}
    return rs


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def rules_pass(text: str) -> list[Finding]:
    out: list[Finding] = []
    taken: list[tuple[int, int]] = []
    for rule in load_rules().rules:
        for pat in rule.patterns:
            for m in pat.finditer(text):
                if any(m.start() < e and s < m.end() for s, e in taken):
                    continue  # one finding per span: the first (most specific) rule wins
                taken.append((m.start(), m.end()))
                out.append(Finding(rule_id=rule.id, cls=rule.cls, tier=rule.tier, phrase=m.group(0),
                                   start=m.start(), end=m.end(), basis=rule.basis, explanation=rule.explanation,
                                   suggestion=rule.suggestion, source="rules"))
    return sorted(out, key=lambda f: f.start)


def _sentences(text: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in re.finditer(r"[^.!?\n]+(?:[.!?]+|$)\s*|\n+", text)]


def _match_case(src: str, repl: str) -> str:
    return repl[:1].upper() + repl[1:] if src[:1].isupper() else repl


def rules_fix(text: str, findings: list[Finding] | None = None) -> str:
    """The deterministic fixed version: a rule's `fix` replaces its match; a hit with no fix drops its sentence."""
    findings = rules_pass(text) if findings is None else [f for f in findings if f.start >= 0]
    rules = load_rules().by_id
    drop: set[tuple[int, int]] = set()
    spans = _sentences(text)
    replacements: list[Finding] = []
    for f in findings:
        rule = rules.get(f.rule_id)
        if rule and rule.fix is not None:
            replacements.append(f)
        else:
            drop.update(sp for sp in spans if sp[0] <= f.start < sp[1])
    out, cursor = [], 0
    for f in sorted(replacements, key=lambda x: x.start):
        if any(a <= f.start < b for a, b in drop) or f.start < cursor:
            continue
        out.append(text[cursor:f.start])
        out.append(_match_case(f.phrase, rules[f.rule_id].fix))
        cursor = f.end
    out.append(text[cursor:])
    fixed = "".join(out)
    if drop:  # recompute sentence spans on the original and drop by content
        dropped = [text[a:b] for a, b in sorted(drop)]
        for sent in dropped:
            fixed = fixed.replace(sent, "", 1)
    fixed = re.sub(r"[ \t]{2,}", " ", fixed).strip()
    fixed = re.sub(r"\s+([.,;!?])", r"\1", fixed)
    return fixed


def rules_summary() -> str:
    rs = load_rules()
    lines = [f"Rules version {rs.version}."]
    for r in rs.rules:
        lines.append(f"- {r.id} | {r.cls} | {r.tier}: {r.explanation} Suggested: {r.suggestion}")
    return "\n".join(lines)


def system_prompt() -> str:
    return (HERE / "prompts" / "review.v1.md").read_text().replace("{rules_summary}", rules_summary())


def model_pass(s: Session, text: str, provider: ModelProvider, channel: str):
    """One Haiku call; returns (review | None, ModelResult | None, error | None)."""
    try:
        result = provider.generate("fairhousing.review", FairHousingReview, {"channel": channel, "text": text},
                                   s=s, module="fairhousing", system=system_prompt(),
                                   prompt_version=PROMPT_VERSION, side="seller")
    except (ReplayMiss, SpendCapReached) as e:
        return None, None, str(e)
    review: FairHousingReview = clean_model(result.output)
    return review, result, None


def merge(text: str, rule_hits: list[Finding], review: FairHousingReview | None) -> list[Finding]:
    findings = list(rule_hits)
    if review is None:
        return findings
    rules = load_rules().by_id
    lower = text.lower()
    for mf in review.findings:
        phrase = mf.phrase.strip().strip('"')
        start = lower.find(phrase.lower()) if phrase else -1
        end = start + len(phrase) if start >= 0 else -1
        overlap = next((f for f in findings if start >= 0 and f.start < end and start < f.end), None)
        if overlap:
            if overlap.source == "rules":
                overlap.source = "rules+model"
            if mf.tier == "block" and overlap.tier == "warn" and overlap.source != "model":
                # the model reads a preference into a warn-tier phrase: keep the stricter reading
                overlap.tier = "block"
                overlap.explanation = f"{overlap.explanation} Model review: {mf.explanation}"
            continue
        rule = rules.get(mf.rule_id)
        findings.append(Finding(
            rule_id=mf.rule_id if rule else "MODEL", cls=mf.protected_class, tier=mf.tier,
            phrase=text[start:end] if start >= 0 else phrase, start=start, end=end,
            basis=rule.basis if rule else "L36/L37: model review (no rule names this pattern yet)",
            explanation=mf.explanation, suggestion=mf.suggestion, source="model"))
    return sorted(findings, key=lambda f: (f.start < 0, f.start))


def _fixed_version(text: str, findings: list[Finding], review: FairHousingReview | None) -> str:
    if not findings:
        return text
    candidate = None
    if review is not None and review.fixed_text.strip() and review.fixed_text.strip() != text.strip():
        candidate = clean(review.fixed_text.strip())
        if any(f.tier == "block" for f in rules_pass(candidate)):
            candidate = None  # the model's rewrite still trips a rule: fall back to the rules' own fix
    if candidate is None:
        candidate = rules_fix(text, [f for f in findings if f.source != "model"])
    # Warn-tier wording left in the candidate: the AI applies the rule's fix.
    leftover = [f for f in rules_pass(candidate) if f.tier == "warn"]
    return rules_fix(candidate, leftover) if leftover else candidate


def _ai_choices(findings: list[Finding], fixed: str) -> None:
    rules = load_rules().by_id
    for f in findings:
        if f.tier != "warn":
            continue
        if f.phrase and f.phrase.lower() not in fixed.lower():
            f.ai_choice = "rewritten"
            f.ai_reason = f"The AI used neutral wording: {rules[f.rule_id].suggestion if f.rule_id in rules else f.suggestion}."
        else:
            f.ai_choice = "kept"
            f.ai_reason = "Kept as a plain description of the property, not a preference."


def run(s: Session, *, text: str, provider: ModelProvider, entity: str, entity_id: int, version: int,
        deal_id: int | None, channel: str) -> FairHousingResult:
    """Both passes on one exact text; stores and returns the result."""
    hits = rules_pass(text)
    review, mres, error = model_pass(s, text, provider, channel)
    findings = merge(text, hits, review)
    fixed = _fixed_version(text, findings, review)
    _ai_choices(findings, fixed)
    blocks = [f for f in findings if f.tier == "block"]
    passed = not blocks and review is not None  # no model pass, no pass: the gate stays shut
    res = FairHousingResult(
        deal_id=deal_id, entity=entity, entity_id=entity_id, version=version, text_hash=text_hash(text),
        findings=[asdict(f) for f in findings], fixed_text=fixed if findings else None, passed=passed,
        rules_version=load_rules().version, model_mode=mres.mode if mres else None,
        model=mres.model if mres else None, model_error=error)
    s.add(res)
    s.flush()
    record_event(s, actor="ai", kind="ai_action", entity=entity, entity_id=entity_id,
                 summary=(f"Fair-housing check v{version}: {'passed' if passed else 'not passed'}; "
                          f"{len(blocks)} block, {len(findings) - len(blocks)} warn"
                          f"{'; model pass unavailable' if error else ''}"))
    log.info("fair_housing_check", entity=entity, entity_id=entity_id, version=version, passed=passed,
             blocks=len(blocks), findings=len(findings))
    return res


def latest_result(s: Session, entity: str, entity_id: int) -> FairHousingResult | None:
    q = (select(FairHousingResult).where(FairHousingResult.entity == entity, FairHousingResult.entity_id == entity_id)
         .order_by(FairHousingResult.id.desc()).limit(1))
    return s.execute(q).scalar_one_or_none()


def require_pass(s: Session, entity: str, entity_id: int, version: int, text: str) -> FairHousingResult:
    """Refuse unless the newest result for this entity is a pass on exactly this version and text."""
    res = latest_result(s, entity, entity_id)
    if res is None:
        raise FairHousingBlocked("No fair-housing check has run on this text yet.")
    if res.version != version or res.text_hash != text_hash(text):
        raise FairHousingBlocked("The text changed after the last fair-housing check; it must be checked again.")
    if not res.passed:
        blocks = [f for f in res.findings if f["tier"] == "block"]
        if blocks:
            listed = "; ".join(f"{f['rule_id']} ({f['cls']}): \"{f['phrase']}\"" for f in blocks)
            raise FairHousingBlocked(f"The fair-housing check found {len(blocks)} block finding(s): {listed}.")
        raise FairHousingBlocked(f"The model review pass did not run ({res.model_error}); the gate stays shut.")
    return res
