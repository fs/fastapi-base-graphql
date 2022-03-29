from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=engine)
session = scoped_session(SessionLocal)
