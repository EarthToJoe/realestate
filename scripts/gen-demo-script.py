#!/usr/bin/env python3
"""Writes docs/DEMO-SCRIPT.md from app/demo/steps.yaml, so the script and the screens stay one for one (SC11).
   python3 scripts/gen-demo-script.py          write the file
   python3 scripts/gen-demo-script.py --check  exit 1 if the committed file differs (the test does this too)"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "DEMO-SCRIPT.md"


def generate() -> str:
    steps = yaml.safe_load((ROOT / "app" / "demo" / "steps.yaml").read_text())["steps"]
    built = [s for s in steps if s["built"]]
    total = sum(s["minutes"] for s in steps)
    lines = [
        "# Demo walkthrough script",
        "",
        "Generated from `app/demo/steps.yaml` by `scripts/gen-demo-script.py`; do not edit by hand (a test fails if",
        "this file and the screens drift apart). Open https://realestate.hughesnode.com (house login), press",
        "**Start demo**, and follow the screens in order. **Presenter notes** (bottom right of each screen) opens the",
        "same words; the audience sees only the product until you open it.",
        "",
        f"Built so far: {', '.join(f'step {s['n']} ({s['title']})' for s in built)}. Target length when all ten",
        f"steps are built: {total:g} minutes plus a 30-second introduction.",
        "",
        "**Colours on every screen:** blue = the AI did it; amber = the seller's or buyer's own decision (the next",
        "step waits for it); red = **NY law today** requires a licensed broker or a lawyer for this act (recorded,",
        "does not stop the flow); grey = a person or third party outside the software. **View as** (top right)",
        "changes who is acting: Presenter, Seller or Buyer. Only the client whose decision it is can make it. Each",
        "screen leads with its result; tables, drafts and records sit in folds (\"Show the working\").",
        "",
        "**The presenter's controls (phone or laptop):**",
        "",
        "- **Start demo** (home) and **Start over** (under the step list) ask first (\"This resets the deal to the beginning\"), then opens step 1 with the demo house",
        "  filled in and one line saying what to press next.",
        "- **\"As Seller\" / \"As Buyer\" below** means: on the amber card, tap **Decide as the seller** (or buyer). One",
        "  tap switches the persona and comes back to the same card; the decision is recorded as the client's. Tap",
        "  **Back to the Presenter** on the card afterwards. The Presenter can never make a client's decision.",
        "- **Any step link works at any time.** A step that needs an earlier one shows a card: what is missing, on",
        "  which step, who must do it, and a button to go there.",
        "- **Fast-forward the demo to here** (on that card, and the ⏩ button beside each step in the step list): plays the earlier",
        "  steps with this script's choices and the recorded AI answers (no cost), each client decision recorded as",
        "  the client's, then opens the step. Use it to jump straight to the part you want to show.",
        "- **On a phone** a compact bar at the top of every screen says where you are (\"Step 6 of 10: Offers\"), with",
        "  arrows to the previous and next screen; \"Steps\" opens the full list with the fast-forward buttons.",
        "",
    ]
    order = [s["n"] for s in steps]
    if order != sorted(order):
        lines += [f"**Walk order:** {', '.join(map(str, order))}. The step list on screen stays in number order; the",
                  "buyer's side (step 8) is walked before the offers (step 6) because offer B comes from the firm's own",
                  "buyer, and the buyer's reply to the seller's counter is made on step 8's offer screen (decision 34).",
                  ""]
    for s in steps:
        lines.append(f"## {s['n']}. {s['title']} ({s['minutes']:g} min){'' if s['built'] else f' (slice {s['slice']})'}")
        lines.append("")
        if not s["built"]:
            sc = s["screens"][0]
            lines += [f"Not built yet. {sc['say']}", "", f"Records: {sc['marker']}.", ""]
            continue
        for i, sc in enumerate(s["screens"], 1):
            lines += [f"### {s['n']}.{i} {sc['title']} (`{sc['route']}`)", "",
                      f"- **Click:** {sc['click']}", f"- **Say:** {sc['say']}",
                      f"- **Markers and decisions:** {sc['marker']}", ""]
    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    text = generate()
    if "--check" in sys.argv:
        sys.exit(0 if OUT.exists() and OUT.read_text() == text else 1)
    OUT.write_text(text)
    print(f"wrote {OUT}")
