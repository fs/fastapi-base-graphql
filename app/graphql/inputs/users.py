import strawberry

from app.schemas import UserCreate, UserUpdate


@strawberry.experimental.pydantic.input(model=UserCreate, all_fields=True)
class CreateUserInput:
    """Create user input."""


@strawberry.experimental.pydantic.input(model=UserUpdate, all_fields=True)
class UpdateUserInput:
    """Update user fields mutation input."""
