"""Database engine and session. SQLite, one file; the POC rebuilds from the seed (no migrations)."""

from __future__ import annotations

from contextlib import contextmanager

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    pass


_engine = None
_Session: sessionmaker | None = None

# The audit log is append-only: SQLite refuses UPDATE and DELETE on it.
AUDIT_TRIGGERS = [
    """CREATE TRIGGER IF NOT EXISTS events_no_update BEFORE UPDATE ON events
       BEGIN SELECT RAISE(ABORT, 'events is append-only'); END""",
    """CREATE TRIGGER IF NOT EXISTS events_no_delete BEFORE DELETE ON events
       BEGIN SELECT RAISE(ABORT, 'events is append-only'); END""",
]


def init_engine(url: str):
    global _engine, _Session
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    kwargs = {}
    if url.startswith("sqlite+pysqlcipher"):
        import sqlcipher3

        kwargs["module"] = sqlcipher3
    _engine = create_engine(url, connect_args=connect_args, hide_parameters=True, **kwargs)
    if url.startswith("sqlite"):

        @event.listens_for(_engine, "connect")
        def _pragmas(dbapi_conn, _):
            cur = dbapi_conn.cursor()
            cur.execute("PRAGMA foreign_keys=ON")
            cur.execute("PRAGMA journal_mode=WAL")
            cur.close()

    _Session = sessionmaker(bind=_engine, expire_on_commit=False)
    return _engine


def engine():
    return _engine


def create_all() -> None:
    from app import models  # noqa: F401  (register tables)

    Base.metadata.create_all(_engine)
    with _engine.begin() as conn:
        for ddl in AUDIT_TRIGGERS:
            conn.execute(text(ddl))


# Kept across a demo reset: the spend log, so the spend cap counts every live call ever made.
KEEP_ON_RESET = {"model_call"}


def reset_all() -> None:
    """Rebuild every table from scratch except the spend log."""
    from app import models  # noqa: F401

    with _engine.begin() as conn:
        conn.execute(text("DROP TRIGGER IF EXISTS events_no_update"))
        conn.execute(text("DROP TRIGGER IF EXISTS events_no_delete"))
    tables = [t for t in Base.metadata.sorted_tables if t.name not in KEEP_ON_RESET]
    Base.metadata.drop_all(_engine, tables=tables)
    create_all()


def new_session() -> Session:
    return _Session()


@contextmanager
def session_scope():
    s = new_session()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()


def get_session():
    """FastAPI dependency: one session per request; commit on success, roll back on any refusal or error."""
    s = new_session()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()
