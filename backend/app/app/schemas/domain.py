import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DomainBase(BaseModel):
    id: Optional[uuid.UUID]
    name: Optional[str] = None


class DomainCreate(DomainBase):
    deployed_on: Optional[datetime]
    last_updated: Optional[datetime]
    description: Optional[str] = None
    support_email: Optional[str] = None
    version_name: Optional[str] = None
    repository: Optional[str] = None
    branch: Optional[str] = None
    commit_hash: Optional[str] = None


class DomainUpdate(DomainCreate):
    pass


class DomainInDBBase(DomainBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Domain(DomainInDBBase):
    name: str
    pass


class DomainProfile(DomainInDBBase):
    name = str
    deployed_on: Optional[datetime]
    description: Optional[str] = None
    support_email: Optional[str] = None


class DomainConfiguration(DomainInDBBase):
    # TODO: Add require daa when it is ready
    #require_daa: bool
    pass


class DomainUpdateVersion(DomainInDBBase):
    last_updated: Optional[datetime]
    version_name: Optional[str] = None
    repository: Optional[str] = None
    branch: Optional[str] = None
    commit_hash: Optional[str] = None
