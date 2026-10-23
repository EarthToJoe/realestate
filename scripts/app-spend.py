#!/usr/bin/env python3
"""Rolls the app's own model calls (the `model_call` table: module, task, model, tokens, cost, mode) up into
docs/SPEND-LOG.md (SC "Spend"), between the markers <!-- app-spend:begin --> and <!-- app-spend:end -->.

  .venv/bin/python scripts/app-spend.py            the hosted app's database (/srv/realestate/data, SQLCipher with
                                                    the DB_KEY secret; read only) plus the local recording ledger
                                                    tmp/slice4-live-calls.jsonl; rewrites the section
  .venv/bin/python scripts/app-spend.py --print    print the section, change nothing

The hosted table keeps every call since the container's database was created (Start demo keeps the spend log).
Recordings made locally (scripts/slice*-models.py) are in their own run databases; the slice-4 recorder appends its
live calls to the ledger, and the earlier ones are in the hand-kept table above the section.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
LOG = ROOT / "docs" / "SPEND-LOG.md"
LEDGER = ROOT / "tmp" / "slice4-live-calls.jsonl"
BEGIN, END = "<!-- app-spend:begin -->", "<!-- app-spend:end -->"


def hosted_rows() -> list[dict]:
    from sqlalchemy import create_engine, text

    from app.config import Settings

    st = Settings(data_dir=Path("/srv/realestate/data"), secrets_dir=Path("/srv/realestate/secrets"))
    eng = create_engine(st.db_url)
    with eng.connect() as c:
        rows = c.execute(text("select ts, module, task, model, mode, input_tokens, cache_write_tokens, "
                              "cache_read_tokens, output_tokens, cost_usd from model_call")).mappings().all()
    return [dict(r) for r in rows]


def ledger_rows() -> list[dict]:
    if not LEDGER.exists():
        return []
    return [json.loads(ln) for ln in LEDGER.read_text().splitlines() if ln.strip()]


def section(hosted: list[dict], ledger: list[dict]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    by_mode = defaultdict(lambda: [0, 0.0])
    live = defaultdict(lambda: [0, 0, 0, 0, 0, 0.0])
    for r in hosted:
        by_mode[r["mode"]][0] += 1
        by_mode[r["mode"]][1] += r["cost_usd"] or 0
        if r["mode"] == "live":
            k = live[(r["task"], r["model"])]
            k[0] += 1
            for i, f in enumerate(("input_tokens", "cache_write_tokens", "cache_read_tokens", "output_tokens"), 1):
                k[i] += r[f] or 0
            k[5] += r["cost_usd"] or 0
    total_live = sum(v[5] for v in live.values())
    led = sum(r["cost_usd"] for r in ledger)
    lines = [BEGIN, "", f"### The app's own calls, rolled up by `scripts/app-spend.py` ({now})", "",
             "**Hosted app** (`model_call` in the container's database, every call since it was created):", "",
             "| Mode | Calls | Cost (USD) |", "|---|---|---|"]
    for mode in sorted(by_mode):
        lines.append(f"| {mode} | {by_mode[mode][0]:,} | {by_mode[mode][1]:.4f} |")
    if live:
        lines += ["", "Live calls on the hosted app, by task:", "",
                  "| Task | Model | Calls | In | Cache write | Cache read | Out | Cost (USD) |",
                  "|---|---|---|---|---|---|---|---|"]
        for (task, model), v in sorted(live.items()):
            lines.append(f"| {task} | {model} | {v[0]} | {v[1]:,} | {v[2]:,} | {v[3]:,} | {v[4]:,} | {v[5]:.4f} |")
    lines += ["", f"**Hosted live spend: ${total_live:.4f}** of the $12 app cap (the footer of every page shows the "
                  "same figure).", ""]
    if ledger:
        lines += [f"**Local recordings logged by `scripts/slice4-models.py`** ({len(ledger)} live calls): "
                  f"${led:.4f}.", ""]
    lines.append(END)
    return "\n".join(lines)


def main() -> int:
    try:
        hosted = hosted_rows()
    except Exception as e:  # no access to the server's database (a laptop): roll up the ledger only
        print(f"hosted database not readable here ({type(e).__name__}); ledger only")
        hosted = []
    text = section(hosted, ledger_rows())
    if "--print" in sys.argv:
        print(text)
        return 0
    doc = LOG.read_text()
    if BEGIN in doc and END in doc:
        doc = doc[:doc.index(BEGIN)] + text + doc[doc.index(END) + len(END):]
    else:
        anchor = "## 2026-10-23, morning:"
        doc = doc.replace(anchor, text + "\n\n" + anchor, 1) if anchor in doc else doc.rstrip() + "\n\n" + text + "\n"
    LOG.write_text(doc)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
