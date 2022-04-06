from datetime import datetime

from pydantic import BaseModel, validator

from app.core.config import settings
from app.crud.crud_refresh_token import refresh_token


class TokenPayloadBase(BaseModel):
    """Token shared properties."""

    iat: datetime = datetime.now()
    exp: datetime = datetime.now() + settings.JWT_SETTINGS['REFRESH_TOKEN_EXPIRATION_DELTA']
    user_id: int
    jti: str

    @validator('jti')
    def is_revoked(cls, value):
        """Check revocation in database."""
        db_obj = refresh_token.get_by_jti(jti=value)
        if not db_obj:
            return value

        if db_obj.revoked_at:
            raise ValueError('This token has been revoked')

        return value


class AccessTokenPayload(TokenPayloadBase):
    """Access token payload model."""

    scope: str = 'access_token'


class RefreshTokenPayload(TokenPayloadBase):
    """Refresh token payload model."""

    scope: str = 'refresh_token'
