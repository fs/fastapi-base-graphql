import strawberry
from strawberry.types import Info
from fastapi import HTTPException
from datetime import datetime

from app.graphql.types.authentication import TokenPairType, SignOutType, UserType
from app.core import tokens
from app.crud import crud_user, crud_refresh_token
from app.graphql.inputs.authentication import SignInInput, SignOutInput
from app.schemas.refresh_token import RefreshTokenCreate
from app.core import security
from app.core import settings


def user_sign_in(input: SignInInput, info: Info) -> TokenPairType:
    current_user = crud_user.user.get_by_email(email=input.email)
    if not current_user or not security.verify_password(input.password, current_user.password):
        raise HTTPException(status_code=403, detail='Wrong credentials')

    jti = security.generate_hash_for_jti(current_user.id, datetime.now())
    access_token = tokens.encode_access_token(current_user.id, jti)
    refresh_token = tokens.encode_refresh_token(current_user.id, jti)

    obj_in = RefreshTokenCreate.parse_obj({
        'user_id': current_user.id,
        'jti': jti,
        'token': refresh_token
    })

    crud_refresh_token.refresh_token.create(obj_in=obj_in)
    return TokenPairType(access_token=access_token, refresh_token=refresh_token, me=UserType.from_pydantic(current_user))


def new_token_pair(info: Info) -> TokenPairType:
    if not info.context.authenticated:
        raise HTTPException(status_code=403, detail='Not authenticated')

    refresh_token = info.context.request.cookies.get(settings.JWT_SETTINGS['JWT_REFRESH_TOKEN_COOKIE_NAME'])
    if not refresh_token:
        raise HTTPException(status_code=401, detail='Refresh token was not provided')

    new_access_token, new_refresh_token = tokens.new_token_pair(refresh_token)
    return TokenPairType(access_token=new_access_token, refresh_token=new_refresh_token.token, me=UserType.from_pydantic(new_refresh_token.user))


def user_sign_out(input: SignOutInput, info: Info) -> SignOutType:
    if not input.everywhere:
        access_token = info.context.access_token
        if not access_token:
            raise HTTPException(status_code=403, detail='Not authenticated')

        jti = tokens.decode_access_token(access_token)['jti']
        crud_refresh_token.refresh_token.revoke(jti)
        return SignOutType(message='User sign out successfully')
    else:
        access_token = info.context.access_token
        if not access_token:
            raise HTTPException(status_code=403, detail='Not authenticated')

        crud_refresh_token.refresh_token.revoke_all_for_user(user_id=info.context.current_user.id)
        return SignOutType(message='User sign out successfully')


@strawberry.type
class Mutation:
    """Authentication mutation fields."""
    sign_in = strawberry.field(resolver=user_sign_in)
    sign_out = strawberry.field(resolver=user_sign_out)
    new_token_pair = strawberry.field(resolver=new_token_pair)
