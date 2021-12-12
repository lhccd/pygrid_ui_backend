from typing import Optional

from pydantic import BaseModel


class RoleDataScientist(BaseModel):
    name = "Data Scientist"
    can_make_data_requests = True

class RoleAdmin(RoleDataScientist):
    name = "Admin"
    can_triage_data_requests = True
    can_manage_privacy_budget = True
    can_create_users = True
    can_manage_users = True
    can_edit_roles = True
    can_upload_data = True
    can_upload_legal_document = True
    can_edit_domain_settings = True

class RoleComplianceOfficer(RoleDataScientist):
    name = "Compliance Officer"
    can_make_data_requests = False
    can_triage_data_requests = True
    can_manage_privacy_budget = True
    can_manage_users = True

class RoleOwner(RoleAdmin):
    name = "Owner"
    can_manage_infrastructure = True
