from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from db.models import Animal
from schemas import Animal as AnimalSchema, AnimalDisplay


def insert_animal(db: Session, request: AnimalSchema):
    new_animal = Animal(
        name=request.name,
        breed=request.breed,
        type=request.type,
        age=request.age,
        color=request.color,
        image_url=request.image_url,        
        availability=request.availability
    )

    db.add(new_animal)
    db.commit()
    db.refresh(new_animal)

    animal_response = AnimalDisplay(
    id=new_animal.id,
    name=new_animal.name,
    breed=new_animal.breed,
    type=new_animal.type,
    age=new_animal.age,
    color=new_animal.color,
    image_url=new_animal.image_url,
    availability=new_animal.availability
)

    return JSONResponse(
        content={"detail": "Animal created successfully!", "new_animal": animal_response.dict()},
        status_code=status.HTTP_201_CREATED,
    )

    return new_animal


def update_animal(db: Session, id: int, request: AnimalSchema):
    animal = db.query(Animal).filter(Animal.id == id).first()

    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Animal {id} not found!")

    
    for attr, value in request.dict().items():
        setattr(animal, attr, value)

    db.commit()
    db.refresh(animal)  
    return {"detail": f"Animal {id} updated successfully!", "updated_animal": animal}


def delete_animal(db: Session, id: int):
    animal = db.query(Animal).filter(Animal.id == id).first()
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Animal {id} not found!")
    db.delete(animal)
    db.commit()
    return {"detail": f"Animal {id} deleted successfully!"}


def get_animal(db: Session, animal_id: int):
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Animal {animal_id} not found!")
    return animal


def get_animals(db: Session, response_model=List[AnimalDisplay]):
    animals = db.query(Animal).all()
    if not animals:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No animals found!")
    return animals

def get_animal_by_id(db: Session, animal_id: int):
    return db.query(Animal).filter(Animal.id == animal_id).first()