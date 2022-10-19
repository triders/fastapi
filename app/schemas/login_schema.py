from typing import Optional
from pydantic import BaseModel, EmailStr


class LoginBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class LoginRequest(LoginBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
