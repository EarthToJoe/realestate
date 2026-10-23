"""The one-page flyer as HTML and as a PDF (WeasyPrint, try-first check T1). The DEMONSTRATION mark is printed
in the page margin of every page (CSS @page), in the body, and as a diagonal watermark, so no page of the flyer
can be shown without it (spec section 0, point 3). No photos: none are taken yet and portal photos are never used."""

from __future__ import annotations

from app.brokerage import brokerage
from app.models import CopyArtifact, Deal
from app.modules.listing_copy.service import DEMO_MARK, parse_flyer
from app.web import templates


def flyer_html(deal: Deal, art: CopyArtifact) -> str:
    return templates.get_template("copy/flyer_print.html").render(
        deal=deal, art=art, flyer=parse_flyer(art.text), firm=brokerage(), demo_mark=DEMO_MARK)


def flyer_pdf(deal: Deal, art: CopyArtifact) -> bytes:
    from weasyprint import HTML

    return HTML(string=flyer_html(deal, art)).write_pdf()
