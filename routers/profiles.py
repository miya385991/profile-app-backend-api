# FastAPIをインポート
from fastapi import APIRouter, Depends, File, UploadFile, Form, Header
from sqlalchemy.orm import Session
import models, shutil, sys
from pydantic import BaseModel
from routers.setting import get_db, http_exception, successful_response, \
    get_current_user
from os import getcwd, remove

sys.path.append("..")

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    responses={401: {"user": "Not authorized"}})


class Profiles(BaseModel):
    location: str
    short_intro: str
    bio: str
    image_url: str


@router.get("/")
async def profile_all(db: Session = Depends(get_db)):
    profiles = db.query(models.Profiles).all()
    return profiles


@router.get("/{profile_id}")
async def search_user(profile_id: int,
                      db: Session = Depends(get_db)):
    profile = db.query(models.Profiles) \
        .filter(models.Profiles.id == profile_id).first()

    if profile is None:
        raise http_exception()

    return profile


@router.post("/")
async def create_profile(profile: Profiles,
                         user: dict = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    profile_model = models.Profiles()

    if profile is None:
        raise http_exception()
    # profileデータ
    profile_model.user_id = user.get('id')
    profile_model.location = profile.location
    profile_model.short_intro = profile.short_intro
    profile_model.bio = profile.bio
    profile_model.image_url = profile.image_url

    db.add(profile_model)
    db.commit()

    return successful_response(201)


@router.put('/{profile_id}')
async def update_profile(profile_id: int, profile: Profiles,
                         db: Session = Depends(get_db)):
    profile_model = db.query(models.Profiles) \
        .filter(models.Profiles.id == profile_id).first()

    if profile_model is None:
        raise http_exception()

    profile_model.location = profile.location
    profile_model.short_intro = profile.short_intro
    profile_model.bio = profile.bio
    profile_model.image_url = profile.image_url
    db.add(profile)

    db.add(profile_model)
    db.commit()
    return successful_response(201)


@router.get('user/{user_id}')
async def user_profile(user_id: int,
                       db: Session = Depends(get_db)):
    profile_model = db.query(models.Profiles) \
        .filter(models.Profiles.user_id == user_id).first()
    return profile_model


@router.delete('/{profile_id}')
async def delete_user(profile_id: int,
                      db: Session = Depends(get_db)):
    profile_model = db.query(models.Profiles) \
        .filter(models.Profiles.id == profile_id).first()

    if profile_model is None:
        raise http_exception()

    db.query(models.Profiles). \
        filter(models.Profiles.id == profile_id).delete()
    db.commit()
    return successful_response(200)
