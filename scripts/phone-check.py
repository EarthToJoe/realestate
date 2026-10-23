#!/usr/bin/env python3
"""Every demo screen at phone width (390 x 844, a current iPhone) in headless Chromium: the compact step bar is on
screen without scrolling, every visible button is at least 44 px tall, and nothing scrolls sideways. Checked twice:
right after "Start demo" (the gate cards) and with the deal fast-forwarded through every built step (full screens).

  .venv/bin/python scripts/phone-check.py                       a local app on recorded replays (no key, $0)
  .venv/bin/python scripts/phone-check.py https://realestate.hughesnode.com   the live site (house login; it
                                                                 resets the live deal, then walks it to the end)
Needs: uv pip install --python .venv/bin/python playwright && .venv/bin/python -m playwright install chromium
"""
from __future__ import annotations

import shutil
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

W, H = 390, 844
MEASURE = """() => {
  // measure with the overflow-x backstop in app.css switched off: clipped content would count as too wide
  for (const e of [document.documentElement, document.body]) e.style.overflowX = 'visible';
  const wide = [...document.querySelectorAll('body *')].filter(e => {
      const r = e.getBoundingClientRect(); if (r.width === 0 || r.right <= innerWidth + 1) return false;
      for (let a = e.parentElement; a; a = a.parentElement) {
        const o = getComputedStyle(a).overflowX; if ((o === 'auto' || o === 'scroll') && a !== document.body) return false; }
      return true; }).map(e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : '')).slice(0, 5);
  const vis = e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
                     return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const small = [...document.querySelectorAll('button, .button, select, input[type=submit]')].filter(vis)
    .map(e => [Math.round(e.getBoundingClientRect().height), (e.innerText || e.value || e.name || e.tagName).trim().slice(0, 40)])
    .filter(([h]) => h < 44);
  const bar = document.querySelector('.stepbar');
  const r = bar ? bar.getBoundingClientRect() : null;
  return {scrollWidth: document.documentElement.scrollWidth, wide, small,
          bar: r ? {visible: vis(bar), bottom: Math.round(r.bottom), pills: bar.querySelectorAll('a').length} : null};
}"""


def local_server() -> str:
    import uvicorn

    from app.config import Settings
    from app.main import create_app

    data = ROOT / "tmp" / "phone-check"
    shutil.rmtree(data, ignore_errors=True)
    app = create_app(Settings(data_dir=data, model_mode="replay", secrets_dir=ROOT / "tmp" / "no-secrets",
                              review_dir=ROOT / "tmp" / "no-review"))
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=8765, log_level="warning"))
    threading.Thread(target=server.run, daemon=True).start()
    for _ in range(100):
        if server.started:
            break
        time.sleep(0.1)
    return "http://127.0.0.1:8765"


def main() -> int:
    from playwright.sync_api import sync_playwright

    from app.web import steps

    base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else local_server()
    # the house login (blank username), read from a root-only file; never written in the repo
    creds = ({"username": "", "password": open("/srv/realestate/secrets/HOUSE_PASSWORD").read().strip()}
             if base.startswith("https://") else None)
    routes = ["/", "/demo/start"] + [sc["route"] for st in steps() for sc in st["screens"]]
    fail = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=3, is_mobile=True,
                                  has_touch=True, http_credentials=creds)
        page = ctx.new_page()
        for phase in ("after Start demo", "every built step walked"):
            if phase == "after Start demo":
                page.goto(base + "/demo/start")
                page.click("#confirm-reset")
            else:
                page.goto(base + "/timeline")
                # the whole walk, step 10 included ("Do this screen for me" on the last screen)
                page.request.post(base + "/demo/play", form={"route": steps()[-1]["screens"][-1]["route"]})
            if phase != "after Start demo":
                page.goto(base + "/contract")
                if not page.query_selector("#signed"):
                    print("FAIL the deal was not walked to the signed contract")
                    fail = 1
            print(f"-- {phase}")
            for route in routes:
                resp = page.goto(base + route)
                m = page.evaluate(MEASURE)
                problems = []
                if resp is None or resp.status != 200 or page.url.split("#")[0].split("?")[0] != base + route.split("?")[0]:
                    problems.append(f"HTTP {resp.status if resp else '?'} at {page.url}")
                if m["scrollWidth"] > W or m["wide"]:
                    problems.append(f"scrolls sideways ({m['scrollWidth']} px wide: {m['wide']})")
                if m["small"]:
                    problems.append(f"buttons under 44 px: {m['small'][:4]}")
                if not m["bar"] or not m["bar"]["visible"] or m["bar"]["bottom"] > H:
                    problems.append(f"step bar not on screen: {m['bar']}")
                fail |= bool(problems)
                print(f"{'ok  ' if not problems else 'FAIL'} {route:22} width {m['scrollWidth']}"
                      f"{'' if not problems else '  ' + '; '.join(problems)}")
            shot = ROOT / "tmp" / f"phone-{'gate' if phase.startswith('after') else 'walked'}.png"
            page.goto(base + ("/pricing" if phase.startswith("after") else "/offers"))
            page.screenshot(path=str(shot))
        browser.close()
    print("PHONE CHECK: OK" if not fail else "PHONE CHECK: FAILED")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
