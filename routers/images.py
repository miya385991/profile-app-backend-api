# FastAPIをインポート
import os

from fastapi import APIRouter, Depends, File, UploadFile, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
from pathlib import Path
from fastapi.responses import FileResponse, JSONResponse
from routers.setting import get_db, http_exception, \
    successful_response, model_exception
import models, shutil, datetime
from shutil import rmtree

from os import getcwd, remove
# import sys
#
# sys.path.append("..")
from fastapi.staticfiles import StaticFiles

router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={401: {"images": "Not authorized"}})


@router.post('/')
async def create_upload_file(upload_file: UploadFile = File(...)):
    path = f'images/{upload_file.filename}'
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return {
        'filename': path,
        "type": upload_file.content_type
    }


@router.delete("/")
async def delete_file(folder: str = Form(...)):
    remove(f'images/{folder}')
    return JSONResponse(
        content={
            "removed": True
        }, status_code=200)
