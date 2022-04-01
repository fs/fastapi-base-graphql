import strawberry
from fastapi import HTTPException
from strawberry.types import Info

from app.core import settings, tokens
from app.graphql.types.authentication import TokenPairType, SignOutType
from app.crud import crud_refresh_token


def new_token_pair(info: Info) -> TokenPairType:
    if not info.context['authenticated']:
        raise HTTPException(status_code=403, detail='Not authenticated')

    refresh_token = info.context['request'].cookies.get(settings.JWT_SETTINGS['JWT_REFRESH_TOKEN_COOKIE_NAME'])
    if not refresh_token:
        raise HTTPException(status_code=401, detail='Refresh token was not provided')

    new_access_token, new_refresh_token = tokens.new_token_pair(refresh_token)
    return TokenPairType(access_token=new_access_token, refresh_token=new_refresh_token)


def user_sign_out(info: Info) -> SignOutType:
    access_token = info.context['access_token']
    if not access_token:
        raise HTTPException(status_code=403, detail='Not authenticated')

    jti = tokens.decode_access_token(access_token)['jti']
    crud_refresh_token.refresh_token.revoke(jti)
    return SignOutType(message='User sign out successfully')


@strawberry.type
class Query:
    """Authentication query fields."""
    sign_out = strawberry.field(resolver=user_sign_out)
    new_token_pair = strawberry.field(resolver=new_token_pair)
