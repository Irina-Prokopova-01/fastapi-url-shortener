from typing import Annotated

from fastapi import Depends, Request

from storage.short_urls import ShortUrlsStorage


def get_short_url_storage(
    request: Request,
) -> ShortUrlsStorage:
    return request.app.state.short_urls_storage


GetShortUrlsStorage = Annotated[ShortUrlsStorage, Depends(get_short_url_storage)]
