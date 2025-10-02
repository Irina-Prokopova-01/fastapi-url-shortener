import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    status,
    BackgroundTasks,
    Request,
    Header,
)
from fastapi.params import Depends

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from core.config import API_TOKENS

# from api.api_v1.short_url.views import SHORT_URLS
from schemas.short_url import ShortUrl
from .crud import storage

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})

statica_api_token = HTTPBearer(
    scheme_name="Static API Token",
    description="Your **Static API token** from the developer portal. [Read more](#)",
    auto_error=False,
)


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
    request: Request,
    background_tasks: BackgroundTasks,
):
    # код выполняемый до
    log.info("Incoming %r request", request.method)
    yield
    # код выполняемый после покидания view функции
    if request.method in UNSAFE_METHODS:
        log.info("Add BackgroundTasks to save_storage")
        background_tasks.add_task(storage.save_state)


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(statica_api_token),
    ] = None,
):
    log.info("Api token %s", api_token)
    if request.method not in UNSAFE_METHODS:
        return
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required.",
        )
    if api_token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )
