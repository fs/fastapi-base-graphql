from typing import Any, Union

from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry.permission import BasePermission
from strawberry.types import Info

from app.core import tokens
from app.crud import crud_refresh_token


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request: Union[Request, WebSocket] = info.context['request']

        token = request.access_token
        if not token:
            return False

        refresh_token = crud_refresh_token.refresh_token.get_by_jti(jti=tokens.decode_access_token(token).jti)
        if refresh_token and not refresh_token.revoked_at:
            return True

        return False


