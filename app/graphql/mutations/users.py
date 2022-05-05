from typing import Optional

import strawberry
from strawberry.types import Info

from app.core.permissions import IsAuthenticated
from app.crud import crud_user
from app.graphql.inputs.users import UpdateUserInput
from app.graphql.types.users import UserType
from app.graphql.core.type import strawberry_type


async def user_update(input: UpdateUserInput, info: Info) -> Optional[UserType]:
    """Destroy session or all sessions for user."""
    current_user = info.context['request'].current_user
    updated_user = await crud_user.user.update(db_obj=current_user, obj_in=input.to_pydantic())
    return UserType.from_pydantic(updated_user)


@strawberry_type
class Mutation:
    """Base users operation mutation."""

    update_user = strawberry.field(
        resolver=user_update,
        description='Update user fields',
        permission_classes=[IsAuthenticated],
    )
