from typing import List

import strawberry

from app.db.session import session
from app.graphql.types import users
from app.models import User


def get_users() -> List[users.User]:
    """Get all users."""
    return session.query(User).all()


@strawberry.type
class Query:
    """User query fields."""

    users = strawberry.field(resolver=get_users)
