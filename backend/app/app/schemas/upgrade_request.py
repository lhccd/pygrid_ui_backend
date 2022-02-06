import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UpgradeRequestBase(BaseModel):
    id: Optional[uuid.UUID]
    request_owner_name: Optional[str] = None
    domain: Optional[uuid.UUID] = None
    request_date: Optional[datetime] = None
    requested_budget: Optional[float] = None
    status: Optional[str] = None
    reason: Optional[str] = None
    request_owner: Optional[uuid.UUID] = None
    initial_budget: Optional[float] = None


class UpgradeRequestCreate(UpgradeRequestBase):
    pass


class UpgradeRequestUpdate(UpgradeRequestBase):
    reviewer_comments: Optional[str] = None
    updated_on: Optional[datetime] = None
    updated_by: Optional[str] = None
    pass


class UpgradeRequestInDBBase(UpgradeRequestBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


class UpgradeRequest(UpgradeRequestInDBBase):
    reviewer_comments: Optional[str] = None
    updated_on: Optional[datetime] = None
    updated_by: Optional[str] = None
    pass
