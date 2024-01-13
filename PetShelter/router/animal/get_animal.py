from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_animal
from db.database import get_db
from db.models import Animal as DBAnimal
from schemas import Animal as SchemaAnimal, AnimalDisplay


router = APIRouter(
    prefix="/animal",
    tags=["Animal"]
)

@router.get("/{animal_id}", response_model=AnimalDisplay)
def get_animal_by_id(
    animal_id: int, 
    db: Session = Depends(get_db)
):
    return db_animal.get_animal(db, animal_id)
    