import strawberry

from app.schemas import User as UserDB


@strawberry.experimental.pydantic.type(model=UserDB, all_fields=True)
class User:
    """Common user type."""
