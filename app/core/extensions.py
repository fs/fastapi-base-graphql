from typing import Optional
from fastapi import HTTPException
from starlette.requests import Request

from app.models import User
from app.core import tokens
from app.core.config import settings
from app.crud import crud_user, crud_refresh_token


def access_token(request: Request) -> Optional[str]:
    authorization_header = request.headers.get(settings.JWT_SETTINGS['JWT_AUTH_HEADER_NAME'].lower())
    if not authorization_header:
        return None

    auth = authorization_header.split()
    if len(auth) != 2 or auth[0] != settings.JWT_SETTINGS['JWT_AUTH_HEADER_PREFIX']:
        return None

    return auth[1]


async def current_user(request: Request) -> Optional[User]:
    token = access_token(request)
    if not token:
        return None

    user_id = tokens.decode_access_token(token).user_id
    user_obj = await crud_user.user.get(user_id)
    return user_obj


async def authenticated(request: Request) -> bool:
    token = access_token(request)
    if not token:
        return False

    refresh_token = await crud_refresh_token.refresh_token.get_by_jti(jti=tokens.decode_access_token(token).jti)
    if not refresh_token:
        return False
    elif refresh_token.revoked_at:
        return False

    return True
