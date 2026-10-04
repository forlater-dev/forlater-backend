from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from api.config import DATABASE_URL
from api import models  # noqa: F401 -- Register tables before creating the schema.

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
