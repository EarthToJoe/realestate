#!/usr/bin/env python3
"""The one-path acceptance run in headless Chromium (decisions 47 to 51; the BUILD-PATH brief's acceptance 0 to 4).

On a local app in replay mode with no key (any AI answer that is not recorded fails the run, so the hosted demo
runs end to end at $0), or on a given base URL (the house login is read from /srv/realestate/secrets/HOUSE_PASSWORD;
never written here). Laptop 1280 x 800 and phone 390 x 844, one browser at a time, long timeouts (the server is
shared and loaded).

1. The one-button walk: from the home page, as a first-time visitor (presenting off), press only each screen's
   primary button from Start to the finale. Clean (no "not yet" card, no 4xx or 5xx, no console error), the clicks
   counted, the primary button on screen without scrolling on every screen.
2. The back-step test (laptop): on every screen, Back shows the previous screen exactly as it was left, and pressing
   its button again duplicates nothing; a mid-sale change of the seller's name; changing the price names what
   re-opens; typing then pressing a step in the progress list asks "Leave without saving?".
3. The visitor's layer: no presenter notes, "Do this screen for me", "screen N of", fast-forward, "View as", record
   codes or FH-RULES on any screen. Then presenting: the notes, Do this screen for me, spotlight and skip ahead.
4. Crowding on every screen at 1280 x 800, outside folds: primary buttons, other buttons; the chrome above the
   content on a phone.

  .venv/bin/python scripts/e2e-demo.py                both widths, every check, screenshots of every screen to
                                                       docs/build/screens/one-path/, report docs/build/e2e-demo-run.md
  .venv/bin/python scripts/e2e-demo.py --quick        the phone walk only (the pytest wrapper uses this)
  .venv/bin/python scripts/e2e-demo.py --base https://realestate.hughesnode.com   the same against a server
"""
from __future__ import annotations

import importlib.util
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
OUT = ROOT / "docs" / "build" / "screens" / "one-path"
REPORT = ROOT / "docs" / "build" / "e2e-demo-run.md"
LAPTOP = ("laptop", {"width": 1280, "height": 800})
PHONE = ("phone", {"width": 390, "height": 844})
TIMEOUT = 180_000
CODES = re.compile(r"\bCP-\d+|\b[FL]\d{1,3}\b|\bWS3-|FH-RULES")
BAD_TEXT = ("Do this screen for me", "View as", "⏩")

MEASURE = """() => {
  const vis = e => { if (!e.getClientRects().length) return false; const s = getComputedStyle(e);
                     return s.visibility !== 'hidden' && s.display !== 'none'; };
  const buttons = [...document.querySelectorAll('button, .button, input[type=submit]')].filter(vis)
    .filter(e => !e.closest('.menu'));
  const prim = buttons.filter(e => e.id === 'ab-primary');
  const p = document.getElementById('ab-primary');
  const r = p ? p.getBoundingClientRect() : null;
  const main = document.getElementById('main');
  const top = main ? Math.round(main.getBoundingClientRect().top + window.scrollY) : null;
  const unlabelled = [...document.querySelectorAll('button, a[href]')].filter(vis)
    .filter(e => !(e.innerText || '').trim() && !e.getAttribute('aria-label') && !e.title).length;
  return {primary: prim.length, others: buttons.length - prim.length,
          otherLabels: buttons.filter(e => e.id !== 'ab-primary').map(e => (e.innerText || e.value || '').trim().slice(0, 40)),
          primaryOnScreen: !!r && r.top >= 0 && r.bottom <= innerHeight && r.width > 0,
          primaryLabel: p ? p.innerText.trim() : null, chromeTop: top, unlabelled,
          height: document.documentElement.scrollHeight, width: document.documentElement.scrollWidth,
          text: document.body.innerText};
}"""
STATE = """() => {
  const vals = [...document.querySelectorAll('main input, main textarea, main select')]
    .filter(e => e.type !== 'hidden' && e.name)
    .map(e => e.name + '=' + ((e.type === 'radio' || e.type === 'checkbox') ? (e.checked ? e.value : '') : e.value));
  const decided = [...document.querySelectorAll('[data-decided]')].map(e => e.innerText.replace(/\\s+/g, ' ').trim());
  return {vals, decided};
}"""


def _server() -> str:
    spec = importlib.util.spec_from_file_location("phone_check", ROOT / "scripts" / "phone-check.py")
    pc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pc)
    return pc.local_server()  # replay mode, an empty secrets dir: no key, no live call possible


def _counts() -> dict | None:
    """Rows that must never be duplicated by going back and pressing again (local runs only)."""
    try:
        from app import db
        from app.models import Checkpoint, Deal, Message
        from app.modules.offers import service as offers

        s = db.new_session()
        try:
            deal = s.query(Deal).order_by(Deal.id.desc()).first()
            return {"deals": s.query(Deal).count(), "records": s.query(Checkpoint).count(),
                    "messages": s.query(Message).count(),
                    "offers": len(offers.offers(deal)) if deal else 0}
        finally:
            s.close()
    except Exception:  # noqa: BLE001 (a remote server: counts are not readable from here)
        return None


class Run:
    def __init__(self, base: str, creds: dict | None, shots: bool):
        self.base, self.creds, self.shots = base, creds, shots
        self.problems: list[str] = []
        self.rows: dict[str, dict] = {}  # crowding per screen
        self.walks: dict[str, dict] = {}

    def ctx(self, browser, vp, name):
        c = browser.new_context(viewport=vp, device_scale_factor=1, is_mobile=(name == "phone"),
                                has_touch=(name == "phone"), http_credentials=self.creds)
        c.set_default_timeout(TIMEOUT)
        c.set_default_navigation_timeout(TIMEOUT)
        return c

    def watch(self, page, name):
        page.on("console", lambda m: m.type == "error" and self.problems.append(f"{name}: console error {m.text[:160]}"))
        page.on("response", lambda r: r.status >= 400 and r.request.resource_type == "document"
                and self.problems.append(f"{name}: HTTP {r.status} at {r.url}"))
        page.on("pageerror", lambda e: self.problems.append(f"{name}: page error {str(e)[:160]}"))

    def shot(self, page, name, k, slug):
        if not self.shots:
            return
        OUT.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(OUT / f"{name}-{k:02d}-{slug}.png"))
        page.screenshot(path=str(OUT / f"{name}-{k:02d}-{slug}-full.png"), full_page=True)

    def visitor_checks(self, name, path, m):
        text = m["text"]
        for bad in BAD_TEXT:
            if bad in text:
                self.problems.append(f"{name}: visitor sees {bad!r} on {path}")
        if re.search(r"screen \d+ of", text):
            self.problems.append(f"{name}: visitor sees 'screen N of' on {path}")
        found = CODES.findall(text)
        if found:
            self.problems.append(f"{name}: visitor sees codes {found[:4]} on {path}")
        if m["unlabelled"]:
            self.problems.append(f"{name}: {m['unlabelled']} buttons or links without a label on {path}")

    def walk(self, browser, name, vp, back_step: bool):
        """The one-button walk, as a first-time visitor; on the laptop also the back-step checks."""
        ctx = self.ctx(browser, vp, name)
        page = ctx.new_page()
        self.watch(page, name)
        t0 = time.monotonic()
        page.goto(self.base + "/", wait_until="load")
        self.shot(page, name, 0, "home")
        if page.query_selector("#start-over"):  # a sale in progress (a remote server): start over first
            page.click("#start-over")
            page.click("#confirm-reset")
        else:
            page.click("#start-demo")
        page.wait_for_load_state("load")
        clicks, k, path, seen = 1, 0, None, []
        while True:
            path = page.evaluate("location.pathname")
            if path not in seen:
                seen.append(path)
                k = len(seen)
                m = page.evaluate(MEASURE)
                row = self.rows.setdefault(path, {"path": path})
                row[f"{name}_arrive"] = m
                if 'id="gate-card"' in page.content():
                    self.problems.append(f"{name}: 'not yet' card on {path}")
                if not m["primaryOnScreen"]:
                    self.problems.append(f"{name}: the primary button is not on screen without scrolling on {path}")
                if m["width"] > vp["width"]:
                    self.problems.append(f"{name}: {path} is {m['width']} px wide")
                self.visitor_checks(name, path, m)
                self.shot(page, name, k, (path.strip("/").replace("/", "-") or "home"))
            if path == "/timeline":
                break
            if clicks > 60:
                self.problems.append(f"{name}: the walk did not reach the finale in 60 presses")
                break
            label = page.inner_text("#ab-primary")
            if back_step and label.startswith("Continue"):
                self.back_step(page, name, path)
            if label.startswith("Continue"):
                self.rows[path][f"{name}_leave"] = page.evaluate(MEASURE)
            self.rows[path]["state"] = page.evaluate(STATE)  # the screen as it is left
            with page.expect_navigation(wait_until="load"):
                page.click("#ab-primary")
            clicks += 1
            if back_step and page.evaluate("location.pathname") == "/offers" and "mid_sale" not in self.walks:
                self.walks["mid_sale"] = self.mid_sale(page, name)
        m = page.evaluate(MEASURE)
        self.rows.setdefault("/timeline", {"path": "/timeline"})[f"{name}_arrive"] = m
        self.walks[name] = {"clicks": clicks, "seconds": round(time.monotonic() - t0, 1), "screens": seen}
        if back_step:
            page.goto(self.base + "/contract", wait_until="load")
            self.walks["contract_name"] = "Robin Q. Seller" in page.content()
            if not self.walks["contract_name"]:
                self.problems.append(f"{name}: the changed seller name is not on the contract")
            self.change_price(page, name)
            self.unsaved(page, name)
        ctx.close()

    def back_step(self, page, name, path):
        """Back from here to the previous screen shows it as it was left; its button again duplicates nothing."""
        here = page.evaluate(STATE)
        before = _counts()
        with page.expect_navigation(wait_until="load"):
            page.click("#ab-back")
        prev = page.evaluate("location.pathname")
        state = page.evaluate(STATE)
        left = self.rows.get(prev, {}).get("state")
        if left is not None and state != left:
            self.problems.append(f"{name}: Back to {prev} shows something else than was left: {left} vs {state}")
        with page.expect_navigation(wait_until="load"):
            page.click("#ab-primary")  # Continue: back to here
        again = page.evaluate("location.pathname")
        if again != path:
            self.problems.append(f"{name}: from {prev} the button went to {again}, not back to {path}")
            page.goto(self.base + path, wait_until="load")
        after = _counts()
        if before is not None and after != before:
            self.problems.append(f"{name}: going back from {path} and pressing again changed {before} to {after}")
        if page.evaluate(STATE) != here:
            self.problems.append(f"{name}: {path} changed after going back and forward")
        # the browser's Back, then forward: the same page, as saved
        page.go_back(wait_until="load")
        page.go_forward(wait_until="load")
        if page.evaluate("location.pathname") != path or page.evaluate(STATE) != here:
            self.problems.append(f"{name}: the browser's Back and forward did not return {path} as it was")

    def mid_sale(self, page, name):
        """After reaching the offers, change the seller's name on step 1: the same deal, the offers still there."""
        before = _counts()
        page.goto(self.base + "/intake", wait_until="load")
        page.fill("input[name=seller_name]", "Robin Q. Seller")
        with page.expect_navigation(wait_until="load"):
            page.click("#ab-primary")
        if 'id="change-confirm"' in page.content():
            self.problems.append(f"{name}: a name change asked to redo later steps")
        after = _counts()
        ok = before is None or (after["deals"] == before["deals"] == 1 and after["offers"] == before["offers"])
        if not ok:
            self.problems.append(f"{name}: the name change touched the deal or the offers: {before} -> {after}")
        page.goto(self.base + "/offers", wait_until="load")
        return {"ok": ok, "before": before, "after": after}

    def change_price(self, page, name):
        page.goto(self.base + "/path/change/price", wait_until="load")
        text = page.inner_text("main")
        self.walks["change_price"] = text[:400]
        if "the listing copy" not in text:
            self.problems.append(f"{name}: changing the price does not name the listing copy: {text[:200]}")
        page.click("#cancel-change")
        page.wait_for_load_state("load")

    def unsaved(self, page, name):
        page.goto(self.base + "/intake", wait_until="load")
        page.fill("input[name=street]", "12 Typed Lane")
        seen = []
        page.once("dialog", lambda d: (seen.append(d.message), d.dismiss()))
        page.click('.pathnav a[href="/pricing"]')
        page.wait_for_timeout(500)
        self.walks["unsaved_prompt"] = seen[:1]
        if not seen or "Leave without saving?" not in seen[0]:
            self.problems.append(f"{name}: no 'Leave without saving?' after typing and pressing a step")
        if page.evaluate("location.pathname") != "/intake" or page.input_value("input[name=street]") != "12 Typed Lane":
            self.problems.append(f"{name}: dismissing the prompt lost the typing")

    def presenting(self, browser, name, vp):
        """The guided demo with presenting on: notes beside the content, Do this screen for me, spotlight, skip."""
        ctx = self.ctx(browser, vp, name)
        page = ctx.new_page()
        self.watch(page, name + "/presenting")
        page.goto(self.base + "/", wait_until="load")
        page.click("#menu > summary")
        with page.expect_navigation(wait_until="load"):
            page.click("#presenting-on")
        page.goto(self.base + "/demo/start", wait_until="load")
        if page.query_selector("#confirm-reset"):
            with page.expect_navigation(wait_until="load"):
                page.click("#confirm-reset")
        # skip ahead from a "not yet" card
        page.goto(self.base + "/offers", wait_until="load")
        if not page.query_selector("#gate-ff"):
            self.problems.append(f"{name}: no skip ahead on the 'not yet' card while presenting")
        else:
            with page.expect_navigation(wait_until="load"):
                page.click("#gate-ff")
            if page.query_selector("#gate-card"):
                self.problems.append(f"{name}: skip ahead did not open the offers")
        # Do this screen for me, screen by screen to the end, with the notes open beside the content
        for route in ("/offers", "/contract", "/timeline"):
            page.goto(self.base + route, wait_until="load")
            if not page.is_visible("#presenter-notes"):  # remembered open from the screen before, on a laptop
                page.click("#menu > summary")
                page.click("#menu [data-notes-toggle]")
            if not page.is_visible("#presenter-notes"):
                self.problems.append(f"{name}: the presenter notes did not open on {route}")
            elif vp["width"] > 760:
                main = page.eval_on_selector("#main", "e => e.getBoundingClientRect().right")
                notes = page.eval_on_selector("#presenter-notes", "e => e.getBoundingClientRect().left")
                if main > notes + 1:
                    self.problems.append(f"{name}: the notes cover the content on {route}")
            if self.shots and route == "/offers":
                page.screenshot(path=str(OUT / f"{name}-presenting-notes.png"))
            if page.query_selector("#notes-play"):
                with page.expect_navigation(wait_until="load"):
                    page.click("#notes-play")
            if route == "/timeline":
                page.click("#presenter-notes [data-spotlight-start]")
                page.wait_for_selector(".driver-popover", timeout=TIMEOUT)
                if self.shots:
                    page.wait_for_timeout(800)
                    page.screenshot(path=str(OUT / f"{name}-presenting-spotlight.png"))
                page.keyboard.press("Escape")
        if "(played by the demo)" not in page.content():
            self.problems.append(f"{name}: the timeline does not mark decisions played by the demo")
        # presenting off again, and the sale left reset
        page.click("#menu > summary")
        with page.expect_navigation(wait_until="load"):
            page.click("#presenting-off")
        ctx.close()


def crowding_table(run: Run) -> list[str]:
    lines = ["| Screen | Primary buttons (laptop) | Other buttons (laptop) | Chrome above content (phone, px) | "
             "Page height (phone, px) |", "|---|---|---|---|---|"]
    for path, row in run.rows.items():
        lap = [row.get(k) for k in ("laptop_arrive", "laptop_leave") if row.get(k)]
        ph = row.get("phone_arrive") or {}
        prim = max((m["primary"] for m in lap), default="")
        oth = max((m["others"] for m in lap), default="")
        lines.append(f"| `{path}` | {prim} | {oth} | {ph.get('chromeTop', '')} | {ph.get('height', '')} |")
        for m in lap:
            if m["primary"] > 1:
                run.problems.append(f"laptop: {m['primary']} primary buttons on {path}")
            if m["others"] > 4:
                run.problems.append(f"laptop: {m['others']} other buttons on {path}: {m['otherLabels']}")
        if ph and ph.get("chromeTop") and ph["chromeTop"] > 90:
            run.problems.append(f"phone: the chrome above the content is {ph['chromeTop']} px on {path}")
    return lines


def report(run: Run) -> str:
    table = crowding_table(run)
    lines = ["# End-to-end run of the one path (BUILD-PATH)", "",
             "Written by `scripts/e2e-demo.py`: headless Chromium on a local app in replay mode with **no API key**",
             "(an AI answer that is not recorded would fail the run), laptop 1280 x 800 and phone 390 x 844.",
             "Screenshots of every screen: `docs/build/screens/one-path/`.", "",
             f"**Problems found: {len(run.problems)}.**", ""]
    lines += [f"- {p}" for p in run.problems] + ([""] if run.problems else [])
    lines += ["## 1. The one-button walk", ""]
    for name in ("laptop", "phone"):
        w = run.walks.get(name)
        if w:
            lines.append(f"- {name}: **{w['clicks']} presses** from Start to the finale (target 30 or fewer), "
                         f"{len(w['screens'])} screens, {w['seconds']} s on this machine.")
    lines += ["", "## 2. Back, change and unsaved typing (laptop)", "",
              "- On every screen, Back showed the previous screen as it was left, the button again duplicated nothing,",
              "  and the browser's Back and forward returned the same page (any exception is listed above).",
              f"- Mid-sale: the seller's name changed on step 1 after the offers: {run.walks.get('mid_sale')}; the",
              f"  new name on the contract: {run.walks.get('contract_name')}.",
              f"- Changing the price after the copy exists, the confirm says: \"{(run.walks.get('change_price') or '')[:240]}\"",
              f"- Typing then pressing a step: {run.walks.get('unsaved_prompt')}", "",
              "## 3. Crowding, measured on every screen (outside folds; the menu closed)", ""] + table
    return "\n".join(lines) + "\n"


def run(widths=(LAPTOP, PHONE), shots: bool = True, base: str | None = None, full: bool = True) -> Run:
    from playwright.sync_api import sync_playwright

    creds = None
    if base and base.startswith("https://"):
        creds = {"username": "", "password": open("/srv/realestate/secrets/HOUSE_PASSWORD").read().strip()}
    r = Run(base or _server(), creds, shots)
    if shots:
        OUT.mkdir(parents=True, exist_ok=True)
        for p in OUT.glob("*.png"):
            p.unlink()
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, vp in widths:
            r.walk(b, name, vp, back_step=full and name == "laptop")
        if full:
            for nm, vp in (LAPTOP, PHONE):
                try:
                    r.presenting(b, nm, vp)
                except Exception as e:  # noqa: BLE001 (recorded as a problem; the report is still written)
                    r.problems.append(f"{nm}: presenting run stopped: {str(e).splitlines()[0][:200]}")
        b.close()
    return r


if __name__ == "__main__":
    quick = "--quick" in sys.argv
    base = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else None
    res = run(widths=(PHONE,) if quick else (LAPTOP, PHONE), shots=not quick, base=base, full=not quick)
    if not quick:
        REPORT.write_text(report(res))
        print(f"wrote {REPORT}; screenshots in {OUT}")
        print("\n".join(crowding_table(res)))
    for prob in res.problems:
        print("PROBLEM", prob)
    for name, w in res.walks.items():
        if isinstance(w, dict) and "clicks" in w:
            print(name, w["clicks"], "presses,", len(w["screens"]), "screens,", w["seconds"], "s")
    raise SystemExit(1 if res.problems else 0)
