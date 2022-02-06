import uuid
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Data_Request(Base):
    __tablename__ = "data_request"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain = Column(UUID(as_uuid=True), ForeignKey("domain.id"))
    domain_relation = relationship("Domain", back_populates="data_request_rel_domain")
    name = Column(String(255))
    requester_name = Column(String(255))
    request_date = Column(DateTime, default=datetime.datetime.utcnow)
    data_subjects = Column(Integer())
    linked_datasets = Column(String(255))
    request_size = Column(Float(), default=0.0)
    status = Column(String(255))
    tags = Column(String(2048))
    result_id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    num_of_values = Column(Integer())
    reason = Column(String(1024))
    updated_on = Column(DateTime)
    updated_by = Column(String(255))
    reviewer_comments = Column(String(2048))
    request_owner = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    budget = Column(Float(), default=0.0)
    request_owner_user_rel = relationship("User", back_populates="data_request_rel")
