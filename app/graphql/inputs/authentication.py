import strawberry

from app.schemas import SignInUser


@strawberry.experimental.pydantic.input(model=SignInUser, all_fields=True)
class SignInInput:
    """Sign In user input"""


@strawberry.type
class SignOutInput:
    everywhere: bool