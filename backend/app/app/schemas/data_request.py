import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class DataRequestBase(BaseModel):
    id: Optional[uuid.UUID]
    name: Optional[str]
    #domain
    request_date: Optional[datetime]
    data_subjects: Optional[int]
    linked_datasets: Optional[str]
    request_size: Optional[float]
    status: Optional[str]
    tags: Optional[str]
    num_of_values: Optional[int]
    reason: Optional[str]
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
