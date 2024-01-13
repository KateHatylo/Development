from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from db.models import DbUser, UserFavorites, Animal
from schemas import Favorites


def add_to_favorites(db: Session, animal_id: int, user_id: int):
    animal = db.query(Animal).filter(Animal.id == animal_id, Animal.availability == "available").first()
    if not animal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Animal with ID {animal_id} not found or not available!"
        )

    existing_favorite_item = (
        db.query(UserFavorites)
        .filter(UserFavorites.user_id == user_id, UserFavorites.animal_id == animal_id)
        .first()
    )

    if existing_favorite_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Animal with ID {animal_id} is already in the favorites!"
        )

    new_favorite_item = UserFavorites(user_id=user_id, animal_id=animal_id)
    db.add(new_favorite_item)
    db.commit()
    db.refresh(new_favorite_item)
    return JSONResponse(
        content={"detail": f"Animal {animal_id} is added to the favorites of user {user_id} successfully!"},
        status_code=status.HTTP_201_CREATED,
    )


def check_favorites(db: Session, user_id: int):
    favorites = db.query(UserFavorites).filter(UserFavorites.user_id == user_id).all()
    if not favorites:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Favorites not found for user with ID {user_id}!"
        )
    
    return favorites


def get_all_favorites(db: Session, response_model=List[UserFavorites]):
    favorites = db.query(UserFavorites).all()
    return favorites