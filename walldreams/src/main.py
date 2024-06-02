from fastapi import FastAPI
from wallpaper.router import router as wallpaper_router
from category.router import router as category_router
from fastapi.staticfiles import StaticFiles
from user.router import router as user_router
import uvicorn
from auth.router import router as auth_router

app = FastAPI()

app.mount("/images", StaticFiles(directory="utils/images"), name="images")
app.mount("/resized_images", StaticFiles(directory="utils/resized_images"), name="resized_images")

app.include_router(category_router, prefix="/walldreams/category", tags=["category"])
app.include_router(wallpaper_router, prefix="/walldreams/wallpaper", tags=["wallpaper"])
app.include_router(wallpaper_router, prefix="/walldreams/wallpaper", tags=["wallpaper"])
app.include_router(user_router, prefix="/walldreams/user", tags=["user"])
app.include_router(auth_router, prefix="/walldreams/auth", tags=["auth"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)



