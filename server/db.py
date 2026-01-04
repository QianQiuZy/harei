import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from server.models.base import Base

_engine = None
_Session = None


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", "mysql+pymysql://root:password@127.0.0.1:3306/harei")


def init_db() -> None:
    global _engine, _Session
    if _engine is None:
        _engine = create_engine(get_database_url(), pool_pre_ping=True)
        _Session = scoped_session(sessionmaker(bind=_engine, autocommit=False, autoflush=False))
        Base.metadata.create_all(_engine)


def get_session():
    if _Session is None:
        init_db()
    return _Session


@contextmanager
def session_scope():
    session = get_session()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
