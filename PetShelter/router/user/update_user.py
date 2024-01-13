from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_user
from db.database import get_db
from db.models import DbUser
from schemas import UserDisplayLogIn, UserBase
from utils.role_checks import check_user_permission
from auth.oauth2 import oauth2_schema, get_current_user


router = APIRouter(
	prefix="/user",
	tags=["User"]
)


@router.put("/{id}")
def update_user(
    id: int,
    request: UserBase,
    db: Session = Depends(get_db),
    current_user: UserDisplayLogIn = Depends(get_current_user)
):
    check_user_permission(current_user, id)
    return db_user.update_user(db, id, request)
