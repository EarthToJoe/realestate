"""T2: sqlcipher3 with SQLAlchemy: create, encrypt, reopen (and a wrong key fails)."""
import os
import tempfile

from sqlalchemy import create_engine, text

path = os.path.join(tempfile.mkdtemp(), "t2.db")


def engine(key):
    import sqlcipher3

    return create_engine(f"sqlite+pysqlcipher://:{key}@/{path}", module=sqlcipher3)


with engine("k1").begin() as c:
    c.execute(text("create table t (x text)"))
    c.execute(text("insert into t values ('secret value')"))
raw = open(path, "rb").read()
assert b"secret value" not in raw and not raw.startswith(b"SQLite format 3"), "file is not encrypted"
with engine("k1").connect() as c:
    assert c.execute(text("select x from t")).scalar() == "secret value"
try:
    with engine("wrong").connect() as c:
        c.execute(text("select x from t")).scalar()
    print("T2 FAIL: wrong key opened the file")
except Exception as ex:
    print(f"T2 PASS: encrypted on disk, reopened with the key, wrong key refused ({type(ex).__name__})")
