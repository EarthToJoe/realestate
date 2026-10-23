#!/usr/bin/env python3
"""Writes docs/DEMO-SCRIPT.md from app/demo/steps.yaml, so the script and the screens stay one for one (SC11).
   python3 scripts/gen-demo-script.py          write the file
   python3 scripts/gen-demo-script.py --check  exit 1 if the committed file differs (the test does this too)

The path (decision 51): eleven steps of the sale, then the finale, then "one more thing". Talk time is estimated
from the words at 150 a minute; the click path is measured by the end-to-end run (docs/build/e2e-demo-run.md)."""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "DEMO-SCRIPT.md"
WPM = 150


def words(text: str) -> int:
    return len(text.split())


def section(lines: list[str], head: str, sc: dict) -> None:
    lines += [head, "", f"Screen `{sc['route']}`. **The visitor reads:** {sc['explain'].strip()}", "",
              f"- **Do:** {sc['click']}", f"- **Say:** {sc['say']}"]
    if sc.get("point"):
        lines.append(f"- **Point at:** {sc['point']}")
    lines.append(f"- **Markers and decisions:** {sc['marker']}")
    if sc.get("spotlight"):
        lines.append(f"- **Spotlight:** {'; '.join(x['text'] for x in sc['spotlight'])}")
    lines.append("")


def generate() -> str:
    data = yaml.safe_load((ROOT / "app" / "demo" / "steps.yaml").read_text())
    steps, intro, finale, after = data["steps"], data["intro"], data["finale"], data["after"]
    every = steps + [finale, after]
    total = intro["minutes"] + sum(s["minutes"] for s in every)
    talk = (words(intro["say"]) + sum(words(s["say"]) for s in every)) / WPM
    lines = [
        "# Demo walkthrough script",
        "",
        "Generated from `app/demo/steps.yaml` by `scripts/gen-demo-script.py`; do not edit by hand (a test fails if",
        "this file and the screens drift apart). Open https://realestate.hughesnode.com (house login) and press",
        "**Start**.",
        "",
        f"**Length.** {len(steps)} steps of the sale, then the finale and one more thing: target {total:g} minutes",
        f"with the introduction (SC11: 12 to 15). The words below take about {talk:.1f} minutes to say at {WPM} words",
        "a minute; the rest is pressing and letting the audience look. The timed run is in",
        "`docs/build/e2e-demo-run.md`.",
        "",
        "**How the screens work (decisions 47 to 51).** One path, walked in order. Every screen ends in one action",
        "bar: **← Back** on the left, one button on the right. The button does the next thing on the screen, worded",
        "for what it does (\"Seller: list at $640,000\"); when nothing is left it reads **Continue: <next step>**.",
        "**You play the seller and the buyer: the amber buttons are their decisions. The AI does everything else**,",
        "on its own, as soon as what it waits for is done, so each screen opens with the AI's work already there.",
        "Every decision has a **Change** link once made: it says what it re-opens, then re-opens only that. Going",
        "back never loses anything.",
        "",
        "**Colours on every screen:** blue = the AI did it; amber = the seller's or buyer's own decision; red = **NY",
        "law today** requires a licensed broker or a lawyer for this act (recorded, does not stop the flow); grey = a",
        "person or third party outside the software. Each screen leads with its result; tables, drafts and records",
        "sit in folds (\"Show the working\").",
        "",
        "**Presenting.** Open the menu (top right) and press **I'm presenting**: it is remembered on that device.",
        "Then the menu also holds:",
        "",
        "- **Presenter notes**: these words, in a drawer beside the screen on a laptop (the screen narrows; nothing is",
        "  covered) or a sheet from the bottom on a phone (starts closed).",
        "- **Do this screen for me**: plays this screen's buttons the way this script does, with the recorded AI",
        "  answers (no cost). Each seller or buyer decision it plays is recorded as theirs and marked \"played by",
        "  the demo\" on its card and on the timeline.",
        "- **Spotlight**: points at the parts of the screen this script names, one at a time.",
        "- **Skip ahead**: plays every step before the chosen one with this script's choices, then opens it. A",
        "  step that comes later in the sale shows a \"Not yet\" card with the same Skip ahead button.",
        "- The demo devices (plant a fair-housing violation, a bolder headline, a refused ad target, a counter by",
        "  hand) sit in a \"Presenter's tools\" fold on their screens, only when presenting.",
        "",
        "Without presenting, a visitor sees the product only: no notes, no skip ahead, no codes.",
        "",
        f"## Introduction ({intro['minutes']:g} min, on the home page)",
        "",
        f"- **Say:** {intro['say']}",
        f"- **Point at:** {intro['point']}",
        "",
    ]
    for s in steps:
        section(lines, f"## {s['n']}. {s['title']} ({s['minutes']:g} min)", s)
    section(lines, f"## The finale: {finale['title']} ({finale['minutes']:g} min)", finale)
    section(lines, f"## After the finale: {after['title']} ({after['minutes']:g} min)", after)
    lines += ["## Step numbers and the success criteria", "",
              "The records and the success criteria keep their own step numbers; the path's steps map to them:", "",
              "| On screen | Success criteria |", "|---|---|"]
    for s in steps + [finale, after]:
        label = f"{s['n']}. {s['title']}" if s.get("n") else s["title"]
        lines.append(f"| {label} | {', '.join('SC' + str(x) for x in s['sc'])} |")
    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    text = generate()
    if "--check" in sys.argv:
        sys.exit(0 if OUT.exists() and OUT.read_text() == text else 1)
    OUT.write_text(text)
    print(f"wrote {OUT}")
