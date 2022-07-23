
# FastAPIをインポート
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from base import Users
from opsions import get_db, http_exception, successful_response
import models
import sys

sys.path.append("..")

# FastAPIのインスタンス作成
router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={401: {"user": "Not authorized"}})


@router.get("/")
async def user_all(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users


@router.get("/{user_id}")
async def search_user(user_id: int,
                      db: Session = Depends(get_db)):
    users = db.query(models.Users) \
        .filter(models.Users.id == user_id).first()

    if users is None:
        raise http_exception()
    return users


@router.post("/")
async def create_user(user: Users, db: Session = Depends(get_db)):
    user_model = models.Users()
    if user_model is None:
        raise http_exception()

    user_model.username = user.username
    user_model.email = user.email
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name
    db.add(user_model)
    db.commit()
    return successful_response(201)


@router.put('/{user_id}')
async def update_user(user_id: int, user: Users,
                      db: Session = Depends(get_db)):
    user_model = db.query(models.Users) \
        .filter(models.Users.id == user_id).first()

    if user_model is None:
        raise http_exception()

    user_model.username = user.username
    user_model.email = user.email
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name
    db.add(user_model)
    db.commit()

    return successful_response(200)


@router.delete('/{user_id}')
async def delete_user(user_id: int,
                      db: Session = Depends(get_db)):
    user_model = db.query(models.Users) \
        .filter(models.Users.id == user_id).first()

    if user_model is None:
        raise http_exception()

    db.query(models.Users). \
        filter(models.Users.id == user_id).delete()
    db.commit()
    return successful_response(200)
