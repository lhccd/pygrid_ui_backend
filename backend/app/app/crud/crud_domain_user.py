import uuid
from typing import Any, Dict, Optional, Union

from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.domain_user import Domain_User
from app.schemas.domain_user import DomainUserBase, DomainUserCreate, DomainUserUpdate
from app import crud


class CRUDDomainUser(CRUDBase[Domain_User, DomainUserCreate, DomainUserUpdate]):

    def get_by_id(self, db: Session, *, id: int) -> Optional[Domain_User]:
        return db.query(Domain_User).filter(Domain_User.id == id).first()

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

    def get_users_of_domain(self, db: Session, *, domain_name: str):
        domain = crud.domain.get_by_name(db=db, name=domain_name)
        #return db.query(Domain_User).filter(Domain_User.domain == domain.id).all()
        domain_users = db.query(Domain_User).filter(Domain_User.domain == domain.id).all()
        users = []
        for u in domain_users:
            users.append(crud.user.get_by_id(db, id=u.user))
        return users


    def get_owner(self, db: Session, *, domain_name: str):
        """
        GET owner of the domain, return a user detail so that we can now user's name
        """
        users = self.get_users_of_domain(db, domain_name=domain_name)
        print(users)
        #return users.filter(Domain_User.Role == 1).first()  # find the user


domain_user = CRUDDomainUser(Domain_User)
