from fastapi import APIRouter, HTTPException
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate, UserRead
from auth.service import get_password_hash
from database import SessionLocal
from fastapi import Depends

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


crud_router = SQLAlchemyCRUDRouter(
    schema=UserCreate,
    db_model=User,
    db=get_db,
    create_schema=UserCreate,
)

@router.post('/create', response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# @router.get("/me", response_model=TokenData)
# async def read_users_me(current_user: TokenData = Depends(get_current_user)):
#     if not current_user.username:
#         raise HTTPException(status_code=404, detail="User not found")
#     return current_user