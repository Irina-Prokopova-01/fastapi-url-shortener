from fastapi import (
    status,
    APIRouter,
    BackgroundTasks,
)
from fastapi.params import Depends

from api.api_v1.short_url.crud import storage
from api.api_v1.short_url.dependencies import save_storage_state
from schemas.short_url import ShortUrlCreate, ShortUrl, ShortUrlRead

router = APIRouter(
    prefix="/short_url",
    tags=["Short URLs"],
    dependencies=[Depends(save_storage_state)],
)


@router.get(
    "/",
    response_model=list[ShortUrlRead],
)
def read_short_urls_list() -> list[ShortUrl]:
    return storage.get()


@router.post(
    "/",
    response_model=ShortUrlRead,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_create: ShortUrlCreate,
) -> ShortUrl:
    return storage.create(short_url_create)
