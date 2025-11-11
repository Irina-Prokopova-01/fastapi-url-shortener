import random
import string
from collections.abc import Generator
from os import getenv

import pytest
from starlette.testclient import TestClient

from api.api_v1.short_url.crud import storage
from schemas.short_url import ShortUrlCreate, ShortUrl

if getenv("TESTING") != "1":
    pytest.exit(
        "Environment is not ready for pytest testing",
    )


def create_short_url() -> ShortUrl:
    short_url_in = ShortUrlCreate(
        slug="".join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=8,
            ),
        ),
        description="A short url",
        target_url="https://example.com",
    )
    return storage.create(short_url_in)


@pytest.fixture()
def short_url() -> Generator[ShortUrl]:
    short_url = create_short_url()
    # print("Created short url %s", short_url.slug)
    yield short_url
    storage.delete(short_url)
    # 1/0
    # print("Deleted short url %s", short_url.slug)
