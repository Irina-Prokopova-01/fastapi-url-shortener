__all__ = ("storage",)

import logging
from typing import Iterable, cast

from pydantic import BaseModel

# from pygments.lexers import data
from redis import Redis

from core import config
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlPartialUpdate,
    ShortUrlUpdate,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_SHORT_URLS,
    decode_responses=True,
)


class ShortUrlBaseError(Exception):
    """
    Base exception for short url CRUD actions
    """


class ShortUrlAlreadyExists(ShortUrlBaseError):
    """
    Raised on short url creation if such slug already exists
    """


class ShortUrlStorage(BaseModel):
    """
    Это словарь, который сопоставляет "slug"
    (короткое имя URL) с объектом ShortUrl.
    Словарь инициализируется пустым словарем.
    """

    def save_short_url(self, short_url: ShortUrl) -> None:
        redis.hset(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )

    def get(self) -> list[ShortUrl]:
        return [
            ShortUrl.model_validate_json(value)
            for value in cast(
                Iterable[str], redis.hvals(name=config.REDIS_SHORT_URLS_HASH_NAME),
            )
        ]

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        if data := redis.hget(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=slug,
        ):
            assert isinstance(data, str)
            return ShortUrl.model_validate_json(data)
        return None

    def exists(
        self,
        slug: str,
    ) -> bool:
        return cast(
            bool,
            redis.hexists(
                name=config.REDIS_SHORT_URLS_HASH_NAME,
                key=slug,
            ),
        )

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url_in.model_dump(),
        )
        self.save_short_url(short_url)
        # self.slug_to_short_url[short_url.slug] = short_url
        log.info("Created short url")
        return short_url

    def create_or_raise_if_exists(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        if not self.exists(short_url_in.slug):
            return self.create(short_url_in)

        log.info("Short url can not be create")
        raise ShortUrlAlreadyExists(short_url_in.slug)

    def delete_by_slug(self, slug: str) -> None:
        # self.slug_to_short_url.pop(slug, None)
        # self.save_state()
        redis.hdel(
            config.REDIS_SHORT_URLS_HASH_NAME,
            slug,
        )
        log.info("Delete_by_slug short url")

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)
        self.save_short_url(short_url)
        # self.save_state()
        log.info("Update short url")
        return short_url

    def update_partial(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field_name, value)
        # self.save_state()
        self.save_short_url(short_url)
        log.info("Update_partial short url")
        return short_url


storage = ShortUrlStorage()

# try:
#     storage = ShortUrlStorage.from_state()
#     log.warning("Recovered data from storage file")
# except ValidationError:
#     storage = ShortUrlStorage()
#     storage.save_state()
#     log.warning("Rewritten storege file")


# def init_storage_from_state():
#     try:
#         data = ShortUrlStorage.from_state()
#     except ValidationError:
#         storage.save_state()
#         log.warning("Rewritten storege file")
#         return
#
#     # storage.slug_to_short_url = data.slug_to_short_url
#     # мы обновляем свойство на прямую и если будут новые свойства, мы хотим их тоже обновить
#     storage.slug_to_short_url.update(
#         data.slug_to_short_url,
#     )
#     log.warning("Recovered data from storage file")
#

# storage = ShortUrlStorage()
#
# storage.create(
#     ShortUrlCreate(
#         target_url=AnyHttpUrl("http://example.com"),
#         slug="example",
#         description="example описание",
#     )
# )
# storage.create(
#     ShortUrlCreate(
#         target_url=AnyHttpUrl("http://google.com"),
#         slug="google",
#         description="google описание",
#     )
# )
