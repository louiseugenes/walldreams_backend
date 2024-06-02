from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from wallpaper.models import *
from database import Base

class Category(Base):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True)
    name = Column(String)
    wallpapers = relationship("Wallpaper", back_populates="category")
    count = Column(Integer)