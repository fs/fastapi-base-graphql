from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

from app.db.base import Base
from app.db.session import database

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base CRUD class."""

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, obj_id: Any) -> Optional[ModelType]:
        """Get object by id."""
        query = select(self.model).filter_by(id=obj_id)
        result = await database.fetch_one(query=query)
        return self.model(**result)

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        """Get queryset of objects."""
        query = select(self.model).offset(skip).limit(limit)
        result = await database.fetch_all(query=query)
        return [self.model(instance) for instance in result]

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        """Create new object."""
        values = obj_in.dict()
        instance = self.model(**values)
        query = insert(self.model).values(**values)
        instance.id = await database.execute(query=query)
        return instance

    async def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """Update object."""
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        query = update(self.model).filter_by(id=db_obj.id).values(**update_data)
        return await database.execute(query=query)

    async def remove(self, *, obj_id: int) -> ModelType:
        """Remove object by id."""
        query = delete(self.model).filter_by(id=obj_id)
        return await database.execute(query=query)
