from pydantic import BaseModel

class Wallpaper(BaseModel):
    wallpaper_id: int
    title: str
    url: str
    description: str
    week_download_count: int
    category: str
    like_count: int
    upload_datetime: str

class DownloadWallpaper(BaseModel):
    download_id: int
    wallpaper_id: int
    name: str
    email: str
    download_datetime: str

