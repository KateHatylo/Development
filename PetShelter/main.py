from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

from db.database import engine
from db import models

from auth import authentication

from router.user import (
    delete_user,
    get_user,
    signup_post,
    update_user,
    userlist_get,
)
from router.animal import (
    animal_post,
    animallist_get,
    delete_animal,
    get_animal,
    update_animal,
    animal_image_post,
)
from router.favorites import (
    favorites_post, 
    favorites_get,
    all_favorites_get
)

from router.adoption_application import (
    application_put, 
    apply_adopt_post, 
    check_status_get, 
    adopted_post
)

app = FastAPI(title="Pet Shelter")


app.include_router(signup_post.router)
app.include_router(update_user.router)
app.include_router(delete_user.router)
app.include_router(userlist_get.router)
app.include_router(get_user.router)

app.include_router(animal_post.router)
app.include_router(update_animal.router)
app.include_router(delete_animal.router)
app.include_router(animallist_get.router)
app.include_router(get_animal.router)

app.include_router(animal_image_post.router)

app.include_router(apply_adopt_post.router)
app.include_router(check_status_get.router)

app.include_router(application_put.router)
app.include_router(animal_post.router)

app.include_router(adopted_post.router)

app.include_router(favorites_post.router)
app.include_router(favorites_get.router)
app.include_router(all_favorites_get.router)

app.include_router(authentication.router)


models.Base.metadata.create_all(engine)


app.mount("/images", StaticFiles(directory="images"), name="images")