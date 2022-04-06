from datetime import datetime
from typing import Optional

import strawberry
from fastapi import HTTPException
from strawberry.types import Info

from app.core import security, settings, tokens
from app.crud import crud_refresh_token, crud_user
from app.graphql.inputs.authentication import (
    SignInInput,
    SignOutInput,
    SignUpInput,
)
from app.graphql.types.authentication import Authentication, Message, User
from app.schemas import UserCreate
from app.schemas.refresh_token import RefreshTokenCreate


def user_sign_in(input: SignInInput, info: Info) -> Optional[Authentication]:
    """Check email, password and give tokens pair."""
    current_user = crud_user.user.get_by_email(email=input.email)
    if not current_user or not security.verify_password(input.password, current_user.password):
        raise HTTPException(status_code=403, detail='Wrong credentials')

    jti = security.generate_hash_for_jti(current_user.id, datetime.now())
    access_token = tokens.encode_access_token(current_user.id, jti)
    refresh_token = tokens.encode_refresh_token(current_user.id, jti)

    obj_in = RefreshTokenCreate.parse_obj({
        'user_id': current_user.id,
        'jti': jti,
        'token': refresh_token,
    })

    crud_refresh_token.refresh_token.create(obj_in=obj_in)
    return Authentication(access_token=access_token, refresh_token=refresh_token, me=User.from_pydantic(current_user))


def new_token_pair(info: Info) -> Optional[Authentication]:
    """Update tokens pair by given refresh token."""
    if not info.context.authenticated:
        raise HTTPException(status_code=403, detail='Not authenticated')

    refresh_token = info.context.request.cookies.get(settings.JWT_REFRESH_TOKEN_COOKIE_NAME)
    if not refresh_token:
        raise HTTPException(status_code=401, detail='Refresh token was not provided')

    new_access_token, new_refresh_token = tokens.new_token_pair(refresh_token)
    return Authentication(
        access_token=new_access_token,
        refresh_token=new_refresh_token.token,
        me=User.from_pydantic(new_refresh_token.user),
    )


def user_sign_out(input: SignOutInput, info: Info) -> Optional[Message]:
    """Destroy session or all sessions for user."""
    access_token = info.context.access_token
    if not access_token:
        raise HTTPException(status_code=403, detail='Not authenticated')

    if input.everywhere:
        crud_refresh_token.refresh_token.revoke_all_for_user(user_id=info.context.current_user.id)
    else:
        jti = tokens.decode_access_token(access_token).jti
        crud_refresh_token.refresh_token.revoke(jti=jti)

    return Message(message='User sign out successfully')


def user_sign_up(input: SignUpInput, info: Info) -> Optional[Authentication]:
    """Sign up with generating tokens."""
    db_user = crud_user.user.get_by_email(email=input.email)
    if db_user:
        raise ValueError('User with this email was already created')

    db_obj = crud_user.user.create(obj_in=UserCreate.parse_obj({
        'email': input.email,
        'password': input.password,
        'full_name': f'{input.first_name} {input.last_name}',
    }))

    jti = security.generate_hash_for_jti(db_obj.id, datetime.now())
    access_token = tokens.encode_access_token(db_obj.id, jti)
    refresh_token = tokens.encode_refresh_token(db_obj.id, jti)
    crud_refresh_token.refresh_token.create(obj_in=RefreshTokenCreate.parse_obj({
        'user_id': db_obj.id,
        'jti': jti,
        'token': refresh_token,
    }))
    return Authentication(
        access_token=access_token,
        refresh_token=refresh_token,
        me=User.from_pydantic(db_obj),
    )


@strawberry.type
class Mutation:
    """Authentication mutation fields."""

    signup = strawberry.field(resolver=user_sign_up, description='Signup mutation with JWT tokens.')
    signin = strawberry.field(resolver=user_sign_in, description='JWT signin mutation for users.')
    signout = strawberry.field(resolver=user_sign_out, description='Refresh tokens revoking mutation.')
    update_token = strawberry.field(resolver=new_token_pair, description='JWT tokens updating mutation.')
