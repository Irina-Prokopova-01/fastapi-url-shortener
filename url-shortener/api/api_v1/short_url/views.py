from typing import Annotated

from fastapi import (
    HTTPException,
    status,
    Depends,
    APIRouter,
)

from api.api_v1.short_url.crud import SHORT_URLS
from api.api_v1.short_url.dependencies import prefetch_short_url
from schemas.short_url import ShortUrlCreate, ShortUrl

router = APIRouter(
    prefix="/short_url",
    tags=["Short URLs"],
)


@router.get("/", response_model=list[ShortUrl])
def read_short_urls_list():
    return SHORT_URLS


@router.post(
    "/",
    response_model=ShortUrlCreate,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_create: ShortUrlCreate,
) -> ShortUrlCreate:
    return ShortUrlCreate(
        **short_url_create.model_dump(),
        # target_url=short_url_create.target_url, slug=short_url_create.slug
    )


@router.get("/{slug}", response_model=ShortUrl)
def read_short_url_detail(url: Annotated[ShortUrl, Depends(prefetch_short_url)]):
    return url
