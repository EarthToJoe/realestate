"""The review site publisher (scripts/publish_review.py): every internal link and anchor on the published pages
works, no link is left pointing at a raw .md file, and the index opens with the newcomer's "Start here" block.

Needs the markdown package, which only the publisher's uv run supplies; run it with
  uv run --no-project --with 'markdown==3.7' --with pytest python3 -m pytest tests/test_publish_review.py
"""

from __future__ import annotations

import importlib.util
import re
import sys

import pytest

from app.config import ROOT

pytest.importorskip("markdown")


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    out = tmp_path_factory.mktemp("site")
    argv = sys.argv
    sys.argv = ["publish_review.py", str(out)]
    try:
        spec = importlib.util.spec_from_file_location("publish_review_run", ROOT / "scripts" / "publish_review.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.main()
    finally:
        sys.argv = argv
    return mod, out


def test_no_broken_internal_links_or_anchors(site, capsys):
    mod, out = site
    written = {p.name for p in out.glob("*.html")}
    problems = mod.check(out, written)
    assert not problems, "\n".join(problems)


def test_no_link_left_pointing_at_a_markdown_file(site):
    _, out = site
    for page in out.glob("*.html"):
        hrefs = re.findall(r'href="([^"#]*\.md)(?:#[^"]*)?"', page.read_text())
        local = [h for h in hrefs if not h.startswith(("http://", "https://"))]
        assert not local, f"{page.name} links to raw .md files: {local}"


def test_index_starts_with_demo_summary_and_memo(site):
    _, out = site
    text = (out / "index.html").read_text()
    start = text.split('class="start"', 1)[1].split("</ol>", 1)[0]
    hrefs = re.findall(r'href="([^"]+)"', start)
    assert hrefs == ["/", "docs-executive-summary.html", "docs-research-memo-father-in-law.html"]
    assert text.index('class="start"') < text.index("Waiting on you") < text.index("How this was built")


def test_every_page_has_a_way_back_at_top_and_bottom(site):
    _, out = site
    for page in out.glob("*.html"):
        if page.name != "index.html":
            assert page.read_text().count('href="index.html"') >= 2, page.name
