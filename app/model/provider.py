"""`ModelProvider.generate(task, schema, context)`: one schema-checked model call per AI step.

Three implementations behind one interface, so no screen changes when the provider does (SC "Modular"):
- `AnthropicProvider` (live): Anthropic SDK `messages.parse` with a Pydantic output schema; the fixed system
  prompt is cached. Refuses once the app's own logged live spend passes SPEND_CAP_USD. Records every response
  as a replay.
- `ReplayProvider`: answers from recorded responses keyed by the masked request hash; a miss falls back to live
  if a key exists, otherwise raises `ReplayMiss` (the screen shows a "not recorded" card).
- `FakeProvider`: deterministic answers for tests; keeps every request so tests can inspect what was sent.

Every call writes a `model_call` row (tokens, cost, latency, mode). Request bodies are masked before hashing
and before recording, and no prompt or response body is logged.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import yaml
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import ROOT
from app.logging_setup import log
from app.models import ModelCall
from app.pii import MASKER

MODELS_YAML = ROOT / "config" / "models.yaml"
SHIPPED_REPLAYS = ROOT / "replays"


class SpendCapReached(Exception):
    pass


class ReplayMiss(Exception):
    pass


@dataclass
class ModelResult:
    output: BaseModel
    mode: str  # live | replay | fake
    model: str
    cost_usd: float
    recorded_at: str | None = None  # for replays: when the live run was recorded


def models_config() -> dict:
    return yaml.safe_load(MODELS_YAML.read_text())


def task_config(task: str) -> dict:
    cfg = models_config()
    return cfg["tasks"].get(task) or {"model": "claude-haiku-5-5", "max_tokens": 1500}


def cost_usd(model: str, input_tokens: int, output_tokens: int, cache_write: int = 0, cache_read: int = 0) -> float:
    p = models_config()["prices"][model]
    return round((input_tokens * p["input"] + cache_write * p["cache_write"] + cache_read * p["cache_read"]
                  + output_tokens * p["output"]) / 1_000_000, 6)


def build_request(task: str, schema: type[BaseModel], context: dict, system: str, prompt_version: str) -> dict:
    """The exact, masked request: what is hashed, recorded and (for live) sent."""
    cfg = task_config(task)
    return {
        "task": task,
        "model": cfg["model"],
        "max_tokens": cfg.get("max_tokens", 1500),
        "prompt_version": prompt_version,
        "schema": schema.__name__,
        "system": MASKER.mask(system),
        "user": MASKER.mask(json.dumps(context, sort_keys=True, ensure_ascii=False, default=str)),
    }


def request_hash(req: dict) -> str:
    stable = {k: req[k] for k in ("task", "model", "prompt_version", "schema", "system", "user")}
    return hashlib.sha256(json.dumps(stable, sort_keys=True).encode()).hexdigest()


def live_spend(s: Session) -> float:
    total = s.execute(select(func.coalesce(func.sum(ModelCall.cost_usd), 0.0)).where(ModelCall.mode == "live"))
    return float(total.scalar_one())


class ModelProvider:
    mode = "base"

    def generate(self, task: str, schema: type[BaseModel], context: dict, *, s: Session, module: str,
                 system: str, prompt_version: str, side: str | None = None) -> ModelResult:
        req = build_request(task, schema, context, system, prompt_version)
        h = request_hash(req)
        t0 = time.monotonic()
        result, usage = self._call(req, h, schema, s)
        latency = int((time.monotonic() - t0) * 1000)
        s.add(ModelCall(module=module, task=task, side=side, model=req["model"], mode=result.mode,
                        prompt_version=prompt_version, request_hash=h, latency_ms=latency,
                        input_tokens=usage.get("input", 0), output_tokens=usage.get("output", 0),
                        cache_write_tokens=usage.get("cache_write", 0), cache_read_tokens=usage.get("cache_read", 0),
                        cost_usd=result.cost_usd))
        s.flush()
        log.info("model_call", module=module, task=task, side=side, mode=result.mode, model=req["model"],
                 cost_usd=result.cost_usd, latency_ms=latency, request_hash=h[:12])
        return result

    def _call(self, req: dict, h: str, schema: type[BaseModel], s: Session) -> tuple[ModelResult, dict]:
        raise NotImplementedError


class ReplayStore:
    """Recorded responses: JSON files named by request hash. Shipped ones live in replays/ (committed; masked,
    no PII); runtime recordings go to the write dir (the data volume in Docker)."""

    def __init__(self, write_dir: Path, read_dirs: list[Path] | None = None):
        self.write_dir = write_dir
        self.read_dirs = [write_dir] + [d for d in (read_dirs or [SHIPPED_REPLAYS]) if d != write_dir]

    def get(self, h: str) -> dict | None:
        for d in self.read_dirs:
            p = d / f"{h}.json"
            if p.exists():
                return json.loads(p.read_text())
        return None

    def put(self, h: str, req: dict, output: dict) -> None:
        self.write_dir.mkdir(parents=True, exist_ok=True)
        rec = {"request_hash": h, "task": req["task"], "model": req["model"], "prompt_version": req["prompt_version"],
               "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
               "output": MASKER.mask_obj(output), "request": req}
        (self.write_dir / f"{h}.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False))


class AnthropicProvider(ModelProvider):
    mode = "live"

    def __init__(self, api_key: str, store: ReplayStore, spend_cap_usd: float):
        import anthropic

        self.client = anthropic.Anthropic(api_key=api_key, max_retries=2)
        self.store = store
        self.cap = spend_cap_usd

    def _call(self, req, h, schema, s):
        spent = live_spend(s)
        if spent >= self.cap:
            raise SpendCapReached(f"Live model spend ${spent:.2f} has reached the ${self.cap:.2f} cap; use replay.")
        resp = self.client.messages.parse(
            model=req["model"],
            max_tokens=req["max_tokens"],
            system=[{"type": "text", "text": req["system"], "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": req["user"]}],
            output_format=schema,
        )
        parsed = resp.parsed_output
        if parsed is None:
            raise RuntimeError(f"{req['task']}: the model returned no parsable output (stop: {resp.stop_reason})")
        u = resp.usage
        usage = {"input": u.input_tokens or 0, "output": u.output_tokens or 0,
                 "cache_write": getattr(u, "cache_creation_input_tokens", 0) or 0,
                 "cache_read": getattr(u, "cache_read_input_tokens", 0) or 0}
        cost = cost_usd(req["model"], usage["input"], usage["output"], usage["cache_write"], usage["cache_read"])
        self.store.put(h, req, parsed.model_dump())
        return ModelResult(output=parsed, mode="live", model=req["model"], cost_usd=cost), usage


class ReplayProvider(ModelProvider):
    mode = "replay"

    def __init__(self, store: ReplayStore, live: AnthropicProvider | None = None):
        self.store = store
        self.live = live

    def _call(self, req, h, schema, s):
        rec = self.store.get(h)
        if rec is None:
            if self.live is not None:
                return self.live._call(req, h, schema, s)
            raise ReplayMiss(f"No recorded answer for {req['task']} with these inputs (request {h[:12]}).")
        out = schema.model_validate(rec["output"])
        return ModelResult(output=out, mode="replay", model=rec["model"], cost_usd=0.0,
                           recorded_at=rec.get("recorded_at")), {}


class FakeProvider(ModelProvider):
    """Deterministic answers for tests. `responders[task](context) -> dict` builds the output."""

    mode = "fake"

    def __init__(self, responders: dict[str, Callable[[dict], dict]] | None = None):
        self.responders = responders or {}
        self.requests: list[dict] = []

    def _call(self, req, h, schema, s):
        self.requests.append(req)
        context = json.loads(req["user"])
        if req["task"] in self.responders:
            data: Any = self.responders[req["task"]](context)
        else:
            from app.model import fakes

            data = fakes.default(req["task"], context)
        return ModelResult(output=schema.model_validate(data), mode="fake", model=req["model"], cost_usd=0.0), {}


def make_provider(settings) -> ModelProvider:
    """live: every call goes to the API. replay: recorded answers; a miss goes live if a key exists (spec 7).
    fake: tests. REALESTATE_RECORD_TO_REPO=1 writes recordings into replays/ so they can be committed."""
    write_dir = SHIPPED_REPLAYS if os.environ.get("REALESTATE_RECORD_TO_REPO") == "1" else settings.data_dir / "replays"
    store = ReplayStore(write_dir)
    mode = settings.resolved_model_mode()
    if mode == "fake":
        return FakeProvider()
    key = settings.secret("ANTHROPIC_API_KEY")
    live = AnthropicProvider(key, store, settings.spend_cap_usd) if key else None
    if mode == "live" and live is not None:
        return live
    return ReplayProvider(store, live=live)
