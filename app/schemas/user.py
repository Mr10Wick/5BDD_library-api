from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
