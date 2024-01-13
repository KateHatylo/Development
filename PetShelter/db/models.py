from typing import Optional

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from db.database import Base


class Animal(Base):
    __tablename__ = "animals"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    breed = Column(String)
    type = Column(String)
    age = Column(Integer)
    color = Column(String)
    image_url = Column(String, nullable=True)
    availability = Column(String, default="available")

    adopted = relationship("AdoptedAnimals", back_populates="animal")
    adoption_applications = relationship("AdoptionApplication", back_populates="animal")
    wishlist_items = relationship("UserFavorites", back_populates="animal")
    

class DbUser(Base): 
    __tablename__ = 'users' 
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    e_mail = Column(String, index=True)
    first_name = Column(String)
    second_name = Column(String)
    username = Column(String, index=True)
    password = Column(String)
    home_address = Column(String)
    postal_code = Column(String)
    role = Column(String, default="user")

    adopted = relationship("AdoptedAnimals", back_populates="user")
    adoption_applications = relationship("AdoptionApplication", back_populates="user")
    wishlist_items = relationship("UserFavorites", back_populates="user")
    

class AdoptedAnimals(Base): 
    __tablename__ = "adopted" 
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    animal_id = Column(Integer, ForeignKey("animals.id"))

    animal = relationship("Animal", back_populates="adopted")
    user = relationship("DbUser", back_populates="adopted")


class AdoptionApplication(Base):
    __tablename__ = "adoption_applications"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    animal_id = Column(Integer, ForeignKey("animals.id"))
    username = Column(String, ForeignKey("users.username"))
    additional_info = Column(String)
    status = Column(String)

    animal = relationship("Animal", back_populates="adoption_applications")
    user = relationship("DbUser", back_populates="adoption_applications")


class UserFavorites(Base):
    __tablename__ = "user_wishlist"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    animal_id = Column(Integer, ForeignKey("animals.id"))

    user = relationship("DbUser", back_populates="wishlist_items")
    animal = relationship("Animal", back_populates="wishlist_items")