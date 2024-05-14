from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from .service import *
from .schemas import *

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def list_all_categories(db: Session = Depends(get_db)):
    return get_all_categories(db)

@router.get("/{category_id}")
async def read_category(category_id: int, db: Session = Depends(get_db)):
    _category = get_category(db, category_id)
    return Response(code="200",status="Ok", message="Success get data", result=_category).dict(exclude_none=True)

@router.post("/create")
async def create(request: RequestCategory, db: Session = Depends(get_db)):
    _category = create_category(db, request.parameter)
    return Response(code="200",status="Ok", message="Category created", result=_category).dict(exclude_none=True)

@router.delete("/{category_id}")
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    _category = remove_category(db, category_id)
    return Response(code="200",status="Ok", message="Category deleted", result=_category).dict(exclude_none=True)

@router.post("/update/{category_id}")
async def update_category(request: RequestCategory, db: Session = Depends(get_db)):
    _category = update_category(db,category_id=request.parameter.id)
    return Response(code="200",status="Ok", message="Category updated", result=_category).dict(exclude_none=True)
