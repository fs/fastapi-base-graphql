from datetime import datetime

from pydantic import BaseModel, validator

from app.core.config import settings
from app.crud.crud_refresh_token import refresh_token


class TokenPayloadBase(BaseModel):
    """Token shared properties."""

    iat: datetime = datetime.now()
    exp: datetime = datetime.now() + settings.REFRESH_TOKEN_EXPIRATION_DELTA
    user_id: int
    jti: str


class AccessTokenPayload(TokenPayloadBase):
    """Access token payload model."""

    scope: str = 'access_token'


class RefreshTokenPayload(TokenPayloadBase):
    """Refresh token payload model."""

    scope: str = 'refresh_token'
