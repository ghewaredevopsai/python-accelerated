"""Shared fixtures. Every test gets its own Store, so tests never leak state into each other."""
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@pytest.fixture
def store():
    from askops.store import Store

    return Store.from_dir(DATA_DIR)


@pytest.fixture
def client(store):
    """A TestClient whose app uses this test's own store."""
    from fastapi.testclient import TestClient

    from askops.app import app
    from askops.deps import get_store

    app.dependency_overrides[get_store] = lambda: store
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
