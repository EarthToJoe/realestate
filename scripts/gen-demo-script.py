#!/usr/bin/env python3
"""Writes docs/DEMO-SCRIPT.md from app/demo/steps.yaml, so the script and the screens stay one for one (SC11).
   python3 scripts/gen-demo-script.py          write the file
   python3 scripts/gen-demo-script.py --check  exit 1 if the committed file differs (the test does this too)

Steps are numbered as the screens number them: in the order the demo walks them (Q47). Talk time is estimated from
the words at 150 a minute; the click path is measured by the end-to-end run (docs/build/e2e-demo-run.md)."""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "DEMO-SCRIPT.md"
WPM = 150


def words(text: str) -> int:
    return len(text.split())


def generate() -> str:
    data = yaml.safe_load((ROOT / "app" / "demo" / "steps.yaml").read_text())
    steps, intro = data["steps"], data["intro"]
    built = [s for s in steps if s["built"]]
    total = intro["minutes"] + sum(s["minutes"] for s in steps)
    talk = (words(intro["say"]) + sum(words(sc["say"]) for s in steps for sc in s["screens"])) / WPM
    n_screens = sum(len(s["screens"]) for s in steps)
    lines = [
        "# Demo walkthrough script",
        "",
        "Generated from `app/demo/steps.yaml` by `scripts/gen-demo-script.py`; do not edit by hand (a test fails if",
        "this file and the screens drift apart). Open https://realestate.hughesnode.com (house login), press",
        "**Start demo**, and follow the screens in order. The same words are in the app: **Notes** in the bar at the",
        "top of a phone, **Presenter notes** under the step list on a laptop. The audience sees only the product",
        "until you open them.",
        "",
        f"**Length.** {len(steps)} steps, {n_screens} screens, target {total:g} minutes with the introduction "
        f"(SC11: 12 to 15). The",
        f"words below take about {talk:.1f} minutes to say at {WPM} words a minute; the rest is tapping and letting",
        "the audience look. The timed run is in `docs/build/e2e-demo-run.md`.",
        "",
        f"Built: {', '.join(f'step {i} ({s['title']})' for i, s in enumerate(steps, 1) if s['built'])}."
        if len(built) < len(steps) else "Built: all ten steps.",
        "",
        "**Colours on every screen:** blue = the AI did it; amber = the seller's or buyer's own decision (the next",
        "step waits for it); red = **NY law today** requires a licensed broker or a lawyer for this act (recorded,",
        "does not stop the flow); grey = a person or third party outside the software. **View as** (top right)",
        "changes who is acting: Presenter, Seller or Buyer. Only the client whose decision it is can make it. Each",
        "screen leads with its result; tables, drafts and records sit in folds (\"Show the working\").",
        "",
        "**The presenter's controls (phone or laptop):**",
        "",
        "- **Start demo** (home) asks first (\"This resets the deal to the beginning\"), then opens step 1 with the",
        "  guided demo on: the notes open on every screen (close them with ×; they stay closed on that device until",
        "  you open them again), with **Next** to the following screen in walk order.",
        "- **Spotlight** (in the notes) points at the parts of the screen this script names, one at a time, with a",
        "  short caption the audience may read.",
        "- **Do this screen for me** (in the notes) does this screen's taps the way this script does, with the",
        "  recorded AI answers (no cost); each client decision is still recorded as the client's.",
        "- **Decide as the seller** (or buyer) on an amber card switches the persona in one tap and comes back to the",
        "  card; **Back to the Presenter** afterwards. The Presenter can never make a client's decision.",
        "- **Any step link works at any time.** A step that needs an earlier one shows a card: what is missing, on",
        "  which step, who must do it, a button to go there and **Fast-forward the demo to here** (also the ⏩ beside",
        "  each step in the list), which plays the earlier steps with this script's choices at no cost.",
        "- **On a phone** the bar at the top says where you are (\"Step 7 of 10: Offers\"), with arrows to the",
        "  previous and next screen in walk order, **Notes**, and ☰ for the full list.",
        "",
        "**Step numbers.** The screens number the steps in the order the demo walks them, 1 to 10 (Q47). The",
        "success criteria number three of them differently; the mapping, once:",
        "",
        "| On screen and in this script | Success criteria |",
        "|---|---|",
    ]
    for i, s in enumerate(steps, 1):
        lines.append(f"| {i}. {s['title']} | SC{s['n']}{'' if s['n'] == i else ' (renumbered)'} |")
    lines += ["", f"## Introduction ({intro['minutes']:g} min, on the home page)", "",
              f"- **Say:** {intro['say']}", f"- **Point at:** {intro['point']}", ""]
    k = 0
    for i, s in enumerate(steps, 1):
        lines.append(f"## {i}. {s['title']} ({s['minutes']:g} min){'' if s['built'] else f' (slice {s['slice']})'}")
        lines.append("")
        if not s["built"]:
            sc = s["screens"][0]
            lines += [f"Not built yet. {sc['say']}", "", f"Records: {sc['marker']}.", ""]
            continue
        for j, sc in enumerate(s["screens"], 1):
            k += 1
            lines += [f"### {i}.{j} {sc['title']} (`{sc['route']}`, screen {k} of {n_screens})", "",
                      f"- **Do:** {sc['click']}", f"- **Say:** {sc['say']}"]
            if sc.get("point"):
                lines.append(f"- **Point at:** {sc['point']}")
            lines.append(f"- **Markers and decisions:** {sc['marker']}")
            if sc.get("spotlight"):
                lines.append(f"- **Spotlight:** {'; '.join(x['text'] for x in sc['spotlight'])}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    text = generate()
    if "--check" in sys.argv:
        sys.exit(0 if OUT.exists() and OUT.read_text() == text else 1)
    OUT.write_text(text)
    print(f"wrote {OUT}")
