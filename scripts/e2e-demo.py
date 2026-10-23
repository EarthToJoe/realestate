#!/usr/bin/env python3
"""The end-to-end run of the demo (SC "Tests"; SC11): headless Chromium plays the guided demo from the home page,
as a presenter would, on a local app in **replay mode with no key** (so any AI answer that is not recorded fails the
run: the hosted demo then runs end to end at $0). Phone (390 px) and laptop (1280 px).

On every screen of the walk, in walk order: open it from the narration card's "Next", tap "Do this screen for me"
if the screen has taps, check there is no gate card and no "not recorded" page, and screenshot what the audience
sees (notes closed). It also checks the spotlight (Driver.js) on one screen and that nothing scrolls sideways.

  .venv/bin/python scripts/e2e-demo.py                 both widths; screenshots to docs/build/screens/slice4/;
                                                         timing to docs/build/e2e-demo-run.md
  .venv/bin/python scripts/e2e-demo.py --quick         phone only, no screenshots (the pytest wrapper uses this)
"""
from __future__ import annotations

import importlib.util
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
OUT = ROOT / "docs" / "build" / "screens" / "slice4"
REPORT = ROOT / "docs" / "build" / "e2e-demo-run.md"
WPM = 150
WIDTHS = [("phone", {"width": 390, "height": 844}), ("laptop", {"width": 1280, "height": 800})]


def _server() -> str:
    spec = importlib.util.spec_from_file_location("phone_check", ROOT / "scripts" / "phone-check.py")
    pc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pc)
    return pc.local_server()  # replay mode, an empty secrets dir: no key, no live call possible


def run(widths=WIDTHS, shots: bool = True) -> dict:
    from playwright.sync_api import sync_playwright

    import yaml

    data = yaml.safe_load((ROOT / "app" / "demo" / "steps.yaml").read_text())
    walk = [(i, st, sc) for i, st in enumerate(data["steps"], 1) for sc in st["screens"]]
    base = _server()
    if shots:
        OUT.mkdir(parents=True, exist_ok=True)
        for p in OUT.glob("*.png"):
            p.unlink()
    results = {"widths": {}, "problems": []}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, vp in widths:
            ctx = b.new_context(viewport=vp, device_scale_factor=1, is_mobile=(name == "phone"),
                                has_touch=(name == "phone"))
            pg = ctx.new_page()
            t_start = time.monotonic()
            pg.goto(base + "/", wait_until="networkidle")
            if shots:
                pg.screenshot(path=str(OUT / f"{name}-00-home.png"))
            pg.click("#start-demo")
            pg.click("#confirm-reset")
            pg.wait_for_load_state("networkidle")
            # the guided demo opens the notes on step 1; the presenter reads them, then closes them (remembered)
            assert pg.is_visible("#presenter-notes"), "the guided demo did not open the narration card"
            if shots:
                pg.screenshot(path=str(OUT / f"{name}-01-notes-open.png"))
            pg.click("[data-notes-close]")
            timings = []
            for k, (i, st, sc) in enumerate(walk, 1):
                t0 = time.monotonic()
                if k > 1:  # Next, from the notes (opened from the chrome, as the presenter does)
                    toggle = ".stepbar [data-notes-toggle]" if name == "phone" else ".presenter-box [data-notes-toggle]"
                    pg.click(toggle)
                    pg.click("#notes-next")
                    pg.wait_for_load_state("networkidle")
                    if pg.is_visible("#presenter-notes"):
                        pg.click("[data-notes-close]")
                path = pg.evaluate("location.pathname")
                if path != sc["route"]:
                    results["problems"].append(f"{name}: expected {sc['route']}, at {path}")
                    pg.goto(base + sc["route"], wait_until="networkidle")
                if pg.query_selector("#play-screen"):  # "Do this screen for me", from the notes
                    toggle = ".stepbar [data-notes-toggle]" if name == "phone" else ".presenter-box [data-notes-toggle]"
                    pg.click(toggle)
                    with pg.expect_navigation():
                        pg.click("#play-screen")
                    pg.wait_for_load_state("networkidle")
                    if pg.is_visible("#presenter-notes"):
                        pg.click("[data-notes-close]")
                html = pg.content()
                if 'id="gate-card"' in html:
                    results["problems"].append(f"{name}: gate card on {sc['route']} after playing it")
                if "The AI's answer is not recorded" in html or "Not recorded:" in html:
                    results["problems"].append(f"{name}: an AI answer was not recorded on {sc['route']}")
                width = pg.evaluate("document.documentElement.scrollWidth")
                if width > vp["width"]:
                    results["problems"].append(f"{name}: {sc['route']} is {width} px wide")
                if name == "laptop" and sc["route"] == "/timeline":  # the spotlight works (Driver.js)
                    pg.click(".presenter-box [data-notes-toggle]")
                    pg.click("#spotlight-start")
                    pg.wait_for_selector(".driver-popover", timeout=5000)
                    pg.wait_for_timeout(800)  # let the spotlight's fade-in finish
                    if shots:
                        pg.screenshot(path=str(OUT / f"{name}-{k + 1:02d}b-spotlight.png"))
                    pg.keyboard.press("Escape")
                    pg.wait_for_timeout(300)
                    if pg.is_visible("#presenter-notes"):
                        pg.click("[data-notes-close]")
                timings.append({"k": k, "step": i, "route": sc["route"], "title": sc["title"],
                                "seconds": round(time.monotonic() - t0, 2),
                                "height": pg.evaluate("document.documentElement.scrollHeight")})
                if shots:
                    slug = sc["route"].strip("/").replace("/", "-")
                    pg.screenshot(path=str(OUT / f"{name}-{k + 1:02d}-{slug}.png"))
            # people and their data: open, export, the access log
            pg.goto(base + "/people", wait_until="networkidle")
            pg.click("#open-seller")
            if shots:
                pg.screenshot(path=str(OUT / f"{name}-{len(walk) + 2:02d}-people.png"))
            with pg.expect_download() as dl:
                pg.click("#export")
            if "legal_name" not in Path(dl.value.path()).read_text():
                results["problems"].append(f"{name}: the export lacks the PII fields")
            results["widths"][name] = {"screens": timings, "click_path_s": round(time.monotonic() - t_start, 1)}
            ctx.close()
        b.close()
    talk = {(st["n"], sc["route"]): len(sc["say"].split()) / WPM * 60 for _, st, sc in walk}
    taps = {(st["n"], sc["route"]): len(re.findall(r'"[^"]+"', sc["click"])) for _, st, sc in walk}
    results["walk"] = [(i, st, sc, talk[(st["n"], sc["route"])], taps[(st["n"], sc["route"])]) for i, st, sc in walk]
    results["intro_talk_s"] = len(data["intro"]["say"].split()) / WPM * 60
    return results


def report(res: dict) -> str:
    walk = res["walk"]
    talk = res["intro_talk_s"] + sum(w[3] for w in walk)
    taps = sum(w[4] for w in walk)
    # A presenter's pace, stated: 4 s a tap (find it, tap it, watch the result), 10 s a screen for the audience to
    # look before the words start. The click path itself is measured below; talk is from the words at 150 a minute.
    est = talk + taps * 4 + len(walk) * 10
    lines = ["# End-to-end demo run (slice 4)", "",
             "Written by `scripts/e2e-demo.py`: headless Chromium plays the guided demo from the home page on a local",
             "app in replay mode with **no API key**, so any AI answer that is not recorded would fail the run. On",
             "every screen, in walk order, it opens the screen from the narration card's Next, taps \"Do this screen",
             "for me\" where the screen has taps, checks for gate cards, unrecorded answers and sideways scrolling, and",
             "screenshots what the audience sees (`docs/build/screens/slice4/`).", "",
             f"**Problems found: {len(res['problems'])}.**" + ("" if not res["problems"] else " " + "; ".join(res["problems"])),
             ""]
    for name, w in res["widths"].items():
        lines.append(f"- {name}: {len(w['screens'])} screens walked, click path {w['click_path_s']} s (the machine's "
                     "time: replays answer at once)")
    lines += ["", "## How long the demo takes with the narration", "",
              f"- Talk: {talk / 60:.1f} min ({sum(len(w[2]['say'].split()) for w in walk)} words of narration plus the "
              f"introduction, at {WPM} words a minute)",
              f"- Taps: {taps} named buttons in the script at about 4 s each: {taps * 4 / 60:.1f} min",
              f"- Looking: {len(walk)} screens at about 10 s each before the words start: {len(walk) * 10 / 60:.1f} min",
              f"- **Estimated run: {est / 60:.1f} minutes** (SC11: 12 to 15). Targets in steps.yaml add up to "
              f"{sum(st['minutes'] for st in {id(w[1]): w[1] for w in walk}.values()) + 0.5:g} minutes.",
              "", "The pace figures are stated assumptions [INFERENCE]; a rehearsal with a person timing it is the",
              "real test. If a rehearsal runs long, trim in this order: skip the MLS package screen (3.2, about 30 s),",
              "the search screen (6.2, 25 s) and the disclosure form (8.2, 25 s), whose points the next screens repeat.",
              "", "## Per screen (phone run)", "", "| # | Step | Screen | Words | Taps | Page height (px) |",
              "|---|---|---|---|---|---|"]
    phone = {t["k"]: t for t in res["widths"].get("phone", {}).get("screens", [])}
    for k, (i, st, sc, t, n) in enumerate(walk, 1):
        h = phone.get(k, {}).get("height", "")
        lines.append(f"| {k} | {i}. {st['title']} | {sc['title']} | {len(sc['say'].split())} | {n} | {h} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    quick = "--quick" in sys.argv
    res = run(widths=WIDTHS[:1] if quick else WIDTHS, shots=not quick)
    for prob in res["problems"]:
        print("PROBLEM", prob)
    if not quick:
        REPORT.write_text(report(res))
        print(f"wrote {REPORT}; screenshots in {OUT}")
    for name, w in res["widths"].items():
        print(name, len(w["screens"]), "screens", w["click_path_s"], "s")
    raise SystemExit(1 if res["problems"] else 0)
