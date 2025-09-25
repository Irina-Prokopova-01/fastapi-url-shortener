from pydantic import BaseModel, AnyHttpUrl

from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)


class ShortUrlStorage(BaseModel):
    """
    Это словарь, который сопоставляет "slug"
    (короткое имя URL) с объектом ShortUrl.
    Словарь инициализируется пустым словарем.
    """

    slug_to_short_url: dict[str, ShortUrl] = {}

    def get(self) -> list[ShortUrl]:
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_to_short_url.get(slug)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url_in.model_dump(),
        )
        self.slug_to_short_url[short_url.slug] = short_url
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_short_url.pop(slug, None)

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)
        return short_url

    def update_partial(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ):
        for field_name, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field_name, value)
        return short_url


storage = ShortUrlStorage()

storage.create(
    ShortUrlCreate(
        target_url=AnyHttpUrl("http://example.com"),
        slug="example",
        description="example описание",
    )
)
storage.create(
    ShortUrlCreate(
        target_url=AnyHttpUrl("http://google.com"),
        slug="google",
        description="google описание",
    )
)
