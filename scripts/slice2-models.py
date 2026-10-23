#!/usr/bin/env python3
"""Slice 2 live model work. Uses the key at /srv/realestate/secrets/ANTHROPIC_API_KEY (never printed); every live
call is logged with its cost in the model_call table of the data dir used, and summed here.

  .venv/bin/python scripts/slice2-models.py compare   Haiku vs Sonnet on pricing.recommend and copy.draft, the
                                                       demo-house flow through the real screens; writes
                                                       docs/build/model-side-by-side-slice2.md (replays to tmp/)
  .venv/bin/python scripts/slice2-models.py record    the demo run for steps 2 to 4 with config/models.yaml as
                                                       it stands, recorded into replays/ (committed; masked, no PII)
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient  # noqa: E402

from app import db  # noqa: E402
from app.config import Settings  # noqa: E402
from app.models import ModelCall  # noqa: E402

HAIKU, SONNET = "claude-haiku-5-5", "claude-sonnet-5-5"


def make_client(data_dir: Path, mode: str = "live") -> TestClient:
    """live: every call goes to the API. replay: recorded answers first; a miss goes live and is recorded."""
    from app.main import create_app

    shutil.rmtree(data_dir, ignore_errors=True)
    settings = Settings(data_dir=data_dir, model_mode=mode, review_dir=ROOT / "tmp" / "no-review")
    app = create_app(settings)
    p = app.state.provider
    if (p.live if mode == "replay" else p if p.mode == "live" else None) is None:
        sys.exit("No key readable at /srv/realestate/secrets/ANTHROPIC_API_KEY")
    db.reset_all()
    return TestClient(app)


def persona(c: TestClient, p: str) -> None:
    c.cookies.set("persona", p)


def demo_flow(c: TestClient, plant: bool = True) -> dict:
    """Steps 1 to 4 exactly as the demo script clicks them."""
    from app.modules.intake.service import demo_input
    from app.modules.listing_copy import service as copy_service
    from app.modules.pricing import service as pricing
    from app.web import current_deal

    d = demo_input()
    persona(c, "presenter")
    c.post("/intake", data={"street": d.street, "city": d.city, "zip": d.zip, "seller_name": d.seller_name,
                            "seller_email": d.seller_email, "seller_phone": d.seller_phone, **d.facts})
    c.post("/intake/infer")
    persona(c, "seller")
    c.post("/intake/agency", data={"decision": "acknowledge"})
    persona(c, "presenter")
    c.post("/intake/accept")
    persona(c, "seller")
    c.post("/intake/sign", data={"decision": "sign"})
    persona(c, "presenter")
    c.get("/pricing")
    c.post("/pricing/recommend")
    s = db.new_session()
    try:
        pa = pricing.current(s, current_deal(s))
        advice, summary = pa.advice, pa.summary
    finally:
        s.close()
    persona(c, "seller")
    c.post("/pricing/choose", data={"price": str(advice["recommended_price"])})
    persona(c, "presenter")
    c.post("/copy/draft")
    s = db.new_session()
    try:
        deal = current_deal(s)
        arts = copy_service.artifacts(s, deal)
        portal_id = next(a.id for a in arts if a.channel == "portal")
    finally:
        s.close()
    if plant:
        c.post(f"/copy/{portal_id}/plant")
        c.post(f"/copy/{portal_id}/fix")
    c.post("/copy/ready-all")
    c.get("/channels")
    persona(c, "seller")
    c.post("/channels/authorise", data={"decision": "sign", "exposure": "Publish to Internet",
                                        "granted": ["cooperating_brokers", "lockbox", "photographer"]})
    persona(c, "presenter")
    c.post("/channels/mls-entry")
    from app.fairhousing import check as fh

    s = db.new_session()
    try:
        deal = current_deal(s)
        out = {"advice": advice, "range": [summary["range_low"], summary["range_high"]],
               "indicated": summary["indicated_value"], "copy": [], "calls": []}
        for a in copy_service.artifacts(s, deal):
            res = fh.latest_result(s, "copy_artifact", a.id)
            out["copy"].append({"channel": a.channel, "version": a.version, "status": a.status, "text": a.text,
                                "findings": [(f["rule_id"], f["tier"], f["phrase"], f["source"]) for f in res.findings]})
        for m in s.query(ModelCall).filter(ModelCall.mode == "live").all():
            out["calls"].append({"task": m.task, "model": m.model, "in": m.input_tokens, "out": m.output_tokens,
                                 "cache_r": m.cache_read_tokens, "cache_w": m.cache_write_tokens,
                                 "cost": m.cost_usd, "ms": m.latency_ms})
    finally:
        s.close()
    return out


def compare() -> None:
    import app.model.provider as prov

    original = prov.task_config
    results = {}
    for model in (HAIKU, SONNET):
        def cfg(task, _m=model):
            c = dict(original(task))
            if task in ("pricing.recommend", "copy.draft"):
                c["model"] = _m
            return c

        prov.task_config = cfg
        c = make_client(ROOT / "tmp" / f"compare-{model}")
        results[model] = demo_flow(c, plant=False)
    prov.task_config = original
    write_report(results)


def write_report(results: dict) -> None:
    lines = ["# Model side-by-side, slice 2 (pricing advice and listing copy)", "",
             "Generated by `scripts/slice2-models.py compare` on the demo house, through the real screens, live. "
             "Same inputs for both models; the fair-housing review pass is Haiku in both runs (spec section 7). "
             "Costs are from the app's own `model_call` log.", ""]
    for model, r in results.items():
        calls = [x for x in r["calls"] if x["task"] in ("pricing.recommend", "copy.draft")]
        fh_calls = [x for x in r["calls"] if x["task"] == "fairhousing.review"]
        lines += [f"## {model}", "",
                  "| Task | Input tok | Output tok | Cost USD | Latency ms |", "|---|---|---|---|---|"]
        for x in calls:
            lines.append(f"| {x['task']} | {x['in']} | {x['out']} | {x['cost']:.4f} | {x['ms']} |")
        lines.append(f"| fairhousing.review x{len(fh_calls)} (Haiku) | {sum(x['in'] for x in fh_calls)} | "
                     f"{sum(x['out'] for x in fh_calls)} | {sum(x['cost'] for x in fh_calls):.4f} | "
                     f"{max([x['ms'] for x in fh_calls] or [0])} max |")
        a = r["advice"]
        lines += ["", f"**Range** ${r['range'][0]:,} to ${r['range'][1]:,}, indicated ${r['indicated']:,}. "
                      f"**Recommended** ${a['recommended_price']:,}.", "",
                  f"**Method.** {a['method_plain']}", "", f"**Reasoning.** {a['reasoning']}", "",
                  "**Weak comps.** " + "; ".join(f"#{w['rank']}: {w['why']}" for w in a["weak_comps"]), "",
                  "**Would change it.** " + "; ".join(a["things_that_would_change_it"]), ""]
        for cp in r["copy"]:
            lines += [f"**{cp['channel']}** (v{cp['version']}, {cp['status']}; findings: "
                      f"{cp['findings'] or 'none'})", "", "> " + cp["text"].replace("\n", "\n> "), ""]
    out = ROOT / "docs" / "build" / "model-side-by-side-slice2.md"
    out.write_text("\n".join(lines) + "\n")
    total = sum(x["cost"] for r in results.values() for x in r["calls"])
    print(f"wrote {out}; live cost of the comparison ${total:.4f}")


def record() -> None:
    os.environ["REALESTATE_RECORD_TO_REPO"] = "1"
    c = make_client(ROOT / "tmp" / "record-slice2", mode="replay")
    r = demo_flow(c, plant=True)
    print(json.dumps({"advice": r["advice"]["recommended_price"], "range": r["range"],
                      "copy": [(x["channel"], x["version"], x["status"], x["findings"]) for x in r["copy"]]}, indent=1))
    total = sum(x["cost"] for x in r["calls"])
    print(f"live calls {len(r['calls'])}, cost ${total:.4f}")


if __name__ == "__main__":
    {"compare": compare, "record": record}[sys.argv[1] if len(sys.argv) > 1 else "compare"]()
