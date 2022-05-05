from contextlib import suppress
from typing import Optional

from fastapi import HTTPException
from starlette.requests import Request
from strawberry.extensions import Extension

from app.core import settings, tokens
from app.crud import crud_user


def get_access_token_from_request(request: Request) -> Optional[str]:
    """Retrieve access from request headers."""
    authorization_header = request.headers.get(settings.JWT_AUTH_HEADER_NAME.lower())
    if not authorization_header:
        return None
    prefix = settings.JWT_AUTH_HEADER_PREFIX
    auth = authorization_header.split()
    if len(auth) != 2 or auth[0] != prefix:
        return None

    return auth[1]


class CurrentUserExtension(Extension):
    """Link current authenticated user to request."""

    async def on_request_start(self):
        """Call before query and mutation, setting user instance and access token."""
        request = self.execution_context.context['request']
        token = get_access_token_from_request(request)
        user_obj = None
        with suppress(HTTPException):
            if token:
                user_id = tokens.decode_access_token(token).user_id
                user_obj = await crud_user.user.get(user_id)

        setattr(request, 'current_user', user_obj)
        setattr(request, 'access_token', token if user_obj else None)
