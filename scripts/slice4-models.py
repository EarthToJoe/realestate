#!/usr/bin/env python3
"""Slice 4: record the whole demo walk's AI answers, so the hosted demo runs end to end on replays at $0.

  .venv/bin/python scripts/slice4-models.py record   reset, then every milestone of the walk (app/demo/walk.py, the
                                                      same plays as fast-forward and "Do this screen for me"),
                                                      steps 1 to 10 in walk order; replay first, a miss goes live
                                                      and is recorded into replays/ (committed; masked, no PII)
  .venv/bin/python scripts/slice4-models.py check    the same walk with no key: fails on any replay miss

Uses the key at /srv/realestate/secrets/ANTHROPIC_API_KEY (never printed). Every live call is logged with its cost
in the model_call table of tmp/slice4-models/, and summed here.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def main(mode: str) -> int:
    if mode == "record":
        os.environ["REALESTATE_RECORD_TO_REPO"] = "1"
    from app import db
    from app.config import Settings
    from app.demo import walk
    from app.main import create_app
    from app.models import ModelCall

    data = ROOT / "tmp" / "slice4-models"
    shutil.rmtree(data, ignore_errors=True)
    secrets = Path("/srv/realestate/secrets") if mode == "record" else ROOT / "tmp" / "no-secrets"
    app = create_app(Settings(data_dir=data, model_mode="replay", secrets_dir=secrets,
                              review_dir=ROOT / "tmp" / "no-review"))
    provider = app.state.provider
    db.reset_all()
    s = db.new_session()
    try:
        played = walk.play_screen(s, provider, walk.WALK[-1].route)
        calls = s.query(ModelCall).all()
        live = [c for c in calls if c.mode == "live"]
        print(f"played {len(played)} milestones: {' '.join(m.key for m in played)}")
        print(f"model calls: {len(calls)} ({len(live)} live, {len(calls) - len(live)} replayed)")
        for c in live:
            print(f"  live {c.task:24} {c.model:18} in {c.input_tokens:6} out {c.output_tokens:6} ${c.cost_usd:.4f}")
        print(f"live cost of this run: ${sum(c.cost_usd for c in live):.4f}")
        # the data dir is rebuilt on every run: keep the live calls in a ledger that survives it
        ledger = ROOT / "tmp" / "slice4-live-calls.jsonl"
        with ledger.open("a") as f:
            for c in live:
                f.write(json.dumps({"ts": c.ts.isoformat(), "task": c.task, "model": c.model, "in": c.input_tokens,
                                    "out": c.output_tokens, "cost_usd": c.cost_usd}) + "\n")
        return 0 if (mode == "record" or not live) else 1
    finally:
        s.close()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "check"))
