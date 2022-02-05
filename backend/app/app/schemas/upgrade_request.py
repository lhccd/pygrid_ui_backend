import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UpgradeRequestBase(BaseModel):
    id: Optional[uuid.UUID]
    domain: Optional[uuid.UUID]
    request_date: Optional[datetime]
    requested_budget: Optional[float]
    status: Optional[str]
    tags: Optional[str]
    result_id: Optional[uuid.UUID]
    reason: Optional[str]
    updated_on: Optional[datetime]
    reviewer_comments: Optional[str]
    updated_by: Optional[str]
    request_owner: Optional[uuid.UUID]

class UpgradeRequestCreate(UpgradeRequestBase):
    pass

class UpgradeRequestUpdate(UpgradeRequestBase):
    pass
