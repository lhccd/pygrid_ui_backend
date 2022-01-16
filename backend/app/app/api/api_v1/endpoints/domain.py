import io
import uuid
from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, File, UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from fastapi.responses import FileResponse

from app import crud, models, schemas
from starlette.responses import StreamingResponse

from app.models.domain import Domain
from ....models.pdf import PDFObject
from ....schemas.user import UserProfile, PendingUser, ActiveUser, DeniedUser, UserDetail, UserUpdate
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email
from ....schemas.domain import Domain, DomainCreate, DomainDetail

router = APIRouter()


@router.post("/create-domain", response_model=Domain)
def create_domain(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        name=Body(...),
        description=Body(...),
        support_email=Body(...),
        version_name=Body(...),
        repository=Body(...),
        branch=Body(...),
        commit_hash=Body(...),
) -> Any:
    """
    Create a domain
    """
    domain = crud.domain.get_by_name(db, name=name)
    if domain:
        raise HTTPException(
            status_code=400,
            detail="This domain " + name + " already exists in the system",
        )
    domain_in = schemas.DomainCreate(
        name=name, deployed_on=datetime.now(), description=description, support_email=support_email,
        version_name=version_name,
        repository=repository, branch=branch, commit_hash=commit_hash
    )
    domain = crud.domain.create(db, obj_in=domain_in)
    return domain


@router.get("/domains", response_model=List[Domain])
def get_all_domains(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Get all the domains
    """
    domains = crud.domain.get_domains(db)
    return domains


@router.get("/domain-detail", response_model=DomainDetail)
def get_domain(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str,
) -> Any:
    """
    Get a specific domain by domain name
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="This domain " + domain_name + " does not exist",
        )
    return domain
