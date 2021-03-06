from typing import Optional

from app.graphql.core.type import strawberry_type
from app.graphql.types.users import User


@strawberry_type
class Authentication:
    """Output for authenticated mutation."""

    access_token: Optional[str]
    refresh_token: Optional[str]
    me: Optional[User]


@strawberry_type
class Message:
    """Output message after signout."""

    message: Optional[str]
