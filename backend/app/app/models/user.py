import uuid

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, index=True)
    email = Column(String(255))
    hashed_password = Column(String(512))
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    #inserted new columns
    name = Column(String(255), default="")
    budget = Column(Float(), default=0.0)
    salt = Column(String(255))
    private_key = Column(String(2048))
    verify_key = Column(String(2048))
    added_by = Column(String(2048))
    website = Column(String(2048))
    institution = Column(String(2048))
    created_at = Column(DateTime())
    status = Column(String(255))
    daa_pdf = Column(Integer, ForeignKey("daa_pdf.id"))
    #role = Column(Integer, ForeignKey("role.id"))
    #roles = relationship("Role", back_populates="user_role")
    domains = relationship("Domain_User", back_populates="users")
