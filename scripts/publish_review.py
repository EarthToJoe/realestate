"""Renders the repo's documents as phone-readable pages for Joe at https://realestate.hughesnode.com.

Run through scripts/publish-review.sh (which supplies the markdown package via uv). Reads docs/ and
research_notes/ from the repo, writes static HTML into the hughesnode app's public/ folder. Pages that do
not exist yet are listed as "being written", so the index always shows the whole project.

Links between documents are rewritten to their pages; a link to a document that is not published becomes plain
text. Every internal link and anchor is then checked, and anything left broken is printed as a WARNING
(tests/test_publish_review.py fails on any).
"""
import html
import os
import posixpath
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

import markdown

REPO = Path(__file__).resolve().parent.parent
TZ = "America/New_York"  # Joe reads in Eastern time
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/srv/hughesnode/apps/realestate/public")
DEMO = "/"  # the demo app answers at the site root; these pages keep their old addresses beside it
TOC_MIN_CHARS = 3000  # about three phone screens of text: longer pages get an "On this page" fold

# The first three things a newcomer (Joe's father-in-law, sent the index link) should open, in order.
START_HERE = [
    (DEMO, "Open the demo", "The AI agent selling a real Hudson Valley house, step by step"),
    ("docs/EXECUTIVE-SUMMARY.md", "The executive summary", "The idea, the findings and the plan on a few pages"),
    ("docs/research/memo-father-in-law.md", "The memo on your role",
     "Broker and lawyer in one deal; running a NY firm from out of state"),
]
WORKSTREAMS = ("WS1 to WS6 are the six research workstreams: WS1 what an agent does, WS2 legal and licensing, "
               "WS3 listing and data access, WS4 cost model, WS5 competitors, WS6 free inspection. "
               "WS7 is the search for ready-made parts to build the demo from.")

# (section, [(repo path, short title, one-line note)]); order is the order on the home page.
SECTIONS = [
    ("Waiting on you", [
        ("docs/SUCCESS-CRITERIA.md", "Demo finish line", "Reply SIGN-OFF in the chat, or say what to change"),
        ("docs/QUESTIONS-FOR-JOE.md", "Questions for Joe", "One line each; my default holds until you answer"),
    ]),
    ("The proposal", [
        ("docs/EXECUTIVE-SUMMARY.md", "Executive summary", "The short version: the idea, the findings, the plan"),
        ("docs/PLAN.md", "Project plan", "Phases, costs, open questions, human-in-the-loop map"),
        ("docs/research/memo-father-in-law.md", "Memo: the attorney-broker role", "Broker and lawyer in one deal; running a NY firm from out of state"),
        ("docs/DEMO-SCRIPT.md", "Demo walkthrough script", "What to click and say, screen by screen"),
        ("docs/specs/demo-house.md", "Demo house: 146 Rt 292, Holmes", "Official-record facts and nearby sales"),
    ]),
    ("Research", [
        ("docs/research/WS1-agent-functions.md", "WS1. What an agent does", "Every function, and whether software can do it"),
        ("docs/research/WS2-legal-licensing.md", "WS2. Legal and licensing hurdles", "Where a licence or a lawyer is required"),
        ("docs/research/WS3-listing-data-access.md", "WS3. Listing and data access", "MLS, Zillow, Redfin, Realtor.com: API or human?"),
        ("docs/research/WS4-cost-model.md", "WS4. Cost model", "Upfront, ongoing, break-even"),
        ("docs/research/WS5-competitors.md", "WS5. Competitors", "Who already does this, and can a local launch win"),
        ("docs/research/WS6-free-inspection.md", "WS6. Free inspection", "Pros, cons, liability"),
        ("docs/research/fact-check.md", "Fact-check of the reports", "Independent check of the key claims"),
    ]),
    ("Living documents", [
        ("docs/ASSUMPTIONS.md", "Riskiest assumptions", "Ranked, with kill criteria and status"),
        ("docs/DECISIONS.md", "Decision log", "Every choice and why"),
        ("docs/TRACEABILITY.md", "Traceability", "Each demo feature, the agent function and the law behind it"),
        ("docs/OUT-OF-SCOPE.md", "Out of scope", "What the demo will not do"),
        ("docs/BRIEF.md", "Your brief", "Verbatim, the source of truth"),
    ]),
    ("How this was built", [
        ("docs/PROGRESS.md", "Progress", "Daily summary, newest first"),
        ("docs/SPEND-LOG.md", "API spend", "Where the $200 credit went, per workstream"),
        ("docs/specs/poc-architecture.md", "Architecture plan", "How the demo is built, what it costs per run, build days"),
        ("docs/build/site-audit-2026-10-23.md", "Whole-site audit (evening)", "Why entries were lost, what is confusing, and the fix"),
        ("docs/build/audit-fresh-eyes-2026-10-23.md", "First-time visitor's audit", "A separate reviewer walks the site as three newcomers"),
        ("docs/build/ui-audit-2026-10-23.md", "Demo screens: audit", "What looks wrong and what the redesign fixes"),
    ] + [(f"docs/research/handoff/WS{n}.md", f"WS{n} handoff", "Assumption status lines and open items, as handed over")
         for n in range(1, 8)]),
]
NOTES_SECTION = "Research"  # the raw research notes fold sits at the end of this section
LABELS = {"PRIMARY": "p", "SECONDARY": "s", "CLAIMED": "c", "INFERENCE": "i"}

CSS = """
:root{--bg:#fbfaf7;--fg:#1d1d1b;--muted:#6b6a65;--line:#e4e1d9;--card:#fff;--accent:#1f5f8b;--warn:#8a5a00;
--p:#1e6b3a;--s:#30557a;--c:#8a5a00;--i:#6a3d8a;--code:#f2f0ea}
@media (prefers-color-scheme:dark){:root{--bg:#161614;--fg:#e9e7e1;--muted:#a19f98;--line:#33322e;--card:#1e1e1b;
--accent:#7db7e0;--warn:#e0b25a;--p:#7cc796;--s:#8fb4dc;--c:#e0b25a;--i:#c39be0;--code:#262622}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
main{max-width:46rem;margin:0 auto;padding:12px 16px 48px;overflow-wrap:break-word}
a{color:var(--accent)}h1{font-size:1.6rem;line-height:1.25;margin:.4em 0 .3em}
h2{font-size:1.25rem;margin:1.8em 0 .4em;line-height:1.3}h3{font-size:1.05rem;margin:1.4em 0 .3em}
h2,h3,h4{scroll-margin-top:12px}
.meta{color:var(--muted);font-size:.9rem}.meta code{font-size:.8rem}
.top,.bottom{font-size:1rem}.top a,.bottom a{display:inline-flex;align-items:center;min-height:44px;padding:0 16px 0 0}
.bottom{margin-top:40px;border-top:1px solid var(--line);padding-top:8px}
.tw{overflow-x:auto;margin:1em 0;border:1px solid var(--line);border-radius:8px}
table{border-collapse:collapse;font-size:1rem;min-width:100%}th,td{padding:6px 9px;border-bottom:1px solid var(--line);
text-align:left;vertical-align:top}th{background:var(--code)}
code{background:var(--code);padding:1px 4px;border-radius:4px;font-size:.88em;overflow-wrap:anywhere}
pre{background:var(--code);padding:12px;border-radius:8px;overflow-x:auto}pre code{padding:0}
blockquote{margin:1em 0;padding:.2em 1em;border-left:3px solid var(--line);color:var(--muted)}
.lab{font-size:.75rem;font-weight:600;letter-spacing:.03em;padding:1px 5px;border-radius:4px;border:1px solid currentColor;
white-space:nowrap}.lab.p{color:var(--p)}.lab.s{color:var(--s)}.lab.c{color:var(--c)}.lab.i{color:var(--i)}
.sec{margin-top:28px}.sec>h2{font-size:.9rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:0 0 8px}
.sec>p{margin:0 0 8px;color:var(--muted)}
.item{display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:8px 0;
text-decoration:none;color:var(--fg)}.item b{color:var(--accent)}.item span{display:block;color:var(--muted);font-size:1rem}
.item.pending{opacity:.55}.item.pending b{color:var(--muted)}.badge{float:right;font-size:.8rem;color:var(--muted)!important;
margin-left:8px}.item.wait{border-color:var(--warn)}
.start{border:2px solid var(--accent);border-radius:12px;padding:12px 14px;margin:16px 0 0;background:var(--card)}
.start h2{margin:0 0 4px;font-size:1.15rem}.start ol{margin:0;padding-left:1.4em}.start li{margin:2px 0}
.start li a{display:block;padding:8px 0;min-height:44px;text-decoration:none}.start li a b{text-decoration:underline}
.start li a span{display:block;color:var(--muted)}
details{margin:6px 0}summary{cursor:pointer;color:var(--accent);padding:10px 0;min-height:44px}
.toc{border:1px solid var(--line);border-radius:8px;padding:0 14px;margin:12px 0 20px;background:var(--card)}
.toc summary{font-weight:600}.toc ol{margin:0 0 10px;padding-left:1.4em}.toc li a{display:block;padding:9px 0;min-height:44px}
img{max-width:100%}hr{border:0;border-top:1px solid var(--line);margin:2em 0}
"""


def git_date(path: str = "", fmt: str = "%b %-d, %-I:%M %p ET") -> str:
    r = subprocess.run(["git", "-C", str(REPO), "log", "-1", "--format=%cd", f"--date=format-local:{fmt}",
                        "--", *([path] if path else [])], capture_output=True, text=True, env={**os.environ, "TZ": TZ})
    return r.stdout.strip() or "not yet committed"


def slug(path: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", Path(path).with_suffix("").as_posix().lower()).strip("-") + ".html"


def page(title: str, body: str, back: bool = True) -> str:
    nav = '<a href="index.html">&larr; All documents</a>'
    top = f'<div class="top">{nav}</div>' if back else ""
    bottom = f'<div class="bottom">{nav} <a href="#">Back to top</a></div>' if back else ""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">'
            f'<title>{html.escape(title)}</title><style>{CSS}</style></head><body><main>{top}{body}{bottom}'
            f'</main></body></html>')


def resolve(src: str, href: str, links: dict) -> str | None:
    """The repo path a relative link from the document `src` points at, if it is a repo file."""
    target = unquote(href.split("#")[0])
    if not target:
        return None
    joined = posixpath.normpath(posixpath.join(posixpath.dirname(src), target))
    if (REPO / joined).is_file():
        return joined
    bare = target.lstrip("./")  # written from the repo root ("docs/PLAN.md") or by bare name
    if (REPO / bare).is_file():
        return bare
    hits = [p for p in links if p.endswith("/" + bare)]
    return hits[0] if len(hits) == 1 else None


def relink(out: str, src: str, links: dict, warnings: list) -> str:
    """Point links between repo documents at their pages; unlink (keep the words) any to an unpublished file."""
    def fix(m):
        attrs, href, text = m.group(1), html.unescape(m.group(2)), m.group(3)
        if re.match(r"[a-z][a-z0-9+.-]*:|/|#", href):  # outside link, site-absolute, or in-page anchor
            return m.group(0)
        path = resolve(src, href, links)
        if path in links:
            frag = href.partition("#")[2]
            new = links[path] + ("#" + frag if frag else "")
            return f'<a{attrs.replace(m.group(2), html.escape(new))}>{text}</a>'
        warnings.append(f"{src}: unpublished target {href!r}, link removed (text kept)")
        return text
    return re.sub(r'<a( [^>]*?href="([^"]*)"[^>]*)>(.*?)</a>', fix, out, flags=re.S)


def render(md_text: str, src: str, links: dict, warnings: list) -> tuple[str, list]:
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc"])
    out = md.convert(md_text)
    out = out.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    out = re.sub(r"\[(PRIMARY|SECONDARY|CLAIMED|INFERENCE)\]",
                 lambda m: f'<span class="lab {LABELS[m.group(1)]}">{m.group(1)}</span>', out)
    h2s = []

    def walk(tokens):
        for t in tokens:
            if t["level"] == 2:
                h2s.append((t["id"], re.sub(r"<[^>]+>", "", html.unescape(t["name"]))))
            walk(t["children"])
    walk(md.toc_tokens)
    return relink(out, src, links, warnings), h2s


def toc(h2s: list) -> str:
    items = "".join(f'<li><a href="#{html.escape(i)}">{html.escape(name)}</a></li>' for i, name in h2s)
    return f'<details class="toc"><summary>On this page ({len(h2s)} sections)</summary><ol>{items}</ol></details>'


def check(out: Path, written: set) -> list:
    """Every internal link on the published pages opens a published page, and every anchor exists."""
    ids, hrefs = {}, {}
    for name in written:
        text = (out / name).read_text()
        ids[name] = set(re.findall(r'\bid="([^"]+)"', text))
        hrefs[name] = [html.unescape(h) for h in re.findall(r'\bhref="([^"]*)"', text)]
    problems = []
    for name, hs in hrefs.items():
        for h in hs:
            if re.match(r"[a-z][a-z0-9+.-]*:", h) or h in (DEMO, "#"):
                if re.match(r"https?://realestate\.hughesnode\.com/[^#?]*\.md\b", h):
                    problems.append(f"{name}: link to a raw .md file {h!r}")
                continue
            target, _, frag = h.partition("#")
            target = target or name
            if target.endswith(".md"):
                problems.append(f"{name}: link to a raw .md file {h!r}")
            elif target not in written:
                problems.append(f"{name}: link to a page that is not published {h!r}")
            elif frag and unquote(frag) not in ids[target]:
                problems.append(f"{name}: missing anchor {h!r}")
    return problems


def notes_title(path: str) -> str:
    h1 = re.search(r"^# (.+)$", (REPO / path).read_text(), re.M)
    return h1.group(1).strip() if h1 else Path(path).stem.replace("_", " ")


def card(path: str, short: str, note: str, links: dict, cls: str = "item") -> str:
    if path in links:
        return (f'<a class="{cls}" href="{links[path]}"><span class="badge">{git_date(path)}</span>'
                f'<b>{html.escape(short)}</b><span>{html.escape(note)}</span></a>')
    return (f'<div class="item pending"><span class="badge">being written</span>'
            f'<b>{html.escape(short)}</b><span>{html.escape(note)}</span></div>')


def index(notes: list, links: dict) -> str:
    head = subprocess.run(["git", "-C", str(REPO), "log", "-1", "--format=%h"], capture_output=True, text=True).stdout.strip()
    parts = ['<h1>AI real estate agent: the demo and the research</h1>',
             f'<p class="meta">Updated {git_date(fmt="%b %-d, %Y, %-I:%M %p ET")} &middot; <code>{html.escape(head)}</code></p>',
             '<div class="start"><h2>Start here</h2><ol>']
    for path, short, note in START_HERE:
        href = path if path == DEMO else links.get(path)
        if href:
            parts.append(f'<li><a href="{href}"><b>{html.escape(short)}</b><span>{html.escape(note)}</span></a></li>')
    parts.append("</ol></div>")
    for section, items in SECTIONS:
        parts.append(f'<div class="sec"><h2>{section}</h2>')
        if section == "Waiting on you":
            parts.append("<p>Joe's own to-do list for this project; visitors can skip it.</p>")
        if section == NOTES_SECTION:
            parts.append(f"<p>{html.escape(WORKSTREAMS)}</p>")
        for path, short, note in items:
            parts.append(card(path, short, note, links, "item wait" if section == "Waiting on you" else "item"))
        if section == NOTES_SECTION:
            parts.append(f'<details><summary>Raw research notes: {len(notes)} files, every claim sourced and labelled'
                         '</summary>')
            for path in notes:
                parts.append(f'<a class="item" href="{links[path]}"><b>{html.escape(notes_title(path))}</b>'
                             f'<span>{html.escape(Path(path).parent.name)}</span></a>')
            parts.append("</details>")
        parts.append("</div>")
    return "".join(parts)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    notes = sorted(p.relative_to(REPO).as_posix() for p in (REPO / "research_notes").rglob("*.md"))
    all_paths = [p for _, items in SECTIONS for p, _, _ in items] + notes
    links = {p: slug(p) for p in all_paths if (REPO / p).exists()}
    written, warnings = set(), []
    for path in links:
        text = (REPO / path).read_text()
        h1 = re.search(r"^# (.+)$", text, re.M)
        title = h1.group(1).strip() if h1 else Path(path).stem
        body, h2s = render(text, path, links, warnings)
        head = f'<p class="meta">Updated {git_date(path)} &middot; <code>{html.escape(path)}</code></p>'
        plain = re.sub(r"<[^>]+>", "", body)
        if len(plain) > TOC_MIN_CHARS and len(h2s) >= 2:
            head += toc(h2s)
        body = body.replace("</h1>", "</h1>" + head, 1) if "</h1>" in body else head + body
        (OUT / links[path]).write_text(page(title, body))
        written.add(links[path])

    (OUT / "index.html").write_text(page("AI real estate agent: the demo and the research", index(notes, links), back=False))
    written.add("index.html")

    for stale in OUT.glob("*.html"):  # drop pages whose source was renamed or removed
        if stale.name not in written:
            stale.unlink()
    for w in warnings + check(OUT, written):
        print("WARNING:", w, file=sys.stderr)
    print(f"published {len(written)} pages to {OUT}")


if __name__ == "__main__":
    main()
