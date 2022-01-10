from pydantic import BaseModel
from typing import Optional
class Feedback(BaseModel):
    frustrations: Optional[str] = None
    suggestions:  Optional[str] = None
