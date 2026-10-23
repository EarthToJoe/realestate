"""Step 5 of the path, The listing (decision 51): the AI's copy with its fair-housing checks and the MLS pre-check and
package, on one screen; the flyer. Every action redirects back to the screen (Post/Redirect/Get)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, Response

from app.db import get_session
from app.demo import path
from app.fairhousing import check as fh
from app.model.provider import ReplayMiss, SpendCapReached
from app.modules.listing_copy import pdf, service
from app.records import service as records
from app.records.service import GateError
from app.web import current_deal, gate_page, redirect, render

router = APIRouter()


def _gate(s, deal) -> str | None:
    try:
        records.require(s, deal.id, "CP-03", action="write listing copy (no marketing before the listing agreement, L9)")
        records.require(s, deal.id, "CP-05", action="write listing copy (the seller chooses the list price first)")
    except GateError as e:
        return e.message
    return None


def _panel(s, art) -> dict:
    res = fh.latest_result(s, "copy_artifact", art.id)
    current = res is not None and res.version == art.version and res.text_hash == fh.text_hash(art.text)
    return {"art": art, "res": res if current else None,
            "marked": service.highlight(art.text, res.findings) if current and res.findings else None,
            "mls_checks": service.remarks_checks(art.text) if art.channel == "mls_remarks" else None,
            "flyer": service.parse_flyer(art.text) if art.channel == "flyer" else None}


@router.get("/copy")
def listing(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    gate = _gate(s, deal)
    arts = [] if gate else service.artifacts(s, deal)
    remarks = next((a for a in arts if a.channel == "mls_remarks"), None)
    res = fh.latest_result(s, "copy_artifact", remarks.id) if remarks else None
    return render(request, s, "copy/listing.html", gate=gate, panels=[_panel(s, a) for a in arts],
                  rules_version=fh.load_rules().version, cp06=records.records(s, deal.id, "CP-06"),
                  planted=service.PLANTED, remarks=remarks,
                  checks=service.remarks_checks(remarks.text) if remarks else [], fh_res=res,
                  package=service.mls_package(s, deal) if arts else [])


def _deal_or_gone(s):
    deal = current_deal(s)
    return deal, (None if deal else RedirectResponse("/intake", status_code=303))


@router.post("/copy/draft")
def draft(request: Request, s=Depends(get_session)):
    deal, gone = _deal_or_gone(s)
    if gone:
        return gone
    provider = request.app.state.provider
    try:
        service.draft(s, deal, provider)
    except (ReplayMiss, SpendCapReached) as e:
        s.rollback()
        return redirect("/copy", path.plain_failure(e, provider.mode == "replay"))
    return redirect("/copy", "The AI wrote the listing and checked every piece for fair housing.")


ACTION_DONE = {"check": "The AI checked {t} again", "plant": "Planted a violation in {t}: the check caught it",
               "fix": "The AI applied the fix to {t} and checked it again", "ready": "The AI marked {t} ready to publish"}


@router.post("/copy/{artifact_id}/{action}")
def artifact_action(artifact_id: int, action: str, request: Request, s=Depends(get_session)):
    if action not in ACTION_DONE:
        return Response(status_code=404)
    deal, gone = _deal_or_gone(s)
    if gone:
        return gone
    gate = _gate(s, deal)
    if gate:
        raise GateError("CP-05", gate)
    art = service.get(s, deal, artifact_id)
    provider = request.app.state.provider
    was_ready = art.status == "ready"
    if action == "ready":  # refused (409, in plain words) unless the newest check passed on this exact text
        service.mark_ready(s, deal, art)
    else:
        try:
            {"check": service.check, "plant": service.plant, "fix": service.apply_fix}[action](s, deal, art, provider)
        except (ValueError, ReplayMiss, SpendCapReached) as e:
            s.rollback()
            return redirect(f"/copy#art-{artifact_id}", path.plain_failure(e, provider.mode == "replay"))
    flash = ACTION_DONE[action].format(t=art.title.lower() if art.title[:3] != "MLS" else art.title)
    if action == "check":
        flash += ": it still passes and stays ready to publish" if was_ready and art.status == "ready" else (
            ": it passes" if art.status == "passed" else ": it is blocked until fixed")
    elif action in ("plant", "fix") and art.status != "ready":
        flash += (". The text changed, so it needs marking ready again" if art.status == "passed" else "")
    return redirect(f"/copy#art-{artifact_id}", flash + ".")


@router.post("/copy/ready-all")
def ready_all(request: Request, s=Depends(get_session)):
    deal, gone = _deal_or_gone(s)
    if gone:
        return gone
    gate = _gate(s, deal)
    if gate:
        raise GateError("CP-05", gate)
    done, refused = service.mark_all_ready(s, deal)
    flash = f"The AI marked {len(done)} piece{'s' if len(done) != 1 else ''} ready to publish"
    if refused:
        flash += "; not " + ", ".join(a.title.lower() for a, _ in refused) + ": its check has not passed"
    return redirect("/copy", flash + ".")


@router.get("/copy/flyer")
def flyer_html(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    art = next((a for a in service.artifacts(s, deal) if a.channel == "flyer"), None) if deal else None
    if art is None:
        return RedirectResponse("/copy", status_code=303)
    return Response(pdf.flyer_html(deal, art), media_type="text/html")


@router.get("/copy/flyer.pdf")
def flyer_pdf(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    art = next((a for a in service.artifacts(s, deal) if a.channel == "flyer"), None) if deal else None
    if art is None:
        return RedirectResponse("/copy", status_code=303)
    return Response(pdf.flyer_pdf(deal, art), media_type="application/pdf",
                    headers={"Content-Disposition": 'inline; filename="flyer-DEMONSTRATION.pdf"'})
