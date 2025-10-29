from fastapi import (
    APIRouter,
    HTTPException,
    status,
)
from fastapi.params import Depends

from api.api_v1.short_url.crud import ShortUrlAlreadyExists, storage
from api.api_v1.short_url.dependencies import (
    # save_storage_state,
    # user_basic_auth_required_for_unsafe_methods,
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)
from schemas.short_url import ShortUrl, ShortUrlCreate, ShortUrlRead

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
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "A short url already exists.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Sort URL with slug='name' already exists.",
                    },
                },
            },
        },
    },
)
def create_short_url(
    short_url_create: ShortUrlCreate,
    # _=Depends(api_token_required)
) -> ShortUrl:
    try:
        return storage.create_or_raise_if_exists(short_url_create)
    except ShortUrlAlreadyExists:
        # if not storage.get_by_slug(short_url_create.slug):
        #     return storage.create(short_url_create)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Short URL with slug={short_url_create.slug!r} already exists",
        )
