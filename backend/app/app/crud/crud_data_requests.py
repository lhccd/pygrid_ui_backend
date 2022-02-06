import base64
import uuid
from uuid import UUID

from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_

from app import crud
from app.crud.base import CRUDBase


from app.models.data_request import Data_Request
from app.schemas.data_request import DataRequestCreate, DataRequestUpdate

class CRUDDataRequests(CRUDBase[Data_Request, DataRequestCreate, DataRequestUpdate]):

    def get_by_id(self, db: Session, *, id: uuid.UUID) -> Optional[Data_Request]:
        return db.query(Data_Request).filter(Data_Request.id == id).first()

    def get_upgrade_requests_of_domain(self, db: Session, *, domain_id: uuid.UUID):
        return db.query(Data_Request).filter(Data_Request.domain == domain_id).all()

    def get_requests(self, db: Session, *, domain_id: uuid.UUID, status: str = "pending"):
        if status is not "pending":
            return db.query(Data_Request).filter(and_(
                Data_Request.domain == domain_id,
                not_(Data_Request.status.like("pending"))
            )).all()
        return db.query(Data_Request).filter(and_(
                Data_Request.domain == domain_id,
                Data_Request.status.like(status)
            )).all()

    def create(self, db: Session, *, obj_in: DataRequestCreate):
        db_obj = Data_Request(
            domain=obj_in.domain,
            request_date=obj_in.request_date,
            requested_budget=obj_in.requested_budget,
            status=obj_in.status,
            reason=obj_in.reason,
            request_owner=obj_in.request_owner
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Data_Request, obj_in: DataRequestUpdate) -> Data_Request:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def delete(self, db: Session, *, id: uuid.UUID) -> None:
        db.query(Data_Request).filter(Data_Request.id == id).delete()
        db.commit()


data_requests = CRUDDataRequests(Data_Request)
