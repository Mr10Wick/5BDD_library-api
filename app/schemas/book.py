from datetime import date, datetime
from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str | None = None
    published_date: date | None = None

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: str | None = None
    published_date: date | None = None
    available: bool | None = None

class BookOut(BaseModel):
    id: int
    title: str
    author: str
    genre: str | None = None
    published_date: date | None = None
    available: bool
    created_at: datetime

    class Config:
        from_attributes = True
