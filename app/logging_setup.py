"""Application logs through structlog, with a processor that keeps PII out (spec section 6).

The processor drops any key named after a PII-registry column and masks known personal values plus e-mail and
phone patterns in every remaining value.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import structlog

from app.pii import MASKER

PII_KEYS: set[str] = set()


def set_pii_keys(keys: set[str]) -> None:
    PII_KEYS.clear()
    PII_KEYS.update(keys)


def mask_pii(_, __, event_dict: dict) -> dict:
    for key in list(event_dict):
        if key in PII_KEYS:
            event_dict[key] = "[PII REMOVED]"
        else:
            event_dict[key] = MASKER.mask_obj(event_dict[key])
    return event_dict


def configure(log_file: Path | None = None) -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))
    logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=handlers, force=True)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            mask_pii,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=False,
    )


log = structlog.get_logger("realestate")
