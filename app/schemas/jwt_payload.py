from pydantic import BaseModel, validator
from datetime import datetime
from app.crud.crud_refresh_token import refresh_token
from app.core.config import settings


class TokenPayloadBase(BaseModel):
    iat: datetime = datetime.now()
    exp: datetime = datetime.now() + settings.JWT_SETTINGS['REFRESH_TOKEN_EXPIRATION_DELTA']
    user_id: int
    jti: str

    @validator('jti')
    def is_revoked(cls, value):
        db_obj = refresh_token.get_by_jti(jti=value)
        if not db_obj:
            return value

        if db_obj.revoked_at:
            raise ValueError('This token has been revoked')

        return value


class AccessTokenPayload(TokenPayloadBase):
    scope: str = 'access_token'


class RefreshTokenPayload(TokenPayloadBase):
    scope: str = 'refresh_token'
