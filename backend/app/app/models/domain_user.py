import uuid

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class Domain_User(Base):
    __tablename__ = "domain_user"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    users = relationship("User", back_populates="domains")
    domain = Column(UUID(as_uuid=True), ForeignKey("domain.id"))
    domain_reference = relationship("Domain", back_populates="users_in_domain")
    role = Column(Integer, ForeignKey("role.id"))
    domain_role = relationship("Role", back_populates="rel_user")
