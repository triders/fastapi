from typing import Literal
from pydantic import BaseModel


class VoteBase(BaseModel):
    post_id: int
    vote: Literal[0, 1]

    class Config:
        orm_mode = True
