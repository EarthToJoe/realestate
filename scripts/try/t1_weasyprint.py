"""T1: WeasyPrint renders a 10-page contract-like HTML to PDF in under 5 s (run inside the Docker image)."""
import sys
import time

from weasyprint import HTML

para = ("This contract of sale is a demonstration drafted by software. NY law today: only a lawyer may draft a "
        "contract of sale for another (L21, L22). ") * 12
pages = "".join(f"<section style='page-break-after:always'><h2>Section {i}</h2>" + f"<p>{para}</p>" * 6
                + "</section>" for i in range(1, 11))
html = ("<html><head><style>@page{size:Letter;margin:1in;@bottom-center{content:'DEMONSTRATION. Drafted by "
        "software for the parties. Page ' counter(page)}} body{font-family:DejaVu Serif;font-size:11pt}</style>"
        "</head><body>" + pages + "</body></html>")
t0 = time.monotonic()
doc = HTML(string=html).render()
pdf = doc.write_pdf()
dt = time.monotonic() - t0
out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/t1.pdf"
open(out, "wb").write(pdf)
ok = len(doc.pages) >= 10 and dt < 5
print(f"T1 pages={len(doc.pages)} bytes={len(pdf)} seconds={dt:.2f} {'PASS' if ok else 'FAIL'}")
