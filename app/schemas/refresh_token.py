from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RefreshTokenBase(BaseModel):
    """Refresh token base model."""

    user_id: Optional[int] = None
    jti: Optional[str] = None
    token: Optional[str] = None


class RefreshTokenCreate(RefreshTokenBase):
    """Refresh token creating with required fields."""

    user_id: int
    jti: str
    token: str


class RefreshTokenUpdate(RefreshTokenBase):
    """Refresh token update operation fields."""

    jti: str
    token: str


class RefreshTokenInDBBase(RefreshTokenBase):
    """Refresh token database model with common fields."""

    id: Optional[int] = None

    class Config:
        orm_mode = True


class RefreshToken(RefreshTokenInDBBase):
    """Refresh token main model for using."""


class RefreshTokenInDB(RefreshTokenInDBBase):
    """Refresh token model database representation."""

    created_at: datetime
    updated_at: datetime
    revoked_at: Optional[datetime]
