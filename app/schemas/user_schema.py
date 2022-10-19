from pydantic import BaseModel, EmailStr
from datetime import datetime


# Users
class UserBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserRequest(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime
