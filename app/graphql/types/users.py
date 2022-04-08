import strawberry

from app.graphql.core.type import strawberry_pydantic_type
from app.schemas import User as UserDB


@strawberry_pydantic_type(model=UserDB, all_fields=True)
class UserType:
    """Common user type."""
