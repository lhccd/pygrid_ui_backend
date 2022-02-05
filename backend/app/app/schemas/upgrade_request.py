import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UpgradeRequestBase(BaseModel):
    id: Optional[uuid.UUID]
    domain: Optional[uuid.UUID] = None
    request_date: Optional[datetime] = None
    requested_budget: Optional[float] = None
    status: Optional[str] = None
    tags: Optional[str] = None
    result_id: Optional[uuid.UUID] = None
    reason: Optional[str] = None
    updated_on: Optional[datetime] = None
    reviewer_comments: Optional[str] = None
    updated_by: Optional[str] = None
    request_owner: Optional[uuid.UUID] = None


class UpgradeRequestCreate(UpgradeRequestBase):
    pass


class UpgradeRequestUpdate(UpgradeRequestBase):
    pass


class UpgradeRequestInDBBase(UpgradeRequestBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


class UpgradeRequest(UpgradeRequestInDBBase):
    pass
