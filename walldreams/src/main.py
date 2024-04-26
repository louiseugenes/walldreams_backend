from fastapi import FastAPI
from walldreams.routers import wallpaper

app = FastAPI()

app.include_router(wallpaper.router)
