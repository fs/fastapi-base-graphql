import strawberry
from fastapi import Depends
from starlette.requests import Request
from strawberry.fastapi import BaseContext, GraphQLRouter

import app.graphql.mutations.authentication
import app.graphql.queries.users
from app.core import extensions


@strawberry.type
class Query(
    app.graphql.queries.users.Query,
):
    """Main query type class."""


@strawberry.type
class Mutation(
    app.graphql.mutations.authentication.Mutation,
):
    """Main mutation type class."""


class CustomContext(BaseContext):
    """Customer context for link current authenticated session params."""

    def __init__(self, request: Request):
        """Init current authenticated user and token."""
        super().__init__()
        if request:
            self.current_user = extensions.current_user(request)
            self.authenticated = extensions.authenticated(request)
            self.access_token = extensions.access_token(request)


def custom_context_dependency(request: Request = None) -> CustomContext:
    """Wrap function for context instance."""
    return CustomContext(request)


async def get_context(
    custom_context=Depends(custom_context_dependency),
):
    """Define custom context dependency."""
    return custom_context


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
)
