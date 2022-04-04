from ast import Call
import inspect
import base64
from math import perm
from typing import Any, Callable, Generic, Optional, TypeVar
from functools import wraps
from attr import field
import strawberry

from app.graphql.types.users import UserType
from app.db.session import session
from sqlalchemy.orm import Query
import strawberry.field
from strawberry.arguments import UNSET
GenericType = TypeVar('GenericType')


@strawberry.type
class Connection(Generic[GenericType]):
    """Represents a paginated relationship between two entities

    This pattern is used when the relationship itself has attributes.
    In a Facebook-based domain example, a friendship between two people
    would be a connection that might have a `friendshipStartTime`
    """

    page_info: 'PageInfo'
    edges: list['Edge[GenericType]']


@strawberry.type
class PageInfo:
    """Pagination context to navigate objects with cursor-based pagination

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
    """An edge may contain additional information of the relationship. This is the trivial case"""

    node: GenericType
    cursor: str

    @classmethod
    def build_cursor(cls):
        """Build base64 encoded node cursor."""
        nodeid = f'{id(cls.node)}'.encode('utf-8')
        return base64.b64encode(nodeid).decode()


# TODO: Add cursor pagination


def connection(*args, **kwargs):
    func = args[0]
    annotation = func.__annotations__.get('return')

    def wrap(before: str = None, after: str = None, last: int = None, first: int = None) -> annotation:
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return wrap


def connection_field(
    resolver=None,
    *,
    before: str = None,
    after: str = None,
    last: int = None,
    first: int = None,
    name=None,
    is_subscription=False,
    description=None,
    permission_classes=None,
    deprecation_reason=None,
    default=UNSET,
    default_factory=UNSET,
    directives=(),
    init=None,
) -> Any:

    resolver = connection(resolver)
    field_ = strawberry.field(
        resolver=resolver,
        name=name,
        is_subscription=is_subscription,
        description=description,
        permission_classes=permission_classes,
        deprecation_reason=deprecation_reason,
        default=default,
        default_factory=default_factory,
        directives=directives,
        init=init,
    )
    return field_
