from fastapi import FastAPI
from wallpaper.router import router as wallpaper_router
from category.router import router as category_router
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

app.mount("/images", StaticFiles(directory="utils/images"), name="images")
app.mount("/resized_images", StaticFiles(directory="utils/resized_images"), name="resized_images")

app.include_router(category_router, prefix="/walldreams/category", tags=["category"])
app.include_router(wallpaper_router, prefix="/walldreams/wallpaper", tags=["wallpaper"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)



