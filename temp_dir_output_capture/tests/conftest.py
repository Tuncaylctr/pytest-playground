import pytest
from fastapi.testclient import TestClient

from ..src import app


@pytest.fixture(scope='session')
def client():
    """Make a test api client for testing our FastAPI app."""
    with TestClient(app) as c:
        yield c
