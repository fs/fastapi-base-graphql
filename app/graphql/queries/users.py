from typing import List

import strawberry

from app.db.session import session
from app.graphql.types.users import UserType
from app.models import User


def get_users() -> List[UserType]:
    """Get all users."""
    users = session.query(User).all()
    return [UserType.from_pydantic(user) for user in users]


@strawberry.type
class Query:
    """User query fields."""

    users = strawberry.field(resolver=get_users)
