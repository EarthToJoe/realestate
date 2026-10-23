"""Step 9 screen: the deal timeline and hurdle map, from records only."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.db import get_session
from app.modules.timeline import service
from app.web import current_deal, gate_page, render

router = APIRouter()


@router.get("/timeline")
def timeline(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    if deal is None:
        return gate_page(request, s)
    return render(request, s, "timeline/timeline.html", tl=service.build(s, deal))
