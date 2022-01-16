from app.core.celery_app import celery_app
from app.utils import send_test_email
from typing import Any, List

from fastapi import APIRouter, Body, Depends
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from app import crud, models, schemas

from ....schemas.utils import Feedback

from app.api import deps


router = APIRouter()


@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}


@router.post("/submit-feedback", response_model=Feedback, status_code=201)
def submit_feedback(
    *,
    db: Session = Depends(deps.get_db),
    frustrations: str = Body(...),
    suggestions: str = Body(...),
) -> Any:

    return crud.feedback.create_feedback(db, frustrations=frustrations, suggestions=suggestions)


@router.get("/feedbacks", response_model=List[Feedback], status_code=201)
def get_all_feedbacks(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:

    return crud.feedback.get_all(db=db)
