from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.models.pdf import PDFObject
from app.schemas.user import UserCreate, UserUpdate, UserProfile


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_open(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            website=obj_in.website,
            institution=obj_in.institution,
            budget=obj_in.budget,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_user_profile(self, db: Session, *, id: int) -> Optional[UserProfile]:
        return db.query(User).filter(User.id == id).first()

    def create_with_daa(self, db: Session, *, obj_in: UserCreate) -> User:
        _pdf_obj = PDFObject(binary=obj_in.daa_pdf)
        db.add(_pdf_obj)
        db.commit()
        db.refresh(_pdf_obj)
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            website=obj_in.website,
            institution=obj_in.institution,
            budget=obj_in.budget,
            daa_pdf=_pdf_obj.id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def delete(self, db: Session, *, email: str) -> None:
        db.query(User).filter(User.email == email).delete()
        db.commit()

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    ### Just for testing purposes
    def get_pdf_by_email(self, db: Session, *, email: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        pdf_id = user.daa_pdf
        pdf = db.query(PDFObject).filter(PDFObject.id == pdf_id).first()
        with open('example.pdf', 'wb') as fout:
            fout.write(pdf.binary)


user = CRUDUser(User)
