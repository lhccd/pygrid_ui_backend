import uuid
from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from ....schemas.data_request import DataRequest, DataRequestCreate, DataRequestUpdate
from ....schemas.user import UserBudget

router = APIRouter()


@router.post("/create", response_model=DataRequest)
def create_request(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str = Body(...),
        request_size: float = Body(...),
        reason: str = Body(None),
        data_subjects: str = Body(None),
        linked_datasets: str = Body(None),
        tags: str = Body(None),
        num_of_values: str = Body(None),
) -> Any:
    """
    Create a request
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="This domain " + domain_name + " does not exist in the system",
        )
    data_request_in = DataRequestCreate(
        name=current_user.full_name,
        domain=domain.id,
        data_subjects=data_subjects,
        linked_datasets=linked_datasets,
        tags=tags,
        num_of_values=num_of_values,
        request_date=datetime.now(),
        request_size=request_size,
        status="pending",
        reason=reason,
        request_owner=current_user.id
    )
    data_request = crud.data_requests.create(db, obj_in=data_request_in)
    if not data_request:
        raise HTTPException(
            status_code=500,
            detail="error when creating an data requests"
        )
    return data_request


@router.get("/", response_model=List[DataRequest])
def get_requests(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str
) -> Any:
    domain = crud.domain.get_by_name(db, name=domain_name)
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="This domain " + domain_name + " does not exist in the system",
        )
    return crud.data_requests.get_data_requests_of_domain(db, domain_id=domain.id)


@router.get("/current", response_model=List[DataRequest])
def get_current_requests(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str
) -> Any:
    domain = crud.domain.get_by_name(db, name=domain_name)
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="This domain " + domain_name + " does not exist in the system",
        )
    return crud.data_requests.get_requests(db, domain_id=domain.id)



@router.get("/history", response_model=List[DataRequest])
def get_history_requests(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str
) -> Any:
    domain = crud.domain.get_by_name(db, name=domain_name)
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="This domain " + domain_name + " does not exist in the system",
        )
    return crud.data_requests.get_requests(db, domain_id=domain.id, status="history")


@router.put("/accept", response_model=DataRequest)
def accept_request(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        request_id: uuid.UUID,
        reviewer_comments: str,
) -> Any:
    request = crud.data_requests.get_by_id(db, id=request_id)
    if not request:
        raise HTTPException(
            status_code=400,
            detail="This request does not exist in the system",
        )
    request_in = DataRequestUpdate(
        status="accepted",
        reviewer_comments=reviewer_comments,
        updated_by=current_user.full_name,
        updated_on=datetime.now()
    )
    result = crud.data_requests.update(db, db_obj=request, obj_in=request_in)
    user = crud.user.get_by_id(db, id=result.request_owner)
    user_in = UserBudget(budget=(user.budget + request.requested_budget))
    crud.user.update_budget(db, db_obj=user, obj_in=user_in)
    return result


@router.put("/reject", response_model=DataRequest)
def accept_request(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        request_id: uuid.UUID,
        reviewer_comments: str,
) -> Any:
    request = crud.data_requests.get_by_id(db, id=request_id)
    if not request:
        raise HTTPException(
            status_code=400,
            detail="This request does not exist in the system",
        )
    request_in = DataRequestUpdate(
        status="rejected",
        reviewer_comments=reviewer_comments,
        updated_by=current_user.full_name,
        updated_on=datetime.now()
    )
    result = crud.data_requests.update(db, db_obj=request, obj_in=request_in)
    return result


