import uuid

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


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
    allocated_budget: Optional[float] = None
    budget: Optional[float] = None
    status: str = ""
    created_at: Optional[datetime]


# Properties to receive via API on update
class UserUpdate(UserBase):
    status: Optional[str] = None
    added_by: Optional[str] = None
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    status: str
    pass


class UserProfile(UserInDBBase):
    email: EmailStr
    full_name: str
    institution: Optional[str] = None
    website: Optional[str] = None
    status: Optional[str] = None


class UserBudget(UserInDBBase):
    allocated_budget: Optional[float] = None
    budget: Optional[float] = None


class UserDetail(UserProfile):
    role: Optional[str]
    budget: Optional[float]
    allocated_budget: Optional[float]
    created_at: Optional[datetime]
    added_by: Optional[str]
    daa_pdf: Optional[bytes]


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


# Schemas for users table
class ActiveUser(UserBase):
    id: Optional[uuid.UUID]
    budget: Optional[float] = None
    allocated_budget: Optional[float] = None
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

class UserUpdateWithPassword(UserBase):
    full_name: Optional[str]
    website: Optional[str]
    email: Optional[EmailStr]
    institution: Optional[str]
    password: Optional[str] = None
