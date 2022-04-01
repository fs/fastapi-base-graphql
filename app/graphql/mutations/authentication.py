from typing import Any, NoReturn

import strawberry
from strawberry.types import Info
from fastapi import HTTPException
from datetime import datetime

from app.graphql.types.authentication import TokenPairType, SignOutType
from app.core import tokens
from app.crud import crud_user, crud_refresh_token
from app.graphql.inputs.authentication import SignInUserInput
from app.schemas.refresh_token import RefreshTokenCreate
from app.core import security
from app.core import settings


def user_sign_in(input: SignInUserInput, info: Info) -> TokenPairType:
    current_user = crud_user.user.get_by_email(input.email)
    if not current_user or not security.verify_password(input.password, current_user.password):
        raise HTTPException(status_code=403, detail='Wrong credentials')

    previous_token = crud_refresh_token.refresh_token.get_by_user_id(current_user.id)
    if previous_token and not previous_token.revoked_at:
        crud_refresh_token.refresh_token.revoke(jti=previous_token.jti)

    jti = security.generate_hash_for_jti(current_user.id, datetime.now())
    access_token = tokens.encode_access_token(current_user.id, jti)
    refresh_token = tokens.encode_refresh_token(current_user.id, jti)

    crud_refresh_token.refresh_token.create(obj_in=RefreshTokenCreate(current_user.id, jti, refresh_token))
    return TokenPairType(access_token=access_token, refresh_token=refresh_token)


@strawberry.type
class Mutation:
    """Authentication mutation fields."""
    sign_in = strawberry.field(resolver=user_sign_in)
