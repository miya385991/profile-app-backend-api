# FastAPIをインポート
import uvicorn
from fastapi import FastAPI
from database import engine
from fastapi.staticfiles import StaticFiles
from routers import profiles, projects, users, skills, \
    medias, portfolio, images, authentication


from fastapi.middleware.cors import CORSMiddleware
import models

# FastAPIのインスタンス作成

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# db 実行0
models.Base.metadata.create_all(bind=engine)
app.include_router((authentication.router))
app.include_router(portfolio.router)
app.include_router(images.router)
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(projects.router)
app.include_router(skills.router)
app.include_router(medias.router)


app.mount("/images", StaticFiles(directory="images"), name="images")


if __name__ == "__main__":
    uvicorn.run("profile-app-backend-api.main:app",
                port=8000, host='127.0.0.1', reload=True)
