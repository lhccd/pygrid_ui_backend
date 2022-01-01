from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.roles import Role


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    full_name: str
    password: str
    website: Optional[str] = None
    institution: Optional[str] = None
    daa_pdf: Optional[bytes] = None
    budget: Optional[float] = None
    status: Optional[str]


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


class UserProfile(UserInDBBase):
    email: EmailStr
    full_name: str
    institution: Optional[str] = None
    website: Optional[str] = None


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str

# Schemas for users table
class ActiveUser(UserBase):
    id: Optional[int] = None
    budget: Optional[float] = None
    created_at: Optional[datetime] = None
    added_by: Optional[str] = None

    class Config:
        orm_mode = True

class PendingUser(UserBase):
    created_at: Optional[datetime] = None
    daa_pdf: Optional[bytes] = None
    institution: Optional[str] = None

class DeniedUser(PendingUser):
    added_by: Optional[str] = None

    class Config:
            orm_mode = True
