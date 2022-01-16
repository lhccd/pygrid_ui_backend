from pydantic import BaseModel
from typing import Optional


class FeedbackBase(BaseModel):
    frustrations: Optional[str] = None
    suggestions:  Optional[str] = None


class FeedbackCreate(FeedbackBase):
    frustrations: Optional[str] = None
    suggestions:  Optional[str] = None


class FeedbackUpdate(FeedbackBase):
    frustrations: Optional[str] = None
    suggestions:  Optional[str] = None


class FeedbackInDBBase(FeedbackBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Feedback(FeedbackInDBBase):
    frustrations: Optional[str] = None
    suggestions:  Optional[str] = None
