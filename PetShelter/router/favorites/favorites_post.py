from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_userfavorites
from db.database import get_db
from db.models import DbUser, UserFavorites
from schemas import Favorites
from auth.oauth2 import get_current_user
from utils.role_checks import check_user_permission


router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)


@router.post("/{animal_id}/add")
def add_to_favorites(
    animal_id: int,
    db: Session = Depends(get_db),
    current_user: DbUser = Depends(get_current_user)
):
    check_user_permission(current_user, current_user.id)
    return db_userfavorites.add_to_favorites(db, animal_id, current_user.id)
