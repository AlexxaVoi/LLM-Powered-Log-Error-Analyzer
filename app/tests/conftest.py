import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models.base import BaseModel
from app.models.user import UserModel
from app.models.log import LogModel
from unittest.mock import patch, AsyncMock

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="function")
def db():
    BaseModel.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        BaseModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def user(db):
    user = UserModel(
        username="test_user",
        password="test123"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def log_in_db(db, user):
    log = LogModel(user_id=user.id, log_text="ERROR Something happened")
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@pytest.fixture
def mock_ai_analysis():
    with patch("app.routers.log.get_ai_analysis", new_callable=AsyncMock) as mock:
        yield mock
