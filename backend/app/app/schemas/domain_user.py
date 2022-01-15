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
    pass

class DomainUserUpdate(DomainUserBase):
    pass
