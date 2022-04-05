from re import fullmatch
from typing import Optional

import strawberry
from app.graphql.core.types import BaseType
from app.models.user import User as UserModel


@strawberry.type
class User(BaseType):
    """Common user type."""

    id: int
    full_name: Optional[str]
    email: str
    is_active: Optional[bool]
    is_superuser: bool

    class Meta:
        model = UserModel
        exclude_fields = ('password',)
