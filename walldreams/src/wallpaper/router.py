from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
from sqlalchemy.orm import Session
from .service import *
from .schemas import *
from typing import List
from fastapi.responses import FileResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def list_all_wallpapers(db: Session = Depends(get_db)):
    return get_all_wallpapers(db)

@router.get("/{wallpaper_id}")
async def read_wallpaper(wallpaper_id: int, db: Session = Depends(get_db)):
    _wallpaper = get_wallpaper(db, wallpaper_id)
    return Response(code="200",status="Ok", message="Success get data", result=_wallpaper).dict(exclude_none=True)

@router.post("/create")
async def create_wallpaper(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    wallpaper_schema = WallpaperSchema(title=title, description=description, category=category)
    _wallpaper = create_wallpaper_db(db, wallpaper_schema, file)
    return Response(code="200",status="Ok", message="Wallpaper created", result=_wallpaper).dict(exclude_none=True)

@router.delete("/{wallpaper_id}")
async def delete_wallpaper(wallpaper_id: int, db: Session = Depends(get_db)):
    _wallpaper = remove_wallpaper(db, wallpaper_id)
    return Response(code="200",status="Ok", message="Wallapper deleted", result=_wallpaper).dict(exclude_none=True)

@router.post("/update/{wallpaper_id}")
async def update_wallpaper(request: RequestWallpaper, db: Session = Depends(get_db)):
    _wallpaper = update_wallpaper_db(db,category_id=request.parameter.id)
    return Response(code="200",status="Ok", message="Category updated", result=_wallpaper).dict(exclude_none=True)

@router.get("/download_wallpaper/{wallpaper_id}/")
def download_wallpaper(wallpaper_id: int, resolution: str ="HD",db: Session = Depends(get_db)):
    wallpaper = get_wallpaper(db=db, wallpaper_id=wallpaper_id)
    if not wallpaper:
        raise HTTPException(status_code=404, detail="Wallpaper not found")
    resolutions = {
        "HD": "HD",
        "FullHD": "FullHD",
        "4K": "4K"
    }
    if resolution not in resolutions:
        raise HTTPException(status_code=400, detail="Invalid resolution. Choose from HD, FullHD, or 4K.")
    
    file_name = wallpaper.url.split("/")[-1]
    wallpaper_path = f"utils/resized_images/{resolutions[resolution]}_{file_name}"
    
    return FileResponse(wallpaper_path)