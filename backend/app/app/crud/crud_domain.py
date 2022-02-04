import base64
import uuid
from uuid import UUID

from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app import crud
from app.crud.base import CRUDBase
from app.models.domain import Domain
from app.schemas.domain import DomainBase, DomainCreate, DomainUpdate
from app.schemas.domain_user import DomainUserBase, DomainUserCreate, DomainUserUpdate

from app.models.pdf import PDFObject


class CRUDDomain(CRUDBase[Domain, DomainCreate, DomainUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Domain]:
        return db.query(Domain).filter(Domain.name == name).first()

    def get_by_id(self, db: Session, *, id: uuid.UUID) -> Optional[Domain]:
        return db.query(Domain).filter(Domain.id == id).first()

    def create(self, db: Session, *, obj_in: DomainCreate) -> Domain:
        _pdf_obj = PDFObject(binary=obj_in.pdf_daa)
        db.add(_pdf_obj)
        db.commit()
        db.refresh(_pdf_obj)
        db_obj = Domain(
            name=obj_in.name,
            deployed_on=obj_in.deployed_on,
            description=obj_in.description,
            support_email=obj_in.support_email,
            version_name=obj_in.version_name,
            repository=obj_in.repository,
            branch=obj_in.branch,
            commit_hash=obj_in.commit_hash,
            require_daa=True,
            pdf_daa_id=_pdf_obj.id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_no_daa(self, db: Session, *, obj_in: DomainCreate) -> Domain:
        db_obj = Domain(
            name=obj_in.name,
            deployed_on=obj_in.deployed_on,
            description=obj_in.description,
            support_email=obj_in.support_email,
            version_name=obj_in.version_name,
            repository=obj_in.repository,
            branch=obj_in.branch,
            commit_hash=obj_in.commit_hash,
            require_daa=False
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_user(self, db: Session, *, obj_in: DomainUserCreate):
        return crud.domain_user.create(db, obj_in=obj_in)

    def get_domains(self, db: Session):
        return db.query(Domain).all()

    def get_users(self, db: Session, *, domain_name: str):
        return crud.domain_user.get_users_of_domain(db, domain_name=domain_name)

    def update_version(self, db: Session, *, db_obj: Domain, obj_in: DomainUpdate) -> Domain:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


    def add_pdf(self, db: Session, *, obj_in: DomainUpdate) -> PDFObject:
        _pdf_obj = PDFObject(binary=obj_in.pdf_daa)
        db.add(_pdf_obj)
        db.commit()
        db.refresh(_pdf_obj)
        return _pdf_obj

    def update_config(self, db: Session, *, db_obj: Domain, obj_in: DomainUpdate) -> Domain:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_domain_pdf(self, db: Session, *, pdf_id: int) -> Optional[PDFObject]:
        return db.query(PDFObject).filter(PDFObject.id == pdf_id).first()
        #outfile = open('./test.pdf', 'wb')
        #outfile.write(obj.binary)
        #outfile.close()

    def delete_domain(self):
        # TODO: DELETE A DOMAIN
        pass

    def reset_domain(self):
        # TODO: RESET A DOMAIN, I DON'T KNOW WHAT IT MEANS EXACTLY????
        pass


domain = CRUDDomain(Domain)
