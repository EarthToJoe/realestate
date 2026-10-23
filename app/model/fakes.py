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
    if task == "inbox.reply":
        sheet = context["fact_sheet"]
        return {"reply": f"The seller reports a pond at the back edge of the lot; a survey would confirm how much "
                         f"is inside the lot lines. The roof dates from {sheet.get('Roof', 'the seller will confirm')}. "
                         f"Please note the house has {sheet.get('Heating fuel', 'oil')} heat, a private well and "
                         "septic, and no central air.",
                "disclosed": ["oil heat", "private well and septic", "no central air"]}
    if task == "offers.advise":
        offers = context["offers"]
        pick = next((o for o in offers if o["label"] == "B"), offers[0])
        lst = context["list_price"] or 640000
        return {"offers": [{"label": o["label"], "summary": f"${o['price']:,}, {o['financing']}.",
                            "risks": o["contingencies"][:2], "advice": "Workable; counter on price."}
                           for o in offers],
                "recommendation": f"Work with offer {pick['label']}: shorter contingencies. Counter on price and the "
                                  "closing date. You decide.",
                "suggested_offer": pick["label"], "suggested_action": "counter",
                "suggested_counter_price": lst, "suggested_lowest_price": lst - 10000,
                "suggested_closing_days": 45, "suggested_terms": "Keep the inspection at 7 days; no requests."}
    if task == "contract.draft":
        t = context["terms"]
        heads = [h.split(". ", 1)[1] for h in context["standard_form_headings"]]
        sections = [{"number": str(i), "heading": h, "text": f"{h}: terms between [SELLER_1] and [BUYER_1]."}
                    for i, h in enumerate(heads, 1)]
        sections[2]["text"] = (f"The purchase price is ${t['price']:,}, of which ${t['deposit']:,} is paid on signing "
                               "as a deposit held in escrow.")
        sections[14]["text"] = f"The closing will take place on or about {t['closing_date']}."
        rider = [{"number": "R1", "heading": "Mortgage commitment",
                  "text": f"[BUYER_1] has {t['mortgage_commitment_days']} days to obtain a mortgage commitment."},
                 {"number": "R2", "heading": "Home inspection",
                  "text": f"[BUYER_1] may inspect within {t['inspection_days']} days."},
                 {"number": "R3", "heading": "Disclosures", "text": "The Property Condition Disclosure Statement "
                                                                  "completed by [SELLER_1] is attached."}]
        return {"title": "Residential Contract of Sale", "sections": sections, "rider": rider,
                "side_by_side": [{"standard_number": i, "draft_ref": str(i), "note": "Same substance"}
                                 for i in range(1, len(heads) + 1)],
                "notes_to_parties": ["Each of you may have a lawyer of your choice review this draft."]}
    if task == "buyer.alert":
        return {"message": f"{len(context['listings'])} homes match your search.",
                "notes": [{"id": x["id"], "why": f"{x['beds']} bedrooms on {x['acres']} acres in {x['town']}."}
                          for x in context["listings"]]}
    if task == "buyer.offer_advise":
        lst = context["listing"]["list_price"]
        return {"advice": "Offer below the list price: the public sales support it, and the house has no central "
                          "air. Keep the inspection and the well and septic tests.",
                "recommended_price": lst - 20000, "walk_away_note": "You have room under your own maximum.",
                "deposit_pct": 10, "financing": "Conventional mortgage, 25% down; pre-approval attached",
                "mortgage_days": 30, "inspection_days": 7, "closing_days": 45,
                "contingencies": ["mortgage commitment", "home inspection", "well and septic tests"],
                "requests": [], "risks": ["Septic age unknown until tested"]}
    if task == "buyer.counter_advise":
        mine, theirs = context["buyer_offer"], context["seller_counter"]
        mid = (mine["price"] + theirs["price"]) // 2 // 1000 * 1000
        maximum = context["instructions"]["confidential"]["maximum_price"]
        if theirs["price"] <= mine["price"] + 6000 or len(context["replies_sent"]) >= 1:
            return {"advice": "The counter is close and within your limit: accept.", "action": "accept",
                    "price": theirs["price"], "closing_days": theirs["closing_days"],
                    "inspection_days": theirs["inspection_days"], "mortgage_days": theirs["mortgage_days"],
                    "requests": theirs.get("requests") or []}
        return {"advice": "Meet the seller part way.", "action": "counter", "price": min(mid, maximum),
                "closing_days": theirs["closing_days"], "inspection_days": theirs["inspection_days"],
                "mortgage_days": theirs["mortgage_days"], "requests": []}
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
    if task == "brand.campaign":
        return {"landing_page": {
                    "headline": f"Sell your {context['area'].split(' and ')[0]} home with an AI agent",
                    "body": [f"{context['firm']} is a new kind of brokerage: AI software does the agent's work, from "
                             "pricing to the signed contract, and you make every decision.",
                             f"One flat fee: {context['flat_fee']}. Founded by {context['founder']}."],
                    "call_to_action": "Start with your address"},
                "local_ad": {"headline": "An AI agent for your sale", "text": "Pricing, marketing, offers and "
                             "the contract draft, at one flat fee. Every decision stays yours."},
                "lead_magnet": {"title": "What selling a home here costs and takes",
                                "pitch": "A plain guide to the costs, the steps and the time a sale takes.",
                                "outline": ["The steps from listing to closing", "Transfer tax and closing costs",
                                            "Disclosures the seller completes", "How long a sale takes"]},
                "targeting_reason": f"The ad reaches everyone {context['ad_area']}, by place only."}
    if task == "probe.mask_roundtrip":
        return {"reply": "Hello [BUYER_1], thanks for asking. The house has 3 bedrooms.", "tokens_seen": ["[BUYER_1]"]}
    raise KeyError(f"no fake output for task {task}")
