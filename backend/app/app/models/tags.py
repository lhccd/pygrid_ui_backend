import uuid

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Tags(Base):
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255))
    domain = Column(UUID(as_uuid=True), ForeignKey("domain.id"))
    domain_rel = relationship("Domain", back_populates="domain_tags")
