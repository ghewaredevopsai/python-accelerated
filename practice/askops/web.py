"""The HTML pages, served by the same app.

Mission 4: build the page from docs/web-spec.md. The tests in tests/test_m4_web.py are the spec.
"""
from pathlib import Path

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
