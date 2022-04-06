from datetime import datetime

import jwt
from fastapi import HTTPException

from app.core.config import settings
from app.core.security import generate_hash_for_jti
from app.crud.crud_refresh_token import refresh_token as crud_rt
from app.models.refresh_token import RefreshToken
from app.schemas import (
    AccessTokenPayload,
    RefreshTokenCreate,
    RefreshTokenPayload,
)


def encode_access_token(user_id: int, jti: str) -> str:
    """Make jwt access token."""
    payload = {
        'exp': datetime.utcnow() + settings.ACCESS_TOKEN_EXPIRATION_DELTA,
        'iat': datetime.utcnow(),
        'scope': 'access_token',
        'user_id': str(user_id),
        'jti': jti,
    }
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> AccessTokenPayload:
    """Get access token payload by token string."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')

    try:
        return AccessTokenPayload.parse_obj(payload)
    except ValueError as validation_error:
        validation_message = str(validation_error.args[0][0].exc)
        raise HTTPException(status_code=401, detail=validation_message)


def decode_refresh_token(refresh_token: str) -> RefreshTokenPayload:
    """Get refresh token payload by token string."""
    try:
        jwt_payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Refresh token expired')

    try:
        return RefreshTokenPayload.parse_obj(jwt_payload)
    except ValueError as validation_error:
        validation_error_message = str(validation_error.args[0][0].exc)
        raise HTTPException(status_code=401, detail=validation_error_message)


def encode_refresh_token(user_id: int, jti: str) -> str:
    """Make JWT refresh token."""
    payload = {
        'exp': datetime.utcnow() + settings.REFRESH_TOKEN_EXPIRATION_DELTA,
        'iat': datetime.utcnow(),
        'scope': 'refresh_token',
        'user_id': str(user_id),
        'jti': jti,
    }
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def new_token_pair(refresh_token: str) -> tuple[str, RefreshToken]:
    """Update tokens pair by refresh token."""
    payload = decode_refresh_token(refresh_token)
    user_id = payload.user_id
    db_obj = crud_rt.get_by_jti(jti=payload.jti)

    if db_obj.revoked_at:
        raise HTTPException(status_code=401, detail='This token has been revoked')

    crud_rt.revoke(jti=payload.jti)
    jti = generate_hash_for_jti(user_id, datetime.now())
    new_obj = crud_rt.create(obj_in=RefreshTokenCreate.parse_obj({
        'user_id': user_id,
        'jti': jti,
        'token': encode_refresh_token(user_id, jti),
    }))
    return encode_access_token(user_id, jti), new_obj
