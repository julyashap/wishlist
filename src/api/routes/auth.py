import hashlib
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserAuth
from ..auth import create_access_token

auth_router = APIRouter(prefix="/api/auth")


def hash_password(password: str) -> str:
    """Хеширует пароль."""
    return hashlib.sha256(password.encode()).hexdigest()


@auth_router.post("/register")
def register(user_data: UserAuth, db: Session = Depends(get_db)) -> dict[str, Any]:
    """Регистрирует пользователя."""
    db_user = db.query(User).filter(User.username == user_data.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Имя пользователя занято")
    new_user = User(
        username=user_data.username, hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "Регистрация успешна"}


@auth_router.post("/login")
def login(
    user_data: UserAuth, response: Response, db: Session = Depends(get_db)
) -> dict[str, Any]:
    """Выполняет вход пользователя в систему."""
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user:
        raise HTTPException(
            status_code=400, detail="Пользователя с таким именем не существует"
        )
    if user.hashed_password != hash_password(user_data.password):
        raise HTTPException(
            status_code=400, detail="Неверный пароль, попробуйте еще раз"
        )
    token = create_access_token(data={"sub": user.username})
    response.set_cookie(key="access_token", value=token, httponly=True, samesite="lax")
    return {"message": "Вход выполнен успешно"}


@auth_router.post("/logout")
def logout(response: Response) -> dict[str, Any]:
    """Выполняет выход из системы для пользователя."""
    response.delete_cookie(key="access_token")
    return {"message": "Вышли из системы"}
