from sqlalchemy.orm import Session
from .schemas import *
from .models import *
from PIL import Image
from fastapi import UploadFile, File
import shutil
from sqlalchemy.exc import SQLAlchemyError
import os
from sqlalchemy import desc, not_, or_
from category.models import Category

def resize_wallpaper(image_path: str, output_path: str, size: tuple):
    with Image.open(image_path) as img:
        img = img.resize(size, Image.LANCZOS)
        img.save(output_path)

def get_all_wallpapers(db: Session, skip: int = 0, limit: int = 100):
    query = db.query(Wallpaper).offset(skip).limit(limit)
    wallpapers = query.all()
    total_elements = query.count()
    return wallpapers, total_elements

def get_most_downloaded_wallpapers(db: Session, limit: int = 3):
    return db.query(Wallpaper).filter(Wallpaper.download_count.isnot(None)
            ).order_by(desc(Wallpaper.download_count)
            ).limit(limit).all()

def get_latest_wallpapers_released(db: Session, limit: int = 3):
    return db.query(Wallpaper).order_by(desc(Wallpaper.upload_datetime)).limit(limit).all() 

def get_wallpaper(db: Session, wallpaper_id: int):
    return db.query(Wallpaper).filter(Wallpaper.wallpaper_id == wallpaper_id).first()

def search_wallpaper_db(db: Session,category_id: int, wallpaper_keyword: str):
    keyword_pattern = f"%{wallpaper_keyword}%"
    
    if category_id is not None:
        result = db.query(Wallpaper).filter(
            or_(
                Wallpaper.category_id == category_id
            )
        ).all()
        return result
    else:
        result = db.query(Wallpaper).filter(
            or_(
                Wallpaper.description.like(keyword_pattern),
                Wallpaper.title.like(keyword_pattern)
            )
        ).all()
        return result

def like_wallpaper(db: Session, wallpaper_id: int):
    _wallpaper = get_wallpaper(db=db, wallpaper_id=wallpaper_id)

    if _wallpaper.like_count is None:
        _wallpaper.like_count = 1
        db.commit()
        db.refresh(_wallpaper)
        return db.query(Wallpaper).filter(Wallpaper.wallpaper_id == wallpaper_id).first()

    _wallpaper.like_count += 1
    db.commit()
    db.refresh(_wallpaper)

    return db.query(Wallpaper).filter(Wallpaper.wallpaper_id == wallpaper_id).first()

def deslike_wallpaper(db: Session, wallpaper_id: int):
    _wallpaper = get_wallpaper(db=db, wallpaper_id=wallpaper_id)

    if _wallpaper.like_count is None:
        _wallpaper.like_count = None
        db.commit()
        db.refresh(_wallpaper)
        return db.query(Wallpaper).filter(Wallpaper.wallpaper_id == wallpaper_id).first()
    
    if _wallpaper.like_count == 1:
        _wallpaper.like_count = None
        db.commit()
        db.refresh(_wallpaper)
        return db.query(Wallpaper).filter(Wallpaper.wallpaper_id == wallpaper_id).first()
    
    if _wallpaper.like_count > 1:
        _wallpaper.like_count -= 1
        db.commit()
        db.refresh(_wallpaper)
        return db.query(Wallpaper).filter(Wallpaper.wallpaper_id == wallpaper_id).first()

def create_wallpaper_db(db: Session, wallpaper: WallpaperSchema, file: UploadFile):
    try:
        category = db.query(Category).filter(Category.name == wallpaper.category).first()

        images_dir = "utils/images"
        os.makedirs(images_dir, exist_ok=True)
        file_path = os.path.join(images_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        url = f"images/{file.filename}"

        _wallpaper = Wallpaper(title=wallpaper.title, url=url, description=wallpaper.description, category_id=category.category_id)
        db.add(_wallpaper)
        db.commit()
        db.refresh(_wallpaper)
        
        resolutions = {
                "HD": (1280, 720),
                "FullHD": (1920, 1080),
                "4K": (3840, 2160)
            }
        for res_name, size in resolutions.items():
            resized_file_location = f"utils/resized_images/{res_name}_{file.filename}"
            resize_wallpaper(file_path, resized_file_location, size)
            
    except SQLAlchemyError as e:
        db.rollback()
        return Response(code="500",status="Error", message=f"Error description: {e}").dict(exclude_none=True)
    
    return _wallpaper

def remove_wallpaper(db: Session, wallpaper_id: int):
    _wallpaper = get_wallpaper(db=db, wallpaper_id=wallpaper_id)
    db.delete(_wallpaper)
    db.commit()
    db.refresh(_wallpaper)
    return _wallpaper

def update_wallpaper_db(db: Session, wallpaper_id: int, title: str, description: str):
    _wallpaper = get_wallpaper(db=db, wallpaper_id=wallpaper_id)
    _wallpaper.title = title
    _wallpaper.description = description
    db.commit()
    db.refresh(_wallpaper)
    return _wallpaper


def record_download(db: Session, wallpaper_id: int, name: str, email: str):
    try:
        wallpaper = db.query(Wallpaper).filter(Wallpaper.wallpaper_id == wallpaper_id).first()
        if not wallpaper:
            return False
        download = Download(
            wallpaper_id=wallpaper_id,
            download_datetime=datetime.now(),
            name=name,
            email=email
        )
        db.add(download)
        download_count_before = wallpaper.download_count

        if download_count_before is None:
            wallpaper.download_count = 1
        else:
            wallpaper.download_count += 1

        db.commit()
        db.refresh(wallpaper)
        return True
    except SQLAlchemyError as e:
        db.rollback()
        return Response(code="500",status="Error", message=f"Error: {e}").dict(exclude_none=True)