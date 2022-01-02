import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class DomainBase(BaseModel):
    id: Optional[uuid.UUID]
    name: Optional[str] = None

class DomainCreate(DomainBase):
    deployed_on: Optional[datetime]
    description: Optional[str] = None
    support_email: Optional[str] = None
    version_name: Optional[str] = None
    repository: Optional[str] = None
    branch: Optional[str] = None
    commit_hash: Optional[str] = None

class DomainUpdate(DomainCreate):
    pass
