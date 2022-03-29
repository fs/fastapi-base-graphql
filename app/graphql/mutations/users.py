import strawberry

from app.crud import crud_user
from app.graphql.inputs.users import CreateUserInput
from app.graphql.types.users import UserType


def create_user(input: CreateUserInput) -> UserType:
    """Create user mutation test resolver."""
    if crud_user.user.get_by_email(email=input.email):
        raise ValueError('User already created')  # TODO: Add exception and exceptions structure
    user = crud_user.user.create(obj_in=input.to_pydantic())
    return UserType.from_pydantic(user)


@strawberry.type
class Mutation:
    """User mutation fields."""

    create_user = strawberry.field(resolver=create_user)
