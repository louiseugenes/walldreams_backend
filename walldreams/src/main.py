from fastapi import FastAPI
from wallpaper.router import router as wallpaper_router
from category.router import router as category_router

app = FastAPI()

app.include_router(category_router, prefix="/walldreams/category", tags=["category"])
app.include_router(wallpaper_router, prefix="/walldreams/wallpaper", tags=["wallpaper"])


