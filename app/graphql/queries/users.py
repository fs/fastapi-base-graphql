import strawberry
from typing import Optional
from app.db.session import session
from app.graphql.types.users import UserType
from app.models import User
from app.graphql.core.relay.node import connection


@connection
def get_users() -> list[UserType]:
    """Get all users."""
    users = session.query(User).all()
    return [UserType.from_instance(user) for user in users]


@strawberry.type
class Query:
    """User query fields."""

    @strawberry.field
    def users(
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[str] = None,
        last: Optional[str] = None,
    ) -> list[UserType]:
        return get_users()
