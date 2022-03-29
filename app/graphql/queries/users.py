from app.graphql.types import users
import strawberry
from typing import List
from app.models.user import User
from app.db.session import session


def get_users() -> List[users.User]:
    """Get all users."""
    return session.query(User).all()


@strawberry.type
class Query:
    """User query fields."""

    users = strawberry.field(resolver=get_users)
