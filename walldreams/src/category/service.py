from sqlalchemy.orm import Session
from .models import *
from .schemas import *
from sqlalchemy import or_, desc

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.category_id == category_id).first()

def get_all_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()    

def create_category(db: Session, category: CategorySchema):
    _category = Category(name=category.name)
    db.add(_category)
    db.commit()
    db.refresh(_category)
    return _category

def remove_category(db: Session, category_id: int):
    _category = get_category(db=db, category_id=category_id)
    db.delete(_category)
    db.commit()
    return True

def update_category(db: Session, category_id: int, name: str):
    _category = get_category(db=db, category_id=category_id)
    _category.name = name
    db.commit()
    db.refresh(_category)
    return _category

def search_category_db(db: Session, category_keyword: str):
    keyword_pattern = f"%{category_keyword}%"
    result = db.query(Category).filter(
        or_(
            Category.name.like(keyword_pattern),
        )
    ).all()
    return result

def count_category_db(db: Session, category_id: str):
    result = db.query(Category).filter(
        or_(
            Category.category_id == category_id,
        )
    ).first()
    if result.count is None:
        result.count = 1
        db.commit()
        db.refresh(result)
        return result
    else:
        result.count += 1
        db.commit()
        db.refresh(result)
        return result
    
def get_most_searched_categories(db: Session, limit: int = 3):
    return db.query(Category).filter(Category.count.isnot(None)
            ).order_by(desc(Category.count)
            ).limit(limit).all()