import inflection
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """Base db model class."""

    id: int = Column(Integer, primary_key=True, index=True)
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        """Generate __tablename__ automatically."""
        if cls.__name__[-1] == 'y':
            name = cls.__name__[:-1] + 'ies'
            return inflection.underscore(name)
        return inflection.underscore(cls.__name__) + 's'
