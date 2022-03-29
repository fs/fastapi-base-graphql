from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db import Base


class User(Base):

    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    refresh_tokens = relationship('RefreshToken', back_populates='user')
