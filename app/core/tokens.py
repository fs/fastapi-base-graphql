from fastapi import HTTPException

from app.core.config import settings
from app.core.security import generate_hash_for_jti
from app.crud.crud_refresh_token import refresh_token as crud_rt

from datetime import datetime
import jwt

from app.models.refresh_token import RefreshToken
from app.schemas import RefreshTokenCreate, AccessTokenPayload, RefreshTokenPayload


def encode_access_token(user_id: int, jti: str) -> str:
    payload = AccessTokenPayload.parse_obj({
        'user_id': str(user_id),
        'jti': jti
    })
    return jwt.encode(
        payload.dict(),
        settings.JWT_SETTINGS['JWT_SECRET_KEY'],
        settings.JWT_SETTINGS['JWT_ALGORITHM']
    )


def decode_access_token(token: str) -> AccessTokenPayload:
    try:
        payload = AccessTokenPayload.parse_obj(jwt.decode(token, settings.JWT_SETTINGS['JWT_SECRET_KEY'], algorithms=[settings.JWT_SETTINGS['JWT_ALGORITHM']]))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e.args[0][0].exc))

    return payload


def encode_refresh_token(user_id: int, jti: str) -> str:
    payload = RefreshTokenPayload.parse_obj({
        'user_id': str(user_id),
        'jti': jti
    })
    return jwt.encode(
        payload.dict(),
        settings.JWT_SETTINGS['JWT_SECRET_KEY'],
        algorithm=settings.JWT_SETTINGS['JWT_ALGORITHM']
    )


def new_token_pair(refresh_token: str) -> tuple[str, RefreshToken]:
    try:
        payload = RefreshTokenPayload.parse_obj(jwt.decode(refresh_token, settings.JWT_SETTINGS['JWT_SECRET_KEY'], algorithms=[settings.JWT_SETTINGS['JWT_ALGORITHM']]))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Refresh token expired')
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e.args[0][0].exc))

    user_id = payload.user_id
    db_obj = crud_rt.get_by_jti(jti=payload.jti)
    if not db_obj.revoked_at:
        crud_rt.revoke(jti=payload.jti)
        jti = generate_hash_for_jti(user_id, datetime.now())
        new_access_token = encode_access_token(user_id, jti)
        new_refresh_token = encode_refresh_token(user_id, jti)
        new_obj = crud_rt.create(obj_in=RefreshTokenCreate.parse_obj({
            'user_id': user_id,
            'jti': jti,
            'token': new_refresh_token
        }))
        return new_access_token, new_obj
    else:
        raise HTTPException(status_code=401, detail='This token has been revoked')