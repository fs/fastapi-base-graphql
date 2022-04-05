from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    """Base user pydantic model."""

    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    """Model for user creation."""

    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    """Model for user fields updating."""

    password: Optional[str] = None


class SignInUser(BaseModel):
    email: EmailStr
    password: str


class UserToken(BaseModel):
    access_token: str


class UserInDBBase(UserBase):
    """Database user schema."""

    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    """Additional properties to return via API."""
    
    id: int
    email: EmailStr


class UserInDB(UserInDBBase):
    """Additional properties stored in DB."""

    hashed_password: str
