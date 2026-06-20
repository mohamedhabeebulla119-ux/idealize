import pytest
from fastapi.testclient import TestClient
import os
import sys

# Ensure backend imports work natively
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app
from backend.cache import cache_manager

@pytest.fixture(scope="session")
def client():
    """Returns a FastAPI TestClient instance."""
    return TestClient(app)

@pytest.fixture(autouse=True)
def clear_cache_before_tests():
    """Ensure we have a clean cache state before running the suite."""
    # We clear the cache dictionary to ensure tests actually hit the fallback endpoints.
    # Note: we don't wipe the actual cache.json file to preserve user data, 
    # we just temporarily override it in memory for testing.
    original_cache = cache_manager.cache.copy()
    cache_manager.cache = {}
    yield
    # Restore cache after tests
    cache_manager.cache = original_cache
