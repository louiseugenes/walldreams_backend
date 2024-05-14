from sqlalchemy.orm import Session
from .schemas import *
from .models import *

def get_all_wallpepers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Wallpaper).offset(skip).limit(limit).all()    

def get_wallpaper(db: Session, wallpaper_id: int):
    return db.query(Wallpaper).filter(Wallpaper.wallpaper_id == wallpaper_id).first()

def create_wallpaper(db: Session, wallpaper: WallpaperSchema):
    _wallpaper = Wallpaper(title=wallpaper.title, url=wallpaper.url, description=wallpaper.description, upload_datetime=wallpaper.upload_datetime)
    db.add(_wallpaper)
    db.commit()
    db.refresh(_wallpaper)
    return _wallpaper

def remove_wallpaper(db: Session, wallpaper_id: int):
    _wallpaper = get_wallpaper(db=db, wallpaper_id=wallpaper_id)
    db.delete(_wallpaper)
    db.commit()
    db.refresh(_wallpaper)
    return _wallpaper

def update_wallpaper(db: Session, wallpaper_id: int, title: str, url: str, description: str, upload_datetime: datetime):
    _wallpaper = get_wallpaper(db=db, wallpaper_id=wallpaper_id)
    _wallpaper.title = title
    _wallpaper.url = url
    _wallpaper.description = description
    _wallpaper.upload_datetime = upload_datetime
    db.commit()
    db.refresh(_wallpaper)
    return _wallpaper
