"""People and their data: the PII screens (spec section 6). Not a step of the sale: the firm's own duty to the people
whose data it holds. Linked from the step list and the footer."""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, Response

from app.db import get_session
from app.modules.people import service
from app.web import current_deal, persona, render

router = APIRouter()


@router.get("/people")
def people(request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    who = persona(request)
    return render(request, s, "people/people.html", people=service.people(s, deal), may_view=service.may_view,
                  log=service.access_rows(s, limit=60) if who == "presenter" else [], retention=service.RETENTION)


@router.get("/people/{person_id}")
def person(person_id: int, request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    p = service.get(s, deal, person_id)
    vals = service.view(s, p, persona(request), request.url.path)
    return render(request, s, "people/person.html", p=p, vals=vals, log=service.access_rows(s, p.id),
                  retention=service.RETENTION, erased=service.ERASED)


@router.get("/people/{person_id}/export")
def export(person_id: int, request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    p = service.get(s, deal, person_id)
    data = service.export(s, deal, p, persona(request), request.url.path)
    return Response(json.dumps(data, indent=1, ensure_ascii=False), media_type="application/json",
                    headers={"Content-Disposition": f'attachment; filename="{p.role}-{p.id}-export.json"'})


@router.get("/people/{person_id}/delete")
def delete_confirm(person_id: int, request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    p = service.get(s, deal, person_id)
    service.require_view(persona(request), p)
    return render(request, s, "people/delete.html", p=p, retention=service.RETENTION)


@router.post("/people/{person_id}/delete")
def delete(person_id: int, request: Request, s=Depends(get_session)):
    deal = current_deal(s)
    p = service.get(s, deal, person_id)
    service.erase(s, p, persona(request))
    return RedirectResponse(f"/people/{p.id}", status_code=303)
