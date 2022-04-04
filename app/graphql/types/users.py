import strawberry

from app.schemas import User


@strawberry.experimental.pydantic.type(model=User, all_fields=True)
class UserType:
    """Common user type."""
