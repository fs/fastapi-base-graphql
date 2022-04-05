from typing import Optional

import strawberry

from app.schemas import SignInUser


@strawberry.input(description='Signup mutation input.')
class SignUpInput:
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]


@strawberry.experimental.pydantic.input(model=SignInUser, all_fields=True, description='Sign in mutation input.')
class SignInInput:
    pass


@strawberry.input(description='Sign out mutation input, which revokes all user refresh tokens or current.')
class SignOutInput:
    everywhere: Optional[bool]
