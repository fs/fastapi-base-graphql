from datetime import datetime
from typing import Literal

from pydantic import BaseModel, validator

from app.crud.crud_refresh_token import refresh_token


class AccessTokenPayload(BaseModel):
    """Access token payload model."""

    iat: datetime
    exp: datetime
    scope: Literal['access_token']
    user_id: int
    jti: str

    @validator('jti')
    def is_revoked(cls, value):
        """Check revocation in database."""
        db_obj = refresh_token.get_by_jti(jti=value)
        if db_obj.revoked_at:
            raise ValueError('This access token has been revoked')
        return value


class RefreshTokenPayload(BaseModel):
    """Refresh token payload model."""

    iat: datetime
    exp: datetime
    scope: Literal['refresh_token']
    user_id: int
    jti: str

    @validator('jti')
    def is_revoked(cls, value):
        """Check revocation in database."""
        db_obj = refresh_token.get_by_jti(jti=value)
        if db_obj.revoked_at:
            raise ValueError('This refresh token has been revoked')
        return value
