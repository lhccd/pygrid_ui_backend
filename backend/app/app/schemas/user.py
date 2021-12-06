from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None
    daa_pdf: Optional[bytes]
    budget: Optional[float]


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    full_name: Optional[str]
    password: str
    website: Optional[str] = None
    institution: Optional[str] = None
    budget: Optional[float]


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


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
