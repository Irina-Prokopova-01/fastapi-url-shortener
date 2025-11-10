from unittest import TestCase

from pydantic import ValidationError
from typing_extensions import Annotated

from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlPartialUpdate,
    ShortUrlUpdate,
)


class ShortUrlCreateTestCase(TestCase):
    def test_short_url_can_be_created_from_create_schemas(self) -> None:
        short_url_in = ShortUrlCreate(
            description="some_description",
            slug="some_slug",
            target_url="https://example.com",
        )
        short_url = ShortUrl(
            **short_url_in.model_dump(),
        )
        self.assertEqual(
            short_url.target_url,
            short_url_in.target_url,
        )
        self.assertEqual(
            short_url.slug,
            short_url_in.slug,
        )
        self.assertEqual(
            short_url.description,
            short_url_in.description,
        )

    def test_short_url_can_be_update_from_schemas(self) -> None:
        short_url_in = ShortUrlUpdate(
            description="some_description",
            target_url="https://example.com",
        )
        short_url = ShortUrl(
            slug="some_slug",
            **short_url_in.model_dump(),
        )
        self.assertEqual(
            short_url.target_url,
            short_url_in.target_url,
        )
        self.assertEqual(
            short_url.description,
            short_url_in.description,
        )

    def test_short_url_can_be_update_partial_from_schemas(self) -> None:
        short_url_in = ShortUrlPartialUpdate(
            description="some_description",
            target_url="https://example.com",
        )
        short_url = ShortUrl(
            slug="some_slug",
            **short_url_in.model_dump(),
        )
        self.assertEqual(
            short_url.target_url,
            short_url_in.target_url,
        )
        self.assertEqual(
            short_url.description,
            short_url_in.description,
        )

    def test_short_url_create_accepts_different_urls(self) -> None:
        urls = [
            "http://example.com",
            "https://example",
            # "rtmp://video.example.com",
            # "rtmps://video.example.com",
            "http://abc.example.com",
            "https://www.example.com/foobar/",
        ]

        for url in urls:
            with self.subTest(url=url, msg=f"test-url {url}"):
                short_url_create = ShortUrlCreate(
                    slug="some_slug",
                    target_url=url,
                    description="some_description",
                )
                self.assertEqual(
                    url.rstrip("/"),
                    short_url_create.model_dump(mode="json")["target_url"].rstrip("/"),
                )

    def test_short_url_slug_to_short(self) -> None:
        with self.assertRaises(ValidationError) as exc_info:
            ShortUrlCreate(
                slug="s",
                target_url="https://example.com",
                description="some_description",
            )
        print(exc_info.exception)
        print(exc_info.exception.json())
        print(exc_info.exception.errors())
        error_details = exc_info.exception.errors()[0]
        expected_type = "string_too_short"
        self.assertEqual(expected_type, error_details["type"])

    def test_short_url_slug_to_regex(self) -> None:
        with self.assertRaisesRegex(
            ValidationError,
            expected_regex="String should have at least 3 characters",
        ):
            ShortUrlCreate(
                slug="s",
                target_url="https://example.com",
                description="some_description",
            )
