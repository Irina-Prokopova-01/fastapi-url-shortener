from unittest import TestCase

from schemas.short_url import ShortUrl, ShortUrlCreate


class ShortUrlCreateTestCase(TestCase):
    def test_short_url_can_be_created_from_create_schemas(self):
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
