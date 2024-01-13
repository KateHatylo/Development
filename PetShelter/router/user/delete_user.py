from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_user
from db.database import get_db
from schemas import UserDisplayLogIn
from db.hash import Hash
from auth.oauth2 import get_current_user
from utils.role_checks import check_user_permission


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.delete("/{id}")
def delete_user(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: UserDisplayLogIn = Depends(get_current_user)
):
    check_user_permission(current_user, id)
    return db_user.delete_user(db, id)