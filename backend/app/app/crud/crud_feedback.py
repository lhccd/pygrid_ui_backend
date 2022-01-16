from typing import Any, Dict, Optional, Union, List

from app.schemas.utils import FeedbackCreate, FeedbackUpdate

from app.models.feedback import Feedback

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase


class CRUDFeedback(CRUDBase[Feedback, FeedbackCreate, FeedbackUpdate]):

    def create_feedback(self,  db: Session, *, frustrations: str, suggestions: str) -> Feedback:
        db_obj = Feedback(
            frustrations=frustrations,
            suggestions=suggestions,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(self, *, db: Session) -> List[Feedback]:
        return db.query(Feedback).all()


feedback = CRUDFeedback(Feedback)

