"""

from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.schemas.utils import Feedback

class CRUDFeedback(CRUDBase[Feedback]):

    def create_feedback(self,  db: Session, *, frustrations: str, suggestions: str) -> Feedback:
        db_obj = Feedback(
            frustrations=frustrations,
            suggestions=suggestions,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

"""
