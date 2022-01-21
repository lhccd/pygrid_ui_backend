import uuid
import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class Domain(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    deployed_on = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(String(2048))
    support_email = Column(String(255))
    version_name = Column(String(255))
    repository = Column(String(255))
    branch = Column(String(255))
    commit_hash = Column(String(255))
    users_in_domain = relationship("Domain_User", back_populates="domain_reference")
    domain_tags = relationship("Tags", back_populates="domain_rel")
