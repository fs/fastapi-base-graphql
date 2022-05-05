import strawberry

from app.graphql.core.type import strawberry_pydantic_type
from app.schemas import User as UserDB


@strawberry_pydantic_type(model=UserDB, fields=('id', 'email', 'full_name'))
class UserType:
    """Common user type."""
