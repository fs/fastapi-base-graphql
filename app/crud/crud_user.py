from typing import Any, Dict, Optional, Union
from sqlalchemy import select, insert, update
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.db.session import database
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy.future import select


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """User CRUD class."""

    async def get_by_email(self, *, email: str) -> Optional[User]:
        """Get user by email equality."""
        query = select(User).filter_by(email=email)
        result = await database.fetch_one(query)
        return User(**result) if result else None

    async def create(self, obj_in: UserCreate) -> User:
        """Create new user."""
        obj_in.password = get_password_hash(obj_in.password)
        values = obj_in.dict()
        instance = User(**values)
        query = insert(User).values(**values)
        instance.id = await database.execute(query)
        return instance

    async def update(
        self, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """Update user instance fields."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data['password']:
            hashed_password = get_password_hash(update_data['password'])
            update_data.pop('password')
            update_data['hashed_password'] = hashed_password
        query = update(User).filter_by(id=db_obj.id).values(obj_in.dict(exclude_none=True)).returning(User)
        result = await database.fetch_one(query=query)
        return User(**result)

    async def authenticate(self, *, email: str, password: str) -> Optional[User]:
        """Find user by email and check password."""
        user = await self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """User activity attr."""
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        """User admin permissions attr."""
        return user.is_superuser


user = CRUDUser(User)
