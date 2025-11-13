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


def build_short_url_create(
    slug: str,
    description: str = "A short url",
) -> ShortUrlCreate:
    return ShortUrlCreate(
        slug=slug,
        description=description,
        target_url="https://example.com",
    )


def build_short_url_create_random_slug(
    description: str = "A short url",
) -> ShortUrlCreate:
    return build_short_url_create(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
        description=description,
    )


@pytest.fixture()
def short_url() -> Generator[ShortUrl]:
    short_url = create_short_url()
    # print("Created short url %s", short_url.slug)
    yield short_url
    storage.delete(short_url)
    # 1/0
    # print("Deleted short url %s", short_url.slug)


def create_short_url(
    slug: str,
    description: str = "A short url",
) -> ShortUrl:
    short_url_in = build_short_url_create(
        slug=slug,
        description=description,
    )
    return storage.create(short_url_in)


def create_short_url_random_slug(
    description: str = "A short url",
) -> ShortUrl:
    short_url = build_short_url_create(
        description=description,
    )
    return storage.create(short_url)
