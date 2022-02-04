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
    pdf_daa: Optional[bytes] = None


class DomainUpdate(DomainCreate):
    require_daa: Optional[bool] = None
    pdf_daa_id: Optional[int] = None


class DomainInDBBase(DomainBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Domain(DomainInDBBase):
    name: Optional[str]
    pass


class DomainProfile(DomainInDBBase):
    name = str
    deployed_on: Optional[datetime]
    description: Optional[str] = None
    support_email: Optional[str] = None
    require_daa: Optional[bool] = None



class DomainUpdateVersion(DomainInDBBase):
    last_updated: Optional[datetime]
    version_name: Optional[str] = None
    repository: Optional[str] = None
    branch: Optional[str] = None
    commit_hash: Optional[str] = None
