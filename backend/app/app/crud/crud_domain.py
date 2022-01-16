from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.domain import Domain
from app.schemas.domain import DomainBase, DomainCreate, DomainUpdate

class CRUDDomain(CRUDBase[Domain, DomainCreate, DomainUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Domain]:
        return db.query(Domain).filter(Domain.name == name).first()

    def create(self, db: Session, *, obj_in: DomainCreate) -> Domain:
        db_obj = Domain(
            name = obj_in.name,
            deployed_on = obj_in.deployed_on,
            description = obj_in.description,
            support_email = obj_in.support_email,
            version_name = obj_in.version_name,
            repository = obj_in.repository,
            branch = obj_in.branch,
            commit_hash = obj_in.commit_hash
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    def get_domains(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(Domain).offset(skip).limit(limit).all()

domain = CRUDDomain(Domain)
