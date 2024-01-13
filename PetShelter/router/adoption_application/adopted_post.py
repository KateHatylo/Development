from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_adopted
from db.database import get_db
from db.models import Animal, DbUser
from schemas import AdoptedAnimals
from auth.oauth2 import get_current_user
from utils.role_checks import check_admin_role


router = APIRouter(  
    prefix="/adoption",
    tags=["Adopted Animals (archive)"]
)


@router.post("/{animal_id}/archive")
def add_animal_to_archive(
    application_data: AdoptedAnimals,
    db: Session = Depends(get_db),
    current_user: DbUser = Depends(get_current_user)
):

    """
    Only for admin!

    Add user_id and animal_id to the achive.

    Change the status of animal to "adopted".

    Animal becomes unavailable for other users to apply for.
    """

    check_admin_role(current_user)
    return db_adopted.add_addopted_animal(db, user_id=application_data.user_id, animal_id=application_data.animal_id)