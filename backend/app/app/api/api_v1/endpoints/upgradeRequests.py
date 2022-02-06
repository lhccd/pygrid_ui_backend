import uuid
from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from ....schemas.upgrade_request import UpgradeRequest, UpgradeRequestCreate, UpgradeRequestUpdate

router = APIRouter()


@router.post("/create", response_model=UpgradeRequest)
def create_request(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str = Body(...),
        requested_budget: float = Body(...),
        reason: str = Body(None)
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
    upgrade_request_in = UpgradeRequestCreate(domain = domain.id,
                                           request_date=datetime.now(),
                                           requested_budget=requested_budget,
                                           status="pending",
                                           reason=reason,
                                           request_owner=current_user.id)
    upgrade_request = crud.upgrade_requests.create(db, obj_in=upgrade_request_in)
    if not upgrade_request:
        raise HTTPException(
            status_code=500,
            detail="error when creating an upgrade requests"
        )
    return upgrade_request


@router.get("/", response_model=List[UpgradeRequest])
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
    return crud.upgrade_requests.get_upgrade_requests_of_domain(db, domain_id=domain.id)


@router.get("/current", response_model=List[UpgradeRequest])
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
    return crud.upgrade_requests.get_requests(db, domain_id=domain.id)



@router.get("/history", response_model=List[UpgradeRequest])
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
    return crud.upgrade_requests.get_requests(db, domain_id=domain.id, status="history")


@router.put("/accept", response_model=UpgradeRequest)
def accept_request(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        request_id: uuid.UUID,
        reviewer_comments: str,
) -> Any:
    request = crud.upgrade_requests.get_by_id(db, id=request_id)
    if not request:
        raise HTTPException(
            status_code=400,
            detail="This request does not exist in the system",
        )
    request_in = UpgradeRequestUpdate(
        status="accepted",
        reviewer_comments=reviewer_comments,
        updated_by=current_user.full_name,
        updated_on=datetime.now()
    )
    result = crud.upgrade_requests.update(db, db_obj=request, obj_in=request_in)
    return result


@router.put("/reject", response_model=UpgradeRequest)
def accept_request(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        request_id: uuid.UUID,
        reviewer_comments: str,
) -> Any:
    request = crud.upgrade_requests.get_by_id(db, id=request_id)
    if not request:
        raise HTTPException(
            status_code=400,
            detail="This request does not exist in the system",
        )
    request_in = UpgradeRequestUpdate(
        status="rejected",
        reviewer_comments=reviewer_comments,
        updated_by=current_user.full_name,
        updated_on=datetime.now()
    )
    result = crud.upgrade_requests.update(db, db_obj=request, obj_in=request_in)
    return result


