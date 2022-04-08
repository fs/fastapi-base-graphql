from functools import partial
from typing import Callable, Optional, TypeVar

import strawberry

__all__ = ['strawberry_type', 'strawberry_pydantic_input', 'strawberry_pydantic_interface']


def docs_type_wrapper(cls=None, type_func: Optional[Callable] = strawberry.type, is_pydantic=False, **kwargs):
    """Add docs as a description for any types as strawberry.type, pydantic.type."""

    def wrapper(cls_):  # noqa: WPS442
        cls_docs = cls_.__doc__
        if cls_docs:
            kwargs.update(description=cls_docs)

        if is_pydantic:
            return type_func(**kwargs)(cls_)

        return type_func(cls, **kwargs)

    if cls:
        return wrapper(cls)

    return wrapper


# default strawberry type
strawberry_type = docs_type_wrapper

# default strawberry input
strawberry_input = partial(
    docs_type_wrapper,
    type_func=strawberry.type,
    is_input=True,
)

# experimental strawberry pydantic type
strawberry_pydantic_type = partial(
    docs_type_wrapper,
    type_func=strawberry.experimental.pydantic.type,
    is_pydantic=True,
)

# experimental strawberry pydantic input type
strawberry_pydantic_input = partial(
    docs_type_wrapper,
    is_input=True,
    type_func=strawberry.experimental.pydantic.type,
    is_pydantic=True,
)

# experimental strawberry pydantic interface type
strawberry_pydantic_interface = partial(
    docs_type_wrapper,
    is_interface=True,
    type_func=strawberry.experimental.pydantic.type,
    is_pydantic=True,
)
