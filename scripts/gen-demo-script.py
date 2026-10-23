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
        "**Start demo**, and follow the screens in order. The narration card at the top of each screen says the same.",
        "",
        f"Built so far: {', '.join(f'step {s['n']} ({s['title']})' for s in built)}. Target length when all ten",
        f"steps are built: {total:g} minutes plus a 30-second introduction.",
        "",
        "**Colours on every screen:** blue = the AI did it; amber = the seller's or buyer's own decision (the next",
        "step waits for it); red = **NY law today** requires a licensed broker or a lawyer for this act (recorded,",
        "does not stop the flow); grey = a person or third party outside the software. The persona switcher (top",
        "right) changes who is acting: Presenter, Seller or Buyer. Only the client whose decision it is can make it.",
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
