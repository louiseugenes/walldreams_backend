from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .service import *
from .schemas import *
from typing import List

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

@router.post("/")
async def create_wallpaper(request: RequestWallpaper, db: Session = Depends(get_db)):
    _wallpaper = create_wallpaper(db, request.parameter)
    return Response(code="200",status="Ok", message="Wallpaper created", result=_wallpaper).dict(exclude_none=True)

@router.delete("/{wallpaper_id}")
async def delete_wallpaper(wallpaper_id: int, db: Session = Depends(get_db)):
    _wallpaper = remove_wallpaper(db, wallpaper_id)
    return Response(code="200",status="Ok", message="Wallapper deleted", result=_wallpaper).dict(exclude_none=True)

@router.post("/update/{wallpaper_id}")
async def update_wallpaper(request: RequestWallpaper, db: Session = Depends(get_db)):
    _wallpaper = update_wallpaper(db,category_id=request.parameter.id)
    return Response(code="200",status="Ok", message="Category updated", result=_wallpaper).dict(exclude_none=True)
