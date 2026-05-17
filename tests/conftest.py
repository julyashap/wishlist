import pytest
from typing import Generator
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

import sqlalchemy
test_engine = sqlalchemy.create_engine(
    "sqlite:///:memory:", 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
sqlalchemy.create_engine = lambda *args, **kwargs: test_engine

from src.api.app import create_app
from src.api.database import Base, get_db

try:
    import src.api.models
except ImportError:
    pass

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db() -> Generator[Session, None, None]:
    """Тестовая сессия базы данных."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def setup_database() -> Generator[None, None, None]:
    """Автоматически создает чистые таблицы перед каждым тестом."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    """Базовый клиент для неавторизованных запросов."""
    app: FastAPI = create_app()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def auth_client(client: TestClient) -> TestClient:
    """Готовый клиент с валидной сессией авторизации."""
    user: dict[str, str] = {"username": "tester", "password": "password123"}
    client.post("/api/auth/register", json=user)
    client.post("/api/auth/login", json=user)
    return client
