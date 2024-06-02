from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
from sqlalchemy.orm import Session
from .service import *
from .schemas import *
from typing import List
from fastapi.responses import FileResponse
from category.service import search_category_db,count_category_db

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def list_all_wallpapers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    wallpapers, total_elements = get_all_wallpapers(db, skip, limit)
    return {"total_elements": total_elements, "wallpapers": wallpapers}

@router.get("/list_most_downloaded_wallpapers")
async def list_most_downloaded_wallpapers(db: Session = Depends(get_db)):
    return get_most_downloaded_wallpapers(db)

@router.get("/list_latest_wallpapers_released")
async def list_latest_wallpapers_released(db: Session = Depends(get_db)):
    return get_latest_wallpapers_released(db)

@router.get("/like_wallpaper/{wallpaper_id}")
async def list_latest_wallpapers_released(wallpaper_id: int, db: Session = Depends(get_db)):
    return like_wallpaper(db, wallpaper_id)

@router.get("/deslike_wallpaper/{wallpaper_id}")
async def list_latest_wallpapers_released(wallpaper_id: int, db: Session = Depends(get_db)):
    return deslike_wallpaper(db, wallpaper_id)

@router.get("/{wallpaper_id}")
async def read_wallpaper(wallpaper_id: int, db: Session = Depends(get_db)):
    _wallpaper = get_wallpaper(db, wallpaper_id)
    if _wallpaper is None:
        return Response(code="500",status="Error", message="Wallpaper not exists", result=_wallpaper).dict(exclude_none=True)
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
def download_wallpaper(wallpaper_id: int, resolution: str ="HD", name: str="unknowm", email: str="unknowm", db: Session = Depends(get_db)):
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
    record_download(db, wallpaper_id, name, email)
    
    return FileResponse(wallpaper_path)

@router.get("/v2/download_wallpaper/{wallpaper_id}/")
def download_wallpaper(wallpaper_id: int, resolution: str ="HD", db: Session = Depends(get_db)):
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

@router.get("/search/{wallpaper_keyword}")
async def search_wallpaper(wallpaper_keyword: str, db: Session = Depends(get_db)):
    _category = search_category_db(db, wallpaper_keyword)
    category_id = _category[0].category_id if _category else None

    _wallpaper = search_wallpaper_db(db, category_id, wallpaper_keyword)
    if _wallpaper is None:
        return Response[Optional[dict]](code="500", status="Error", message="Wallpaper not exists", result=None).dict(exclude_none=True)
    
    processed_category_ids = set()

    for wallpaper in _wallpaper:
        if wallpaper.category_id not in processed_category_ids:
            count_category_db(db, wallpaper.category_id)
            processed_category_ids.add(wallpaper.category_id)

    return Response(code="200",status="Ok", message="Wallpaper Found", result=_wallpaper).dict(exclude_none=True)
