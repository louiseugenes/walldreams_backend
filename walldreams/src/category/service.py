from sqlalchemy.orm import Session
from ..category.models import *
from ..database import SessionLocal

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.category_id == category_id).first()

def create_category(db: Session, category_data: dict):
    db_category = Category(**category_data)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
