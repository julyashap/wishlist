from typing_extensions import Annotated
from pydantic import BaseModel, HttpUrl, Field, ConfigDict


class UserAuth(BaseModel):
    """Схема регистрации пользователя."""

    username: str
    password: str


class UserResponse(BaseModel):
    """Схема ответа с данными пользователя."""

    id: int
    username: str
    
    model_config = ConfigDict(from_attributes=True)


class WishBase(BaseModel):
    """Базовая схема модели желания."""

    description: Annotated[str | None, Field(default=None)]
    link: Annotated[HttpUrl | None, Field(default=None)]
    price: Annotated[float | None, Field(default=None)]
    priority: Annotated[str, Field(default="low")]


class WishCreate(WishBase):
    """Схема создания модели желания."""

    title: str


class WishUpdate(WishBase):
    """Схема обновления модели желания."""

    title: Annotated[str | None, Field(default=None)]]
    is_bought: Annotated[bool | None, Field(default=None)]


class WishResponse(WishBase):
    """Схема ответа с данными модели желания."""

    id: int
    title: str
    is_bought: bool
    user_id: int

    model_config = ConfigDict(from_attributes=True)
