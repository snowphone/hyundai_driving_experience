from __future__ import annotations

import os
from typing import (
    Any,
    Iterable,
)

from dotenv import load_dotenv
from sqlalchemy import (
    Column,
    DateTime,
    String,
    create_engine,
    desc,
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)
from sqlalchemy.sql.functions import now

load_dotenv()

engine = create_engine(os.getenv("DB_URL"))  # type: ignore
Base: Any = declarative_base(bind=engine)


def session_scope():
    sess = sessionmaker(bind=engine, future=True)
    return sess.begin()


class History(Base):
    __tablename__ = "history"

    datetime = Column(DateTime(timezone=True), primary_key=True, default=now())
    text = Column(String, nullable=False)

    @classmethod
    def store(cls, texts: Iterable[str]):
        text = "\n".join(texts)
        with session_scope() as sess:
            sess.add(History(text=text))

    @classmethod
    def get_latest(cls) -> set[str]:
        with session_scope() as sess:
            latest: History | None = (
                sess.query(History).order_by(desc(History.datetime)).first()
            )
            if latest is None:
                return set()
            return set(latest.text.splitlines())  # type: ignore


Base.metadata.create_all(engine)
