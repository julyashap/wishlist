import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# настройка урла СУБД
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# настройка движка
engine = create_engine(DATABASE_URL)

# настройка сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Базовый класс для моделей."""

    pass


def get_db():
    """Автоматически открывает и закрывает соединение с БД."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
