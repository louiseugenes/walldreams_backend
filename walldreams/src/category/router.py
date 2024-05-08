from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..services.wallpaper import get_wallpaper, create_wallpaper
from ..models.wallpaper import Wallpaper

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/wallpapers/{wallpaper_id}")
async def read_wallpaper(wallpaper_id: int, db: Session = Depends(get_db)):
    wallpaper = get_wallpaper(db, wallpaper_id)
    if wallpaper is None:
        raise HTTPException(status_code=404, detail="Wallpaper not found")
    return wallpaper

@router.post("/wallpapers/")
async def create_wallpaper(wallpaper_data: Wallpaper, db: Session = Depends(get_db)):
    return create_wallpaper(db, wallpaper_data.dict())
