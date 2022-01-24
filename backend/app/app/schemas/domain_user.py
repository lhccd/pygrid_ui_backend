import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DomainUserBase(BaseModel):
    id: Optional[int]
    user: Optional[uuid.UUID]
    domain: Optional[uuid.UUID]
    role: Optional[int]


class DomainUserCreate(DomainUserBase):
    id: Optional[int]
    user: Optional[uuid.UUID]
    domain: Optional[uuid.UUID]
    role: Optional[int]


class DomainUserUpdate(DomainUserBase):
    id: Optional[int]
    user: Optional[uuid.UUID]
    domain: Optional[uuid.UUID]
    role: Optional[int]


class DomainUserDB(DomainUserBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class DomainUser(DomainUserDB):
    user: Optional[uuid.UUID]
    domain: Optional[uuid.UUID]
    role: Optional[int]
