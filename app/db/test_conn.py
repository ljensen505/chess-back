import os

from .conn import connect_db


def test_env():
    assert os.getenv("DB_HOST") is not None
    assert os.getenv("DB_USER") is not None
    assert os.getenv("DB_PASSWORD") is not None
    assert os.getenv("DB_DATABASE") is not None


def test_connect_db():
    db = connect_db()
    assert db.is_connected() is True
    db.close()
    assert db.is_connected() is False
