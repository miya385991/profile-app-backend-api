from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
from pydantic import BaseModel

from routers.setting import get_db, http_exception, successful_response, \
    get_current_user
import models, random
import sys

sys.path.append("..")

color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])

# FastAPIのインスタンス作成
router = APIRouter(
    prefix="/skill",
    tags=["skill"],
    responses={401: {"skill": "Not authorized"}})


class Skills(BaseModel):
    name: str


@router.get("/")
async def skill_all(db: Session = Depends(get_db)):
    skill = db.query(models.Skills).all()
    return skill


@router.get("/{skill_id}")
async def search_skill(skill_id: int,
                       db: Session = Depends(get_db)):
    skills = db.query(models.Skills) \
        .filter(models.Skills.id == skill_id).first()

    if skills is None:
        raise http_exception()
    return skills


@router.post("/")
async def create_skill(skill: Skills, user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    skill_model = models.Skills()

    if skill_model is None:
        raise http_exception()
    skill_model.name = skill.name
    skill_model.user_id = user.get('id')
    db.add(skill_model)
    db.commit()

    return successful_response(201)


@router.put('/{skill_id}')
async def update_skill(skill_id: int, skill: Skills,
                       user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    skill_model = db.query(models.Skills) \
        .filter(models.Skills.id == skill_id).first()

    if skill_model is None:
        raise http_exception()

    skill_model.skill_name = skill.skill_name
    skill_model.user_id = user.get('id')
    db.add(skill_model)
    db.commit()

    return successful_response(200)


@router.delete('/{skill_id}')
async def delete_skill(skill_id: int,
                       db: Session = Depends(get_db)):
    skill_model = db.query(models.Skills) \
        .filter(models.Skills.id == skill_id).first()

    if skill_model is None:
        raise http_exception()

    db.query(models.Skills). \
        filter(models.Skills.id == skill_id).delete()
    db.commit()
    return successful_response(200)
