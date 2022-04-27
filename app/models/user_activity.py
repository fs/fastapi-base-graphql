import enum
from datetime import datetime

from sqlalchemy import Column, Enum, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserActivityTypeEnum(enum.Enum):
    USER_LOGGED_IN = 'USER_LOGGED_IN'
    USER_REGISTERED = 'USER_REGISTERED'
    USER_RESET_PASSWORD = 'USER_RESET_PASSWORD'
    RESET_PASSWORD_REQUESTED = 'RESET_PASSWORD_REQUESTED'
    USER_UPDATED = 'USER_UPDATED'


class UserActivity(Base):
    event = Column(Enum(UserActivityTypeEnum))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship('User', back_populates='activities')
