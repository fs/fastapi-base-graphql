from typing import Optional

import strawberry
from strawberry.types import Info
from fastapi import HTTPException
from datetime import datetime

from app.graphql.types.authentication import Authentication, Message, User
from app.core import tokens
from app.crud import crud_user, crud_refresh_token
from app.graphql.inputs.authentication import SignInInput, SignOutInput, SignUpInput
from app.schemas import UserCreate
from app.schemas.refresh_token import RefreshTokenCreate
from app.core import security
from app.core import settings


async def user_sign_in(input: SignInInput, info: Info) -> Optional[Authentication]:
    current_user = await crud_user.user.get_by_email(email=input.email)
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

    await crud_refresh_token.refresh_token.create(obj_in=obj_in)
    return Authentication(access_token=access_token, refresh_token=refresh_token, me=User.from_pydantic(current_user))


def new_token_pair(info: Info) -> Optional[Authentication]:
    if not info.context.authenticated:
        raise HTTPException(status_code=403, detail='Not authenticated')

    refresh_token = info.context.request.cookies.get(settings.JWT_SETTINGS['JWT_REFRESH_TOKEN_COOKIE_NAME'])
    if not refresh_token:
        raise HTTPException(status_code=401, detail='Refresh token was not provided')

    new_access_token, new_refresh_token = tokens.new_token_pair(refresh_token)
    return Authentication(access_token=new_access_token, refresh_token=new_refresh_token.token,
                          me=User.from_pydantic(new_refresh_token.user))


async def user_sign_out(input: SignOutInput, info: Info) -> Optional[Message]:
    if not input.everywhere:
        access_token = info.context.access_token
        if not access_token:
            raise HTTPException(status_code=403, detail='Not authenticated')

        jti = tokens.decode_access_token(access_token).jti
        print(f'JTI = {jti}')
        await crud_refresh_token.refresh_token.revoke(jti=jti)
        return Message(message='User sign out successfully')
    else:
        access_token = info.context.access_token
        if not access_token:
            raise HTTPException(status_code=403, detail='Not authenticated')

        await crud_refresh_token.refresh_token.revoke_all_for_user(user_id=info.context.current_user.id)
        return Message(message='User sign out successfully')


async def user_sign_up(input: SignUpInput, info: Info) -> Optional[Authentication]:
    db_user = await crud_user.user.get_by_email(email=input.email)
    if db_user:
        raise ValueError('User with this email was already created')
    else:
        db_obj = await crud_user.user.create(obj_in=UserCreate.parse_obj({
            'email': input.email,
            'password': input.password,
            'full_name': f'{input.first_name} {input.last_name}'
        }))

        jti = security.generate_hash_for_jti(db_obj.id, datetime.now())
        access_token = tokens.encode_access_token(db_obj.id, jti)
        refresh_token = tokens.encode_refresh_token(db_obj.id, jti)
        await crud_refresh_token.refresh_token.create(obj_in=RefreshTokenCreate.parse_obj({
            'user_id': db_obj.id,
            'jti': jti,
            'token': refresh_token
        }))
        return Authentication(access_token=access_token, refresh_token=refresh_token,
                              me=User.from_pydantic(db_obj))


@strawberry.type
class Mutation:
    """Authentication mutation fields."""
    signup = strawberry.field(resolver=user_sign_up, description='Signup mutation with JWT tokens.')
    signin = strawberry.field(resolver=user_sign_in, description='JWT signin mutation for users.')
    signout = strawberry.field(resolver=user_sign_out, description='Refresh tokens revoking mutation.')
    update_token = strawberry.field(resolver=new_token_pair, description='JWT tokens updating mutation.')
