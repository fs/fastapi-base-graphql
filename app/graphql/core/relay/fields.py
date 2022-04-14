
from typing import Any, Callable, Generic, Optional, TypeVar
from functools import wraps
import strawberry
from strawberry.arguments import UNSET
from graphql_relay import get_offset_with_default, connection_from_array_slice
from functools import partial
from app.graphql.core.relay.node import PageInfo
from graphql_relay.connection.connectiontypes import ConnectionType


def page_info_adapter(startCursor, endCursor, hasPreviousPage, hasNextPage):
    """Adapter for creating PageInfo instances"""
    return PageInfo(
        start_cursor=startCursor,
        end_cursor=endCursor,
        has_previous_page=hasPreviousPage,
        has_next_page=hasNextPage,
    )


def connection_adapter(cls, edges, pageInfo):
    """Adapter for creating Connection instances"""
    return cls(edges=edges, page_info=pageInfo)


def resolve_connection(connection, query, max_limit=None, ** kwargs):
    """Resolve connection for query instance."""
    after = kwargs.get("after")
    list_length = query.count()
    list_slice_length = (
        min(max_limit, list_length) if max_limit is not None else list_length
    )

    after = min(get_offset_with_default(
        kwargs.get("after"), -1) + 1, list_length)

    if max_limit is not None and kwargs.get("first", None) == None:
        if kwargs.get('last', None) != None:
            after = list_length - kwargs['last']
        else:
            kwargs["first"] = max_limit

    connection = connection_from_array_slice(
        query.slice[after:],
        kwargs,
        slice_start=after,
        array_length=list_length,
        array_slice_length=list_slice_length,
        connection_type=partial(connection_adapter, connection),
        edge_type=connection.Edge,
        page_info_type=page_info_adapter,
    )
    connection.iterable = query
    connection.length = list_length
    return connection


def connection(*args, **kwargs):
    func = args[0]
    annotation = func.__annotations__.get('return')
    query = annotation.get_query()

    def wrap(before: str = None, after: str = None, last: int = None, first: int = None) -> annotation:
        def wrapper(*args, **kwargs):
            return resolve_connection(connection=func, query=query)
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
