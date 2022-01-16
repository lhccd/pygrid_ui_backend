from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.domain_user import Domain_User
from app.schemas.domain_user import DomainUserBase, DomainUserCreate, DomainUserUpdate

class CRUDDomainUser(CRUDBase[DomainUserBase, DomainUserCreate, DomainUserUpdate]):
    def get_by_id(self, db: Session, *, id: int) -> Optional[Domain_User]:
        return db.query(Domain_User).filter(Domain_User.id == id).first()

    def create(self, db: Session, *, obj_in: Domain_User) -> Domain_User:
        db_obj = Domain_User(
            user = obj_in.user,
            domain = obj_in.domain,
            role = obj_in.role
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

domain_user = CRUDDomainUser(Domain_User)
