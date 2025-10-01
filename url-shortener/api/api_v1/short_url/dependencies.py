import logging

from fastapi import (
    HTTPException,
    status,
    BackgroundTasks,
)

# from api.api_v1.short_url.views import SHORT_URLS
from schemas.short_url import ShortUrl
from .crud import storage

log = logging.getLogger(__name__)


def prefetch_short_url(
    slug: str,
) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found.",
    )


def save_storage_state(
    background_tasks: BackgroundTasks,
):
    # код выполняемый до
    log.info("first time inside dependency save_storage_state")
    yield
    # код выполняемый после покидания view функции
    log.info("Add BackgroundTasks to save_storage")
    background_tasks.add_task(storage.save_state)
