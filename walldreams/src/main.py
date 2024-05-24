from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from wallpaper.router import router as wallpaper_router
from category.router import router as category_router
import uvicorn


app = FastAPI()

app.mount("/images", StaticFiles(directory="utils/images"), name="images")
app.mount("/resized_images", StaticFiles(directory="utils/resized_images"), name="resized_images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens, você pode especificar origens específicas se preferir
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

app.include_router(category_router, prefix="/walldreams/category", tags=["category"])
app.include_router(wallpaper_router, prefix="/walldreams/wallpaper", tags=["wallpaper"])

if __name__ == "__main__":
    import uvicorn    
    uvicorn.run(app, host="127.0.0.1", port=8000)
