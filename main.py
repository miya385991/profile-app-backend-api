# FastAPIをインポート
from fastapi import FastAPI, Depends, HTTPException
from database import engine

from routers import profiles, projects, users

import models

# FastAPIのインスタンス作成
app = FastAPI()
# db 実行
models.Base.metadata.create_all(bind=engine)


app.include_router(users.router)
app.include_router(projects.router)
app.include_router(profiles.router)
