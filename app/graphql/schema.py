import asyncio

import strawberry
from strawberry.fastapi import GraphQLRouter, BaseContext
from starlette.requests import Request

import app.graphql.queries.users
import app.graphql.mutations.authentication
from app.core.extensions import current_user, authenticated, access_token
from fastapi import Depends


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
    def __init__(self, request: Request):
        super().__init__()
        if request:
            self.current_user = asyncio.run(current_user(request))
            self.authenticated = asyncio.run(authenticated(request))
            self.access_token = access_token(request)


def custom_context_dependency(request: Request = None) -> CustomContext:
    return CustomContext(request)


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
