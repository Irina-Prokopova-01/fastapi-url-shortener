from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.responses import RedirectResponse

from api.api_v1.short_url.dependencies import prefetch_short_url
from schemas.short_url import ShortUrl

router = APIRouter(
    prefix="/r",
    tags=["Redirect"],
)


@router.get("/{slug}/")
@router.get("/{slug}")
def redirect_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_url),
    ],
) -> RedirectResponse:
    return RedirectResponse(
        url=str(url.target_url),
    )
