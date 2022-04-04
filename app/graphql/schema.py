import strawberry
from strawberry.fastapi import GraphQLRouter, BaseContext

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
    def __init__(self):
        super().__init__()
        self.current_user = extensions.current_user(self.request)
        self.authenticated = extensions.authenticated(self.request)
        self.access_token = extensions.access_token(self.request)


def custom_context_dependency() -> CustomContext:
    return CustomContext()


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
