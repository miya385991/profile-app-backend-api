# FastAPIをインポート
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from routers.setting import get_db, http_exception, \
    successful_response, model_exception, get_user_exception, token_excetin, \
    authenticate_user, create_access_token, get_password_hash, \
    get_current_user, oauth2_bearer, token_expires
import models
import sys, pprint
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError

from fastapi.testclient import TestClient


sys.path.append("..")

# FastAPIのインスタンス作成
router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={401: {"user": "Not authorized"}})


class Users(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    password: str



@router.get("/")
async def user_all(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users


@router.get("/{user_id}")
async def search_user(user_id: int,
                      db: Session = Depends(get_db), token:str = Depends(oauth2_bearer)):
    users = db.query(models.Users) \
        .filter(models.Users.id == user_id).first()

    if users is None:
        raise http_exception()
    return users


@router.post("/")
async def create_user(user: Users, db: Session = Depends(get_db)):
    user_model = models.Users()
    model_exception(user_model)

    user_model.username = user.username
    user_model.email = user.email
    user_model.phone_number = user.phone_number
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name

    hash_password = get_password_hash(user.password)
    user_model.hash_password = hash_password
    #
    db.add(user_model)
    db.commit()
    return successful_response(201)


@router.put('/{user_id}')
async def update_user(user_id: int, user: Users,
                      db: Session = Depends(get_db)):
    user_model = db.query(models.Users) \
        .filter(models.Users.id == user_id).first()

    model_exception(user_model)

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
    model_exception(user_model)
    db.query(models.Users). \
        filter(models.Users.id == user_id).delete()
    db.commit()
    return successful_response(200)
