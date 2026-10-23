"""Step 10 Marketing the business (spec section 3, step 10; SC10).

The AI drafts and publishes (simulated) the brokerage's own campaign: a landing page for home sellers, one local ad
and one seller lead magnet. Everything a piece of listing copy goes through, these go through too, plus two checks
that only the firm's own advertising needs:

1. `draft`: one model call (`brand.campaign`) writes the three pieces from the firm's config (no deal facts, no PII).
   Each is a `copy_artifact` (channels brand_landing, brand_ad, brand_magnet), checked at once.
2. `check`: the fair-housing pipeline (rules + model review, the same gate as step 3) and the **claims check**
   (code): no "licensed", no "replaces your agent / lawyer", no "you don't need a lawyer", no reviews or
   testimonials, no guarantees (L54, L23); savings figures warn. A pass on both writes CP-26 (per piece, step 10).
3. `plant` (demo button) puts the bold claim the idea invites on the landing page; the claims check refuses it;
   `apply_fix` removes it and re-checks.
4. The landing page's **required notices** are added by code, never by the model, and checked present: the firm's
   identity block with the broker-of-record line (L10, CP-35), the fair-housing notice link (L40, 19 NYCRR 175.29),
   the DOS-2156 link (L39), the AI-use notice (L55, L62) and the lead magnet's consent line (L50 to L52).
5. **Targeting** (L38): the AI sets the ad's audience from the allowed criteria only (housing ad category, place by
   radius, everyone 18 and over); `try_targeting` refuses any blocked criterion in code (age, gender, family,
   ZIP code, lookalike, interests that stand for a protected class, client-list audiences) and logs the refusal.
6. `publish`: refused unless every piece passed both checks on its exact text, the notices are present and the
   targeting holds only allowed criteria; then the AI marks each piece ready, publishes (simulated) and writes the
   **CP-19** marker: only a licensed broker may place the firm's advertising and approve each ad (L10, L18, L38).
"""

from __future__ import annotations

import copy
import re
from pathlib import Path

from markupsafe import Markup, escape
from sqlalchemy import select
from sqlalchemy.orm import Session, object_session

from app.audit import record_event
from app.brokerage import brokerage
from app.fairhousing import check as fh
from app.model.provider import ModelProvider, ModelResult
from app.models import BrandState, CopyArtifact, Deal, FairHousingResult, now
from app.modules.brand.schemas import Campaign
from app.records import service as records
from app.sanitize import clean_model
from app.web import NotFound

PROMPTS = Path(__file__).with_name("prompts")
PROMPT_VERSION = "campaign.v1"
STEP = 10
FOUNDER = "[FOUNDER]"
PIECES = [("brand_landing", "Landing page"), ("brand_ad", "Local ad"), ("brand_magnet", "Seller lead magnet")]
# The claim the idea invites, planted by the demo button: the claims check must refuse it (L54, L23).
PLANTED = "The AI that replaces your agent and your lawyer."


class CampaignRefused(Exception):
    """Publishing or targeting was refused by a check in code."""


# ---- claims check (L54, L23): code, not the model --------------------------------------------------------------

CLAIMS = [
    ("CL-LAWYER", "block", re.compile(
        r"\b(?:no need for|(?:don'?t|do not|never|won'?t) need|without|skip(?:ping)?|replac\w*|instead of|cut out)\b"
        r"[^.\n]{0,30}\b(?:lawyers?|attorneys?|legal fees?)\b|\bno (?:lawyers?|attorneys?)\b|"
        r"\b(?:lawyers?|attorneys?) (?:is |are )?(?:not needed|not required|unnecessary|optional)\b", re.I),
     "Says or implies a seller does not need a lawyer.",
     "L23: the firm may never tell anyone they do not need a lawyer, nor discourage them from consulting one "
     "(DOS LI04; Judiciary Law §§478, 484)."),
    ("CL-REPLACE", "block", re.compile(
        r"\breplac\w*\b[^.\n]{0,30}\b(?:agents?|realtors?|brokers?)\b|\b(?:no|without (?:an?|the|your))\s+"
        r"(?:real estate )?(?:agents?|realtors?|brokers?)\b", re.I),
     "Claims to replace agents or brokers.",
     "L54: no \"replaces your agent and lawyer\" claims (FTC Act §5; GBL §§349, 350). NY law today still requires a "
     "licensed broker for the agent's acts, so the claim would mislead."),
    ("CL-LICENSED", "block", re.compile(
        r"\b(?:we(?:'re| are)|our (?:firm|team|AI) is|fully|state)[- ]licensed\b|\blicensed (?:AI|brokerage|firm|"
        r"broker of record|real estate (?:firm|company))\b", re.I),
     "Claims the firm or its AI is licensed.",
     "L54 and CP-35: this demonstration has no licensed broker of record, so \"licensed\" would be deceptive."),
    ("CL-REVIEWS", "block", re.compile(
        r"\b\d(?:\.\d)?[- ]?stars?\b|\bfive[- ]star\b|\b(?:customer|client|seller) (?:reviews?|testimonials?)\b|"
        r"\btestimonials?\b|[\"“][^\"”]{10,}[\"”]\s*[-–—]\s*\w", re.I),
     "Uses reviews, ratings or testimonials.",
     "L54: no generated or unsubstantiated reviews or testimonials (16 CFR 465.2, 465.5)."),
    ("CL-GUARANTEE", "block", re.compile(r"\bguarantee[ds]?\b", re.I),
     "Makes a guarantee.",
     "L54: every claim must be substantiated; a guarantee needs stated terms (FTC Act §5)."),
    ("CL-SAVINGS", "warn", re.compile(
        r"\bsav(?:e|es|ing|ings)\b[^.\n]{0,40}(?:\$\s?[\d,]+|thousands|\d+\s?%)", re.I),
     "States a saving.",
     "L54: a savings figure needs substantiation (FTC Act §5); state the flat fee as a fact instead."),
]


def claims_check(text: str) -> list[dict]:
    out = []
    for rule_id, tier, pat, what, basis in CLAIMS:
        for m in pat.finditer(text):
            out.append({"rule_id": rule_id, "tier": tier, "phrase": m.group(0), "start": m.start(), "end": m.end(),
                        "what": what, "basis": basis})
    return sorted(out, key=lambda f: f["start"])


def claims_fix(text: str) -> str:
    """Drop every paragraph (or sentence) holding a block claim."""
    bad = [f for f in claims_check(text) if f["tier"] == "block"]
    if not bad:
        return text
    parts = text.split("\n\n")
    keep = []
    for p in parts:
        if any(f["phrase"] in p for f in bad):
            sentences = re.split(r"(?<=[.!?])\s+", p)
            rest = " ".join(x for x in sentences if not any(f["phrase"] in x for f in bad)).strip()
            if rest:
                keep.append(rest)
        else:
            keep.append(p)
    return "\n\n".join(keep)


# ---- the landing page's required notices (code, never the model) -------------------------------------------------

def notices() -> list[dict]:
    b = brokerage()
    return [
        {"id": "identity", "title": "The firm's identity and broker of record",
         "text": f"{b['name']} ({b['name_note']}) · {b['office_address']} · {b['phone']} · {b['broker_of_record']}.",
         "basis": "L10: every advertisement names the broker as licensed (19 NYCRR 175.25); CP-35"},
        {"id": "fair_housing", "title": "Fair-housing notice",
         "text": "Equal Housing Opportunity. New York's Fair Housing Notice and the Housing and Anti-Discrimination "
                 "Disclosure Form (DOS-2156) are linked here.",
         "links": [("New York State Fair Housing Notice (19 NYCRR 175.29)",
                    "https://www.law.cornell.edu/regulations/new-york/19-NYCRR-175.29"),
                   ("Housing and Anti-Discrimination Disclosure Form (DOS-2156)",
                    "https://dos.ny.gov/housinganti-discrimination-form-dos-2156")],
         "basis": "L40: a homepage link to the fair-housing notice (19 NYCRR 175.29); L39"},
        {"id": "ai_use", "title": "AI-use notice",
         "text": "You are dealing with AI software, not a person. AI answers may be inaccurate. Nothing here is legal "
                 "advice; you may consult a lawyer of your choice at any time.",
         "basis": "L55 (GBL §396-b, Art. 47) and L62 (pending AI-inaccuracy notice); L23, L29"},
        {"id": "consent", "title": "Lead-magnet consent line",
         "text": "We e-mail you the guide once. No calls, texts or further e-mail without your separate consent; "
                 "unsubscribe at any time.",
         "basis": "L50 to L52: consent before marketing calls, texts and e-mail (TCPA, CAN-SPAM, GBL §399-z)"},
    ]


def notices_present(rendered: str) -> list[dict]:
    """Each notice and whether its text is on the rendered landing page."""
    return [{**n, "present": n["text"] in rendered} for n in notices()]


# ---- targeting (L38) ----------------------------------------------------------------------------------------------

def allowed_targeting() -> list[dict]:
    b = brokerage()
    return [
        {"id": "category", "label": "Ad category", "value": "Housing (special ad category)",
         "why": "Required for housing ads: the platform removes age, gender, ZIP-code and detailed targeting "
                "(DOJ and Meta settlement, 2022)."},
        {"id": "place", "label": "Where", "value": f"Within {b['ad_radius_miles']} miles of {b['ad_center']}",
         "why": "Place by radius only, at least 15 miles, never by ZIP code: a radius does not pick out "
                "neighbourhoods."},
        {"id": "who", "label": "Who", "value": "Everyone 18 and over, every gender",
         "why": "No one is left out for who they are."},
        {"id": "audiences", "label": "Interests and audiences", "value": "None",
         "why": "No interests, lookalike audiences or uploaded lists: each can stand in for a protected class."},
    ]


BLOCKED = [
    ("age", "Age range (for example 25 to 44)", "Age is a protected class in New York (Executive Law §296); "
     "housing ads may not be targeted by age (L38)."),
    ("gender", "Gender", "Sex and gender identity are protected classes (L36, L38)."),
    ("family", "Parents, families with children, newlyweds", "Familial and marital status are protected classes; "
     "targeting by them expresses a preference (42 U.S.C. §3604(c); L38)."),
    ("zip", "ZIP codes", "ZIP codes stand in for race and national origin; the DOJ and Meta settlement bars them "
     "for housing ads (L38)."),
    ("lookalike", "Lookalike audience of past clients", "A lookalike copies the make-up of an existing group; "
     "barred for housing ads since the 2022 settlement (L38)."),
    ("interests", "Interests (a place of worship, a language, a heritage month)", "Interests can stand in for "
     "religion, national origin or other classes (Executive Law §296(5-a): effects count; L38, L58)."),
    ("client_list", "Uploaded client list (custom audience)", "Targeting a list of people sorts them by who they "
     "are, and uses their personal data without marketing consent (L38, L50 to L52)."),
]
BLOCKED_IDS = {b[0] for b in BLOCKED}


def try_targeting(s: Session, deal: Deal, criterion: str) -> None:
    """Demo: try to add a blocked criterion. Always refused, in code, with the reason; logged."""
    hit = next((b for b in BLOCKED if b[0] == criterion), None)
    if hit is None:
        raise ValueError("Unknown targeting criterion.")
    st = state(deal)
    st.setdefault("refused", []).append({"criterion": hit[1], "why": hit[2], "at": now().isoformat()})
    _save(s, deal, st)
    record_event(s, actor="presenter", kind="system", entity="brand", entity_id=deal.id,
                 summary=f"Targeting refused by code: {hit[1]} (L38)")
    raise CampaignRefused(f"Refused: the ad cannot be targeted by \"{hit[1]}\". {hit[2]}")


def check_targeting(targeting: list[dict]) -> None:
    ids = {t["id"] for t in targeting}
    bad = ids & BLOCKED_IDS
    if bad or ids - {t["id"] for t in allowed_targeting()}:
        raise CampaignRefused(f"The ad's targeting holds criteria that are not allowed: {sorted(bad or ids)}.")


# ---- state ------------------------------------------------------------------------------------------------------

def _row(deal: Deal) -> BrandState:
    s = object_session(deal)
    row = s.execute(select(BrandState).where(BrandState.deal_id == deal.id)).scalar_one_or_none()
    if row is None:
        row = BrandState(deal_id=deal.id, state={})
        s.add(row)
        s.flush()
    return row


def state(deal: Deal) -> dict:
    return copy.deepcopy(_row(deal).state or {})


def _save(s: Session, deal: Deal, st: dict) -> None:
    _row(deal).state = st
    s.flush()


def artifacts(s: Session, deal: Deal) -> list[CopyArtifact]:
    order = {c: i for i, (c, _) in enumerate(PIECES)}
    rows = s.execute(select(CopyArtifact).where(CopyArtifact.deal_id == deal.id,
                                                CopyArtifact.channel.in_(list(order)))).scalars().all()
    return sorted(rows, key=lambda a: order[a.channel])


def get(s: Session, deal: Deal, artifact_id: int) -> CopyArtifact:
    art = s.get(CopyArtifact, artifact_id)
    if art is None or art.deal_id != deal.id or art.channel not in dict(PIECES):
        raise NotFound("No such campaign piece.")
    return art


# ---- the pieces as text and back --------------------------------------------------------------------------------

def landing_text(lp: dict) -> str:
    return "\n\n".join([lp["headline"], *lp["body"], lp["call_to_action"]])


def ad_text(ad: dict) -> str:
    return f"{ad['headline']}\n\n{ad['text']}"


def magnet_text(mg: dict) -> str:
    return "\n\n".join([mg["title"], mg["pitch"], "\n".join(f"- {x}" for x in mg["outline"])])


def parse(art: CopyArtifact) -> dict:
    """The stored text back into parts for the screen."""
    parts = [p for p in art.text.split("\n\n") if p.strip()]
    if art.channel == "brand_landing":
        return {"headline": parts[0] if parts else "", "body": parts[1:-1], "cta": parts[-1] if len(parts) > 1 else ""}
    if art.channel == "brand_ad":
        return {"headline": parts[0] if parts else "", "text": " ".join(parts[1:])}
    outline = [ln[2:] for p in parts for ln in p.splitlines() if ln.startswith("- ")]
    rest = [p for p in parts if not p.startswith("- ")]
    return {"title": rest[0] if rest else "", "pitch": " ".join(rest[1:]), "outline": outline}


def founder(text: str) -> str:
    return text.replace(FOUNDER, brokerage()["founder_display"])


def founder_html(marked: Markup) -> Markup:
    """The founder placeholder inside already-escaped HTML (the token has no characters HTML escapes)."""
    return Markup(str(marked).replace(FOUNDER, str(escape(brokerage()["founder_display"]))))


# ---- the AI's acts ------------------------------------------------------------------------------------------------

def model_context() -> dict:
    """Whitelist: the firm's config only. No deal, no property, no person."""
    b = brokerage()
    return {"firm": b["name"], "firm_note": b["name_note"], "founder": FOUNDER, "area": b["area"],
            "services": b["services"], "flat_fee": b["flat_fee"], "timeline": b["timeline"],
            "ad_area": f"within {b['ad_radius_miles']} miles of {b['ad_center']}"}


def draft(s: Session, deal: Deal, provider: ModelProvider) -> ModelResult | None:
    if artifacts(s, deal):
        return None
    system = (PROMPTS / f"{PROMPT_VERSION}.md").read_text()
    result = provider.generate("brand.campaign", Campaign, model_context(), s=s, module="brand", system=system,
                               prompt_version=PROMPT_VERSION, side="seller")
    out: Campaign = clean_model(result.output)
    result.output = out
    texts = {"brand_landing": landing_text(out.landing_page.model_dump()),
             "brand_ad": ad_text(out.local_ad.model_dump()),
             "brand_magnet": magnet_text(out.lead_magnet.model_dump())}
    for channel, title in PIECES:
        s.add(CopyArtifact(deal_id=deal.id, channel=channel, title=title, text=texts[channel],
                           mode=result.mode, model=result.model))
    st = state(deal)
    st["draft"] = {"mode": result.mode, "model": result.model, "recorded_at": result.recorded_at,
                   "targeting_reason": out.targeting_reason}
    _save(s, deal, st)
    record_event(s, actor="ai", kind="ai_action", entity="brand", entity_id=deal.id,
                 summary=f"Firm campaign: AI wrote a landing page, a local ad and a lead magnet ({result.mode}, "
                         f"{result.model})")
    for art in artifacts(s, deal):
        check(s, deal, art, provider)
    return result


def claims_of(art: CopyArtifact) -> list[dict]:
    return claims_check(art.text)


def check(s: Session, deal: Deal, art: CopyArtifact, provider: ModelProvider) -> FairHousingResult:
    res = fh.run(s, text=art.text, provider=provider, entity="copy_artifact", entity_id=art.id, version=art.version,
                 deal_id=deal.id, channel=art.channel)
    claims_block = [c for c in claims_of(art) if c["tier"] == "block"]
    art.status = "passed" if res.passed and not claims_block else "blocked"
    if art.status == "passed":
        records.record_auto(s, deal.id, "CP-26",
                            reason=f"Fair-housing and claims checks passed: {art.title} v{art.version} "
                                   f"({res.rules_version}; model review {res.model_mode})",
                            attached_to=f"copy_artifact:{art.id}:v{art.version}", step=STEP)
    else:
        record_event(s, actor="ai", kind="ai_action", entity="copy_artifact", entity_id=art.id,
                     summary=f"{art.title} v{art.version} not passed: {len(claims_block)} claim(s) refused"
                             f"{'' if res.passed else '; fair-housing check not passed'}")
    s.flush()
    return res


def _new_version(s: Session, art: CopyArtifact, text: str, edited_by: str) -> None:
    art.text = text
    art.version += 1
    art.edited_by = edited_by
    art.status = "draft"
    art.ready_at = None
    s.flush()


def plant(s: Session, deal: Deal, art: CopyArtifact, provider: ModelProvider) -> FairHousingResult:
    """Demo button: put the bold claim under the landing page's headline; the claims check refuses it."""
    if art.channel != "brand_landing":
        raise ValueError("The demo claim goes on the landing page.")
    parts = art.text.split("\n\n")
    _new_version(s, art, "\n\n".join([parts[0], PLANTED, *parts[1:]]), "planted (demo)")
    record_event(s, actor="presenter", kind="system", entity="copy_artifact", entity_id=art.id,
                 summary=f"Demo: planted a claim in {art.title} (v{art.version})")
    return check(s, deal, art, provider)


def apply_fix(s: Session, deal: Deal, art: CopyArtifact, provider: ModelProvider) -> FairHousingResult:
    text = claims_fix(art.text)
    res = fh.latest_result(s, "copy_artifact", art.id)
    if res is not None and not res.passed and res.fixed_text and res.version == art.version:
        text = claims_fix(res.fixed_text)
    if text == art.text:
        raise ValueError("There is nothing to fix in the current text.")
    _new_version(s, art, text, "ai_fix")
    record_event(s, actor="ai", kind="ai_action", entity="copy_artifact", entity_id=art.id,
                 summary=f"AI removed the refused wording from {art.title} (v{art.version})")
    return check(s, deal, art, provider)


def set_targeting(s: Session, deal: Deal) -> list[dict]:
    """The AI sets the ad's audience from the allowed criteria only."""
    st = state(deal)
    if st.get("targeting"):
        return st["targeting"]
    targeting = allowed_targeting()
    check_targeting(targeting)
    st["targeting"] = targeting
    _save(s, deal, st)
    record_event(s, actor="ai", kind="ai_action", entity="brand", entity_id=deal.id,
                 summary="AI set the ad's targeting: housing category, place by radius, everyone 18 and over")
    return targeting


def rendered_landing(art: CopyArtifact) -> str:
    """What the published page carries: the AI's text plus the notices the code adds."""
    return founder(art.text) + "\n\n" + "\n\n".join(n["text"] for n in notices())


def publish(s: Session, deal: Deal) -> dict:
    """The AI publishes the campaign (simulated) and writes CP-19. Refused, here in the service layer, unless every
    piece passed both checks on its exact text, the landing page carries every notice and the targeting is allowed."""
    st = state(deal)
    if st.get("published"):
        return st["published"]
    arts = artifacts(s, deal)
    if len(arts) != len(PIECES):
        raise CampaignRefused("The campaign is not drafted yet.")
    for art in arts:
        fh.require_pass(s, "copy_artifact", art.id, art.version, art.text)
        blocks = [c for c in claims_of(art) if c["tier"] == "block"]
        if blocks:
            raise CampaignRefused(f"{art.title}: the claims check refuses \"{blocks[0]['phrase']}\" "
                                  f"({blocks[0]['basis']})")
    landing = next(a for a in arts if a.channel == "brand_landing")
    missing = [n["title"] for n in notices_present(rendered_landing(landing)) if not n["present"]]
    if missing:
        raise CampaignRefused(f"The landing page lacks a required notice: {', '.join(missing)}.")
    if not st.get("targeting"):
        raise CampaignRefused("The ad's targeting is not set yet.")
    check_targeting(st["targeting"])
    for art in arts:
        art.status = "ready"
        art.ready_at = now()
    b = brokerage()
    st["published"] = {"at": now().isoformat(), "where": [
        "Landing page: the firm's website (simulated)",
        f"Local ad: Facebook and Instagram, housing category, within {b['ad_radius_miles']} miles of "
        f"{b['ad_center']} (simulated)",
        "Lead magnet: offered on the landing page (simulated)"]}
    _save(s, deal, st)
    records.mark_law(s, deal.id, "CP-19", reason="The AI published the firm's campaign (simulated): a landing page, "
                                                 "a local ad and a seller lead magnet, each fair-housing and claims "
                                                 "checked, the ad targeted by place only", attached_to="brand")
    record_event(s, actor="ai", kind="ai_action", entity="brand", entity_id=deal.id,
                 summary="AI published the firm's campaign (simulated)")
    return st["published"]
