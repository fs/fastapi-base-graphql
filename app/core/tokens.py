from fastapi import HTTPException

from app.core.config import settings
from app.core.security import generate_hash_for_jti
from app.crud.crud_refresh_token import refresh_token as crud_rt

from datetime import datetime
import jwt


def encode_access_token(user_id: int, jti: str) -> str:
    payload = {
        'exp': datetime.utcnow() + settings.JWT_SETTINGS['ACCESS_TOKEN_EXPIRATION_DELTA'],
        'iat': datetime.utcnow(),
        'scope': 'access_token',
        'user_id': str(user_id),
        'jti': jti
    }
    return jwt.encode(
        payload,
        settings.JWT_SETTINGS['JWT_SECRET_KEY'],
        algorithm=settings.JWT_SETTINGS['JWT_ALGORITHM']
    )


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_SETTINGS['JWT_ALGORITHM']])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')

    if payload['scope'] == 'access_token':
        return payload
    else:
        raise HTTPException(status_code=401, detail='Scope for the token is invalid')


def encode_refresh_token(user_id: int, jti: str) -> str:
    payload = {
        'exp': datetime.utcnow() + settings.JWT_SETTINGS['REFRESH_TOKEN_EXPIRATION_DELTA'],
        'iat': datetime.utcnow(),
        'scope': 'refresh_token',
        'user_id': str(user_id),
        'jti': jti
    }
    return jwt.encode(
        payload,
        settings.JWT_SETTINGS['JWT_SECRET_KEY'],
        algorithm=settings.JWT_SETTINGS['JWT_ALGORITHM']
    )


def new_token_pair(refresh_token: str) -> tuple[str, str]:
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.JWT_SETTINGS['JWT_ALGORITHM']])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Refresh token expired')

    if payload['scope'] == 'refresh_token':
        user_id = payload['user_id']
        db_obj = crud_rt.get_by_jti(payload['jti'])
        if not db_obj.revoked_at:
            crud_rt.revoke(payload['jti'])
            jti = generate_hash_for_jti(user_id, datetime.now())
            new_access_token = encode_access_token(user_id, jti)
            new_refresh_token = encode_refresh_token(user_id, jti)
            return new_access_token, new_refresh_token
        else:
            raise HTTPException(status_code=401, detail='This token has been revoked')
    else:
        raise HTTPException(status_code=401, detail='Invalid scope for token')
