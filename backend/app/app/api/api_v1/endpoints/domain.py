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

router = APIRouter()


@router.post("/create-domain", response_model=Domain)
async def create_domain(
        *,
        db: Session = Depends(deps.get_db),
        name=Body(...),
        description=Body(...),
        support_email=Body(...),
        version_name=Body(...),
        repository=Body(...),
        branch=Body(...),
        commit_hash=Body(...),
        daa_pdf: UploadFile = File(...),
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
    pdf_file = await daa_pdf.read()
    pdf_obj = models.pdf.PDFObject(binary=pdf_file)
    domain_in = schemas.DomainCreate(
        name=name, deployed_on=datetime.now(), description=description, support_email=support_email,
        version_name=version_name,
        repository=repository, branch=branch, commit_hash=commit_hash, pdf_daa=pdf_obj.binary
    )
    domain = crud.domain.create(db, obj_in=domain_in)
    return domain


@router.post("/create-domain-no-daa", response_model=Domain)
def create_domain_no_daa(
        *,
        db: Session = Depends(deps.get_db),
        name=Body(...),
        description=Body(...),
        support_email=Body(...),
        version_name=Body(...),
        repository=Body(...),
        branch=Body(...),
        commit_hash=Body(...),
) -> Any:
    """
    Create a domain with no daa
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
    domain = crud.domain.create_no_daa(db, obj_in=domain_in)
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


"""
@router.get("/domain-profile")
def get_domain_profile(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str,
) -> Any:
    domain = crud.domain.get_by_name(db, name=domain_name)
    owner = crud.domain_user.get_owner(db, domain_name=domain_name)
    list = []
    list.append(domain)
    list.append(owner)
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="This domain " + domain_name + " does not exist",
        )
    return list
"""


@router.get("/domain-pdf")
def get_domain_pdf(
        *,
        db: Session = Depends(deps.get_db),
        domain_name: str,
) -> Any:
    """
    Get the Daa Agreement Of the Domain
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="This domain " + domain_name + " does not exist",
        )
    pdf_id = domain.pdf_daa_id
    pdf_obj = crud.domain.get_domain_pdf(db, pdf_id=pdf_id)
    json_compatible_item_data = jsonable_encoder(pdf_obj.binary, custom_encoder={
        bytes: lambda v: base64.b64encode(v).decode('utf-8')})
    return json_compatible_item_data


@router.get("/domain-owner", response_model=UserDetail)
def get_domain_owner(
        *,
        db: Session = Depends(deps.get_db),
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


@router.put("/add-tags", response_model=List[Tags])
def add_tags_to_domain(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str = Body(...),
        tags: List[str] = Body(...),
) -> Any:
    """
        Add a tag to the domain
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    crud.tags.delete_all_from_domain(db, domain_id=domain.id)
    result = []
    for tag in tags:
        tag_in = Tags(name=tag, domain=domain.id)
        result.append(crud.tags.create(db, obj_in=tag_in))
    return result


@router.get("/domain-tags", response_model=List[Tags])
def get_tags(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str,
) -> Any:
    """
    Get all tags for the domain in which user is logged in
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    tags = crud.tags.get_tags_for_domain(db, domain_id=domain.id)
    if not tags:
        return []
    return tags


@router.get("/domain-tags-open", response_model=List[Tags])
def get_tags(
        *,
        db: Session = Depends(deps.get_db),
        domain_name: str,
) -> Any:
    """
    Get all tags for the domain.
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    tags = crud.tags.get_tags_for_domain(db, domain_id=domain.id)
    if not tags:
        return []
    return tags


@router.delete("/{tag_id}")
def delete_tag(
        tag_id: int,
        current_user: models.User = Depends(deps.get_current_user),
        db: Session = Depends(deps.get_db),
) -> None:
    """
    Deleting a single tag
    """
    try:
        crud.tags.delete_tag_by_id(db, tag_id=tag_id)
    except Exception as err:
        raise HTTPException(
            status_code=500, detail="Error"
        )


@router.get("/domain-version", response_model=DomainUpdateVersion)
def get_domain_version(
        *,
        db: Session = Depends(deps.get_db),
        domain_name: str,
) -> Any:
    """
    Get Domain Version
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="This domain " + domain_name + " does not exist",
        )
    return domain


@router.put("/update-domain-version", response_model=DomainUpdateVersion)
def update_domain(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str,
        repository: str = Body(...),
        branch: str = Body(...),
        commit_hash: str = Body(...),
) -> Any:
    """
    Update a domain's version
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    domain_in = DomainUpdate(repository=repository, branch=branch, commit_hash=commit_hash, last_updated=datetime.now())
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="The domain does not exist in the system",
        )
    domain = crud.domain.update_version(db, db_obj=domain, obj_in=domain_in)
    return domain


@router.put("/domain-profile", response_model=DomainProfile)
def update_domain_settings(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str,
        description: str = Body(...),
        support_email: str = Body(...),
) -> Any:
    """
    Update domain's settings
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    domain_in = DomainUpdate(description=description, support_email=support_email)
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="The domain does not exist in the system",
        )
    domain = crud.domain.update_version(db, db_obj=domain, obj_in=domain_in)
    return domain


@router.put("/add-pdf", response_model=Domain)
async def add_pdf(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str,
        daa_pdf: UploadFile = File(...)
) -> Any:
    """
    Add a pdf for a domain
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="The domain does not exist in the system",
        )
    pdf_file = await daa_pdf.read()
    pdf_obj = models.pdf.PDFObject(binary=pdf_file)
    domain_in = DomainUpdate(pdf_daa=pdf_obj.binary)
    pdf_model = crud.domain.add_pdf(db, obj_in=domain_in)
    return pdf_model

@router.put("/add-pdf-id")
async def add_pdf(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str,
        pdf_daa_id: int
) -> Any:
    """
    Add a pdf for a domain
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    if not domain:
        raise HTTPException(
            status_code=400,
            detail="The domain does not exist in the system",
        )
    domain_in = DomainUpdate(require_daa=True, last_updated=datetime.now(), pdf_daa_id=pdf_daa_id)
    domain = crud.domain.update_version(db, db_obj=domain, obj_in=domain_in)
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


@router.get("/role-by-user", response_model=RoleInDB)
def get_role_of_user_in_domain(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        user_email: EmailStr,
        domain_name: str
) -> Any:
    """
    Get user's role based on user's email.
    """
    user = crud.user.get_by_email(db, email=user_email)
    domain = crud.domain.get_by_name(db, name=domain_name)
    user_domain_role = crud.domain_user.get_by_user_id(db, user_id=user.id, domain_id=domain.id)
    role = crud.role.get_by_id(db, id=user_domain_role.role)

    if not role:
        raise HTTPException(
            status_code=500,
            detail="Error",
        )
    return role

@router.get("/get-roles-by-domain", response_model=List[RoleInDB])
def get_role_by_domain(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str
) -> Any:
    """
    Get roles in the domain by domain_name.
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    domain_user = crud.domain_user.get_by_domain_id(db, domain_id=domain.id)

    roles = []
    roles.append(domain_user[0])

    for k in domain_user:
        if k.role == roles[0].role:
            pass
        else:
            roles.insert(0, k)

    roles_in_domain = []
    for k in roles:
        role = crud.role.get_by_id(db, id=k.role)
        roles_in_domain.append(role)

    if not roles:
           raise HTTPException(
               status_code=500,
               detail="Error",
           )
    return roles_in_domain

@router.put("/update-role-in-domain", response_model=RoleInDB)
def update_role_in_domain(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
        domain_name: str,
        role_name: str,
        can_make_data_requests: bool = Body(...),
        can_triage_data_requests: bool = Body(...),
        can_manage_privacy_budget: bool = Body(...),
        can_create_users: bool = Body(...),
        can_manage_users: bool = Body(...),
        can_edit_roles: bool = Body(...),
        can_manage_infrastructure: bool = Body(...),
        can_upload_data: bool = Body(...),
        can_upload_legal_document: bool = Body(...),
        can_edit_domain_settings: bool = Body(...),
) -> Any:
    """
    Update a single role in the domain by domain_name.
    """
    domain = crud.domain.get_by_name(db, name=domain_name)
    domain_user = crud.domain_user.get_by_domain_id(db, domain_id=domain.id)

    # TODO: do some enumeration for the roles
    role_num = 1

    root = floor(domain_user[0].role / 4)

    target_role_id = root * 4 - role_num

    fetched_role = crud.role.get_by_id(db, id=target_role_id)

    role_in = RoleInDB(
        can_make_data_requests=can_make_data_requests,
        can_triage_data_requests=can_triage_data_requests,
        can_manage_privacy_budget=can_manage_privacy_budget,
        can_create_users=can_create_users,
        can_manage_users=can_manage_users,
        can_edit_roles=can_edit_roles,
        can_manage_infrastructure=can_manage_infrastructure,
        can_upload_data=can_upload_data,
        can_upload_legal_document=can_upload_legal_document,
        can_edit_domain_settings=can_edit_domain_settings
    )
    role = crud.role.update_role(db, db_obj=fetched_role, obj_in=role_in)

    if not role:
           raise HTTPException(
               status_code=500,
               detail="Domain doesn't have this role.",
           )
    return role
