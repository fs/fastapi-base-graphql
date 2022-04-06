from typing import Optional
from contextlib import suppress

from fastapi import HTTPException
from starlette.requests import Request

from app.core import tokens, settings
from app.crud import crud_user

from strawberry.extensions import Extension


def get_access_token_from_request(request: Request) -> Optional[str]:
    authorization_header = request.headers.get(settings.JWT_SETTINGS['JWT_AUTH_HEADER_NAME'])
    if not authorization_header:
        return None

    auth = authorization_header.split()
    if len(auth) != 2 or auth[0] != settings.JWT_SETTINGS['JWT_AUTH_HEADER_PREFIX']:
        return None

    return auth[1]


class CurrentUserExtension(Extension):
    def on_request_start(self):
        context = self.execution_context.context
        request = context['request']
        token = get_access_token_from_request(request)
        user_obj = None
        with suppress(HTTPException):
            if token:
                user_id = tokens.decode_access_token(token).user_id
                user_obj = crud_user.user.get(user_id)
        context['current_user'] = user_obj
        context['access_token'] = token
