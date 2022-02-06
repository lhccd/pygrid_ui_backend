import uuid
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Upgrade_Request(Base):
    __tablename__ = "upgrade_request"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain = Column(UUID(as_uuid=True), ForeignKey("domain.id"))
    request_date = Column(DateTime, default=datetime.datetime.utcnow)
    requested_budget = Column(Float(), default=0.0)
    status = Column(String(255))
    tags = Column(String(2048))
    result_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    reason = Column(String(1024))
    updated_on = Column(DateTime)
    reviewer_comments = Column(String(2048))
    updated_by = Column(String(255))
    request_owner_name = Column(String(255))
    initial_budget = Column(Float(), default=0.0)
    allocated_budget = Column(Float(), default=0.0)
    request_owner = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    request_owner_user = relationship("User", back_populates="upgrade_request_rel")

