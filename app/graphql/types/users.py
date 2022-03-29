from typing import Optional
import strawberry


@strawberry.type
class User:
    """Common user type."""

    id: Optional[int]
    fullName: str
    email: Optional[str]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
