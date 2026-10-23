"""T4: Driver.js spotlight across two htmx swaps. T7: Leaflet + OSM tiles, with a static fallback offline.
   uv run --no-project --with playwright==1.64.1 python scripts/try/t4_t7_browser.py
Serves throwaway pages built from the vendored files in app/static/vendor on a local port."""
import functools
import http.server
import shutil
import tempfile
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
web = Path(tempfile.mkdtemp())
for f in (ROOT / "app" / "static" / "vendor").iterdir():
    shutil.copy(f, web / f.name)

HEAD = ('<link rel="stylesheet" href="driver.css"><script src="htmx.min.js"></script>'
        '<script src="driver.js.iife.js"></script>')
(web / "t4.html").write_text(f"""<html><head>{HEAD}</head><body>
<div id="container" style="margin:40px;padding:20px;border:1px solid #ccc">
  <div id="panel">Before <button id="go" hx-get="f1.html" hx-target="#container" hx-swap="innerHTML">swap</button></div>
</div>
<script>
  const d = window.driver.js.driver({{animate:false}});
  window.tour = d;
  window.highlightInner = false;
  document.body.addEventListener('htmx:afterSettle', () => {{
    if (window.highlightInner) d.highlight({{element:'#panel', popover:{{title:'AI work', description:'re-pinned'}}}});
    else d.refresh();
  }});
</script></body></html>""")
for i, nxt in ((1, 2), (2, 3)):
    (web / f"f{i}.html").write_text(f'<div id="panel">After {i} <button id="go" hx-get="f{nxt}.html" '
                                    f'hx-target="#container" hx-swap="innerHTML">swap</button></div>')
(web / "f3.html").write_text('<div id="panel">After 3</div>')

(web / "t7.html").write_text("""<html><head><link rel="stylesheet" href="leaflet.css"><script src="leaflet.js"></script>
</head><body><div id="map" style="width:600px;height:400px"></div>
<div id="map-fallback" style="display:none;width:600px;height:400px;background:#eef">
  <svg viewBox="0 0 600 400" width="600" height="400"><circle cx="300" cy="200" r="8" fill="#b42318"/>
  <text x="315" y="205" font-size="14">146 Route 292, Holmes (41.5232, -73.6451)</text>
  <text x="20" y="380" font-size="12">Map tiles need internet; static fallback.</text></svg></div>
<script>
  const map = L.map('map').setView([41.523196, -73.645089], 14);
  let errors = 0;
  const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',
      {maxZoom: 19, attribution: '&copy; OpenStreetMap contributors'}).addTo(map);
  tiles.on('tileerror', () => { if (++errors >= 3) { document.getElementById('map').style.display = 'none';
      document.getElementById('map-fallback').style.display = 'block'; } });
  L.marker([41.523196, -73.645089]).addTo(map);
</script></body></html>""")


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(web)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_address[1]}"


def spotlight_state(page, selector):
    return page.evaluate("""(sel) => {
        const active = document.querySelector('.driver-active-element');
        const pop = document.querySelector('.driver-popover');
        const target = document.querySelector(sel);
        return {active: !!active, connected: !!(active && active.isConnected), same: active === target,
                popover: !!(pop && getComputedStyle(pop).display !== 'none' && pop.getBoundingClientRect().width > 0)};
    }""", selector)


with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    # T4a: spotlight on the swap container (the app's pattern: hx-target is a stable container, innerHTML swap)
    page.goto(base + "/t4.html")
    page.evaluate("tour.highlight({element:'#container', popover:{title:'AI work', description:'container'}})")
    for _ in range(2):
        page.click("#go", force=True)
        page.wait_for_timeout(400)
    a = spotlight_state(page, "#container")
    print("T4a container target after 2 swaps:", a)
    # T4b: spotlight on an element the swap replaces, re-pinned on htmx:afterSettle
    page.goto(base + "/t4.html")
    page.evaluate("window.highlightInner = true; tour.highlight({element:'#panel', popover:{title:'AI', description:'x'}})")
    for _ in range(2):
        page.click("#go", force=True)
        page.wait_for_timeout(400)
    bb = spotlight_state(page, "#panel")
    print("T4b replaced target, re-pinned after each swap:", bb, page.inner_text("#panel")[:20])
    t4 = all(a.values()) and all(bb.values())
    print("T4", "PASS" if t4 else "FAIL")

    # T7a online: tiles load
    page = b.new_page()
    page.goto(base + "/t7.html")
    page.wait_for_timeout(5000)
    loaded = page.evaluate("document.querySelectorAll('img.leaflet-tile-loaded').length")
    print("T7a online tiles loaded:", loaded)
    # T7b offline tiles: fallback shows
    page2 = b.new_page()
    page2.route("**/tile.openstreetmap.org/**", lambda route: route.abort())
    page2.goto(base + "/t7.html")
    page2.wait_for_timeout(2500)
    fb = page2.evaluate("getComputedStyle(document.getElementById('map-fallback')).display")
    print("T7b offline fallback display:", fb)
    print("T7", "PASS" if loaded > 0 and fb == "block" else ("PARTIAL (fallback only)" if fb == "block" else "FAIL"))
    b.close()
srv.shutdown()
