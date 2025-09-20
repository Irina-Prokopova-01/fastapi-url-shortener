from typing import Annotated

from annotated_types import Len
from fastapi import (
    HTTPException,
    status,
    Depends,
    APIRouter,
    Form,
)
from fastapi.responses import RedirectResponse
from pydantic import AnyHttpUrl

from api.api_v1.short_url.crud import SHORT_URLS
from api.api_v1.short_url.dependencies import prefetch_short_url
from schemas.short_url import ShortUrl

router = APIRouter(
    prefix="/short_url",
    tags=["Short URLs"],
)


@router.get("/", response_model=list[ShortUrl])
def read_short_urls_list():
    return SHORT_URLS


@router.post(
    "/",
    response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    target_url: Annotated[AnyHttpUrl, Form()],
    slug: Annotated[str, Len(min_length=3, max_length=100), Form()],
) -> ShortUrl:
    return ShortUrl(target_url=target_url, slug=slug)


@router.get("/{slug}", response_model=ShortUrl)
def read_short_url_detail(url: Annotated[ShortUrl, Depends(prefetch_short_url)]):
    return url
