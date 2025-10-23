from fastapi import (
    status,
    APIRouter,
    BackgroundTasks,
    HTTPException,
)
from fastapi.params import Depends

from api.api_v1.short_url.crud import storage
from api.api_v1.short_url.dependencies import (
    # save_storage_state,
    # user_basic_auth_required_for_unsafe_methods,
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)
from schemas.short_url import ShortUrlCreate, ShortUrl, ShortUrlRead

router = APIRouter(
    prefix="/short_url",
    tags=["Short URLs"],
    dependencies=[
        # Depends(save_storage_state),
        # Depends(api_token_required_for_unsafe_methods),
        # Depends(user_basic_auth_required_for_unsafe_methods),
        Depends(api_token_or_user_basic_auth_required_for_unsafe_methods),
    ],
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
    # dependencies=[Depends(user_basic_auth_required)],
)
def create_short_url(
    short_url_create: ShortUrlCreate,
    # _=Depends(api_token_required)
) -> ShortUrl:
    if storage.get_by_slug(short_url_create.slug):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Short URL with slug={short_url_create.slug!r} already exists",
        )
    return storage.create(short_url_create)
