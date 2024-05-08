from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..category.models import Category
from ..database import Base

class Wallpaper(Base):
  __tablename__= 'wallpaper'

  wallpaper_id = Column(Integer, primary_key=True)
  title = Column(String)
  url = Column(String)
  description = Column(String)
  category_id = Column(Integer, ForeignKey('category.category_id'))
  category = relationship("Category", back_populates="category")
  downloads = relationship("Download", back_populates="download_wallpaper")
  upload_datetime = Column(DateTime)

class DownloadWallpaper(Base):
  __tablename__= 'download_wallpaper'

  download_id = Column(Integer, primary_key=True)
  wallpapers = relationship("Wallpapers", back_populates="wallpaper")
  wallpaper_id = Column(Integer, ForeignKey('wallpaper.wallpaper_id'))
  download_datime = Column(DateTime)
  name = Column(String)
  email = Column(String)
  