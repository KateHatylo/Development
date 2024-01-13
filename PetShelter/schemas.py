from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from fastapi import Body


ALLOWED_ROLES = {"user", "admin"}


class Animal(BaseModel):
    name: str
    breed: str
    type: str
    age: int
    color: str
    image_url: str
    availability: str = "available"


class AnimalDisplay(BaseModel):
    id: int
    name: str
    breed: str
    type: str
    age: int
    color: str
    image_url: str
    availability: str

    class Config():
        from_attributes = True
        

class UserBase(BaseModel):
    e_mail: str
    first_name: str
    second_name: str 
    username: str 
    password: str 
    home_address: Optional[str]
    postal_code: Optional[str]


class UserDisplaySingUp(BaseModel): 
    id: int
    e_mail: str
    first_name: str
    second_name: str
    username: str
    home_address: Optional[str]
    postal_code: Optional[str]

    class Config():
        from_attributes = True 


class UserDisplayLogIn(BaseModel):
    message: str

    class Config():
        from_attributes = True


class AssignRoleRequest(BaseModel):
    user_id: int
    new_role: str


class AdoptedAnimals(BaseModel):
    user_id: int 
    animal_id: int


class AdoptionApplicationCreate(BaseModel):
    animal_id: int
    username: str
    additional_info: str


class AdoptionApplicationResponse(BaseModel):
    id: int
    type: str
    name: str
    additional_info: str
    status: str
    message: str

    class Config():
        from_attributes = True 


class AdoptionApplicationStatusResponse(BaseModel):
    id: int
    status: str
    message: str

    class Config():
        from_attributes = True 


class Favorites(BaseModel):
    id: int
    user_id: int
    animal_id: int