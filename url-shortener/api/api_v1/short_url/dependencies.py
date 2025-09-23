from fastapi import (
    HTTPException,
    status,
)

# from api.api_v1.short_url.views import SHORT_URLS
from schemas.short_url import ShortUrl
from .crud import storage


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
