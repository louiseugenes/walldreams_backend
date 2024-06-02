from pydantic import BaseModel
from typing import Optional
from pydantic.fields import Field
from typing import Generic, TypeVar, List
from pydantic.generics import GenericModel
from datetime import datetime
from fastapi import UploadFile, File

T = TypeVar('T')

class WallpaperSchema(BaseModel):
    wallpaper_id: Optional[int]=None
    title: Optional[str]=None
    url: Optional[str]=None
    description: Optional[str]=None
    download_count: Optional[int]=None
    category: Optional[str]=None
    like_count: Optional[int]=None
    upload_datetime: Optional[datetime] = None

    class Config:
        from_attributes = True
        exclude = {"wallpaper_id", "url", "download_count", "like_count", "upload_datetime"}

class RequestWallpaper(BaseModel):
    parameter: WallpaperSchema = Field(...)
    file: UploadFile = File(...)

class DownloadSchema(BaseModel):
    download_id: Optional[int]=None
    wallpaper_id: Optional[int]=None
    name: Optional[str]=None
    email: Optional[str]=None
    download_datetime: Optional[str]=None

    class Config:
        from_attributes = True

class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[List[T]] = None
