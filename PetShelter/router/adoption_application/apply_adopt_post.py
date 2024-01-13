from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_adoption
from db.database import get_db
from schemas import (
    AdoptionApplicationCreate,
    AdoptionApplicationResponse,
    UserDisplayLogIn,
    UserBase,
)
from utils.role_checks import check_username_match
from auth.oauth2 import get_current_user


router = APIRouter(  
    prefix="/adoption",
    tags=["Adoption Application"]
)


@router.post("/apply", response_model=AdoptionApplicationResponse)
def apply_for_adoption(
    application_data: AdoptionApplicationCreate,
    db: Session = Depends(get_db),
    current_user: UserDisplayLogIn = Depends(get_current_user)
):
    check_username_match(application_data.username, current_user)
    return db_adoption.apply_for_adoption(db, application_data)

