#!/usr/bin/env python3
"""Slice 3 live model work. Uses the key at /srv/realestate/secrets/ANTHROPIC_API_KEY (never printed); every live
call is logged with its cost in the model_call table of the data dir used, and summed here.

  .venv/bin/python scripts/slice3-models.py record    the whole demo walk (steps 1 to 8, in the walk order of
                                                       app/demo/steps.yaml, as scripts/live-flow.sh clicks it) with
                                                       config/models.yaml as it stands, replay first, misses live
                                                       and recorded into replays/ (committed; masked, no PII)
  .venv/bin/python scripts/slice3-models.py compare   the contract draft by Opus 5.5 against the recorded Sonnet 5.5
                                                       draft on the same inputs (the walk replays up to the draft);
                                                       writes docs/build/model-side-by-side-slice3.md
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

spec = importlib.util.spec_from_file_location("slice2", ROOT / "scripts" / "slice2-models.py")
slice2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(slice2)

from app import db  # noqa: E402
from app.models import ModelCall  # noqa: E402

OPUS, SONNET = "claude-opus-5-5", "claude-sonnet-5-5"
persona = slice2.persona


def _form_value(html: str, name: str) -> str:
    m = re.search(rf'name="{name}"[^>]*value="([^"]*)"', html)
    return m.group(1) if m else ""


def walk_5_to_8(c, until_draft: bool = False) -> dict:
    """Steps 5, 8, 6 and 7 in the demo's walk order, exactly as scripts/live-flow.sh clicks them."""
    log = []
    # Step 5
    c.get("/inbox")
    persona(c, "seller")
    c.post("/inbox/approve", data={"decision": "approve", "self_guided": "yes"})
    persona(c, "presenter")
    c.post("/inbox/all")
    # Step 8: intake, agreement, search alert, tour, consents, offer
    from app.modules.buyer.service import demo_input
    c.post("/buyer", data=demo_input())
    persona(c, "buyer")
    c.post("/buyer/sign", data={"decision": "sign"})
    persona(c, "presenter")
    c.post("/buyer/alert")
    c.post("/buyer/tour", data={"kind": "self-guided"})
    for p in ("buyer", "seller"):
        persona(c, p)
        c.post("/buyer/consent", data={"decision": "consent"})
    persona(c, "presenter")
    c.post("/buyer/offer/advise")
    persona(c, "buyer")
    c.post("/buyer/offer/approve", data={"decision": "approve"})
    # Step 6: advice, the seller's counter at the AI's suggested figures, the AI sends it
    persona(c, "presenter")
    c.post("/offers/advise")
    persona(c, "seller")
    page = c.get("/offers").text
    form = {k: _form_value(page, k) for k in ("counter_price", "lowest_price", "closing_days", "closing_min",
                                              "closing_max", "inspection_max", "mortgage_max")}
    offer = re.search(r'<option selected>([AB])</option>', page)
    form.update(decision="counter", offer=offer.group(1) if offer else "B")
    log.append({"seller_decision": form})
    c.post("/offers/decide", data=form)
    persona(c, "presenter")
    c.post("/offers/negotiate")
    # the buyer's replies until agreed (the seller's AI answers each on its own)
    for _ in range(5):
        if 'id="accepted"' in c.get("/offers").text or form["offer"] != "B":
            break
        c.post("/buyer/counter/advise")
        persona(c, "buyer")
        c.post("/buyer/counter/approve", data={"decision": "approve"})
        persona(c, "presenter")
    if 'id="accepted"' not in c.get("/offers").text and form["offer"] == "A":
        c.post("/offers/negotiate")
    log.append({"agreed": 'id="accepted"' in c.get("/offers").text})
    # Step 7: draft before the PCDS (the refusal is part of the demo), then the PCDS, attach, sign
    c.post("/contract/draft")
    if until_draft:
        return {"log": log}
    c.post("/contract/open-signing")
    persona(c, "seller")
    c.post("/disclosures/pcds/prepared")
    persona(c, "presenter")
    c.post("/contract/attach")
    c.post("/contract/open-signing")
    for p in ("seller", "buyer"):
        persona(c, p)
        c.post("/contract/sign", data={"decision": "sign"})
    persona(c, "presenter")
    return {"log": log}


def _state():
    from app.modules.contract import service as contract
    from app.modules.offers import service as offers
    from app.modules.buyer import service as buyer
    from app.web import current_deal
    s = db.new_session()
    try:
        deal = current_deal(s)
        calls = [{"task": m.task, "model": m.model, "in": m.input_tokens, "out": m.output_tokens,
                  "cost": m.cost_usd, "ms": m.latency_ms} for m in s.query(ModelCall).filter(ModelCall.mode == "live")]
        return {"offers": offers.state(deal), "buyer": buyer.state(deal), "contract": contract.state(deal),
                "calls": calls}
    finally:
        s.close()


def record() -> None:
    os.environ["REALESTATE_RECORD_TO_REPO"] = "1"
    c = slice2.make_client(ROOT / "tmp" / "record-slice3", mode="replay")
    slice2.demo_flow(c, plant=True)
    out = walk_5_to_8(c)
    st = _state()
    acc = st["offers"].get("accepted") or {}
    print(json.dumps({"walk": out["log"], "accepted": {k: acc.get(k) for k in ("label", "final_price", "closing_days",
                                                                                 "agreed_by")},
                      "thread": [(t["from"], t["terms"]["price"]) for t in st["offers"].get("thread", [])],
                      "contract": {k: st["contract"].get(k) for k in ("version", "passed", "model", "mode")},
                      "findings": st["contract"].get("findings")}, indent=1))
    total = sum(x["cost"] for x in st["calls"])
    print(f"live calls {len(st['calls'])}, cost ${total:.4f}")
    for x in st["calls"]:
        print(f"  {x['task']:24} {x['model']:18} in {x['in']:6} out {x['out']:6} ${x['cost']:.4f} {x['ms']} ms")


def compare() -> None:
    """Opus on the contract; everything before it replays the recorded walk (same inputs)."""
    import app.model.provider as prov
    from app.modules.contract import service as contract

    original = prov.task_config
    results = {}
    for model in (SONNET, OPUS):
        def cfg(task, _m=model):
            conf = dict(original(task))
            if task == "contract.draft":
                conf["model"] = _m
            return conf
        prov.task_config = cfg
        c = slice2.make_client(ROOT / "tmp" / f"compare3-{model}", mode="replay")
        slice2.demo_flow(c, plant=True)
        t0 = time.monotonic()
        walk_5_to_8(c, until_draft=True)
        st = _state()
        call = next((x for x in st["calls"] if x["task"] == "contract.draft"), None)
        results[model] = {"contract": st["contract"], "call": call, "secs": round(time.monotonic() - t0, 1),
                          "accepted": st["offers"].get("accepted")}
        # every other call should have replayed
        results[model]["other_live"] = [x["task"] for x in st["calls"] if x["task"] != "contract.draft"]
    prov.task_config = original
    write_report(results)


def write_report(results: dict) -> None:
    from app.modules.contract import service as contract
    lines = ["# Model side-by-side, slice 3 (the contract draft)", "",
             "Generated by `scripts/slice3-models.py compare` on the demo house, through the real screens. The walk "
             "replays the recorded run up to the contract step, so both models draft from the same accepted offer and "
             "the same deal facts; only `contract.draft` differs. Costs and tokens are from the app's own "
             "`model_call` log (a recorded draft shows no new cost: see the record run's line in `docs/SPEND-LOG.md`).",
             ""]
    lines += ["| | " + " | ".join(results) + " |", "|---|" + "---|" * len(results)]

    def row(name, f):
        lines.append(f"| {name} | " + " | ".join(str(f(r)) for r in results.values()) + " |")
    row("Body clauses", lambda r: len(r["contract"]["draft"]["sections"]))
    row("Rider clauses", lambda r: len(r["contract"]["draft"]["rider"]))
    row("Words (body + rider)", lambda r: sum(len((c["text"] + " " + c["heading"]).split())
                                              for c in r["contract"]["draft"]["sections"] + r["contract"]["draft"]["rider"]))
    row("Side-by-side rows", lambda r: len(r["contract"]["draft"]["side_by_side"]))
    row("Code checks", lambda r: "passed" if r["contract"]["passed"] else "block")
    row("Findings", lambda r: "; ".join(f"{f['tier']} {f['rule']}" for f in r["contract"]["findings"]) or "none")
    row("Input / output tokens", lambda r: f"{r['call']['in']:,} / {r['call']['out']:,}" if r["call"] else "replayed")
    row("Cost", lambda r: f"${r['call']['cost']:.3f}" if r["call"] else "replayed")
    row("Latency", lambda r: f"{r['call']['ms'] / 1000:.0f} s" if r["call"] else "replayed")
    row("Other live calls (should be none)", lambda r: ", ".join(r["other_live"]) or "none")
    lines.append("")
    for model, r in results.items():
        d = r["contract"]["draft"]
        lines += [f"## {model}", "", f"**{d['title']}**", ""]
        for c in d["sections"] + d["rider"]:
            lines.append(f"- **{c['number']}. {c['heading']}.** {c['text']}")
        lines += ["", "Side by side:", ""]
        for row_ in contract.side_by_side(d):
            lines.append(f"- {row_['n']}. {row_['heading']}: {row_['draft_ref']}: {row_['note']}")
        lines += ["", "Notes to the parties: " + " / ".join(d.get("notes_to_parties") or []), ""]
    out = ROOT / "docs" / "build" / "model-side-by-side-slice3.md"
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out}")
    for model, r in results.items():
        print(model, json.dumps({k: r["contract"].get(k) for k in ("passed", "findings")}),
              r["call"] and {k: r["call"][k] for k in ("in", "out", "cost", "ms")}, r["other_live"])


if __name__ == "__main__":
    {"record": record, "compare": compare}[sys.argv[1] if len(sys.argv) > 1 else "record"]()
