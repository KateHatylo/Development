from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import db_adoption
from db.database import get_db
from schemas import (
    AdoptionApplicationCreate,
    AdoptionApplicationResponse,
    AdoptionApplicationStatusResponse,
)


router = APIRouter(  
    prefix="/adoption",
    tags=["Adoption Application"]
)

    
@router.get("/{application_id}/status", response_model=AdoptionApplicationStatusResponse)
def get_adoption_status(
    application_id: int,
    db: Session = Depends(get_db),
):
    return db_adoption.get_adoption_application_by_id(db, application_id)
