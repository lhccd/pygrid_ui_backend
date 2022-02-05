import base64
import uuid
from uuid import UUID

from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app import crud
from app.crud.base import CRUDBase


from app.models.upgrade_request import Upgrade_Request
from app.schemas.upgrade_request import UpgradeRequestCreate, UpgradeRequestUpdate

class CRUDUpgradeRequests(CRUDBase[Upgrade_Request, UpgradeRequestCreate, UpgradeRequestUpdate]):

    def get_by_id(self, db: Session, *, id: uuid.UUID) -> Optional[Upgrade_Request]:
        return db.query(Upgrade_Request).filter(Upgrade_Request.id == id).first()

    def get_upgrade_requests_of_domain(self, db: Session, *, domain_id: uuid.UUID):
        return db.query(Upgrade_Request).filter(Upgrade_Request.domain == domain_id).all()

    def create(self, db: Session, *, obj_in: UpgradeRequestCreate):
        db_obj = Upgrade_Request(
            domain=obj_in.domain,
            request_date=obj_in.request_date,
            requested_budget= obj_in.requested_budget,
            status=obj_in.status,
            tags=obj_in.tags,
            reason=obj_in.reason,
            request_owner=obj_in.request_owner
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Upgrade_Request, obj_in: UpgradeRequestUpdate) -> Upgrade_Request:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def delete(self, db: Session, *, id: uuid.UUID) -> None:
        db.query(Upgrade_Request).filter(Upgrade_Request.id == id).delete()
        db.commit()


upgrade_requests = CRUDUpgradeRequests(Upgrade_Request)
