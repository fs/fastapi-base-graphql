import strawberry
from strawberry.fastapi import GraphQLRouter, BaseContext
from starlette.requests import Request
from starlette.responses import Response

import app.graphql.mutations.users
import app.graphql.queries.users
import app.graphql.mutations.authentication
from app.core import extensions
from fastapi import Depends


@strawberry.type
class Query(
    app.graphql.queries.users.Query,
):
    """Main query type class."""


@strawberry.type
class Mutation(
    app.graphql.mutations.users.Mutation,
    app.graphql.mutations.authentication.Mutation,
):
    """Main mutation type class."""


class CustomContext(BaseContext):
    def __init__(self, request: Request, response: Response):
        super().__init__()
        if request:
            self.current_user = extensions.current_user(request)
            self.authenticated = extensions.authenticated(request)
            self.access_token = extensions.access_token(request)


def custom_context_dependency(request: Request = None, response: Response = None) -> CustomContext:
    return CustomContext(request, response)


async def get_context(
    custom_context=Depends(custom_context_dependency),
):
    return custom_context


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)
