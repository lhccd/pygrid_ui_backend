from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255))
    can_make_data_requests = Column(Boolean(), default=False)
    can_triage_data_requests = Column(Boolean(), default=False)
    can_manage_privacy_budget = Column(Boolean(), default=False)
    can_create_users = Column(Boolean(), default=False)
    can_manage_users = Column(Boolean(), default=False)
    can_edit_roles = Column(Boolean(), default=False)
    can_manage_infrastructure = Column(Boolean(), default=False)
    can_upload_data = Column(Boolean(), default=False)
    can_upload_legal_document = Column(Boolean(), default=False)
    can_edit_domain_settings = Column(Boolean(), default=False)
    domain_name = Column(String(255))
    rel_user = relationship("Domain_User", back_populates="domain_role")

    def __str__(self) -> str:
        return (
            f"<Role id: {self.id}, name: {self.name}, "
            f"can_make_data_requests: {self.can_make_data_requests}, "
            f"can_triage_data_requests: {self.can_triage_data_requests}, "
            f"can_manage_privacy_budget: {self.can_manage_privacy_budget}, "
            f"can_create_users: {self.can_create_users}, "
            f"can_manage_users: {self.can_manage_users}, "
            f"can_edit_roles: {self.can_edit_roles}>, "
            f"can_manage_infrastructure: {self.can_manage_infrastructure}>"
            f"can_upload_data: {self.can_upload_data}>"
        )
