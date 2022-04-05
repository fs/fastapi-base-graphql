from typing import Optional
from contextlib import suppress

from fastapi import HTTPException
from starlette.requests import Request

from app.core import tokens, settings
from app.crud import crud_user

from strawberry.extensions import Extension


def get_access_token_from_request(request: Request) -> Optional[str]:
    authorization_header = request.headers.get(settings.JWT_SETTINGS['JWT_AUTH_HEADER_NAME'].lower())
    if not authorization_header:
        return None

    auth = authorization_header.split()
    if len(auth) != 2 or auth[0] != settings.JWT_SETTINGS['JWT_AUTH_HEADER_PREFIX']:
        return None

    return auth[1]


class CurrentUserExtension(Extension):
    def on_request_start(self):
        request = self.execution_context.context['request']
        token = get_access_token_from_request(request)
        with suppress(HTTPException):
            if token:
                user_id = tokens.decode_access_token(token).user_id
                user_obj = crud_user.user.get(user_id)
                setattr(request, 'current_user', user_obj)
                setattr(request, 'access_token', token)
                return
        setattr(request, 'current_user', None)
        setattr(request, 'access_token', None)

