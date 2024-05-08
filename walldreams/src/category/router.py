from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .service import *
from .models import *

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/categorys/{category_id}")
async def read_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="category not found")
    return category

@router.post("/categorys/")
async def create_category(category_data: Category, db: Session = Depends(get_db)):
    return create_category(db, category_data.dict())
