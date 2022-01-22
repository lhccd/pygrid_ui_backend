from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.tags import Tags
from app.schemas.tags import TagCreate, TagUpdate

class CRUDTags(CRUDBase[Tags, TagCreate, TagUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Tags]:
        return db.query(Tags).filter(Tags.name == name).first()

    def get_by_id(self, db: Session, *, id: int) -> Optional[Tags]:
        return db.query(Tags).filter(Tags.id == id).first()

    def create(self, db: Session, *, obj_in: TagCreate) -> Tags:
        db_obj = Tags(
            name = obj_in.name,
            deployed_on = obj_in.deployed_on,
            domain = obj_in.domain
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all_tags(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(Tags).offset(skip).limit(limit).all()

    def get_tags_for_domain(self):
        pass

tags = CRUDTags(Tags)
