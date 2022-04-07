from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.main import app


@pytest.fixture(scope='session')
def db() -> Generator:
    """Get SQLA session."""
    yield SessionLocal()


@pytest.fixture(scope='module')
def client() -> Generator:
    """Client for functional tests."""
    with TestClient(app) as c:
        yield c
