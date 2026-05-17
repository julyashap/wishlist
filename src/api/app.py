from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from .routes import auth_router, wish_router


def create_app() -> FastAPI:
    """Создает FastAPI-приложение."""
    # автоматически создаем таблицы
    Base.metadata.create_all(bind=engine)

    # создание приложения
    app = FastAPI(title="Wishlist API")

    # регистрация роутов
    app.include_router(auth_router)
    app.include_router(wish_router)

    # встройка статики
    app.mount("/", StaticFiles(directory="src/frontend", html=True), name="frontend")

    return app
