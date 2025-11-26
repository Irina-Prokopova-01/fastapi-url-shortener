from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient

from api.api_v1.short_url.crud import storage
from main import app
from schemas.short_url import DESCRIPTION_MAX_LENGTH, ShortUrl
from testing.conftest import create_short_url_random_slug

pytestmark = pytest.mark.apitest


class TestShortUrlUpdatePartial:
    @pytest.fixture()
    def short_url(self, request: SubRequest) -> Generator[ShortUrl]:
        description = request.param
        short_url = create_short_url_random_slug(
            description=description,
        )
        yield short_url
        storage.delete(short_url)

    @pytest.mark.parametrize(
        "short_url, new_description",
        [
            pytest.param(
                "some description",
                "",
                id="some-description-to-no-description",
            ),
            pytest.param(
                "",
                "some-description",
                id="no-description-to-some-description",
            ),
            pytest.param(
                "a" * DESCRIPTION_MAX_LENGTH,
                "",
                id="max-description-to-min-description",
            ),
            pytest.param(
                "",
                "a" * DESCRIPTION_MAX_LENGTH,
                id="min-description-to-max-description",
            ),
        ],
        indirect=["short_url"],
    )
    def test_update_short_url_details_partial(
        self,
        short_url: ShortUrl,
        auth_client: TestClient,
        new_description: str,
    ) -> None:
        url = app.url_path_for(
            "update_short_url_details_partial",
            slug=short_url.slug,
        )
        # new_description = short_url.description * 20
        response = auth_client.patch(
            url,
            json={"description": new_description},
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        short_url_db = storage.get_by_slug(short_url.slug)
        assert short_url_db
        assert short_url_db.description == new_description
        # assert short_url_db.description != short_url.description
