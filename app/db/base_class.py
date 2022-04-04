from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """Base db model class."""

    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        """Generate __tablename__ automatically."""
        return cls.__name__.lower()
