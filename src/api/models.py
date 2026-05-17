from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    """Модель пользователя."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    wishes = relationship("Wish", back_populates="user", cascade="all, delete-orphan")


class Wish(Base):
    """Модель желания."""

    __tablename__ = "wishes"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    link = Column(String, nullable=True)
    price = Column(Float, nullable=True)

    priority = Column(String, default="low")

    is_bought = Column(Boolean, default=False)

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="wishes")
