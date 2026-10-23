"""PII as a first-class concern (spec section 6).

- `pii_column(category)` marks a column as PII and encrypts it with Fernet.
- `registry()` lists every PII column, built from the model metadata; masking, the access log and export use it.
- `Masker` hides known personal values plus e-mail and phone patterns (logs, model requests).
- `tokenize` / `detokenize` swap people's names for tokens such as [SELLER_1] before a model call and put the
  real values back only in rendered output (try-first check T6).
"""

from __future__ import annotations

import os
import re
import threading
from dataclasses import dataclass, field
from pathlib import Path

from cryptography.fernet import Fernet
from sqlalchemy import String
from sqlalchemy.types import TypeDecorator

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}(?!\d)")

_fernet: Fernet | None = None
_lock = threading.Lock()


def configure_key(secret_value: str | None, data_dir: Path) -> None:
    """Use the PII_KEY secret; locally (no secret) generate one in the data dir, mode 600."""
    global _fernet
    key = secret_value
    if not key:
        path = data_dir / "pii.key"
        if not path.exists():
            path.write_text(Fernet.generate_key().decode())
            os.chmod(path, 0o600)
        key = path.read_text().strip()
    _fernet = Fernet(key.encode())


def fernet() -> Fernet:
    if _fernet is None:
        raise RuntimeError("PII key not configured: call pii.configure_key() at start-up")
    return _fernet


class EncryptedString(TypeDecorator):
    """A string column stored Fernet-encrypted; decrypted on read."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return fernet().encrypt(str(value).encode()).decode()

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return fernet().decrypt(value.encode()).decode()


def pii_column_info(category: str) -> dict:
    return {"pii": category}


def registry(base) -> dict[str, list[tuple[str, str]]]:
    """{table: [(column, category), ...]} for every column marked info={'pii': ...}."""
    out: dict[str, list[tuple[str, str]]] = {}
    for table in base.metadata.sorted_tables:
        cols = [(c.name, c.info["pii"]) for c in table.columns if "pii" in c.info]
        if cols:
            out[table.name] = cols
    return out


@dataclass
class Masker:
    """Masks known personal values (names, addresses) and any e-mail or phone pattern."""

    known: dict[str, str] = field(default_factory=dict)  # value -> replacement label

    def register(self, value: str | None, label: str) -> None:
        if value and len(value.strip()) >= 3:
            with _lock:
                self.known[value.strip()] = label

    def mask(self, text: str) -> str:
        if not text:
            return text
        for value in sorted(self.known, key=len, reverse=True):
            text = re.sub(re.escape(value), self.known[value], text, flags=re.IGNORECASE)
        text = EMAIL_RE.sub("[EMAIL]", text)
        text = PHONE_RE.sub("[PHONE]", text)
        return text

    def mask_obj(self, obj):
        if isinstance(obj, str):
            return self.mask(obj)
        if isinstance(obj, dict):
            return {k: self.mask_obj(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [self.mask_obj(v) for v in obj]
        return obj


# One process-wide masker: the seed and every person write register their values here.
MASKER = Masker()


def tokenize(text: str, people: dict[str, dict[str, str | None]]) -> tuple[str, dict[str, str]]:
    """Replace each person's name, e-mail and phone with tokens.

    people: {"SELLER_1": {"name": "...", "email": "...", "phone": "..."}, ...}
    Returns (masked_text, {token: real_value}) so `detokenize` can restore the values in rendered output.
    Any e-mail or phone left over (not belonging to a known person) is masked without a way back.
    """
    mapping: dict[str, str] = {}
    for token, fields in people.items():
        for kind, value in fields.items():
            if not value:
                continue
            tok = f"[{token}]" if kind == "name" else f"[{token}_{kind.upper()}]"
            mapping[tok] = value
            text = re.sub(re.escape(value), tok, text, flags=re.IGNORECASE)
            if kind == "name":  # first names on their own ("Hi Maria,")
                first = value.split()[0]
                if len(first) >= 3:
                    text = re.sub(rf"\b{re.escape(first)}\b", tok, text)
    text = EMAIL_RE.sub("[EMAIL]", text)
    text = PHONE_RE.sub("[PHONE]", text)
    return text, mapping


def detokenize(text: str, mapping: dict[str, str]) -> str:
    for tok in sorted(mapping, key=len, reverse=True):
        text = text.replace(tok, mapping[tok])
    return text
