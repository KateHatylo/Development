from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import db_user
from db.database import get_db
from db.models import DbUser
from schemas import UserDisplaySingUp
from utils.role_checks import check_admin_role
from auth.oauth2 import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["User"]
)


@router.get("", response_model=List[UserDisplaySingUp])
def get_users(
    db: Session = Depends(get_db), 
    current_user: DbUser = Depends(get_current_user)
):
    check_admin_role(current_user)
    return db_user.get_users(db)
