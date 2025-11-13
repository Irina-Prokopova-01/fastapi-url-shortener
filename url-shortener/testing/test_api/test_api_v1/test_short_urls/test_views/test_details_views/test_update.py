from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from pydantic import AnyHttpUrl
from starlette import status
from starlette.testclient import TestClient

from api.api_v1.short_url.crud import storage
from main import app
from schemas.short_url import ShortUrl, DESCRIPTION_MAX_LENGTH, ShortUrlUpdate
from testing.conftest import short_url, create_short_url, create_short_url_random_slug
from testing.test_api.conftest import auth_client


class TestUpdate:
    @pytest.fixture
    def short_url(self, request: SubRequest) -> Generator[ShortUrl]:
        description, target_url = request.param
        short_url = create_short_url_random_slug(
            target_url=target_url,
            description=description,
        )
        yield short_url
        storage.delete(short_url)

    @pytest.mark.parametrize(
        "short_url, new_description, new_target_url",
        [
            pytest.param(
                ("some description", "https://example.com"),
                "some description",
                "https://site.com",
                id="same-description-and-new-target-url",
            ),
            pytest.param(
                ("old description", "https://www.example.com"),
                "new description",
                "https://www.qwerty.com",
                id="new-description-and-new-target-url",
            ),
            pytest.param(
                ("basic description", "https://example.com"),
                "",
                "https://basic-site-name.com",
                id="empty-description-and-new-target-url",
            ),
            pytest.param(
                ("the description", "https://example.com"),
                "a" * DESCRIPTION_MAX_LENGTH,
                "https://example.com",
                id="max-description-and-same-target-url",
            ),
        ],
        indirect=["short_url"],
    )
    def test_update_short_url_details(
        self,
        short_url: ShortUrl,
        new_target_url: str | AnyHttpUrl,
        new_description: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for(
            "update_short_url_details",
            slug=short_url.slug,
        )
        update = ShortUrlUpdate(
            description=new_description,
            target_url=new_target_url,
        )
        response = auth_client.put(
            url,
            json=update.model_dump(mode="json"),
        )
        assert response.status_code == status.HTTP_200_OK
        short_url_db = storage.get_by_slug(short_url.slug)
        assert short_url_db
        new_data = ShortUrlUpdate(**short_url_db.model_dump())
        assert new_data == update
