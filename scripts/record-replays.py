#!/usr/bin/env python3
"""Records the demo's model answers with live calls, into replays/ (committed; masked, no PII).

   .venv/bin/python scripts/record-replays.py            intake inference + the T6 masking probe
Uses the key from /srv/realestate/secrets/ANTHROPIC_API_KEY (never printed). Each live call is logged in the
model_call table of the local data dir (tmp/data) with its cost, and printed here. Replays are keyed by the
masked request hash, so a demo run with the demo-house inputs replays them at no cost.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["REALESTATE_RECORD_TO_REPO"] = "1"

from pydantic import BaseModel  # noqa: E402

from app import db, pii  # noqa: E402
from app.config import Settings  # noqa: E402
from app.model.provider import AnthropicProvider, ReplayStore, SHIPPED_REPLAYS, live_spend  # noqa: E402
from app.models import ModelCall  # noqa: E402
from app.modules.intake import service  # noqa: E402


class Reply(BaseModel):
    reply: str
    tokens_seen: list[str]


def main() -> None:
    settings = Settings(data_dir=Path("tmp/record-data"))
    key = settings.secret("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("No key readable at /srv/realestate/secrets/ANTHROPIC_API_KEY")
    pii.configure_key(None, settings.data_dir)
    db.init_engine(settings.db_url)
    db.reset_all()
    live = AnthropicProvider(key, ReplayStore(SHIPPED_REPLAYS), settings.spend_cap_usd)
    with db.session_scope() as s:
        deal = service.start_intake(s, service.demo_input())
        r = service.infer_gaps(s, deal, live)
        print("intake.infer_gaps:", r.mode, r.model, f"${r.cost_usd:.5f}")
        print(json.dumps(r.output.model_dump(), indent=1)[:1500])
        # T6: a buyer message, masked before the call; real values only re-inserted in the output.
        msg = ("Hi, this is Sam Whitfield-Arora (sam.wa@example.com, 914-555-0187). Could I see the house on "
               "Saturday morning? Sam")
        masked, mapping = pii.tokenize(msg, {"BUYER_1": {"name": "Sam Whitfield-Arora", "email": "sam.wa@example.com",
                                                         "phone": "914-555-0187"}})
        t6 = live.generate("probe.mask_roundtrip", Reply, {"message": masked}, s=s, module="probe",
                           system="You answer a buyer enquiry for a listing in one or two sentences. Address the "
                                  "buyer by the token you see. List every [TOKEN] you saw in tokens_seen.",
                           prompt_version="t6.v1")
        print("probe.mask_roundtrip:", t6.mode, f"${t6.cost_usd:.5f}")
        print("  masked request:", masked)
        print("  model reply   :", t6.output.reply)
        print("  rendered      :", pii.detokenize(t6.output.reply, mapping))
        rows = s.query(ModelCall).all()
        print("model_call rows:", [(m.task, m.model, m.input_tokens, m.output_tokens, m.cache_write_tokens,
                                    m.cache_read_tokens, m.cost_usd, m.latency_ms) for m in rows])
        print(f"live spend logged: ${live_spend(s):.5f}")


if __name__ == "__main__":
    main()
