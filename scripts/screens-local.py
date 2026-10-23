#!/usr/bin/env python3
"""Screenshots every demo screen of a local app on recorded replays (no key, $0), with the deal fast-forwarded
through every built step, at phone (390 px) and laptop (1280 px) width; prints each page's size and TOO WIDE if a
page is wider than its viewport. For checking a screen change before it is deployed; scripts/screens.py does the
same against the live site.

  .venv/bin/python scripts/screens-local.py OUT_DIR [--gates]     --gates: right after a reset (the gate cards)
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

PAGES = ["/", "/intake", "/intake/profile", "/intake/disclosures", "/intake/onboarding", "/pricing", "/pricing/advice",
         "/copy", "/copy/mls", "/channels", "/inbox", "/offers", "/buyer", "/buyer/search", "/buyer/tour",
         "/buyer/offer", "/contract", "/disclosures/pcds", "/timeline", "/brand", "/brand/targeting", "/people",
         "/demo/start"]


def main() -> int:
    import importlib.util

    from playwright.sync_api import sync_playwright

    spec = importlib.util.spec_from_file_location("phone_check", ROOT / "scripts" / "phone-check.py")
    pc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pc)
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    base = pc.local_server()
    gates = "--gates" in sys.argv
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, vp in [("phone", {"width": 390, "height": 844}), ("laptop", {"width": 1280, "height": 800})]:
            ctx = b.new_context(viewport=vp, device_scale_factor=1, is_mobile=(name == "phone"), has_touch=(name == "phone"))
            pg = ctx.new_page()
            pg.goto(base + "/demo/start")
            pg.click("#confirm-reset")
            if not gates:
                pg.request.post(base + "/demo/play", form={"route": "/brand/targeting"})  # the whole walk
            for path in PAGES:
                slug = path.strip("/").replace("/", "-") or "home"
                pg.goto(base + path, wait_until="networkidle")
                pg.screenshot(path=str(out / f"{name}-{slug}.png"), full_page=False)
                pg.screenshot(path=str(out / f"{name}-{slug}-full.png"), full_page=True)
                h = pg.evaluate("document.documentElement.scrollHeight")
                w = pg.evaluate("document.documentElement.scrollWidth")
                print(name, path, f"{w}x{h}", "TOO WIDE" if w > vp["width"] else "")
            ctx.close()
        b.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
