import strawberry

from app.schemas import UserCreate


@strawberry.experimental.pydantic.input(model=UserCreate, all_fields=True)
class CreateUserInput:
    """Create user input."""
