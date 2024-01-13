from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from db.models import AdoptionApplication, Animal, DbUser
from schemas import AdoptionApplicationCreate, AdoptionApplicationResponse, AdoptionApplicationStatusResponse


def apply_for_adoption(db: Session, application_data: AdoptionApplicationCreate):
    animal = db.query(Animal).filter(
        Animal.id == application_data.animal_id,
        Animal.availability == "available"
    ).first()

    username = db.query(DbUser).filter(DbUser.username == application_data.username).first()

    if not animal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found or not available for adoption!"
        )

    if not username:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found for the given username!"
        )

    new_application = AdoptionApplication(
        animal_id=animal.id,
        username=username.username,
        additional_info=application_data.additional_info,
        status="pending"  # Default status
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return AdoptionApplicationResponse(
        id=new_application.id,
        type=animal.type,
        name=animal.name,
        additional_info=new_application.additional_info,
        status=new_application.status,
        message=f"Your application ID is {new_application.id}. You could check the status of your application by your application ID!"
    )


def approve_adoption_application(db: Session, application_id: int):
    db_application = db.query(AdoptionApplication).filter(AdoptionApplication.id == application_id).first()

    if db_application:
        if db_application.status == "approved":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This application has already been approved!"
            )

        animal = db.query(Animal).filter(Animal.id == db_application.animal_id).first()

        if animal.availability != "available":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This animal is not available for adoption!"
            )

        animal.availability = "reserved"
        db.commit()
        db.refresh(animal)

        db_application.status = "approved"
        db.commit()
        db.refresh(db_application)

        return {"detail": f"Adoption application with ID {db_application.id} approved successfully!"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Adoption application not found!"
    )


def reject_adoption_application(db: Session, application_id: int):
    db_application = db.query(AdoptionApplication).filter(AdoptionApplication.id == application_id).first()

    if db_application:
        if db_application.status == "rejected":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This application has already been rejected!"
            )


        animal = db.query(Animal).filter(Animal.id == db_application.animal_id).first()

        animal.availability = "available"
        db.commit()
        db.refresh(animal)

        db_application.status = "rejected"
        db.commit()
        db.refresh(db_application)

        return {"detail": f"Adoption application with ID {db_application.id} rejected successfully!"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Adoption application not found!"
    )


def get_adoption_application_by_id(db: Session, application_id: int):
    application = db.query(AdoptionApplication).filter(AdoptionApplication.id == application_id).first()

    if not application:
        raise HTTPException(status_code=404, detail="Adoption application not found!")
    
    message = "Default message"

    if application.status == "approved":
        message = "Thanks for your application! Our manager will call you soon!"
    elif application.status == "rejected":
        message = "Sorry, but now it is impossible to adopt. You could contact us to get more details!"
    elif application.status == "pending":
        message = "Your application is still pending. We'll notify you once a decision is made!"

    return AdoptionApplicationStatusResponse(
        id=application.id,
        status=application.status,
        message=message
    )





