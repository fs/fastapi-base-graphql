from app.crud import crud_user
from app.graphql.types import users
import strawberry
from app.graphql.inputs.users import CreateUser


def create_user(input: CreateUser) -> users.User:
    """Create user mutation test resolver."""
    user = crud_user.user.get_by_email(email=input.email)
    if user:
        raise ValueError('User already created')
    user = crud_user.user.create(obj_in=user)
    return user


@strawberry.type
class Mutation:
    """User mutation fields."""

    create_user = strawberry.field(resolver=create_user)
