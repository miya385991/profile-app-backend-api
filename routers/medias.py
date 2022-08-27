# FastAPIをインポート
from fastapi import APIRouter, Depends
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from routers.setting import get_db, http_exception, \
    successful_response, model_exception, get_current_user
import models
import sys

sys.path.append("..")

# FastAPIのインスタンス作成
router = APIRouter(
    prefix="/media",
    tags=["media"],
    responses={401: {"media": "Not authorized"}})


class Medias(BaseModel):
    name: str
    link: str


@router.get('/')
async def media_all(db: Session = Depends(get_db)):
    media = db.query(models.Medias).all()
    return media


@router.get('/{media_id}')
async def media_search(media_id: int, db: Session = Depends(get_db)):
    media = db.query(models.Medias) \
        .filter(models.Medias.id == media_id).first()
    return media


@router.post('/')
async def create_media(media: Medias,
                       user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    media_model = models.Medias()
    model_exception(media_model)

    media_model.name = media.name
    media_model.link = media.link
    media_model.user_id = user.get('id')
    db.add(media_model)
    db.commit()
    return successful_response(201)


@router.put('/{media_id}')
async def media_update(media_id: int, media: Medias,
                       user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    media_model = db.query(models.Medias) \
        .filter(models.Medias.id == media_id).first()

    model_exception(media_model)
    media_model.name = media.name
    media_model.link = media.link
    media_model.user_id = user.get('id')

    db.add(media_model)
    db.commit()

    return successful_response(201)


@router.delete('/{media_id}')
async def delete_media(media_id: int,
                       db: Session = Depends(get_db)):
    media_model = db.query(models.Medias). \
        filter(models.Medias.id == media_id).first()
    if media_model is None:
        raise http_exception()
    model_exception(media_model)
    db.query(models.Medias). \
        filter(models.Medias.id == media_id).delete()
    db.commit()
    return successful_response(200)
