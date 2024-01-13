from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_animal
from db.database import get_db
from db.models import Animal, DbUser
from schemas import Animal as AnimalSchema, AnimalDisplay
from auth.oauth2 import get_current_user
from utils.role_checks import check_admin_role



router = APIRouter(
	prefix="/animal",
	tags=["Animal"]
)


@router.put("/{id}")
def update_animal(
    id: int, 
    request: AnimalSchema, 
    db: Session = Depends(get_db), 
    current_user: DbUser = Depends(get_current_user)
):
    check_admin_role(current_user)
    return db_animal.update_animal(db, id, request)