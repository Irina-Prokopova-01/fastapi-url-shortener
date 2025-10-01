import logging

from pydantic import BaseModel, AnyHttpUrl, ValidationError

from core.config import SHORT_URL_STORAGE_FILEPATH
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)

log = logging.getLogger(__name__)


class ShortUrlStorage(BaseModel):
    """
    Это словарь, который сопоставляет "slug"
    (короткое имя URL) с объектом ShortUrl.
    Словарь инициализируется пустым словарем.
    """

    slug_to_short_url: dict[str, ShortUrl] = {}

    def save_state(self) -> None:
        for _ in range(30_000):
            SHORT_URL_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        SHORT_URL_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        log.info(f"Saved short urls to storage file.")

    @classmethod
    def from_state(cls) -> "ShortUrlStorage":
        if not SHORT_URL_STORAGE_FILEPATH.exists():
            log.info(f"Short urls to storage file does not exist.")
            return ShortUrlStorage()
        return cls.model_validate_json(SHORT_URL_STORAGE_FILEPATH.read_text())

    def init_storage_from_state(self):
        try:
            data = ShortUrlStorage.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file")
            return

        # storage.slug_to_short_url = data.slug_to_short_url
        # мы обновляем свойство на прямую и если будут новые свойства, мы хотим их тоже обновить
        self.slug_to_short_url.update(
            data.slug_to_short_url,
        )
        log.warning("Recovered data from storage file")

    def get(self) -> list[ShortUrl]:
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_to_short_url.get(slug)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url_in.model_dump(),
        )
        self.slug_to_short_url[short_url.slug] = short_url
        log.info("Created short url")
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_short_url.pop(slug, None)
        self.save_state()

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)
        self.save_state()
        return short_url

    def update_partial(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ):
        for field_name, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field_name, value)
        self.save_state()
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
