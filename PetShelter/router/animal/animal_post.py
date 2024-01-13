from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_animal
from db.database import get_db
from db.models import Animal, DbUser
from schemas import Animal
from auth.oauth2 import get_current_user
from utils.role_checks import check_admin_role


router = APIRouter(
        tags=["Animal"]
    )


@router.post("/animal")
def create_animal(
    animal_data: Animal,
    db: Session = Depends(get_db),
    current_user: DbUser = Depends(get_current_user)
):
    check_admin_role(current_user)
    return db_animal.insert_animal(db=db, request=animal_data)
