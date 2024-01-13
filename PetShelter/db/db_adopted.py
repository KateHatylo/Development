from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from db.models import AdoptedAnimals, DbUser, Animal
from schemas import AdoptedAnimals


def add_addopted_animal(db: Session, user_id: int, animal_id: int):
    user_exists = db.query(DbUser).filter(DbUser.id == user_id).first()
    animal = db.query(Animal).filter(Animal.id == animal_id).first()

    if not (user_exists and animal):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or animal not found!"
        )

    existing_adoption = db.query(AdoptedAnimals).filter(
        AdoptedAnimals.animal_id == animal_id
    ).first()

    if existing_adoption:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This animal has already been adopted!"
        )

    new_adoption = AdoptedAnimals(user_id=user_id, animal_id=animal_id)
    db.add(new_adoption)
    db.commit()
    db.refresh(new_adoption)

    animal.availability = "adopted"
    db.commit()
    db.refresh(animal)

    return {"detail": f"User {user_id} and animal {animal_id} are added successfully!"}
