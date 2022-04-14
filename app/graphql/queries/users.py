from typing import Optional

import strawberry
from strawberry.types import Info

from app.core.permissions import IsAuthenticated
from app.graphql.types.users import User
from app.graphql.core.relay.fields import connection_field
from app.models import User as UserModel
from sqlalchemy.orm import Query


def get_current_user(info: Info) -> Optional[User]:
    return User.from_instance(info.context.current_user)


def get_users(*args, **kwargs) -> User:
    return Query(UserModel)


@strawberry.type
class Query:
    """User query fields."""

    me = strawberry.field(
        resolver=get_current_user,
        description='Current User model query',
        permission_classes=[IsAuthenticated],
    )

    users = connection_field(resolver=get_users)
