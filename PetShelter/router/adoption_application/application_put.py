from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_adoption
from db.database import get_db
from db.models import Animal, DbUser
from auth.oauth2 import get_current_user
from utils.role_checks import check_admin_role


router = APIRouter(
    prefix="/adoption",
    tags=["Approve / Reject Adoption Application"]
)

@router.put("/{application_id}/approve")
def approve_adoption(
        application_id: int,
        db: Session = Depends(get_db),
        current_user: DbUser = Depends(get_current_user)
):

    """
    Only for admin!

    Approve user's adoption application.

    The adoption application status changes from "pending" to "approved".

    Change the status of animal from "available" to "reserved".

    Animal is still available for other users to apply for.
    """

    check_admin_role(current_user)
    return db_adoption.approve_adoption_application(db, application_id)
    

@router.put("/{application_id}/reject")
def reject_adoption_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: DbUser = Depends(get_current_user)
):

    """
    Only for admin!
    
    Reject user's adoption application.

    The adoption application status changes from "approved" to "rejected".

    Change the status of animal from "reserved" to "available".

    """

    check_admin_role(current_user)
    return db_adoption.reject_adoption_application(db, application_id)
