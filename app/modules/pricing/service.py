"""Step 2 Pricing (spec section 3, step 2): comparative market analysis, not an appraisal.

1. `analyse`: code, no model. Reads the comparable sales (`PublicRecordConnector` fixture: Dutchess County
   ParcelAccess, public records only), adjusts each one toward the subject with the rates in `RATES` (stated on
   screen), flags weak comparables, and computes the indicated value and a suggested range.
2. `advise`: one model call (`pricing.recommend`). The model writes the method in plain words, flags weak
   comparables, and recommends a list price with its reasoning. The AI advising on price is an agent act NY law
   reserves to a licensed broker: CP-25 marker. Opens CP-05: the seller chooses the price.
3. `choose_price`: the seller's own decision (CP-05). Listing copy stays blocked until it is made.
4. `net_sheet`: code, at any price.

No PII reaches this module: the model sees property facts and the comparables only.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from statistics import median

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit import record_event
from app.brokerage import brokerage
from app.connectors.public_records import FixtureRecords
from app.model.context import AgentContext
from app.model.provider import ModelProvider, ModelResult
from app.models import Deal, PricingAnalysis
from app.modules.pricing.schemas import PricingAdvice
from app.records import service as records
from app.sanitize import clean_model

PROMPTS = Path(__file__).with_name("prompts")
PROMPT_VERSION = "recommend.v2"
AS_OF = date(2026, 10, 23)  # the analysis date: the demo-house records were read on this day

# Adjustment rates (USD), applied to each comparable toward the subject. [INFERENCE] demonstration rates for
# rural Dutchess County one-family homes, set by us from the fixture's own evidence and stated on screen; a
# production CMA would derive them by paired-sales analysis.
# Re-examined 2026-10-23 against docs/specs/demo-house.md (decision 30, dated note):
# - time: the equalisation-rate move (29.61 -> 27.35, about +8%) falls between the two rolls' valuation dates,
#   before most of these sales; the fixture's own sales show no trend after it (Pawling sale / 2026 full market
#   value: Jul 2025 1.034, Aug 2025 1.049, Sep 2025 1.033, Mar 2026 1.029). Cut from +4% to +2% a year.
# - basement: the -8% style rate was measured on raised ranches that have finished lower levels, so for a sale of
#   another style it already prices the subject's basement; adjusting both counted it twice (+$21,000 on five
#   sales). Now adjusted only between sales of the same style.
# - lot: the fixture shows no acreage premium (the 6.55-acre sale had the lowest price a foot, $222); cut from
#   $5,000 to $2,500 an acre.
RATES = {
    "time_pct_per_month": 0.17,  # about +2% a year
    "living_area_per_sqft": 75,  # about 30% of the comparables' median $258/sq ft: added area is worth less
    "finished_basement_per_sqft": 25, "basement_same_style_only": True,
    "lot_per_acre": 2500, "lot_cap_acres": 3.0,  # rural acreage beyond a building lot adds little
    "year_built_per_year": 1000,
    "bedroom": 5000, "full_bath": 10000, "half_bath": 5000,
    "central_air": 8000, "garage": 15000,
    "style_pct": -8.0,  # a raised ranch's lower level counts in living area but sells for less a foot: the two
    # raised-ranch sales averaged $245/sq ft against a median of about $266 for the other styles (fixture)
}
WEAK_GROSS_PCT = 25.0  # gross adjustments above this share of the sale price mark a weak comparable
WEAK_DISTANCE_MI = 3.0

LABEL = "Comparative market analysis, not an appraisal"


def subject_facts(deal: Deal) -> dict:
    """The subject's numbers, from the public record plus the seller's answers (garage)."""
    data = FixtureRecords().data["property"]
    facts = {f.field: f.value for f in deal.property.facts}
    parking = (facts.get("ParkingFeatures") or "").lower()
    return {
        "address": f"{deal.property.street}, {deal.property.city}, NY",
        "style": data["building_style"]["value"], "year_built": int(data["year_built"]["value"]),
        "living_area_sqft": int(data["living_area_sqft"]["value"]),
        "finished_basement_sqft": int(data["finished_basement_sqft"]["value"] or 0),
        "bedrooms": int(data["bedrooms"]["value"]), "bathrooms_full": int(data["bathrooms_full"]["value"]),
        "bathrooms_half": int(data["bathrooms_half"]["value"] or 0), "acres": float(data["lot_acres"]["value"]),
        "central_air": bool(data["central_air"]["value"]),
        "garage": "garage" in parking and "no garage" not in parking,
        "heating_fuel": data["heating_fuel"]["value"],
        "full_market_value_2026": data["assessments"]["value"][0]["full_market_value"]
        if isinstance(data["assessments"].get("value"), list) else None,
    }


def _months(sale_date: str) -> float:
    d = date.fromisoformat(sale_date)
    return round((AS_OF - d).days / 30.44, 1)


def adjust(comp: dict, subj: dict) -> dict:
    """Adjust one sale toward the subject. Positive = the subject has more of it than the comparable."""
    price = comp["sale_price"]
    lines = []

    def add(name: str, amount: float, why: str) -> None:
        if round(amount):
            lines.append({"factor": name, "amount": int(round(amount, -2)), "why": why})

    months = _months(comp["sale_date"])
    add("Date of sale", price * RATES["time_pct_per_month"] / 100 * months,
        f"sold {months:g} months before {AS_OF.isoformat()}, +{RATES['time_pct_per_month']}% a month")
    d_area = subj["living_area_sqft"] - comp["living_area_sqft"]
    add("Living area", d_area * RATES["living_area_per_sqft"], f"{d_area:+,} sq ft at ${RATES['living_area_per_sqft']}")
    d_bsmt = subj["finished_basement_sqft"] - (comp.get("finished_basement_sqft") or 0)
    if RATES["basement_same_style_only"] and comp["style"].lower() != subj["style"].lower():
        d_bsmt = 0  # inside the style rate (measured on raised ranches with finished lower levels)
    add("Finished basement", d_bsmt * RATES["finished_basement_per_sqft"],
        f"{d_bsmt:+,} sq ft at ${RATES['finished_basement_per_sqft']}")
    d_acres = subj["acres"] - comp["acres"]
    capped = max(-RATES["lot_cap_acres"], min(RATES["lot_cap_acres"], d_acres))
    add("Lot size", capped * RATES["lot_per_acre"],
        f"{d_acres:+.2f} acres at ${RATES['lot_per_acre']:,} an acre (first {RATES['lot_cap_acres']:g} acres of "
        f"difference only)")
    d_year = subj["year_built"] - comp["year_built"]
    add("Age", d_year * RATES["year_built_per_year"], f"built {comp['year_built']} vs {subj['year_built']}")
    d_bed = subj["bedrooms"] - comp["bedrooms"]
    add("Bedrooms", d_bed * RATES["bedroom"], f"{d_bed:+d} bedroom(s)")
    d_full = subj["bathrooms_full"] - comp["bathrooms_full"]
    add("Full baths", d_full * RATES["full_bath"], f"{d_full:+d} full bath(s)")
    d_half = subj["bathrooms_half"] - (comp.get("bathrooms_half") or 0)
    add("Half baths", d_half * RATES["half_bath"], f"{d_half:+d} half bath(s)")
    d_air = int(subj["central_air"]) - int(bool(comp.get("central_air")))
    add("Central air", d_air * RATES["central_air"], "the comparable has central air; the subject has none"
        if d_air < 0 else "the subject has central air; the comparable has none")
    d_gar = int(subj["garage"]) - int(bool(comp.get("garage_recorded")))
    add("Garage", d_gar * RATES["garage"], "the comparable has a garage; the subject has none"
        if d_gar < 0 else "the subject has a garage; the comparable has none")
    if comp["style"].lower() != subj["style"].lower():
        add("Style", price * RATES["style_pct"] / 100,
            f"{comp['style']} vs the subject's {subj['style'].lower()}: {RATES['style_pct']:g}%")
    net = sum(x["amount"] for x in lines)
    gross = sum(abs(x["amount"]) for x in lines)
    weak = []
    if gross / price * 100 > WEAK_GROSS_PCT:
        weak.append(f"large adjustments ({gross / price * 100:.0f}% gross)")
    if comp["distance_mi_straight"] > WEAK_DISTANCE_MI:
        weak.append(f"{comp['distance_mi_straight']} miles away")
    return {
        "rank": comp["rank"], "address": comp["address"], "municipality": comp.get("municipality"),
        "distance_mi": comp["distance_mi_straight"], "sale_date": comp["sale_date"], "sale_price": price,
        "style": comp["style"], "same_style": comp["style"].lower() == subj["style"].lower(),
        "year_built": comp["year_built"], "living_area_sqft": comp["living_area_sqft"],
        "finished_basement_sqft": comp.get("finished_basement_sqft") or 0, "bedrooms": comp["bedrooms"],
        "baths": f"{comp['bathrooms_full']}/{comp.get('bathrooms_half') or 0}", "acres": comp["acres"],
        "central_air": bool(comp.get("central_air")), "garage": bool(comp.get("garage_recorded")),
        "price_per_sqft": comp.get("price_per_sqft"), "adjustments": lines, "net_adjustment": net,
        "gross_pct": round(gross / price * 100, 1), "adjusted_price": int(price + net), "weak": weak,
        "source": "Dutchess County ParcelAccess residential sales and property card (public record)",
        "deed": f"Liber {comp.get('deed_book')} page {comp.get('deed_page')}",
    }


def _round(v: float, to: int = 5000) -> int:
    return int(round(v / to) * to)


def cross_checks() -> list[dict]:
    """The three cross-checks of docs/specs/demo-house.md section 4, from the fixture's reference arithmetic."""
    ref = FixtureRecords().data["cma_reference"]
    a, b, c = (ref["method_a_price_per_sqft_all"], ref["method_b_same_style"],
               ref["method_c_assessment_ratio_pawling"])
    area = ref["subject_living_area_sqft"]
    return [
        {"key": "A", "name": "Median price a foot, all 8 sales", "value": a["median_value"],
         "how": f"median ${a['median']}/sq ft x {area:,} sq ft"},
        {"key": "B", "name": "Same style only (the two raised ranches)", "value": b["value"],
         "how": f"${b['mean_price_per_sqft']}/sq ft x {area:,} sq ft; only two sales"},
        {"key": "C", "name": "Town assessment ratio (four Pawling sales)", "value": c["value"],
         "how": f"median sale/assessment {c['median_ratio']} x ${ref['subject_full_market_value_2026']:,}; "
                "Pawling assessments scatter about 13%, so a cross-check only"},
    ]


# Reconciliation: half weight on the adjusted sales, half on the median of the three cross-checks (each is an
# unadjusted method with its own weakness; the adjusted sales rest on demonstration rates). Stated on screen.
RECONCILE_WEIGHT_ADJUSTED = 0.5


def summarise(comps: list[dict]) -> dict:
    """Weights favour comparables needing less adjustment and of the same style; the range spans the
    adjusted prices of the comparables not flagged weak (all of them if fewer than three are strong)."""
    strong = [c for c in comps if not c["weak"]]
    basis = strong if len(strong) >= 3 else sorted(comps, key=lambda c: (len(c["weak"]), c["gross_pct"]))[:5]
    for c in comps:
        w = 1 / (1 + c["gross_pct"] / 10)
        if not c["same_style"]:
            w *= 0.8  # adjusted for style, but a same-style sale is the better guide
        if any("miles away" in x for x in c["weak"]):
            w *= 0.7
        c["weight"] = round(w, 3)
    total = sum(c["weight"] for c in comps)
    indicated = sum(c["adjusted_price"] * c["weight"] for c in comps) / total
    adj = sorted(c["adjusted_price"] for c in basis)
    checks = cross_checks()
    check_mid = median(x["value"] for x in checks)
    reconciled = RECONCILE_WEIGHT_ADJUSTED * indicated + (1 - RECONCILE_WEIGHT_ADJUSTED) * check_mid
    # the range runs from the lower to the higher of the cross-checks and the adjusted-sales indication, so both
    # methods' answers sit inside it and the reconciled value sits between them
    low = _round(min(min(x["value"] for x in checks), indicated), 10000)
    high = _round(max(max(x["value"] for x in checks), indicated), 10000)
    return {
        "indicated_value": _round(reconciled), "adjusted_indicated": _round(indicated),
        "adjusted_range_low": _round(min(adj)), "adjusted_range_high": _round(max(adj)),
        "cross_checks": checks, "cross_check_median": int(check_mid),
        "reconcile_weight_adjusted": RECONCILE_WEIGHT_ADJUSTED,
        "range_low": low, "range_high": high,
        "median_adjusted": _round(median(c["adjusted_price"] for c in comps)),
        "range_rule": ("from the lower to the higher of the cross-checks and the adjusted-sales indication, "
                       "rounded to $10,000; the indicated value gives the adjusted sales and the cross-checks "
                       "half weight each"),
        "adjusted_range_rule": ("lowest to highest adjusted price of the comparables not flagged weak"
                                if len(strong) >= 3 else
                                "lowest to highest adjusted price of the five least-adjusted comparables"),
        "range_basis": [c["rank"] for c in basis], "rates": RATES, "as_of": AS_OF.isoformat(), "label": LABEL,
        "count": len(comps),
    }


def analyse(s: Session, deal: Deal) -> PricingAnalysis:
    existing = current(s, deal)
    if existing:
        return existing
    subj = subject_facts(deal)
    comps = [adjust(c, subj) for c in FixtureRecords().data["comparables"]]
    pa = PricingAnalysis(deal_id=deal.id, comps=comps, summary={**summarise(comps), "subject": subj})
    s.add(pa)
    s.flush()
    record_event(s, actor="ai", kind="ai_action", entity="pricing_analysis", entity_id=pa.id,
                 summary=f"Pricing: {len(comps)} comparable sales adjusted in code; range "
                         f"${pa.summary['range_low']:,} to ${pa.summary['range_high']:,}")
    return pa


def current(s: Session, deal: Deal) -> PricingAnalysis | None:
    q = select(PricingAnalysis).where(PricingAnalysis.deal_id == deal.id).order_by(PricingAnalysis.id.desc())
    return s.execute(q.limit(1)).scalar_one_or_none()


def model_context(s: Session, deal: Deal, pa: PricingAnalysis) -> dict:
    """Whitelist: property facts, the subject's numbers, the adjusted comparables and the computed range.
    No PII and none of the seller's confidential instructions (motivation, floor): the advice is on the market."""
    ctx = AgentContext(s, deal, "seller").build(
        facts=["ArchitecturalStyle", "YearBuilt", "LivingArea", "BelowGradeFinishedArea", "BedroomsTotal",
               "BathroomsFull", "LotSizeAcres", "Cooling", "HeatingFuel", "WaterSource", "Sewer", "ParkingFeatures",
               "ConditionUpdates", "RoofYear", "WaterfrontFeatures", "FullMarketValueState", "SchoolDistrict",
               "FloodZone"],
        instructions=False)
    ctx["subject"] = pa.summary["subject"]
    ctx["comparables"] = [{k: c[k] for k in ("rank", "address", "distance_mi", "sale_date", "sale_price", "style",
                                              "living_area_sqft", "acres", "adjustments", "net_adjustment",
                                              "gross_pct", "adjusted_price", "weak", "weight")}
                          for c in pa.comps]
    ctx["computed"] = {k: pa.summary.get(k) for k in (
        "indicated_value", "adjusted_indicated", "adjusted_range_low", "adjusted_range_high", "cross_checks",
        "cross_check_median", "reconcile_weight_adjusted", "range_low", "range_high", "median_adjusted",
        "range_rule", "rates", "as_of")}
    ctx["not_adjusted_for"] = FixtureRecords().data["cma_reference"]["not_adjusted_for"]
    return ctx


def advise(s: Session, deal: Deal, provider: ModelProvider) -> ModelResult:
    records.require(s, deal.id, "CP-03", action="start pricing (no marketing before the listing agreement, L9)")
    pa = analyse(s, deal)
    system = (PROMPTS / f"{PROMPT_VERSION}.md").read_text()
    result = provider.generate("pricing.recommend", PricingAdvice, model_context(s, deal, pa), s=s,
                               module="pricing", system=system, prompt_version=PROMPT_VERSION, side="seller")
    out: PricingAdvice = clean_model(result.output)
    result.output = out
    pa.advice = out.model_dump()
    pa.mode, pa.model, pa.recorded_at = result.mode, result.model, result.recorded_at
    inside = pa.summary["range_low"] <= out.recommended_price <= pa.summary["range_high"]
    pa.advice["inside_range"] = inside
    records.mark_law(s, deal.id, "CP-25",
                     reason=f"AI recommended a list price of ${out.recommended_price:,} "
                            f"(range ${pa.summary['range_low']:,} to ${pa.summary['range_high']:,}) with its "
                            f"reasoning ({result.mode}, {result.model})",
                     attached_to=f"pricing_analysis:{pa.id}")
    if not records.is_done(s, deal.id, "CP-05"):  # a chosen price stays chosen; new advice does not reopen it
        records.open_decision(s, deal.id, "CP-05", attached_to=f"pricing_analysis:{pa.id}")
    record_event(s, actor="ai", kind="ai_action", entity="pricing_analysis", entity_id=pa.id,
                 summary=f"Pricing: AI recommended ${out.recommended_price:,} ({result.mode})")
    s.flush()
    return result


def choose_price(s: Session, deal: Deal, persona: str, price: int):
    """CP-05: the seller's own decision. Only the seller may make it (records.decide checks the persona)."""
    cp = records.latest(s, deal.id, "CP-05")
    if cp is None:
        raise records.GateError("CP-25", "The AI has not given its price advice yet, so there is no price to "
                                         "choose. Click \"Let the AI recommend a price\" first.")
    if price < 50_000 or price > 5_000_000:
        raise ValueError("Enter a list price between $50,000 and $5,000,000.")
    pa = current(s, deal)
    rec = (pa.advice or {}).get("recommended_price") if pa else None
    records.decide(s, cp, persona=persona, decision="choose",
                   reason=f"The seller chose a list price of ${price:,}"
                          + (f" (the AI recommended ${rec:,})" if rec else ""))
    deal.list_price = price
    deal.current_step = max(deal.current_step, 3)
    s.flush()
    return cp


def net_sheet(price: int, annual_tax: int | None = None) -> dict:
    """The seller's estimated proceeds before any mortgage payoff. Figures are estimates for the demonstration
    [INFERENCE] except the NY transfer tax rate (Tax Law §1402: $2 per $500 of consideration, paid by the seller)."""
    b = brokerage()
    fee = 4995
    lines = [
        {"item": f"{b['name']} flat listing fee (paid at closing)", "amount": fee, "note": b["flat_fee"]},
        {"item": "NY State real estate transfer tax (0.4%)", "amount": int(round(price * 0.004)),
         "note": "Tax Law §1402; paid by the seller. Under $1 million: no mansion tax (that is the buyer's)."},
        {"item": "Buyer's agent compensation", "amount": 0,
         "note": "None offered in this plan; the seller may choose to offer it. It never goes in MLS fields "
                 "(OneKey Rule 502)."},
        {"item": "Seller's attorney, if the seller engages one (estimate)", "amount": 2000,
         "note": "Hudson Valley custom is that each side has a lawyer (L25, custom, not law); the seller decides."},
        {"item": "Recording, payoff and courier fees (estimate)", "amount": 500, "note": "Estimate."},
    ]
    total = sum(x["amount"] for x in lines)
    return {"price": price, "lines": lines, "total_costs": total, "net_before_mortgage": price - total,
            "tax_note": (f"Property taxes (${annual_tax:,} a year from the seller) are prorated at closing; "
                         "not included." if annual_tax else "Property taxes are prorated at closing; not included."),
            "mortgage_note": "Any mortgage payoff comes out of this figure; the POC does not collect it."}
