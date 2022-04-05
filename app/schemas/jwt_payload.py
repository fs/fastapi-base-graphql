from pydantic import BaseModel, validator
from datetime import datetime


class AccessTokenPayload(BaseModel):
    iat: datetime
    exp: datetime
    scope: str
    user_id: int
    jti: str

    @validator('scope')
    def scope_validate(cls, value):
        if value != 'access_token':
            raise ValueError('Invalid scope for token')
        return value


class RefreshTokenPayload(BaseModel):
    iat: datetime
    exp: datetime
    scope: str
    user_id: int
    jti: str

    @validator('scope')
    def scope_validate(cls, value):
        if value != 'refresh_token':
            raise ValueError('Invalid scope for token')
        return value
