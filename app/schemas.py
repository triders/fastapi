from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    is_published: Optional[bool]

    class Config:
        orm_mode = True


class PostRequest(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
