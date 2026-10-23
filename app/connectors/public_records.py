"""`PublicRecordConnector`: property facts from public records.

The POC implementation, `FixtureRecords`, reads fixtures/demo_house.json (official records gathered by hand,
public records only, no owner name). A real connector (Open NY assessment rolls, NYS parcels, FEMA) would
return the same `RecordFact` list, so no screen changes.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from app.config import ROOT

FIXTURE = ROOT / "fixtures" / "demo_house.json"


@dataclass
class RecordFact:
    field: str
    label: str
    group: str
    value: str | None
    source: str  # public_record | inferred | gap
    source_ref: str | None = None
    confidence: str | None = None
    inferred_reason: str | None = None


@dataclass
class RecordLookup:
    found: bool
    address: dict
    facts: list[RecordFact]
    gaps: list[dict]
    sources: dict


class PublicRecordConnector(Protocol):
    def lookup(self, street: str, city: str, zip_code: str | None) -> RecordLookup: ...


def _money(v) -> str:
    return f"${v:,.0f}"


def _yes_no(v) -> str:
    return "Yes" if v else "No"


# (fixture key, field name (RESO-style), label, group, formatter)
FIELD_MAP = [
    ("parcel_id", "ParcelNumber", "Parcel ID (SWIS, print key)", "Location", None),
    ("property_class", "PropertyClass", "Property class", "Location", lambda v, e: f"{v} {e.get('description', '')}"),
    ("school_district", "SchoolDistrict", "School district (name only)", "Location", None),
    ("zoning", "Zoning", "Zoning", "Location", lambda v, e: f"{v}, {e.get('description', '')}".strip(", ")),
    ("flood_zone", "FloodZone", "FEMA flood zone", "Location", lambda v, e: f"Zone {v}: {e.get('description', '')}"),
    ("property_type", "PropertySubType", "Property type", "Structure", None),
    ("building_style", "ArchitecturalStyle", "Building style", "Structure", None),
    ("year_built", "YearBuilt", "Year built", "Structure", None),
    ("living_area_sqft", "LivingArea", "Living area (sq ft)", "Structure", lambda v, e: f"{v:,}"),
    ("basement", "Basement", "Basement", "Structure", None),
    ("finished_basement_sqft", "BelowGradeFinishedArea", "Finished basement (sq ft)", "Structure", lambda v, e: f"{v:,}"),
    ("stories", "Stories", "Stories", "Structure", lambda v, e: f"{v:g}"),
    ("bedrooms", "BedroomsTotal", "Bedrooms", "Structure", None),
    ("bathrooms_full", "BathroomsFull", "Full bathrooms", "Structure", None),
    ("bathrooms_half", "BathroomsHalf", "Half bathrooms", "Structure", None),
    ("kitchens", "Kitchens", "Kitchens", "Structure", None),
    ("fireplaces", "FireplacesTotal", "Fireplaces", "Structure", None),
    ("quality_grade", "QualityGrade", "Assessor's quality grade", "Structure", None),
    ("condition", "AssessorCondition", "Assessor's condition rating", "Structure", None),
    ("heating", "Heating", "Heating", "Systems", None),
    ("heating_fuel", "HeatingFuel", "Heating fuel", "Systems", None),
    ("central_air", "Cooling", "Central air", "Systems", lambda v, e: "None recorded" if v is False else _yes_no(v)),
    ("water_supply", "WaterSource", "Water", "Systems", None),
    ("sewer", "Sewer", "Sewer", "Systems", None),
    ("utilities", "Utilities", "Utilities", "Systems", None),
    ("lot_acres", "LotSizeAcres", "Lot size (acres)", "Land", None),
    ("improvements", "OtherStructures", "Other structures", "Land",
     lambda v, e: "; ".join(f"{i['structure']} {i['sqft']} sq ft ({i['year_built']})" for i in v)),
    ("mapped_wetlands_and_water", "WaterfrontFeatures", "Mapped water and wetlands", "Land",
     lambda v, e: (f"No state wetland on the parcel; a pond of about {v['pond_acres']} acres at the lot's edge, "
                   f"about {v['pond_share_inside_parcel_pct']}% inside the mapped lot lines")),
    ("agricultural_district", "AgriculturalDistrict", "Agricultural district", "Records", lambda v, e: v or "None"),
    ("condominium", "Condominium", "Condominium", "Records", lambda v, e: _yes_no(v)),
    ("assessments", "AssessedValue", "Assessed value (2026 final roll)", "Records",
     lambda v, e: f"{_money(v[0]['total_av'])} (land {_money(v[0]['land_av'])})"),
    ("assessments", "FullMarketValueState", "State full market value (formula, not an appraisal)", "Records",
     lambda v, e: f"{_money(v[0]['full_market_value'])} at {v[0]['equalization_rate_pct']}% equalisation"),
    ("last_recorded_transfer", "LastTransfer", "Last recorded transfer", "Records",
     lambda v, e: f"{v['date']}, ${v['price']:,}, code {v['condition_code']} ({v['condition_meaning']}): not a market sale"),
]

# Gaps the seller fills on the intake form: field -> (label, group).
SELLER_FIELDS = {
    "parking": ("ParkingFeatures", "Parking / garage", "Structure"),
    "condition": ("ConditionUpdates", "Condition and updates", "Structure"),
    "roof_year": ("RoofYear", "Roof installed (year)", "Systems"),
    "oil_tank": ("OilTank", "Oil tank", "Systems"),
    "annual_tax_bill": ("TaxAnnualAmount", "Annual property tax bill", "Records"),
    "hoa": ("AssociationYN", "Homeowners' association", "Records"),
    "other": ("SellerNotes", "Other facts from the seller", "Land"),
}


def normalise_street(street: str) -> str:
    s = street.lower().strip()
    s = re.sub(r"[.,#]", " ", s)
    s = re.sub(r"\b(route|rte|rt|state route|nys route|ny)\b", "route", s)
    s = re.sub(r"\broute\s+route\b", "route", s)
    return re.sub(r"\s+", " ", s).strip()


class FixtureRecords:
    """Reads the demo-house fixture. Any other address returns found=False (no real lookups in the POC)."""

    def __init__(self, path: Path = FIXTURE):
        self.data = json.loads(path.read_text())

    def _source_ref(self, src) -> str | None:
        keys = src if isinstance(src, list) else [src] if src else []
        names = []
        for k in keys:
            meta = self.data["sources"].get(k)
            if meta:
                names.append(f"{meta['name']} ({meta.get('url', '')}, read {meta.get('accessed', '')})")
        return "; ".join(names) or None

    def matches(self, street: str, zip_code: str | None) -> bool:
        target = normalise_street(self.data["property"]["address"]["street"]["value"])
        zip_ok = not zip_code or zip_code.strip()[:5] == self.data["property"]["address"]["zip"]["value"]
        return normalise_street(street) == target and zip_ok

    def lookup(self, street: str, city: str, zip_code: str | None) -> RecordLookup:
        if not self.matches(street, zip_code):
            return RecordLookup(found=False, address={"street": street, "city": city, "zip": zip_code}, facts=[],
                                gaps=[], sources={})
        p = self.data["property"]
        a = p["address"]
        facts: list[RecordFact] = []
        for key, field, label, group, fmt in FIELD_MAP:
            e = p[key]
            v = e.get("value")
            if v is None and e.get("provenance") == "not_in_record":
                continue
            value = fmt(v, e) if fmt else (str(v) if v is not None else None)
            prov = e.get("provenance")
            source = "inferred" if prov == "inferred" else "public_record"
            facts.append(RecordFact(field=field, label=label, group=group, value=value, source=source,
                                    source_ref=self._source_ref(e.get("source")),
                                    confidence="high" if source == "public_record" else "medium",
                                    inferred_reason=e.get("note") if source == "inferred" else None))
        address = {"street": a["street"]["value"], "city": a["postal_city"]["value"], "zip": a["zip"]["value"],
                   "county": a["county"]["value"], "municipality": a["municipality"]["value"],
                   "hamlet": a["hamlet"]["value"], "latitude": a["latitude"]["value"],
                   "longitude": a["longitude"]["value"], "upi": p["parcel_id"]["value"]}
        return RecordLookup(found=True, address=address, facts=facts, gaps=self.data["gaps"],
                            sources=self.data["sources"])

    def year_built(self) -> int:
        return int(self.data["property"]["year_built"]["value"])

    def in_ag_district(self) -> bool:
        return bool(self.data["property"]["agricultural_district"]["value"])
