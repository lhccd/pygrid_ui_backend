from typing import Optional

from pydantic import BaseModel

class RoleBase(BaseModel):
    name: Optional[str] = None

class RoleCreate(RoleBase):
    can_make_data_requests: Optional[bool]
    can_triage_data_requests: Optional[bool]
    can_manage_privacy_budget: Optional[bool]
    can_create_users: Optional[bool]
    can_manage_users: Optional[bool]
    can_edit_roles: Optional[bool]
    can_manage_infrastructure: Optional[bool]
    can_upload_data: Optional[bool]
    can_upload_legal_document: Optional[bool]
    can_edit_domain_settings: Optional[bool]

class RoleUpdate(RoleBase):
    pass

class RoleInDB(RoleBase):
    can_make_data_requests: Optional[bool]
    can_triage_data_requests: Optional[bool]
    can_manage_privacy_budget: Optional[bool]
    can_create_users: Optional[bool]
    can_manage_users: Optional[bool]
    can_edit_roles: Optional[bool]
    can_manage_infrastructure: Optional[bool]
    can_upload_data: Optional[bool]
    can_upload_legal_document: Optional[bool]
    can_edit_domain_settings: Optional[bool]

    class Config:
            orm_mode = True
