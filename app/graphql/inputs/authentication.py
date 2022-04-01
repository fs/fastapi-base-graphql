import strawberry

from app.schemas import SignInUser


@strawberry.experimental.pydantic.input(model=SignInUser, all_fields=True)
class SignInUserInput:
    """Sign In user input"""
