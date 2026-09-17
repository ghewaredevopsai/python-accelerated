"""FastAPI dependencies. Complete - nothing to do here.

`Depends(get_store)` is how an endpoint asks for the store instead of importing a global.
Tests replace it with `app.dependency_overrides[get_store] = ...` - the Python equivalent of
constructor injection, without a container.
"""
import os
from functools import lru_cache
from pathlib import Path

from askops.store import Store

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@lru_cache(maxsize=1)
def get_store() -> Store:
    return Store.from_dir(os.environ.get("ASKOPS_DATA", DEFAULT_DATA_DIR))
