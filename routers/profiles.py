
# FastAPIをインポート
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from base import Profiles
from opsions import get_db, http_exception, successful_response
import models
import sys

sys.path.append("..")

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    responses={401: {"user": "Not authorized"}})


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
async def create_profile(profile: Profiles, db: Session = Depends(get_db)):
    profile_model = models.Profiles()

    if profile is None:
        raise http_exception()

    profile_model.user_id = profile.user_id
    profile_model.location = profile.location
    profile_model.short_intro = profile.short_intro
    profile_model.bio = profile.bio
    # profile_model.profile_image = profile.profile_image
    profile_model.github = profile.github
    profile_model.twitter = profile.twitter
    profile_model.youtube = profile.youtube
    profile_model.website = profile.website

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

    profile_model.user_id = profile.user_id
    profile_model.location = profile.location
    profile_model.short_intro = profile.short_intro
    profile_model.bio = profile.bio
    # profile_model.profile_image = profile.profile_image
    profile_model.github = profile.github
    profile_model.twitter = profile.twitter
    profile_model.youtube = profile.youtube
    profile_model.website = profile.website

    db.add(profile_model)
    db.commit()
    return successful_response(201)


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
