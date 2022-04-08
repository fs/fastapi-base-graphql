# flake8: noqa
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    """Base user pydantic model with shared properties."""

    email: EmailStr
    is_active: Optional[bool] = True
    full_name: Optional[str] = None
    password: str


class UserCreate(UserBase):
    """Properties to receive via creation mutation."""


# Properties to receive via API on update
class UserUpdate(UserBase):
    """Model for user fields updating."""

    password: Optional[str] = None


class SignInUser(BaseModel):
    """Sign in user models."""

    password: str


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
