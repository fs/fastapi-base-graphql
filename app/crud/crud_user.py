from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.db.session import session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """User CRUD class."""

    def get_by_email(self, *, email: str) -> Optional[User]:
        """Get user by email equality."""
        return session.query(User).filter(User.email == email).first()

    def create(self, obj_in: UserCreate) -> User:
        """Create new user."""
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(
        self, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]],
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
        return super().update(db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """Find user by email and check password."""
        user = self.get_by_email(db, email=email)
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
