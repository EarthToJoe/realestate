"""The road from the signed contract to closing: the planned records the timeline shows (CP-20 to CP-23, CP-34).

Each item is one planned record, written at intake so the timeline shows the whole sale from the start, and dated
on the timeline from the signed contract's terms once there is one. Who acts is a third party, except CP-34, a
planned "NY law today" marker (negotiating repairs is a broker's act; changing the contract is a lawyer's).
`days` is counted from the contract's signing; `from_terms` takes it from the agreed offer instead (inspection,
mortgage commitment, closing), with an offset.
"""

from __future__ import annotations

# (code, key, what, who, days after signing, or (term, offset) from the agreed terms)
ROAD = [
    ("CP-20", "escrow", "Deposit into escrow", "Escrow holder (by custom, the seller's attorney)", 3, None),
    ("CP-21", "inspection", "Home inspection", "Licensed home inspector", None, ("inspection_days", 0)),
    ("CP-34", "repairs", "Repairs or credits after the inspection, written into the contract",
     "The AI today; NY law: a licensed broker negotiates, a lawyer amends the contract", None,
     ("inspection_days", 3)),
    ("CP-22", "appraisal", "Appraisal", "Licensed appraiser, ordered by the lender", None, ("mortgage_days", -10)),
    ("CP-22", "mortgage", "Mortgage commitment", "The buyer's lender", None, ("mortgage_days", 0)),
    ("CP-22", "title", "Title search and title insurance", "Title company", None, ("closing_days", -14)),
    ("CP-23", "walkthrough", "Final walkthrough", "The buyer; the owner opens the door", None, ("closing_days", -1)),
    ("CP-23", "closing", "Closing: the deed signed in ink before a notary; the fee paid",
     "Title company, lender, notary; the parties", None, ("closing_days", 0)),
]
BY_KEY = {key: (code, key, what, who, days, rel) for code, key, what, who, days, rel in ROAD}
