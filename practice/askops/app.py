"""The ASGI application. Complete - nothing to do here.

    uvicorn askops.app:app --reload        then open http://127.0.0.1:8000  and  /docs
"""
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from askops import api, web

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-7s %(name)s: %(message)s")

app = FastAPI(title="AskOps", version="0.1.0", description="Runbooks, incidents, and a way to ask.")
app.include_router(api.router, prefix="/api")
app.include_router(web.router)
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
