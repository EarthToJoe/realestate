"""The catalogue is the one source of record texts (spec section 3)."""

from collections import Counter

from app.config import ROOT
from app.records import catalogue


def test_counts_by_kind():
    kinds = Counter(e.kind for e in catalogue.load().values())
    assert len(catalogue.load()) == 35
    assert kinds == {"client_decision": 11, "law_marker": 13, "human_required": 3, "third_party": 4, "automated": 4}


def test_markers_and_human_required_are_complete():
    for code, e in catalogue.load().items():
        if e.kind in ("law_marker", "human_required"):
            assert e.rule.strip(), f"{code} has no rule sentence"
            assert e.who.strip(), f"{code} has no who"
            assert e.f_ids, f"{code} has no F-ID"
            assert e.l_ids or e.ws3_ids, f"{code} has no L-ID or WS3 ID"
            assert e.link.startswith("https://realestate.hughesnode.com/"), f"{code} link {e.link!r}"
        if e.kind == "law_marker":
            assert e.law_actor in ("L", "A", "L+A"), f"{code} law_actor"


def test_only_client_decisions_block():
    for e in catalogue.load().values():
        assert e.blocking == (e.kind == "client_decision")


def test_every_code_is_in_traceability():
    text = (ROOT / "docs" / "TRACEABILITY.md").read_text()
    missing = [code for code in catalogue.load() if code not in text]
    assert not missing, f"codes missing from docs/TRACEABILITY.md: {missing}"


def test_links_point_at_review_pages_that_publish_writes():
    import re

    from tests.scripts_publish import review_slugs

    slugs = review_slugs()
    for code, e in catalogue.load().items():
        page = re.sub(r"^https://realestate\.hughesnode\.com/", "", e.link)
        assert page in slugs, f"{code} links to {page}, which publish-review.sh does not write"
