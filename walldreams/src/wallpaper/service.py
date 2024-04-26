from sqlalchemy.orm import Session
from ..models.wallpaper import Wallpaper
from ..database import SessionLocal

def get_wallpaper(db: Session, wallpaper_id: int):
    return db.query(Wallpaper).filter(Wallpaper.id == wallpaper_id).first()

def create_wallpaper(db: Session, wallpaper_data: dict):
    db_wallpaper = Wallpaper(**wallpaper_data)
    db.add(db_wallpaper)
    db.commit()
    db.refresh(db_wallpaper)
    return db_wallpaper
