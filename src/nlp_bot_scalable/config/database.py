from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from nlp_bot_scalable.config.settings import settings
from nlp_bot_scalable.database.models import Base


def _sqlite_connect_args(database_url: str) -> dict:
    if database_url.startswith("sqlite"):
        return {"connect_args": {"check_same_thread": False}}
    return {}


engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    **_sqlite_connect_args(settings.database_url),
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base.metadata.create_all(bind=engine)
