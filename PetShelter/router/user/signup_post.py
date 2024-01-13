from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import UserBase, UserDisplaySingUp
from db.database import get_db
from db.models import DbUser
from db.db_user import sign_up_post

router = APIRouter(
	prefix="/user",
	tags=["User"]
)


@router.post("", response_model=UserDisplaySingUp)
def sign_up(
    user_data: UserBase,
    db: Session = Depends(get_db),
):
    return sign_up_post(db=db, request=user_data)



