from typing import Optional
import strawberry


@strawberry.input
class CreateUser:
    """Create user input."""

    email: str
    password: str
    is_active: Optional[bool] = True
    full_name: Optional[str] = None
