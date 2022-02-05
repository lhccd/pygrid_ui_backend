import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class DataRequestBase(BaseModel):
    id: Optional[uuid.UUID]
    name: Optional[str]
    request_date: Optional[datetime]
    data_subjects: Optional[int]
    linked_datasets: Optional[str]
    request_size: Optional[float]
    status: Optional[str]
    tags: Optional[str]
    result_id: Optional[uuid.UUID]
    num_of_values: Optional[int]
    reason: Optional[str]
    updated_on: Optional[datetime]
    updated_by: Optional[str]
    reviewer_comments: Optional[str]

class DataRequestCreate(DataRequestBase):
    pass

class DataRequestUpdate(DataRequestBase):
    pass
