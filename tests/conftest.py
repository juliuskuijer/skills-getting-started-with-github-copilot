from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset in-memory activities so tests never leak state into each other."""
    original_state = deepcopy(app_module.activities)

    yield

    app_module.activities.clear()
    app_module.activities.update(original_state)


@pytest.fixture
def client():
    return TestClient(app_module.app)
