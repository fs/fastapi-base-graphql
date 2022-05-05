from app.core.config import settings
from databases import Database


database = Database(settings.SQLALCHEMY_DATABASE_URI)
