# flake8: noqa
from typing import Optional

from pydantic import BaseModel, EmailStr, validator, Field


class UserBase(BaseModel):
    """Base user pydantic model with shared properties."""

    email: EmailStr = Field(description='User email')
    is_active: Optional[bool] = Field(True, description='User can authenticate')
    full_name: Optional[str] = Field(None, description='Full name for user, e.g. Ivanov Ivan')
    password: str = Field(description='Password for login')


class UserCreate(UserBase):
    """Properties to receive via creation mutation."""

    first_name: str = Field(description='First name')
    last_name: str = Field(description='Last name')


class UserUpdate(UserBase):
    """ Properties to receive via mutation on update"""

    password: Optional[str] = Field(description='New password for user.')


class SignInUser(BaseModel):
    """Sign in user models."""

    email: EmailStr = Field(description='User email')
    password: str = Field(description='Password for login')


class UserInDBBase(UserBase):
    """Database user schema."""

    id: Optional[int] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    """Additional properties to return via API."""

    id: int = Field(description='The ID of user')


class UserInDB(UserInDBBase):
    """Additional properties stored in DB."""

    hashed_password: str
