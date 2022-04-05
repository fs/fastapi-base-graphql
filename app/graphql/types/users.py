from re import fullmatch
from typing import Optional

import strawberry
from app.graphql.core.types import BaseType
from app.models.user import User


@strawberry.type
class UserType(BaseType):
    """Common user type."""

    id: int
    full_name: Optional[str]
    email: str
    is_active: Optional[bool]
    is_superuser: bool

    class Meta:
        model = User
        exclude_fields = ('password',)
