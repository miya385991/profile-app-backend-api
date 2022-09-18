from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from routers.setting import get_db, get_current_user
import models
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

    user = db.query(models.Users) \
        .filter(models.Users.id == user_id).first()

    # データ取得がない場合はからので空のdictを入れる。
    profile = db.query(models.Profiles) \
        .filter(models.Profiles.user_id == user_id).first()
    if not profile:
        profile = {}

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

