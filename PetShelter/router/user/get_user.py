from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db import db_user
from db.database import get_db
from db.models import DbUser
from schemas import UserBase, UserDisplaySingUp
from auth.oauth2 import get_current_user
from utils.role_checks import check_admin_role


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get("/{user_id}", response_model=UserDisplaySingUp)
def get_user_by_id(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user: DbUser = Depends(get_current_user)
):
    check_admin_role(current_user)
    return db_user.get_user(db, user_id)