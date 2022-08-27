from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from routers.setting import get_db, http_exception, successful_response, \
    get_current_user
import models, random
import sys

sys.path.append("..")

# FastAPIのインスタンス作成
router = APIRouter(
    prefix="/portfolio",
    tags=["portfolio"],
    responses={401: {"portfolio": "Not authorized"}})


@router.get("/")
async def portfolio_get_all(user: dict = Depends(get_current_user),
                            db: Session = Depends(get_db)):

    user_id = user.get('id')
    # Usersから取得
    user = db.query(models.Users) \
        .filter(models.Users.id == user_id).first()

    # profilesから取得
    profile = db.query(models.Profiles) \
        .filter(models.Profiles.user_id == user_id).first()

    # projectsから取得
    projects = db.query(models.Projects) \
        .filter(models.Projects.user_id == user_id).all()

    skill = db.query(models.Skills) \
        .filter(models.Skills.user_id == user_id).all()

    media = db.query(models.Medias) \
        .filter(models.Medias.user_id == user_id).all()

    return {
        'user': user,
        'profile': profile,
        'project': projects,
        'skill': skill,
        'media': media
    }
