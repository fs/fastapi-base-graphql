import strawberry
from app.schemas.user import UserUpdate
from app.graphql.core.type import strawberry_pydantic_input


@strawberry_pydantic_input(model=UserUpdate, all_fields=True)
class UpdateUserInput:
    """Update user fields."""
