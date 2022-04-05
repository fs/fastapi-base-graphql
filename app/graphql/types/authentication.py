from typing import Optional

import strawberry
from app.graphql.types.users import User


@strawberry.type(description='Output for authenticated mutation.')
class Authentication:
    access_token: Optional[str]
    refresh_token: Optional[str]
    me: Optional[User]


@strawberry.type(description='Output message after signout.')
class Message:
    message: Optional[str]
