from app.schemas import user
from app.graphql.core.type import strawberry_pydantic_input


@strawberry_pydantic_input(model=user.UserUpdate, all_fields=True)
class UpdateUserInput:
    """Update user fields."""
