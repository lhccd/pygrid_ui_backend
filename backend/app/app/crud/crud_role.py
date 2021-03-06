from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.roles import Role
from app.schemas.roles import RoleBase, RoleCreate, RoleUpdate, RoleInDB
from sqlalchemy import and_

class CRUDRole(CRUDBase[RoleBase, RoleCreate, RoleUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name).first()

    def get_by_id(self, db: Session, *, id: int) -> Optional[Role]:
        role = db.query(Role).filter(Role.id == id).first()
        return role

    def get_by_name_and_domain(self, db: Session, *, name: str, domain_name: str):
        role = db.query(Role).filter(Role.name == name, Role.domain_name == domain_name).first()
        return role

    def create(self, db: Session, *, obj_in: Role) -> Role:
        db_obj = Role(
            name = obj_in.name,
            can_make_data_requests = obj_in.can_make_data_requests,
            can_triage_data_requests = obj_in.can_triage_data_requests,
            can_manage_privacy_budget = obj_in.can_manage_privacy_budget,
            can_create_users = obj_in.can_create_users,
            can_manage_users = obj_in.can_manage_users,
            can_edit_roles = obj_in.can_edit_roles,
            can_manage_infrastructure = obj_in.can_manage_users,
            can_upload_data = obj_in.can_upload_data,
            can_upload_legal_document = obj_in.can_upload_legal_document,
            can_edit_domain_settings = obj_in.can_edit_domain_settings,
            domain_name = obj_in.domain_name,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_role(self, db: Session, *, db_obj: Role, obj_in: RoleInDB) -> Role:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

role = CRUDRole(Role)
