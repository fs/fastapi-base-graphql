import strawberry
from app.schemas.user import User


@strawberry.experimental.pydantic.type(model=User, all_fields=True)
class UserType:
    """ User model"""


@strawberry.type
class TokenPairType:
    access_token: str
    refresh_token: str
    me: UserType


@strawberry.type
class SignOutType:
    message: str
