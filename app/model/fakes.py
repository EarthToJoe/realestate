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
    if task == "probe.mask_roundtrip":
        return {"reply": "Hello [BUYER_1], thanks for asking. The house has 3 bedrooms.", "tokens_seen": ["[BUYER_1]"]}
    raise KeyError(f"no fake output for task {task}")
