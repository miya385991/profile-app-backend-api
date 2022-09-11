# FastAPIをインポート
import os

from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
import shutil

from os import getcwd, remove


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
