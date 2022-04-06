import base64
from typing import Generic, Optional, TypeVar

import strawberry

GenericType = TypeVar('GenericType')


@strawberry.type
class Connection(Generic[GenericType]):
    """Represents a paginated relationship between two entities.

    This pattern is used when the relationship itself has attributes.
    In a Facebook-based domain example, a friendship between two people
    would be a connection that might have a `friendshipStartTime`
    """

    page_info: 'PageInfo'
    edges: list['Edge[GenericType]']


@strawberry.type
class PageInfo:
    """Pagination context to navigate objects with cursor-based pagination.

    Instead of classic offset pagination via `page` and `limit` parameters,
    here we have a cursor of the last object and we fetch items starting from that one

    Read more at:
        - https://graphql.org/learn/pagination/#pagination-and-edges
        - https://relay.dev/graphql/connections.htm
    """

    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]


@strawberry.type
class Edge(Generic[GenericType]):
    """An edge may contain additional information of the relationship. This is the trivial case."""

    node: GenericType
    cursor: str

    @classmethod
    def build_cursor(cls):
        """Build base64 encoded node cursor."""
        node_instance_address = id(cls.node)
        nodeid = f'{node_instance_address}'.encode('utf-8')
        return base64.b64encode(nodeid).decode()


# TODO: Add cursor pagination
