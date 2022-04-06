from typing import Optional

import strawberry
from strawberry.types import Info

from app.graphql.types.users import User
from app.core.permissions import IsAuthenticated


def get_current_user(info: Info) -> Optional[User]:
    return User.from_pydantic(info.context['current_user'])


@strawberry.type
class Query:
    """User query fields."""

    me = strawberry.field(
        resolver=get_current_user,
        description='Current User model query',
        permission_classes=[IsAuthenticated],
    )
