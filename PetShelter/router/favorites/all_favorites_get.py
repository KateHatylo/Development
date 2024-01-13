from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_userfavorites
from db.database import get_db
from db.models import UserFavorites, DbUser
from schemas import Favorites
from auth.oauth2 import get_current_user
from utils.role_checks import check_admin_role


router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)


@router.get("", response_model=List[Favorites])
def get_favorites(
    db: Session = Depends(get_db), 
    current_user: DbUser = Depends(get_current_user)
):
    check_admin_role(current_user)
    return db_userfavorites.get_all_favorites(db)


