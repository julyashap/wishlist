from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Wish, User
from ..schemas import WishCreate, WishUpdate, WishResponse
from ..auth import get_current_user

wish_router = APIRouter(prefix="/api/wishes")


@wish_router.post("/", response_model=WishResponse, status_code=status.HTTP_201_CREATED)
def create_wish(
    wish_data: WishCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Wish:
    """Создает желание."""
    new_wish = Wish(**wish_data.model_dump(), user_id=current_user.id)
    db.add(new_wish)
    db.commit()
    db.refresh(new_wish)
    return new_wish


@wish_router.get("/", response_model=list[WishResponse])
def get_wishes(
    is_bought: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Wish]:
    """Возвращает список всех желаний."""
    wishes = (
        db.query(Wish)
        .filter(Wish.user_id == current_user.id, Wish.is_bought == is_bought)
        .all()
    )
    return wishes


@wish_router.get("/{wish_id}", response_model=WishResponse)
def get_one_wish(
    wish_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Wish:
    """Возвращает одно желание по ID."""
    wish = (
        db.query(Wish)
        .filter(Wish.id == wish_id, Wish.user_id == current_user.id)
        .first()
    )
    if not wish:
        raise HTTPException(status_code=404, detail="Желание не найдено")
    return wish


@wish_router.patch("/{wish_id}", response_model=WishResponse)
def update_wish(
    wish_id: int,
    wish_data: WishUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Wish:
    """Обновляет желание."""
    wish = (
        db.query(Wish)
        .filter(Wish.id == wish_id, Wish.user_id == current_user.id)
        .first()
    )
    if not wish:
        raise HTTPException(status_code=404, detail="Желание не найдено")

    update_data = wish_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(wish, key, value)

    db.commit()
    db.refresh(wish)
    return wish


@wish_router.delete("/{wish_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wish(
    wish_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Удаляет желание."""
    wish = (
        db.query(Wish)
        .filter(Wish.id == wish_id, Wish.user_id == current_user.id)
        .first()
    )
    if not wish:
        raise HTTPException(status_code=404, detail="Желание не найдено")

    db.delete(wish)
    db.commit()
    return None
