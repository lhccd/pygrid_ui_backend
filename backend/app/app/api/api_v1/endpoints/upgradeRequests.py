import base64
import io
import uuid
from datetime import datetime
from math import floor
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, File, UploadFile, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from starlette.responses import StreamingResponse, PlainTextResponse

from ....schemas.domain import Domain, DomainCreate, DomainUpdate, DomainProfile, DomainUpdateVersion
from ....schemas.tags import Tags
from ....schemas.user import UserDetail, User
from ....schemas.domain_user import DomainUserCreate, DomainUser
from ....schemas.roles import RoleInDB
from pydantic.networks import EmailStr
from fastapi.responses import FileResponse
from ....schemas.upgrade_request import UpgradeRequest, UpgradeRequestCreate

router = APIRouter()


@router.post("/create", response_model=UpgradeRequest)
def create_request(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str = Body(...),
        requested_budget: float = Body(...),
        tags: str = Body(None),
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
                                           tags=tags,
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


@router.put("/accept", response_model=UpgradeRequest)
def accept_request(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),

) -> Any:
    pass


