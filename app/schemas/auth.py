from pydantic import BaseModel

class UserRegister(BaseModel):
    name: str
    email: str
    phone: str | None = None
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
