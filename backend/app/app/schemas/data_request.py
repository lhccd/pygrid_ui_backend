import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class DataRequestBase(BaseModel):
    id: Optional[uuid.UUID]
    name: Optional[str] = None
    domain: Optional[uuid.UUID] = None
    request_date: Optional[datetime] = None
    data_subjects: Optional[int] = None
    linked_datasets: Optional[str] = None
    request_size: Optional[float] = None
    status: Optional[str] = None
    tags: Optional[str] = None
    num_of_values: Optional[int] = None
    reason: Optional[str] = None
    request_owner: Optional[uuid.UUID] = None

class DataRequestCreate(DataRequestBase):
    pass

class DataRequestUpdate(DataRequestBase):
    reviewer_comments: Optional[str] = None
    updated_on: Optional[datetime] = None
    updated_by: Optional[str] = None
    result_id: Optional[uuid.UUID] = None
    pass


class DataRequestInDBBase(DataRequestBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


class DataRequest(DataRequestInDBBase):
    reviewer_comments: Optional[str] = None
    updated_on: Optional[datetime] = None
    updated_by: Optional[str] = None
    result_id: Optional[uuid.UUID] = None
    pass
