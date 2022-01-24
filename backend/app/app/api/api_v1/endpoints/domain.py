import io
import uuid
from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from ....schemas.domain import Domain, DomainCreate, DomainProfile, DomainConfiguration
from ....schemas.tags import Tags
from ....schemas.user import UserDetail, User
from ....schemas.domain_user import DomainUserCreate, DomainUser
from pydantic.networks import EmailStr

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


@router.post("/add-user", response_model=DomainUser)
def add_user_to_domain(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str = Body(...),
        user_email: EmailStr = Body(...),
        role: int = Body(...)
) -> Any:
    """
    Add a user into already created domain
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="This domain " + domain_name + " does not exists in the system",
        )
    user = crud.user.get_by_email(db, email=user_email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    existing_domain_user = crud.domain_user.get_user(db, domain_name=domain_name, user_email=user_email)
    if existing_domain_user:
        raise HTTPException(
            status_code=400,
            detail="This is user already in this domain"
        )
    domain_user_in = DomainUserCreate(user=user.id, domain=domain.id, role=role)
    print(domain_user_in)
    domain_user = crud.domain_user.create(db, obj_in=domain_user_in)
    return domain_user


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


@router.get("/domain-users", response_model=List[User])
def get_users_of_domain(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str,
) -> Any:
    """
    Get users of a specific domain
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="This domain " + domain_name + " does not exist",
        )
    return crud.domain.get_users(db, domain_name=domain_name)


@router.get("/domain-profile", response_model=DomainProfile)
def get_domain_profile(
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


@router.get("/domain-owner", response_model=UserDetail)
def get_domain_owner(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str,
) -> Any:
    """
    Get domain owner
    """
    domain_user = crud.domain_user.get_owner(db, domain_name=domain_name)
    if not domain_user:
        raise HTTPException(
            status_code=500,
            detail="Server Error!"
        )
    return domain_user


@router.get("/domain-tags", response_model=List[Tags])
def get_tags(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str,
) -> Any:
    """
    Get all tags for user
    """
    tags = crud.tags.get_tags_for_domain()
    if not tags:
        raise HTTPException(
            status_code=400,
            detail="This domain " + domain_name + " does not exist"
        )
    return tags


@router.get("/domain-configuration", response_model=DomainConfiguration)
def get_domain_configuration(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str,
) -> Any:
    """
    Get domain configuration, whether daa is required or not
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="This domain " + domain_name + " does not exist",
        )
    return domain


@router.delete("/delete")
def delete_domain(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str,
) -> Any:
    """
    Delete a domain
    """
    try:
        crud.domain.delete(db, name=domain_name)
    except Exception as err:
        raise HTTPException(
            status_code=500, detail="Error"
        )
