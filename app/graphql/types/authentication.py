import strawberry
from app.graphql.types.users import UserType


@strawberry.type
class TokenPairType:
    access_token: str
    refresh_token: str
    me: UserType


@strawberry.type
class SignOutType:
    message: str
