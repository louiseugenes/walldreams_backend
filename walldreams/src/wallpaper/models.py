from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from category.models import *
from database import Base

class Wallpaper(Base):
    __tablename__ = 'wallpaper'

    wallpaper_id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('category.category_id'))
    category = relationship("Category", back_populates="wallpapers")
    downloads = relationship("Download", back_populates="wallpaper")
    upload_datetime = Column(DateTime)

class Download(Base):
    __tablename__ = 'download'

    download_id = Column(Integer, primary_key=True)
    wallpaper_id = Column(Integer, ForeignKey('wallpaper.wallpaper_id'))
    wallpaper = relationship("Wallpaper", back_populates="downloads")
    download_datetime = Column(DateTime)
    name = Column(String)
    email = Column(String)
  