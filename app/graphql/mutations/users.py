import strawberry
from strawberry.types import Info

from app.crud import crud_user
from app.graphql import inputs
from app.graphql.types.users import UserType
def update_user(info: Info, input: inputs.UpdateUserInput) -> UserType:
    """Update user fields."""
    current_user = info.context.current_user
    user = crud_user.user.update(db_obj=current_user, obj_in=input.to_pydantic())
    return UserType.from_pydantic(user)
@strawberry.type
class Mutation:
    """User mutation fields."""

    update_user = strawberry.field(resolver=update_user)