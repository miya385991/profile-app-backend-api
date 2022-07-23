
# FastAPIをインポート
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from base import Projects
import models

from opsions import get_db, http_exception, successful_response
import sys

sys.path.append("..")

router = APIRouter(
    prefix="/project",
    tags=["project"],
    responses={401: {"user": "Not authorized"}})


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
async def create_project(project: Projects, db: Session = Depends(get_db)):
    project_model = models.Projects()
    if project_model is None:
        raise http_exception()

    project_model.owner = project.owner
    project_model.title = project.title
    project_model.description = project.description
    project_model.demo_link = project.demo_link
    project_model.source_link = project.source_link
    project_model.vote_total = project.vote_total
    project_model.vote_ratio = project.vote_ratio
    db.add(project_model)
    db.commit()
    return successful_response(201)


@router.put('/{project_id}')
async def update_project(project_id: int, project: Projects,
                         db: Session = Depends(get_db)):
    project_model = db.query(models.Projects) \
        .filter(models.Projects.id == project_id).first()

    if project_model is None:
        raise http_exception()

    project_model.owner = project.owner
    project_model.title = project.title
    project_model.description = project.description
    project_model.demo_link = project.demo_link
    project_model.source_link = project.source_link
    project_model.vote_total = project.vote_total
    project_model.vote_ratio = project.vote_ratio
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
