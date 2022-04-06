from typing import Optional

import strawberry
from strawberry.types import Info

from app.core.permissions import IsAuthenticated
from app.graphql.types.users import User


def get_current_user(info: Info) -> Optional[User]:
    """Get pydantic user from context."""
    return User.from_pydantic(info.context.current_user)


@strawberry.type
class Query:
    """User query fields."""

    me = strawberry.field(
        resolver=get_current_user,
        description='Current User model query',
        permission_classes=[IsAuthenticated],
    )
