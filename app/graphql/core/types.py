from typing import Any
import strawberry
from abc import ABC, abstractclassmethod, abstractproperty, abstractstaticmethod
from app.db.session import session
from app.db.base_class import Base
from app.models.user import User


@strawberry.type
class BaseType:
    """Base strawberry type."""

    class Meta:
        model: Any = None
        exclude_fields: Any = None

    @abstractclassmethod
    def from_instance(cls, instance: Any):
        """Init cls with instance params."""
        if not isinstance(instance, cls.Meta.model):
            raise AssertionError

        if len(cls.Meta.exclude_fields) is None:
            model_fields = cls.Meta.model.__table__column.keys()
        else:
            model_fields = cls.filtered_fields()

        fields = set(cls.__annotations__.keys()).intersection(model_fields)
        return cls(**{field_: instance.__dict__[field_] for field_ in fields})

    @abstractclassmethod
    def filtered_fields(cls) -> list([str]):
        """Get model fields without excluded ones."""
        exclude_fields = cls.Meta.exclude_fields
        model_fields = cls.model_fields()
        return [field for field in model_fields if field not in exclude_fields]

    @abstractclassmethod
    def model_fields(cls) -> list([str]):
        return cls.Meta.model.__table__.columns.keys()

    @abstractclassmethod
    def get_query(cls):
        return session.query(cls.Meta.model)
