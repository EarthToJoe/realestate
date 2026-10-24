"""The path's own endpoints (decisions 47 to 50): the generic action behind the action bar's buttons, "Change",
starting and resetting the sale, the presenter's tools (presenting on or off, "Do this screen for me", skip ahead)
and the redirects that keep old screens' links working."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse

from app import db
from app.db import get_session
from app.demo import path, walk
from app.logging_setup import log
from app.records.service import NotYourDecision
from app.web import (COOKIE, PRESENTING_COOKIE, YEAR, actor, current_deal, presenting, redirect, render, screen_for,
                     stops)

router = APIRouter()


def local(url: str | None, default: str = "/") -> str:
    return url if url and url.startswith("/") and not url.startswith("//") else default


# ---- starting -------------------------------------------------------------------------------------------------

@router.get("/demo/start")
def demo_start(request: Request, back: str = "/", s=Depends(get_session)):
    """Start: a first visit goes straight in; with a sale in progress it asks first (fresh-eyes audit 12)."""
    if current_deal(s) is None:
        return RedirectResponse("/intake", status_code=303)
    return render(request, s, "demo_start.html", back=local(back))


@router.post("/demo/reset")
def demo_reset():
    """Start over: rebuild the database from the seed (the spend log is kept) and open step 1."""
    db.reset_all()
    log.info("demo_reset")
    resp = redirect("/intake", "The sale is reset. The demo house is filled in: press Save and continue.")
    resp.set_cookie(COOKIE, "presenter", httponly=True, samesite="lax")
    return resp


@router.post("/demo/presenting")
def demo_presenting(on: str = Form("on"), back: str = Form("/")):
    """"I'm presenting" (decision 50): the presenter's tools on this device, remembered for a year."""
    resp = redirect(local(back), "Presenting is on: the notes, Do this screen for me and skip ahead are in the menu."
                    if on == "on" else "Presenting is off.")
    if on == "on":
        resp.set_cookie(PRESENTING_COOKIE, "on", max_age=YEAR, httponly=True, samesite="lax")
    else:
        resp.delete_cookie(PRESENTING_COOKIE)
    return resp


# ---- the action bar ---------------------------------------------------------------------------------------------

DECIDED = {
    "agency": {"acknowledge": "The seller acknowledged the agency form",
               "refuse_with_declaration": "The seller refused the agency form, with a signed declaration"},
    "listing": {"sign": "The seller signed the listing agreement", "decline": "The seller declined the listing "
                "agreement"},
    "buyer_agreement": {"sign": "The buyer signed the buyer agreement", "decline": "The buyer declined the buyer "
                        "agreement"},
    "dual_agency": {"consent": "The {who} consented to dual agency", "decline": "The {who} declined dual agency"},
    "signed": {"sign": "The {who} signed the contract", "decline": "The {who} declined to sign"},
    "pcds": {"complete": "The seller submitted the disclosure form"},
}
AI_DONE = {"mls": "A person at the firm keyed the listing into the MLS (simulated)"}


def _decide(s, deal, key: str, who: str, choice: str) -> None:
    from app.disclosures import pcds
    from app.modules.buyer import service as buyer
    from app.modules.contract import service as contract
    from app.modules.intake import service as intake

    if key == "agency":
        intake.acknowledge_agency(s, deal, who, choice or "acknowledge")
    elif key == "listing":
        intake.sign_listing_agreement(s, deal, who, choice or "sign")
    elif key == "buyer_agreement":
        buyer.sign_agreement(s, deal, who, choice or "sign")
    elif key == "dual_agency":
        buyer.consent_dual_agency(s, deal, who, choice or "consent")
    elif key == "signed":
        contract.sign(s, deal, who, choice or "sign")
    elif key == "pcds":
        pcds.submit(s, deal, who, pcds.prepared_answers(), prepared=True)
    else:
        raise ValueError("That decision is made on its own form on the screen.")


@router.post("/path/act/{key}")
async def act(key: str, request: Request, s=Depends(get_session)):
    """One button of the action bar: an AI act, a person's simulated act, or a client's decision recorded as the
    client the button names. The AI's own acts never record a client decision (decision 49)."""
    m = walk.BY_KEY.get(key)
    if m is None:
        return RedirectResponse("/", status_code=303)
    deal = current_deal(s)
    if deal is None:
        return redirect("/intake", "Start with step 1: the seller signs up.")
    form = await request.form()
    provider = request.app.state.provider
    firm = m.route == "/brand"
    ai_turn = m.who == "ai" or (key == "agreed" and walk.negotiation_next(s, deal) in ("seller_ai", "buyer_ai"))
    if ai_turn or m.who == "person":
        if walk.is_done(s, deal, m):
            return redirect(m.route)
        try:
            walk._negotiate_ai(s, deal, provider) if key == "agreed" else m.play(s, deal, provider)
            s.commit()
        except Exception as e:  # noqa: BLE001 (said in plain words; nothing is lost)
            s.rollback()
            return redirect(m.route, path.plain_failure(e, provider.mode == "replay"))
        did = path.did_text([key], s, current_deal(s))
        done = AI_DONE.get(key) or (did[:1].upper() + did[1:])
        return redirect(m.route, path.after_action(s, provider, done, firm=firm))
    who = actor(request, form)
    choice = str(form.get("choice") or "")
    _decide(s, deal, key, who, choice)
    text = DECIDED.get(key, {}).get(choice) or next(iter(DECIDED.get(key, {"": "Saved"}).values()))
    return redirect(m.route, path.after_action(s, provider, text.format(who=who)))


# ---- Change (decision 48) -----------------------------------------------------------------------------------

@router.get("/path/change/{key}")
def change_confirm(key: str, request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None or key not in path.CHANGEABLE:
        return RedirectResponse("/", status_code=303)
    m = walk.BY_KEY[key]
    return render(request, s, "change.html", key=key, m=m, label=path.CHANGE_LABEL[key],
                  reopens=path.change_plan(s, deal, key), reopens_text=path.reopens_text(path.change_plan(s, deal, key)),
                  back=m.link)


@router.post("/path/change/{key}")
def change(key: str, request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None or key not in path.CHANGEABLE:
        return RedirectResponse("/", status_code=303)
    m = walk.BY_KEY[key]
    flash = path.apply_change(s, request.app.state.provider, deal, key)
    flash = path.after_action(s, request.app.state.provider, flash.rstrip("."))
    return redirect(m.link if m.key != "agreed" else "/offers#negotiation", flash)


# ---- the presenter's tools (decision 50) ---------------------------------------------------------------------

def _presenter_only(request: Request) -> None:
    if not presenting(request):
        raise NotYourDecision("This is one of the presenter's tools: turn on \"I'm presenting\" in the menu first.")


@router.post("/demo/play")
def demo_play(request: Request, route: str = Form(...), s=Depends(get_session)):
    """"Do this screen for me": plays this screen's steps the way the script does (recorded answers), each client
    decision recorded as the client's and marked "played by the demo"."""
    _presenter_only(request)
    st, _ = screen_for(route)
    if st is None:
        raise ValueError("That is not a screen of the demo.")
    played = walk.play_screen(s, request.app.state.provider, st["route"])
    log.info("demo_play", route=route, played=[m.key for m in played])
    return redirect(st["route"], f"The demo played this screen: {len(played)} step{'s' if len(played) != 1 else ''}"
                                 + (f" ({', '.join(m.what.lower() for m in played[-3:])})." if played else "."))


@router.post("/demo/skip")
def demo_skip(request: Request, route: str = Form(...), s=Depends(get_session)):
    """Skip ahead: play every step before this screen with the script's choices, then open it."""
    _presenter_only(request)
    st, _ = screen_for(route)
    if st is None:
        raise ValueError("That is not a screen of the demo.")
    played = walk.fast_forward(s, request.app.state.provider, st["route"])
    log.info("demo_skip", route=route, played=[m.key for m in played])
    return redirect(st["route"], f"Skipped ahead: the demo played {len(played)} earlier step"
                                 f"{'s' if len(played) != 1 else ''} with the script's choices.")


@router.get("/step/{n}")
def step_link(n: int):
    """A step by its number on the path (1 to 11), for links and the presenter."""
    st = next((x for x in stops() if x.get("n") == n), None)
    return RedirectResponse(st["route"] if st else "/", status_code=303)


@router.get("/demo/continue")
def resume(s=Depends(get_session)):
    """Pick up where the sale was left."""
    return RedirectResponse(path.resume_route(s, current_deal(s)), status_code=303)
