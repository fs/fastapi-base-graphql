from typing import Any, Union

from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry.permission import BasePermission
from strawberry.types import Info

from app.core import tokens
from app.crud import crud_refresh_token


class IsAuthenticated(BasePermission):
    """Permission for check request is authenticated."""

    message = 'User is not authenticated'

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        """Get access token from request and check revocation."""
        request: Union[Request, WebSocket] = info.context['request']

        token = request.access_token
        if not token:
            return False

        refresh_token = crud_refresh_token.refresh_token.get_by_jti(jti=tokens.decode_access_token(token).jti)
        return refresh_token is not None and not refresh_token.revoked_at
