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
        if not refresh_token:
            return False
        elif refresh_token.revoked_at:
            return False

        return True


class IsAdmin(BasePermission):
    message = "User doesn't have admin permissions"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        request: Union[Request, WebSocket] = info.context['request']

        user_obj = request.current_user
        if not user_obj:
            return False

        if user_obj.is_superuser:
            return True

        return False


