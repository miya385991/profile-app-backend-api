# FastAPIをインポート
from pprint import pprint

from fastapi import APIRouter, Depends, File, UploadFile, Form, Body
from pydantic import BaseModel
from sqlalchemy import desc
from sqlalchemy.orm import Session
import models

from routers.setting import get_db, http_exception, successful_response, \
    get_current_user
import sys, json
from os import getcwd, remove

sys.path.append("..")

router = APIRouter(
    prefix="/project",
    tags=["project"],
    responses={401: {"project": "Not authorized"}})


class Projects(BaseModel):
    title: str
    description: str
    demo_link: str
    source_link: str
    image_url: str


@router.get("/")
async def project_all(db: Session = Depends(get_db)):
    project = db.query(models.Projects).all()
    return project


@router.get("/{project_id}")
async def search_project(project_id: int,
                         db: Session = Depends(get_db)):
    project = db.query(models.Projects) \
        .filter(models.Projects.id == project_id).first()

    if project is None:
        raise http_exception()

    return project


@router.post("/")
async def create_project(
        project: Projects,
        user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)):
    project_model = models.Projects()
    if project_model is None:
        raise http_exception()

    project_model.title = project.title
    project_model.description = project.description
    project_model.demo_link = project.demo_link
    project_model.source_link = project.source_link
    project_model.image_url = project.image_url
    project_model.user_id = user.get('id')
    db.add(project_model)

    db.commit()

    return successful_response(201)


@router.put('/{project_id}')
async def update_project(project_id: int, project: Projects,
                         user: dict = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    project_model = db.query(models.Projects) \
        .filter(models.Projects.id == project_id).first()

    if project_model is None:
        raise http_exception()

    project_model.title = project.title
    project_model.description = project.description
    project_model.demo_link = project.demo_link
    project_model.source_link = project.source_link
    project_model.image_url = project.image_url
    project_model.user_id = user.get('id')
    db.add(project_model)

    db.commit()

    return successful_response(200)


@router.delete('/{project_id}')
async def delete_project(project_id: int,
                         db: Session = Depends(get_db)):
    project_model = db.query(models.Projects) \
        .filter(models.Projects.id == project_id).first()

    if project_model is None:
        raise http_exception()

    db.query(models.Projects). \
        filter(models.Projects.id == project_id).delete()
    db.commit()
    return successful_response(200)


@router.get('/owners/{user_id}')
async def owners_projects(user_id: int,
                          db: Session = Depends(get_db)):
    project = db.query(models.Projects) \
        .filter(models.Projects.owner == user_id).all()
    return project
