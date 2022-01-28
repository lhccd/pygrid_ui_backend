import uuid
from uuid import UUID

from typing import Any, Dict, Optional, Union

from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.domain_user import Domain_User
from app.models.domain import Domain
from app.schemas.domain_user import DomainUserBase, DomainUserCreate, DomainUserUpdate
from app import crud


class CRUDDomainUser(CRUDBase[Domain_User, DomainUserCreate, DomainUserUpdate]):

    def get_by_id(self, db: Session, *, id: int) -> Optional[Domain_User]:
        return db.query(Domain_User).filter(Domain_User.id == id).first()

    def get_by_user_id(self, db: Session, *, user_id: uuid.UUID, domain_id: uuid.UUID) -> Optional[Domain_User]:
        return db.query(Domain_User).filter(Domain_User.user == user_id, Domain_User.domain == domain_id).first()

    def get_user(self, db: Session, *, domain_name: str, user_email: EmailStr):
        domain = crud.domain.get_by_name(db=db, name=domain_name)
        user = crud.user.get_by_email(db, email=user_email)
        return db.query(Domain_User).filter(Domain_User.domain == domain.id and Domain_User.user == user.id).first()

    def create(self, db: Session, *, obj_in: Domain_User) -> Domain_User:
        db_obj = Domain_User(
            user=obj_in.user,
            domain=obj_in.domain,
            role=obj_in.role
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_role(self, db: Session, *, domain_name: str, user_email):
        # TODO: GET User Role by domain name and user email, return None if user is not in the domain
        pass

    def get_domain_owner_role(self, db: Session, *, domain_name: str):
        domain_user_owner = db.query(Domain_User).filter(Domain_User.role == 2).first()
        return domain_user_owner

    def get_users_of_domain(self, db: Session, *, domain_name: str):
        domain = crud.domain.get_by_name(db=db, name=domain_name)
        #return db.query(Domain_User).filter(Domain_User.domain == domain.id).all()
        domain_users = db.query(Domain_User).filter(Domain_User.domain == domain.id).all()
        users = []
        for u in domain_users:
            users.append(crud.user.get_by_id(db, id=u.user))
        return users

    def get_current_user_domain(self, db: Session, *, user_id: uuid.UUID) -> Optional[Domain]:
        # assumption - user belongs to just one domain
        domain_users = db.query(Domain_User).filter(Domain_User.user == user_id).first()
        domain = crud.domain.get_by_id(db=db, id=domain_users.domain)
        return domain

    def get_owner(self, db: Session, *, domain_name: str):
        """
        GET owner of the domain, return a user detail so that we can know user's name
        """
        domain_user_owner = self.get_domain_owner_role(db, domain_name=domain_name)
        print(domain_user_owner.user)
        owner = crud.user.get_by_id(db=db, id=domain_user_owner.user)
        return owner


domain_user = CRUDDomainUser(Domain_User)
