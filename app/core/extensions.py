from typing import Optional

from starlette.requests import Request

from app.core import tokens
from app.core.config import settings
from app.crud import crud_refresh_token, crud_user
from app.models import User


def access_token(request: Request) -> Optional[str]:
    """Get access token from request headers."""
    authorization_header = request.headers.get(settings.JWT_AUTH_HEADER_NAME.lower())
    if not authorization_header:
        return None
    prefix = settings.JWT_AUTH_HEADER_PREFIX
    auth = authorization_header.split()
    if len(auth) != 2 or auth[0] != prefix:
        return None

    return auth[1]


def current_user(request: Request) -> Optional[User]:
    """Find current user."""
    token = access_token(request)
    if not token:
        return None

    user_id = tokens.decode_access_token(token).user_id
    return crud_user.user.get(user_id)


def authenticated(request: Request) -> bool:
    """Check token availability."""
    token = access_token(request)
    if not token:
        return False

    refresh_token = crud_refresh_token.refresh_token.get_by_jti(jti=tokens.decode_access_token(token).jti)
    return refresh_token is not None and not refresh_token.revoked_at
