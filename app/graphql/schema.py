import strawberry
from strawberry.fastapi import GraphQLRouter

import app.graphql.mutations.authentication
import app.graphql.mutations.users
import app.graphql.mutations.aws
import app.graphql.queries.users
from app.core.extensions import CurrentUserExtension


@strawberry.type
class Query(
    app.graphql.queries.users.Query,
):
    """Main query type class."""


@strawberry.type
class Mutation(
    app.graphql.mutations.authentication.Mutation,
    app.graphql.mutations.users.Mutation,
    app.graphql.mutations.aws.Mutation,
):
    """Main mutation type class."""


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[CurrentUserExtension],
)

graphql_app = GraphQLRouter(schema)
