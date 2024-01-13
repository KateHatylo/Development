from fastapi import HTTPException, status
from db.models import DbUser
from schemas import UserDisplayLogIn


def check_admin_role(current_user: DbUser):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges. Only admin can perform this operation!"
        )


def check_user_permission(current_user: DbUser, profile_id: int):
    if current_user.role != "admin" and current_user.id != profile_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this operation!"
        )


def check_username_match(username: str, current_user: UserDisplayLogIn):
    if username != current_user.username:
        raise HTTPException(
            status_code=403,
            detail="You can only apply for adoption on behalf of yourself!"
        )