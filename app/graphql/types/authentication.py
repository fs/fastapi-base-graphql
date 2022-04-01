import strawberry


@strawberry.type
class TokenPairType:
    access_token: str
    refresh_token: str


@strawberry.type
class SignOutType:
    message: str
