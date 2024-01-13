from typing import List

from sqlalchemy import select
from sqlalchemy.orm.session import Session
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse

from db.database import get_db
from db.models import DbUser
from schemas import UserBase, UserDisplaySingUp
from db.hash import Hash


def sign_up_post(db: Session, request: UserBase):
    existing_username = db.query(DbUser).filter(DbUser.username == request.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username already exists, please choose another one!",
        )

    existing_email = db.query(DbUser).filter(DbUser.e_mail == request.e_mail).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email already exists, please choose another one!",
        )

    new_user = DbUser(
        e_mail=request.e_mail,
        first_name=request.first_name,
        second_name=request.second_name,
        username=request.username,
        password=Hash.bcrypt(request.password),
        home_address=request.home_address,
        postal_code=request.postal_code
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user_response = UserDisplaySingUp(
    id=new_user.id,
    e_mail=new_user.e_mail,
    first_name=new_user.first_name,
    second_name=new_user.second_name,
    username=new_user.username,
    home_address=new_user.home_address,
    postal_code=new_user.postal_code
)

    return JSONResponse(
        content={"detail": "User created successfully!", "new_user": user_response.dict()},
        status_code=status.HTTP_201_CREATED,
    )

    return new_user


def update_user(db: Session, id: int, request: UserBase): 
    user = db.query(DbUser).filter(DbUser.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found!")

    for attr, value in request.dict().items():
        if attr == "password":
            setattr(user, attr, Hash.bcrypt(value))
        else:
            setattr(user, attr, value)

    db.commit()
    db.refresh(user)

    updated_user_dict = {
        "e_mail": user.e_mail,
        "first_name": user.first_name,
        "second_name": user.second_name,
        "username": user.username,
        "home_address": user.home_address,
        "postal_code": user.postal_code,
    }

    return JSONResponse(
        content={"detail": f"User {id} updated successfully!", "updated_user": updated_user_dict},
        status_code=status.HTTP_200_OK,
    )


def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found!")
    
    db.delete(user)
    db.commit()
    return {"detail": f"User {id} deleted successfully!"}


def get_user(db: Session, user_id: int):
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found!")
    return user


def get_users(db: Session):
    users = db.query(DbUser).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found!")
    return users


def get_user_by_username(db: Session, username: str):
    return db.query(DbUser).filter(DbUser.username == username).first()