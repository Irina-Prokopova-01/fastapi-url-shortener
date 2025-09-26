import logging
from typing import Annotated
from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
    Depends,
)
from fastapi.responses import RedirectResponse
from core import config

from api import router as api_router
from api.redirect_views import router as redirect_views

from schemas.short_url import ShortUrl

logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)
app = FastAPI(
    title="URL Shortener",
)

app.include_router(redirect_views)
app.include_router(api_router)


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "massage": "Hello {name}",
        "docs": str(docs_url),
    }
