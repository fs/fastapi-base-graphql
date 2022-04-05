from pydantic import ConfigError
import strawberry
from typing import Optional
from app.db.session import session
from app.graphql.types.users import UserType
from app.models import User
from app.graphql.core.relay.node import connection, connection_field, Connection


def get_users():
    """Get all users."""
    return session.query(User)


@strawberry.type
class Query:
    """User query fields."""

    users: Connection[UserType] = connection_field(resolver=get_users)
