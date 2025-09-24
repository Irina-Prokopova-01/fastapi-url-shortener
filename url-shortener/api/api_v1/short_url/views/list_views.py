from fastapi import (
    status,
    APIRouter,
)

from api.api_v1.short_url.crud import storage
from schemas.short_url import ShortUrlCreate, ShortUrl

router = APIRouter(
    prefix="/short_url",
    tags=["Short URLs"],
)


@router.get(
    "/",
    response_model=list[ShortUrl],
)
def read_short_urls_list() -> list[ShortUrl]:
    return storage.get()


@router.post(
    "/",
    response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_create: ShortUrlCreate,
) -> ShortUrl:
    return storage.create(short_url_create)
