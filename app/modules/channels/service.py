"""Step 4 Marketing plan: the channel board (spec section 3, step 4). No model call: every card's status comes
from the connector stubs and the records, so each one says honestly what happens and who does it.

- CP-07: the seller signs the listing-exposure choice and the authorisations (cooperating brokers, lockbox,
  photographer). The MLS entry waits for it.
- CP-08 "human required": OneKey MLS has no listing-input API; a licensed MLS participant (or registered
  Administrative User) keys the listing from the AI's package (`StubMLS.submit` says so). The Presenter records a
  simulated completion; the portal and website cards read it.
- Portals are "fed from the MLS" (`SimulatedPortals`); the firm's website is held by the Clear Cooperation clock.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.connectors.mls import StubMLS
from app.connectors.portals import SimulatedPortals
from app.models import Deal
from app.modules.listing_copy import service as copy_service
from app.records import catalogue
from app.records import service as records

WS3 = catalogue.load()["CP-08"].link
EXPOSURES = {
    "Publish to Internet": "MLS and every portal and public site (the usual choice)",
    "MLS Only": "Other MLS members see it; no portals or public sites",
    "Private / office exclusive": "Not in the MLS; only this firm markets it (needs the seller's signed choice)",
}
AUTHORISATIONS = [
    ("cooperating_brokers", "Cooperating brokers may show and sell the listing", "OneKey Rule 319.4"),
    ("lockbox", "A lockbox may be placed on the house", "OneKey Rule 405.4"),
    ("photographer", "A licensed photographer may photograph the house; photo rights stay with the firm",
     "OneKey Rule 603"),
]


def open_authorisations(s: Session, deal: Deal):
    records.require(s, deal.id, "CP-03", action="plan the marketing (no marketing before the listing agreement, L9)")
    existing = records.latest(s, deal.id, "CP-07")
    if existing and existing.status == "done":
        return existing
    return records.open_decision(s, deal.id, "CP-07", attached_to="channels:authorisations")


def sign_authorisations(s: Session, deal: Deal, persona: str, decision: str, exposure: str, granted: list[str]):
    cp = open_authorisations(s, deal)
    if decision == "sign" and exposure not in EXPOSURES:
        raise ValueError("Choose how widely the listing is shown.")
    names = [label for key, label, _ in AUTHORISATIONS if key in granted]
    reason = (f"Exposure: {exposure}. Authorised: " + ("; ".join(names) if names else "none")
              if decision == "sign" else "The seller declined to sign the marketing authorisations")
    return records.decide(s, cp, persona=persona, decision=decision, reason=reason)


def exposure_choice(s: Session, deal: Deal) -> str | None:
    cp = records.latest(s, deal.id, "CP-07")
    if not cp or cp.status != "done" or not cp.reason:
        return None
    return cp.reason.split(".")[0].replace("Exposure: ", "")


def ready_channels(s: Session, deal: Deal) -> set[str]:
    return {a.channel for a in copy_service.artifacts(s, deal) if a.status == "ready"}


def record_mls_entry(s: Session, deal: Deal):
    """The Presenter records the simulated human step. Needs the seller's authorisations (CP-07) and the remarks
    marked ready to publish; the package carries everything else."""
    records.require(s, deal.id, "CP-07", action="record the MLS entry (the seller signs the authorisations first)")
    if "mls_remarks" not in ready_channels(s, deal):
        raise records.GateError("CP-06", "Cannot record the MLS entry: the MLS public remarks are not marked ready "
                                         "to publish yet (step 3).")
    if exposure_choice(s, deal) == "Private / office exclusive":
        raise records.GateError("CP-07", "The seller chose an office-exclusive listing: it is not keyed into the MLS.")
    existing = records.latest(s, deal.id, "CP-08")
    if existing:
        return existing
    hr = StubMLS().submit(copy_service.mls_package(s, deal))
    return records.record_human(s, deal.id, "CP-08", reason=(
        f"Simulated: a licensed MLS participant keyed the listing into {hr.tool} from the AI's package"))


def board(s: Session, deal: Deal) -> list[dict]:
    cp07 = records.latest(s, deal.id, "CP-07")
    cp08 = records.latest(s, deal.id, "CP-08")
    exposure = exposure_choice(s, deal)
    entered_at = cp08.created_at if cp08 else None
    ready = ready_channels(s, deal)
    package = copy_service.mls_package(s, deal)
    missing = [r["label"] for r in package if r["required"] and not r["ok"]]
    hr = StubMLS().submit(package)
    cards = []

    if cp08:
        mls_status = "keyed in (simulated)"
    elif not cp07 or cp07.status != "done":
        mls_status = "waiting for the seller's authorisations (CP-07)"
    elif "mls_remarks" not in ready:
        mls_status = "waiting for the remarks to be marked ready (step 3)"
    else:
        mls_status = "package ready; waiting for a licensed MLS participant to key it"
    cards.append({"id": "mls", "name": "OneKey MLS", "kind": "human_required", "status": mls_status, "cp": cp08,
                  "code": "CP-08",
                  "detail": f"{hr.reason} Tool: {hr.tool}. The AI prepared the package in OneKey order; missing: "
                            f"{', '.join(missing) if missing else 'nothing'}.",
                  "ids": list(hr.f_ids) + list(hr.l_ids) + list(hr.ws3_ids), "link": hr.link,
                  "action": None if cp08 else "mls"})
    for ps in SimulatedPortals().status(entered_at, exposure):
        cards.append({"id": ps.ws3_id, "name": ps.name, "kind": "fed", "status": ps.status, "detail": ps.detail,
                      "human_step": ps.human_step, "ids": [ps.ws3_id], "link": WS3})
    if exposure and exposure != "Publish to Internet":
        web_status, web_detail = "not shown", f"The seller chose \"{exposure}\"."
    elif cp08:
        web_status, web_detail = "published (simulated)", "The MLS entry is recorded, so the firm's own page may go live."
    else:
        web_status, web_detail = ("held by the Clear Cooperation clock",
                                  "No public page until the MLS entry is recorded; once any public marketing starts, "
                                  "OneKey requires the MLS entry within one business day (Rule 302.2; fines $2,500 "
                                  "plus $100 a day).")
    cards.append({"id": "web", "name": "The firm's website", "kind": "automated", "status": web_status,
                  "detail": web_detail, "ids": ["WS3-C13", "WS3-R1"], "link": WS3})
    social_ready = sorted(c for c in ready if c.startswith("social_"))
    if not social_ready:
        social_status = "waiting for posts marked ready (step 3)"
    elif cp08:
        social_status = f"{len(social_ready)} post(s) drafted and scheduled (simulated)"
    else:
        social_status = f"{len(social_ready)} post(s) drafted; scheduled to follow the MLS entry"
    cards.append({"id": "social", "name": "Social: Facebook, Instagram, Nextdoor", "kind": "automated",
                  "status": social_status,
                  "detail": "Fair-housing checked in step 3. Posting is a person's job on these platforms: platform "
                            "rules forbid automated posting (Craigslist) and Marketplace listings from business pages "
                            "(Meta).", "human_step": "A person posts from the scheduled drafts",
                  "ids": ["WS3-C15"], "link": WS3})
    cards.append({"id": "gbp", "name": "Google Business Profile", "kind": "automated",
                  "status": "draft post ready (stub)" if "portal" in ready else "waiting for copy (step 3)",
                  "detail": "The AI drafts the post from the portal description; posting by API is optional and "
                            "stubbed in the demo.", "ids": ["WS3-C14"], "link": WS3})
    auth = (cp07.reason or "") if cp07 and cp07.status == "done" else ""
    for cid, name, needs, detail in (
        ("photos", "Photos", "photographer", "A licensed photographer (OneKey Rule 603); AI-altered images are "
                                              "labelled; no portal or other brokers' photos are ever used (WS3-R8)."),
        ("sign", "Yard sign", None, "Sign vendor installs; the sign names the firm (L10)."),
        ("lockbox", "Lockbox", "lockbox", "Needs the seller's lockbox authorisation (OneKey Rule 405.4); keys and "
                                          "PINs may not be lent (Rule 405.8)."),
    ):
        ok = needs is None or (needs == "photographer" and "photographer" in auth) or (needs == "lockbox" and "lockbox" in auth)
        cards.append({"id": cid, "name": name, "kind": "vendor",
                      "status": "vendor booking (simulated)" if ok else "waiting for the seller's authorisation (CP-07)",
                      "detail": detail, "ids": ["WS3-R3", "WS3-R8"] if cid == "photos" else ["WS3-R3"], "link": WS3})
    cards.append({"id": "open_house", "name": "Open house", "kind": "owner", "status": "owner hosts (step 5)",
                  "detail": "Someone must open the door; the owner may show their own home (CP-10, step 5).",
                  "ids": ["F39", "F40", "L19", "WS3-R4"], "link": WS3})
    return cards
