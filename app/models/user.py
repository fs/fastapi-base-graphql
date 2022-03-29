from sqlalchemy import Boolean, Column, Integer, String

from app.db.base_class import Base


class User(Base):

    __tablename__: str = 'users'

    id: int = Column(Integer, primary_key=True, index=True)
    full_name: str = Column(String, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    password: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean(), default=True)
    is_superuser: bool = Column(Boolean(), default=False)
    access_token: str = Column('accessToken', String, unique=True, index=True)
