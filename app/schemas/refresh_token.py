from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RefreshTokenBase(BaseModel):
    user_id: Optional[int] = None
    jti: Optional[str] = None
    token: Optional[str] = None


class RefreshTokenCreate(RefreshTokenBase):
    user_id: int
    jti: str
    token: str


class RefreshTokenUpdate(RefreshTokenBase):
    jti: str
    token: str


class RefreshTokenInDBBase(RefreshTokenBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class RefreshToken(RefreshTokenInDBBase):
    pass


class RefreshTokenInDB(RefreshTokenInDBBase):
    created_at: datetime
    updated_at: datetime
    revoked_at: Optional[datetime]
