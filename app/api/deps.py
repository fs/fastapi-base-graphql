from typing import Generator

from app.db.session import SessionLocal


def get_db() -> Generator:
    """Get db session generator."""
    try:  # noqa: WPS501
        yield db := SessionLocal()
    finally:
        db.close()
