"""Deterministic outputs for the FakeProvider (tests and offline development)."""

from __future__ import annotations


def default(task: str, context: dict) -> dict:
    if task == "intake.infer_gaps":
        facts = {f["field"]: f["value"] for f in context.get("property", {}).get("facts", [])}
        out = [{"field": "OilTankLikely", "label": "Oil storage tank", "confidence": "high",
                "value": "Likely an oil tank on site", "reason": f"Heating fuel recorded as {facts.get('HeatingFuel')}"}]
        if facts.get("Sewer", "").lower().startswith("private"):
            out.append({"field": "SepticInspection", "label": "Septic inspection", "confidence": "medium",
                        "value": "A buyer's lender will probably ask for a septic and well test",
                        "reason": "Private well and septic on the record"})
        out.append({"field": "LivingAreaLowerLevel", "label": "Lower level in living area", "confidence": "low",
                    "value": "Probably includes part of the raised ranch's lower level",
                    "reason": "Raised ranch, one story recorded, finished basement recorded separately"})
        return {"inferences": out, "questions_for_seller": ["Is there a garage or carport?"],
                "summary": "The record covers size, rooms and systems. The AI inferred three facts. "
                           "The seller should confirm parking and the roof's age."}
    if task == "pricing.recommend":
        c = context["computed"]
        weak = [{"rank": x["rank"], "why": "; ".join(x["weak"])} for x in context["comparables"] if x["weak"]]
        price = int(round(c["indicated_value"] / 5000) * 5000)
        return {"method_plain": "We used eight nearby one-family sales from the county's public records and "
                                "adjusted each toward this house for date, size, lot, age, rooms and style.",
                "weak_comps": weak, "recommended_price": price,
                "reconciliation": f"The adjusted sales indicate ${c['adjusted_indicated']:,}, above the "
                                  f"cross-checks' median of ${c['cross_check_median']:,}; the style and date "
                                  "adjustments explain most of the gap.",
                "reasoning": f"${price:,} sits at the weighted indicated value, inside the computed range. The "
                             "adjustments leave out the pond and interior condition.",
                "things_that_would_change_it": ["A septic or well problem at inspection",
                                                "Confirmed pond frontage inside the lot lines"]}
    if task == "copy.draft":
        price = context.get("list_price") or 0
        return {"mls_remarks": "Raised ranch on 4.18 acres in Holmes with three bedrooms and three full baths, "
                               "an 840 sq ft finished lower level, a kitchen updated in 2019 and windows from 2016. "
                               "A pond sits at the back edge of the lot. Private well and septic; oil heat. "
                               "About 6 minutes' drive to the Patterson Metro-North station. Pawling Central "
                               "School District.",
                "portal_description": "This raised ranch sits on 4.18 acres in the hamlet of Holmes, Town of "
                                      "Pawling. Three bedrooms and three full baths, a finished lower level, a "
                                      "kitchen updated in 2019 and new windows in 2016. Spacious master bedroom.",
                "social_posts": [
                    {"platform": "Facebook", "text": f"New in Holmes: a raised ranch on 4.18 acres, ${price:,}."},
                    {"platform": "Instagram", "text": f"4.18 acres, a pond at the back of the lot. ${price:,}."},
                    {"platform": "Nextdoor", "text": f"Raised ranch on Route 292 in Holmes, ${price:,}."}],
                "flyer": {"headline": "Raised ranch on 4.18 acres", "subhead": "Holmes, NY · 3 beds · 3 baths",
                          "bullets": ["4.18 acres with a pond at the back edge", "Kitchen updated 2019",
                                      "840 sq ft finished lower level", "Private well and septic",
                                      "About 6 minutes to Patterson station"],
                          "paragraph": "A raised ranch on a large lot in the Town of Pawling."}}
    if task == "fairhousing.review":
        from app.fairhousing.check import rules_fix

        text = context["text"]
        coded = {"same faith": ("creed", "block"), "gentleman of leisure": ("sex; age", "block"),
                 "manage the stairs without help": ("disability", "block")}
        findings = [{"phrase": k, "protected_class": cls, "rule_id": "MODEL", "tier": tier,
                     "explanation": "Implies a preferred buyer.", "suggestion": "Describe the property."}
                    for k, (cls, tier) in coded.items() if k in text.lower()]
        return {"findings": findings, "fixed_text": rules_fix(text)}
    if task == "probe.mask_roundtrip":
        return {"reply": "Hello [BUYER_1], thanks for asking. The house has 3 bedrooms.", "tokens_seen": ["[BUYER_1]"]}
    raise KeyError(f"no fake output for task {task}")
