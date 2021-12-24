from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    # default roles init
    administrator_in = schemas.RoleCreate(
        name = "Administrator",
        can_make_data_requests = True,
        can_triage_data_requests = True,
        can_manage_privacy_budget = True,
        can_create_users = True,
        can_manage_users = True,
        can_edit_roles = True,
        can_upload_data = True,
        can_upload_legal_document = True,
        can_edit_domain_settings = True
    )

    domain_owner_in = schemas.RoleCreate(
        name = "Domain Owner",
        can_make_data_requests = True,
        can_triage_data_requests = True,
        can_manage_privacy_budget = True,
        can_create_users = True,
        can_manage_users = True,
        can_edit_roles = True,
        can_upload_data = True,
        can_upload_legal_document = True,
        can_edit_domain_settings = True,
        can_manage_infrastructure = True
    )

    compliance_officer_in = schemas.RoleCreate(
        name = "Compliance Officer",
        can_triage_data_requests = True,
        can_manage_privacy_budget = True,
        can_manage_users = True
    )

    data_scientist_in = schemas.RoleCreate(
        name = "Data Scientist",
        can_make_data_requests = True
    )

    administrator = crud.role.get_by_name(db, name="Administrator")

    if not administrator:
        administrator = crud.role.create(db, obj_in=administrator_in)

    domain_owner = crud.role.get_by_name(db, name="Domain Owner")

    if not domain_owner:
        domain_owner = crud.role.create(db, obj_in=domain_owner_in)

    compliance_officer = crud.role.get_by_name(db, name="Compliance Officer")

    if not compliance_officer:
        compliance_officer = crud.role.create(db, obj_in=compliance_officer_in)

    data_scientist  = crud.role.get_by_name(db, name="Data Scientist")

    if not data_scientist:
        data_scientist = crud.role.create(db, obj_in=data_scientist_in)

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)

    if not user:
    #administrator + domain's owner + permissions
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            full_name="Thiago Porto",
            password=settings.FIRST_SUPERUSER_PASSWORD,
            status="active"
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
