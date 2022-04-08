from typing import Optional

import strawberry

from app.schemas import SignInUser, UserCreate
from app.graphql.core.type import strawberry_pydantic_input, strawberry_input


@strawberry_pydantic_input(model=UserCreate, fields=('email', 'full_name', 'password'))
class SignUpInput:
    """Fields for user sign up mutation."""


@strawberry_pydantic_input(model=SignInUser, all_fields=True)
class SignInInput:
    """Fields for user sign in mutation."""


@strawberry_input
class SignOutInput:
    """Signout mutation input with everywhere param for logout from all sessions."""

    everywhere: Optional[bool] = strawberry.field(description='Logout from all devices.')
