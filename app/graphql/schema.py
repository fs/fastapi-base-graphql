import strawberry
from strawberry.fastapi import GraphQLRouter
import app.graphql.mutations.users
import app.graphql.queries.users


@strawberry.type
class Query(
    app.graphql.queries.users.Query,
):
    """Main query type class."""


@strawberry.type
class Mutation(
    app.graphql.mutations.users.Mutation,
):
    """Main mutation type class."""


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)

graphql_app = GraphQLRouter(schema)
