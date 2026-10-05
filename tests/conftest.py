import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from nlp_bot_scalable.api.dependencies import get_db
from nlp_bot_scalable.database.models import Base
from nlp_bot_scalable.main import app


@pytest.fixture
def db_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine):
    session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine,
    )
    session = session_factory()
    yield session
    session.close()


@pytest.fixture
def client(db_engine):
    session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine,
    )

    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
