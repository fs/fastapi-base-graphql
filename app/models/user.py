from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    """User db schema."""

    full_name: str = Column(String, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    password: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean(), default=True)

    refresh_tokens = relationship('RefreshToken', back_populates='user')
