import strawberry


def strawberry_type(cls, **kwargs):
    """Add docs as a description for strawberry type."""

    def wrapper(cls):  # noqa: WPS442
        cls_docs = cls.__doc__
        if cls_docs:
            kwargs.update(description=cls_docs)

        return strawberry.type(cls, **kwargs)

    return wrapper(cls)
