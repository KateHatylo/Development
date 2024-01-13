from typing import List

from fastapi import (
    APIRouter,
    File,
    UploadFile,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Animal, DbUser
from db.db_animal import get_animal_by_id
from auth.oauth2 import get_current_user
from utils.role_checks import check_admin_role

import random
import string
import shutil


router = APIRouter(
    prefix="/animal",
    tags=["Animal"]
)


@router.post("/{animal_id}/upload-image")
def upload_image(   
    animal_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: DbUser = Depends(get_current_user)
):
    check_admin_role(current_user)
    animal = get_animal_by_id(db, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found!")

    letters = string.ascii_letters
    rand_str = "".join(random.choice(letters) for i in range(5))
    new = f"_{rand_str}."
    filename = new.join(file.filename.rsplit(".", 1))
    path = f"images/{filename}"

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(file.file, buffer)

    animal.image_url = path
    db.commit()

    return {"detail": "Image uploaded successfully!"}