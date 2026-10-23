"""Renders the repo's documents as phone-readable pages for Joe at https://realestate.hughesnode.com.

Run through scripts/publish-review.sh (which supplies the markdown package via uv). Reads docs/ and
research_notes/ from the repo, writes static HTML into the hughesnode app's public/ folder. Pages that do
not exist yet are listed as "being written", so the index always shows the whole project.
"""
import html
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import markdown

REPO = Path(__file__).resolve().parent.parent
TZ = "America/New_York"  # Joe reads in Eastern time
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/srv/hughesnode/apps/realestate/public")

# (section, [(repo path, short title, one-line note)]); order is the order on the home page.
SECTIONS = [
    ("Waiting on you", [
        ("docs/SUCCESS-CRITERIA.md", "Demo finish line", "Reply SIGN-OFF in the chat, or say what to change"),
        ("docs/QUESTIONS-FOR-JOE.md", "Questions for Joe", "One line each; my default holds until you answer"),
    ]),
    ("Today", [
        ("docs/PROGRESS.md", "Progress", "Daily summary, newest first"),
        ("docs/SPEND-LOG.md", "API spend", "Where the $200 credit went, per workstream"),
    ]),
    ("For your father-in-law", [
        ("docs/EXECUTIVE-SUMMARY.md", "Executive summary", "The one document to hand him"),
        ("docs/PLAN.md", "Project plan", "Phases, costs, open questions, human-in-the-loop map"),
        ("docs/DEMO-SCRIPT.md", "Demo walkthrough script", "What to click and say, screen by screen"),
    ]),
    ("Research deliverables", [
        ("docs/research/WS1-agent-functions.md", "1. What an agent does", "Every function, and whether software can do it"),
        ("docs/research/WS2-legal-licensing.md", "2. Legal and licensing hurdles", "Where a licence or a lawyer is required"),
        ("docs/research/WS3-listing-data-access.md", "3. Listing and data access", "MLS, Zillow, Redfin, Realtor.com: API or human?"),
        ("docs/research/WS4-cost-model.md", "4. Cost model", "Upfront, ongoing, break-even"),
        ("docs/research/WS5-competitors.md", "5. Competitors", "Who already does this, and can a local launch win"),
        ("docs/research/WS6-free-inspection.md", "6. Free inspection", "Pros, cons, liability"),
    ]),
    ("Living documents", [
        ("docs/ASSUMPTIONS.md", "Riskiest assumptions", "Ranked, with kill criteria and status"),
        ("docs/DECISIONS.md", "Decision log", "Every choice and why"),
        ("docs/TRACEABILITY.md", "Traceability", "Each demo feature, the agent function and the law behind it"),
        ("docs/OUT-OF-SCOPE.md", "Out of scope", "What the demo will not do"),
        ("docs/BRIEF.md", "Your brief", "Verbatim, the source of truth"),
    ]),
]
LABELS = {"PRIMARY": "p", "SECONDARY": "s", "CLAIMED": "c", "INFERENCE": "i"}

CSS = """
:root{--bg:#fbfaf7;--fg:#1d1d1b;--muted:#6b6a65;--line:#e4e1d9;--card:#fff;--accent:#1f5f8b;--warn:#8a5a00;
--p:#1e6b3a;--s:#30557a;--c:#8a5a00;--i:#6a3d8a;--code:#f2f0ea}
@media (prefers-color-scheme:dark){:root{--bg:#161614;--fg:#e9e7e1;--muted:#a19f98;--line:#33322e;--card:#1e1e1b;
--accent:#7db7e0;--warn:#e0b25a;--p:#7cc796;--s:#8fb4dc;--c:#e0b25a;--i:#c39be0;--code:#262622}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
main{max-width:46rem;margin:0 auto;padding:20px 16px 64px}
a{color:var(--accent)}h1{font-size:1.6rem;line-height:1.25;margin:.4em 0 .3em}
h2{font-size:1.25rem;margin:1.8em 0 .4em;line-height:1.3}h3{font-size:1.05rem;margin:1.4em 0 .3em}
.meta{color:var(--muted);font-size:.85rem}.top{font-size:.9rem;margin-bottom:8px}
.tw{overflow-x:auto;margin:1em 0;border:1px solid var(--line);border-radius:8px}
table{border-collapse:collapse;font-size:.85rem;min-width:100%}th,td{padding:6px 9px;border-bottom:1px solid var(--line);
text-align:left;vertical-align:top}th{background:var(--code);position:sticky;top:0}
code{background:var(--code);padding:1px 4px;border-radius:4px;font-size:.88em;overflow-wrap:anywhere}
pre{background:var(--code);padding:12px;border-radius:8px;overflow-x:auto}pre code{padding:0}
blockquote{margin:1em 0;padding:.2em 1em;border-left:3px solid var(--line);color:var(--muted)}
.lab{font-size:.68rem;font-weight:600;letter-spacing:.03em;padding:1px 5px;border-radius:4px;border:1px solid currentColor;
white-space:nowrap}.lab.p{color:var(--p)}.lab.s{color:var(--s)}.lab.c{color:var(--c)}.lab.i{color:var(--i)}
.sec{margin-top:28px}.sec h2{font-size:.8rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:0 0 8px}
.item{display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:8px 0;
text-decoration:none;color:var(--fg)}.item b{color:var(--accent)}.item span{display:block;color:var(--muted);font-size:.88rem}
.item.pending{opacity:.55}.item.pending b{color:var(--muted)}.badge{float:right;font-size:.75rem;color:var(--muted)}
.item.wait{border-color:var(--warn)}details{margin:6px 0}summary{cursor:pointer;color:var(--accent)}
img{max-width:100%}hr{border:0;border-top:1px solid var(--line);margin:2em 0}
"""


def git_date(path: str) -> str:
    r = subprocess.run(["git", "-C", str(REPO), "log", "-1", "--format=%cd", "--date=format-local:%b %-d, %-I:%M %p ET",
                        "--", path], capture_output=True, text=True, env={**os.environ, "TZ": TZ})
    return r.stdout.strip() or "not yet committed"


def slug(path: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", Path(path).with_suffix("").as_posix().lower()).strip("-") + ".html"


def page(title: str, body: str, back: bool = True) -> str:
    nav = '<div class="top"><a href="index.html">&larr; All documents</a></div>' if back else ""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">'
            f'<title>{html.escape(title)}</title><style>{CSS}</style></head><body><main>{nav}{body}</main></body></html>')


def render(md_text: str, links: dict) -> str:
    out = markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists", "toc"])
    out = out.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    out = re.sub(r"\[(PRIMARY|SECONDARY|CLAIMED|INFERENCE)\]",
                 lambda m: f'<span class="lab {LABELS[m.group(1)]}">{m.group(1)}</span>', out)

    def relink(m):  # point links between repo documents at their rendered pages
        target = m.group(1).split("#")[0]
        for repo_path, page_name in links.items():
            if target and repo_path.endswith(target.lstrip("./")):
                return f'href="{page_name}"'
        return m.group(0)
    return re.sub(r'href="([^"]+\.md(?:#[^"]*)?)"', relink, out)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    notes = sorted(p.relative_to(REPO).as_posix() for p in (REPO / "research_notes").rglob("*.md"))
    all_paths = [p for _, items in SECTIONS for p, _, _ in items] + notes
    links = {p: slug(p) for p in all_paths if (REPO / p).exists()}
    written = set()
    for path in links:
        text = (REPO / path).read_text()
        h1 = re.search(r"^# (.+)$", text, re.M)
        title = h1.group(1).strip() if h1 else Path(path).stem
        meta = f'<p class="meta">Updated {git_date(path)} &middot; <code>{html.escape(path)}</code></p>'
        (OUT / links[path]).write_text(page(title, meta + render(text, links)))
        written.add(links[path])

    head = subprocess.run(["git", "-C", str(REPO), "log", "-1", "--format=%h %s"], capture_output=True, text=True).stdout.strip()
    parts = ['<h1>Real estate: review home</h1>',
             f'<p class="meta">Published {datetime.now(ZoneInfo(TZ)).strftime("%b %-d, %-I:%M %p ET")} from commit '
             f'<code>{html.escape(head[:80])}</code>. Refreshes on every commit.</p>']
    for section, items in SECTIONS:
        parts.append(f'<div class="sec"><h2>{section}</h2>')
        for path, short, note in items:
            if path in links:
                cls = "item wait" if section == "Waiting on you" else "item"
                parts.append(f'<a class="{cls}" href="{links[path]}"><span class="badge">{git_date(path)}</span>'
                             f'<b>{html.escape(short)}</b><span>{html.escape(note)}</span></a>')
            else:
                parts.append(f'<div class="item pending"><span class="badge">being written</span>'
                             f'<b>{html.escape(short)}</b><span>{html.escape(note)}</span></div>')
        parts.append("</div>")
    parts.append('<div class="sec"><h2>Raw research notes</h2><details><summary>'
                 f'{len(notes)} notes files, every claim sourced and labelled</summary>')
    for path in notes:
        parts.append(f'<a class="item" href="{links[path]}"><b>{html.escape(Path(path).stem.replace("_", " "))}</b>'
                     f'<span>{html.escape(Path(path).parent.name)}</span></a>')
    parts.append("</details></div>")
    (OUT / "index.html").write_text(page("Real estate: review home", "".join(parts), back=False))
    written.add("index.html")

    for stale in OUT.glob("*.html"):  # drop pages whose source was renamed or removed
        if stale.name not in written:
            stale.unlink()
    print(f"published {len(written)} pages to {OUT}")


if __name__ == "__main__":
    main()
