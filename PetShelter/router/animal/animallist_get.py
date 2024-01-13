from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_animal
from db.database import get_db
from db.models import Animal as DBAnimal
from schemas import Animal as SchemaAnimal, AnimalDisplay


router = APIRouter(
    prefix="/animals",
    tags=["Animal"]
)


@router.get("", response_model=List[AnimalDisplay])
def get_animals(db: Session = Depends(get_db)):
    return db_animal.get_animals(db)
    
    



