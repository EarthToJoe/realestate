"""Screenshots every demo screen at phone (390 px) and laptop (1280 px) width, and reports any page wider than
its viewport. The UI audit (docs/build/ui-audit-2026-10-23.md) was made from these.

    uv run --no-project --with playwright python3 scripts/screens.py OUT_DIR [BASE_URL]

The house login is read from /srv/realestate/secrets/HOUSE_PASSWORD (blank username); it is never written here.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]
BASE = sys.argv[2] if len(sys.argv) > 2 else "https://realestate.hughesnode.com"
PASSWORD = Path("/srv/realestate/secrets/HOUSE_PASSWORD").read_text().strip()
PAGES = ["/", "/intake", "/intake/profile", "/intake/onboarding", "/pricing", "/copy", "/channels", "/inbox",
         "/offers", "/buyer", "/contract", "/timeline", "/index.html"]
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, vp in [("phone", {"width": 390, "height": 844}), ("laptop", {"width": 1280, "height": 800})]:
        ctx = b.new_context(viewport=vp, http_credentials={"username": "", "password": PASSWORD},
                            device_scale_factor=1, is_mobile=(name == "phone"), has_touch=(name == "phone"))
        pg = ctx.new_page()
        for path in PAGES:
            slug = path.strip("/").replace("/", "-").replace(".html", "") or "home"
            try:
                pg.goto(BASE + path, wait_until="networkidle", timeout=30000)
                pg.screenshot(path=f"{OUT}/{name}-{slug}.png", full_page=False)
                pg.screenshot(path=f"{OUT}/{name}-{slug}-full.png", full_page=True)
                h = pg.evaluate("document.documentElement.scrollHeight"); w = pg.evaluate("document.documentElement.scrollWidth")
                print(name, path, f"{w}x{h}", "TOO WIDE" if w > vp["width"] else "")
            except Exception as e:
                print(name, path, "ERR", e)
        ctx.close()
    b.close()
