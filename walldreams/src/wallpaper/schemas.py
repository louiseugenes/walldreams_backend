from pydantic import BaseModel

class Wallpaper(BaseModel):
    id: int
    title: str
    url: str