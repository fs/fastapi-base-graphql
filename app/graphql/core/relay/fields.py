
from typing import Any, Callable, Generic, Optional, TypeVar
from functools import wraps
import strawberry
from strawberry.arguments import UNSET


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
