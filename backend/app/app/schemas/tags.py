import uuid
from typing import Optional

from pydantic import BaseModel


class TagBase(BaseModel):
    name: Optional[str]
    domain: Optional[uuid.UUID]


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class Tags(TagBase):
    id: Optional[int]
    name: Optional[str]
    domain: Optional[uuid.UUID]

    class Config:
        orm_mode = True
