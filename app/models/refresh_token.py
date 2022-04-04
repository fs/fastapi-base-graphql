from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base_class import Base


class RefreshToken(Base):

    __tablename__ = 'refresh_tokens'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    jti = Column(String)
    token = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, onupdate=datetime.now)
    revoked_at = Column(DateTime, nullable=True)

    user = relationship('User', back_populates='refresh_tokens')
