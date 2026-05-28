import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as activities_data

INITIAL_ACTIVITIES = copy.deepcopy(activities_data)


@pytest.fixture(autouse=True)
def reset_activities():
    activities_data.clear()
    activities_data.update(copy.deepcopy(INITIAL_ACTIVITIES))
    yield


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
