from typing import Optional

from pydantic import BaseModel, EmailStr

class Role(BaseModel):
    name: Optional[str]
    can_make_data_requests: Optional[bool] = False
    can_triage_data_requests: Optional[bool] = False
    can_manage_privacy_budget: Optional[bool] = False
    can_create_users: Optional[bool] = False
    can_manage_users: Optional[bool] = False
    can_edit_roles: Optional[bool] = False
    can_manage_infrastructure: Optional[bool] = False
    can_upload_data: Optional[bool] = False
    can_upload_legal_document: Optional[bool] = False
    can_edit_domain_settings: Optional[bool] = False

class RoleAdmin(BaseModel):
    name: Optional[str] = "Admin"
    can_make_data_requests: Optional[bool] = True
    can_triage_data_requests: Optional[bool] = True
    can_manage_privacy_budget: Optional[bool] = True
    can_create_users: Optional[bool] = True
    can_manage_users: Optional[bool] = True
    can_edit_roles: Optional[bool] = True
    can_manage_infrastructure: Optional[bool] = False
    can_upload_data: Optional[bool] = True
    can_upload_legal_document: Optional[bool] = True
    can_edit_domain_settings: Optional[bool] = True

class RoleDataScientist(BaseModel):
    name: Optional[str] = "Data Scientist"
    can_make_data_requests: Optional[bool] = True
    can_triage_data_requests: Optional[bool] = False
    can_manage_privacy_budget: Optional[bool] = False
    can_create_users: Optional[bool] = False
    can_manage_users: Optional[bool] = False
    can_edit_roles: Optional[bool] = False
    can_manage_infrastructure: Optional[bool] = False
    can_upload_data: Optional[bool] = False
    can_upload_legal_document: Optional[bool] = False
    can_edit_domain_settings: Optional[bool] = False

class RoleComplianceOfficer(BaseModel):
    name: Optional[str] = "Compliance Officer"
    can_make_data_requests: Optional[bool] = False
    can_triage_data_requests: Optional[bool] = True
    can_manage_privacy_budget: Optional[bool] = True
    can_create_users: Optional[bool] = False
    can_manage_users: Optional[bool] = True
    can_edit_roles: Optional[bool] = False
    can_manage_infrastructure: Optional[bool] = False
    can_upload_data: Optional[bool] = False
    can_upload_legal_document: Optional[bool] = False
    can_edit_domain_settings: Optional[bool] = False

class RoleOwner(BaseModel):
    name: Optional[str] = "Owner"
    can_make_data_requests: Optional[bool] = True
    can_triage_data_requests: Optional[bool] = True
    can_manage_privacy_budget: Optional[bool] = True
    can_create_users: Optional[bool] = True
    can_manage_users: Optional[bool] = True
    can_edit_roles: Optional[bool] = True
    can_manage_infrastructure: Optional[bool] = True
    can_upload_data: Optional[bool] = True
    can_upload_legal_document: Optional[bool] = True
    can_edit_domain_settings: Optional[bool] = True
