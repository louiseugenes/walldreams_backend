from fastapi import FastAPI
from wallpaper.router import wallpaper

app = FastAPI()

app.include_router(wallpaper.router)
